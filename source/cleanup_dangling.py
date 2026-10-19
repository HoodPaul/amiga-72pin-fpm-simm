from pathlib import Path
import pcbnew as p,re,collections
r=Path(__file__).resolve().parent.parent;path=r/'HY8M-SIMM.kicad_pcb'
for iteration in range(1):
 b=p.LoadBoard(str(path));b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.WriteDRCReport(b,str(r/'docs/drc-routed.txt'),p.EDA_UNITS_MILLIMETRES,True)
 report=(r/'docs/drc-routed.txt').read_text();counts=collections.Counter(re.findall(r'^\[([^]]+)\]',report,re.M));print(iteration,dict(counts))
 assert '** Found 0 unconnected pads **' in report
 changes=[]
 for block in re.split(r'(?=^\[)',report,flags=re.M):
  if not block.startswith(('[via_dangling]','[track_dangling]')):continue
  m=re.search(r'@\(([-.\d]+) mm, ([-.\d]+) mm\): (Via|Track) \[([^]]+)\](?: on ([^,\n]+))?',block);assert m,block
  x,y=float(m[1]),float(m[2]);typ,net=m[3],m[4]
  items=[]
  for t in b.GetTracks():
   if isinstance(t,p.PCB_VIA)!=(typ=='Via') or t.GetNetname()!=net:continue
   if abs(p.ToMM(t.GetPosition().x)-x)>.0001 or abs(p.ToMM(t.GetPosition().y)-y)>.0001:continue
   if typ=='Track' and b.GetLayerName(t.GetLayer())!=m[5]:continue
   if typ=='Track':
    length=float(re.search(r'length ([-.\d]+) mm',block)[1])
    if abs(p.ToMM(t.GetLength())-length)>.0002:continue
   items.append(t)
  assert len(items)==1,(block,len(items));changes.append(items[0])
 if not changes:break
 for t in changes:b.Remove(t)
 b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(r/'routing/cleanup-candidate.kicad_pcb'),b)
 p.WriteDRCReport(b,str(r/'routing/cleanup-drc.txt'),p.EDA_UNITS_MILLIMETRES,True)
 test=(r/'routing/cleanup-drc.txt').read_text()
 assert '** Found 0 unconnected pads **' in test,'Removal breaks connection; previous saved board retained.'
 p.SaveBoard(str(path),b)

