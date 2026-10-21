# Project history

This records the saved design snapshots leading to A7. Earlier snapshots describe design work, not hardware-tested releases. The repository contains the current A7 project and selected references, rather than a complete copy of every previous directory.

## Revisions

| Revision | Saved design and principal change |
|---|---|
| A0, preliminary | Unrouted 8 MB schematic/placement draft: four HY5118160JC-70 devices, two per face; 107.95 mm length, provisional 22 mm height and proposed four-layer construction. |
| A1 | First fully connected routed draft. Six copper layers: four routing layers plus GND and +5 V planes. Height remained 22 mm. Rear data ordering and corresponding CAS byte enables were permuted to share front/rear connections. |
| A2 | Height increased to **25.4 mm**. ICs/capacitors moved upwards by 3.4 mm; contacts, retaining holes and notch stayed fixed. Two four-layer trials retained 18 missing-connection findings, so this snapshot used the completed six-layer fallback. |
| A3 | Completed the **four-layer, 25.4 mm** design. F.Cu/In2.Cu/B.Cu carry signals; In1.Cu is GND; In2.Cu also carries +5 V fill. Added common 4 MB/8 MB populations, rear-rank enable links and separate 60/70 ns assembly files. Placement/fanout changes included the rotated right IC pair, rear A0–A7 reversal, planned under-chip buses and symmetric notch bridges. |
| A4 | Silkscreen/showpiece revision. Added the white UK Computing logo, compact PD tables, Front/Rear and contact-number labels. Chip references and donor numbers were visibly below the footprints. Removed physical model/untested wording; the project's untested status did not change. Copper and mechanics matched A3. |
| A5 | Expanded the rear resistor legend to distinguish R1/R2 0 Ω links from R3/R4 10 kΩ pull-ups. No copper or mechanical change. |
| A6 | Moved chip references/donor markings inside the chip-body envelopes and Front/Rear towards the lower outer edges. Adjusted the rear legend wording. Copper and mechanics stayed unchanged. |
| A7 | Adopted the uploaded, manually edited **KiCad 10** PCB as the artwork baseline. Preserved that layout, added the 18.000 × 3.480 mm JMC logo on the front top right and updated revision text. The uploaded PCB already used PD1–PD4; schematic/BOM references were aligned to those names. Exact comparison found no moved copper, pads, components or board profile. |

A3 introduced the accepted four-layer routing; A4–A7 did not reroute it. Each layer is physical copper: the mixed In2.Cu signal/+5 V fill does not add another layer.

## A7 artwork and reference preservation

The user's edited layout retained the UK Computing artwork on the front left. Rear assembly instructions occupy the U4 body area, and the PD table occupies the U3 body area. They are visible on a front-only build and covered when rear ICs are fitted. JMC occupies x193–211 mm and y87.06–90.54 mm on front silkscreen.

The A7 artwork application starts from [the retained upload](../source/user-silkscreen-reference.kicad_pcb). It preserves the original board content except the intended revision wording and appended JMC silkscreen polygons. See [artwork-preservation.txt](artwork-preservation.txt).

The [retained A6 PCB](../source/copper-reference-A6.kicad_pcb) provides the earlier copper reference. The [portable comparison tool](../source/compare_copper.py) records A3–A6 source-file hashes and canonical geometry hashes, and compares A6, the upload and the current A7 PCB.

The comparison preserves:

- 864 track segments and 195 vias, including coordinates, widths, layers and nets.
- 336 pads and 17 component placements.
- 13 Edge.Cuts primitives, including the contacts' surrounding board profile, retaining holes and key notch.
- Two zone outlines and ten saved filled copper polygons.
- Four copper layers and the proposed 1.2 mm board thickness.

RPD1–RPD4 in older files and PD1–PD4 in A7 are component-reference aliases. KiCad version changes to numeric layer/net identifiers, UUID fields and save order are normalised; they are not treated as physical movement. No zone refill is performed by the audit.

## Manufacturing-package correction

An A7 packaging review removed two obsolete A6 inner-layer Gerber duplicates. The native PCB and current A7 exports were unchanged. The corrected package contains exactly four copper layers, described in [layer-file-map.txt](layer-file-map.txt) and the Gerber job manifest.

## Manufacturing progress

**19 October 2026:** donor components were ordered and PCBWay quotation/order
settings were documented, including selective hard gold and a proposed bevel.

**20 October 2026:** the PCBWay price was too high for this prototype batch, so
the project moved to JLCPCB. An order for **15 boards** was placed with four
layers, nominal 1.2 mm thickness, 1 oz inner/outer copper, black mask, white
silkscreen, ENIG 2 microinch, ink-plugged vias, deburring and no bevel. Edge
plating, assembly, stencil and manufacturer mark were not selected. The layer
sequence was explicitly checked against the four-layer file map.

JLCPCB's returned production archive was compared with the original A7 files.
All fourteen original files matched byte for byte. The processed geometry
preserves all 72 contacts per face, the functional copper connections, all
195 via positions, the outline/notch and artwork. CAM compensation, removal
of isolated inner-layer pads and small dead-end fill tips were reviewed.
The retaining holes remain 3.18 mm finished, with 3.25 mm compensated tools.
No functional connection change or production-blocking correction was found.
See [the detailed review](JLCPCB-PRODUCTION-REVIEW.md).

The order's “1 item Requires Action” was the requested production-file
confirmation. The review supported confirmation for this prototype batch.

**21 October 2026:** Paul reported that the donor RAM is **in transit** and
the **15 new JLCPCB PCBs are in manufacture**. Assembly, socket fit and Amiga
hardware testing remain pending. This status update does not change the
native A7 PCB or original Gerbers.

No revision has been physically validated in an Amiga. The intended 8 MB assembly providing 2 MB Chip RAM remains an inference from host wiring. CAD connectivity and mapping checks are separate from timing, refresh, fit and hardware testing.

The inherited native contact setback remains 0.2286 mm against the 0.50 mm
generic edge rule; JLCPCB compensation reduces it to approximately 0.221 mm.
No bevel is selected for this batch. Finished thickness, edge quality, donor
health, assembly and socket fit still require inspection. A7 remains an
unvalidated prototype design; the CAM review does not establish hardware
operation or qualify another manufacturer's process.

See [validation.txt](validation.txt) for current check results and [the README](../README.md) for assembly options, fabrication issues and attribution.
