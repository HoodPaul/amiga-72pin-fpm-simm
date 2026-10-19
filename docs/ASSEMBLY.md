# 70 ns assembly reference

The current donor is a four-chip HYM532220WG-70 module fitted with genuine,
readable HY5118160JC-70 devices. Each chip is a 5 V, 1M x16 FPM DRAM in the
42-pin, 400 mil SOJ package, with 1K refresh. The chip marking and package must
match; the module's advertised 8 MB capacity alone is not sufficient.

Test donor modules before removing chips where suitable test equipment is
available. Ten four-chip donors contain forty chips before removal losses.
Use new capacitors, resistors and links.

For quantities, selected supplier part numbers and a ten-module shopping list
with spares, see [component ordering](COMPONENT-ORDERING.md).

## Parts fitted per PCB

| Reference | Component | Package | 4 MB front only | 8 MB front and rear |
|---|---|---|---:|---:|
| PCB | HY8M A7 common board | 72-pin SIMM | 1 | 1 |
| U1/U2 | HY5118160JC-70 | SOJ42, 400 mil | 2 | 2 |
| U3/U4 | HY5118160JC-70 | SOJ42, 400 mil | Unfitted | 2 |
| C1/C2 | 220 nF, X7R, +/-10%, 16 V or higher | 0805 | 2 | 2 |
| C3/C4 | Same capacitors | 0805 | Unfitted | 2 |
| R1/R2 | 0 ohm links | 0603 | Unfitted | 2 |
| R3/R4 | 10 kohm resistors | 0603 | Unfitted | 2 |
| PD1/PD2 | 0 ohm links | 0603 | 2 | Unfitted |
| PD3 | 0 ohm link | 0603 | 1 | 1 |
| PD4 | Leave open | 0603 pads | Unfitted | Unfitted |

220 nF equals 0.22 microfarad. The capacitors are non-polarised.
Package names are imperial: 0603 is approximately 1.6 x 0.8 mm and 0805 is
approximately 2.0 x 1.25 mm. Observe IC pin-one markings on each face.

The exact machine-readable build files are:

- [4 MB /70 ns BOM](../variants/4MB-70ns/BOM.csv)
- [8 MB /70 ns BOM](../variants/8MB-70ns/BOM.csv)
- [All assembly options](../assembly-options.csv)

The common PCB and paste plots include every component position. Physical
population follows the selected variant BOM and DNP-marked schematic.

## Complete-system quantities

The intended set of one 8 MB assembly for the Chip RAM socket and four 4 MB
assemblies for Fast RAM requires five PCBs, twelve DRAMs, twelve capacitors,
fifteen 0-ohm links and two 10-kohm resistors. Three four-chip donors provide
the twelve DRAMs before removal losses.

Alternatively, three fully populated 8 MB assemblies require the same twelve
DRAMs for the intended Chip RAM plus Fast RAM arrangement.

These are population counts, not hardware validation. The A7 board has not yet
been demonstrated in an Amiga, including the intended 8 MB assembly supplying
2 MB of Chip RAM. See [compatibility-research.md](compatibility-research.md).

## 60 ns alternative

Separate 60 ns BOMs and schematics are retained under `variants`. They specify
HY5118160BJC-60 and different PD fitting. HY5118160JC-70 donor chips must use
the 70 ns assembly options; changing a PD strap does not change their rating.
