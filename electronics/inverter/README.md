# Tool-sensor interface (24 V sensor → Carvera input 0.21)

**Why:** NPN M12 laser sensors like the GTRIC LS05-S12N1 put **+24 V on the signal line when not triggered**. The Carvera input is 3.3 V logic (LPC1768), so it must never see 24 V. Both options below do the same job: sensor HIGH → input pulled LOW (inverted). Firmware then reads it with `0.21!^`.

## Option A (recommended): PC817 optocoupler, galvanically isolated

```
 Sensor side                         Carvera side (EXT 4-pin, yellow = 0.21)
 +24V ─────────── sensor brown        
 GND  ─────────── sensor blue         
 sensor black (signal) ──[R1 4.7k 1/4W]──► PC817 pin1 (A)      PC817 pin4 (C) ──► 0.21 (yellow)
 GND ───────────────────────────────────► PC817 pin2 (K)      PC817 pin3 (E) ──► Carvera GND
                                                                (pull-up = MCU internal ^)
```
- LED current ≈ (24 − 1.2) / 4.7 k ≈ **4.9 mA** (CTR ≥ 80 % → can sink > 3.9 mA, far more than the pull-up needs).
- Parts: PC817C (LCSC **C20612594**), 4.7 k ¼ W, a 30 × 20 mm perfboard offcut, `cad/custom/stl/signal_board_box.stl`.
- Shortcut: a "1-channel PC817 optocoupler module" from Amazon.ca. Check that its input resistor suits 24 V (many are rated 12–24 V).

## Option B (upstream circuit): 2N2222 inverter

Signal → R2 10 k → base, base → R1 100 k → GND, emitter → GND, collector → 0.21. This is the schematic from Warioo's guide. It works, but it isn't isolated.

## Bench test before connecting (5 min)
1. Power the sensor from 24 V. Put a 10 k pull-up from PC817 pin 4 to 3.3 V (e.g. the Pico's 3V3) and measure pin 4.
2. No target: expect ≈ 0 V. Hold a tool in the beam: expect ≈ 3.3 V. If it's the other way round, use `0.21^` in config.
3. Only then cut and connect the **yellow wire of the EXT connector** with the machine **OFF**.

## Phase 2 note
This becomes part of a single small "ATC I/O board" (opto input, switch input, connectors; possibly an AS5600 clamp-angle sensor). Design it in KiCad and order it from JLCPCB with LCSC parts. You can reflow it on the hot plate.
