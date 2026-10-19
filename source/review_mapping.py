#!/usr/bin/env python3
"""Independent logical review of the A3 pin map, without modifying its CAD."""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent.parent
data_path = root / 'docs/design-data.json'
data = json.loads(data_path.read_text())
maps = data['net_maps']
pins = data['chip_pin_names']
checks = []

def check(condition, description):
    if not condition:
        raise AssertionError(description)
    checks.append(description)

# This expected edge map is intentionally independent of the project generator.
cas_contacts = {0:'40', 1:'43', 2:'41', 3:'42'}
for byte, contact in cas_contacts.items():
    check(maps['J1'][contact] == f'CAS{byte}_N',
          f'CAS{byte} uses standard SIMM contact {contact}')
for contact, net in {'44':'RAS0_N','45':'RAS1_N',
                     '34':'RAS2_N','33':'RAS3_N'}.items():
    check(maps['J1'][contact] == net, f'{net} uses standard SIMM contact {contact}')

chip_data = {}
byte_routes = []
for ref in ('U1','U2','U3','U4'):
    expected_half = set(range(0,16) if ref in ('U1','U3') else range(16,32))
    assignment = {}
    for pin, function in pins.items():
        if not function.startswith('DQ'):
            continue
        internal_bit = int(function[2:])
        external = maps[ref][pin]
        check(external.startswith('DQ'), f'{ref}.{pin} remains a data signal')
        external_bit = int(external[2:])
        check(external_bit in expected_half,
              f'{ref}.{pin} stays in its RAS-controlled module halfword')
        cas_pin = '31' if internal_bit < 8 else '30'
        expected_cas = f'CAS{external_bit // 8}_N'
        check(maps[ref][cas_pin] == expected_cas,
              f'{ref} internal DQ{internal_bit} / module DQ{external_bit} uses {expected_cas}')
        assignment[internal_bit] = external_bit
    check(len(assignment) == 16 and set(assignment.values()) == expected_half,
          f'{ref} maps its complete 16-bit halfword bijectively')
    chip_data[ref] = assignment
    byte_routes.append((ref,
                        [assignment[i] for i in range(8)], maps[ref]['31'],
                        [assignment[i] for i in range(8,16)], maps[ref]['30']))

for refs, description in [(('U1','U2'),'front 4 MiB rank'),
                          (('U3','U4'),'rear 4 MiB rank')]:
    counts = Counter(bit for ref in refs for bit in chip_data[ref].values())
    check(counts == Counter(range(32)), f'{description} contains every data bit once')

for ref in ('U1','U2','U3','U4'):
    assigned = {}
    for pin, function in pins.items():
        if not function.startswith('A'):
            continue
        internal = int(function[1:])
        expected = 7 - internal if ref in ('U3','U4') and internal < 8 else internal
        check(maps[ref][pin] == f'A{expected}',
              f'{ref} internal A{internal} maps to module A{expected}')
        assigned[internal] = expected
    check(set(assigned.values()) == set(range(10)), f'{ref} address mapping is bijective')
    for pin in ('1','6','21'):
        check(maps[ref][pin] == '+5V', f'{ref}.{pin} supply is +5 V')
    for pin in ('22','29','37','42'):
        check(maps[ref][pin] == 'GND', f'{ref}.{pin} ground/OE is grounded')
    check(maps[ref]['13'] == 'WE_N', f'{ref} shares the module write-enable input')
    for pin in ('11','12','15','16','32'):
        check(maps[ref][pin] is None, f'{ref}.{pin} NC is unconnected')

check(maps['U1']['14'] == 'RAS0_N', 'Front low halfword uses RAS0')
check(maps['U2']['14'] == 'RAS2_N', 'Front high halfword uses RAS2')
check(maps['U3']['14'] == 'REAR_LO_N', 'Rear low halfword uses its isolated RAS net')
check(maps['U4']['14'] == 'REAR_HI_N', 'Rear high halfword uses its isolated RAS net')
for ref, expected in {
    'R1':{'1':'RAS1_N','2':'REAR_LO_N'},
    'R2':{'1':'RAS3_N','2':'REAR_HI_N'},
    'R3':{'1':'+5V','2':'REAR_LO_N'},
    'R4':{'1':'+5V','2':'REAR_HI_N'},
}.items():
    check(maps[ref] == expected, f'{ref} rear-rank enable/pull-up connectivity is correct')

for number in range(1,5):
    net = f'PD{number}'
    check(maps['J1'][str(66+number)] == net, f'{net} uses SIMM contact {66+number}')
    check(maps[f'PD{number}'] == {'1':net,'2':'GND'}, f'{net} has an independent ground strap')

def permute_address(value):
    low = sum(((value >> bit) & 1) << (7 - bit) for bit in range(8))
    return (value & 0x300) | low

for size in (256,512,1024):
    check({permute_address(value) for value in range(size)} == set(range(size)),
          f'Rear permutation preserves the complete {size}-row address subset')

lines = [
    'HY8M-SIMM A3 independent logical mapping review',
    f'Input: {data_path}',
    '',
    f'PASS: {len(checks)} assertions.',
    '',
    'Data/byte-enable assignments (internal chip DQ order):',
]
for ref, low, lcas, high, ucas in byte_routes:
    lines.append(f'{ref}: lower byte {low}, {lcas}; upper byte {high}, {ucas}')
lines += [
    '',
    'Front-only assembly: U1/U2 provide all 32 module data bits, with each',
    '8-bit group governed by the correct independent CAS line. Their RAS0',
    'and RAS2 connections implement one complete 1M x32 (4 MiB) rank.',
    '',
    'Rear assembly: U3/U4 provide another complete 1M x32 rank. R1 connects',
    'RAS1 to the lower halfword and R2 connects RAS3 to the upper halfword.',
    'With R1/R2 fitted as 0 ohms, the two ranks give 8 MiB physical capacity.',
    '',
    'If the rear chips are fitted but disabled, omit R1/R2 and fit R3/R4',
    'pull-ups so the rear RAS inputs remain inactive. This disables access',
    'to that rank. Populate only the front chips for a physically single-sided',
    '4 MiB module suitable for the intended adjacent-socket installation.',
    '',
    'Address mapping: front chips retain identity A0..A9. Rear chips reverse',
    'A0..A7 while preserving A8/A9. All ten-bit addresses remain bijective,',
    'and the 256-, 512- and 1024-row subsets are individually preserved.',
    'The finite permutation check establishes mapping equivalence; it does',
    'not validate timing or prove hardware refresh behaviour.',
    '',
    'PD1..PD4 each have independent, correctly connected ground straps.',
    'Actual population must follow the capacity/speed table. Strap population',
    'and resistor values are not represented in design-data.json and were',
    'therefore not verified by this logical net-map review.',
    '',
    'Scope: JSON circuit mapping only. This review does not compare the',
    'schematic netlist or routed PCB, check electrical timing, establish',
    'A4000 Chip RAM operation, confirm donor chips, or approve fabrication.',
    '',
    'Detailed assertions:',
]
lines.extend(f'PASS {description}' for description in checks)
report = '\n'.join(lines) + '\n'
report_path = root / 'docs/mapping-review.txt'
report_path.write_text(report)
print(f'{len(checks)} assertions passed; report: {report_path}')
