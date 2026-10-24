# Development and editing

## Environment

Use Git, Python 3 and KiCad 10.0 or newer for native project work. The portable
comparison/mapping/verifier scripts use Python's standard library. PCB rendering
requires a matching KiCad `pcbnew` environment, and PNG appearance generation
also requires CairoSVG. There is no application server, database or frontend build.

## Safe workflow

1. Clone the repository, inspect HEAD/status and read [AGENTS.md](../AGENTS.md).
2. Create a focused branch and independent checkout/worktree. Preserve manual work.
3. Identify whether the task is documentation, assembly population, artwork, electrical connectivity or mechanical layout. A shipping update changes documentation only.
4. Before CAD changes, preserve the source revision and use [source/WORKFLOW.md](../source/WORKFLOW.md). Do not run the historical generation/routing pipeline to reopen the board.
5. Use the selected variant BOM and DNP-marked schematic. Do not copy a generic SOJ pinout or old chat jumper table without source verification.
6. Run relevant checks in an isolated copy and inspect their output/diff. Re-export netlists/DRC after CAD changes; old exported files cannot validate a changed design.
7. Update the current handover, affected guides and consequential decisions. Open a draft PR with evidence and remaining limitations.

## Generation hazards

`apply_a7_artwork.py` and `finish_board.py` reconstruct the main PCB from the
retained uploaded baseline, replacing later manual edits. `create_assemblies.py`
regenerates variant files. Older build/routing/fill scripts can replace accepted
geometry or artwork. None is a routine documentation-maintenance command.

The comparison and verification tools write reports even when they preserve
native CAD. Keep newly generated reports separate from dated evidence until
reviewed. Git checkout times can affect the verifier's export freshness checks;
a genuinely fresh export is preferable to touching a stale file to bypass it.

## Manufacturing changes

Keep the already manufactured A7 baseline traceable. Any new design or CAM
package needs its own revision/source identity, export review and documented
acceptance. Use a clean export directory to avoid obsolete duplicate inner layers.
Do not upload or order boards merely because the repository can generate files.
