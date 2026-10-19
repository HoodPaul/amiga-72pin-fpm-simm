#!/usr/bin/env python3
"""Compare native SIMM copper/mechanics without requiring a KiCad installation.

Supports the retained KiCad 7 A6 reference and the user's KiCad 10 PCB. Numeric
tokens use exact Decimal arithmetic; net numbers resolve to names; irrelevant
save order, object UUIDs and layer numeric IDs do not affect the comparison.
Run from any directory: python3 path/to/source/compare_copper.py
"""
import argparse
from collections import Counter
from decimal import Decimal
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+')
NUMBER = re.compile(r'^[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?$')
HISTORICAL_AUDIT = [{'revision': 'A3-4Layer',
  'native_file_sha256': 'd18ebd9610cf5aacb079e09870d238fe38a214e46122209507661d99dc60998b',
  'canonical_geometry_sha256': {'tracks': '6519b2d453000776c493c500a016da0c45c88cf0a5b0728f3b8fc6781ddbd746',
                                'vias': 'fea7d7d9dded4ad135c5e3ec61b7b95512e4b5564f14970507bf56708aa591ba',
                                'pads': 'b49ee27fdc29f588fc2c7b46d785e9c3cd22646a12db1435d393e39f0e76ae32',
                                'component_placements': '0cd271e3dd0b08700828ae588619e3e6690fbd12c831f89dcb3eb4462d4c411b',
                                'board_outline': '36b85c9c996f7a93f3f45da0c86dfd03032a34749b41b3b6e04c87a0ae294d13',
                                'zone_outlines': '17f2d0cf6f90e5a26b360fd88cddd5e77cc71f21a99a32c1e7ac3717d8c3493d',
                                'filled_zone_polygons': '48017f68de960df058d650ae189a49d54a5cc6e848e5454db44b4837a11893b2',
                                'other_copper_graphics': '4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945',
                                'copper_layer_stack': '197c9c6e72e18ca3123af7381d1ec48e579da1936d16f883e633a452f17a5389',
                                'board_thickness': '2387a9e70ebcfb1ea2a781b548ab31f719e86d13e97851f6864e09801e7450ac'},
  'counts': {'tracks': 864,
             'vias': 195,
             'pads': 336,
             'component_placements': 17,
             'board_outline': 13,
             'zone_outlines': 2,
             'filled_zone_polygons': 10,
             'other_copper_graphics': 0,
             'copper_layer_stack': 1,
             'board_thickness': 1}},
 {'revision': 'A4-Showpiece',
  'native_file_sha256': 'e07668d8e1762ac16fe11fe61163c9728c7ebff15b636b04b8963a3766476741',
  'canonical_geometry_sha256': {'tracks': '6519b2d453000776c493c500a016da0c45c88cf0a5b0728f3b8fc6781ddbd746',
                                'vias': 'fea7d7d9dded4ad135c5e3ec61b7b95512e4b5564f14970507bf56708aa591ba',
                                'pads': 'b49ee27fdc29f588fc2c7b46d785e9c3cd22646a12db1435d393e39f0e76ae32',
                                'component_placements': '0cd271e3dd0b08700828ae588619e3e6690fbd12c831f89dcb3eb4462d4c411b',
                                'board_outline': '36b85c9c996f7a93f3f45da0c86dfd03032a34749b41b3b6e04c87a0ae294d13',
                                'zone_outlines': '17f2d0cf6f90e5a26b360fd88cddd5e77cc71f21a99a32c1e7ac3717d8c3493d',
                                'filled_zone_polygons': '48017f68de960df058d650ae189a49d54a5cc6e848e5454db44b4837a11893b2',
                                'other_copper_graphics': '4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945',
                                'copper_layer_stack': '197c9c6e72e18ca3123af7381d1ec48e579da1936d16f883e633a452f17a5389',
                                'board_thickness': '2387a9e70ebcfb1ea2a781b548ab31f719e86d13e97851f6864e09801e7450ac'},
  'counts': {'tracks': 864,
             'vias': 195,
             'pads': 336,
             'component_placements': 17,
             'board_outline': 13,
             'zone_outlines': 2,
             'filled_zone_polygons': 10,
             'other_copper_graphics': 0,
             'copper_layer_stack': 1,
             'board_thickness': 1}},
 {'revision': 'A5-Showpiece',
  'native_file_sha256': '5e3c8978c20298230ecc2f4772475a2b7964594f1a03658afea0441a90998d33',
  'canonical_geometry_sha256': {'tracks': '6519b2d453000776c493c500a016da0c45c88cf0a5b0728f3b8fc6781ddbd746',
                                'vias': 'fea7d7d9dded4ad135c5e3ec61b7b95512e4b5564f14970507bf56708aa591ba',
                                'pads': 'b49ee27fdc29f588fc2c7b46d785e9c3cd22646a12db1435d393e39f0e76ae32',
                                'component_placements': '0cd271e3dd0b08700828ae588619e3e6690fbd12c831f89dcb3eb4462d4c411b',
                                'board_outline': '36b85c9c996f7a93f3f45da0c86dfd03032a34749b41b3b6e04c87a0ae294d13',
                                'zone_outlines': '17f2d0cf6f90e5a26b360fd88cddd5e77cc71f21a99a32c1e7ac3717d8c3493d',
                                'filled_zone_polygons': '48017f68de960df058d650ae189a49d54a5cc6e848e5454db44b4837a11893b2',
                                'other_copper_graphics': '4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945',
                                'copper_layer_stack': '197c9c6e72e18ca3123af7381d1ec48e579da1936d16f883e633a452f17a5389',
                                'board_thickness': '2387a9e70ebcfb1ea2a781b548ab31f719e86d13e97851f6864e09801e7450ac'},
  'counts': {'tracks': 864,
             'vias': 195,
             'pads': 336,
             'component_placements': 17,
             'board_outline': 13,
             'zone_outlines': 2,
             'filled_zone_polygons': 10,
             'other_copper_graphics': 0,
             'copper_layer_stack': 1,
             'board_thickness': 1}},
 {'revision': 'A6-Showpiece',
  'native_file_sha256': '6cfa72e0f8b486be5644dbfe0fd81b1854d0e7880b6ae8f9a5ce642dc426458b',
  'canonical_geometry_sha256': {'tracks': '6519b2d453000776c493c500a016da0c45c88cf0a5b0728f3b8fc6781ddbd746',
                                'vias': 'fea7d7d9dded4ad135c5e3ec61b7b95512e4b5564f14970507bf56708aa591ba',
                                'pads': 'b49ee27fdc29f588fc2c7b46d785e9c3cd22646a12db1435d393e39f0e76ae32',
                                'component_placements': '0cd271e3dd0b08700828ae588619e3e6690fbd12c831f89dcb3eb4462d4c411b',
                                'board_outline': '36b85c9c996f7a93f3f45da0c86dfd03032a34749b41b3b6e04c87a0ae294d13',
                                'zone_outlines': '17f2d0cf6f90e5a26b360fd88cddd5e77cc71f21a99a32c1e7ac3717d8c3493d',
                                'filled_zone_polygons': '48017f68de960df058d650ae189a49d54a5cc6e848e5454db44b4837a11893b2',
                                'other_copper_graphics': '4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945',
                                'copper_layer_stack': '197c9c6e72e18ca3123af7381d1ec48e579da1936d16f883e633a452f17a5389',
                                'board_thickness': '2387a9e70ebcfb1ea2a781b548ab31f719e86d13e97851f6864e09801e7450ac'},
  'counts': {'tracks': 864,
             'vias': 195,
             'pads': 336,
             'component_placements': 17,
             'board_outline': 13,
             'zone_outlines': 2,
             'filled_zone_polygons': 10,
             'other_copper_graphics': 0,
             'copper_layer_stack': 1,
             'board_thickness': 1}}]
