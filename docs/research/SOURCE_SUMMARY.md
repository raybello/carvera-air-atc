# Source research: existing Carvera Air ATC work

| Source | Link | What it is |
|---|---|---|
| Warioo, *Carvera Air ATC Mod* (Instructables, 2026-02-22, upd. 2026-10-29) | https://www.instructables.com/Carvera-Air-ATC-Mod/ | The complete build: BOM, STEP files, wiring, firmware commands. License **CC BY-NC-ND 4.0** |
| Hackster News (Cameron Coward) | https://www.hackster.io/news/you-can-add-an-atc-to-your-makera-carvera-air-33040c3d7130 | News write-up of the above. Notes the <$100 BOM, and that the magazine sits far right and costs some X travel |
| Demo video | https://www.youtube.com/watch?v=ZFGinEx2lbY | Short demo |
| Community firmware | https://github.com/Carvera-Community/Carvera_Community_Firmware | ≥ 2.1.0c-RC1 required; `atc.detector.enable` added in the 2026-03-08 dev build |
| Community controller | https://github.com/Carvera-Community/Carvera_Controller | Matching controller |
| PDFs saved by the owner | `docs/research/*.pdf` (gitignored) | Offline copies |

## Key facts (from the guide)
- Makera pre-wired the Air for an ATC: the head has an **"ATC motor"** cable (JST-PH 6-pin) and an **"ATC sensor"** cable, and the board has a spare driver socket. The firmware treats it as a C1 once you run `fset func 5`.
- Mechanism: a 50:1 geared NEMA17 drives a 24T HTD-5M pulley, which drives a 24T pulley on the **manual collet-lever cylinder** (1:1). A cam on the bottom pulley trips a roller microswitch (COM + NC, fail-safe).
- Magazine: 8 spring-loaded pods (3 springs each, 0.4 × 4 × 17 mm) at **20 mm pitch**. It bolts to an **SMW fixture plate** with 2× M6 (holes 180 mm apart). Stock-MDF and Funssor mounts were "coming soon" and don't exist yet.
- Tool presence: M12 laser sensor (GTRIC LS05-S12N1), aimed under the magazine lip. Its 24 V output is inverted to input **0.21** (EXT connector, yellow wire).
- DRV8825 VRef ≈ **0.55 V** for the 1.58 A motor. Upstream swapped the inner 2 motor wires.
- Upstream warnings: gear and pod bore dimensions are critical (may need reprints); mill the magazine bottom flat; Tinmorry PETG-CF specifically worked well.
- Upstream TODOs (opportunities for us): no gerbers or STEP for the inverter board, no TMC2209 guide, no stock-bed mount, no chip caps.

## Measured from the STEP files (`scripts/step_to_stl.py`)
See `upstream_part_dimensions.md`. Highlights:
- TopGear and BottomGear are both **24 T HTD-5M**, OD 37.04 (pitch Ø 38.2), so the ratio is 1:1.
- BottomGear bore **Ø14.06** (lever cylinder). TopGear bore **Ø8.1** + 3 mm key (gearbox shaft).
- Magazine body 27 × 199.3 × 59.5 mm. M6 holes at Y +93.5 / −86.5 (180 mm pitch) in model coordinates, one with a Ø11 counterbore. 8 pod bores Ø8.1 at 20 mm pitch.
- `TopGear_v2_milled_keyway` = a Ø28 × 4 mm metal inlay meant to be **machined on the Carvera** (fits our "made by the CNC" goal).

## Product-relevant gaps (feed Phase 2)
1. A mount for the **stock bed** (largest user base). We have a first cut: `cad/custom/atc_bed_adapter`.
2. **One-board electronics**: opto input + connectors + optional AS5600 clamp-angle sensing instead of the microswitch.
3. **Pre-crimped harnesses** (the biggest friction for buyers).
4. Machined magazine (HDPE/Delrin/Al) instead of a long, delamination-prone print.
5. Clear calibration tooling (slot teaching, bore coupons).
