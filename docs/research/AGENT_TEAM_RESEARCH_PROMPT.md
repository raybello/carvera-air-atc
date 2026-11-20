# Prompt: deep research team for a Carvera Air ATC kit

Paste everything below the line into the orchestrating AI. It assumes the AI can read the repo at `/Users/raybello/Github/carvera-air-atc` and run sub-agents.

---

You are leading a team of research agents. Your job is to produce a decision-grade research package for turning a working DIY prototype into a **standardized automatic tool changer (ATC) kit for the Makera Carvera Air** desktop CNC, sold to makers through voltpak.ca (Accessories category).

## Context you must load first
1. Read `/Users/raybello/Github/carvera-air-atc/AGENTS.md` in full. It is the project's source of truth: status, decisions, open questions and rules.
2. Then read, in this order:
   - `docs/research/SOURCE_SUMMARY.md`
   - `docs/research/upstream_part_dimensions.md`
   - `docs/phase1/BUILD_PLAN.md`
   - `bom/BOM.md`
   - `docs/LICENSING.md`
   - `firmware/config/`
   - `electronics/inverter/README.md`
   - `docs/phase2/README.md`
   - `docs/phase3/README.md`
3. Summarize back in 10 lines what the prototype is, before assigning any work.

### Key facts already established (don't re-research these, build on them)
- The Carvera Air ships without an ATC, but Makera pre-wired it for one:
  - **Wiring:** an "ATC motor" cable (JST-PH 6-pin) and an "ATC sensor" cable in the spindle head, plus a spare stepper-driver socket on the board.
  - **Firmware:** the Carvera Community Firmware (≥ 2.1.0c-RC1) enables the full Carvera's ATC routine with `fset func 5`.
- **The prototype replicates Warioo's Instructables mod** (CC BY-NC-ND 4.0, so the product must be a clean-room design):
  - A 50:1 geared NEMA17 drives a 24T HTD-5M pulley, which turns the manual collet-lever cylinder 1:1.
  - A roller microswitch reads clamp state.
  - An 8-pod spring magazine sits at 20 mm pitch.
  - An M12 24 V NPN laser sensor checks that a tool is present, through an opto interface to input 0.21.
- **The owner's machine has the stock 15 mm MDF bed.** The bed is held by M5 low-head screws. A custom adapter clamps through 3 of those screws and the 4 mm dowel at (142, −15).
- **Tool numbering:** T1 is at the back, next to the toolsetter; T8 is at the front.

## Research questions (the core of the job)

### RQ1: How does the machine know which tool is in the spindle and in each pod?
This is the most important question. Cover:
- **How the Carvera (C1) and the Community Firmware track tool state today:**
  - the current tool number
  - the tool table and tool-length offsets
  - what happens after power loss, a manual swap, or an aborted change
  - how the auto tool-length probe and the "ATC detector" input are used
- **Every identification method used by other machines, hobby or industrial:**
  - firmware state tracking only
  - tool-length signature matching
  - per-pod presence sensors
  - RFID/NFC tags in holders (Balluff, Haas, Tormach)
  - magnetic or hall-effect coding
  - optical, barcode or QR reading
  - camera-based identification
  - weight
  - capacitive sensing
  - collet/holder geometry keys
- **For each method:** how it works, accuracy, failure modes, cost at 1, 100 and 1,000 units, space it needs, and whether it can work inside the Carvera Air's existing firmware or needs a companion controller (e.g. RP2040 Pico + AS5600 / hall sensors / RFID reader talking to the machine).
- **Recommendation:** what a $200–$400 kit should do in v1, and what a v2 could add. Include a failure-mode table: wrong tool loaded, empty pod, tool pulled out of the collet, crash mid-change.

### RQ2: ATC mechanisms and prior art for desktop CNC
- **Commercial and open-source ATCs to survey:**
  - Makera Carvera (C1)
  - RapidChange ATC
  - Sienci Labs ATC
  - Onefinity / Millright / Shapeoko add-ons
  - Tormach TTS and ATC
  - Pocket NC
  - LinuxCNC / grblHAL / FluidNC / Klipper tool-change implementations
  - community Carvera Air mods (Makera forum, Reddit, Printables, Instructables, YouTube)
- **For each:** clamping method, tool-holder standard, magazine layout, sensing, firmware integration, price, install effort, and known problems from user forums.
- **Which ideas we can legally reuse:** we can reuse ideas, not files. Flag every patent you find (Google Patents), with number, claims summary and expiry, so we know what we can't copy.

### RQ3: Software and firmware
- **Carvera Community Firmware and Controller source** (GitHub: Carvera-Community): where the ATC code lives, the M6 flow, configurable parameters (`atc.*`), detector logic, and `custom_tool_slots.txt` handling. Link to the files and line ranges.
- **What a kit needs from software:**
  - setup wizard
  - slot teaching
  - tool-table sync
  - safety checks
  - a CAM post-processor
  - MakeraCAM / Fusion / FreeCAD tool libraries
