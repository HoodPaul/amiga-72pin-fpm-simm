#!/usr/bin/env python3
"""Read-only A7 native/XML verification, using fresh KiCad 10 CLI exports.

Run after exporting docs/schematic-netlist.xml, variants/*/netlist.xml and
 docs/drc-routed.json. Only Python's standard library is required. This script
never imports pcbnew, fills zones, saves a board or changes a schematic. It
writes only docs/validation.txt and docs/variant-validation.txt; the existing
copper and mapping reviewers write their reports in temporary directories.
"""
from collections import Counter
from decimal import Decimal as D
import csv, hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
import compare_copper as n
R=Path(__file__).resolve().parents[1]

def need(value, message):
    if not value: raise AssertionError(message)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def read_xml(path, schematic):
    need(path.is_file(), f'Missing exported netlist: {path}')
    need(path.stat().st_mtime+1>=schematic.stat().st_mtime, f'Re-export stale netlist: {path}')
    x=ET.parse(path);tool=x.findtext('./design/tool','')
    m=re.search(r'Eeschema (\d+)\.',tool)
    need(m and int(m[1])>=10, f'KiCad 10 XML export required: {tool}')
    pins={}
    for net in x.findall('./nets/net'):
        for node in net.findall('node'):
            key=(node.get('ref'),node.get('pin'))
            need(key not in pins,f'Duplicate XML pin {key}')
            pins[key]=net.get('name')
    return pins,{c.get('ref'):c for c in x.findall('./components/comp')},tool

def check_xml(pins,maps):
    count=0
    for ref,assignment in maps.items():
        for pin,net in assignment.items():
            value=pins.get((ref,pin),'')
            if net:
                need(value=='/'+net,f'XML {ref}.{pin}: {value} versus {net}');count+=1
            else:need(not value or value.startswith('unconnected-'),f'NC pin connected: {ref}.{pin}')
    need(all(ref in maps and pin in maps[ref] for ref,pin in pins),'Unexpected XML pin')
    return count

def independent_reviews():
    with tempfile.TemporaryDirectory(prefix='hy8m-a7-review-') as temp:
        t=Path(temp)
        run=subprocess.run([sys.executable,str(R/'source/compare_copper.py'),'--report-dir',str(t/'copper')],text=True,capture_output=True)
        need(run.returncode==0,'Copper comparison failed:\n'+run.stdout+run.stderr)
        copper=json.loads((t/'copper/copper-comparison.json').read_text())
        need(copper['result']=='PASS','Saved copper or mechanics changed')
        (t/'mapping/source').mkdir(parents=True);(t/'mapping/docs').mkdir()
        shutil.copyfile(R/'source/review_mapping.py',t/'mapping/source/review_mapping.py')
        shutil.copyfile(R/'docs/design-data.json',t/'mapping/docs/design-data.json')
        run=subprocess.run([sys.executable,str(t/'mapping/source/review_mapping.py')],text=True,capture_output=True)
        need(run.returncode==0 and '321 assertions passed' in run.stdout,'Logical review failed:\n'+run.stdout+run.stderr)
    return copper

