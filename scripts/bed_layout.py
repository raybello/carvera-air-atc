#!/usr/bin/env python3
"""Dimensioned top-view drawing: stock Carvera Air bed + ATC adapter + magazine + pods."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "cad/custom/src"))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import parts as P

fig, (ax, az) = plt.subplots(1, 2, figsize=(16, 9), gridspec_kw={"width_ratios": [1.5, 1]})
for a in (ax, az):
    a.add_patch(Rectangle((-153, -111), 306, 222, fc="#e9dcc3", ec="k", lw=1.2, label="Stock MDF bed 306 x 222"))
    a.add_patch(Circle(P.TOOLSETTER, 7.0, fc="white", ec="k", lw=1))
    for x, y in P.BED_SCREWS:
        a.add_patch(Circle((x, y), 5.0, fc="#555", ec="k")); 
    for x, y in P.DOWELS:
        a.add_patch(Circle((x, y), 2.0, fc="#c33", ec="k"))
    a.add_patch(Rectangle((116, -111), 37, 111 + P.NOTCH_Y, fc="#7fb3e0", ec="#1f5f99", lw=1.5, alpha=.85, label="ATC adapter 37 x 199.3 x 12"))
    a.add_patch(Rectangle((126, -111), 27, 111 + P.NOTCH_Y, fc="none", ec="#0b3", lw=2, ls="--", label="Magazine footprint 27 x 199.3"))
    for x, y in P.MAG_HOLES:
        a.add_patch(Circle((x, y), 3.3, fc="#ff0", ec="k", zorder=5))
    for i, (x, y) in enumerate(P.PODS):
        a.add_patch(Circle((x, y), 4.05, fc="none", ec="#0b3", lw=1.2, zorder=5))
        a.text(x - 9, y, f"T{i+1}", fontsize=8, ha="right", va="center", color="#063", zorder=6)
    a.set_aspect("equal"); a.grid(alpha=.25)

ax.set_xlim(-165, 175); ax.set_ylim(-125, 125)
ax.set_title("Stock Carvera Air bed (top view, origin = bed centre, +Y = back)")
ax.text(0, 0, "+", ha="center", va="center", fontsize=14)
ax.legend(loc="lower left", fontsize=8, framealpha=.95,
          handles=ax.patches[:1] + [ax.patches[-1 - 8 - 2 - 1], ax.patches[-1 - 8 - 2]] +
          [Circle((0, 0), 1, fc="#555", label="9x M6 bed hold-down screws"),
           Circle((0, 0), 1, fc="#c33", label="4 mm dowel locations"),
           Circle((0, 0), 1, fc="#ff0", ec="k", label="Magazine M6 (nut trap)")])
for lbl, xy in [("x=-142.5", (-142.5, 82)), ("x=-5.5", (-5.5, 82)), ("x=129.5", (129.5, 116))]:
    ax.annotate(lbl, xy, fontsize=7, ha="center")

az.set_xlim(108, 160); az.set_ylim(-118, 100)
az.set_title("Right edge detail (mm)")
def dim(a, p0, p1, t, off=(0, 0), **kw):
    a.annotate("", p0, p1, arrowprops=dict(arrowstyle="<->", lw=.9))
    a.text((p0[0] + p1[0]) / 2 + off[0], (p0[1] + p1[1]) / 2 + off[1], t, fontsize=8, ha="center", backgroundcolor="w", **kw)
dim(az, (129.5, 60), (153, 60), "23.5", (0, 2))
dim(az, (140, 50), (153, 50), "13.0", (0, 2))
dim(az, (116, 95), (153, 95), "37.0", (0, 1))
dim(az, (112, -111), (112, -100.5), "10.5", (-3, 0), rotation=90)
dim(az, (112, -100.5), (112, -6.75), "93.75", (-3, 0), rotation=90)
dim(az, (112, -6.75), (112, 74), "80.75", (-3, 0), rotation=90)
dim(az, (157, -100), (157, 80), "180.0 (magazine M6)", (3, 0), rotation=90)
dim(az, (149, -111), (149, -100), "11", (2.5, 0), rotation=90)
dim(az, (146, 36.5), (146, 56.5), "20 pitch", (2.5, 0), rotation=90)
az.annotate("dowel (142,-15)\nØ4.1 thru", (142, -15), (116.5, -30), fontsize=7, arrowprops=dict(arrowstyle="->", lw=.6))
az.annotate("toolsetter\nclear R7.2", P.TOOLSETTER, (113, 90), fontsize=7, arrowprops=dict(arrowstyle="->", lw=.6))
az.annotate("T1 centre\n(140.5, 56.5)", P.PODS[0], (113, 40), fontsize=7, arrowprops=dict(arrowstyle="->", lw=.6))

fig.text(0.01, 0.01,
         "VERIFY ON YOUR MACHINE BEFORE MAKING THE ADAPTER: right-column bed screw centres are 23.5 mm from the right edge and 10.5 / 104.25 / 185.0 mm "
         "from the front edge.\nAdapter clamps through those 3 screws (replace with M6 screws +12 mm longer), locates on the 4 mm dowel at (142,-15); "
         "magazine bolts into 2 captive M6 nuts at (140, 80) and (140, -100).\nSource of bed geometry: Saunders Machine Works Carvera Air plate drawing S1988 rev 2 "
         "(reuses stock screw/dowel positions). Magazine position: Warioo SMW install.", fontsize=8.5, va="bottom")
out = pathlib.Path(__file__).resolve().parents[1] / "cad/custom/renders/stock_bed_layout.png"
fig.tight_layout(rect=(0, 0.07, 1, 1)); fig.savefig(out, dpi=120); print(out)
