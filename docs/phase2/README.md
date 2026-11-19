# Phase 2: Polish and optimize (NOT STARTED, wait for owner go-ahead)

Inputs: `docs/phase1/BUILD_LOG.md`, `docs/research/SOURCE_SUMMARY.md` (gaps list), `docs/LICENSING.md`.

Goals:
1. **Clean-room CAD** for every part. Parametric CadQuery lives in `cad/custom/src/`, with no upstream geometry.
2. Mount for **stock bed + SMW + Funssor**; a magazine machinable on the Carvera itself from HDPE/Delrin/Al.
3. **One ATC I/O PCB** (KiCad → JLCPCB, LCSC parts): opto input, switch or AS5600 clamp-angle input, keyed connectors, maybe an onboard DRV8825/TMC2209.
4. **Pre-made harnesses** (JST-PH motor lead, sensor leads), so buyers don't crimp anything.
5. Cost model at 10 / 50 / 200 units (LCSC + JLCPCB + bulk motors + belts).
6. Faster install: aim for under 60 min, no cutting, plug-and-play sensor wiring.