# Recorded from the A3-A6 native source files before this A7 audit was packaged.


def parse(path):
    stack, result = [], None
    for match in TOKENS.finditer(Path(path).read_text(encoding="utf-8")):
        token = match.group()
        if token == "(":
            node = []
            if stack:
                stack[-1].append(node)
            else:
                result = node
            stack.append(node)
        elif token == ")":
            if not stack:
                raise ValueError("Unbalanced native S-expression")
            stack.pop()
        else:
            atom = json.loads(token, strict=False) if token.startswith('"') else Decimal(token) if NUMBER.fullmatch(token) else token
            stack[-1].append(atom)
    if stack or not result or result[0] != "kicad_pcb":
        raise ValueError("Not a complete native KiCad PCB")
    return result


def children(node, key):
    return [item for item in node if isinstance(item, list) and item and item[0] == key]


def child(node, key, default=None):
    found = children(node, key)
    return found[0] if found else default


def freeze(value):
    return tuple(freeze(item) for item in value) if isinstance(value, list) else value


def field(node, key, default=()):
    found = child(node, key)
    return freeze(found[1:]) if found else default


def position(node):
    values = list(field(node, "at", (Decimal(0), Decimal(0))))
    if len(values) == 2:
        values.append(Decimal(0))
    values[2] = (values[2] % Decimal(360) + Decimal(360)) % Decimal(360)
    return tuple(values)


