#!/usr/bin/env python3
"""Render STEP parts to PNG sheets: isometric shaded view + top view with overall dims.

Usage: .venv/bin/python scripts/render.py <step_dir> <png_dir> [--notes notes.json]
notes.json: {"part_stem": ["line 1", "line 2", ...]} printed on the sheet.
"""
import sys, json, pathlib
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cadquery as cq

def mesh(path):
    shp = cq.importers.importStep(str(path)).val()
    v, t = shp.tessellate(0.15, 0.3)
    return np.array([(p.x, p.y, p.z) for p in v]), np.array(t), shp.BoundingBox()

def shade(tri, light=np.array([0.4, -0.5, 0.75])):
    n = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    k = 0.35 + 0.65 * np.abs(n @ (light / np.linalg.norm(light)))
    base = np.array([0.20, 0.55, 0.85])
    return np.clip(base[None] * k[:, None] + 0.1, 0, 1)

def dim(ax, a, b, off, text, horiz=True):
    if horiz:
        ax.annotate("", (a, off), (b, off), arrowprops=dict(arrowstyle="<->", lw=1))
        ax.text((a + b) / 2, off, text, ha="center", va="bottom", fontsize=9, backgroundcolor="w")
    else:
        ax.annotate("", (off, a), (off, b), arrowprops=dict(arrowstyle="<->", lw=1))
        ax.text(off, (a + b) / 2, text, ha="right", va="center", fontsize=9, rotation=90, backgroundcolor="w")

def render(step, out, notes):
    V, T, bb = mesh(step)
    tri = V[T]
    fig = plt.figure(figsize=(13, 6.5))
    fig.suptitle(f"{step.stem}   —   {bb.xlen:.1f} × {bb.ylen:.1f} × {bb.zlen:.1f} mm (X×Y×Z)", fontsize=13, weight="bold")
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.add_collection3d(Poly3DCollection(tri, facecolors=shade(tri), edgecolor="none"))
    c = V.mean(0); r = max(bb.xlen, bb.ylen, bb.zlen) * 0.36
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(28, -55); ax.set_axis_off(); ax.set_title("Isometric")
    ax2 = fig.add_subplot(1, 2, 2)
    up = tri[np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])[:, 2] > 1e-6]
    from matplotlib.collections import PolyCollection
    ax2.add_collection(PolyCollection(up[:, :, :2], facecolors="#9cc8ec", edgecolors="none"))
    ax2.set_xlim(bb.xmin - 0.25 * bb.xlen - 8, bb.xmax + 0.1 * bb.xlen + 4)
    ax2.set_ylim(bb.ymin - 0.2 * bb.ylen - 8, bb.ymax + 0.1 * bb.ylen + 4)
    ax2.set_aspect("equal"); ax2.grid(alpha=0.3); ax2.set_title("Top view (mm, grid = model coords)")
    dim(ax2, bb.xmin, bb.xmax, bb.ymin - 0.1 * bb.ylen - 4, f"{bb.xlen:.1f}")
    dim(ax2, bb.ymin, bb.ymax, bb.xmin - 0.12 * bb.xlen - 4, f"{bb.ylen:.1f}", horiz=False)
    if notes:
        fig.text(0.02, 0.02, "\n".join(notes), fontsize=9, family="monospace", va="bottom")
    fig.savefig(out, dpi=110); plt.close(fig)

if __name__ == "__main__":
    src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]); dst.mkdir(parents=True, exist_ok=True)
    notes = json.loads(pathlib.Path(sys.argv[sys.argv.index("--notes") + 1]).read_text()) if "--notes" in sys.argv else {}
    for f in sorted(src.glob("*.step")):
        render(f, dst / (f.stem + ".png"), notes.get(f.stem)); print("rendered", f.stem, flush=True)
