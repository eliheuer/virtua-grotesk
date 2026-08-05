#!/usr/bin/env python3
"""Lane-3 skeleton constructions for the Arabic completion pass.

Each builder emits explicit point lists in the green-donor idiom
(bar 104, stem 96, chamfer 16) with Rubik supplying topology and
proportions only. Output goes to both masters, marked blue.

EVEN-TERMINAL RULE (Eli, 2026-08-04): a free-standing terminal on an
isolated boat or cup rises to 288 with a 16-chamfer and a 64 flat, and
BOTH ends of a symmetric form use it. 432 is the height of a joining
TOOTH (beh.init/medi, seen's teeth) and must not be borrowed for a
terminal — that made the isolated beh lopsided. Simple, even and
geometric beats expressive in this design.

Usage:
    ./.venv/bin/python scripts/arabic_skeletons.py behDotless-ar behDotless-ar.fina
    ./.venv/bin/python scripts/arabic_skeletons.py --all
"""

import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from arabic_build import write_glyph, read_points, MASTERS  # noqa: E402


def signed_area(contour):
    """Approximate signed area over the on+off polygon — sign only."""
    pts = [(x, y) for x, y, *_ in contour]
    a = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        a += x0 * y1 - x1 * y0
    return a


DONOR_SIGN = None


def match_winding(contour):
    """Flip contour if its winding differs from the green tooth donor."""
    global DONOR_SIGN
    if DONOR_SIGN is None:
        DONOR_SIGN = signed_area(read_points("behDotless-ar.init")[0]) > 0
    if (signed_area(contour) > 0) != DONOR_SIGN:
        from arabic_build import reverse_contour
        return reverse_contour(contour)
    return contour


# ---------------------------------------------------------------------------

def build_behDotless_isol():
    """Beh boat, isolated: two EVEN rising terminals over a flat bottom.

    EVEN-TERMINAL RULE (Eli, 2026-08-04): an isolated boat/cup is mirror
    symmetric — both terminals rise to the same height (288) with the same
    16-chamfer and 64 flat. The first version borrowed the init/medi tooth
    height (432) for the right end, which made the form lopsided. This is a
    neo-grotesk: simple, even, geometric beats expressive.
    """
    c = [
        (64, 176, "line", False),        # left outer edge (chamfer above)
        (64, 72, None, False),
        (136, 0, None, False),
        (240, 0, "curve", True),         # onto bottom edge
        (704, 0, "line", False),
        (808, 0, None, False),
        (880, 72, None, False),
        (880, 176, "curve", True),       # right terminal outer edge
        (880, 272, "line", False),
        (864, 288, "line", False),       # chamfer
        (800, 288, "line", False),       # right terminal flat
        (784, 272, "line", False),       # chamfer
        (784, 200, "line", True),        # right terminal inner edge down
        (784, 136, None, False),
        (752, 104, None, False),
        (688, 104, "curve", True),       # onto inner bowl bottom
        (256, 104, "line", True),
        (192, 104, None, False),
        (160, 136, None, False),
        (160, 200, "curve", True),       # inner left rise
        (160, 272, "line", False),
        (144, 288, "line", False),       # chamfer
        (80, 288, "line", False),        # left terminal flat
        (64, 272, "line", False),        # chamfer, closes to (64,176)
    ]
    anchors = [("top", 832, 272), ("topDots", 832, 288),
               ("bottom", 472, 16), ("bottomDots", 472, 0)]
    write_glyph("behDotless-ar", 944, contours=[match_winding(c)],
                anchors=anchors)


def build_behDotless_fina():
    """Beh boat, final: the isolated boat with its RIGHT terminal replaced
    by the joining bar out to the advance edge.

    The first version put a medial-style tooth (432) in the middle of the
    final form, copied from behDotless-ar.medi. A final beh has no tooth —
    it is a shallow bowl that connects on the right and rises on the left
    only. Same EVEN/SIMPLE rule as the isolated form.
    """
    adv = 1024
    c = [
        (64, 176, "line", False),        # left terminal outer edge
        (64, 72, None, False),
        (136, 0, None, False),
        (240, 0, "curve", True),         # onto the flat bottom
        (adv, 0, "line", False),         # bottom runs to the advance edge
        (adv, 104, "line", False),       # entry edge
        (256, 104, "line", True),        # bar top / inner bowl, leftward
        (192, 104, None, False),
        (160, 136, None, False),
        (160, 200, "curve", True),       # inner left rise
        (160, 272, "line", False),
        (144, 288, "line", False),       # chamfer
        (80, 288, "line", False),        # left terminal flat
        (64, 272, "line", False),        # chamfer, closes to (64,176)
    ]
    anchors = [("top", 544, 272), ("topDots", 544, 288),
               ("bottom", 544, 16), ("bottomDots", 544, 0)]
    write_glyph("behDotless-ar.fina", adv, contours=[match_winding(c)],
                anchors=anchors)


def build_noonghunna_isol():
    """Noon cup, isolated: deep round cup dipping below the baseline, with
    two EVEN terminals at 288 (same rule as the beh boat — an isolated cup
    is mirror symmetric). Rubik noonghunna-ar for the depth ratio (its cup
    dips ~-133 on a 750 cap -> -160 here)."""
    c = [
        (64, 168, "line", False),        # left outer wall
        (64, -8, None, False),
        (176, -160, None, False),
        (340, -160, "curve", True),      # cup outer bottom
        (504, -160, None, False),
        (616, -8, None, False),
        (616, 168, "curve", True),       # right outer wall rise
        (616, 272, "line", False),
        (600, 288, "line", False),       # chamfer
        (536, 288, "line", False),       # right terminal flat
        (520, 272, "line", False),       # chamfer
        (520, 152, "line", True),        # right inner wall down
        (520, 8, None, False),
        (444, -56, None, False),
        (340, -56, "curve", True),       # cup inner bottom
        (236, -56, None, False),
        (160, 8, None, False),
        (160, 152, "curve", True),       # left inner wall rise
        (160, 272, "line", False),
        (144, 288, "line", False),       # chamfer
        (80, 288, "line", False),        # left tip flat
        (64, 272, "line", False),        # chamfer
    ]
    anchors = [("top", 340, 272), ("topDots", 340, 288),
               ("bottom", 340, -176), ("bottomDots", 340, -176)]
    write_glyph("noonghunna-ar", 680, contours=[match_winding(c)],
                anchors=anchors)


