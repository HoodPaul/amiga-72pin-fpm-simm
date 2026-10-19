#!/usr/bin/env python3
"""Create population BOMs and DNP-marked schematics for the common A7 PCB."""
from pathlib import Path
import json,re,csv,shutil
r=Path(__file__).resolve().parent.parent
base=(r/'HY8M-SIMM.kicad_sch').read_text()
all_refs={f'U{i}' for i in range(1,5)}|{f'C{i}' for i in range(1,5)}|{f'R{i}' for i in range(1,5)}|{f'PD{i}' for i in range(1,5)}
variants={}
for size in [4,8]:
 for speed in [60,70]:
  tag=f'{size}MB-{speed}ns';fitted={'U1','U2','C1','C2'}
  if size==8:fitted|={'U3','U4','C3','C4','R1','R2','R3','R4'}
  pd=[size==4,size==4,speed==70,False]
  fitted|={f'PD{i+1}' for i,on in enumerate(pd) if on}
  variants[tag]={'capacity_mib':size,'speed_ns':speed,'dram_mpn':'HY5118160BJC-60' if speed==60 else 'HY5118160JC-70','fitted':sorted(fitted),'dnp':sorted(all_refs-fitted),'pd_grounded':pd,'rear_enabled':size==8}
def blocks(s):
 for m in re.finditer(r'^\(symbol \(lib_id ',s,re.M):
  i=m.start();depth=0;quoted=False;escape=False
  for j in range(i,len(s)):
   c=s[j]
   if quoted:
    if escape:escape=False
    elif c=='\\':escape=True
    elif c=='"':quoted=False
   elif c=='"':quoted=True
   elif c=='(':depth+=1
   elif c==')':
    depth-=1
    if depth==0:yield i,j+1,s[i:j+1];break
def make_schematic(v):
 s=base
 for a,z,b in reversed(list(blocks(base))):
  ref=re.search(r'\(property "Reference" "([^"]+)"',b)[1]
  dnp=ref in v['dnp'];b=re.sub(r'\(dnp (?:yes|no)\)',f'(dnp {"yes" if dnp else "no"})',b,count=1)
  if ref.startswith('U'):
   b=re.sub(r'(\(property "Value" )"[^"]+"',lambda m:m[1]+json.dumps(v['dram_mpn']),b,count=1)
  elif ref=='J1':
   value=f'72-pin / {v["capacity_mib"]} MB / {v["speed_ns"]} ns FPM'
   b=re.sub(r'(\(property "Value" )"[^"]+"',lambda m:m[1]+json.dumps(value),b,count=1)
  s=s[:a]+b+s[z:]
 s=re.sub(r'(\(title )"[^"]+"',lambda m:m[1]+json.dumps(f'HY8M | {v["capacity_mib"]} MB {v["speed_ns"]} ns | ASSEMBLY DRAFT'),s,count=1)
 s=re.sub(r'(\(comment 1 )"[^"]+"',lambda m:m[1]+json.dumps(f'{v["dram_mpn"]} x{2 if v["capacity_mib"]==4 else 4} / 5 V / {v["capacity_mib"]} MB populated'),s,count=1)
 return s
(r/'docs/assembly-variants.json').write_text(json.dumps(variants,indent=2)+'\n')
notes={
 'U':'42-pin 400 mil SOJ; 5 V; 1Mx16; FPM; 1K refresh. Readable exact donor marking required.',
 'C':'220 nF; 0805; 16 V or higher; X7R; +/-10%; fit new capacitors.',
 'R1':'0 ohm rear low-halfword RAS enable. Fit with R2 for 8 MB.',
 'R2':'0 ohm rear high-halfword RAS enable. Fit with R1 for 8 MB.',
 'R3':'10 kohm rear low-halfword RAS pull-up to +5 V.',
 'R4':'10 kohm rear high-halfword RAS pull-up to +5 V.',
 'PD':'0 ohm link from PD pin to GND. Unfitted means electrically open.'}
def part(ref,v):
 if ref[0]=='U':return v['dram_mpn'],'SOJ42 400 mil',notes['U']
 if ref[0]=='C':return '220 nF','0805',notes['C']
 if ref.startswith('PD'):return '0 ohm','0603',notes['PD']
 return ('0 ohm' if ref in ['R1','R2'] else '10 kohm'),'0603',notes[ref]
for tag,v in variants.items():
 d=r/'variants'/tag;d.mkdir(parents=True,exist_ok=True)
 sch=make_schematic(v);(d/'HY8M-SIMM.kicad_sch').write_text(sch)
 (d/'sym-lib-table').write_text('(sym_lib_table (lib (name "HY8M")(type "KiCad")(uri "${KIPRJMOD}/../../HY8M.kicad_sym")(options "")(descr "Shared project symbols")))\n')
 (d/'fp-lib-table').write_text('(fp_lib_table (lib (name "HY8M")(type "KiCad")(uri "${KIPRJMOD}/../../HY8M.pretty")(options "")(descr "Shared project footprints")))\n')
 with (d/'BOM.csv').open('w',newline='') as f:
  w=csv.writer(f);w.writerow(['Reference','Quantity','Value_or_MPN','Package','Notes'])
  w.writerow(['PCB',1,'HY8M A7 common PCB','72-pin SIMM','107.95 x 25.4 mm; four layers; 1.2 mm proposed; fabrication review pending'])
  for ref in v['fitted']:w.writerow([ref,1,*part(ref,v)])
 (d/'README.md').write_text(f'''# {tag} assembly

Use the common routed PCB at `../../HY8M-SIMM.kicad_pcb`.
This schematic marks the unfitted components with KiCad DNP flags.
Use this folder's BOM. There is no separate PCB geometry for this assembly.

Fit: {', '.join(v['fitted'])}.

Leave unfitted: {', '.join(v['dnp'])}.

The {v['capacity_mib']} MB build uses {len([x for x in v['fitted'] if x.startswith('U')])} {v['dram_mpn']} devices.
Physical fit, donor health, timing and A4000 operation remain untested.
''')
# Main project is the 8MB/70ns assembly; all four configurations share its copper.
(r/'HY8M-SIMM.kicad_sch').write_text(make_schematic(variants['8MB-70ns']))
with (r/'BOM.csv').open('w',newline='') as f:
 w=csv.writer(f);tags=list(variants);w.writerow(['Reference','70ns_value','60ns_value','Package',*tags,'Notes'])
 w.writerow(['PCB','HY8M A7','HY8M A7','72-pin SIMM',*[1]*4,'Common four-layer 107.95 x 25.4 mm board; proposed 1.2 mm thickness'])
 for ref in sorted(all_refs):
  a,p,n=part(ref,variants['8MB-70ns']);b,_,_=part(ref,variants['8MB-60ns'])
  w.writerow([ref,a,b,p,*[int(ref in variants[tag]['fitted']) for tag in tags],n])
with (r/'assembly-options.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Build','DRAM_MPN','Front_chips','Rear_chips','R1_R2','R3_R4','PD1','PD2','PD3','PD4','Intended_use'])
 for tag,v in variants.items():w.writerow([tag,v['dram_mpn'],'U1 U2','U3 U4' if v['rear_enabled'] else 'DNP','0 ohm' if v['rear_enabled'] else 'DNP','10 kohm' if v['rear_enabled'] else 'DNP',*['0 ohm' if on else 'DNP' for on in v['pd_grounded']], 'Fast RAM one rank' if v['capacity_mib']==4 else 'Fast RAM two ranks; intended 2 MB Chip RAM experiment'])
print('Created four assembly options, individual BOMs and DNP schematics')
