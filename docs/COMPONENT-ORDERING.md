# Component ordering: ten-module build

Prepared **19 October 2026** for the A7 PCB and **HY5118160JC-70** donor chips.
The recommended order covers **either ten 8 MB double-sided modules or ten
4 MB front-only modules**, or any mixture totalling ten PCBs, with passive
component spares. It is not the combined requirement for twenty modules.

## Exact fitted quantities

| Component | Package | 10 x 8 MB, both faces | 10 x 4 MB, front only | Maximum for either build |
|---|---|---:|---:|---:|
| HY8M A7 PCB | 72-pin SIMM | 10 | 10 | 10 |
| HY5118160JC-70 DRAM | SOJ42, 400 mil | 40 | 20 | 40 |
| 220 nF capacitors | 0805 imperial | 40 | 20 | 40 |
| 0 ohm links | 0603 imperial | 30 | 30 | 30 |
| 10 kohm pull-up resistors | 0603 imperial | 20 | 0 | 20 |

For an 8 MB / 70 ns board, the three zero-ohm links are **R1, R2 and PD3**;
R3/R4 are the two 10 kohm pull-ups. PD1, PD2 and PD4 remain open.
For a 4 MB / 70 ns board, the three zero-ohm links are **PD1, PD2 and PD3**;
R1-R4 and PD4 are unfitted. Only C1/C2 and U1/U2 are required on the 4 MB board.

Fitting C3/C4 without rear DRAMs does not increase memory capacity. If those
optional capacitors are fitted on all ten single-sided boards, forty capacitors
are required, still covered by the order below.

## Recommended DigiKey UK order

Choose **Cut Tape (CT)** for manual assembly. The following are component
selections within the existing BOM specifications; no circuit change is needed.
Package numbers are imperial: **0805 = 2012 metric**, **0603 = 1608 metric**.

| Item | Manufacturer part number | DigiKey cut-tape code | Order quantity | Spare allowance against maximum |
|---|---|---|---:|---:|
| 220 nF / 0.22 uF, X7R, +/-10%, 50 V, 0805 | Samsung **CL21B224KBFNNNE** | [1276-1093-1-ND](https://www.digikey.co.uk/en/products/detail/samsung-electro-mechanics/CL21B224KBFNNNE/3889179) | **50** | 10 |
| 0 ohm jumper, 0.1 W, 0603 | Yageo **RC0603JR-070RL** | [311-0.0GRCT-ND](https://www.digikey.co.uk/en/products/detail/yageo/RC0603JR-070RL/726675) | **50** | 20 |
| 10 kohm, +/-1%, 0.1 W, 0603 | Panasonic **ERJ-3EKF1002V** | [P10.0KHCT-ND](https://www.digikey.co.uk/en/products/detail/panasonic-industry/ERJ-3EKF1002V/198102) | **50** | 30 |

The 50 V capacitor meets the BOM's requirement for 16 V or higher; the SIMM
still operates from its existing 5 V supply. These capacitors are non-polarised.
Do not confuse 220 nF / 0.22 uF with 220 pF or 220 uF.

The [copy/paste ordering list](DIGIKEY-ORDER-10-MODULES.txt) contains two
tab-separated columns: DigiKey part number and quantity. Check the recognised
part numbers, quantities and Cut Tape packaging before checkout.

## Price and stock snapshot

The linked DigiKey UK pages were checked on **19 October 2026**. All three
selected parts were listed as active and in stock. These are displayed figures,
not reserved stock or an order confirmation.

| DigiKey cut-tape code | Stock displayed | Unit price at 50, GBP ex VAT | Price for 50, GBP ex VAT |
|---|---:|---:|---:|
| 1276-1093-1-ND | 823 | 0.02440 | 1.22 |
| 311-0.0GRCT-ND | 8,863,483 | 0.00640 | 0.32 |
| P10.0KHCT-ND | 2,119,912 | 0.01780 | 0.89 |
| **Parts subtotal** | | | **2.43** |

VAT and delivery are additional. The UK delivery banner currently states a
**GBP 22 charge below GBP 65**, with free delivery at GBP 65 or more. Delivery
therefore costs more than the components for this small standalone order;
combining with another parts order may be worthwhile. Confirm the final basket
price, tax and shipping method. Cut Tape avoids the separately listed
GBP 4.50 Digi-Reel reeling fee.

The Panasonic 10 kohm part was selected because the comparable Yageo
RC0603FR-0710KL was out of stock at DigiKey when checked. The board BOM specifies
the value/package, rather than requiring one resistor brand.

## Donor DRAM and PCBs

The PCB and donor components have already been ordered, as recorded in the
project status. They are separate from this passive-component shopping list.

Ten four-chip donor modules provide **forty DRAMs before removal losses**.
That is exactly enough for ten 8 MB boards, or enough for twenty 4 MB boards.
An additional suitable four-chip donor would provide four spare DRAMs if needed.
Confirm the actual chip markings and test donors before removal where possible.

No socket or separate edge connector is fitted to the module: the gold fingers
are part of the PCB. Solder, flux and cleaning materials are assembly consumables
and are not included in this component order.

If both batches are required, meaning **ten double-sided plus ten single-sided
boards**, the fitted totals are 20 PCBs, 60 DRAMs, 60 capacitors, 60 zero-ohm links
and 20 ten-kilohm resistors. A rounded passive order for that twenty-board case
is 100 capacitors, 100 zero-ohm links and 50 ten-kilohm resistors.

See [the assembly guide](ASSEMBLY.md), [the master BOM](../BOM.csv) and
[assembly options](../assembly-options.csv) for the authoritative populations.
This ordering list does not change the documented manufacturing-review and
hardware-testing status.