def build_noonghunna_fina():
    """Noon cup, final: cup + entry bar at the right edge. Bar joins the
    cup wall with plain corners (the hah.init stub idiom)."""
    c = [
        (64, 168, "line", False),
        (64, -8, None, False),
        (176, -160, None, False),
        (400, -160, "curve", True),
        (536, -160, None, False),
        (736, -104, None, False),
        (736, -48, "curve", True),       # outer right wall, vertical tangent
        (736, 0, "line", False),
        (800, 0, "line", False),         # bar bottom to advance edge
        (800, 104, "line", False),       # entry edge
        (640, 104, "line", False),       # bar top leftward, corner into wall
        (640, 0, "line", True),          # inner right wall down
        (640, -26, None, False),
        (562, -56, None, False),
        (400, -56, "curve", True),       # cup inner bottom
        (236, -56, None, False),
        (160, 8, None, False),
        (160, 152, "curve", True),       # left inner wall rise
        (160, 272, "line", False),
        (144, 288, "line", False),       # chamfer
        (80, 288, "line", False),        # left tip flat
        (64, 272, "line", False),        # chamfer
    ]
    anchors = [("top", 400, 120), ("topDots", 400, 120),
               ("bottom", 400, -176), ("bottomDots", 400, -176)]
    write_glyph("noonghunna-ar.fina", 800, contours=[match_winding(c)],
                anchors=anchors)


# ---------------------------------------------------------------------------
# donor splicing

def find_pt(contour, x, y):
    for i, (px, py, *_rest) in enumerate(contour):
        if px == x and py == y:
            return i
    raise ValueError(f"point ({x},{y}) not in donor")


def cup_replacing_stub(wall_x, tip_x=64, depth=-160, tip_top=288):
    """The noon-cup run that replaces a left joining stub, traversed in the
    donor direction (arriving at the stub's (0,0) corner from the bottom
    edge, leaving toward its (0,104) corner along the top).

    wall_x: x of the stub corner column in final coordinates (donor 0 + dx).
    Returns the point run from (wall_x,0) exclusive-start replacement:
    starts with the line down the outer wall, ends at (wall_x-96, 104)
    corner, ready to line-join to the donor's (0,104) point."""
    inner_x = wall_x - 96
    cx = (tip_x + wall_x) // 2          # cup center
    run = [
        (wall_x, 0, "curve", False),     # stub corner (keeps donor's type:
                                         # it ends the bottom-edge curve)
        (wall_x, -48, "line", True),
        (wall_x, -104, None, False),
        (cx + 136, depth, None, False),
        (cx, depth, "curve", True),      # cup outer bottom (R->L)
        (cx - 224, depth, None, False),
        (tip_x, depth + 152, None, False),
        (tip_x, tip_top - 120, "curve", True),  # left outer wall
        (tip_x, tip_top - 16, "line", False),
        (tip_x + 16, tip_top, "line", False),   # chamfer
        (tip_x + 80, tip_top, "line", False),   # tip flat
        (tip_x + 96, tip_top - 16, "line", False),
        (tip_x + 96, tip_top - 136, "line", True),
        (tip_x + 96, depth + 168, None, False),
        (tip_x + 174, depth + 104, None, False),
        (cx, depth + 104, "curve", True),       # cup inner bottom (L->R)
        (cx + 162, depth + 104, None, False),
        (inner_x, depth + 134, None, False),
        (inner_x, 0, "curve", True),            # inner wall rise
        (inner_x, 104, "line", False),          # corner to bar-top level
    ]
    return run


def cup_run(wall_x, tip_x=64, depth=-160, tip_top=288, land_type="curve"):
    """Generalized noon-style cup replacing a left stub (land at (wall_x,0)
    from the bottom edge, exit at (wall_x-96,104)). Controls scale with the
    cup span so narrow (qaf) and wide (seen) cups keep the same look."""
    inner_x = wall_x - 96
    cx = (tip_x + wall_x) // 2
    span = cx - tip_x
    run = [
        (wall_x, 0, land_type, False),
        (wall_x, -48, "line", True),
        (wall_x, -104, None, False),
        (cx + round(0.45 * span), depth, None, False),
        (cx, depth, "curve", True),
        (cx - round(0.74 * span), depth, None, False),
        (tip_x, depth + 152, None, False),
        (tip_x, tip_top - 120, "curve", True),
        (tip_x, tip_top - 16, "line", False),
        (tip_x + 16, tip_top, "line", False),
        (tip_x + 80, tip_top, "line", False),
        (tip_x + 96, tip_top - 16, "line", False),
        (tip_x + 96, tip_top - 136, "line", True),
        (tip_x + 96, depth + 168, None, False),
        (tip_x + 96 + round(0.64 * span), depth + 104, None, False),
        (cx, depth + 104, "curve", True),
        (cx + round(0.53 * span), depth + 104, None, False),
        (inner_x, depth + 134, None, False),
        (inner_x, 0, "curve", True),
        (inner_x, 104, "line", False),
    ]
    return run


def boat_run(wall_x, tip_x=64, tip_top=288):
    """Shallow beh-boat tail replacing a left joining stub: land at
    (wall_x, 0) coming along the bottom edge, exit at (wall_x, 104) on the
    bar top. Mirrors the geometry of the hand-built behDotless-ar isol."""
    return [
        (wall_x, 0, "curve", True),
        (wall_x - 104, 0, None, False),
        (tip_x, 72, None, False),
        (tip_x, 176, "curve", True),
        (tip_x, tip_top - 16, "line", False),
        (tip_x + 16, tip_top, "line", False),
        (tip_x + 80, tip_top, "line", False),
        (tip_x + 96, tip_top - 16, "line", False),
        (tip_x + 96, 200, "line", True),
        (tip_x + 96, 136, None, False),
        (wall_x - 64, 104, None, False),
        (wall_x, 104, "curve", True),
    ]


