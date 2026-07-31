"""
Generate visual assets for the Meridian Astrolabium repository.

Eat your own cooking. Every image is produced by the project's own code
from the project's own data. The geometry is the argument.

Outputs:
  assets/banner.png              — repository banner (the twelve-fold wheel)
  assets/divine-hours-wheel.png  — 8-fold unequal hour division at a location
  assets/lunar-architecture.png  — 6+2 Cantong qi trigram-law cycle
  assets/temporal-bodies.png     — The four temporal bodies, concentric

Palette: the eight ADONAJ BA Law colours. The prime-Law derivation is
held in the parent Falco research environment.

Background    #0D0D0D  void
Bone          #E8E8E0  text
Gold          #D4A845  heading accent (the sunrise-key Law is Fall of Events)
Silver        #9FA7B3  the sunset key
Dim accent    #2A2A3A  panel edges
"""

from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Wedge
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ── Repo layout ──
REPO = Path(__file__).resolve().parents[1]
ASTRO_SRC = REPO / "astrolabium" / "src"
ASSETS = REPO / "assets"
ASSETS.mkdir(exist_ok=True)

sys.path.insert(0, str(REPO / "astrolabium"))
sys.path.insert(0, str(ASTRO_SRC))

# ── Register Windows fonts with CJK + trigram glyph coverage ──
FONTS_DIR = Path("C:/Windows/Fonts")
for fname in ["msyh.ttc", "seguisym.ttf", "cambria.ttc", "consola.ttf"]:
    fpath = FONTS_DIR / fname
    if fpath.exists():
        try:
            fm.fontManager.addfont(str(fpath))
        except Exception:
            pass

# Matplotlib won't pick fallback fonts from a multi-family list across glyph
# coverage automatically — but it does honor a per-text fontfamily list. We
# set the global font to a stack that resolves CJK and trigram chars correctly.
plt.rcParams["font.family"] = ["Consolas", "Microsoft YaHei", "Segoe UI Symbol", "DejaVu Sans Mono"]
plt.rcParams["font.monospace"] = ["Consolas", "Microsoft YaHei", "Segoe UI Symbol", "DejaVu Sans Mono"]

# ── Palette (prime-law correspondence) ──
LAW_COLORS = {
    "Synchronicity":        "#FF9500",  # 89  Qian ☰  Full Moon       orange / Heart
    "Sole Atom":            "#00E676",  # 19  Zhen ☳  First Crescent  green  / Sexual Organs
    "Divinity":             "#E8E8F0",  # 31  Li ☲    Silver Key      white  / Crown
    "Geometric Essence":    "#E74C3C",  # 67  Xun ☴  Waning Gibbous  brick  / Sacrum
    "Time Matrix":          "#A8B4C0",  # 29  Dui ☱  First Quarter   silver / Mobile 8th
    "Fall of Events":       "#7B68EE",  # 11  Kan ☵  Gold Key        indigo / Third Eye
    "Kaos":                 "#FFD700",  # 23  Kun ☷  New Moon        gold   / Solar Plexus
    "Arrow of Complexity":  "#00BFFF",  # 17  Gen ☶  Last Quarter    azure  / Throat
}
BG          = "#0D0D0D"
BONE        = "#E8E8E0"
SILVER      = "#C0C0C0"
SILVER_KEY  = "#9FA7B3"
GOLD        = "#D4A845"
INDIGO      = "#3D3D6B"
DIM         = "#2A2A3A"

# Six cyclic Laws (in lunar-phase order, starting at New Moon)
SIX_PHASE_LAWS = [
    ("Kaos",                "Kun",  "☷", "New Moon"),
    ("Sole Atom",           "Zhen", "☳", "Waxing Crescent"),
    ("Time Matrix",         "Dui",  "☱", "First Quarter / Waxing Gibbous"),
    ("Synchronicity",       "Qian", "☰", "Full Moon"),
    ("Geometric Essence",   "Xun",  "☴", "Waning Gibbous"),
    ("Arrow of Complexity", "Gen",  "☶", "Last Quarter / Waning Crescent"),
]

