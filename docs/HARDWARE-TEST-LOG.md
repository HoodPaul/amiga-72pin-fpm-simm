# Hardware inspection and test log

## Current evidence, 24 October 2026

**No physical inspection, assembly or Amiga hardware test result is recorded.**
Paul reports fabrication complete and the PCBs in transit. Receipt is pending.
This is a log structure for future evidence; the checklist below has not been run.

## Receiving and pre-assembly checklist

- [ ] Record receipt date, counted quantity and a non-sensitive internal batch reference.
- [ ] Photograph both faces and inspect the A7 marking, outline/notch, holes, mask, silkscreen and UK Computing/JMC artwork.
- [ ] Measure connector thickness and inspect contacts/edges for damage or burrs. Do not infer exact finish thickness from colour or photographs.
- [ ] Confirm donor receipt, complete chip markings, condition and pin-one orientation. Test intact donors before desoldering where suitable equipment permits.
- [ ] Check new passive values/packages against the chosen variant BOM, including 220 nF capacitors.
- [ ] Assemble one reviewed variant; inspect joints, orientation and intended link population before scaling up.
- [ ] Perform suitable unpowered continuity/short checks against the schematic. Do not energise a suspected fault or force socket fit.

## Copy for each assembled module or configuration

```text
Test date/time and timezone:
Operator:
Module identifier (non-sensitive):
PCB revision / source commit / batch:
Assembly variant and BOM revision:
DRAM complete markings and donor checks:
Inspection and measured thickness:
Unpowered electrical checks:
Host model / motherboard revision / relevant configuration:
Socket positions and other installed memory:
Firmware / OS / test utility and versions:
Expected capacity:
Observed capacity:
Cold/warm-start observations:
Memory patterns, address range, test duration and actual results:
Retention/refresh observations and conditions:
Graphics/DMA observations (Chip RAM experiment):
Errors, temperatures or abnormal behaviour:
Result: NOT TESTED / PASS WITH STATED SCOPE / FAIL / INCONCLUSIVE
Limitations and next action:
Evidence paths (sanitised photos/logs):
```

Do not mark a variant passed until an actual result is recorded. One module's
pass does not certify all donors, assembled boards or motherboard revisions.
Keep private order/tracking/address information out of this public file.