def _feh_with_boat(donor_name, out_name, advance, dxt=384):
    contours = read_points(donor_name)
    outer_i = next(i for i, c in enumerate(contours)
                   if any(p[0] == -16 for p in c))
    d = [(x + dxt, y, t, s) for x, y, t, s in contours[outer_i]]
    i0 = find_pt(d, dxt, 0)
    i104 = find_pt(d, dxt, 104)
    boat = boat_run(wall_x=dxt)
    x, y, _t, s = boat[0]
    boat[0] = (x, y, d[i0][2], s)
    c = d[:i0] + boat + d[i104 + 1:]
    out = [c] + [[(x + dxt, y, t, s) for x, y, t, s in contours[i]]
                 for i in range(len(contours)) if i != outer_i]
    write_glyph(out_name, advance, contours=out,
                anchors=[("top", 224 + dxt, 608), ("bottom", 224 + dxt, -16)])


def build_fehDotless_isol():
    _feh_with_boat("fehDotless-ar.init", "fehDotless-ar", 864)


def build_fehDotless_fina():
    _feh_with_boat("fehDotless-ar.medi", "fehDotless-ar.fina", 976)


def build_lam_alef_isol():
    """Isolated lam-alef: the final ligature with the lam's entry removed
    (lam.init in place of lam.medi, shifted by the width difference)."""
    write_glyph("lam_alef-ar", 544,
                components=[("lam-ar.init", 256, 0),
                            ("alef-ar.fina", 0, 0)])


def build_seen_medi():
    """seen.medi = green seen.init with the right scoop replaced by a bar
    exit to the advance edge (both-side joining)."""
    donor = read_points("seen-ar.init")[0]
    i_lip = find_pt(donor, 768, 184)     # third tooth right edge, line smooth
    i_scoop = find_pt(donor, 576, -16)   # bottom scoop oncurve to keep
    head = donor[:i_lip + 1]             # ... up to (768,184)
    tail = donor[i_scoop:]               # (576,-16) ... to close
    exit_run = [
        (768, 132, None, False),
        (812, 104, None, False),
        (876, 104, "curve", True),
        (992, 104, "line", False),
        (992, 0, "line", False),
        (928, 0, "line", True),
        (856, 0, None, False),
        (704, -16, None, False),
    ]
    c = head + exit_run + tail
    anchors = [("top", 432, 400), ("topDots", 432, 432), ("bottom", 432, 0)]
    write_glyph("seen-ar.medi", 992, contours=[c], anchors=anchors)


def seen_tail_run(J, land_type="curve", left=64, term=432, d_out=-272):
    """The seen/sad tail, as ONE continuous stroke out of the teeth.

    The donor arrives at (J, 0) with a horizontal tangent and leaves
    (J, 104) with a horizontal tangent, so the tail must join tangentially
    at BOTH edges. The first version turned 90 degrees straight off the
    junction, which left a square step where the tail met the teeth — the
    letter read as two pieces butted together (Eli, 2026-08-04).

    Terminal rises to `term` (tooth height), so all four verticals of seen
    line up: even and geometric, per the same rule as the beh boat.
    """
    k = 0.55
    inner_left = left + 96               # 96 = vertical stem
    bend = 120                           # radius of the bar's turn-down
    Rx = J - bend                        # outer right wall of the bowl
    d_in = d_out + 104                   # 104 = horizontal stroke
    ix = Rx - 104                        # inner right wall
    # Both side walls turn into the bowl at the same height as the bar's
    # bend, and the inner curve turns at the SAME y as the outer — that is
    # what makes the stroke a true constant-width offset round the U.
    # Letting these drift apart put a visible dent in the outer edge.
    wall_y = iwall_y = -bend
    Bx = round((left + Rx) / 4) * 2      # outer bowl centre, on the 2-grid
    Ix = round((inner_left + ix) / 4) * 2

    def px(v):
        return round(v / 2) * 2

    return [
        # --- outer: the bar turns down, then a round U, then the left wall
        (J, 0, land_type, True),                    # tangential landing
        (px(J - k * bend), 0, None, False),
        (Rx, px(-k * bend), None, False),
        (Rx, -bend, "curve", True),                 # onto the right wall
        (Rx, px(d_out + k * (wall_y - d_out)), None, False),
        (px(Bx + k * (Rx - Bx)), d_out, None, False),
        (Bx, d_out, "curve", True),                 # bowl outer bottom
        (px(Bx - k * (Bx - left)), d_out, None, False),
        (left, px(d_out + k * (wall_y - d_out)), None, False),
        (left, wall_y, "curve", True),              # onto the left wall
        (left, term - 16, "line", False),
        (left + 16, term, "line", False),           # chamfer
        (left + 80, term, "line", False),           # terminal flat
        (inner_left, term - 16, "line", False),     # chamfer
        # --- inner: back down the left wall, round the bowl, into the tooth
        (inner_left, iwall_y, "line", True),
        (inner_left, px(d_in + k * (iwall_y - d_in)), None, False),
        (px(Ix - k * (Ix - inner_left)), d_in, None, False),
        (Ix, d_in, "curve", True),                  # bowl inner bottom
        (px(Ix + k * (ix - Ix)), d_in, None, False),
        (ix, px(d_in + k * (iwall_y - d_in)), None, False),
        (ix, iwall_y, "curve", True),               # onto the inner right wall
        (ix, px(104 - k * (104 - iwall_y)), None, False),
        (px(J - k * (J - ix)), 104, None, False),
        (J, 104, "curve", True),                    # tangential exit onto bar
    ]


