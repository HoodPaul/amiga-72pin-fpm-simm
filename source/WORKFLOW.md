# A7 development workflow

Open the project with **KiCad 10.0 or newer**. The main PCB is based on the
user's manually edited KiCad 10 file. The delivered native CAD is authoritative.
The uploaded artwork baseline is retained as
`source/user-silkscreen-reference.kicad_pcb`; the older unchanged copper reference
is `source/copper-reference-A6.kicad_pcb`.

## Verify preserved copper and mechanics

From the project directory:

```sh
python3 source/compare_copper.py
```

This portable Python tool needs no KiCad installation. It compares A6, the
uploaded board and the current main PCB with exact Decimal coordinates. It
writes `docs/copper-comparison.txt` and `.json`, and returns a non-zero exit code
if physical geometry differs. The historical A3–A6 file hashes and geometry
hashes are recorded in the tool and reports.

The checks cover tracks, vias, pad geometries/nets, component placements,
Edge.Cuts, zone outlines, saved filled polygons, other copper graphics, layer
allocation and board thickness. RPD1–RPD4 and PD1–PD4 are deliberate reference
aliases. Saved object UUIDs, numeric net IDs, layer IDs, whitespace and save
order do not constitute a moved track.

This is a saved-artwork comparison. DRC, schematic parity, ERC and hardware
validation have separate reports and are not implied by this result.

With the supplied KiCad 10 XML netlists and DRC JSON current, also run:

```sh
python3 source/review_mapping.py
python3 source/verify_project.py
```

The read-only verifier checks pad assignments, assembly populations and the
reported DRC/parity results without loading or saving CAD. Re-export the main
and four variant netlists and the DRC JSON after changing the schematics/PCB.

## Reapply the A7 logo to the uploaded artwork baseline

```sh
python3 source/apply_a7_artwork.py
python3 source/compare_copper.py
```

`finish_board.py` is a wrapper for `apply_a7_artwork.py`. Both rebuild the main
PCB from the retained uploaded baseline, preserve its existing artwork and PD
references, update A6 revision text to A7, and add the JMC artwork. They do not
regenerate placement, pads, tracks or zone fills. The JMC footprint is
`HY8M.pretty/Artwork_White_18mm.kicad_mod`; `source/JMC-source.png` and
`source/JMC-white.svg` retain its source and white vector artwork.

Reapplying the wrapper replaces subsequent manual changes to the main PCB with
the saved baseline plus the A7 logo. Preserve later manual work before using it,
and update the baseline deliberately when adopting a new manual layout.

After any artwork change, export the current PCB layers and rerun the relevant
KiCad checks. `render_appearance.py` uses the current native silkscreen/profile
SVGs and CAD pad geometry for the illustrative black/gold/white views. It needs
a matching KiCad `pcbnew` environment; PNG rendering also needs CairoSVG.
Colours and plating processes remain manufacturing order choices.

## Assembly references

The PCB, main schematic, all four variant schematics, BOMs and pin-map records
use **PD1–PD4**. The uploaded PCB already used those references. Their pads and
nets are the original RPD1–RPD4 circuits, unchanged electrically.

Use the selected variant BOM and DNP-marked schematic. The common PCB/paste
files include every footprint; a 4 MB front-only build omits the rear ICs,
rear capacitors and R1–R4. R3/R4 are 10 kΩ resistors on the 8 MB build, while
R1/R2 and fitted PD straps are 0 Ω links.

## Historical development scripts

`build_project.py`, routing preparation/import tools, `fill_power.py`,
`cleanup_dangling.py`, `even_notch_bridges.py` and the retained routing checkpoint
record the earlier circuit/routing development. They can regenerate older
artwork, component reference labels, placement or board-format assumptions.
Do not run that historical pipeline as a routine A7 artwork update.

`create_assemblies.py` regenerates assembly files and can replace their manual
changes. The delivered variant files and BOMs are the current assembly record;
regenerate and verify them deliberately after changing circuit or population.

The accepted board uses four physical copper layers: F.Cu/In2.Cu/B.Cu carry
signal routes, In1.Cu is GND, and In2.Cu also carries +5 V fill. The six-layer
fallback is not part of this delivered layout.

When exporting manufacturing files, start with an empty output directory.
KiCad versions can use different inner-layer extensions. Retaining older
exports alongside new ones can make an uploader detect duplicate layers.
The current A7 filenames and physical order are in docs/layer-file-map.txt.
