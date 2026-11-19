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
# Measured from SMW_atcMagazine_v3.step (see docs/research/upstream_part_dimensions.md)
MAG_W = 27.0            # magazine footprint X (mm)
MAG_L = 199.3           # magazine footprint Y (mm)
MAG_HOLE_PITCH = 180.0  # the two M6 mounting holes, along Y
# Hole centres relative to magazine footprint centre (Y): +93.5 and -86.5 around model
# centre 2.15 -> +91.35 / -88.65. X: 14.0 from the left edge (centre is 13.5) -> +0.5.
MAG_HOLES = [(0.5, 91.35), (0.5, -88.65)]


# ---------------------------------------------------------------- 1. stock-bed adapter
def bed_adapter(thickness=12.0, width=80.0, length=230.0, slot_len=22.0, slot_w=6.6,
                slot_x=(-23.0, 23.0), slot_y=(-75.0, 0.0, 75.0), insert_d=8.0):
    """Riser plate that lets the SMW magazine sit on the STOCK Carvera Air bed.

    * Magazine side: 2x M6 holes at 180 mm pitch, sized for M6 heat-set/press inserts
      (insert_d) - or tap M6 directly if you mill it from aluminium.
    * Bed side: 6 slots (X direction) so it fits any bed hole grid; bolt with M6 or M5
      cap screws into the bed's threaded inserts. Counterbored so heads sit flush.
    Machine it ON THE CARVERA from 12 mm HDPE (cutting board), MDF or 6061 plate,
    or 3D print it (PETG, 6 walls, 40 % infill).
    """
    p = cq.Workplane("XY").box(width, length, thickness).edges("|Z").fillet(4)
    p = p.faces(">Z").workplane().pushPoints(MAG_HOLES).hole(insert_d)
    pts = [(x, y) for x in slot_x for y in slot_y]
    # bed slots: through slot + counterbore slot (head of M6 SHCS = 10 mm, 6 mm deep)
    for x, y in pts:
        p = p.cut(cq.Workplane("XY").center(x, y).slot2D(slot_len, slot_w, 0)
                  .extrude(thickness * 2, both=True))
        p = p.cut(cq.Workplane("XY").workplane(offset=thickness / 2 - 6.5).center(x, y)
                  .slot2D(slot_len + 4.5, 11.0, 0).extrude(10))
    # edge marks to align magazine footprint
    mark = cq.Workplane("XY").workplane(offset=thickness / 2 - 0.6).center(0.5, 1.35) \
        .rect(MAG_W, MAG_L).rect(MAG_W - 1.2, MAG_L - 1.2).extrude(1)
    return p.cut(mark)


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