# Twelve Earthly Branches (organ-clock windows), in canonical order from 子
EARTHLY_BRANCHES = [
    ("子", "Zi",   "GB",  "Gall Bladder"),
    ("丑", "Chou", "Liv", "Liver"),
    ("寅", "Yin",  "Lu",  "Lung"),
    ("卯", "Mao",  "LI",  "Large Intestine"),
    ("辰", "Chen", "St",  "Stomach"),
    ("巳", "Si",   "Sp",  "Spleen"),
    ("午", "Wu",   "Ht",  "Heart"),
    ("未", "Wei",  "SI",  "Small Intestine"),
    ("申", "Shen", "Bl",  "Bladder"),
    ("酉", "You",  "Kid", "Kidney"),
    ("戌", "Xu",   "Per", "Pericardium"),
    ("亥", "Hai",  "SJ",  "San Jiao"),
]

DIVINE_MONTHS = [
    "ISIS", "SADAM", "LIOTHIL", "EOROS",
    "TASUMER", "MENON", "OSIRIS", "AGAFEST",
    "SAMMA", "SET", "SADAS", "DESURIORIS",
]


# ════════════════════════════════════════════════════════════════════
#  RHOMBIC DODECAHEDRON — clean geometric construction
# ════════════════════════════════════════════════════════════════════

def rhombic_dodecahedron():
    """
    Return (vertices, faces, face_centers, face_normals) for the rhombic
    dodecahedron centered at origin.

    Vertices: 6 axis-vertices at distance 2 (degree-4), and 8 corner-vertices
    at (±1, ±1, ±1) (degree-3). Total: 14 vertices.

    Faces: 12 rhombic faces. Each face = (axis_a, corner+, axis_b, corner-)
    where axis_a and axis_b are on perpendicular axes, and the two corner
    vertices share signs on axis_a and axis_b while differing on the third.

    [MATHEMATICAL FACT] — standard construction, dual of cuboctahedron.
    Verified: 14 vertices, 24 edges, 12 faces, Euler V-E+F = 2. ✓
    """
    # 6 axis vertices, indexed 0..5
    AX = {
        (+1, 0, 0): 0, (-1, 0, 0): 1,
        (0, +1, 0): 2, (0, -1, 0): 3,
        (0, 0, +1): 4, (0, 0, -1): 5,
    }
    AX_pos = {v: 2.0 * np.array(k, dtype=float) for k, v in AX.items()}

    # 8 corner vertices, indexed 6..13
    CR = {}
    next_idx = 6
    for sx in (+1, -1):
        for sy in (+1, -1):
            for sz in (+1, -1):
                CR[(sx, sy, sz)] = next_idx
                next_idx += 1
    CR_pos = {v: np.array(k, dtype=float) for k, v in CR.items()}

    verts = np.zeros((14, 3))
    for v, pos in AX_pos.items():
        verts[v] = pos
    for v, pos in CR_pos.items():
        verts[v] = pos

    # Build the 12 faces.
    # For each ordered pair of perpendicular axes (e.g., +X and +Y),
    # the face has vertices: +X, (+1,+1,+1), +Y, (+1,+1,-1).
    # The third axis (Z here) provides the two corners differing in sign.
    face_list = []
    AXIS_KEYS = list(AX.keys())  # 6 axis directions
    seen_pairs = set()
    for ka in AXIS_KEYS:
        for kb in AXIS_KEYS:
            if ka == kb:
                continue
            # Find the dimension that's nonzero in each
            dim_a = next(i for i, c in enumerate(ka) if c != 0)
            dim_b = next(i for i, c in enumerate(kb) if c != 0)
            if dim_a == dim_b:
                continue  # parallel axes (e.g., +X and -X)
            # Skip duplicate face (each face is shared by ordered pair {a,b})
            key = tuple(sorted([ka, kb]))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            sign_a = ka[dim_a]
            sign_b = kb[dim_b]
            dim_c = ({0, 1, 2} - {dim_a, dim_b}).pop()
            # Find the two corner vertices that match sign_a on dim_a and
            # sign_b on dim_b, differing only in dim_c.
            corner_plus = [0, 0, 0]
            corner_plus[dim_a] = sign_a
            corner_plus[dim_b] = sign_b
            corner_plus[dim_c] = +1
            corner_minus = list(corner_plus)
            corner_minus[dim_c] = -1
            i_axis_a = AX[ka]
            i_axis_b = AX[kb]
            i_corner_plus = CR[tuple(corner_plus)]
            i_corner_minus = CR[tuple(corner_minus)]
            # Order vertices around the rhombus: axis_a -> corner+ -> axis_b -> corner-
            face_list.append((i_axis_a, i_corner_plus, i_axis_b, i_corner_minus))

    assert len(face_list) == 12, f"Expected 12 faces, got {len(face_list)}"

    centers = np.array([verts[list(f)].mean(axis=0) for f in face_list])
    # Normals point from origin to face center (centered at origin, faces tangent to inscribed sphere)
    normals = centers / np.linalg.norm(centers, axis=1, keepdims=True)

    return verts, face_list, centers, normals


