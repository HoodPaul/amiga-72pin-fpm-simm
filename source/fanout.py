"""Fixed fanout and optional planned data buses for the 25.4 mm A3 SIMM.

The caller owns component placement and the schematic/PCB net assignments.
Requires KiCad's pcbnew Python module. No board is loaded or saved on import.

Expected placement (KiCad angles, not a rotation relative to the old board):
    U1 (143,97.5), F.Cu, 90 deg; U3 same XY, B.Cu, 270 deg.
    U2 (175,97.5), F.Cu, 270 deg; U4 same XY, B.Cu, 90 deg.
Rear A0..A7 assignments must be reversed externally to share those vias.
The optional bus geometry is a proposal and must pass board DRC after use.
"""
from collections import Counter
import re
import pcbnew as p


def mmvec(x, y):
    return p.VECTOR2I(p.FromMM(x), p.FromMM(y))


def xy(position):
    return (p.ToMM(position.x), p.ToMM(position.y))


def _point_key(x, y):
    return (round(x, 6), round(y, 6))


def prepare(board, cap_fanout=(0.0, 1.6), locked=True):
    """Add connector joins and chip/capacitor fanout, returning counts.

    Shared vias are deduplicated only when position AND net agree. Any via
    position occupied by a different net raises ValueError, so erroneous
    front/back mappings cannot silently become shorts.

    The signal escape direction is based on SOJ pin function rather than the
    external net name, allowing the caller to use separate RAS strap nets.
    """
    via_at = {}
    track_keys = set()
    counts = Counter()
    for item in board.GetTracks():
        if isinstance(item, p.PCB_VIA):
            key = _point_key(*xy(item.GetPosition()))
            old = via_at.get(key)
            if old is not None and old != item.GetNetCode():
                raise ValueError(f"Existing vias of different nets overlap at {key}")
            via_at[key] = item.GetNetCode()
        else:
            endpoints = sorted((_point_key(*xy(item.GetStart())),
                                _point_key(*xy(item.GetEnd()))))
            track_keys.add((item.GetLayer(), item.GetNetCode(),
                            item.GetWidth(), tuple(endpoints)))

    def add_track(start, end, layer, net, width):
        a, b = _point_key(*start), _point_key(*end)
        if a == b:
            return
        key = (layer, net, p.FromMM(width), tuple(sorted((a, b))))
        if key in track_keys:
            counts['deduplicated_tracks'] += 1
            return
        track = p.PCB_TRACK(board)
        track.SetStart(mmvec(*start))
        track.SetEnd(mmvec(*end))
        track.SetLayer(layer)
        track.SetWidth(p.FromMM(width))
        track.SetNetCode(net)
        track.SetLocked(locked)
        board.Add(track)
        track_keys.add(key)
        counts['tracks'] += 1

    def add_via(location, net):
        key = _point_key(*location)
        if key in via_at:
            if via_at[key] != net:
                old = board.FindNet(via_at[key]).GetNetname()
                new = board.FindNet(net).GetNetname()
                raise ValueError(f"Fanout via collision at {key}: {old} versus {new}")
            counts['deduplicated_vias'] += 1
            return
        via = p.PCB_VIA(board)
        via.SetPosition(mmvec(*location))
        via.SetWidth(p.FromMM(0.6))
        via.SetDrill(p.FromMM(0.3))
        via.SetViaType(p.VIATYPE_THROUGH)
        via.SetLayerPair(p.F_Cu, p.B_Cu)
        via.SetNetCode(net)
        via.SetLocked(locked)
        board.Add(via)
        via_at[key] = net
        counts['vias'] += 1

    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if ref == 'J1':
            for pad in fp.Pads():
                if pad.GetNetCode() == 0:
                    continue
                x, y = xy(pad.GetPosition())
                target = (x, 107.25)
                layer = p.F_Cu if pad.IsOnLayer(p.F_Cu) else p.B_Cu
                add_track((x, y), target, layer, pad.GetNetCode(), 0.25)
                add_via(target, pad.GetNetCode())
                counts['connector_pad_joins'] += 1
        elif ref in {'U1', 'U2', 'U3', 'U4'}:
            cy = p.ToMM(fp.GetPosition().y)
            for pad in fp.Pads():
                if pad.GetNetCode() == 0:
                    continue
                number = int(pad.GetNumber())
                x, y = xy(pad.GetPosition())
                if abs(y - cy) < 4.0:
                    raise ValueError(f'{ref}.{number}: footprint is not horizontal')
                outward = 1.0 if y > cy else -1.0
                # WE, RAS and VCC go inward; DQ, address, CAS and GND/OE
                # go outward. This prevents opposite-face WE/CAS,
                # RAS/OE and VCC/GND escapes from sharing different nets.
                inward = number in {1, 6, 13, 14, 21}
                delta = -outward if inward else outward
                target = (x, y + 1.6 * delta)
                width = 0.4 if number in {1, 6, 21, 22, 29, 37, 42} else 0.2
                add_track((x, y), target, fp.GetLayer(), pad.GetNetCode(), width)
                add_via(target, pad.GetNetCode())
                counts['chip_pad_escapes'] += 1
        elif re.fullmatch(r'C[1-4]', ref):
            for pad in fp.Pads():
                if pad.GetNetCode() == 0:
                    continue
                x, y = xy(pad.GetPosition())
                target = (x + cap_fanout[0], y + cap_fanout[1])
                add_track((x, y), target, fp.GetLayer(), pad.GetNetCode(), 0.4)
                add_via(target, pad.GetNetCode())
                counts['capacitor_pad_escapes'] += 1
    board.BuildConnectivity()
    return dict(counts)


