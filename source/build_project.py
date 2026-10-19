#!/usr/bin/env python3
"""Generate review-stage KiCad 7 schematic and placed, UNROUTED PCB.
Run with KiCad's pcbnew Python module available. No external symbol libraries.
"""
import csv, json, uuid, re
from pathlib import Path
import pcbnew as p

ROOT = Path(__file__).resolve().parent.parent
NAME = 'HY8M-SIMM'
def uid(s): return str(uuid.uuid5(uuid.NAMESPACE_URL, 'hy8m-reva3/' + s))
def q(s): return json.dumps(str(s))
def mm(x,y): return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
rootid=uid('schematic')

# Hyundai HY5118160, document 1AD15-10-MAY95, page 1, SOJ marking-side view.
chip={1:'VCC',2:'DQ0',3:'DQ1',4:'DQ2',5:'DQ3',6:'VCC',7:'DQ4',8:'DQ5',9:'DQ6',10:'DQ7',11:'NC',12:'NC',13:'WE_N',14:'RAS_N',15:'NC',16:'NC',17:'A0',18:'A1',19:'A2',20:'A3',21:'VCC',22:'GND',23:'A4',24:'A5',25:'A6',26:'A7',27:'A8',28:'A9',29:'OE_N',30:'UCAS_N',31:'LCAS_N',32:'NC',33:'DQ8',34:'DQ9',35:'DQ10',36:'DQ11',37:'GND',38:'DQ12',39:'DQ13',40:'DQ14',41:'DQ15',42:'GND'}
# HYM532220 W-Series, 1CD07-10-DEC94 p2. Data numbering normalised
# to contiguous DQ0..31, excluding the manufacturer's unused parity positions.
edge={1:'GND',2:'DQ0',3:'DQ16',4:'DQ1',5:'DQ17',6:'DQ2',7:'DQ18',8:'DQ3',9:'DQ19',10:'+5V',11:None,12:'A0',13:'A1',14:'A2',15:'A3',16:'A4',17:'A5',18:'A6',19:None,20:'DQ4',21:'DQ20',22:'DQ5',23:'DQ21',24:'DQ6',25:'DQ22',26:'DQ7',27:'DQ23',28:'A7',29:None,30:'+5V',31:'A8',32:'A9',33:'RAS3_N',34:'RAS2_N',35:None,36:None,37:None,38:None,39:'GND',40:'CAS0_N',41:'CAS2_N',42:'CAS3_N',43:'CAS1_N',44:'RAS0_N',45:'RAS1_N',46:None,47:'WE_N',48:None,49:'DQ8',50:'DQ24',51:'DQ9',52:'DQ25',53:'DQ10',54:'DQ26',55:'DQ11',56:'DQ27',57:'DQ12',58:'DQ28',59:'+5V',60:'DQ29',61:'DQ13',62:'DQ30',63:'DQ14',64:'DQ31',65:'DQ15',66:None,67:None,68:None,69:'GND',70:None,71:None,72:'GND'}
conn_names={i:(edge[i] or ('PD'+str(i-66) if 67<=i<=70 else 'NC')) for i in edge}
conn_names[69]='PD3'
for n in range(67,71):edge[n]='PD'+str(n-66)
def frontbit(offset,i):
    if offset==0:return i if i<8 else 23-i
    return 23-i if i<8 else 16+i
def chipnets(ras,offset,back=False):
    d={}
    for n,s in chip.items():
        if s=='NC':v=None
        elif s=='VCC':v='+5V'
        elif s=='OE_N':v='GND'
        elif s=='RAS_N':v=('REAR_LO_N' if offset==0 else 'REAR_HI_N') if back else f'RAS{ras}_N'
        elif s=='LCAS_N':v=f'CAS{offset//8+(1 if back else 0)}_N'
        elif s=='UCAS_N':v=f'CAS{offset//8+(0 if back else 1)}_N'
        elif s.startswith('DQ'):
            i=int(s[2:]);v='DQ'+str(frontbit(offset,15-i if back else i))
        elif back and s.startswith('A') and int(s[1:])<8:v='A'+str(7-int(s[1:]))
        else:v=s
        d[n]=v
    return d
