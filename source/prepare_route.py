#!/usr/bin/env python3
"""Prepare deterministic fanout for the A3 four-layer SIMM."""
from pathlib import Path
import sys,json,re,math,collections
import pcbnew as p
import fanout
r=Path(__file__).resolve().parent.parent
b=p.LoadBoard(str(r/'HY8M-SIMM.kicad_pcb'))
assert len(list(b.GetTracks()))==0
b.SetLayerType(p.In1_Cu,p.LT_POWER);b.SetLayerType(p.In2_Cu,p.LT_POWER)
ds=b.GetDesignSettings();ds.m_MinClearance=p.FromMM(.2);ds.m_TrackMinWidth=p.FromMM(.2);ds.m_CopperEdgeClearance=p.FromMM(.5)
nc=b.GetAllNetClasses()['Default'];nc.SetClearance(p.FromMM(.2));nc.SetTrackWidth(p.FromMM(.2));nc.SetViaDiameter(p.FromMM(.6));nc.SetViaDrill(p.FromMM(.3))
print('Fanout',fanout.prepare(b))
def vec(x,y):return p.VECTOR2I(round(x*1e6),round(y*1e6))
for fp in b.GetFootprints():
 if fp.GetReference().startswith('R'):
  for pad in fp.Pads():
   pos=pad.GetPosition();x,y=p.ToMM(pos.x),p.ToMM(pos.y);end=vec(x,y-1)
   t=p.PCB_TRACK(b);t.SetStart(pos);t.SetEnd(end);t.SetLayer(p.F_Cu);t.SetWidth(p.FromMM(.2));t.SetNet(pad.GetNet());t.SetLocked(True);b.Add(t)
   z=p.PCB_VIA(b);z.SetPosition(end);z.SetWidth(p.FromMM(.6));z.SetDrill(p.FromMM(.3));z.SetViaType(p.VIATYPE_THROUGH);z.SetLayerPair(p.F_Cu,p.B_Cu);z.SetNet(pad.GetNet());z.SetLocked(True);b.Add(z)
for layer,name in [(p.In1_Cu,'/GND'),(p.In2_Cu,'/+5V')]:
 z=p.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet(name));z.SetZoneName(name+' plane');z.SetLocalClearance(p.FromMM(.25));z.SetMinThickness(p.FromMM(.2));z.SetPadConnection(p.ZONE_CONNECTION_FULL);z.Outline().NewOutline()
 for x,y in [(105.5,86.1),(212.45,86.1),(212.45,107.65),(105.5,107.65)]:z.Outline().Append(round(x*1e6),round(y*1e6))
 b.Add(z)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(r/'routing/fanout-base.kicad_pcb'),b)
p.WriteDRCReport(b,str(r/'routing/drc-fanout.txt'),p.EDA_UNITS_MILLIMETRES,True)
report=(r/'routing/drc-fanout.txt').read_text();print(collections.Counter(re.findall(r'^\[([^]]+)\]',report,re.M)))
# Save the optional planned buses separately so the base is never silently changed.
try:
 plan=fanout.apply_manual_dq_buses(b);(r/'routing/manual-buses.json').write_text(json.dumps(plan,indent=2));p.SaveBoard(str(r/'routing/manual-base.kicad_pcb'),b)
 p.WriteDRCReport(b,str(r/'routing/drc-manual.txt'),p.EDA_UNITS_MILLIMETRES,True)
 report=(r/'routing/drc-manual.txt').read_text();print('Manual',collections.Counter(re.findall(r'^\[([^]]+)\]',report,re.M)))
except Exception as e:print('Manual candidate error',e)
