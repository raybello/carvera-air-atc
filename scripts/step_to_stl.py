#!/usr/bin/env python3
"""Convert STEP files to STL + print a dimensional report (bbox, volume, cylindrical bores).

Usage: .venv/bin/python scripts/step_to_stl.py <in_dir_or_file> <out_dir> [--report report.md]
"""
import sys, pathlib, collections
import cadquery as cq

def analyse(path):
    shape = cq.importers.importStep(str(path))
    solid = shape.val()
    bb = solid.BoundingBox()
    holes = collections.Counter()
    for f in shape.faces("%CYLINDER").vals():
        r = round(f._geomAdaptor().Cylinder().Radius(), 2)
        holes[r * 2] += 1
    return shape, bb, solid.Volume(), len(shape.solids().vals()), holes

def main():
    src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
    report = sys.argv[sys.argv.index("--report") + 1] if "--report" in sys.argv else None
    out.mkdir(parents=True, exist_ok=True)
    files = sorted(src.glob("*.step")) if src.is_dir() else [src]
    lines = ["| Part | Size X×Y×Z (mm) | Volume (cm³) | Solids | Cylindrical face Ø (mm) ×count |", "|---|---|---|---|---|"]
    for f in files:
        shape, bb, vol, n, holes = analyse(f)
        cq.exporters.export(shape, str(out / (f.stem + ".stl")), tolerance=0.02, angularTolerance=0.1)
        hs = ", ".join(f"{d:g}×{c}" for d, c in sorted(holes.items()))
        lines.append(f"| {f.stem} | {bb.xlen:.1f} × {bb.ylen:.1f} × {bb.zlen:.1f} | {vol/1000:.1f} | {n} | {hs} |")
        print(lines[-1], flush=True)
    if report:
        pathlib.Path(report).write_text("\n".join(lines) + "\n")

if __name__ == "__main__":
    main()
