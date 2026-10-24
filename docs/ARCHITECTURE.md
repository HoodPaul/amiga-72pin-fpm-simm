# A7 design architecture

This is a navigation guide to the delivered design, not a new electrical review.

## Main design and supporting evidence

| Area | Current files and purpose |
| --- | --- |
| Native project | `HY8M-SIMM.kicad_pro`, `.kicad_sch`, `.kicad_pcb` at repository root |
| Local libraries | `HY8M.kicad_sym`, `HY8M.pretty/`, project library tables |
| Assembly variants | `variants/`, individual BOMs and DNP-marked schematics/netlists |
| Common population data | `BOM.csv`, `assembly-options.csv`, `docs/assembly-variants.json` |
| Saved checks/research | `docs/`, including XML, DRC JSON, mapping and copper comparison |
| Manufacturing exports | `fabrication-review/gerbers/`, four copper layers plus masks/silk/paste/outline/drill/job files |
| Preservation/reference tools | `source/`, retained A6 and uploaded artwork baselines |
| Historical routing | `routing/`, not the authority for a routine current-board update |
| Illustrative previews | `previews/`, not photos or measured fabricated results |

## Circuit and mechanics

The current design is 72-pin, 32-bit non-parity 5 V FPM. Two 1M ×16 DRAMs form
a 4 MiB rank on the front; a second rear pair provides 8 MiB total. R1/R2 enable
the rear RAS paths and R3/R4 provide their documented pull-ups. PD straps identify
physical capacity/speed; they do not select a faster DRAM grade.

Physical copper order is F.Cu, In1.Cu GND, In2.Cu mixed signals/+5 V fill, B.Cu.
There is no separate fifth power plane. Nominal outline is 107.95 × 25.4 mm with
1.2 mm ordered thickness. Saved tracks, pads, filled zones, contacts, notch and
retaining-hole geometry are preservation invariants unless deliberately revised.

A3 introduced accepted four-layer routing; A4–A7 preserve that copper while
changing artwork/reference presentation. A7 adds the JMC artwork to the uploaded
manual baseline. Preserve the UK Computing/JMC positions and attribution.

## Authority and limits

Current native CAD defines layout, selected variant files define fitting,
manufacturer-reviewed CAM defines the specific processed package, and physical
tests establish actual performance. These are separate evidence layers.

Read [compatibility research](compatibility-research.md) for host wiring and
part sources, [source workflow](../source/WORKFLOW.md) for safe editing and
[testing](TESTING.md) for known findings. Do not infer hardware success from a
connected schematic or CAD appearance image.