maps={'J1':edge,'U1':chipnets(0,0),'U2':chipnets(2,16),'U3':chipnets(1,0,True),'U4':chipnets(3,16,True)}
for i in range(1,5):maps['C'+str(i)]={1:'+5V',2:'GND'}
maps.update({'R1':{1:'RAS1_N',2:'REAR_LO_N'},'R2':{1:'RAS3_N',2:'REAR_HI_N'},'R3':{1:'+5V',2:'REAR_LO_N'},'R4':{1:'+5V',2:'REAR_HI_N'}})
for i in range(1,5):maps['PD'+str(i)]={1:'PD'+str(i),2:'GND'}

symbols={}
pinpos={}
def symbol(name,ref,names,kind='ic'):
    count=len(names); half=count//2
    if kind in ['cap','res']:
        coords={1:(-5.08,0,0),2:(5.08,0,180)}
        drawing='(polyline (pts (xy -0.635 -2.54)(xy -0.635 2.54)) (stroke (width 0.254)(type default))(fill (type none))) (polyline (pts (xy 0.635 -2.54)(xy 0.635 2.54)) (stroke (width 0.254)(type default))(fill (type none)))'
        if kind=='res':drawing='(rectangle (start -1.905 0.762)(end 1.905 -0.762)(stroke (width 0.254)(type default))(fill (type none)))'
    elif kind=='flag':
        coords={1:(0,0,90)}
        drawing='(polyline (pts (xy -1.27 2.54)(xy 0 3.81)(xy 1.27 2.54)(xy 0 1.27)(xy -1.27 2.54)) (stroke (width 0)(type default))(fill (type none)))'
    else:
        coords={n:((-15.24 if n<=half else 15.24), round(((half-1)/2-(n-1 if n<=half else count-n))*2.54,3), (0 if n<=half else 180)) for n in names}
        h=(half+1)*1.27
        drawing=f'(rectangle (start -10.16 {h}) (end 10.16 {-h}) (stroke (width 0.254)(type default))(fill (type background)))'
    pinpos[name]=coords
    pins=[]
    for n,s in names.items():
        x,y,a=coords[n]
        typ='passive'
        if kind=='flag': typ='power_out'
        elif kind=='ic':
            typ='no_connect' if s=='NC' else 'power_in' if s in ['VCC','GND'] else 'bidirectional' if s.startswith('DQ') else 'input'
        ln=4.445 if kind in ['cap','res'] else 2.54 if kind=='flag' else 5.08
        pins.append(f'(pin {typ} line (at {x} {y} {a})(length {ln})(name {q(s)} (effects (font (size 1 1))))(number "{n}" (effects (font (size 1 1)))))')
    symbols[name]=f'''(symbol "HY8M:{name}" (pin_names (offset 0.508)) (in_bom yes)(on_board yes)
      (property "Reference" "{ref}" (id 0)(at 0 0 0)(effects (font (size 1.27 1.27))))
      (property "Value" "{name}" (id 1)(at 0 0 0)(effects (font (size 1.27 1.27))))
      (symbol "{name}_0_1" {drawing})
      (symbol "{name}_1_1" {''.join(pins)}))'''
symbol('HY5118160JC','U',chip)
symbol('SIMM72','J',conn_names,'connector')
symbol('C','C',{1:'1',2:'2'},'cap')
symbol('R','R',{1:'1',2:'2'},'res')
symbol('PWR_FLAG','#FLG',{1:'pwr'},'flag')

sheet=[f'(kicad_sch (version 20230121)(generator eeschema)(uuid {rootid})(paper "A2")',
 '(title_block (title "HY8M | 4/8 MB FPM SIMM | ROUTED DRAFT")(date "2026-10-18")(rev "A7 - JMC AND PD LABELS")(company "Custom 72-pin module")(comment 1 "HY5118160JC-70 x2 or x4 / 5 V / 4 MB or 8 MB")(comment 2 "Not fabrication-ready. Amiga 4000 operation not yet tested."))',
 '(lib_symbols '+''.join(symbols.values())+')']
components={}
def text(t,x,y,size=1.5):
    sheet.append(f'(text {q(t)} (at {x} {y} 0)(effects (font (size {size} {size}))(justify left bottom))(uuid {uid(t+str(x)+str(y))}))')
