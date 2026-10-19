# Fabrication options and outstanding review

These are the PCBWay quotation selections discussed on 19 October 2026.
As of that date, donor components have been ordered and the PCB order has been
submitted. The PCB is awaiting the manufacturer's engineering verification and
approval before manufacture. The settings below record the intended order
specification; manufacturer approval is still outstanding. No price or delivery
date is guaranteed by these files.

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

## Ordering screenshot reminders

These screenshots were supplied on **19 October 2026** to record the PCBWay
order selections. Use them alongside the settings above and the four-layer
file map below. Manufacturer engineering approval of the contact/bevel
geometry and finished stack-up is still outstanding.

### Main order settings

Black solder mask, white silkscreen, 1.2 mm finished thickness, 6/6 mil
capability, 0.30 mm minimum drill and 1 oz outer/inner copper. **Remove product
No.: Yes** means the manufacturer's product number should be omitted.
The pictured **45-degree bevel remains subject to engineering approval**.

![PCBWay main order selections](pcb-ordering/pcbway-order-settings.png)

### Gold-finger plating

The edge-connector selection is hard gold, **Au 30 microinch over Ni
120 microinch**. This should agree with the selective-finish setting below.

![PCBWay hard-gold finger thickness selection](pcb-ordering/pcbway-gold-finger-plating.png)

### Selective finish and plating note

The combined finish is **immersion gold plus selective hard gold**:
1 microinch immersion gold on the component pads, with Au 30 microinch over
Ni 120 microinch hard gold on the SIMM fingers. The screenshot records this
note for the manufacturer:

> hard gold on all 72 SIMM edge contacts on both faces, with ENIG on the remaining component pads

![PCBWay selective finish, thickness and contact-area note](pcb-ordering/pcbway-selective-finish.png)

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