def net_name(node, net_table):
    values = field(node, "net")
    if not values:
        return ""
    if isinstance(values[0], Decimal):
        return values[1] if len(values) > 1 else net_table.get(values[0], "")
    return values[0]


def reference(footprint):
    for prop in children(footprint, "property"):
        if prop[1] == "Reference":
            return prop[2]
    for text in children(footprint, "fp_text"):
        if text[1] == "reference":
            return text[2]
    raise ValueError("A pad-bearing footprint has no reference")


def reference_alias(value):
    # The uploaded project already uses PD1..PD4. This label change is not a
    # physical component movement or a copper change relative to RPD1..RPD4.
    return "PD" + value[3:] if re.fullmatch(r"RPD[1-4]", value) else value


def closed_ring(points_node):
    points = [freeze(item[1:]) for item in points_node[1:] if isinstance(item, list) and item[0] == "xy"]
    if len(points) > 1 and points[0] == points[-1]:
        points.pop()
    if not points:
        return ()
    least, candidates = min(points), []
    for ordered in (points, list(reversed(points))):
        for index, point in enumerate(ordered):
            if point == least:
                candidates.append(tuple(ordered[index:] + ordered[:index]))
    return min(candidates)


def track_record(node, nets):
    kind = node[0]
    endpoints = tuple(sorted((field(node, "start"), field(node, "end"))))
    if kind == "segment":
        return kind, endpoints, field(node, "width"), field(node, "layer"), net_name(node, nets)
    return kind, endpoints, field(node, "mid"), field(node, "width"), field(node, "layer"), net_name(node, nets)


def via_record(node, nets):
    mode = tuple(value for value in node[1:] if isinstance(value, str))
    return position(node), field(node, "size"), field(node, "drill"), tuple(sorted(field(node, "layers"))), net_name(node, nets), mode