def inst(ref,name,value,x,y,nets,fp=''):
    u=uid(ref); components[ref]=(u,fp,value)
    top=48 if name=='SIMM72' else 30 if name=='HY5118160JC' else 7
    sheet.append(f'''(symbol (lib_id "HY8M:{name}")(at {x} {y} 0)(unit 1)(in_bom yes)(on_board yes)(dnp no)(uuid {u})
     (property "Reference" {q(ref)} (id 0)(at {x} {y-top-3} 0)(effects (font (size 1.27 1.27))))
     (property "Value" {q(value)} (id 1)(at {x} {y-top} 0)(effects (font (size 1.27 1.27))))
     (property "Footprint" {q(fp)} (id 2)(at {x} {y} 0)(effects (font (size 1 1)) hide))
     (instances (project "{NAME}" (path "/{rootid}" (reference {q(ref)})(unit 1)))))''')
    for n,(px,py,a) in pinpos[name].items():
        xx=round(x+px,3); yy=round(y-py,3); net=nets[n]
        if net is None:
            sheet.append(f'(no_connect (at {xx} {yy})(uuid {uid(ref+str(n)+"nc")}))')
        else:
            end=round(xx+(-5.08 if a==0 else 5.08 if a==180 else 0),3)
            if end!=xx:
                sheet.append(f'(wire (pts (xy {xx} {yy})(xy {end} {yy}))(stroke (width 0)(type default))(uuid {uid(ref+str(n)+"wire")}))')
            sheet.append(f'(label {q(net)} (at {end} {yy} 0)(effects (font (size 1 1))(justify {"left" if a!=180 else "right"} bottom))(uuid {uid(ref+str(n)+"label")}))')
text('72-PIN EDGE CONNECTOR',25,27,2)
inst('J1','SIMM72','72-pin / 4 or 8 MB / FPM',60.96,106.68,edge,'HY8M:SIMM72')
for ref,x,y in [('U1',172.72,81.28),('U2',269.24,81.28),('U3',172.72,182.88),('U4',269.24,182.88)]:
    inst(ref,'HY5118160JC','HY5118160JC-70',x,y,maps[ref],'HY8M:SOJ42_400mil')
text('BANK 0 / FRONT / 1Mx32 = 4 MB',137,30,2)
text('BANK 1 / BACK / 1Mx32 = 4 MB',137,132,2)
text('LOCAL DECOUPLING',330,30,2)
for i in range(1,5):
    inst('C'+str(i),'C','220 nF / 16 V X7R',355.6,50.8+(i-1)*38.1,maps['C'+str(i)],'HY8M:C_0805')
    text('Place beside U'+str(i),338,60.96+(i-1)*38.1,1.2)
text('REAR BANK ENABLE / 0R LINKS',430,30,2)
for i in range(1,5):
    inst('R'+str(i),'R','0R / REAR EN' if i<3 else '10k / REAR PULLUP',469.9,50.8+(i-1)*25.4,maps['R'+str(i)],'HY8M:R_0603')
text('PRESENCE DETECT / FIT 0R TO GND',430,160,2)
for i in range(1,5):
    inst('PD'+str(i),'R','0R / OPTION',469.9,180.34+(i-1)*25.4,maps['PD'+str(i)],'HY8M:R_0603')
inst('#FLG01','PWR_FLAG','PWR_FLAG',345.44,220.98,{1:'+5V'})
inst('#FLG02','PWR_FLAG','PWR_FLAG',378.46,220.98,{1:'GND'})
text('NOTES',25,180,2)
for i,t in enumerate(['4 MB front pair; 8 MB adds rear pair; 2 MB Chip use untested.',
    'Four CAS signals remain separate. No control outputs are shorted.',
    'OE_N tied to GND as in the Hyundai module circuit.',
    'PD link options: see build table; defaults 8 MB / 70 ns.',
    'DQ permuted within bytes; rear A0..A7 reversed, A8/A9 retained.',
    'NC contacts: 11, 19, 29, 35-38, 46, 48, 66, 71.',
    'Source: Hyundai HYM532220 W-Series, 1CD07-10-DEC94, p2.',
    'Chip: Hyundai HY5118160, 1AD15-10-MAY95, pp1 and 14.']): text(t,25,190+i*5.08,1.2)
