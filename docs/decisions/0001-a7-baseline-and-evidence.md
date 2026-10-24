# 0001: Preserve the manufactured A7 baseline and separate evidence

Recorded: 24 October 2026.

Status: Retrospective record of the existing preservation workflow and this
owner-requested documentation/shipping update. No new CAD approval is implied.

## Context

A7 contains accepted saved geometry and supplied artwork; historical generators
can replace later manual work. Manufacturer CAM review and assembly choices have
separate records. Paul now reports fabrication complete and PCBs in transit.

## Decision

Keep the delivered A7 CAD, BOMs and exports unchanged for this documentation task.
Record shipping as owner-reported progress. Preserve CAD findings and existing
manufacturing history, and require new physical evidence before changing test status.
Use AGENTS.md for shared instructions, a linked Claude entry point and a current
handover for continuation. Keep each technical subject in its established guide.

## Alternatives and consequences

Regenerating the design to update shipping would risk unrequested geometry changes.
Calling the module validated after fabrication would confuse bare-board checks
with assembled-host operation. Relying on old chat memory would reintroduce outdated
capacitor/PD values. Linked repository evidence avoids those errors, but requires
maintainers to update the handover and physical test log as work progresses.

Any later electrical/mechanical revision or different CAM package needs its own
source identity, review and verification. See [workflow](../../source/WORKFLOW.md),
[testing](../TESTING.md) and [fabrication record](../FABRICATION-OPTIONS.md).
