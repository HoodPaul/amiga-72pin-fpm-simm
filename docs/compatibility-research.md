# HY8M-SIMM A3 compatibility research

Research date: 18 October 2026. Target: original Amiga 4000 desktop motherboard with a Chip RAM SIMM socket. This document distinguishes documented host capabilities from electrical inferences for the new, untested module.

## Population options

Each HY5118160 is organised as 1,048,576 words × 16 bits, providing 2 MiB per IC. Two ICs form one 1M × 32 rank (4 MiB); four ICs form two such ranks (8 MiB). Physical sides and electrical ranks are distinct concepts, although the proposed PCB places one rank on each side.

| Module assembly | IC population | Electrical organisation | Intended installation | Host-visible capacity | Evidence status |
|---|---:|---|---|---:|---|
| 4 MiB Fast RAM | Two front-side ICs | One 1M × 32 rank | Four modules in Fast slots 1, 2, 3 and 4 | 16 MiB total | 4 MiB single-sided modules are explicitly documented by Commodore; this PCB remains untested |
| 8 MiB Fast RAM | Four ICs, two on each side | Two 1M × 32 ranks | Two modules in Fast slots 1 and 3; slots 2 and 4 empty | 16 MiB total | Supported by an electrical inference from motherboard rank-select wiring; not an explicit 8 MiB population in the cited user manual |
| 8 MiB assembly used for Chip RAM | Four ICs, two on each side | Two 1M × 32 ranks | Chip RAM SIMM socket U261 | Intended 2 MiB; 6 MiB unused | Rank organisation is consistent with the host wiring, but the underutilised 8 MiB module is outside Commodore's documented 1/2 MiB module capacities and requires hardware testing |

Commodore's User's Guide specifies 72-pin page-mode modules, 80 ns or faster, with a maximum height of 1 inch (25.4 mm). Fast modules must be physically single-sided when adjacent sockets are populated. Chip RAM modules may be single- or double-sided. The guide documents 1 MiB (256K × 32) and 4 MiB (1M × 32) Fast modules, and 1/2 MiB Chip modules. [1, printed pp. 4-2–4-4 and A-1–A-2]

## Motherboard rank-select wiring

The following is transcribed from the A4000 Rev B schematic. Slot numbers here count the four Fast sockets as slots 1–4, corresponding to U850–U853. Commodore's manual labels the same memory banks 0–3. SIMM /RAS0, /RAS1, /RAS2 and /RAS3 are connector signal names; host /RAS0–3 are the four RAMSEY bank selects.

| Socket | SIMM pin 44 (/RAS0) | SIMM pin 34 (/RAS2) | SIMM pin 45 (/RAS1) | SIMM pin 33 (/RAS3) |
|---|---|---|---|---|
| U850, Fast slot 1 / bank 0 | Host /RAS0 | Host /RAS0 | Host /RAS1 | Host /RAS1 |
| U851, Fast slot 2 / bank 1 | Host /RAS1 | Host /RAS1 | +5 V | +5 V |
| U852, Fast slot 3 / bank 2 | Host /RAS2 | Host /RAS2 | Host /RAS3 | Host /RAS3 |
| U853, Fast slot 4 / bank 3 | Host /RAS3 | Host /RAS3 | +5 V | +5 V |
| U261, Chip RAM | /CRAS0 | /CRAS0 | /CRAS1 | /CRAS1 |

Thus an 8 MiB two-rank module in U850 consumes the selects otherwise used by U850 and U851. The equivalent arrangement applies to U852/U853. Do not populate U851 or U853 alongside those two-rank modules. The 4 MiB front-only assembly uses SIMM /RAS0 and /RAS2, allowing all four Fast sockets to be populated. [2, sheet 15/17, PDF page 14]

All four SIMM byte enables remain independent: pin 40 /CAS0, pin 43 /CAS1, pin 41 /CAS2 and pin 42 /CAS3. The Chip RAM motherboard signal labels happen to run in the opposite order: those pins connect respectively to /CCAS3, /CCAS2, /CCAS1 and /CCAS0. This is a host naming convention and does not justify joining the CAS signals. [2, sheets 7/17 and 15/17]

## Configuration and presence detect

For the intended 4 MiB Fast ranks, motherboard jumper J852 uses the setting labelled **1M**, corresponding to pins 1–2 in the Rev B schematic. The alternative 256K setting is for 1 MiB Fast ranks. J852 applies to the Fast RAM section as a whole. The two 8 MiB modules still consist of 4 MiB ranks, so the same 1M setting follows from the schematic. No additional module rank-enable link is required when capacity is selected by IC population. [1, printed p. 4-3; 2, sheet 15/17]