sheet.append(')')
(ROOT/(NAME+'.kicad_sch')).write_text('\n'.join(sheet))
lib='(kicad_symbol_lib (version 20220914)(generator kicad_symbol_editor)'+''.join(s.replace('"HY8M:', '"') for s in symbols.values())+')'
(ROOT/'HY8M.kicad_sym').write_text(lib)
(ROOT/'sym-lib-table').write_text('(sym_lib_table (lib (name "HY8M")(type "KiCad")(uri "${KIPRJMOD}/HY8M.kicad_sym")(options "")(descr "Project-local symbols")))')
(ROOT/'fp-lib-table').write_text('(fp_lib_table (lib (name "HY8M")(type "KiCad")(uri "${KIPRJMOD}/HY8M.pretty")(options "")(descr "Project-local footprints")))')
(ROOT/(NAME+'.kicad_pro')).write_text((ROOT/'source/base-project-settings.json').read_text())

# Create a clean board, preserving the supplied template's edge geometry.
template=ROOT/'source'/'template.kicad_pcb'
# Ignore the source's zero-area placeholder pads before importing geometry.
clean = re.sub(r'^\s*\(pad 0[^\n]*\n', '', template.read_text(), flags=re.M)
tmp = ROOT/'source'/'template-clean.tmp.kicad_pcb'
tmp.write_text(clean)
original=p.LoadBoard(str(tmp)); tmp.unlink()
b=p.BOARD()
connector=next(f for f in original.GetFootprints() if f.GetReference()=='U1').Duplicate()
for pad in connector.Pads(): pad.SetNetCode(0)
b.Add(connector)
for old in original.GetDrawings():
    if old.GetLayer()!=p.Edge_Cuts: continue
    d=old.Duplicate(); b.Add(d)
    # Shorten to 22 mm total height; correct the source's 0.004793 mm edge gap.
    for get,setter in [(d.GetStart,d.SetStart),(d.GetEnd,d.SetEnd)]:
        v=get(); x=p.ToMM(v.x); y=p.ToMM(v.y)
        if abs(y-79.25)<0.01: setter(mm(x,85.6))
        elif abs(x-105)<0.01 and abs(y-104.65)<0.01: setter(mm(x,104.654793))
b.SetCopperLayerCount(4)
b.GetDesignSettings().SetBoardThickness(p.FromMM(1.2))
allnets=sorted({v for d in maps.values() for v in d.values() if v})
nets={}
for s in allnets:
    n=p.NETINFO_ITEM(b,"/"+s); b.Add(n); nets[s]=n
def link(f,ref):
    f.SetReference(ref); f.SetValue(components[ref][2]); f.SetPath(p.KIID_PATH('/'+rootid+'/'+components[ref][0]))
    f.SetFPID(p.LIB_ID(*components[ref][1].split(':')))
    for pad in f.Pads():
        net=maps[ref].get(int(pad.GetNumber()))
        if net: pad.SetNet(nets[net])
    f.Value().SetVisible(False)
link(connector,'J1')
connector.Reference().SetVisible(False)
for pad in connector.Pads():
    ls=p.LSET(); ls.AddLayer(p.F_Cu if pad.IsOnLayer(p.F_Cu) else p.B_Cu); ls.AddLayer(p.F_Mask if pad.IsOnLayer(p.F_Cu) else p.B_Mask)
    pad.SetLayerSet(ls)
# Save connector footprint without board net names and absolute placement.
cf=p.FootprintLoad(str(ROOT/'source'), 'connector') if False else connector.Duplicate()
cf.SetPosition(mm(0,0)); cf.SetReference('REF**'); cf.SetValue('SIMM72')
for pad in cf.Pads(): pad.SetNetCode(0)
p.FootprintSave(str(ROOT/'HY8M.pretty'),cf)
# FootprintSave uses the FPID item name (SIMM72).
def addline(f,x1,y1,x2,y2,layer,width=0.15):
    s=p.FP_SHAPE(f); s.SetShape(p.SHAPE_T_SEGMENT); s.SetStart(mm(x1,y1)); s.SetEnd(mm(x2,y2)); s.SetLayer(layer); s.SetWidth(p.FromMM(width)); s.SetLocalCoord(); f.Add(s)
