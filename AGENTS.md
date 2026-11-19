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
| Q1c | Stock MDF bed thickness + bed-screw type/length | MDF = **15.0 mm**. Stock bed screw measured: thread Ø4.83, head Ø8.39 × 3.49, 3 mm hex, ~23 mm overall → **M5 low-head (DIN 7984), likely M5×20**. Replacement: **3× M5×30 DIN 7984** (2026-11-19) |
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
| 2026-11-19 | Z offset vs Warioo: MDF 15.0 + adapter 12.0 = 27.0 mm vs SMW plate 17.78 mm, so the pods sit **+9.22 mm higher**. Starting slot Z ≈ -71.1; safe_z_empty -40 → **-30.8** | Assumes the MDF bed and the SMW plate sit on the same base surface (SMW reuses the bed screws/standoffs) |
| 2026-11-19 | Stock bed screws are **M5 low-head**, not M6 (the SMW drawing's "M6 SHCS" refers to its own plate). Adapter bed holes: Ø5.5 thru + Ø9.6 × 3.8 counterbore. Replacement = **M5×30 DIN 7984** | Screw passes the 8.2 mm adapter floor + 15 mm MDF, leaving ≈6.8 mm in the base (≈1.4 d). M5×35 risks bottoming out. The low head keeps the counterbore shallow, so it clears the 7.6 mm-deep magazine nut pockets (0.85 mm min) |
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

## Project tracker artifact (owner's live dashboard)
- **URL:** https://claude.ai/artifact/NdJXdfvcmZJ89E6Wkyipub (private to the owner). Tabs: Overview, Build steps, Parts to buy, Print files, Firmware, Phase 2, Phase 3, Log.
- **Source:** `tracker/template.html` + `tracker/data/*.json` (steps, parts, phase scaffolds) + repo files (BOM CSV, firmware, CAD). Build with `python3 tracker/build.py` → `tracker/dist/` (gitignored: it contains upstream files). The supporting-files map is written to `tracker/dist_files.json`.
- **Publish/update:** Artifact tool, `url` = the URL above, `file_path` = `tracker/dist/index.html`, `root` = `tracker/dist`, `files` = contents of `tracker/dist_files.json`. Omit `capabilities` on redeploys (it keeps `db` + `downloads`). In a new session, `read` the artifact first.
- **Owner data lives in the artifact DB** (survives republishes). Read it with the ArtifactData tool at every checkpoint:
  - `state/checks` → `{items: {<stepId>: {done, at}}}` (Phase 1 steps, Phase 2 goals, Phase 3 deliverables)
  - `bom/<BOM id>` → `{status, price (CAD), vendor, ordered, eta, received, notes}`. Delivery days = received − ordered
  - `parts/<part id>` → `{status: todo|printing|printed|installed|reprint}`
  - `log/<id>` → `{date, phase, kind: milestone|feedback|issue|reprint|purchase|note, hours, cost, text}`
  - `shots/<shot id>` → `{status}` · `notes/<section id>` → `{text}` · `product/listing` → Phase 3 listing fields
- **Ids are stable:** never rename a step, BOM, part or shot id (the DB keys on them). Add new ids instead.
- **Checkpoint routine:** read the DB → fold prices, delivery times and feedback into BOM.md, BUILD_LOG.md and the Phase 2/3 docs → update `tracker/data/*.json` for new phase content → rebuild → republish → commit.
- **File transport:** the host serves no .step/.stl/.zip, so STEP ships as `.step.txt` and STL as base64 chunks (`.b64.N.txt`, ≤12 MB each). The page rebuilds a .zip in the browser with JSZip and saves it through the `downloads` capability.

## Session log
| Date | Agent | Summary |
|---|---|---|
| 2026-11-19 | Claude (Opus) | Set up the repo. Researched Instructables + Hackster (full text, 10 STEP files, tool-slot config, 18 photos). Converted and measured all upstream parts. Designed 5 original parts with dimensioned renders. Wrote the Phase 1 plan, BOM (LCSC-checked), firmware config, opto interface, Pico bench tester and licensing rules. |
| 2026-11-19 | Claude (Opus) | Owner confirmed the stock MDF bed. Pulled the bed interface from the SMW plate CAD; redesigned `atc_bed_adapter` (clamps through bed screws, dowel located, captive nuts, toolsetter relief); added `stock_bed_layout.png`; updated the plan, BOM and firmware notes (Z offset, safe-Z). T1 = back. |
| 2026-11-19 | Claude (Opus) | Owner verified the stock-bed screw positions to ±0.01 mm; the adapter is cleared for printing. |
| 2026-11-19 | Claude (Opus) | Recorded MDF = 15.0 mm; computed the +9.22 mm Z offset; updated the slot file comments and setup commands. |
| 2026-11-19 | Claude (Opus) | Owner measured the bed screw: M5 low-head. Adapter holes resized to M5 and nut pockets re-clocked (flat toward the counterbore, 7.6 deep); replacement M5×30 DIN 7984; docs and drawings updated. |
| 2026-11-19 | Claude (Opus) | Built and published the project tracker artifact (db + downloads): BOM order tracking (price, vendor, ordered/ETA/received), step checklists, custom + upstream part downloads, firmware with copy buttons, Phase 2/3 scaffolds, log. Seeded 2 log entries. |