def verify():
    board_path=R/'HY8M-SIMM.kicad_pcb'
    paths=[board_path,R/'HY8M-SIMM.kicad_sch']+sorted((R/'variants').glob('*/HY8M-SIMM.kicad_sch'))
    hashes={path:sha(path) for path in paths}
    maps=json.loads((R/'docs/design-data.json').read_text())['net_maps']
    independent_reviews()
    xp,xc,tool=read_xml(R/'docs/schematic-netlist.xml',R/'HY8M-SIMM.kicad_sch')
    logical_count=check_xml(xp,maps)
    need(set(xc)==set(maps),'Main XML references disagree with circuit')
    b=n.parse(board_path);nets={i[1]:i[2] for i in n.children(b,'net') if len(i)>2}
    fps={};pad_count=connected=nc_count=0
    for fp in n.children(b,'footprint'):
        pads=n.children(fp,'pad')
        if not pads:continue # Padless silk-only logo footprints are not circuitry.
        ref=n.reference(fp);need(ref in maps and ref not in fps,f'Unexpected/duplicate footprint {ref}')
        fps[ref]=fp;seen=Counter()
        for pad in pads:
            pin=str(pad[1]);need(pin in maps[ref],f'Unexpected pad {ref}.{pin}')
            target=maps[ref][pin];actual=n.net_name(pad,nets);seen[pin]+=1
            need(actual==('/'+target if target else ''),f'PCB {ref}.{pin}: {actual} versus {target}')
            pad_count+=1;connected+=bool(target);nc_count+=not bool(target)
            if ref=='J1':need(not any(str(i).endswith('.Paste') for i in n.field(pad,'layers')),'Paste layer on finger')
        need(seen==Counter({pin:2 if ref=='J1' else 1 for pin in maps[ref]}),f'Incorrect pad numbering {ref}')
    need(set(fps)==set(maps),'PCB references disagree with circuit')
    need((pad_count,connected,nc_count)==(336,294,42),f'Unexpected pad counts {(pad_count,connected,nc_count)}')
    for ref in ('U1','U2','U3','U4'):
        need(n.field(fps[ref],'layer')==(('F.Cu',) if ref in ('U1','U2') else ('B.Cu',)),f'Wrong face {ref}')
    layers=[i[1] for i in n.child(b,'layers')[1:] if isinstance(i,list) and str(i[1]).endswith('.Cu')]
    need(layers==['F.Cu','In1.Cu','In2.Cu','B.Cu'],'Expected four copper layers')
    need({(n.field(z,'layer'),n.net_name(z,nets)) for z in n.children(b,'zone')}=={(('In1.Cu',),'/GND'),(('In2.Cu',),'/+5V')},'Power zones changed')
    tracks=n.children(b,'segment')+n.children(b,'arc');vias=n.children(b,'via')
    need((len(tracks),len(vias))==(864,195),'Track/via counts changed')
    need(all(n.field(t,'width')[0]>=D('.2') for t in tracks),'Track below0.20mm')
    need(all(n.field(v,'size')==(D('.6'),) and n.field(v,'drill')==(D('.3'),) for v in vias),'Via size/drill changed')
    need(all(n.field(t,'layer') in [('F.Cu',),('In2.Cu',),('B.Cu',)] for t in tracks),'Route on ground plane')
    need(any(n.field(t,'layer')==('In2.Cu',) and n.net_name(t,nets) not in ('/+5V','/GND') for t in tracks),'Expected mixed-use In2')
    edges=[i for i in b if isinstance(i,list) and i and i[0]=='gr_line' and n.field(i,'layer')==('Edge.Cuts',)]
    pts=[n.field(i,k) for i in edges for k in ('start','end')]
    need(max(p[0] for p in pts)-min(p[0] for p in pts)==D('107.95'),'Board length changed')
    need(max(p[1] for p in pts)-min(p[1] for p in pts)==D('25.4'),'Board height changed')
    need(n.field(n.child(b,'general'),'thickness')==(D('1.2'),),'Proposed thickness changed')
    variants=json.loads((R/'docs/assembly-variants.json').read_text())
    vlines=['A7 common-PCB assembly variant verification','Fresh KiCad 10 XML exports; all options retain common connectivity.','']
    topology={key:value for key,value in xp.items() if not value.startswith('unconnected-')}
    for tag,v in variants.items():
        folder=R/'variants'/tag
        vp,vc,_=read_xml(folder/'netlist.xml',folder/'HY8M-SIMM.kicad_sch')
        need(check_xml(vp,maps)==logical_count,f'{tag}: logical count differs')
        need({key:value for key,value in vp.items() if not value.startswith('unconnected-')}==topology,f'{tag}: connectivity differs')
        need(set(vc)==set(maps),f'{tag}: component set differs')
        fitted,dnp=set(v['fitted']),set(v['dnp'])
        need(not fitted&dnp and fitted|dnp==set(maps)-{'J1'},f'{tag}: incomplete/overlapping population')
        for ref,c in vc.items():
            need((c.find('./property[@name="dnp"]') is not None)==(ref in dnp),f'{tag}: DNP flag {ref}')
            if ref.startswith('U'):need(c.findtext('value')==v['dram_mpn'],f'{tag}: chip value {ref}')
        size,speed=v['capacity_mib'],v['speed_ns']
        need({'U1','U2','C1','C2'}<=fitted,f'{tag}: front rank incomplete')
        need(all((ref in fitted)==(size==8) for ref in ['U3','U4','C3','C4','R1','R2','R3','R4']),f'{tag}: rear rank population')
        need([f'PD{i+1}' in fitted for i in range(4)]==v['pd_grounded']==[size==4,size==4,speed==70,False],f'{tag}: PD code')
        need(v['dram_mpn']==('HY5118160BJC-60' if speed==60 else 'HY5118160JC-70'),f'{tag}: speed-grade MPN')
        need(v['rear_enabled']==(size==8),f'{tag}: rear enable declaration')
        with (folder/'BOM.csv').open(newline='') as handle:bom=list(csv.DictReader(handle))
        need({row['Reference'] for row in bom}==fitted|{'PCB'},f'{tag}: BOM population')
        need(all(row['Quantity']=='1' for row in bom),f'{tag}: BOM quantities')
        need(all(row['Value_or_MPN']==v['dram_mpn'] for row in bom if row['Reference'].startswith('U')),f'{tag}: BOM MPN')
        vlines += [f'PASS: {tag}: all {logical_count} connected logical pins match the common PCB.',f'PASS: {tag}: DNP flags, fitted-component BOM, chip MPN and PD code agree.',f'  Fitted: {", ".join(sorted(fitted))}',f'  DNP: {", ".join(sorted(dnp))}']
    vlines+=['','The common PCB retains every pad and net for each option.','The variant schematic and BOM specify fitting. Population equivalence does not','establish hardware operation or donor authenticity.']
    drc_path=R/'docs/drc-routed.json'
    need(drc_path.stat().st_mtime+1>=board_path.stat().st_mtime,'DRC predates PCB; run KiCad DRC again')
    drc=json.loads(drc_path.read_text())
    need(int(drc['kicad_version'].split('.')[0])>=10,'KiCad10 DRC required')
    need(not drc['unconnected_items'],'Missing PCB connections')
    violations=drc['violations'];parity=drc['schematic_parity']
    need(Counter((i['type'],i['severity']) for i in violations)=={('copper_edge_clearance','error'):144},'Unexpected PCB DRC findings')
    for i in violations:
        need('actual 0.2286 mm' in i['description'],'Unexpected edge distance')
        need(any(re.search(r'Pad \d+ \[.*\] of J1 on [FB]\.Cu',j['description']) for j in i['items']),'Non-contact edge finding')
    need(Counter((i['type'],i['severity']) for i in parity)=={('net_conflict','warning'):42,('footprint_symbol_mismatch','warning'):4},'Unexpected schematic parity findings')
    for i in [j for j in parity if j['type']=='net_conflict']:
        need('Pad missing net given by schematic (unconnected-(' in i['description'],'Functional connected-net conflict')
        need(len(i['items'])==1,'Unexpected NC parity item count')
        m=re.fullmatch(r'Pad (\d+) \[<no net>\] of (\S+) on [FB]\.Cu',i['items'][0]['description'])
        need(m and maps[m[2]][m[1]] is None,'Parity issue affects a connected pad')
    meta=[i for i in parity if i['type']=='footprint_symbol_mismatch']
    need(sum(i['description'].startswith('Value (J1)') for i in meta)==1,'Unexpected value mismatch')
    need({i['items'][0]['description'] for i in meta if 'Do not populate' in i['description']}=={'Footprint PD1','Footprint PD2','Footprint PD4'},'Unexpected PCB DNP mismatch')
    ignored=drc.get('ignored_checks',[])
    need(not any(i.get('severity')=='exclusion' for i in violations+parity),'Excluded report finding')
    erc_lines=[]
    for path in sorted((R/'docs').glob('erc*.json')):
        erc=json.loads(path.read_text());counts=Counter((i.get('type','unknown'),i.get('severity','unknown')) for i in erc.get('violations',[]))
        erc_lines.append(f'ERC report {path.name}: {sum(counts.values())} findings; {dict(counts)}.')
    if not erc_lines:erc_lines=['ERC is available in KiCad 10 but no ERC report is included in this verification.']
    need(all(sha(path)==value for path,value in hashes.items()),'CAD changed during read-only verification')
    lines=[f'HY8M A7 four-layer draft verification, {drc["date"]}, KiCad {drc["kicad_version"]}','',
        'PASS: exact saved copper/mechanics comparison with uploaded PCB and retained A6 reference.',
        'PASS: independent logical mapping reviewer passed all 321 assertions.',
        f'PASS: all 336 physical pads match the intended map and fresh {tool} XML.',
        f'PASS: 294 connected physical pads / {logical_count} logical pins; 42 intentional NC pads.',
        'PASS: complete 4 MiB front/rear ranks; correct independent CAS byte enables and RAS links.',
        'PASS: rear A0..A7 reversal remains bijective; A8/A9 unchanged.',
        'PASS: four variant XML topologies, DNP flags, fitted BOM populations and PD codes agree.',
        'PASS: 107.95 x 25.4 mm outline, retaining holes, notch and 144 contacts preserved.',
        'PASS: four layers; In1 GND; In2 signals/+5V fill; remaining signals F/B.',
        'PASS: 864 saved track segments; 195 through vias; minimum track 0.20 mm; vias 0.60/0.30 mm.',
        'PASS: zero unconnected items; no reported shorts, copper-to-copper clearance or dangling-copper findings.',
        'PASS: checker did not refill zones, save a board or modify PCB/schematic files.','',
        'OUTSTANDING BOARD DRC: 144 copper-edge errors remain visible.',
        'Every finding is a J1 contact pad: 0.2286 mm clearance against the generic 0.50 mm rule.',
        'No non-contact edge findings were reported. Contact hard-gold/bevel requires fabrication review.','',
        'SCHEMATIC PARITY: 46 warnings remain visible; no functional connected-net conflict was found.',
        ' 42: KiCad 10 exports explicit unconnected-(...) nets for NC pins; preserved PCB pads have no net.',
        ' These comprise 22 J1 face pads and 20 DRAM NC pads.',
        ' 1: J1 PCB value is J1; schematic value is 72-pin / 4 or 8 MB / FPM.',
        ' 3: common-PCB DNP attributes differ from the main 8 MB / 70 ns schematic at PD1/PD2/PD4.',
        ' Variant schematics/BOMs specify actual fitting; these metadata warnings do not change copper.','',
        f'Existing project settings ignore {len(ignored)} DRC check types:']
    lines += [f'  {i["key"]}: {i["description"]}' for i in ignored]
    lines += ['No actual findings are excluded from this report. All 144 errors and 46 parity warnings remain visible.','']+erc_lines+['',
        f'Checked native PCB SHA-256: {hashes[board_path]}',
        f'DRC report: docs/drc-routed.json; recorded source: {drc["source"]}.',
        'Verification uses saved zone copper and does not refill or rewrite it.','',
        'Not a fabrication release. Proposed 1.2 mm thickness, stack-up, land pattern, contact finish/bevel',
        'and assembled/socket fit require review. No donor authenticity, physical board, timing, signal',
        'integrity, retention/refresh or A4000 operation has been tested. Intended 8 MiB assembly use',
        'as 2 MiB Chip RAM remains an untested host-wiring inference.']
    (R/'docs/validation.txt').write_text('\n'.join(lines)+'\n')
    (R/'docs/variant-validation.txt').write_text('\n'.join(vlines)+'\n')
    print('\n'.join(lines))

if __name__=='__main__':verify()
