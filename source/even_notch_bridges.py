"""Symmetric45degree notch bridges; optional --front-only finishes an existing back group."""
from pathlib import Path
import pcbnew as p,math,re,collections,sys
r=Path(__file__).resolve().parent.parent;path=r/'HY8M-SIMM.kicad_pcb';b=p.LoadBoard(str(path))
centre=158.975;pitch=.4
profiles=[(name,p.B_Cu,105.55-i*pitch,1+i*pitch*(math.sqrt(2)-1)) for i,name in enumerate(['/A7','/A9','/A8'])]
profiles.append(('/A5',p.F_Cu,105.05,1.165685))
if '--front-only' in sys.argv:profiles=profiles[-1:]
for name,layer,y,half in profiles:
 matches=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA) and t.GetNetname()==name and t.GetLayer()==layer and t.GetStart().y==t.GetEnd().y and min(t.GetStart().x,t.GetEnd().x)<p.FromMM(centre)<max(t.GetStart().x,t.GetEnd().x) and p.ToMM(t.GetStart().y)>104.5]
 assert len(matches)==1,(name,len(matches));old=matches[0];net=old.GetNetCode()
 left,right=sorted([(p.ToMM(t.x),p.ToMM(t.y)) for t in [old.GetStart(),old.GetEnd()]])
 xl,xr=centre-half,centre+half;rise=left[1]-y
 if abs(rise)<.00001 and abs(left[0]-xl)<.00001 and abs(right[0]-xr)<.00001:continue
 assert rise>0,(name,'unexpected route geometry')
 points=[left,(xl-rise,left[1]),(xl,y),(xr,y),(xr+rise,right[1]),right];b.Remove(old)
 for a,z in zip(points,points[1:]):
  t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(round(a[0]*1e6),round(a[1]*1e6)));t.SetEnd(p.VECTOR2I(round(z[0]*1e6),round(z[1]*1e6)));t.SetLayer(layer);t.SetNetCode(net);t.SetWidth(p.FromMM(.2));b.Add(t)
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones())
p.WriteDRCReport(b,str(r/'routing/even-bridges-drc.txt'),p.EDA_UNITS_MILLIMETRES,True)
s=(r/'routing/even-bridges-drc.txt').read_text();counts=collections.Counter(re.findall(r'^\[([^]]+)\]',s,re.M));print(counts)
assert counts=={'copper_edge_clearance':144},'Main board retained for review.'
assert '** Found 0 unconnected pads **' in s
p.SaveBoard(str(path),b);print('Accepted symmetric front bridge and three evenly spaced back bridges')
