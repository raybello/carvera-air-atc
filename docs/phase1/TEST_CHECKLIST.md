# Phase 1 test and calibration checklist

Tick the boxes as you go and log anything odd in `BUILD_LOG.md`.

## A. Power-on sanity (spindle OFF, no tool)
- [ ] Machine boots, no driver alarm, and the DRV8825 isn't hot after 2 min
- [ ] `version` shows Community FW ≥ 2.1.0c-RC1
- [ ] Main-button long press (1.2 s) → motor turns the lever cylinder. Wrong direction? Power off and swap one coil pair
- [ ] No skipped steps or belt jumping at full clamp. If it skips, raise VRef 0.05 V at a time (max ~0.75 V)

## B. Clamp sensor
- [ ] Switch reads open/closed correctly in Controller diagnostics
- [ ] Adjust the bracket height so the cam trips the roller **at the end of unclamp**, without bottoming out the lever
- [ ] Unplug the switch: the machine must refuse or alarm (fail-safe NC check)

## C. Tool-presence laser
- [ ] Beam spot sits right under the magazine lip
- [ ] Sensitivity: does NOT trigger on the black lid, DOES trigger on a tool shank
- [ ] Input 0.21 changes state in diagnostics. If it's inverted, switch `0.21!^` ↔ `0.21^`

## D. Slot teaching
- [ ] Home. Jog an empty holder over pod 1 and lower it until it's seated. Record X/Y/Z in `custom_tool_slots.txt`
- [ ] Repeat for pod 8 and check the pitch is 20.00 mm (skew → magazine not square to Y; re-seat it)
- [ ] Copy to the SD root and reboot

## E. Dry runs (spindle never spins)
- [ ] `M6 T1` from empty → picks T1
- [ ] T1 → T8 → T1 ×10 at reduced feed
- [ ] Remove a tool from a pod, call it → sensor catches it, no crash
- [ ] Full speed: 50 changes, zero faults

## F. Real cut
- [ ] 3-tool job (e.g. 3 mm flat → 1 mm flat → 90° chamfer) with auto tool-length probe
- [ ] Chips: check that pods and caps stay clean

## Exit → Phase 2
- [ ] Log total build hours, costs, every reprint and why, and every "this was annoying" moment
