#!/usr/bin/env python3
"""Build the ATC project tracker page (claude.ai Artifact) from repo data.

    python3 tracker/build.py          -> tracker/dist/index.html + files/*.zip + img/*.png

Static reference content (BOM spec, steps, parts, firmware, phase scaffolds) is
embedded in the page. Everything that changes as you work (done marks, prices,
order/ETA/received dates, print status, log entries, product-page fields) lives in
the artifact's database, so republishing never loses it.
Re-run and republish at every checkpoint.
"""
import csv, json, pathlib, shutil, base64, datetime

ROOT = pathlib.Path(__file__).resolve().parents[1]
T = ROOT / "tracker"
DIST = T / "dist"
CAD = ROOT / "cad/custom"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "files").mkdir(parents=True)
    (DIST / "img").mkdir()

    bom = list(csv.DictReader((ROOT / "bom/phase1_bom.csv").open()))
    steps = json.loads((T / "data/phase1_steps.json").read_text())
    parts = json.loads((T / "data/parts.json").read_text())
    phases = json.loads((T / "data/phases.json").read_text())
    notes = json.loads((CAD / "src/render_notes.json").read_text())

    # Part files are served as text (the artifact host serves no .step/.stl/.zip):
    #   STEP -> files/<name>.step.txt (raw text), STL/PNG -> files/<name>.<ext>.b64.txt (base64).
    # The page fetches them and builds the .zip in the browser (JSZip) when you click Download.
    def pack(src, key):
        if not src.exists():
            return None
        if src.suffix == ".step":
            out = DIST / f"files/{key}.step.txt"; shutil.copy(src, out)
            return {"paths": [str(out.relative_to(DIST))], "name": src.name, "enc": "text"}
        if src.suffix == ".png":  # served as an image already
            out = DIST / f"img/{key}.png"; shutil.copy(src, out)
            return {"paths": [str(out.relative_to(DIST))], "name": src.name, "enc": "bin"}
        data = base64.b64encode(src.read_bytes()).decode()
        CH = 12_000_000   # stay under the 16 MB per-text-file limit
        paths = []
        for i in range(0, len(data), CH):
            out = DIST / f"files/{key}{src.suffix}.b64.{i // CH}.txt"
            out.write_text(data[i:i + CH]); paths.append(str(out.relative_to(DIST)))
        return {"paths": paths, "name": src.name, "enc": "b64"}

    for p in parts["custom"]:
        pid = p["id"]
        p["files"] = [f for f in (pack(CAD / f"step/{pid}.step", pid), pack(CAD / f"stl/{pid}.stl", pid),
                                   pack(CAD / f"renders/{pid}.png", pid)) if f]
        shutil.copy(CAD / f"renders/{pid}.png", DIST / f"img/{pid}.png")
        p["notes"] = notes.get(pid, [])
        p["img"] = f"img/{pid}.png"
    up = ROOT / "third_party/warioo-atc"
    if (up / "step").exists():
        stems = sorted({u["file"] for u in parts["upstream"]} | {"TopGear_v1"})
        upfiles = {}
        for stem in stems:
            key = "up_" + stem
            upfiles[stem] = [f for f in (pack(up / f"step/{stem}.step", key), pack(up / f"stl/{stem}.stl", key),
                                          pack(up / f"renders/{stem}.png", key)) if f]
            if (up / f"renders/{stem}.png").exists():
                shutil.copy(up / f"renders/{stem}.png", DIST / f"img/{key}.png")
        for u in parts["upstream"]:
            u["files"] = upfiles[u["file"]]
            u["img"] = f"img/up_{u['file']}.png"
        shutil.copy(up / "custom_tool_slots.txt", DIST / "files/custom_tool_slots_original.txt")
        parts["upstream_all"] = [dict(f, name=f"{stem}/{f['name']}") for stem in stems for f in upfiles[stem]] + \
            [{"paths": ["files/custom_tool_slots_original.txt"], "name": "custom_tool_slots_original.txt", "enc": "text"}]
    else:
        print("WARNING: third_party/warioo-atc missing; run scripts/fetch_upstream.sh for upstream downloads")
    layout = CAD / "renders/stock_bed_layout.png"
    shutil.copy(layout, DIST / "img/stock_bed_layout.png")
    lay = pack(layout, "stock_bed_layout")
    parts["custom_all"] = [dict(f, name=f"{p['id']}/{f['name']}") for p in parts["custom"] for f in p["files"]] + [lay]

    fw = {
        "setup": (ROOT / "firmware/config/atc_setup_commands.txt").read_text(),
        "slots": (ROOT / "firmware/config/custom_tool_slots.txt").read_text(),
        "bench": (ROOT / "firmware/pico/bench_stepper.py").read_text(),
        "opto": (ROOT / "electronics/inverter/README.md").read_text(),
    }

    data = {
        "built": datetime.date.today().isoformat(),
        "bom": bom, "steps": steps["groups"], "parts": parts, "phases": phases, "fw": fw,
        "repo": "https://github.com/raybello/carvera-air-atc",
    }
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = (T / "template.html").read_text().replace("/*__DATA__*/null", blob)
    (DIST / "index.html").write_text(html)
    size = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    files = sorted(str(f.relative_to(DIST)) for f in DIST.rglob("*") if f.is_file() and f.name != "index.html")
    (T / "dist_files.json").write_text(json.dumps({f: f for f in files}, indent=0))
    print(f"built {DIST/'index.html'}  ({size/1024:.0f} KiB total, {len(files)} supporting files -> tracker/dist_files.json)")


if __name__ == "__main__":
    main()