- **What already exists, what's missing, and how to ship it:** for anything missing, recommend config bundle vs firmware fork vs PR upstream vs companion app. Check firmware license obligations (GPL) for shipping modified firmware.

### RQ4: Market, customers and pricing
- **Market size:** the Carvera Air installed base, as far as can be estimated (Kickstarter numbers, Makera statements, community size).
- **Who buys:** buyer personas and their top pain points with manual tool changes. Use real quotes with links from forums, Reddit and YouTube comments.
- **Competitors and substitutes:**
  - competitor pricing
  - upgrading to the full Carvera (price gap)
  - DIY
- **Our price:** the price point and the willingness-to-pay evidence behind it.
- **Selling in Canada:** shipping and duties for Canada/US, and how voltpak.ca fits.

### RQ5: Productization
- **Standardize the kit:**
  - Bed variants: stock MDF, SMW plate, Funssor.
  - Tool holder / collet standard.
  - Pod count.
  - Pre-crimped harnesses.
  - A single "ATC I/O" PCB with an opto input, a switch or AS5600 clamp-angle input, and an optional RFID/hall tool-ID input.
- **Manufacturing:**
  - parts made by the Carvera itself vs 3D printed vs outsourced (JLCPCB/LCSC, CNC services)
  - materials (PETG-CF, HDPE, Delrin, 6061)
  - unit cost at 10 / 50 / 200 / 1,000
- **Compliance and liability:**
  - CE/UKCA, FCC and ISED for any radio (RFID) or digital electronics
  - product liability for a machine-tool accessory
  - safe use of the "Carvera" and "Makera" trademarks ("for Makera Carvera Air", no logos)

### RQ6: Product and marketing material (research only, no final copy yet)
- **How the best desktop-CNC accessories are presented:** product pages, build guides, and YouTube/Instagram/X content.
- **What converts:** the claims that sell (tool-change time, number of tools, install time, "no drilling"), and the proof formats (demos, side-by-side, cost math).
- **A content inventory to capture during the build:** a shot list for B-roll of the build, use, purchase and unboxing.

## Team structure
- **You are the lead.** You plan, assign, check and merge. Don't do all the research yourself.
- **Sub-agents run on Claude Sonnet 4.6.** This is the project's rule (in Claude Code's Agent tool: `model: "sonnet"`).
- **Brief each sub-agent completely:** its research question, the files it should read, its sources, the output file path and format, and what "done" means.
- **Suggested agents** (split further if a question is large):
  1. Tool identification (RQ1)
  2. Mechanisms and patents (RQ2)
  3. Firmware and software (RQ3)
  4. Market and pricing (RQ4)
  5. Productization, cost and compliance (RQ5)
  6. Marketing and content (RQ6)
- **Run them in parallel where they don't depend on each other.** Have RQ5 read RQ1–RQ3's outputs before it finishes.
- **Add a final reviewer agent.** It checks every claim against its cited source, flags contradictions between reports, and lists what's still unknown.

## Rules
- **Cite everything.** Every factual claim gets a link (and a quote for numbers or user pain points). Mark anything unverified as "unverified". Never invent prices, specs, part numbers, patent numbers or quotes. "Not found" is an acceptable answer.
- **Prefer primary sources:** GitHub source, datasheets, Makera docs, patents and vendor pages. Note the date accessed.
- **Sourcing priority for parts:** Ottawa local store → Amazon.ca → LCSC (give C-numbers) → other online.
- **Units:** mm and CAD, with USD in brackets where useful.
- **Licensing:** don't copy or redistribute Warioo's files or anyone's CAD. Describe ideas and interfaces only. Respect CC BY-NC-ND and patents.
- **Repo boundaries:**
  - Don't change Phase 1 build files (`cad/custom/`, `firmware/config/`, `bom/`, `docs/phase1/`) or `AGENTS.md`'s decisions.
  - Write only to the output paths below.
  - Don't commit or push. The owner reviews first.
- **Phase gate:** this is research for Phases 2 and 3. Don't start designing or building the product. Recommend only.

## Deliverables (write to the repo)
- `docs/research/deep/RQ1_tool_identification.md` … `RQ6_marketing_content.md`. One report per question, each with:
  - summary
  - findings
  - comparison table
  - recommendation
  - open questions
  - sources
- `docs/research/deep/sources.csv`: every source, with columns id, title, url, type, date accessed, used in (RQ#).
- `docs/research/deep/EXECUTIVE_SUMMARY.md` (2 pages max):
  - the recommended v1 kit (mechanism, tool ID method, electronics, software, bed support)
  - target price and unit cost
  - top 5 risks with mitigations
  - the decisions the owner must make
  - a proposed Phase 2 plan with milestones
- `docs/research/deep/OPEN_QUESTIONS.md`: what you couldn't answer and how to find out (a measurement, a test, an email to a supplier).

## Definition of done
- All six reports exist, cite sources, and end with a clear recommendation.
- The reviewer has checked them, and contradictions are resolved or listed.
- The executive summary lets the owner choose the v1 tool-identification approach and kit configuration in one sitting.
- Your final message lists the files written, the top 3 findings, and the decisions waiting on the owner.
