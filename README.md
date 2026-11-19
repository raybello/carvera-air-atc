# carvera-air-atc

An automatic tool changer (ATC) upgrade for the **Makera Carvera Air**. It starts from a community-proven prototype and grows into a maker kit, sold at [voltpak.ca](https://www.voltpak.ca).

> Status: **Phase 1, prototype.** See [`AGENTS.md`](AGENTS.md) for live progress and next steps.

## What it does
A 50:1 geared NEMA17 under the spindle cover drives the collet lever through an HTD-5M belt. A roller switch confirms clamp and unclamp. An 8-pod spring magazine sits on the right of the bed, and an M12 laser checks that a tool is present. The Carvera Air already has the ATC wiring and firmware hooks (`fset func 5` on the Community Firmware).

## Start here
1. [`docs/phase1/BUILD_PLAN.md`](docs/phase1/BUILD_PLAN.md): step-by-step build
2. [`bom/BOM.md`](bom/BOM.md): parts and where to buy them (Ottawa / Amazon.ca / LCSC)
3. [`cad/custom/`](cad/custom/): our printable and machinable parts (STL, STEP, dimensioned renders)
4. [`firmware/config/`](firmware/config/): setup commands and tool-slot file

## Credits
The Phase 1 prototype follows **Warioo's** [Carvera Air ATC Mod](https://www.instructables.com/Carvera-Air-ATC-Mod/) (CC BY-NC-ND 4.0). Their files are **not** included in this repo; `scripts/fetch_upstream.sh` downloads them for personal use. See [`docs/LICENSING.md`](docs/LICENSING.md).

Not affiliated with or endorsed by Makera.