The documented 1 MiB to 2 MiB Chip RAM upgrade requires no jumper change. The schematic's J213 2M setting is pins 1–2. An 8 MiB donor assembly used for 2 MiB Chip RAM must not be treated as an 8 MiB Chip RAM upgrade. No motherboard jumper changes are proposed by this PCB draft. For reference only, the Rev B schematic shows J214's normal VBB connection at pins 2–3 and explicitly reserves pins 1–2 for an 8M Alice; secondary web tables conflict with this, so the original schematic is the source here. [1, printed p. 4-4; 2, sheet 6/17, PDF page 5]

The JEDEC presence-detect codes below describe the physical module capacity and actual speed grade. A Chip RAM assembly containing 8 MiB retains its 8 MiB code even if the Amiga uses only 2 MiB.

| Assembly | Pin 67 / PD1 | Pin 68 / PD2 | Pin 69 / PD3 | Pin 70 / PD4 |
|---|---|---|---|---|
| 4 MiB, 60 ns | GND | GND | Open | Open |
| 4 MiB, 70 ns | GND | GND | GND | Open |
| 8 MiB, 60 ns | Open | Open | Open | Open |
| 8 MiB, 70 ns | Open | Open | GND | Open |

The A4000 motherboard schematic does not use these four presence-detect pins. The straps are nevertheless useful for correct module identification in other hosts. They do not increase the memory speed or select the populated ranks. [2; 3, JEDEC page 4.4.2-3, PDF page 3]

## Refresh and address permutation

The original HY5118160 datasheet specifies ten multiplexed row/column address inputs A0–A9, a ten-bit internal refresh counter, CAS-before-RAS, RAS-only, hidden and self-refresh support, and 1,024 refresh cycles per 16 ms for ordinary parts. [4, first page, printed p. 683]

Commodore's RAMSEY specification states that Fast RAM refresh is CAS-before-RAS. At 25 MHz its normal default interval is 9.52 microseconds. A 1,024-step internal refresh-counter cycle therefore takes approximately 9.75 ms, within the HY5118160's 16 ms limit. This calculation assumes normal RAMSEY configuration, rather than software disabling or excessively slowing refresh. [5, printed pp. 6-29 and 6-32–6-33, PDF pages 67 and 70–71]

For layout, reversing the rear ICs' A0–A7 connections while retaining A8 and A9 is a functional-equivalence inference. Apply the same fixed permutation to each multiplexed address pin for both row and column phases. Reads and writes then select the same permuted cell; the mapping is bijective. Since the high two bits are retained, the same accessible 256-, 512- or 1,024-row subset is preserved, and RAS-only refresh of that subset is not lost. CAS-before-RAS refresh uses the internal counter and is independent of the external address permutation. This does not constitute a manufacturer-approved pin-swap rule or a substitute for a complete memory test.

Chip RAM's underutilised-module operation is less directly documented. The Rev B motherboard generates its CMA9 signal using U212, rather than simply forwarding an Alice address pin. Keep the standard Chip RAM host configuration. The capacity estimate and address-permutation analysis require confirmation using the actual A4000, including sustained retention/refresh testing, graphics/DMA operation and CPU memory testing. No claim of tested 8 MiB-as-2 MiB operation is made for this new PCB. [2, sheets 6/17 and 7/17]

## Verified 60 ns alternative and speed grades

**HY5118160BJC-60 is a datasheet-supported 60 ns alternative for the existing HY5118160JC-70 footprint and connections.** The B-series manufacturer's datasheet lists the JC package, 60/70/80 ns grades, 5 V ±10% operation, 1M ×16 fast-page organisation and 1,024 refresh cycles per 16 ms. Its full 42-pin SOJ mapping matches the original non-B JC part. Package drawings match as well. This establishes documented pin, package, organisation, voltage and refresh compatibility; it does not establish tested operation of this new module in the user's A4000. [4, 6, 7]

| Characteristic | HY5118160JC-70 | HY5118160BJC-60 |
|---|---|---|
| Organisation / mode | 1M ×16, FPM | 1M ×16, FPM |
| Supply | 5 V ±10% | 5 V ±10% |
| Address inputs | A0–A9 | A0–A9 |
| Refresh | 1,024 cycles / 16 ms | 1,024 cycles / 16 ms |
| Package | JC, 42-pin 400 mil SOJ | JC, 42-pin 400 mil SOJ |
| Lead pitch | 1.27 mm | 1.27 mm |
| Body length range | 27.204–27.407 mm | 27.204–27.407 mm |
| Body width range | 10.033–10.287 mm | 10.033–10.287 mm |
| Overall lead width range | 11.0744–11.2776 mm | 11.0744–11.2776 mm |
| Package height range | 3.505–3.759 mm | 3.505–3.759 mm |
| Maximum RAS access, tRAC | 70 ns | 60 ns |
| Maximum CAS access, tCAC | 20 ns | 15 ns |
| Minimum page cycle, tPC | 45 ns | 40 ns |

The following table is a complete comparison of both 42-pin SOJ pinouts, viewed from the marking side. Both part columns match on every pin; the same pair of signal columns applies to both parts. [4, first-page SOJ pin drawing; 6, first-page SOJ pin drawing; 7, p. 3]

