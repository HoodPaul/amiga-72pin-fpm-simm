#!/usr/bin/env python3
"""Apply JMC to the exact user-edited KiCad10 board without reserialising copper.

The saved user-silkscreen-reference board is the authoritative artwork baseline.
No placement, routing, zone, pad or existing text position is regenerated.
"""
from pathlib import Path
import re,uuid
r=Path(__file__).resolve().parents[1]
base=r/'source/user-silkscreen-reference.kicad_pcb'
assert base.exists(),'Missing the authoritative uploaded board snapshot'
s=base.read_text()
for i in range(1,5):
 assert f'(property "Reference" "PD{i}"' in s
 assert f'(property "Reference" "RPD{i}"' not in s
s=s.replace('(rev "A6")','(rev "A7")',1)
s=s.replace('"REV A6"','"REV A7"').replace('"A6 FOUR-LAYER ROUTED DRAFT"','"A7 FOUR-LAYER ROUTED DRAFT"')
mod=(r/'HY8M.pretty/JMC_White_18mm.kicad_mod').read_text()
polys=re.findall(r'\(fp_poly \(pts (.*?)\)\s*\(stroke',mod,re.S)
assert len(polys)==76
namespace=uuid.UUID('f7d0f695-a827-493d-a1b7-329a080bc2fd')
forms=[]
for i,poly in enumerate(polys):
 coords=re.findall(r'\(xy ([^ ]+) ([^)]+)\)',poly);assert len(coords)==3
 pts=' '.join(f'(xy {202+float(x):.6f} {88.8+float(y):.6f})' for x,y in coords)
 u=uuid.uuid5(namespace,f'a7-board-logo-{i}')
 forms.append(f'\t(gr_poly\n\t\t(pts {pts})\n\t\t(stroke (width 0) (type default))\n\t\t(fill yes)\n\t\t(layer "F.SilkS")\n\t\t(uuid "{u}")\n\t)\n')
end=s.rfind(')');assert end>=0
s=s[:end]+''.join(forms)+s[end:]
(r/'HY8M-SIMM.kicad_pcb').write_text(s)
print('Added76filledJMCpolygons; preserved the uploaded board and its PD1-PD4 reference labels.')