def rectangle(f,w,h,layer):
    for a,c in [((-w/2,-h/2),(w/2,-h/2)),((w/2,-h/2),(w/2,h/2)),((w/2,h/2),(-w/2,h/2)),((-w/2,h/2),(-w/2,-h/2))]: addline(f,*a,*c,layer)
def smdmask():
    ls=p.LSET()
    for l in [p.F_Cu,p.F_Paste,p.F_Mask]: ls.AddLayer(l)
    return ls
def makefp(name):
    f=p.FOOTPRINT(b); f.SetFPID(p.LIB_ID('HY8M',name)); f.SetAttributes(p.FP_SMD); f.SetReference('REF**'); f.SetValue(name)
    return f
soj=makefp('SOJ42_400mil')
for n in range(1,43):
    pad=p.PAD(soj); pad.SetNumber(str(n)); pad.SetAttribute(p.PAD_ATTRIB_SMD); pad.SetShape(p.PAD_SHAPE_RECT)
    pad.SetSize(mm(2.0,0.65)); pad.SetPosition(mm(-5.15 if n<=21 else 5.15, (n-11)*1.27 if n<=21 else (32-n)*1.27)); pad.SetLocalCoord(); pad.SetLayerSet(smdmask()); soj.Add(pad)
rectangle(soj,10.16,27.31,p.F_Fab)
rectangle(soj,12.8,28.0,p.F_CrtYd)
addline(soj,-4.0,-13.9,4,-13.9,p.F_SilkS)
addline(soj,-4,13.9,4,13.9,p.F_SilkS)
addline(soj,-6.4,-13.2,-6.4,-12.2,p.F_SilkS,0.25)
soj.Reference().SetPosition(mm(0,-15)); soj.Value().SetVisible(False)
p.FootprintSave(str(ROOT/'HY8M.pretty'),soj)
cap=makefp('C_0805')
for n,x in [(1,-1),(2,1)]:
    pad=p.PAD(cap); pad.SetNumber(str(n)); pad.SetAttribute(p.PAD_ATTRIB_SMD); pad.SetShape(p.PAD_SHAPE_RECT); pad.SetSize(mm(1,1.45)); pad.SetPosition(mm(x,0)); pad.SetLocalCoord(); pad.SetLayerSet(smdmask()); cap.Add(pad)
rectangle(cap,2,1.25,p.F_Fab); rectangle(cap,3.5,2,p.F_CrtYd)
addline(cap,-.4,-.9,.4,-.9,p.F_SilkS); addline(cap,-.4,.9,.4,.9,p.F_SilkS)
cap.Reference().SetPosition(mm(0,-1.8)); cap.Value().SetVisible(False)
p.FootprintSave(str(ROOT/'HY8M.pretty'),cap)
res=makefp('R_0603')
for n,x in [(1,-.8),(2,.8)]:
    pad=p.PAD(res);pad.SetNumber(str(n));pad.SetAttribute(p.PAD_ATTRIB_SMD);pad.SetShape(p.PAD_SHAPE_RECT);pad.SetSize(mm(.9,.95));pad.SetPosition(mm(x,0));pad.SetLocalCoord();pad.SetLayerSet(smdmask());res.Add(pad)