| Pin | HY5118160JC / HY5118160BJC | Pin | HY5118160JC / HY5118160BJC |
|---:|---|---:|---|
| 1 | VCC | 22 | VSS |
| 2 | DQ0 | 23 | A4 |
| 3 | DQ1 | 24 | A5 |
| 4 | DQ2 | 25 | A6 |
| 5 | DQ3 | 26 | A7 |
| 6 | VCC | 27 | A8 |
| 7 | DQ4 | 28 | A9 |
| 8 | DQ5 | 29 | /OE |
| 9 | DQ6 | 30 | /UCAS |
| 10 | DQ7 | 31 | /LCAS |
| 11 | NC | 32 | NC |
| 12 | NC | 33 | DQ8 |
| 13 | /WE | 34 | DQ9 |
| 14 | /RAS | 35 | DQ10 |
| 15 | NC | 36 | DQ11 |
| 16 | NC | 37 | VSS |
| 17 | A0 | 38 | DQ12 |
| 18 | A1 | 39 | DQ13 |
| 19 | A2 | 40 | DQ14 |
| 20 | A3 | 41 | DQ15 |
| 21 | VCC | 42 | VSS |

The verified assembly options can therefore specify **HY5118160JC-70 for 70 ns** and **HY5118160BJC-60 for 60 ns**. The B-series JC-70 is also documented in the same B-series family. All installed DRAMs must meet the speed printed on the module: a 70 ns chip must not be advertised as 60 ns merely by changing presence-detect straps.

Do not confuse the verified **HY5118160B** with **HY5116160B**. The latter is a 4K-refresh part whose extra row addresses A10/A11 occupy pins left NC in the 1K-refresh part; it is not approved by this comparison. Similar-looking part numbers, including HY5118164 variants, are not approved by this comparison. TSOP suffixes TC/RC do not fit the JC SOJ footprint. [6, 7]

## Primary documents

1. **Commodore A4000 User's Guide**, Commodore Electronics Limited, 1992, P/N 368 924-01. Printed pp. 4-2–4-4 and A-1–A-2; PDF pages 45–47 and 74–75 (one-based). <https://www.retromaniek.pl/wp-content/uploads/2019/04/Commodore-Amiga-4000-User-Guide.pdf>
2. **Commodore A4000 schematic 364836, Rev B**, Greg Berlin, 30 March 1992; AmigaWiki rebuilt copy Rev 1.37. Alice/control sheet 6/17 is PDF page 5; Chip RAM sheet 7/17 is PDF page 6; Fast RAM sheet 15/17 is PDF page 14 (one-based). <https://www.amigawiki.org/dnl/schematics/A4000_Rb.pdf>
3. **JEDEC Standard No. 21-C**, section 4.4.2, Release 6–7. Presence-detect truth table on JEDEC page 4.4.2-3, PDF page 3. <https://www.ele.uri.edu/iced/protosys/hardware/datasheets/simm/Jedec-Clearpoint-8MB.pdf>
4. **Hyundai HY5118160 Series**, 1AD15-10-MAY95. First page, printed p. 683, gives organisation, refresh and speed grades. Archived original manufacturer's scan. <https://datasheet.datasheetarchive.com/originals/scans/Scans-101/DSAIHSC000142689.pdf>
5. **Commodore A4000 Service Addendum**, RAMSEY Chip Specification. Printed pp. 6-29, 6-32 and 6-33; PDF pages 67, 70 and 71 (one-based). Functional specification pp. 6-3–6-4, PDF pages 41–42, also confirms the documented module capacities. <https://support.retrorewind.ca/media/commodore/amiga/a4000_service_manual.pdf>

6. **Hyundai HY5118160B Series**, 1AD54-10-MAY95. PDF p. 1 (printed p. 731): organisation, voltage, speed grades, refresh and SOJ pin drawing; PDF p. 2 (printed p. 732): ordering/package types; PDF p. 7 (printed p. 737): tREF; PDF p. 14 (printed p. 744): JC 400 mil SOJ package dimensions. Archived original manufacturer's scan. <https://www.dosdays.co.uk/media/hyundai/HY5118160B_Datasheet.pdf>
7. **Hyundai HY5118160B, HY5116160B**, Rev.00 / Sep.97. PDF p. 1: family grades and ordering information; p. 3: full SOJ pinout with NC distinction for the 1K-refresh part; p. 4: operating supply; p. 7: refresh limits. This later manufacturer's datasheet independently corroborates the B-series organisation and pinout. <https://pdf.dzsc.com/icpdf/5/57111/57111.pdf>

These are original manufacturer/standards documents hosted by archival mirrors. The schematic mirror describes its copy as a rebuild; it is not a physical continuity measurement of the user's motherboard. No physical fit, signal-integrity, electrical loading or hardware operation has been established for the A3 design.