def render_banner(save_path: Path):
    """
    The hero banner. Composition:
      - Title bar (top)
      - Big clean RD in the center, faces colored by 6-cyclic-law palette
      - Numbers strip (right side, vertical)
      - Tagline (bottom)
    """
    fig = plt.figure(figsize=(16, 7), facecolor=BG)
    gs = fig.add_gridspec(
        1, 2, width_ratios=[2.4, 1.0],
        wspace=0.02,
        left=0.02, right=0.97, top=0.86, bottom=0.10
    )

    # ── center: rhombic dodecahedron ──
    ax = fig.add_subplot(gs[0, 0], projection="3d", facecolor=BG)
    verts, faces, centers, normals = rhombic_dodecahedron()

    # Sort faces back-to-front for a clean render (Painter's algorithm).
    view = np.array([1.1, 0.9, 0.5])
    view = view / np.linalg.norm(view)
    face_depth = [(i, np.dot(centers[i], view)) for i in range(12)]
    face_depth.sort(key=lambda t: t[1])  # back first

    # Color faces by 6-cyclic law (each law gets 2 faces, opposite each other)
    cyclic_law_keys = ["Kaos", "Arrow of Complexity", "Time Matrix",
                       "Synchronicity", "Geometric Essence", "Sole Atom"]
    # Assign by direction: faces with closely-aligned normals share a color
    # Sort faces by Z then Y then X to get a stable indexing
    face_order_for_color = sorted(range(12), key=lambda i: (centers[i, 2], centers[i, 1], centers[i, 0]))
    face_color_map = {}
    for slot, face_idx in enumerate(face_order_for_color):
        face_color_map[face_idx] = LAW_COLORS[cyclic_law_keys[slot % 6]]

    # Build polygons in depth order
    polys = []
    colors = []
    alphas = []
    for face_idx, depth in face_depth:
        pts = verts[list(faces[face_idx])]
        polys.append(pts)
        colors.append(face_color_map[face_idx])
        # Front-facing faces brighter, back-facing dimmer
        front = depth > 0
        alphas.append(0.85 if front else 0.35)

    pc = Poly3DCollection(polys, facecolors=colors,
                          edgecolors=BONE, linewidths=0.7)
    pc.set_alpha(0.75)  # global alpha; per-face alphas via facecolors below
    # Re-apply per-face alphas through the facecolors RGBA
    from matplotlib.colors import to_rgba
    fc_rgba = []
    for c, a in zip(colors, alphas):
        r, g, b, _ = to_rgba(c)
        fc_rgba.append((r, g, b, a))
    pc.set_facecolors(fc_rgba)
    ax.add_collection3d(pc)

    # Axis vertices (degree-4) marked in gold; corner vertices (degree-3) in silver
    ax.scatter(verts[:6, 0], verts[:6, 1], verts[:6, 2],
               c=GOLD, s=40, depthshade=True, edgecolors=BG, linewidths=0.6)
    ax.scatter(verts[6:, 0], verts[6:, 1], verts[6:, 2],
               c=SILVER_KEY, s=22, depthshade=True, edgecolors=BG, linewidths=0.6)

    # Label the 12 front-facing faces with their Earthly Branch glyph
    for face_idx, depth in face_depth:
        if depth <= 0.05:
            continue  # back-facing, skip label
        # Position label slightly outside the face center along the normal
        n = normals[face_idx]
        p = centers[face_idx] + n * 0.55
        # Map face order to a branch (deterministic, by face-color slot)
        slot = face_order_for_color.index(face_idx)
        zh, pinyin, abbr, organ = EARTHLY_BRANCHES[slot]
        ax.text(p[0], p[1], p[2], zh, color=BONE,
                fontsize=12, ha="center", va="center", fontweight="bold")

    ax.set_xlim(-2.6, 2.6); ax.set_ylim(-2.6, 2.6); ax.set_zlim(-2.6, 2.6)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_axis_off()
    ax.view_init(elev=22, azim=32)
    ax.set_box_aspect([1, 1, 1])

    # ── right: numbers strip + tagline ──
    axR = fig.add_subplot(gs[0, 1], facecolor=BG)
    axR.set_xlim(0, 1); axR.set_ylim(0, 1); axR.set_axis_off()

    # Stack of big numbers
    numbers = [
        ("12", "rhombic faces"),
        ("6+2", "trigram laws"),
        ("8",  "extraordinary vessels"),
        ("8",  "divine hours"),
        ("13", "divine months"),
        ("6",  "great rites"),
    ]
    y = 0.96
    for n, label in numbers:
        axR.text(0.04, y, n, color=GOLD, fontsize=28, fontweight="bold",
                 ha="left", va="top",
                 family=["Consolas", "DejaVu Sans Mono"])
        axR.text(0.32, y - 0.012, label, color=BONE, fontsize=11,
                 ha="left", va="top", alpha=0.85,
                 family=["Consolas", "DejaVu Sans Mono"])
        y -= 0.115

    # Bottom of right column: derivation arrows
    axR.text(0.04, 0.18, "M E R I D I A N", color=BONE, fontsize=14,
             fontweight="bold", ha="left", va="top",
             family=["Consolas", "DejaVu Sans Mono"])
    axR.text(0.04, 0.12, "navigates the astrolabium", color=SILVER,
             fontsize=9, ha="left", va="top", style="italic", alpha=0.75,
             family=["Consolas", "DejaVu Sans Mono"])

    # ── title bar ──
    fig.text(0.5, 0.94,
             "A S T R O L A B I U M    C A U D A E    R U B R A E",
             ha="center", va="center", fontsize=22, fontweight="bold",
             color=BONE,
             family=["Consolas", "DejaVu Sans Mono"], alpha=0.95)
    fig.text(0.5, 0.905,
             "the red tail astrolabe  ·  a temporal navigation instrument",
             ha="center", va="center", fontsize=11, color=SILVER,
             family=["Consolas", "DejaVu Sans Mono"],
             style="italic", alpha=0.78)

    # ── footer ──
    fig.text(0.5, 0.05,
             "rhombic dodecahedron  ·  12 faces  ·  12 organ windows  ·  the geometry is the argument",
             ha="center", va="center", fontsize=10, color=GOLD,
             family=["Consolas", "DejaVu Sans Mono"], alpha=0.75)

    fig.savefig(save_path, dpi=200, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)
    print(f"  banner          → {save_path.relative_to(REPO)}")


