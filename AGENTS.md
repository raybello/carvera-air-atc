# AGENTS.md: Carvera Air ATC project hub

**Read this first in every session.** It's the single source of truth for status, decisions and next actions. Update it at the end of every session: the Status board, Next actions, and Session log.

## Mission
Add automatic tool changing (ATC) to the owner's **Makera Carvera Air**:
1. **Phase 1:** working prototype, replicating Warioo's proven mod. ← **CURRENT**
2. **Phase 2:** polish and optimize into a cheaper, smaller, easier kit. Clean-room design.
3. **Phase 3:** final product, build guide, firmware bundle, product images, a listing on **voltpak.ca → Accessories** (repo `/Users/raybello/Github/voltpak-web`), and promo content (HyperFrames video, B-roll plan, YouTube/IG/X).

**Do not start a later phase until the owner explicitly says so.**

### Hard requirements
- Parts should be **made with the Carvera itself** wherever practical (machined from cheap stock: HDPE, MDF, epoxy tooling board, 6061). 3D printing (Flashforge AD5M) is fine for speed in Phase 1.
- **Sourcing priority:** owned → **Ottawa local store** → Amazon.ca Prime → LCSC → other online. Always check LCSC part numbers.
- Get it installed **as soon as possible**.

## Status board
| Phase | State | Notes |
|---|---|---|
| 1 Prototype | 🟡 **Plan + files ready; waiting on owner to order and print** | See `docs/phase1/BUILD_PLAN.md` |
| 2 Optimize | ⚪ Not started | Goals in `docs/phase2/README.md` |
| 3 Product + content | ⚪ Not started | Goals in `docs/phase3/README.md` |

