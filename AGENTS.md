# AI instructions: Amiga 72-pin FPM SIMM

## Read first

Read [README.md](README.md), [current handover](docs/AI-HANDOVER.md), [documentation index](docs/README.md), [source workflow](source/WORKFLOW.md) and the feature-specific record before editing. This is a hardware/CAD project, not an application requiring a web framework, database or server deployment.

Verify the current branch, HEAD and working tree. Preserve unrelated work. Use the current repository and Paul's latest instructions rather than older chat summaries. When evidence conflicts, identify the mismatch; never silently rewrite electrical data to match memory.

## Authoritative files and preservation

The delivered `HY8M-SIMM.kicad_pcb`, schematic, project-local libraries and selected variant BOM/DNP schematic define the design. `source/WORKFLOW.md` explains reference baselines and generation hazards. KiCad 10.0 or newer is the established project requirement.

Preserve accepted routing, component positions, outline, notch, contacts, saved zone copper, layer allocation and artwork unless the task explicitly requires a design change. UK Computing remains front-left, JMC front-right; retain [NOTICE.md](NOTICE.md) and template credits. Do not assign a project licence or assume artwork rights beyond the notice.

Do not run historical generation/routing scripts as routine maintenance. `apply_a7_artwork.py` and `finish_board.py` replace the current PCB from a saved baseline, and `create_assemblies.py` can replace assembly edits. Never run them merely to update documentation or shipping status.

## Electrical and assembly constraints

- Current revision A7 is a common four-layer 4 MB front-only / 8 MB front-and-rear PCB, nominal 107.95 × 25.4 mm and 1.2 mm thickness.
- Follow `BOM.csv`, `assembly-options.csv` and the chosen `variants/` BOM/schematic. Current capacitors are **220 nF**, not the older 100 nF proposal.
- For 70 ns: 4 MB fits PD1/PD2/PD3 and leaves R1–R4 unfitted; 8 MB fits R1/R2 at 0 ohm, R3/R4 at 10 kohm and PD3, leaving PD1/PD2 open. PD4 stays open. Verify the selected build rather than transcribing an older jumper table.
- HY5118160JC-70 is the specified 70 ns DRAM; HY5118160BJC-60 is the documented 60 ns alternative. Similar names, EDO parts and different refresh organisations are not approved substitutes. PD straps do not make a chip faster.
- An 8 MB assembly intended to supply 2 MB Chip RAM remains an untested host-wiring inference, not an 8 MB Chip RAM upgrade or confirmed compatibility.

## Evidence and current manufacturing status

Paul reports on 24 October 2026 that fabrication of the 15 JLCPCB boards is complete and they are in transit. Do not mark them received, assembled or tested without new evidence. Donor RAM was last reported in transit on 21 October; no later receipt is confirmed.

The batch uses ENIG and no bevel, not the earlier selective hard-gold/bevel proposal. Do not change CAD/exports or reorder boards based on a status update. Keep CAD checks, manufacturer CAM review, fabrication progress, physical inspection and host testing separate.

Preserve the documented 144 contact-edge findings, 46 parity warnings, ignored DRC check types and lack of an included ERC report. Do not suppress findings or claim a clean DRC to make a release look complete.

## Validation and completion

Use [TESTING.md](docs/TESTING.md), selecting checks appropriate to the change. Verifiers can write reports; run in an isolated copy and review generated diffs. Never turn a successful saved-data comparison into a claim of measured timing, refresh or Amiga operation.

Update the relevant authoritative guide, current handover and dated history. Record source revision, actual checks, remaining work and next action. Open a focused draft PR for review; merge or order/upload fabrication files only under task-specific authorisation. No live ordering, CAD change, paid purchase or hardware test is implied by a documentation request.

This repository is public: omit order IDs, private tracking links, delivery addresses, credentials and personal customer information. Use British English, retain accurate attribution and avoid em dashes.