def _seen_with_cup(donor_contour, name, advance, anchors, dx=640,
                   extra_contours=()):
    """Replace the left stub of a seen-family donor with the flowing tail.
    dx is the tail width (the donor shifts right by it)."""
    d = [(x + dx, y, t, s) for x, y, t, s in donor_contour]
    i00 = find_pt(d, 0 + dx, 0)          # stub corner (0,0)
    i104 = find_pt(d, 0 + dx, 104)       # stub corner (0,104)
    # donor order: ...bottom edge -> (0,0) -> stub pts -> (0,104) -> top...
    tail = seen_tail_run(dx, land_type=d[i00][2] or "line")
    c = d[:i00] + tail + d[i104 + 1:]
    extras = [[(x + dx, y, t, s) for x, y, t, s in e]
              for e in extra_contours]
    write_glyph(name, advance, contours=[c] + extras, anchors=anchors)


def build_seen_isol():
    donor = read_points("seen-ar.init")[0]
    anchors = [("top", 892, 400), ("topDots", 892, 432), ("bottom", 892, 0)]
    _seen_with_cup(donor, "seen-ar", 864 + 640, anchors)


def build_seen_fina():
    donor = read_points("seen-ar.medi")[0]  # the freshly built medi
    anchors = [("top", 892, 400), ("topDots", 892, 432), ("bottom", 892, 0)]
    _seen_with_cup(donor, "seen-ar.fina", 992 + 640, anchors)


def build_sad_isol():
    donor = read_points("sad-ar.init")
    anchors = [("top", 1204, 464), ("topDots", 1204, 464),
               ("bottom", 1204, 0)]
    _seen_with_cup(donor[0], "sad-ar", 1200 + 640, anchors,
                   extra_contours=donor[1:])


def build_sad_fina():
    donor = read_points("sad-ar.medi")
    anchors = [("top", 1204, 464), ("topDots", 1204, 464),
               ("bottom", 1204, 0)]
    _seen_with_cup(donor[0], "sad-ar.fina", 1264 + 640, anchors,
                   extra_contours=donor[1:])


def build_hah_medi():
    """hah.medi = green hah.init + entry bar from the right edge, joined
    with the heh.medi 8-step idiom; bottom edge becomes flat y0."""
    donor = read_points("hah-ar.init")[0]
    i_vertex = find_pt(donor, 672, 304)   # right vertex, curve smooth
    i_stub_end = find_pt(donor, 64, 104)  # after-stub point on top edge
    # donor order: (64,0) (0,0) stub (0,104) (64,104) ... (672,304) offs
    # (592,104) (480,104) (416,104) offs closing -> (64,0)
    head = donor[:i_vertex + 1]           # through (672,304)
    entry = [
        (672, 200, None, False),
        (600, 124, None, False),
        (560, 112, "curve", False),       # curve ends 8 above the bar
        (560, 104, "line", False),        # 8-step
        (800, 104, "line", False),
        (800, 0, "line", False),          # entry edge at advance
    ]
    # flat bottom back to (64,0); donor's first point becomes a line point
    x0, y0, _t, _s = donor[0]
    c = [(x0, y0, "line", True)] + head[1:] + entry
    anchors = [("top", 324, 574), ("topDots", 326, 530), ("bottom", 400, 32),
               ("bottomDots", 400, 0)]
    write_glyph("hah-ar.medi", 800, contours=[c], anchors=anchors)


def hah_bowl_run(dx):
    """The deep hah/jeem descender bowl replacing a left stub, for a donor
    translated +dx. Runs from the bar-bottom landing (donor (64,0)+dx) around
    the bowl and back to the bar-top point (donor (64,104)+dx)."""
    return [
        (64 + dx, 0, "curve", True),      # keeps donor closing-curve landing
        (32 + dx, 0, None, False),
        (8 + dx, -16, None, False),
        (8 + dx, -48, "curve", True),     # inner turn down
        (8 + dx, -96, "line", True),
        (8 + dx, -176, None, False),
        (96 + dx, -248, None, False),
        (256 + dx, -248, "curve", True),  # inner bottom
        (396 + dx, -248, None, False),
        (504 + dx, -190, None, False),
        (504 + dx, -120, "curve", True),  # inner right rise
        (504 + dx, -48, "line", False),
        (520 + dx, -32, "line", False),   # chamfer
        (592 + dx, -32, "line", False),   # tip flat
        (608 + dx, -48, "line", False),   # chamfer
        (608 + dx, -136, "line", True),   # outer right down
        (608 + dx, -252, None, False),
        (452 + dx, -352, None, False),
        (256 + dx, -352, "curve", True),  # outer bottom
        (60 + dx, -352, None, False),
        (-96 + dx, -232, None, False),
        (-96 + dx, -72, "curve", True),   # outer left rise
        (-96 + dx, 8, "line", True),
        (-96 + dx, 60, None, False),
        (-40 + dx, 104, None, False),
        (64 + dx, 104, "curve", True),    # lands on the bar-top point
    ]


def _bowl_replacing_stub(donor_name, out_name, advance, dxt, jx,
                         extra_contours=()):
    """Replace a donor's left joining stub with the deep descender bowl.
    Works for any donor whose walk arrives at the stub along the bar bottom
    (jx, 0) and leaves along the bar top (jx, 104). dxt translates the donor
    right to make room; the bowl run is positioned so its landing/exit match
    the junction column."""
    contours = read_points(donor_name)
    d = [(x + dxt, y, t, s) for x, y, t, s in contours[0]]
    i0 = find_pt(d, jx + dxt, 0)
    i5 = find_pt(d, jx + dxt, 104)
    bowl = hah_bowl_run(dx=jx + dxt - 64)
    x, y, _t, s = bowl[0]
    bowl[0] = (x, y, d[i0][2], s)         # inherit the landing type
    c = bowl + d[i5 + 1:] + d[:i0]
    out = [c]
    for extra in contours[1:]:
        out.append([(x + dxt, y, t, s) for x, y, t, s in extra])
    bx = jx + dxt - 64
    # bottomDots sits at the bowl's INNER top edge, so a below-dot lands
    # inside the bowl (green jeem/khah convention) rather than under it.
    anchors = [("top", 326 + dxt, 574), ("topDots", 326 + dxt, 530),
               ("bottom", 256 + bx, -368), ("bottomDots", 256 + bx, 68)]
    write_glyph(out_name, advance, contours=out, anchors=anchors)


