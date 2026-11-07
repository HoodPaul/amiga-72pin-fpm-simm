# First successful Amiga 4000D hardware test: 7 November 2026

**Status: successful initial memory recognition and reported operation.** This is a documented hardware milestone for the custom **Rev A7 72-pin FPM SIMM** project, not an assertion that comprehensive stability testing has been completed.

## Test configuration

| Item | Observed or reported outcome |
| --- | --- |
| Host | Commodore Amiga 4000D (motherboard revision not supplied) |
| Board design | Rev A7, four-layer custom 72-pin FPM SIMM |
| DRAM | Hyundai HY5118160JC-70, 70 ns FPM, recovered from donor SIMMs |
| Chip RAM | One fully populated **8 MB double-sided** module in dedicated Chip RAM socket; **2.00 MB Chip RAM detected** |
| Fast RAM | Four **4 MB front-only (single-sided)** modules in four Fast RAM sockets; **16.00 MB Fast RAM detected** |
| Utility | Kickstart Memory Scan; version not supplied |
| Screen result | **18.00 MB Total Memory Detected** |
| Breakdown | **Chip 2.00 MB; Fast 16.00 MB; Slow 0.00 MB** |
| Operation | Paul reports that the system is alive and working |
| Evidence | Photographs of installed modules and the memory scan supplied by Paul in the project conversation on 7 November 2026 |
| Full diagnostic tests | No completed memory-pattern, sustained refresh/retention, graphics/DMA, cold/warm restart, or timed stress-test result supplied |

## Significance

The physical **8 MB** double-sided module is recognised as **2 MB Chip RAM** by this A4000D, as originally intended. This is **not** an 8 MB Chip RAM upgrade; the remaining 6 MB is not available to the host as additional Chip RAM.

The four 4 MB front-only modules are recognised together as the full **16 MB Fast RAM** complement. Thus **both principal Rev A7 assembly variants have achieved successful initial host recognition together in one machine**.

These results replace the earlier 'no prototype assembled or tested' project status for this particular configuration. They do not demonstrate the alternative layout of two double-sided 8 MB modules in Fast slots 1 and 3, nor do they validate other motherboard revisions or all assembled PCBs.

## Donor inventory background

Six donor Hyundai SIMMs were photographed after arrival in late October 2026. The identified memory chips were marked **HY5118160JC-70**. Donor PCB revisions included **6B18AA**, **6B17AA** and **6B15AA**; these markings describe donor PCB revisions rather than different chip specifications.

## Remaining validation

- Run and record a complete memory-pattern test of all recognised RAM, including any errors and test duration.
- Check retention/refresh behaviour and Chip RAM graphics/DMA operation over sustained use.
- Record motherboard revision, module identifiers and cold/warm boot repeatability where practical.
- Build and independently test the remaining two intended A4000D sets. The planned three-system total is **three double-sided 8 MB physical Chip modules plus twelve 4 MB front-only Fast modules**.
- Keep alternative two-8 MB Fast configurations explicitly untested until measured.

## Preservation and provenance

This is an **owner-reported and photograph-supported hardware test** dated **7 November 2026**. Photos remain in the ChatGPT project conversation; binary photograph files have not been committed by this documentation update.

Do not change the accepted Rev A7 KiCad design, assembly BOMs, donor requirements, PCB routing, artwork, JLCPCB files, or historical CAM/DRC findings to reflect this milestone. In particular, initial host recognition does not supersede the separate need for full diagnostic validation.
