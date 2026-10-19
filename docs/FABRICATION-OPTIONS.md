# Fabrication options and outstanding review

These are the PCBWay quotation selections discussed on 19 October 2026.
They are proposed order settings, not a completed order or manufacturing
approval. No price or delivery date is guaranteed by these files.

| Parameter | Selected/intended option |
|---|---|
| Supply form | Individual boards; quote quantity ten |
| Copper layers | Four |
| Actual outline | 107.95 x 25.4 mm; quoting interface rounds length to 108 mm |
| Material | FR-4, S1000H TG150 |
| Finished thickness | Proposed 1.2 mm, tolerance/socket fit to be confirmed |
| Track/spacing capability | 6/6 mil, covering the saved 0.20 mm geometry |
| Minimum drilled hole | 0.30 mm |
| Solder mask | Black |
| Silkscreen | White |
| UV colour printing | None |
| Edge connector | Yes; selective hard gold on contacts on both faces |
| Hard-gold plating | Au 30 microinch over Ni 120 microinch |
| Remaining component pads | ENIG, immersion gold 1 microinch |
| Via covering | Tented according to the Gerber mask data |
| Outer/inner copper | 1 oz /1 oz |
| Manufacturer product number | Omit from PCB |
| Stencil/assembly service | Not selected; manual assembly planned |

The hard-gold area is all 72 SIMM edge contacts on each face. The component
pads use ENIG. Gold/nickel thickness fields in both the edge-connector and
combined-finish selections should agree. These process requirements are not
encoded by the Gerber artwork alone.

## Physical layer order

| Layer | Gerber |
|---|---|
| L1, front | HY8M-SIMM-F_Cu.gtl |
| L2, GND | HY8M-SIMM-In1_Cu.g1 |
| L3, signals/+5 V fill | HY8M-SIMM-In2_Cu.g2 |
| L4, rear | HY8M-SIMM-B_Cu.gbl |

Only current A7 exports are included. Obsolete A6 inner-layer duplicates were
removed. See [layer-file-map.txt](layer-file-map.txt) and the Gerber job file.

## Bevel and contact-edge review remains open

The quotation selects a 45-degree bevel, but the native design does not define
its depth, remaining tip thickness or machining tolerance. The contact copper
starts 0.2286 mm from the insertion edge; PCBWay's published gold-finger guide
specifies a minimum 0.5 mm setback. This requires explicit engineering
acceptance or a design change before manufacture.

Ask PCBWay to confirm the finished mating thickness and tolerance; the bevel
cross-section on both faces; whether it intersects the existing fingers; the
remaining usable plated contact length; inner-layer copper clearance; and how
the 25.4 mm board height and key notch will be handled during bevelling.

For a symmetrical ideal 45-degree bevel on a 1.2 mm board, keeping the bevel
entirely before the 0.2286 mm copper setback would require at least 0.7428 mm
remaining tip thickness. This is a geometric observation, not an approved
socket or machining specification.

PCBWay's published ordinary-process guidance flags boards below 45 mm in the
dimension perpendicular to the connector edge. Their engineering team must
confirm an appropriate panel or fixture process for this outline.

References:

- [PCBWay gold-finger guide](https://www.pcbway.com/pcb_prototype/PCB_Gold_fingers.html)
- [PCBWay edge-connector order guidance](https://www.pcbway.com/helpcenter/ordering_parameter_instruction/Edge_Connector.html)
- [PCBWay bevelling requirements](https://www.pcbway.com/helpcenter/Engineering_Questions/The_requirement_of_beveling_on_gold_finger_area.html)

The 144 documented copper-edge DRC errors remain in the supplied reports.
No assembled-board operation, timing, refresh or Amiga compatibility test has
been completed. Read [validation.txt](validation.txt) and
[the fabrication notes](../fabrication-review/READ-BEFORE-ORDERING.txt).