def build_hah_isol():
    _bowl_replacing_stub("hah-ar.init", "hah-ar", 864, dxt=160, jx=64)


def build_hah_fina():
    _bowl_replacing_stub("hah-ar.medi", "hah-ar.fina", 960, dxt=160, jx=64)


def ain_bowl_run(dx):
    """Deep ain bowl replacing a left stub for the ain family (donor
    translated +dx). Donor arrives at (0,104)+dx going left along the bar
    top and leaves at (0,0)+dx going right along the bar bottom; here the
    replacement runs from after (96,104)+dx down around the bowl and lands
    with an 8-step onto the bar bottom."""
    return [
        (dx, 104, "line", False),         # bar top end
        (dx - 64, 104, None, False),
        (dx - 96, 64, None, False),
        (dx - 96, -8, "curve", True),     # outer left turn down
        (dx - 96, -88, "line", True),
        (dx - 96, -232, None, False),
        (dx + 80, -352, None, False),
        (dx + 272, -352, "curve", True),  # outer bottom
        (dx + 450, -352, None, False),
        (dx + 560, -244, None, False),
        (dx + 560, -136, "curve", True),  # outer right rise
        (dx + 560, -48, "line", False),
        (dx + 544, -32, "line", False),   # chamfer
        (dx + 480, -32, "line", False),   # tip flat
        (dx + 464, -48, "line", False),   # chamfer
        (dx + 464, -128, "line", True),   # inner right down
        (dx + 464, -200, None, False),
        (dx + 404, -248, None, False),
        (dx + 272, -248, "curve", True),  # inner bottom
        (dx + 136, -248, None, False),
        (dx + 16, -176, None, False),
        (dx + 16, -108, "curve", True),   # inner left rise
        (dx + 16, -8, "line", False),
        (dx + 24, 0, "line", False),      # 8-step onto bar bottom
    ]


def _ain_with_bowl(donor_name, out_name, advance, dx):
    donor = read_points(donor_name)[0]
    d = [(x + dx, y, t, s) for x, y, t, s in donor]
    i_top = find_pt(d, 96 + dx, 104)      # (96,104) after the 8-step
    i_bot = find_pt(d, 0 + dx, 0)         # (0,0) bar bottom start
    # donor order: (0,0) (bar bottom ->) ... head ... (96,104) (0,104) stub
    c = d[i_bot + 1:i_top + 1] + ain_bowl_run(dx=dx)
    anchors = [("top", 240 + dx, 440), ("topDots", 240 + dx, 440),
               ("bottom", 272 + dx, -368), ("bottomDots", 272 + dx, 68)]
    write_glyph(out_name, advance, contours=[c], anchors=anchors)


def build_ain_isol():
    _ain_with_bowl("ain-ar.init", "ain-ar", 784, dx=160)


def build_ain_fina():
    # ain.medi joins bottom-in/top-out like hah, so the generic splice fits;
    # its junction column is x=0 and it carries a counter contour.
    _bowl_replacing_stub("ain-ar.medi", "ain-ar.fina", 832, dxt=224, jx=0)


# ---------------------------------------------------------------------------
# sad / tah (loop skeletons, built on the seen prefix)

def _sad_prefix():
    """Stub + first tooth + valley of green seen.init, with the first point
    retyped to line (sad's bottom edge is straight)."""
    donor = read_points("seen-ar.init")[0]
    return [(donor[0][0], donor[0][1], "line", False)] + donor[1:15]


SAD_COUNTER = [
    (512, 248, "line", True), (512, 224, None, False),
    (528, 208, None, False), (552, 208, "curve", True),
    (936, 208, "line", True), (960, 208, None, False),
    (976, 224, None, False), (976, 248, "curve", True),
    (976, 304, "line", True), (976, 328, None, False),
    (960, 344, None, False), (936, 344, "curve", True),
    (552, 344, "line", True), (528, 344, None, False),
    (512, 328, None, False), (512, 304, "curve", True),
]


def _sad_loop(exit_kind):
    """The big sad loop after the valley. exit_kind: 'free' descends to the
    baseline (init/isol right end), 'entry' joins a bar to the right edge."""
    run = [
        (344, 88, None, False), (384, 128, None, False),
        (384, 184, "curve", True),
        (384, 344, "line", True),
        (384, 412, None, False), (452, 448, None, False),
        (576, 448, "curve", True),
        (920, 448, "line", True),
        (1024, 448, None, False), (1104, 360, None, False),
        (1104, 224, "curve", True),
    ]
    if exit_kind == "free":
        run += [
            (1104, 112, None, False), (1016, 24, None, False),
            (880, 0, "curve", True),
        ]
    else:
        run += [
            (1104, 150, None, False), (1052, 120, None, False),
            (1008, 112, "curve", False),
            (1008, 104, "line", False),
            (1264, 104, "line", False),
            (1264, 0, "line", False),
        ]
    return run


