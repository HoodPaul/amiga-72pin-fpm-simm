from pathlib import Path
import pcbnew as p,re,collections
r=Path(__file__).resolve().parent.parent;b=p.LoadBoard(str(r/'HY8M-SIMM.kicad_pcb'))
assert b.GetCopperLayerCount()==4
if not any(z.GetNetname()=='/+5V' for z in b.Zones()):
 z=p.ZONE(b);z.SetLayer(p.In2_Cu);z.SetNet(b.FindNet('/+5V'));z.SetZoneName('+5V fill around routed signals');z.SetLocalClearance(p.FromMM(.25));z.SetMinThickness(p.FromMM(.2));z.SetPadConnection(p.ZONE_CONNECTION_FULL);z.Outline().NewOutline()
 for x,y in [(105.5,86.1),(212.45,86.1),(212.45,107.65),(105.5,107.65)]:z.Outline().Append(round(x*1e6),round(y*1e6))
 b.Add(z)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(r/'HY8M-SIMM.kicad_pcb'),b)
p.WriteDRCReport(b,str(r/'docs/drc-routed.txt'),p.EDA_UNITS_MILLIMETRES,True)
s=(r/'docs/drc-routed.txt').read_text();print(collections.Counter(re.findall(r'^\[([^]]+)\]',s,re.M)));print('\n'.join(re.findall(r'^\*\* Found.*$',s,re.M)))