## ▶ Next actions for the owner (in order)
1. Note the MDF thickness and bed-screw length (Q1c), and answer Q2–Q5. The adapter positions are verified, so it's OK to print.
2. **Order the geared stepper today** (StepperOnline 17HS15-1584S-MG50; it's the critical path), then the rest of `bom/BOM.md`.
3. Run `./scripts/fetch_upstream.sh` (already run once on this Mac). Print `cad/custom/stl/bore_test_coupons.stl` first, then the upstream parts (`docs/phase1/BUILD_PLAN.md` §2).
4. Build the opto interface (`electronics/inverter/README.md`) and bench-test it.
5. Install (§4), set up the firmware (§5), and work through `docs/phase1/TEST_CHECKLIST.md`.
6. Log everything in `docs/phase1/BUILD_LOG.md`, then tell the agent "go Phase 2".

## Open questions (owner to answer, then agents record the answers here)
| # | Question | Answer |
|---|---|---|
| Q1 | Bed type: stock MDF / SMW fixture plate / Funssor? | **Stock MDF bed** (2026-11-19) |
| Q1b | Confirm right-column screw centres 23.5 mm from right edge, 10.5/104.25/185 mm from front | **Verified by owner to ±0.01 mm (2026-11-19)**: `atc_bed_adapter` geometry is final for printing |
| Q1c | Stock MDF bed thickness + length of the right-column M6 bed screws (to buy screws +12 mm) | _pending_ |
| Q2 | Is the AD5M nozzle hardened steel (for PETG-CF)? | _pending_ |
| Q3 | Size of the owned circular magnets (need 10×2 ×3)? | _pending_ |
| Q4 | Current firmware version; `model` output (record the number after CA1 → needed to revert) | _pending_ |
| Q5 | Owns the 4th-axis module / a spare DRV8825? | _pending_ |
| Q6 | Ottawa store stock confirmations (belt distributor, filament) | _pending_ |

## Key decisions log
| Date | Decision | Why |
|---|---|---|
| 2026-11-19 | Phase 1 replicates Warioo's Instructables mod as-is (8 pods, geared NEMA17 + HTD belt, roller switch, M12 laser sensor) | Proven, fastest path to a working machine |
| 2026-11-19 | Upstream files are **CC BY-NC-ND 4.0** → kept in gitignored `third_party/`; the product must be a clean-room redesign | `docs/LICENSING.md` |
| 2026-11-19 | Added original parts: stock-bed adapter, bore coupons, chip caps, signal-board box | Upstream gaps (stock bed unsupported; bores are critical) |
| 2026-11-19 | Owner has the **stock MDF bed**. The adapter clamps through the 3 right-column bed screws + the 4 mm dowel at (142,-15), with no drilling. The magazine sits where it would on the SMW plate (holes (140,80)/(140,-100)) | Bed interface read from the public SMW Carvera Air plate drawing/STEP (S1988 rev 2), which reuses the stock screw/dowel positions |
| 2026-11-19 | Tool numbering: T1 = back (next to the toolsetter), T8 = front | Upstream custom_tool_slots.txt: T1 Y=-49.3 → T8 Y=-189.3 |
| 2026-11-19 | PC817 opto interface preferred over the upstream 2N2222 inverter | Isolation; LCSC C20612594 |
| 2026-11-19 | TB6600 / Pico / AS5600 / linear stage are not installed in Phase 1; TB6600+Pico+AS5600 serve as an optional bench tester | The Carvera has its own driver socket and firmware support |

## Repo map
```
AGENTS.md                  ← this file (progress hub)
README.md                  ← public overview
bom/                       ← phase1_bom.csv (machine-readable), BOM.md (sources, LCSC, Ottawa)
cad/custom/src/parts.py    ← OUR parametric CadQuery parts → stl/, step/, renders/
cad/upstream/              ← (empty, reserved) upstream files live in third_party/ instead
third_party/warioo-atc/    ← GITIGNORED: upstream STEP/STL/renders/photos (CC BY-NC-ND)
third_party/smw/           ← GITIGNORED: SMW Carvera Air plate STEP + drawing (bed interface reference)
docs/phase1/               ← BUILD_PLAN.md, TEST_CHECKLIST.md, BUILD_LOG.md
docs/phase2/, docs/phase3/ ← goals and later deliverables
docs/research/             ← SOURCE_SUMMARY.md, upstream_part_dimensions.md, PDFs (gitignored)
docs/LICENSING.md          ← IP rules (read before any product work)
electronics/inverter/      ← 24 V tool-sensor interface
firmware/config/           ← MDI setup commands, custom_tool_slots.txt
firmware/pico/             ← bench_stepper.py (TB6600 + Pico + AS5600 test rig)
scripts/                   ← fetch_upstream.sh, step_to_stl.py, render.py, bed_layout.py (stock-bed drawing)
media/ marketing/ store/   ← Phase 3
```

## Toolchain
- Python venv: `python3 -m venv .venv && .venv/bin/pip install cadquery matplotlib numpy` (`.venv` is gitignored; it has already been created on this Mac).
- Rebuild our parts: `.venv/bin/python cad/custom/src/parts.py`
- Renders: `.venv/bin/python scripts/render.py cad/custom/step cad/custom/renders --notes cad/custom/src/render_notes.json`
- Upstream: `./scripts/fetch_upstream.sh && .venv/bin/python scripts/step_to_stl.py third_party/warioo-atc/step third_party/warioo-atc/stl`
- Slicer: OrcaSlicer (installed), Flashforge Adventurer 5M profile. KiCad is installed for the Phase 2 PCB.
- Downloads from instructables.com need a browser User-Agent and Referer (see the fetch script); plain fetches get 403.

## Rules for agents
1. **Sub-agents:** when work needs sub-agents (research fan-out, sourcing checks, CAD variants, copywriting drafts, etc.), launch them with **Claude Sonnet 4.6**. In Claude Code's Agent tool, pass `model: "sonnet"`. Give each sub-agent a complete brief (files, goal, done criteria) and verify its output before recording it here.
2. Never commit or push anything from `third_party/` or the research PDFs. Never put upstream geometry into `cad/custom/`.
3. Prefer Ottawa-local sources, and record LCSC part numbers (C-numbers) whenever a part exists there. Mark unverified store stock as "verify".
4. Keep units in mm. Keep dimensions measured from files traceable (`docs/research/upstream_part_dimensions.md`).
5. No Claude/AI attribution in commits or PRs.
6. End every session by updating: Status board, Next actions, Open questions, Decisions, and the Session log below.

## Session log
| Date | Agent | Summary |
|---|---|---|
| 2026-11-19 | Claude (Opus) | Set up the repo. Researched Instructables + Hackster (full text, 10 STEP files, tool-slot config, 18 photos). Converted and measured all upstream parts. Designed 5 original parts with dimensioned renders. Wrote the Phase 1 plan, BOM (LCSC-checked), firmware config, opto interface, Pico bench tester and licensing rules. |
| 2026-11-19 | Claude (Opus) | Owner confirmed the stock MDF bed. Pulled the bed interface from the SMW plate CAD; redesigned `atc_bed_adapter` (clamps through bed screws, dowel located, captive nuts, toolsetter relief); added `stock_bed_layout.png`; updated the plan, BOM and firmware notes (Z offset, safe-Z). T1 = back. |
| 2026-11-19 | Claude (Opus) | Owner verified the stock-bed screw positions to ±0.01 mm; the adapter is cleared for printing. |
