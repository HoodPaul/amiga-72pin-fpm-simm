# Hardware inspection and test log

## First hardware validation, 7 November 2026

**PASS WITH STATED SCOPE: successful initial Amiga 4000D memory detection and reported operation.** Five Rev A7 modules were fitted: one fully populated 8 MB double-sided module in the Chip RAM socket, detected as **2 MB Chip RAM**, plus four front-only 4 MB modules in the Fast RAM sockets, detected as **16 MB Fast RAM**. Kickstart Memory Scan reports **18.00 MB total, 2.00 MB Chip, 16.00 MB Fast and 0.00 MB Slow**. Paul reports the system alive and working and supplied photographs of the fitted modules and scan display.

Motherboard revision, memory diagnostic duration, pattern-test completion, refresh/retention, graphics/DMA and cold/warm boot repetition are not yet documented. The remaining two planned A4000D builds are not yet documented as tested. See the [full dated hardware report](2026-11-07-FIRST-A4000D-HARDWARE-TEST.md).

### Historical status on 24 October 2026

No hardware results had yet been supplied; the PCB order was reported manufactured and in transit. Receipt dates, shipment quantity verified, module IDs and measured board thickness remain unrecorded.

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
