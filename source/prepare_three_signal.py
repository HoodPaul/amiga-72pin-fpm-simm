from pathlib import Path
import pcbnew as p,re
r=Path(__file__).resolve().parent.parent;b=p.LoadBoard(str(r/'routing/manual-base.kicad_pcb'))
for z in list(b.Zones()):
 if z.GetNetname()=='/+5V':b.Remove(z)
b.SetLayerType(p.In2_Cu,p.LT_SIGNAL)
nc=b.GetAllNetClasses()['Default'];nc.SetClearance(p.FromMM(.2));nc.SetTrackWidth(p.FromMM(.2));nc.SetViaDiameter(p.FromMM(.6));nc.SetViaDrill(p.FromMM(.3))
b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(r/'routing/three-prepared.kicad_pcb'),b)
assert p.ExportSpecctraDSN(b,str(r/'routing/three-prepared.dsn'))
s=(r/'routing/three-prepared.dsn').read_text();original=(r/'routing/prepared.dsn').read_text()
keepouts=[l for l in original.splitlines() if re.match(r'    \(keepout (key_notch_margin|hole_left_margin|hole_right_margin|top_margin|right_margin|left_margin)',l)]
assert len(keepouts)==6
s=s.replace('    (via "Via[','\n'.join(keepouts)+'\n    (via "Via[',1)
s=re.sub(r'(\(class [^(]+)(?=\(circuit)',lambda m:m[1].replace('/+5V',''),s)
e=s.index('  (wiring\n');prefix=s[:e];i=prefix.rfind('  )\n')
power='    (class A3_SUPPLY /+5V (circuit (use_via Via[0-3]_600:300_um)) (rule (width 400) (clearance 200.1)))\n'
s=prefix[:i]+power+prefix[i:]+s[e:];(r/'routing/three-prepared.dsn').write_text(s)
