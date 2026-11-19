# Firmware config

- `atc_setup_commands.txt`: MDI commands, in order. Run `model` FIRST and record the value.
- `custom_tool_slots.txt`: goes on the **SD card root**. Format: `slot X Y Z` (machine coords, mm).
  - The starting values are Warioo's machine on an **SMW bed**: 8 slots, X = -10.208, Y from -49.312 in **-20 mm** steps, Z = -80.3.
  - **You must re-teach these.** Jog an empty holder into pod 1, read machine X/Y/Z, then fill the other slots at -20 mm Y pitch.
  - Stock bed + `atc_bed_adapter` (12 mm): Z will be about **12 mm higher** (≈ -68.3) as a starting guess.
- Revert to manual: `fset func <original>` (usually 2), then remove the belt and BottomGear and refit the lever.
