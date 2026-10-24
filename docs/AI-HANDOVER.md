# AI handover: Amiga 72-pin FPM SIMM

Last updated: 24 October 2026.

Reviewed source baseline: `5a90faf34ac0664407d348f80cab60a2ef8e9f58` on `main`.
This identifies the source reviewed before this documentation change, not a
claim that a later checkout or manufacturing batch uses that exact commit.

## Resume here

Read [AGENTS.md](../AGENTS.md), the [documentation index](README.md),
[main README](../README.md) and [source workflow](../source/WORKFLOW.md).
The project is the A7 common PCB for 4 MB single-sided and 8 MB double-sided
5 V FPM modules, intended for Amiga 4000 experiments. Paul of UK Computing,
Jon of JMC Electronics and AI assistance through Codex are credited collaborators.

## Current position

- **24 October 2026, owner report:** fabrication of the **15 JLCPCB PCBs is complete and the boards are in transit**. No independent carrier verification was performed.
- Receipt, finished-board inspection, assembly, socket fit and Amiga testing remain pending. Do not describe the first prototype as operational.
- Donor RAM was last reported in transit on 21 October. No later donor receipt or passive-component purchase confirmation has been supplied.
- Production-file review is complete for the package identified in [JLCPCB review](JLCPCB-PRODUCTION-REVIEW.md). Do not repeat its historical confirmation step or assume it validates another package.
- Current order finish is ENIG 2 microinch, with no bevel, black mask and white silk. The older PCBWay hard-gold/bevel proposal is historical.
- This change adds AI/project guides and updates status only. Native CAD, libraries, BOMs, Gerbers, drills and validation reports are unchanged. No new KiCad, electrical or physical testing is claimed.

## Important corrections to older chat context

Use the delivered BOM: capacitors are **220 nF / 0805**, not 100 nF. The 70 ns
4 MB build fits PD1/PD2/PD3; the 8 MB build fits only PD3 amongst PD links.
PD4 stays open. R1/R2 are 0 ohm rear-rank links and R3/R4 are 10 kohm pull-ups
for 8 MB only. See [assembly options](../assembly-options.csv) and
[assembly guide](ASSEMBLY.md), which remain authoritative.

The 2 MB Chip RAM goal uses the four-chip 8 MB assembly with unused capacity;
it is not a separately validated 2 MB module. The two-module 8 MB Fast RAM
configuration also remains a host-wiring inference pending tests.

## Established validation limits

Saved reports record 864 tracks, 195 vias, zero unconnected items and 321 logical
mapping assertions. They also retain 144 contact-edge errors, 46 parity warnings
and seven ignored DRC check types. No ERC report is included. The native CAD/DRC
figures remain dated saved-data findings and were not rerun for this change.

On 24 October, `source/review_mapping.py` was rerun against the reviewed
`docs/design-data.json` in a separate working copy: **321 assertions passed**.
The generated report was not substituted for the archived repository report.
This verifies JSON logical mapping only, not native CAD parity, timing or hardware.
Read [testing](TESTING.md) and [compatibility research](compatibility-research.md).

## Next actions

1. Review this documentation PR; merge only when authorised.
2. When boards arrive, record receipt and inspect quantity, thickness, edges, contacts, mask/silk and artwork before fitting.
3. Confirm donor arrival and complete chip markings; test donors before removal where equipment permits. Confirm the passive parts against the selected BOM.
4. Follow [assembly](ASSEMBLY.md), then use the [hardware test log](HARDWARE-TEST-LOG.md) for staged inspection and actual host results.
5. Keep failed/unproven configurations visible and distinguish source findings from physical measurements. Record future circuit changes as a new reviewed revision; preserve the manufactured A7 baseline.

Do not invent tracking, arrival dates, measured results, successful tests or
manufacturer certificates. Update this current record after each meaningful
session, with PR/commit, real checks and outstanding work. Keep manufacturing
history in [PROJECT-HISTORY.md](PROJECT-HISTORY.md) rather than duplicating it.