# ════════════════════════════════════════════════════════════════════
#  DIVINE HOURS WHEEL — computed live from solar engine for a location
# ════════════════════════════════════════════════════════════════════

def render_divine_hours_wheel(save_path: Path,
                              dt: datetime,
                              lat: float, lon: float, tz: str,
                              location_name: str):
    """
    Compute the eight Divine Hours from the live solar engine. Eat your
    own cooking: the image embodies the actual numbers for this place
    and date.
    """
    from engine import solar  # type: ignore

    solar_pos = solar.get_solar_positions(dt, lat, lon, tz)
    sunrise = solar_pos["sunrise"]
    sunset = solar_pos["sunset"]
    next_solar = solar.get_solar_positions(dt + timedelta(days=1), lat, lon, tz)
    next_sunrise = next_solar["sunrise"]

    day_seconds = (sunset - sunrise).total_seconds()
    day_hour_len = day_seconds / 4
    night_seconds = (next_sunrise - sunset).total_seconds()
    night_hour_len = night_seconds / 4

    fig, ax = plt.subplots(figsize=(9, 9), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-1.35, 1.35); ax.set_ylim(-1.35, 1.35)
    ax.set_aspect("equal"); ax.set_axis_off()

    outer_r = 1.0
    inner_r = 0.55

    # DAY WING — top half (sunrise at left = 180°, midday at top = 90°, sunset at right = 0°)
    day_hour_labels = ["I", "II", "III", "IV"]
    for i in range(4):
        theta_start = 180 - i * 45         # 180, 135, 90, 45
        theta_end   = 180 - (i + 1) * 45   # 135, 90, 45, 0
        w = Wedge((0, 0), outer_r, theta_end, theta_start,
                  width=outer_r - inner_r,
                  facecolor=GOLD, edgecolor=BONE, linewidth=0.8, alpha=0.32)
        ax.add_patch(w)
        mid_theta = np.radians((theta_start + theta_end) / 2)
        r_label = (outer_r + inner_r) / 2
        ax.text(r_label * np.cos(mid_theta), r_label * np.sin(mid_theta),
                day_hour_labels[i], color=BG, fontsize=18, fontweight="bold",
                ha="center", va="center", family=["Consolas"])

    # NIGHT WING — bottom half (sunset at right = 0°, midnight at bottom = -90°, next sunrise at left = 180°)
    night_hour_labels = ["V", "VI", "VII", "VIII"]
    for i in range(4):
        theta_start = -i * 45         # 0, -45, -90, -135
        theta_end   = -(i + 1) * 45   # -45, -90, -135, -180
        w = Wedge((0, 0), outer_r, theta_end, theta_start,
                  width=outer_r - inner_r,
                  facecolor=INDIGO, edgecolor=BONE, linewidth=0.8, alpha=0.65)
        ax.add_patch(w)
        mid_theta = np.radians((theta_start + theta_end) / 2)
        r_label = (outer_r + inner_r) / 2
        ax.text(r_label * np.cos(mid_theta), r_label * np.sin(mid_theta),
                night_hour_labels[i], color=BONE, fontsize=18, fontweight="bold",
                ha="center", va="center", family=["Consolas"])

    # Wing dividers (sunrise/sunset axis)
    ax.plot([-outer_r * 1.05, outer_r * 1.05], [0, 0],
            color=BONE, linewidth=1.0, alpha=0.6, zorder=4)

    # Center disk
    center = plt.Circle((0, 0), inner_r, color=BG, ec=BONE, lw=1.5, zorder=2)
    ax.add_patch(center)

    # Solar cardinal points
    for theta_deg, label, color, glyph in [
        (180, "sunrise",  GOLD,       "☉↑"),
        (90,  "midday",   GOLD,       "☉⌒"),
        (0,   "sunset",   SILVER_KEY, "☉↓"),
        (270, "midnight", SILVER_KEY, "☽"),
    ]:
        theta = np.radians(theta_deg)
        x, y = 1.15 * np.cos(theta), 1.15 * np.sin(theta)
        ax.text(x, y, label, color=color, fontsize=11, fontweight="bold",
                ha="center", va="center", family=["Consolas"])

    # Center text
    day_mm = int(round(day_hour_len / 60))
    night_mm = int(round(night_hour_len / 60))
    ax.text(0, 0.22, location_name, color=BONE, fontsize=13, fontweight="bold",
            ha="center", va="center", family=["Consolas"])
    ax.text(0, 0.10, dt.strftime("%Y - %m - %d"), color=SILVER, fontsize=10,
            ha="center", va="center", family=["Consolas"])
    ax.text(0, -0.05, f"day hour:   {day_mm} min", color=GOLD, fontsize=10,
            ha="center", va="center", family=["Consolas"], alpha=0.9)
    ax.text(0, -0.18, f"night hour: {night_mm} min", color=SILVER_KEY,
            fontsize=10, ha="center", va="center",
            family=["Consolas"], alpha=0.9)
    ax.text(0, -0.34, f"{lat:.2f}°  ·  {lon:.2f}°", color=SILVER,
            fontsize=9, ha="center", va="center",
            family=["Consolas"], alpha=0.7)

    # Title
    fig.text(0.5, 0.96, "T H E   D I V I N E   H O U R S",
             ha="center", va="top", fontsize=16, fontweight="bold",
             color=BONE, family=["Consolas"])
    fig.text(0.5, 0.925,
             "first wing (day, 4 hours)  ·  second wing (night, 4 hours)",
             ha="center", va="top", fontsize=10, color=SILVER,
             family=["Consolas"], style="italic", alpha=0.78)
    fig.text(0.5, 0.04,
             "every hour derives from solar position at your location",
             ha="center", va="bottom", fontsize=10, color=GOLD,
             family=["Consolas"], alpha=0.75)

    fig.savefig(save_path, dpi=200, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)
    print(f"  divine hours    → {save_path.relative_to(REPO)}")


