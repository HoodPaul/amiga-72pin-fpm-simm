#!/usr/bin/env python3
"""Import a local Freerouting SES result into the prepared KiCad board.
Retains schematic-linked footprints and power-plane polygons.
"""
from pathlib import Path
import json,re,sys,collections
import pcbnew as p
root=Path(__file__).resolve().parent.parent
session=Path(sys.argv[1]) if len(sys.argv)>1 else root/'routing/three-signal.ses'
def parse(s):
    s=s.replace('(string_quote ")','(string_quote QUOTE)')
    ts=re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+',s)
    stack=[]; result=None
    for t in ts:
        if t=='(':
            a=[]
            if stack:stack[-1].append(a)
            stack.append(a)
        elif t==')':result=stack.pop()
        else:stack[-1].append(json.loads(t) if t.startswith('"') else t)
    return result
def children(a,name):return [x for x in a if isinstance(x,list) and x and x[0]==name]
def child(a,name):return children(a,name)[0]
data=parse(session.read_text());routes=child(data,'routes');res=child(routes,'resolution')
assert res[1]=='um',res
scale=1000*float(res[2])
def pt(x,y):return p.VECTOR2I(round(float(x)/scale*1e6),round(-float(y)/scale*1e6))
base_path=Path(sys.argv[2]) if len(sys.argv)>2 else root/'routing/prepared.kicad_pcb'
base=base_path.read_text()
clean=re.sub(r'^  \((?:segment|via) (?!locked)[^\n]*\n','',base,flags=re.M)
tmp=root/'routing/import-base.kicad_pcb';tmp.write_text(clean)
board=p.LoadBoard(str(tmp));tmp.unlink()
assert all(t.IsLocked() for t in board.GetTracks())
known=set();vknown=set()
def tk(a,b,layer,net,width):return (tuple(sorted(((a.x,a.y),(b.x,b.y)))),layer,net,width)
for t in board.GetTracks():
    if isinstance(t,p.PCB_VIA):vknown.add((t.GetPosition().x,t.GetPosition().y,t.GetNetCode()))
    else:known.add(tk(t.GetStart(),t.GetEnd(),t.GetLayer(),t.GetNetCode(),t.GetWidth()))
count=collections.Counter()
for n in children(child(routes,'network_out'),'net'):
    name=n[1];net=board.FindNet(name);assert net is not None,name
    for w in children(n,'wire'):
        path=child(w,'path');layer=board.GetLayerID(path[1]);width=round(float(path[2])/scale*1e6)
        coords=path[3:];assert len(coords)%2==0
        points=[pt(coords[i],coords[i+1]) for i in range(0,len(coords),2)]
        for a,b in zip(points,points[1:]):
            key=tk(a,b,layer,net.GetNetCode(),width)
            if key in known or a==b:continue
            t=p.PCB_TRACK(board);t.SetStart(a);t.SetEnd(b);t.SetWidth(width);t.SetLayer(layer);t.SetNet(net);board.Add(t);known.add(key);count['segments']+=1
    for w in children(n,'via'):
        at=pt(w[2],w[3]);key=(at.x,at.y,net.GetNetCode())
        if key in vknown:continue
        # The only via padstack exported by prepare_route.py is 0.6/0.3 mm.
        assert '600:300' in w[1],w[1]
        z=p.PCB_VIA(board);z.SetPosition(at);z.SetWidth(p.FromMM(.6));z.SetDrill(p.FromMM(.3));z.SetViaType(p.VIATYPE_THROUGH);z.SetLayerPair(p.F_Cu,p.B_Cu);z.SetNet(net);board.Add(z);vknown.add(key);count['vias']+=1

board.BuildConnectivity();p.ZONE_FILLER(board).Fill(board.Zones())
p.SaveBoard(str(root/'HY8M-SIMM.kicad_pcb'),board)
board=p.LoadBoard(str(root/'HY8M-SIMM.kicad_pcb'))
print('Imported',dict(count),'resolution',res)
p.WriteDRCReport(board,str(root/'docs/drc-routed.txt'),p.EDA_UNITS_MILLIMETRES,True)
report=(root/'docs/drc-routed.txt').read_text()
print(collections.Counter(re.findall(r'^\[([^]]+)\]',report,re.M)))
print('\n'.join(re.findall(r'^\*\* Found.*$',report,re.M)))