def physical_data(path):
    native = parse(path)
    nets = {node[1]: node[2] for node in children(native, "net") if len(node) > 2}
    data = {key: Counter() for key in ("tracks", "vias", "pads", "component_placements", "board_outline", "zone_outlines", "filled_zone_polygons", "other_copper_graphics", "copper_layer_stack", "board_thickness")}
    zone_attributes = []
    for node in native:
        if not isinstance(node, list) or not node:
            continue
        kind = node[0]
        if kind in ("segment", "arc"):
            data["tracks"][track_record(node, nets)] += 1
        elif kind == "via":
            data["vias"][via_record(node, nets)] += 1
        elif kind == "footprint":
            pads = children(node, "pad")
            for graphic in node[1:]:
                if isinstance(graphic, list) and graphic and field(graphic, "layer") and str(field(graphic, "layer")[0]).endswith(".Cu"):
                    if graphic[0] not in ("pad", "layer"):
                        clean = tuple(freeze(item) for item in graphic if not (isinstance(item, list) and item and item[0] in ("uuid", "tstamp")))
                        data["other_copper_graphics"][(position(node), field(node, "layer"), clean)] += 1
            if not pads:
                continue  # Padless logos are allowed, but copper-layer graphics are audited above.
            ref = reference_alias(reference(node))
            data["component_placements"][(ref, position(node), field(node, "layer"))] += 1
            for pad in pads:
                options = tuple((key, field(pad, key)) for key in ("rect_delta", "roundrect_rratio", "chamfer_ratio", "chamfer", "solder_mask_margin", "solder_paste_margin", "solder_paste_margin_ratio") if child(pad, key))
                record = (ref, pad[1], pad[2], pad[3], position(pad), field(pad, "size"), field(pad, "drill"), tuple(sorted(field(pad, "layers"))), net_name(pad, nets), options)
                data["pads"][record] += 1
        elif field(node, "layer") == ("Edge.Cuts",):
            stroke = field(child(node, "stroke", []), "width") or field(node, "width")
            if kind == "gr_line":
                record = kind, tuple(sorted((field(node, "start"), field(node, "end")))), stroke
            elif kind == "gr_arc":
                record = kind, tuple(sorted((field(node, "start"), field(node, "end")))), field(node, "mid"), stroke
            elif kind == "gr_circle":
                centre, end = field(node, "center"), field(node, "end")
                radius_squared = sum((a-b)**2 for a, b in zip(centre, end))
                record = kind, centre, radius_squared, stroke
            else:
                raise ValueError("Unsupported mechanical outline primitive: " + kind)
            data["board_outline"][record] += 1
        elif kind.startswith("gr_") and field(node, "layer") and str(field(node, "layer")[0]).endswith(".Cu"):
            clean = tuple(freeze(item) for item in node if not (isinstance(item, list) and item and item[0] in ("uuid", "tstamp")))
            data["other_copper_graphics"][clean] += 1
        elif kind == "zone":
            name, layer = net_name(node, nets), field(node, "layer")
            for polygon in children(node, "polygon"):
                data["zone_outlines"][(name, layer, closed_ring(child(polygon, "pts", [])))] += 1
            for polygon in children(node, "filled_polygon"):
                data["filled_zone_polygons"][(name, field(polygon, "layer"), closed_ring(child(polygon, "pts", [])))] += 1
            zone_attributes.append({"net": name, "layer": layer, "filled_areas_thickness": field(node, "filled_areas_thickness"), "fill": field(node, "fill")})
    layers = child(native, "layers", [])
    copper_layers = tuple((entry[1], entry[2]) for entry in layers[1:] if isinstance(entry, list) and str(entry[1]).endswith(".Cu"))
    data["copper_layer_stack"][copper_layers] += 1
    data["board_thickness"][field(child(native, "general", []), "thickness")] += 1
    return data, zone_attributes


def serialise(value):
    if isinstance(value, Decimal):
        return "0" if value == 0 else format(value.normalize(), "f")
    if isinstance(value, (tuple, list)):
        return [serialise(item) for item in value]
    if isinstance(value, dict):
        return {key: serialise(item) for key, item in value.items()}
    return value


