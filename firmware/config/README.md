# Firmware config

- `atc_setup_commands.txt`: MDI commands, in order. Run `model` FIRST and record the value.
- `custom_tool_slots.txt`: goes on the **SD card root**. Format: `slot X Y Z` (machine coords, mm).
  - The starting values are Warioo's machine on an **SMW bed**: 8 slots, X = -10.208, Y from -49.312 in **-20 mm** steps, Z = -80.3.
  - **You must re-teach these.** Jog an empty holder into pod 1, read machine X/Y/Z, then fill the other slots at -20 mm Y pitch.
  - **Stock bed + `atc_bed_adapter` (this machine):** the pods sit about **12 mm higher** than Warioo's SMW setup (more if the stock MDF top sits above where an SMW plate's top would be). Starting guess Z ≈ -68; always re-teach it.
  - X/Y should land close to Warioo's values, because the adapter puts the magazine in the same place as on the SMW plate (flush right and front, T1 at the back by the toolsetter).
  - **Before the first ATC move,** raise `atc.safe_z_empty_mm` and `atc.safe_z_offset_mm` by the same height difference (e.g. -40 → -28). Do the first runs with a hand on the e-stop.
- Revert to manual: `fset func <original>` (usually 2), then remove the belt and BottomGear and refit the lever.
