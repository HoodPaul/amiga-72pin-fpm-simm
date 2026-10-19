from pathlib import Path
import pcbnew as p,math,sys,shutil
r=Path(__file__).resolve().parent.parent
src=Path(sys.argv[1]) if len(sys.argv)>1 else r/'routing/manual-base.kicad_pcb'
b=p.LoadBoard(str(src));p.SaveBoard(str(r/'routing/prepared.kicad_pcb'),b)
assert p.ExportSpecctraDSN(b,str(r/'routing/prepared.dsn'))
s=(r/'routing/prepared.dsn').read_text();extra=[]
for name,cx,cy,rad in [('key_notch_margin',158.975,108.1298,1.9),('hole_left_margin',108.38,100.84,1.9),('hole_right_margin',209.4702,100.84,1.9)]:
 coords=[]
 for i in range(65):
  a=2*math.pi*i/64;coords.extend([f'{(cx+rad*math.cos(a))*1000:.3f}',f'{-(cy+rad*math.sin(a))*1000:.3f}'])
 extra.append('    (keepout '+name+' (polygon signal 0 '+' '.join(coords)+'))')
for name,points in [('top_margin',[(105,85.6),(212.95,85.6),(212.95,85.9),(105,85.9),(105,85.6)]),('right_margin',[(212.65,85.6),(212.95,85.6),(212.95,111),(212.65,111),(212.65,85.6)]),('left_margin',[(105,85.6),(105.3,85.6),(105.3,104.65),(105,104.65),(105,85.6)])]:
 extra.append('    (keepout '+name+' (polygon signal 0 '+' '.join(f'{x*1000:.3f} {-y*1000:.3f}' for x,y in points)+'))')
s=s.replace('    (via "Via[','\n'.join(extra)+'\n    (via "Via[',1);(r/'routing/prepared.dsn').write_text(s)
print('Exported',src)