# ════════════════════════════════════════════════════════════════════
#  LUNAR ARCHITECTURE — 6+2 Cantong qi cycle
# ════════════════════════════════════════════════════════════════════

def render_lunar_architecture(save_path: Path):
    """The 6+2 Cantong qi architecture: six trigrams around the moon,
    two Solar Keys above and below as sunrise/sunset cusps.

    Layout: the six cyclic phases occupy the canonical hexagonal positions
    around the moon at radius R. The two Solar Keys sit OUTSIDE the hex,
    at top-center (Gold/sunrise) and bottom-center (Silver/sunset), so
    they visually read as 'outside the cycle' and never collide with the
    cyclic labels (which radiate outward from the hex positions).
    """
    fig, ax = plt.subplots(figsize=(11, 12), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-2.4, 2.4)
    ax.set_aspect("equal"); ax.set_axis_off()

    R = 1.05
    # The six cyclic positions, placed at canonical hexagonal angles
    # offset 30° from the cardinals so the top/bottom slots are free for
    # the two Solar Keys.  Position 0 = upper-right, going clockwise.
    cyclic_angles_deg = [60, 0, -60, -120, 180, 120]
    # SIX_PHASE_LAWS is in lunar-phase order starting at New Moon.
    # Place New Moon at the leftmost (180°) so the cycle reads
    # NM → top → Full → bottom → NM in the natural waxing-then-waning
    # order. To do that we'll re-index:
    angle_assignment = [180, 120, 60, 0, -60, -120]
    for (law, pinyin, glyph, phase), theta_deg in zip(SIX_PHASE_LAWS, angle_assignment):
        theta = np.radians(theta_deg)
        x, y = R * np.cos(theta), R * np.sin(theta)

        color = LAW_COLORS[law]
        node = plt.Circle((x, y), 0.20, facecolor=color,
                          edgecolor=BONE, linewidth=1.4, alpha=0.92, zorder=3)
        ax.add_patch(node)
        ax.text(x, y + 0.03, glyph, color=BONE, fontsize=18,
                fontweight="bold", ha="center", va="center", zorder=4,
                family=["Segoe UI Symbol", "DejaVu Sans"])
        ax.text(x, y - 0.08, pinyin, color=BONE, fontsize=8,
                ha="center", va="center", zorder=4, family=["Consolas"])

        # External label — radiates outward along the same radius
        r_label = R + 0.55
        lx, ly = r_label * np.cos(theta), r_label * np.sin(theta)
        # Horizontal alignment by side
        ha = "center"
        if lx < -0.3:
            ha = "right"
        elif lx > 0.3:
            ha = "left"
        ax.text(lx, ly + 0.06, law, color=color, fontsize=10,
                fontweight="bold", ha=ha, va="center", family=["Consolas"])
        ax.text(lx, ly - 0.06, phase, color=SILVER, fontsize=8,
                ha=ha, va="center", alpha=0.78, family=["Consolas"])

    # The lunar cycle ring (hexagonal path through the six nodes)
    ring_theta = np.linspace(0, 2 * np.pi, 200)
    ax.plot(R * np.cos(ring_theta), R * np.sin(ring_theta),
            color=DIM, linewidth=1.0, alpha=0.55, zorder=1)

    # Two Solar Keys — top (Gold/sunrise) and bottom (Silver/sunset)
    # Outside the cycle, no horizontal collision with cyclic labels.
    key_specs = [
        # (x, y, name, pinyin, glyph, when, fill, accent, label_y_offset)
        (0,  1.85,  "Gold Key",   "Kǎn", "☵", "sunrise cusp",
         LAW_COLORS["Fall of Events"], GOLD,        +0.40),
        (0, -1.85,  "Silver Key", "Lí",  "☲", "sunset cusp",
         LAW_COLORS["Divinity"],       SILVER_KEY,  -0.40),
    ]
    for x, y, name, pinyin, glyph, when, fill_color, accent, label_dy in key_specs:
        node = plt.Circle((x, y), 0.24, facecolor=fill_color,
                          edgecolor=accent, linewidth=2.2, alpha=0.95, zorder=3)
        ax.add_patch(node)
        ax.text(x, y + 0.03, glyph, color=BONE, fontsize=22,
                fontweight="bold", ha="center", va="center", zorder=4,
                family=["Segoe UI Symbol", "DejaVu Sans"])
        ax.text(x, y - 0.10, pinyin, color=BONE, fontsize=8,
                ha="center", va="center", zorder=4, family=["Consolas"])
        # Label OUTSIDE the node, away from the cycle
        ax.text(x, y + label_dy, name, color=accent, fontsize=12,
                fontweight="bold", ha="center", va="center", family=["Consolas"])
        ax.text(x, y + label_dy + (0.12 if label_dy > 0 else -0.12),
                when, color=SILVER, fontsize=9,
                ha="center", va="center", style="italic", alpha=0.78,
                family=["Consolas"])
        # Dashed connector down/up to the cycle ring
        sgn = -1 if y > 0 else +1   # dashed line from key TOWARD moon
        ax.plot([0, 0],
                [y + sgn * 0.24, sgn * R * 0.95],
                color=accent, linewidth=0.9,
                linestyle="--", alpha=0.45, zorder=1)

    # Center: the moon
    moon = plt.Circle((0, 0), 0.22, facecolor=BG, edgecolor=BONE,
                      linewidth=1.8, zorder=2)
    ax.add_patch(moon)
    ax.text(0, 0.03, "☽", color=BONE, fontsize=26, ha="center", va="center", zorder=3,
            family=["Segoe UI Symbol", "DejaVu Sans"])
    ax.text(0, -0.16, "lunar month", color=SILVER, fontsize=9,
            ha="center", va="center", family=["Consolas"], alpha=0.75)

    # Title
    fig.text(0.5, 0.965, "T H E   6 + 2   A R C H I T E C T U R E",
             ha="center", va="top", fontsize=16, fontweight="bold",
             color=BONE, family=["Consolas"])
    fig.text(0.5, 0.935,
             "six trigrams carry six laws around the lunar month  ·  two solar keys cusp at sunrise and sunset",
             ha="center", va="top", fontsize=10, color=SILVER,
             family=["Consolas"], style="italic", alpha=0.78)
    fig.text(0.5, 0.04,
             "from the cantong qi  ·  火候 huǒ hòu  ·  the fire phasing of the alchemical work",
             ha="center", va="bottom", fontsize=10, color=GOLD,
             family=["Consolas", "Microsoft YaHei"], alpha=0.75)

    fig.savefig(save_path, dpi=200, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)
    print(f"  lunar arch.     → {save_path.relative_to(REPO)}")


