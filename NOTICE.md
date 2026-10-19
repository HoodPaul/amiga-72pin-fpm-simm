# Attribution and supplied artwork

## Project purpose and collaboration

This project was started to create RAM that visually matches Re-Amiga systems:
black PCB, white silkscreen and gold contacts and exposed pads. The common PCB
supports the planned 4 MB front-only and 8 MB front-and-rear assemblies.

The project is a collaboration between **Paul of UK Computing Limited**,
**Jon of JMC Electronics** and **AI assistance through Codex**.

The Hyundai HY5118160 devices were selected for their relatively low SOJ
package profile and the availability of suitable donor SIMMs through online
marketplaces during project planning.

## Original template and technical sources

The mechanical starting point for this project is
[wiretap-retro/72-pin-SIMM-KiCAD-Template](https://github.com/wiretap-retro/72-pin-SIMM-KiCAD-Template).
Credit for that original template belongs to wiretap-retro. The upstream README
states that its outline and contacts are based on the Samsung DRAM Module
KMM53216000CK/CKG datasheet.

The original template README is retained unchanged at
[source/template-README.md](source/template-README.md). The retained mechanical
source is [source/template.kicad_pcb](source/template.kicad_pcb).
Upstream was checked at commit `18e96d14967886655961f81003decb246f4ab043`.

The upstream repository has no separate LICENSE file. Its README gives informal
permission to use the open hardware. This project does not assign a new standard
licence to that upstream material. No project-wide licence has been selected.

Hyundai device specifications, Commodore schematics/manuals and JEDEC
presence-detect information are credited and linked in
[docs/compatibility-research.md](docs/compatibility-research.md).
Manufacturer datasheets and seller photographs are not bundled here.

## Supplied artwork and retention request

The UK Computing and JMC logos are supplied project artwork. The collaborators
ask that anyone sharing or adapting this project **keeps both logos in their
existing positions on the PCB**, including on manufactured boards, and retains
the collaboration and original-template credits in accompanying documentation.

The logos are intended to remain part of this PCB design. Their inclusion does
not grant permission for unrelated use of either brand or logo. This artwork
retention request does not change the upstream template's permissions or
establish a project-wide licence.

The custom circuit, routing and branding changes are documented in this project.
This is not a measured clone of a Hyundai donor PCB and is not an endorsed
Commodore, Hyundai, Samsung or wiretap-retro product.