def build_sad_init():
    c = _sad_prefix() + _sad_loop("free")
    anchors = [("top", 744, 464), ("topDots", 744, 464), ("bottom", 744, 0)]
    write_glyph("sad-ar.init", 1200, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


def build_sad_medi():
    c = _sad_prefix() + _sad_loop("entry")
    anchors = [("top", 744, 464), ("topDots", 744, 464), ("bottom", 744, 0)]
    write_glyph("sad-ar.medi", 1264, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


def _tahify(points):
    """Raise the sad tooth to the alef stem height (tah family)."""
    lift = {(96, 416): (96, 752), (112, 432): (112, 768),
            (176, 432): (176, 768), (192, 416): (192, 752)}
    return [lift.get((x, y), (x, y)) + (t, s) for x, y, t, s in points]


def _cap_left_stub(points):
    """Close a left joining stub into a chamfered terminal (isolated/final
    forms of tah)."""
    swap = {(0, 0): (16, 0), (-16, 16): (0, 16),
            (-16, 88): (0, 88), (0, 104): (16, 104)}
    return [swap.get((x, y), (x, y)) + (t, s) for x, y, t, s in points]


def build_tah_init():
    c = [(x, y, t, s) for x, y, t, s in _tahify(_sad_prefix())] \
        + _sad_loop("free")
    anchors = [("top", 744, 464), ("bottom", 744, 0)]
    write_glyph("tah-ar.init", 1200, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


def build_tah_medi():
    c = _tahify(_sad_prefix()) + _sad_loop("entry")
    anchors = [("top", 744, 464), ("bottom", 744, 0)]
    write_glyph("tah-ar.medi", 1264, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


def build_tah_isol():
    c = _cap_left_stub(_tahify(_sad_prefix())) + _sad_loop("free")
    anchors = [("top", 744, 464), ("bottom", 744, 0)]
    write_glyph("tah-ar", 1200, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


def build_tah_fina():
    c = _cap_left_stub(_tahify(_sad_prefix())) + _sad_loop("entry")
    anchors = [("top", 744, 464), ("bottom", 744, 0)]
    write_glyph("tah-ar.fina", 1264, contours=[c, list(SAD_COUNTER)],
                anchors=anchors)


# ---------------------------------------------------------------------------
# qafDotless (feh head + round cup)

def _qaf_with_cup(donor_name, out_name, advance, dxt):
    contours = read_points(donor_name)
    # outer contour is the one containing the stub (has x == -16)
    outer_i = next(i for i, c in enumerate(contours)
                   if any(p[0] == -16 for p in c))
    d = [(x + dxt, y, t, s) for x, y, t, s in contours[outer_i]]
    i0 = find_pt(d, dxt, 0)
    i104 = find_pt(d, dxt, 104)
    cup = cup_run(wall_x=dxt, depth=-288, tip_top=240,
                  land_type=d[i0][2])
    c = d[:i0] + cup + d[i104 + 1:]
    out = [c] + [[(x + dxt, y, t, s) for x, y, t, s in contours[i]]
                 for i in range(len(contours)) if i != outer_i]
    # bottomDots inside the cup, per the hah/jeem convention
    anchors = [("top", 224 + dxt, 608), ("topDots", 224 + dxt, 608),
               ("bottom", 232, -304), ("bottomDots", 224, 88)]
    write_glyph(out_name, advance, contours=out, anchors=anchors)


def build_qafDotless_isol():
    _qaf_with_cup("fehDotless-ar.init", "qafDotless-ar", 880, dxt=400)


def build_qafDotless_fina():
    _qaf_with_cup("fehDotless-ar.medi", "qafDotless-ar.fina", 1000, dxt=400)


# ---------------------------------------------------------------------------
# meem family (knot + optional tail / joins)

def _meem_contours(dx, entry_to=None, exit_left=False, tail=False,
                   notch=False):
    """Knot outer contour + counter. Knot spans x dx..dx+416, y 0..368,
    center kx. entry_to: advance x of a right entry bar; exit_left: stub at
    x 0/-16 (bar runs from knot to it); tail: straight descender on the left
    flank; notch: 8-dip under the knot between two bars (medial)."""
    kx = dx + 208
    outer = [(kx, 368, "curve", True),
             (kx + 114, 368, None, False),
             (dx + 416, 286, None, False),
             (dx + 416, 184, "curve", True)]
    # right side down
    if entry_to is None:
        outer += [(dx + 416, 80, None, False),
                  (kx + 114, 0, None, False)]
        bottom_landing = (kx, 0, "curve", True)
    else:
        outer += [(dx + 416, 120, None, False),
                  (dx + 384, 112, None, False),
                  (dx + 352, 112, "curve", False),
                  (dx + 352, 104, "line", False),
                  (entry_to, 104, "line", False),
                  (entry_to, 0, "line", False)]
        bottom_landing = None
    # bottom edge and left side
    if tail:
        if bottom_landing:
            outer += [bottom_landing,
                      (kx - 62, 0, None, False),
                      (dx + 96, 10, None, False)]
        else:
            outer += [(kx + 96, 0, "line", True),
                      (kx + 32, 0, None, False),
                      (dx + 96, 8, None, False)]
        outer += [(dx + 96, 48, "curve", True),
                  (dx + 96, -336, "line", False),
                  (dx + 80, -352, "line", False),
                  (dx + 16, -352, "line", False),
                  (dx, -336, "line", False),
                  (dx, 184, "line", True),
                  (dx, 286, None, False),
                  (kx - 114, 368, None, False)]
    elif exit_left:
        if bottom_landing:
            outer += [bottom_landing]
        elif notch:
            outer += [(kx + 80, 0, "line", True),
                      (kx + 40, 0, None, False),
                      (kx + 16, -8, None, False),
                      (kx, -8, "curve", True),
                      (kx - 16, -8, None, False),
                      (kx - 40, 0, None, False),
                      (kx - 80, 0, "curve", True)]
        outer += [(0, 0, "line", False),
                  (-16, 16, "line", False),
                  (-16, 88, "line", False),
                  (0, 104, "line", False),
                  (dx - 16, 104, "line", False),
                  (dx - 8, 112, "line", False),
                  (dx, 150, None, False),
                  (dx, 166, None, False),
                  (dx, 184, "curve", True),
                  (dx, 286, None, False),
                  (kx - 114, 368, None, False)]
    else:
        outer += [bottom_landing,
                  (kx - 114, 0, None, False),
                  (dx, 80, None, False),
                  (dx, 184, "curve", True),
                  (dx, 286, None, False),
                  (kx - 114, 368, None, False)]
    counter = [(kx, 264, "curve", True),
               (kx - 57, 264, None, False),
               (dx + 104, 228, None, False),
               (dx + 104, 184, "curve", True),
               (dx + 104, 140, None, False),
               (kx - 57, 104, None, False),
               (kx, 104, "curve", True),
               (kx + 57, 104, None, False),
               (dx + 312, 140, None, False),
               (dx + 312, 184, "curve", True),
               (dx + 312, 228, None, False),
               (kx + 57, 264, None, False)]
    return outer, counter


def build_meem_isol():
    outer, counter = _meem_contours(dx=64, tail=True)
    write_glyph("meem-ar", 544, contours=[outer, counter],
                anchors=[("top", 272, 384), ("bottom", 128, -368)])


def build_meem_init():
    outer, counter = _meem_contours(dx=144, exit_left=True)
    # exit_left branch expects stub at x dx-144.. : dx=144 puts it at 0/-16
    write_glyph("meem-ar.init", 560, contours=[outer, counter],
                anchors=[("top", 352, 384), ("bottom", 352, -16)])


def build_meem_medi():
    outer, counter = _meem_contours(dx=144, entry_to=816, exit_left=True,
                                    notch=True)
    write_glyph("meem-ar.medi", 816, contours=[outer, counter],
                anchors=[("top", 352, 384), ("bottom", 352, -24)])


def build_meem_fina():
    outer, counter = _meem_contours(dx=224, entry_to=896, tail=True)
    write_glyph("meem-ar.fina", 896, contours=[outer, counter],
                anchors=[("top", 432, 384), ("bottom", 288, -368)])


# ---------------------------------------------------------------------------
# heh family (ring) — isol plain ring, fina ring+entry, init ring+exit stub

def _ring_contours(dx, w=448, h=432, entry_to=None, exit_left=False):
    kx, ky = dx + w // 2, h // 2
    hx, hy = round(0.55 * w / 2), round(0.55 * h / 2)
    outer = [(kx, h, "curve", True),
             (kx + hx, h, None, False),
             (dx + w, ky + hy, None, False),
             (dx + w, ky, "curve", True)]
    if entry_to is None:
        outer += [(dx + w, ky - hy, None, False),
                  (kx + hx, 0, None, False),
                  (kx, 0, "curve", True)]
    else:
        outer += [(dx + w, ky - hy, None, False),
                  (dx + w - 40, 116, None, False),
                  (dx + w - 72, 112, "curve", False),
                  (dx + w - 72, 104, "line", False),
                  (entry_to, 104, "line", False),
                  (entry_to, 0, "line", False),
                  (kx, 0, "line", True)]
    if exit_left:
        outer += [(0, 0, "line", False),
                  (-16, 16, "line", False),
                  (-16, 88, "line", False),
                  (0, 104, "line", False),
                  (dx - 16, 104, "line", False),
                  (dx - 8, 112, "line", False),
                  (dx, ky - hy + 40, None, False),
                  (dx, ky - 20, None, False),
                  (dx, ky, "curve", True),
                  (dx, ky + hy, None, False),
                  (kx - hx, h, None, False)]
    else:
        outer += [(kx - hx, 0, None, False),
                  (dx, ky - hy, None, False),
                  (dx, ky, "curve", True),
                  (dx, ky + hy, None, False),
                  (kx - hx, h, None, False)]
    iw, ih = w - 208, h - 208
    ihx, ihy = round(0.55 * iw / 2), round(0.55 * ih / 2)
    counter = [(kx, h - 104, "curve", True),
               (kx - ihx, h - 104, None, False),
               (dx + 104, ky + ihy, None, False),
               (dx + 104, ky, "curve", True),
               (dx + 104, ky - ihy, None, False),
               (kx - ihx, 104, None, False),
               (kx, 104, "curve", True),
               (kx + ihx, 104, None, False),
               (dx + w - 104, ky - ihy, None, False),
               (dx + w - 104, ky, "curve", True),
               (dx + w - 104, ky + ihy, None, False),
               (kx + ihx, h - 104, None, False)]
    return outer, counter


def build_heh_isol():
    outer, counter = _ring_contours(dx=64)
    write_glyph("heh-ar", 576, contours=[outer, counter],
                anchors=[("top", 288, 448), ("bottom", 288, -16)])


def build_heh_fina():
    outer, counter = _ring_contours(dx=64, entry_to=704)
    write_glyph("heh-ar.fina", 704, contours=[outer, counter],
                anchors=[("top", 288, 448), ("bottom", 288, -16)])


def build_heh_init():
    outer, counter = _ring_contours(dx=144, exit_left=True)
    write_glyph("heh-ar.init", 592, contours=[outer, counter],
                anchors=[("top", 368, 448), ("bottom", 368, -16)])


# ---------------------------------------------------------------------------
# kaf family: init/medi = lam stem + floating sarkash; isol = fina copy

def sarkash(dx, dy=0):
    """The S-form sarkash from green kaf-ar.fina, translated."""
    donor = read_points("kaf-ar.fina")[1]
    return [(x + dx, y + dy, t, s) for x, y, t, s in donor]


def _copy_glyph(src, out_name, advance=None, strip_contours_after=None):
    from arabic_build import read_points as rp
    import xml.etree.ElementTree as ET
    from arabic_build import glif_path, MASTERS as MM
    root = ET.parse(glif_path(MM[0], src)).getroot()
    adv = advance if advance is not None else float(
        root.find("advance").get("width"))
    contours = rp(src)
    if strip_contours_after is not None:
        contours = contours[:strip_contours_after]
    anchors = [(a.get("name"), float(a.get("x")), float(a.get("y")))
               for a in root.iter("anchor")]
    write_glyph(out_name, adv, contours=contours, anchors=anchors)


KAF_INIT_OUTER = [
    (0, 0, "line", False),
    (352, 0, None, False), (416, 72, None, False),
    (416, 200, "curve", True),
    (416, 752, "line", False),
    (400, 768, "line", False),
    (336, 768, "line", False),
    (320, 752, "line", False),
    (320, 200, "line", True),
    (320, 144, None, False), (280, 104, None, False),
    (224, 104, "curve", True),
    (0, 104, "line", False),
    (-16, 88, "line", False),
    (-16, 16, "line", False),
]

KAF_MEDI_OUTER = [
    (64, 0, "line", False),
    (0, 0, "line", False),
    (-16, 16, "line", False),
    (-16, 88, "line", False),
    (0, 104, "line", False),
    (64, 104, "line", True),
    (320, 104, "line", True),
    (352, 104, None, False), (384, 136, None, False),
    (384, 200, "curve", True),
    (384, 752, "line", False),
    (400, 768, "line", False),
    (464, 768, "line", False),
    (480, 752, "line", False),
    (480, 200, "line", True),
    (480, 136, None, False), (512, 104, None, False),
    (576, 104, "curve", True),
    (640, 104, "line", False),
    (640, 0, "line", False),
    (576, 0, "line", True),
    (520, 0, None, False), (472, 4, None, False),
    (448, 64, "curve", False),
    (432, 64, "line", False),
    (408, 4, None, False), (352, 0, None, False),
    (288, 0, "curve", True),
]


def build_kaf_init():
    write_glyph("kaf-ar.init", 512,
                contours=[list(KAF_INIT_OUTER), sarkash(-248)],
                anchors=[("top", 368, 784), ("bottom", 200, 0)])


def build_kaf_medi():
    write_glyph("kaf-ar.medi", 640,
                contours=[list(KAF_MEDI_OUTER), sarkash(-184)],
                anchors=[("top", 432, 784), ("bottom", 320, 0)])


def build_kaf_isol():
    _copy_glyph("kaf-ar.fina", "kaf-ar")


def build_keheh_init():
    write_glyph("keheh-ar.init", 512,
                contours=[list(KAF_INIT_OUTER), sarkash(-248)],
                anchors=[("top", 368, 784), ("bottom", 200, 0)])


def build_keheh_medi():
    write_glyph("keheh-ar.medi", 640,
                contours=[list(KAF_MEDI_OUTER), sarkash(-184)],
                anchors=[("top", 432, 784), ("bottom", 320, 0)])


def build_keheh_isol():
    _copy_glyph("keheh-ar.fina", "keheh-ar")


# ---------------------------------------------------------------------------
# straightforward derivations from green donors

def build_lam_isol():
    _copy_glyph("lam-ar.fina", "lam-ar", advance=576)


def build_reh_isol():
    _copy_glyph("reh-ar.fina", "reh-ar")


def build_waw_fina():
    # join-gap to the previous letter accepted for now (see worklog)
    _copy_glyph("waw-ar", "waw-ar.fina")


def build_alefMaksura_isol():
    _copy_glyph("yeh-ar.fina", "alefMaksura-ar", strip_contours_after=1)


def build_alefMaksura_fina():
    _copy_glyph("yeh-ar.fina", "alefMaksura-ar.fina", strip_contours_after=1)


def build_farsiYeh_isol():
    _copy_glyph("yeh-ar.fina", "farsiYeh-ar", strip_contours_after=1)


def build_yehBarree(name):
    c = [
        (64, -164, "line", False),
        (80, -180, "line", False),
        (736, -180, "line", True),
        (818, -180, None, False),
        (880, -118, None, False),
        (880, -36, "curve", True),
        (880, 288, "line", False),
        (864, 304, "line", False),
        (800, 304, "line", False),
        (784, 288, "line", False),
        (784, -16, "line", True),
        (784, -58, None, False),
        (750, -76, None, False),
        (700, -76, "curve", True),
        (160, -76, "line", False),
        (80, -76, "line", False),
        (64, -92, "line", False),
    ]
    write_glyph(name, 944, contours=[match_winding(c)],
                anchors=[("top", 832, 320), ("bottom", 420, -196)])


BUILDERS = {
    "behDotless-ar": build_behDotless_isol,
    "behDotless-ar.fina": build_behDotless_fina,
    "noonghunna-ar": build_noonghunna_isol,
    "noonghunna-ar.fina": build_noonghunna_fina,
    "seen-ar.medi": build_seen_medi,
    "seen-ar": build_seen_isol,
    "seen-ar.fina": build_seen_fina,
    "hah-ar.medi": build_hah_medi,
    "hah-ar": build_hah_isol,
    "hah-ar.fina": build_hah_fina,
    "ain-ar": build_ain_isol,
    "ain-ar.fina": build_ain_fina,
    "sad-ar.init": build_sad_init,
    "sad-ar.medi": build_sad_medi,
    "sad-ar": build_sad_isol,
    "sad-ar.fina": build_sad_fina,
    "tah-ar.init": build_tah_init,
    "tah-ar.medi": build_tah_medi,
    "tah-ar": build_tah_isol,
    "tah-ar.fina": build_tah_fina,
    "fehDotless-ar": build_fehDotless_isol,
    "fehDotless-ar.fina": build_fehDotless_fina,
    "lam_alef-ar": build_lam_alef_isol,
    "qafDotless-ar": build_qafDotless_isol,
    "qafDotless-ar.fina": build_qafDotless_fina,
    "meem-ar": build_meem_isol,
    "meem-ar.init": build_meem_init,
    "meem-ar.medi": build_meem_medi,
    "meem-ar.fina": build_meem_fina,
    "heh-ar": build_heh_isol,
    "heh-ar.fina": build_heh_fina,
    "heh-ar.init": build_heh_init,
    "kaf-ar.init": build_kaf_init,
    "kaf-ar.medi": build_kaf_medi,
    "kaf-ar": build_kaf_isol,
    "keheh-ar.init": build_keheh_init,
    "keheh-ar.medi": build_keheh_medi,
    "keheh-ar": build_keheh_isol,
    "lam-ar": build_lam_isol,
    "reh-ar": build_reh_isol,
    "waw-ar.fina": build_waw_fina,
    "alefMaksura-ar": build_alefMaksura_isol,
    "alefMaksura-ar.fina": build_alefMaksura_fina,
    "farsiYeh-ar": build_farsiYeh_isol,
    "yehBarree-ar": lambda: build_yehBarree("yehBarree-ar"),
    "yehBarree-ar.fina": lambda: build_yehBarree("yehBarree-ar.fina"),
}


def main():
    args = sys.argv[1:]
    names = list(BUILDERS) if args == ["--all"] else args
    for n in names:
        BUILDERS[n]()


if __name__ == "__main__":
    main()
