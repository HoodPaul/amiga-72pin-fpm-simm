# A7 JLCPCB production-file review

**Reviewed: 20 October 2026.** No CAM change was found that blocks manufacture of this prototype batch. The review supports confirming the specific production files identified below. It does not establish operation of an assembled SIMM in an Amiga.

## Reviewed package

Archive: `JLCPCB - HY8M-SIMM-RevA7-Gerbers-Review_Y2(1).zip`

SHA-256:

```text
f9282f0e866511f561fe8a9710d5ce86f6a220ba5698b2a1964364fe20a96eca
```

All **14 original Gerber, drill and job files** retained in the package match the submitted A7 files byte for byte. The processed production layers were checked using parsed geometry, connected copper regions, drill coordinates, mask openings and rendered silkscreen. Finished-hole definitions were checked separately from drill-tool sizes.

## Findings

- **Profile and positions:** the 107.95 × 25.4 mm outline, key notch and left shoulder are preserved. The CAM origin moves by −105 mm in X and +111 mm in Y; there is no scaling, rotation or customer panelisation. Aligned profile, drill-centre and pad/track position differences are below 0.0001 mm, consistent with coordinate-format rounding.
- **Drills:** all 195 nominal 0.30 mm via drills remain. Both retaining-hole centres are unchanged. Their circular routed profiles became non-plated drill operations with an explicit **3.18 mm finished diameter** and **3.25 mm compensated tool diameter**. The larger tool value does not change the finished-hole target.
- **Contacts and routing:** all 72 contacts on each face, SOJ pads and outer track centrelines remain. Contact pitch and positions are unchanged; no shortening was identified. Most pad and track dimensions grow approximately 0.015 mm overall, consistent with etching compensation. Connected copper remains equivalent: 193 front regions, 177 rear regions, one L2 ground plane and 47 functional L3 regions, with no functional split or merge.
- **Inner-layer cleanup:** CAM removes 170 L2 and 93 L3 non-functional via pads. These pads were independently confirmed isolated from tracks and fill on their respective layers. All via drills/barrels, 25 ground-layer via connections and 102 functional L3 via connections remain. Six tiny dead-end tips of +5 V fill were trimmed without removing pads or track connections or disconnecting the remaining fill. Added mechanical clearances do not cut outer copper.
- **Mask:** all 336 original component/contact openings remain, enlarged approximately 7.5 µm per edge. The auxiliary plugging layer identifies all 195 vias and does not add exposed via openings to the solder mask.
- **Silkscreen:** UK Computing and JMC artwork, PD labels, donor numbers, Front/Rear, contact numbers and rear tables remain correctly positioned. Some 0.12 mm text strokes increase to approximately 0.13 mm. Minor clearance trimming removes no letters, words or logos. No manufacturer product number was added.

## Prototype process and next action

The reviewed production specification records fifteen boards, four layers, nominal 1.2 mm thickness, 1 oz inner and outer copper, black mask, white silkscreen, **ENIG**, ink-plugged vias, **no bevel**, no customer/date code and no PCB assembly. Layer mapping is correct. Order screenshots specify 2 µin gold and deburring; CAM geometry cannot certify actual plating thickness, finishing quality, finished thickness or manufacturing tolerances.

At the 20 October review, these findings supported selecting **“Yes, please proceed to production”** for this reviewed package. No additional Gerber correction was identified. A different archive or later CAM revision needs its own comparison.

**Latest status, 24 October 2026:** Paul reports that fabrication of the 15 JLCPCB PCBs is complete and the boards are now in transit. Receipt, inspection, assembly and hardware testing remain pending. This shipping update does not alter the reviewed files or establish electrical operation.

**Previous update, 21 October 2026:** Paul reported the PCBs in manufacture and donor RAM in transit. Production-file confirmation was no longer outstanding. Donor delivery has not subsequently been confirmed.

JLCPCB explains the original/processed folders and confirmation steps in
[How to confirm the production file](https://jlcpcb.com/help/article/how-to-confirm-the-production-file).

The project remains a prototype. Assembly, timing, refresh, socket fit and Amiga hardware operation are untested. The original CAD findings and the limits of CAD validation remain documented in [validation.txt](validation.txt). See [fabrication options](FABRICATION-OPTIONS.md) for the current process record.
