#!/usr/bin/env python3
"""Original parametric parts for the Carvera Air ATC prototype (Phase 1).

These are OUR designs (not derived from Warioo's CC BY-NC-ND files); they only
match published interface dimensions (hole spacing, bore sizes) measured from them.

Run:  .venv/bin/python cad/custom/src/parts.py
Out:  cad/custom/stl/*.stl, cad/custom/step/*.step, cad/custom/renders/*.png
"""
import pathlib
import cadquery as cq

ROOT = pathlib.Path(__file__).resolve().parents[1]
STL, STEP = ROOT / "stl", ROOT / "step"
for d in (STL, STEP):
    d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- interface data
# BED FRAME: origin = centre of the Carvera Air bed (306 x 222 mm), +X = right, +Y = back,
# Z = 0 = top surface of the stock MDF bed. Interface positions measured from the public
# Saunders Machine Works (SMW) Carvera Air plate drawing/STEP (which reuses the stock bed's
# screws, dowel standoffs and outline) and from the upstream magazine STEP.
BED_X, BED_Y = 306.0, 222.0
BED_SCREWS = [(x, y) for x in (-142.5, -5.5, 129.5) for y in (-100.5, -6.75, 74.0)]  # 9x M6 SHCS
BED_SCREWS_RIGHT = [(129.5, -100.5), (129.5, -6.75), (129.5, 74.0)]
DOWELS = [(-145.5, -15), (-108, -58.5), (-57, -103.5), (-57, 30), (31.5, -58.5), (142, -15)]  # 4 mm pins
TOOLSETTER = (135.44, 93.44)    # centre of the bed's back-right toolsetter notch
NOTCH_Y = 88.3                  # bed edge just in front of the toolsetter (x > ~128.5)
# Upstream magazine as installed on the SMW plate (its holes land on the 20 mm M6 grid):
MAG_HOLES = [(140.0, 80.0), (140.0, -100.0)]     # 180 mm pitch
MAG_X = (126.0, 153.0)                           # footprint flush with right bed edge
MAG_Y = (-111.0, NOTCH_Y)                        # flush with front edge, foot ends at notch
POD_X = 140.5
PODS = [(POD_X, 56.5 - 20 * i) for i in range(8)]  # T1 (back) .. T8 (front), per upstream slot file


# ---------------------------------------------------------------- 1. stock-bed adapter
def bed_adapter(thickness=12.0, x0=116.0, nut_af=10.2, nut_depth=8.0, tapped=False):
    """Riser that puts the SMW-style magazine on the STOCK MDF bed, with NO new holes in the bed.

    * Clamps down through the bed's own right-hand column of 3x M6 hold-down screws
      (x=129.5; y=-100.5, -6.75, 74): swap them for screws `thickness` mm longer.
    * Locates on the stock 4 mm dowel position (142, -15).
    * Magazine bolts to 2x M6 at (140, 80) / (140, -100): captive M6 hex nuts in pockets
      from below (HDPE/MDF/PETG), or `tapped=True` -> 5.0 mm tap drill for M6 in 6061.
      Screws (12 mm adapter): back foot (4.5 mm flange) M6x16, front (11 mm flange) M6x20.
      Nut sits 3-8 mm above the bed, so neither screw tip touches the MDF.
    Model is in BED coordinates (origin = bed centre); CAM/slicer can re-zero it.
    """
    w, y0, y1 = BED_X / 2 - x0, -BED_Y / 2, NOTCH_Y
    p = (cq.Workplane("XY").center((x0 + BED_X / 2) / 2, (y0 + y1) / 2)
         .rect(w, y1 - y0).extrude(thickness).edges("|Z").fillet(2.0))
    # clearance for the toolsetter (r 7.2 around its axis)
    p = p.cut(cq.Workplane("XY").center(*TOOLSETTER).circle(7.2).extrude(thickness * 3, both=True))
    top = cq.Workplane("XY").workplane(offset=thickness)
    # bed hold-down screws: 6.6 thru + 11 counterbore, heads sit 0.5 below the top
    p = p.cut(cq.Workplane("XY").pushPoints(BED_SCREWS_RIGHT).circle(3.3).extrude(thickness))
    p = p.cut(top.workplane(offset=-6.5).pushPoints(BED_SCREWS_RIGHT).circle(5.5).extrude(7))
    # magazine screws
    if tapped:
        p = p.cut(cq.Workplane("XY").pushPoints(MAG_HOLES).circle(2.5).extrude(thickness))
    else:
        p = p.cut(cq.Workplane("XY").pushPoints(MAG_HOLES).circle(3.3).extrude(thickness))
        p = p.cut(cq.Workplane("XY").pushPoints(MAG_HOLES).polygon(6, nut_af / 0.866).extrude(nut_depth))
    # dowel
    p = p.cut(cq.Workplane("XY").center(*DOWELS[-1]).circle(2.05).extrude(thickness))
    # engraved pod index marks (0.6 deep) so slot teaching starts close
    for i, (x, y) in enumerate(PODS):
        p = p.cut(top.workplane(offset=-0.6).center(x0 + 2.5, y).rect(3, 0.8).extrude(1))
    return p