def manual_dq_bus_plan(board):
    """Return 16 parallel data polylines for review and DRC, without mutation.

    U1 upper-row module DQ8..15 and U4 upper-row module DQ16..23 are expected
    in ascending X order. Each path finishes at an existing J1 join via.
    Board must use exactly the placement and byte mappings documented above.
    """
    fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
    definitions = [
        (range(8, 16), 'U1', p.F_Cu, lambda bit: 99.3 - 0.4 * (bit - 8)),
        (range(16, 24), 'U4', p.B_Cu, lambda bit: 96.5 + 0.4 * (bit - 16)),
    ]
    escape = {8:178.175, 9:180.715, 10:183.255, 11:185.795, 12:188.335,
              20:137.285, 21:139.825, 22:142.365, 23:144.905}
    results = []
    for bits, ref, layer, lane in definitions:
        for bit in bits:
            netname = f'/DQ{bit}'
            source = [pad for pad in fps[ref].Pads() if pad.GetNetname() == netname]
            if len(source) != 1:
                raise ValueError(f'{ref}: expected exactly one {netname} pad')
            source = source[0]
            sx, sy = xy(source.GetPosition())
            if abs(sy - 92.35) > 0.00001:
                raise ValueError(f'{ref} {netname}: expected upper pad row y92.35, got {sy}')
            targets = [pad for pad in fps['J1'].Pads()
                       if pad.GetNetname() == netname and pad.IsOnLayer(layer)]
            if len(targets) != 1:
                raise ValueError(f'J1: expected exactly one {netname} pad on layer {layer}')
            tx, _ = xy(targets[0].GetPosition())
            ex, ly = escape.get(bit, tx), round(lane(bit), 6)
            points = [(sx, sy), (sx, ly), (ex, ly), (ex, 105.6),
                      (tx, 105.6), (tx, 107.25)]
            points = [point for i, point in enumerate(points)
                      if i == 0 or point != points[i - 1]]
            results.append({'net':netname, 'net_code':source.GetNetCode(),
                            'layer':layer, 'layer_name':board.GetLayerName(layer),
                            'width_mm':0.2, 'points_mm':points})
    return results


def apply_manual_dq_buses(board, locked=True):
    """Apply proposed bus geometry; caller must perform DRC before accepting it."""
    plan = manual_dq_bus_plan(board)
    for route in plan:
        for start, end in zip(route['points_mm'], route['points_mm'][1:]):
            track = p.PCB_TRACK(board)
            track.SetStart(mmvec(*start))
            track.SetEnd(mmvec(*end))
            track.SetLayer(route['layer'])
            track.SetWidth(p.FromMM(route['width_mm']))
            track.SetNetCode(route['net_code'])
            track.SetLocked(locked)
            board.Add(track)
    board.BuildConnectivity()
    return plan