def encoded(value):
    return json.dumps(serialise(value), ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def category_digest(counter):
    canonical = sorted((encoded(record), count) for record, count in counter.items())
    return hashlib.sha256(encoded(canonical).encode("utf-8")).hexdigest()


def summary(path, data, attributes):
    return {"filename": Path(path).name, "native_file_sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(), "counts": {key: sum(value.values()) for key, value in data.items()}, "canonical_geometry_sha256": {key: category_digest(value) for key, value in data.items()}, "saved_zone_attributes": serialise(attributes)}


def compare(first, second):
    checks = {}
    for key in first:
        same = first[key] == second[key]
        checks[key] = {"identical": same}
        if not same:
            checks[key]["only_first"] = serialise(list((first[key] - second[key]).elements())[:8])
            checks[key]["only_second"] = serialise(list((second[key] - first[key]).elements())[:8])
    return checks


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, default=ROOT / "source" / "copper-reference-A6.kicad_pcb")
    parser.add_argument("--input", type=Path, default=ROOT / "source" / "user-silkscreen-reference.kicad_pcb")
    parser.add_argument("--board", type=Path, default=ROOT / "HY8M-SIMM.kicad_pcb")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "docs")
    args = parser.parse_args()
    paths = {"A6_reference": args.reference, "user_uploaded_PCB": args.input, "final_PCB": args.board}
    records = {key: physical_data(path) for key, path in paths.items()}
    checks = {label: compare(records[first][0], records[second][0]) for label, first, second in (("A6_vs_user_upload", "A6_reference", "user_uploaded_PCB"), ("A6_vs_final", "A6_reference", "final_PCB"), ("user_upload_vs_final", "user_uploaded_PCB", "final_PCB"))}
    passed = all(item["identical"] for check in checks.values() for item in check.values())
    history_matches = all(item["canonical_geometry_sha256"] == summary(args.reference, *records["A6_reference"])["canonical_geometry_sha256"] for item in HISTORICAL_AUDIT)
    report = {
        "result": "PASS" if passed and history_matches else "FAIL",
        "method": "Exact Decimal comparison of saved native geometry. Net IDs resolve to names; layer IDs resolve through native layer names. RPD1-RPD4 and PD1-PD4 are reference aliases. Object UUIDs, whitespace, save order, polygon starting vertices and polygon winding do not affect the result.",
        "files": {key: summary(path, *records[key]) for key, path in paths.items()},
        "comparisons": checks,
        "historical_A3_to_A6_audit": HISTORICAL_AUDIT,
        "historical_geometry_matches_retained_A6": history_matches,
        "notes": ["Silkscreen artwork, text placement, graphic logos, title blocks and padless logo footprints are intentionally outside this copper/mechanical comparison.", "The user's upload already renames RPD1-RPD4 to PD1-PD4. This changes the component references, not their pads, positions or electrical nets.", "KiCad 10 omits the old filled_areas_thickness=no field and explicitly saves island_removal_mode=0. Saved zone outlines and all filled copper polygon vertices are compared independently; the attribute snapshots are recorded for review.", "This audit compares saved native artwork. It does not refill zones, run DRC, or establish hardware operation."]
    }
    args.report_dir.mkdir(parents=True, exist_ok=True)
    (args.report_dir / "copper-comparison.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["A7 copper and mechanical preservation audit", "Result: " + report["result"], "", report["method"], ""]
    for name, entry in report["files"].items():
        counts = entry["counts"]
        lines += [name + ": " + entry["filename"], "  Native SHA-256: " + entry["native_file_sha256"], "  " + ", ".join(f"{key}={count}" for key, count in counts.items())]
    lines.append("")
    for name, check in checks.items():
        lines.append(name + ": " + ("IDENTICAL" if all(item["identical"] for item in check.values()) else "DIFFERENCES FOUND"))
        for category, entry in check.items():
            lines.append("  " + category + ": " + ("IDENTICAL" if entry["identical"] else "DIFFERENT (see JSON)"))
    lines += ["", "Historical A3-A6 source-session checks: " + ("MATCH retained A6 geometry" if history_matches else "DO NOT MATCH")]
    for item in HISTORICAL_AUDIT:
        lines.append("  " + item["revision"] + " native SHA-256: " + item["native_file_sha256"])
    lines += [""] + report["notes"] + ["", "Per-category canonical SHA-256 hashes are in copper-comparison.json."]
    (args.report_dir / "copper-comparison.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:6] + ["", "All three comparisons: " + report["result"], "Reports: " + str(args.report_dir)]))
    return 0 if report["result"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