# ---------------------------------------------------------------- 2. bore test coupons
def bore_coupons():
    """Print these FIRST. Pick the bore that press-fits, then use OrcaSlicer 'X-Y hole compensation' (never scale gears).

    Row A: lever-cylinder bore for BottomGear (nominal 14.06) : 13.9 .. 14.3
    Row B: motor shaft bore + 3 mm key for TopGear (nominal 8.1): 7.9 .. 8.3
    """
    base = cq.Workplane("XY").box(110, 46, 6).edges("|Z").fillet(3)
    a = [13.9, 14.0, 14.1, 14.2, 14.3]
    b = [7.9, 8.0, 8.1, 8.2, 8.3]
    for i, d in enumerate(a):
        base = base.cut(cq.Workplane("XY").center(-44 + i * 22, 10).circle(d / 2).extrude(10, both=True))
    for i, d in enumerate(b):
        x = -44 + i * 22
        hole = cq.Workplane("XY").center(x, -12).circle(d / 2).extrude(10, both=True)
        key = cq.Workplane("XY").center(x + d / 2, -12).rect(3.2, 3.1).extrude(10, both=True)
        base = base.cut(hole).cut(key)
        # engrave a tick count (1..5) so you can tell them apart after printing
        for t in range(i + 1):
            base = base.cut(cq.Workplane("XY").workplane(offset=2.4)
                            .center(x - 6 + t * 3, -21).rect(1.2, 2.5).extrude(1))
            base = base.cut(cq.Workplane("XY").workplane(offset=2.4)
                            .center(x - 6 + t * 3, 20.5).rect(1.2, 2.5).extrude(1))
    return base


# ---------------------------------------------------------------- 3. chip caps
def chip_cap(bore=11.0, depth=6.0, grip=0.15):
    """Push-in cap for the magazine's M6 counterbores so chips don't pack them."""
    body = cq.Workplane("XY").circle(bore / 2 + grip).extrude(depth)
    lip = cq.Workplane("XY").workplane(offset=depth).circle(bore / 2 + 1.2).extrude(1.0)
    pull = cq.Workplane("XY").workplane(offset=depth).rect(1.6, bore - 2).extrude(2.5)
    return body.union(lip).union(pull).faces("<Z").shell(-1.0)


# ---------------------------------------------------------------- 4. signal board box
def signal_box(pcb=(30.0, 20.0), wall=1.6, h=12.0):
    """Enclosure for the 24 V -> controller-safe tool-sensor interface (PC817 board).

    Fits a 30x20 mm perfboard offcut. Cable exits both ends; 2 zip-tie slots on the base.
    """
    ox, oy = pcb[0] + 2 * wall + 1, pcb[1] + 2 * wall + 1
    box = cq.Workplane("XY").box(ox, oy, h, centered=(True, True, False)).edges("|Z").fillet(2)
    box = box.faces(">Z").shell(-wall)
    for s in (-1, 1):
        box = box.cut(cq.Workplane("YZ").workplane(offset=s * ox / 2).center(0, h - 3)
                      .rect(7, 6).extrude(4, both=True))
        box = box.cut(cq.Workplane("XY").center(s * 8, 0).rect(3.5, oy + 2).extrude(0.9))
    lid = cq.Workplane("XY").box(ox, oy, 1.6, centered=(True, True, False)).edges("|Z").fillet(2) \
        .union(cq.Workplane("XY").workplane(offset=-2).rect(ox - 2 * wall - 0.4, oy - 2 * wall - 0.4)
               .rect(ox - 4 * wall - 0.4, oy - 4 * wall - 0.4).extrude(2))
    return box, lid.translate((ox + 6, 0, 0))


PARTS = {
    "atc_bed_adapter": bed_adapter,
    "bore_test_coupons": bore_coupons,
    "magazine_chip_cap": chip_cap,
}

if __name__ == "__main__":
    out = {k: f() for k, f in PARTS.items()}
    box, lid = signal_box()
    out["signal_board_box"] = box
    out["signal_board_lid"] = lid
    for name, shape in out.items():
        cq.exporters.export(shape, str(STL / f"{name}.stl"), tolerance=0.02, angularTolerance=0.1)
        cq.exporters.export(shape, str(STEP / f"{name}.step"))
        bb = shape.val().BoundingBox()
        print(f"{name:22s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f} mm")