# ════════════════════════════════════════════════════════════════════
#  TEMPORAL BODIES — concentric rings
# ════════════════════════════════════════════════════════════════════

def render_temporal_bodies(save_path: Path):
    """The four temporal bodies as nested concentric rings.

    Each ring is labeled with a radial callout at a distinct angle so the
    four labels never collide. Period of each layer is shown on the
    callout line.
    """
    fig, ax = plt.subplots(figsize=(11, 11), facecolor=BG)
    ax.set_facecolor(BG)
    ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal"); ax.set_axis_off()

    # Concentric rings: outermost = fastest layer (Gross), innermost = slowest (Soul).
    # Each ring also has a callout angle so labels distribute around the figure.
    rings = [
        # (outer_r, inner_r, color, body_name,   layer_name,    period_text,                 callout_angle_deg)
        (1.20, 0.95, LAW_COLORS["Synchronicity"],     "GROSS",  "Organ Clock",  "12 windows · solar branches · ~2 h",        45),
        (0.95, 0.72, LAW_COLORS["Time Matrix"],       "ASTRAL", "LGBF Vessels", "8 extraordinary vessels · stem-branch · ~2 h", 135),
        (0.72, 0.50, LAW_COLORS["Divinity"],          "KEYS",   "Solar Keys",   "2 keys · gold sunrise · silver sunset",     225),
        (0.50, 0.25, LAW_COLORS["Geometric Essence"], "SOUL",   "Primeval Law", "6 cyclic laws · lunar phase · ~4.9 d",      315),
    ]

    for outer_r, inner_r, color, body_name, layer_name, period_text, ang_deg in rings:
        ring = Wedge((0, 0), outer_r, 0, 360, width=outer_r - inner_r,
                     facecolor=color, edgecolor=BONE, linewidth=1.1, alpha=0.55)
        ax.add_patch(ring)
        r_mid = (outer_r + inner_r) / 2

        # Callout: a short line from the ring midpoint outward to a label
        ang = np.radians(ang_deg)
        x0, y0 = r_mid * np.cos(ang), r_mid * np.sin(ang)
        r_outer_label = outer_r + 0.30
        x1, y1 = r_outer_label * np.cos(ang), r_outer_label * np.sin(ang)
        ax.plot([x0, x1], [y0, y1], color=color, linewidth=1.0, alpha=0.7, zorder=4)

        # Label block: body name (top), layer name (middle), period (bottom)
        # Position offset further along the same angle
        r_text = r_outer_label + 0.05
        tx, ty = r_text * np.cos(ang), r_text * np.sin(ang)
        # Horizontal alignment based on quadrant
        ha = "left" if np.cos(ang) >= 0 else "right"
        ax.text(tx, ty + 0.16, body_name, color=BONE, fontsize=13,
                fontweight="bold", ha=ha, va="center", family=["Consolas"])
        ax.text(tx, ty + 0.02, layer_name, color=color, fontsize=11,
                fontweight="bold", ha=ha, va="center", family=["Consolas"])
        ax.text(tx, ty - 0.13, period_text, color=SILVER, fontsize=8,
                ha=ha, va="center", style="italic", alpha=0.80, family=["Consolas"])

    # Center
    center = plt.Circle((0, 0), 0.22, facecolor=BG, edgecolor=BONE,
                        linewidth=1.5, zorder=5)
    ax.add_patch(center)
    ax.text(0, 0.04, "☉", color=GOLD, fontsize=28, ha="center", va="center", zorder=6,
            family=["Segoe UI Symbol", "DejaVu Sans"])
    ax.text(0, -0.14, "you", color=BONE, fontsize=11, zorder=6,
            ha="center", va="center", family=["Consolas"], alpha=0.9)

    # Title
    fig.text(0.5, 0.965, "T H E   F O U R   T E M P O R A L   B O D I E S",
             ha="center", va="top", fontsize=16, fontweight="bold",
             color=BONE, family=["Consolas"])
    fig.text(0.5, 0.935,
             "from soul (slowest) to gross (fastest)  ·  unity is when adjacent bodies say the same thing",
             ha="center", va="top", fontsize=10, color=SILVER,
             family=["Consolas"], style="italic", alpha=0.78)
    fig.text(0.5, 0.04,
             "every layer derives from astronomical position at your location",
             ha="center", va="bottom", fontsize=10, color=GOLD,
             family=["Consolas"], alpha=0.75)

    fig.savefig(save_path, dpi=200, bbox_inches="tight",
                facecolor=BG, pad_inches=0.25)
    plt.close(fig)
    print(f"  temporal bodies → {save_path.relative_to(REPO)}")


# ════════════════════════════════════════════════════════════════════
#  ENTRY
# ════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("Generating Astrolabium visual assets...")
    print()

    render_banner(ASSETS / "banner.png")

    import pytz
    rome = pytz.timezone("Europe/Rome")
    spring_eq = rome.localize(datetime(2026, 3, 20, 12, 0, 0))
    render_divine_hours_wheel(
        ASSETS / "divine-hours-wheel.png",
        dt=spring_eq,
        lat=45.4167, lon=7.7833, tz="Europe/Rome",
        location_name="Damanhur, Italy",
    )

    render_lunar_architecture(ASSETS / "lunar-architecture.png")
    render_temporal_bodies(ASSETS / "temporal-bodies.png")

    print()
    print("All assets generated. Eat your own cooking.")
