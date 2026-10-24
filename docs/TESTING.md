# Verification and hardware evidence

## Documentation-only checks

For shipping/handover changes, check dates, owner attribution, links, assembly
values and the Git diff. Verify that native CAD, BOMs, libraries, Gerbers, drills
and archived reports have not changed. Do not regenerate them merely to update status.

## Saved-data tools

Run from the project root in an isolated copy, following [source workflow](../source/WORKFLOW.md):

```sh
python3 source/compare_copper.py
python3 source/review_mapping.py
python3 source/verify_project.py
```

The copper audit compares saved geometry with the retained references and writes
comparison reports. The mapping review writes its own report. The verifier reads
current native CAD plus main/variant XML and DRC JSON, checks export freshness,
and writes validation reports. These tools do not require native KiCad to inspect
existing exports, but CAD changes require fresh KiCad exports before verification.
They are not replacements for fresh DRC/ERC or electrical testing.

## Existing baseline findings

The dated [validation report](validation.txt) records 864 tracks, 195 vias,
zero unconnected items and the independent 321-assertion mapping review.
It also records:

- 144 J1 contact-edge findings: 0.2286 mm native setback versus the generic 0.50 mm rule.
- 46 schematic-parity warnings, with their causes described in the report.
- Seven ignored DRC check types in the existing project settings.
- No included ERC report.

Do not hide these findings or claim that the board has a clean DRC/ERC. The
[JLCPCB review](JLCPCB-PRODUCTION-REVIEW.md) covers a specific processed package,
including contact compensation and finished/tool drill sizes. Manufacturing
completion or a selected factory electrical test does not prove an assembled
module works in an Amiga.

## Physical acceptance

Use [HARDWARE-TEST-LOG.md](HARDWARE-TEST-LOG.md) to record receipt inspection,
assembly, actual motherboard/revision, configuration, test utility/version,
observed capacity, duration and failures. Inspect unpowered first; do not force
an unbevelled board into a socket or energise a suspected short.

Test the intended 4 MB and 8 MB Fast configurations and the 8 MB-as-2 MB Chip
experiment separately. Record cold/warm starts, sustained memory/retention work
and graphics/DMA behaviour as actually tested, not assumed. Do not invent a
universal pass duration or claim comprehensive timing validation from one utility.

## Reporting

Every result needs date, source revision/batch identity, tools/settings, scope,
actual outcome and limitations. Separate owner reports from independently
observed measurements. Preserve failed tests and identify untested variants.
No physical pass has been supplied at the 24 October 2026 checkpoint.
