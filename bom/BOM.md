# Phase 1 BOM: Carvera Air ATC prototype

Machine-readable: [`phase1_bom.csv`](phase1_bom.csv). Prices are **rough CAD estimates (Nov 2026)**. Phone local stores to confirm stock before driving.

**Sourcing priority:** ① what you already own → ② Ottawa store → ③ Amazon.ca Prime (next day in Ottawa) → ④ LCSC (cheap, 3–5 days DHL; best for Phase 2 volume) → ⑤ StepperOnline / AliExpress.

## Must buy (≈ $150–190 CAD)
| # | Item | Spec | Qty | Best source | Ottawa local? | LCSC |
|---|---|---|---|---|---|---|
| M1 | **Geared stepper** | 17HS15-1584S-MG50: NEMA17, 50:1 planetary, 1.58 A, body ≤ 39 mm, 8 mm keyed shaft | 1 | [StepperOnline](https://www.omc-stepperonline.com/nema-17-stepper-motor-l-40mm-gear-ratio-50-1-mg-series-planetary-gearbox-17hs15-1584s-mg50) (~US$34) | ✗ | ✗ |
| M2 | **HTD belt** | Gates **425-5M-09** (5 mm pitch, 425 mm, 85 T, 9 mm) | 1 | Ottawa PT distributor (order-in) | ☎ call Motion / Applied Industrial / BDI | ✗ |
| M3 | Springs | 0.4 wire × 4 OD × 17 free | 24 (+spares) | Amazon.ca assortment | ? Lee Valley / Princess Auto | ✗ |
| M5 | M3 heat inserts | standard 3D-print insert | 8 | Amazon.ca kit | ? | ✗ |
| E1 | Roller microswitch | SPDT, 20×10×6, ~9.5 mm pitch | 1 | **LCSC C87120** Omron SS-5GL2 ($1.07) / Amazon KW11 pack | ✗ | **C87120** |
| E2 | DRV8825 module | Pololu footprint | 1 | Amazon.ca 5-pack | ? Canada Computers | C81582 (bare IC only) |
| E3 | Laser tool sensor | M12, 24 V, NPN, diffuse laser (GTRIC LS05-S12N1) | 1 | AliExpress (2–3 wk) / Amazon.ca equivalent | ✗ | ✗ |
| E4 | Opto interface | PC817C + 4.7 k ¼ W + perfboard | 1 | **LCSC C20612594** / Amazon module | ? | **C20612594** |
| E5 | JST-SM 2.54 kit | 2-pin + 4-pin pairs (+crimper) | 1 | Amazon.ca | ? | (PH alt: **C157952** PHR-6 + **C111515** SPH-002T) |
| F4 | M3 countersunk | 10–16 mm | 16 | Home Depot / Fastenal | ✓ | ✗ |
| F5 | M6×20 SHCS | ISO 4762 | 1 (+1 in F8) | Home Depot / Canadian Tire | ✓ | ✗ |
| F8 | **Stock-bed adapter hardware** | 3× **M5×30 DIN 7984 low-head** (stock = M5 low-head ~M5×20), 2× M6 hex nuts, M6×16 + M6×20, 4 mm dowel pin | 1 set | Fastenal Ottawa / Amazon.ca (low-head M5); rest Home Depot | ✓ verify low-head stock | ✗ |

## Probably have (check inventory)
M4×12 ×4, M4×10 ×2, M3×10 ×2 (your M3/M4 kit) · 10×2 mm magnets ×3 (measure yours) · CA glue · 3-core wire · PETG / PETG-CF filament.

## Stock bed (your machine)
`atc_bed_adapter`: print it in PETG first. Permanent version: 12 mm HDPE cutting board (IKEA / Dollarama / Canadian Tire) or 12 mm 6061 (Metal Supermarkets Ottawa). Hardware is line F8. Bed screws: buy **3× M5×30 DIN 7984 low-head** (stock ones are M5 low-head). Standard M5 socket caps won't fit: their 5 mm head is too tall for the counterbore.

## Your existing inventory: what's used
| You own | Phase 1 role |
|---|---|
| Flashforge AD5M | All printed parts (magazine body is 199.3 mm long and fits the 220 mm bed) |
| Carvera Air + stock material | Faces the magazine flat; mills the adapter, the TopGear metal inlay, and later the magazine |
| M3/M4 screws, standoffs, wire, soldering iron | Assembly, switch and sensor leads, opto board |
| Circular magnets | Cover retention (if 10×2) |
| PCB hot plate | Phase 2 SMD "ATC I/O board" |
| 2× TB6600 + Pi Pico | **Optional bench tester** for the motor and belt (`firmware/pico/bench_stepper.py`). Not installed in the machine: the Carvera drives the ATC from its own socket |
| 2× AS5600 | Optional encoder in the bench test; **Phase 2** candidate to replace the microswitch (absolute clamp angle + stall detection) |
| 50 mm linear stage (28BYJ) | No role found. Possible Phase 2 use: an auto dust lid over the magazine |

## LCSC check summary (2026-11-19)
| Part | LCSC # | Stock | Unit price |
|---|---|---|---|
| Omron SS-5GL2 roller microswitch | C87120 | 8,829 | $1.07 (1+) |
| PC817C DIP-4 optocoupler | C20612594 | 143k | $0.02 |
| DRV8825PWPR (IC, for Phase 2 board) | C81582 | 11,962 | $2.50 |
| JST PHR-6 housing | C157952 | 15,400 | $0.02 |
| JST SPH-002T-P0.5S crimp | C111515 | 6,200 | $0.007 |
| Motor, belt, springs, inserts, laser sensor | – | not carried | – |