rectangle(res,1.6,.8,p.F_Fab);rectangle(res,2.7,1.7,p.F_CrtYd)
res.Reference().SetPosition(mm(0,-1.5));res.Value().SetVisible(False);p.FootprintSave(str(ROOT/'HY8M.pretty'),res)
positions=[('U1',143,97.5,False),('U2',175,97.5,False),('U3',143,97.5,True),('U4',175,97.5,True),('C1',126.5,94.0,False),('C2',191.5,94.0,False),('C3',126.5,94.0,True),('C4',191.5,94.0,True)]
positions += [('R'+str(i),158.975,87.5+(i-1)*2.5,False) for i in range(1,5)]
positions += [('PD'+str(i),203,94+(i-1)*3,False) for i in range(1,5)]
for ref,x,y,back in positions:
    f=p.FootprintLoad(str(ROOT/'HY8M.pretty'),'SOJ42_400mil' if ref[0]=='U' else 'C_0805' if ref[0]=='C' else 'R_0603')
    b.Add(f);f.SetPosition(mm(x,y))
    if ref[0]=='U':f.SetOrientationDegrees(270 if ref in ['U2','U4'] else 90)
    if back:f.Flip(f.GetPosition(),False)
    link(f,ref)
    f.Reference().SetPosition(mm(x,y-7.7 if ref[0]=='U' else y-1.5))
    if ref.startswith('PD'):f.Reference().SetPosition(mm(x-3,y))
    elif ref[0]=='R':f.Reference().SetPosition(mm(x,y+1.25))
    f.Reference().SetTextAngle(p.EDA_ANGLE(90 if ref[0]=='U' else 0,p.DEGREES_T))
    f.Reference().SetTextSize(mm(.8,.8));f.Reference().SetTextThickness(p.FromMM(.12))


# Board silkscreen and explicit drawing-stage status. Colour is a fab choice.
def boardtext(t,x,y,layer,size=1):
    z=p.PCB_TEXT(b); z.SetText(t); z.SetPosition(mm(x,y)); z.SetTextSize(mm(size,size)); z.SetTextThickness(p.FromMM(.15)); z.SetLayer(layer)
    if layer==p.B_SilkS: z.SetMirrored(True)
    b.Add(z)
# Final showpiece legend is added by finish_board.py.
# Front kept clear of revision/status wording.
boardtext('5V / 25.4mm / 4L',158.5,86.65,p.B_SilkS,.85)
boardtext('REV A6',158.5,105,p.B_SilkS,.8)
boardtext('A6 FOUR-LAYER ROUTED DRAFT',158,84,p.Dwgs_User,1.5)
boardtext('107.95 x 25.4 mm | provisional 1.2 mm | black mask / white legend / gold contacts',158,116,p.Dwgs_User,1)
boardtext('REAR EN: R1+R2',117.5,88.8,p.F_SilkS,.8)
boardtext('4MB: FRONT ONLY',117.5,90.5,p.F_SilkS,.8)
boardtext('PD1+2: 4MB',203,87.5,p.F_SilkS,.8)
boardtext('PD3: 70ns',203,89,p.F_SilkS,.8)
boardtext('PD4: OPEN',203,90.5,p.F_SilkS,.8)
b.GetTitleBlock().SetTitle('HY8M 4/8 MB FPM SIMM - FOUR-LAYER DRAFT')
b.GetTitleBlock().SetRevision('A6')
p.SaveBoard(str(ROOT/(NAME+'.kicad_pcb')),b)

with (ROOT/'docs'/'pin-net-map.csv').open('w') as f:
    w=csv.writer(f); w.writerow(['Reference','Pin','Signal','Net'])
    for ref,m in maps.items():
        for n,v in sorted(m.items()): w.writerow([ref,n,(chip[n] if ref[0]=='U' else conn_names[n] if ref=='J1' else str(n)),v or 'NC'])
with (ROOT/'BOM.csv').open('w') as f:
    w=csv.writer(f); w.writerow(['References','Quantity','Value_or_MPN','Package','Specification','Sourcing_note'])
    w.writerow(['U1 U2 U3 U4',4,'HY5118160JC-70','42-pin SOJ 400 mil','5 V; 1Mx16; FPM; 70 ns; 1K refresh','Salvage four identifiable tested chips; do not substitute EDO HY5118164'])
    w.writerow(['C1 C2 C3 C4',4,'220 nF','0805','16 V minimum; X7R; +/-10%','New MLCC; one per chip per original module'])
    w.writerow(['PCB',1,'HY8M Rev A7','72-pin SIMM','107.95 x 25.4 mm; 4-layer proposed; 1.2 mm provisional','UNROUTED: do not order this revision'])
with (ROOT/'docs'/'design-data.json').open('w') as f: json.dump({'chip_pin_names':chip,'net_maps':maps,'component_uuids':{r:v[0] for r,v in components.items()},'sheet_uuid':rootid},f,indent=2)
print('Generated',ROOT)
