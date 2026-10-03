"""Generates the animated SVG assets for the GitHub profile README."""
import math, random

AMBER = "#ffb000"
AMBER_DIM = "#5c4100"
AMBER_FAINT = "#2a1e00"
INK = "#f5efe2"
GREY = "#a39d92"
GREY_DIM = "#6b665c"
RED = "#ff4b2b"
GREEN = "#7dff8a"
BG = "#080706"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def defs_common():
    return f"""
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
    <path d="M24 0H0V24" fill="none" stroke="{AMBER_FAINT}" stroke-width="1"/>
  </pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity="0.22"/>
  </pattern>"""


def brackets(w, h, m=10, s=18, color=AMBER, sw=2):
    pts = [
        (m, m + s, m, m, m + s, m),
        (w - m - s, m, w - m, m, w - m, m + s),
        (m, h - m - s, m, h - m, m + s, h - m),
        (w - m - s, h - m, w - m, h - m, w - m, h - m - s),
    ]
    return "".join(
        f'<path d="M{a} {b}L{c} {d}L{e} {f}" fill="none" stroke="{color}" stroke-width="{sw}"/>'
        for a, b, c, d, e, f in pts
    )


def blink(dur="1.2s", begin="0s"):
    return f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.55;1" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'


# ───────────────────────────── HEADER ─────────────────────────────
def header():
    W, H = 840, 400
    cx, cy, R = 200, 205, 150
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">')
    o.append(f"<defs>{defs_common()}")
    o.append(f'<radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{AMBER}" stop-opacity="0.12"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient>')
    o.append(f'<clipPath id="nameclip"><rect x="390" y="80" width="0" height="140"><animate attributeName="width" from="0" to="440" dur="1.4s" begin="0.3s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1" keyTimes="0;1"/></rect></clipPath>')
    o.append("</defs>")
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#grid)"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R+40}" fill="url(#glow)"/>')

    # radar rings & ticks
    for r in (R, R * 0.75, R * 0.5, R * 0.25):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="none" stroke="{AMBER_DIM}" stroke-width="1"/>')
    o.append(f'<path d="M{cx-R} {cy}H{cx+R}M{cx} {cy-R}V{cy+R}" stroke="{AMBER_DIM}" stroke-width="1"/>')
    for deg in range(0, 360, 5):
        a = math.radians(deg)
        l = 10 if deg % 30 == 0 else 4
        x1, y1 = cx + R * math.cos(a), cy + R * math.sin(a)
        x2, y2 = cx + (R + l) * math.cos(a), cy + (R + l) * math.sin(a)
        o.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{AMBER if deg%30==0 else AMBER_DIM}" stroke-width="1"/>')
    for deg in range(0, 360, 30):
        a = math.radians(deg - 90)
        x, y = cx + (R + 24) * math.cos(a), cy + (R + 24) * math.sin(a) + 3
        o.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{GREY_DIM}" font-size="8" text-anchor="middle">{deg:03d}</text>')

    # sweep (rotates clockwise, starts pointing up)
    sweep = []
    steps = 14
    for i in range(steps):
        a0 = math.radians(-90 - i * 3.2)
        a1 = math.radians(-90 - (i + 1) * 3.2)
        op = 0.55 * (1 - i / steps) ** 1.6
        sweep.append(
            f'<path d="M{cx} {cy}L{cx+R*math.cos(a0):.1f} {cy+R*math.sin(a0):.1f}A{R} {R} 0 0 0 {cx+R*math.cos(a1):.1f} {cy+R*math.sin(a1):.1f}Z" fill="{AMBER}" opacity="{op:.3f}"/>'
        )
    sweep.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-R}" stroke="{AMBER}" stroke-width="2"/>')
    o.append(f'<g>{"".join(sweep)}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="5s" repeatCount="indefinite"/></g>')

    # contacts: UAV / AUV / UGV — light up when the sweep passes
    contacts = [("UAV", 40, 0.78), ("AUV", 155, 0.55), ("UGV", 255, 0.85), ("???", 320, 0.35)]
    for label, bearing, dist in contacts:
        a = math.radians(bearing - 90)
        x, y = cx + R * dist * math.cos(a), cy + R * dist * math.sin(a)
        begin = f"{5 * bearing / 360:.2f}s"
        col = RED if label == "???" else AMBER
        o.append(
            f'<g opacity="0"><circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="none" stroke="{col}" stroke-width="1"/>'
            f'<text x="{x+12:.1f}" y="{y+4:.1f}" fill="{col}" font-size="10" font-weight="700">{label}</text>'
            f'<animate attributeName="opacity" values="0;1;0.15;0" keyTimes="0;0.03;0.7;1" dur="5s" begin="{begin}" repeatCount="indefinite"/></g>'
        )
    o.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{AMBER}"/>')

    # right column
    X = 392
    o.append(f'<text x="{X}" y="62" fill="{AMBER}" font-size="12" letter-spacing="3">◢ GROUND CONTROL · GS-13</text>')
    o.append(f'<g clip-path="url(#nameclip)">')
    o.append(f'<text x="{X-4}" y="138" fill="{INK}" font-size="66" font-weight="800" letter-spacing="2">GURNOOR</text>')
    o.append(f'<text x="{X-4}" y="208" fill="none" stroke="{AMBER}" stroke-width="1.6" font-size="66" font-weight="800" letter-spacing="2">SINGH</text>')
    o.append("</g>")
    o.append(f'<rect x="{X+232}" y="168" width="22" height="40" fill="{AMBER}">{blink("1s")}</rect>')
    o.append(f'<text x="{X}" y="244" fill="{GREY}" font-size="13" letter-spacing="1">AI &amp; ROBOTICS ENGINEER · RESEARCHER · EDUCATOR</text>')
    o.append(f'<line x1="{X}" y1="264" x2="{W-40}" y2="264" stroke="{AMBER_DIM}" stroke-dasharray="2 4"/>')

    rows = [
        [("LAT", "31.634°N"), ("LON", "74.872°E")],
        [("BASE", "GNDU · AMRITSAR"), ("ORBIT", "YEAR 03")],
        [("NOW", "IIT ROPAR LAB"), ("LINK", None)],
    ]
    for i, row in enumerate(rows):
        y = 292 + i * 26
        for j, (k, v) in enumerate(row):
            x = X + j * 220
            o.append(f'<text x="{x}" y="{y}" fill="{GREY_DIM}" font-size="11" letter-spacing="1">{k}</text>')
            if v is None:
                o.append(f'<circle cx="{x+58}" cy="{y-4}" r="4" fill="{GREEN}">{blink("1.6s")}</circle>')
                o.append(f'<text x="{x+68}" y="{y}" fill="{GREEN}" font-size="12" font-weight="700">ONLINE</text>')
            else:
                o.append(f'<text x="{x+52}" y="{y}" fill="{INK}" font-size="12" font-weight="700">{v}</text>')
    o.append(f'<text x="{X}" y="370" fill="{GREY_DIM}" font-size="11" letter-spacing="1">PAYLOAD</text>')
    o.append(f'<rect x="{X+66}" y="358" width="142" height="16" fill="{RED}" opacity="0.15"/>')
    o.append(f'<text x="{X+74}" y="370" fill="{RED}" font-size="12" font-weight="700" letter-spacing="2">[ CLASSIFIED ]<animate attributeName="opacity" values="1;0.35;1" dur="2.4s" repeatCount="indefinite"/></text>')

    # top status strip
    o.append(f'<circle cx="34" cy="30" r="4" fill="{RED}">{blink("1.4s")}</circle>')
    o.append(f'<text x="44" y="34" fill="{GREY}" font-size="10" letter-spacing="2">REC</text>')
    o.append(f'<text x="{W-34}" y="34" fill="{GREY_DIM}" font-size="10" letter-spacing="2" text-anchor="end">SYS.BOOT OK · ALL SUBSYSTEMS NOMINAL</text>')

    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#scan)"/>')
    o.append(brackets(W, H))
    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────────── SUBSYSTEMS ─────────────────────────────
def subsystems():
    W, H = 840, 268
    pw, gap = 195, 20
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">', f"<defs>{defs_common()}</defs>"]
    panels = [
        ("SYS-01", "APPLIED AI", ["ML · DL · NLP · RAG", "YOLO · OpenCV · MediaPipe"]),
        ("SYS-02", "AUTONOMY", ["ROS 2 · Gazebo sim", "QGroundControl · trials"]),
        ("SYS-03", "VEHICLE FIRMWARE", ["ArduCopter → ArduSub", "AHRS · Pixhawk · C/C++"]),
        ("SYS-04", "INSTRUCTION", ["AI instructor × 2 roles", "School + industry cohorts"]),
    ]
    for i, (code, name, lines) in enumerate(panels):
        x0 = i * (pw + gap)
        o.append(f'<g transform="translate({x0},0)">')
        o.append(f'<rect x="0.5" y="0.5" width="{pw-1}" height="{H-1}" rx="10" fill="{BG}" stroke="{AMBER_DIM}"/>')
        o.append(f'<rect x="0.5" y="0.5" width="{pw-1}" height="{H-1}" rx="10" fill="url(#grid)" opacity="0.6"/>')
        o.append(f'<text x="14" y="26" fill="{GREY_DIM}" font-size="10" letter-spacing="2">{code}</text>')
        o.append(f'<circle cx="{pw-70}" cy="22" r="3.5" fill="{GREEN}"><animate attributeName="opacity" values="1;0.3;1" dur="{1.6+i*0.3:.1f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<text x="{pw-14}" y="26" fill="{GREEN}" font-size="9" letter-spacing="1" text-anchor="end">NOMINAL</text>')
        o.append(f'<text x="14" y="50" fill="{INK}" font-size="14" font-weight="800" letter-spacing="1">{name}</text>')
        o.append(f'<line x1="14" y1="62" x2="{pw-14}" y2="62" stroke="{AMBER_DIM}" stroke-dasharray="2 3"/>')
        # viz area: y 72..196
        vx, vy, vw, vh = 14, 74, pw - 28, 118
        o.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="none" stroke="{AMBER_FAINT}"/>')
        o.append(VIZ[i](vx, vy, vw, vh))
        for k, line in enumerate(lines):
            o.append(f'<text x="14" y="{220+k*18}" fill="{GREY if k else INK}" font-size="11">{line}</text>')
        o.append("</g>")
    o.append("</svg>")
    return "\n".join(o)


def viz_perception(x, y, w, h):
    o = []
    # faint "scene" — horizon + shapes
    o.append(f'<path d="M{x} {y+h*0.68}H{x+w}" stroke="{AMBER_FAINT}"/>')
    o.append(f'<path d="M{x+22} {y+h-14}l18 -34l18 34z" fill="none" stroke="{AMBER_DIM}"/>')
    o.append(f'<rect x="{x+w-58}" y="{y+h-46}" width="34" height="32" fill="none" stroke="{AMBER_DIM}"/>')
    o.append(f'<circle cx="{x+w/2}" cy="{y+40}" r="13" fill="none" stroke="{AMBER_DIM}"/>')
    # detection box that hops between objects
    boxes = [(x + 14, y + h - 54, 52, 46, "cone 0.94"), (x + w / 2 - 20, y + 20, 40, 40, "uav 0.97"), (x + w - 66, y + h - 54, 50, 46, "box 0.91")]
    n = len(boxes)
    xs = ";".join(f"{b[0]:.0f}" for b in boxes + [boxes[0]])
    ys = ";".join(f"{b[1]:.0f}" for b in boxes + [boxes[0]])
    ws = ";".join(f"{b[2]:.0f}" for b in boxes + [boxes[0]])
    hs = ";".join(f"{b[3]:.0f}" for b in boxes + [boxes[0]])
    kt = ";".join(f"{k/n:.3f}" for k in range(n + 1))
    anim = lambda a, v: f'<animate attributeName="{a}" values="{v}" keyTimes="{kt}" dur="4.5s" repeatCount="indefinite" calcMode="spline" keySplines="{";".join(["0.6 0 0.2 1"]*n)}"/>'
    o.append(f'<rect fill="{AMBER}" fill-opacity="0.08" stroke="{AMBER}" stroke-width="1.5">{anim("x",xs)}{anim("y",ys)}{anim("width",ws)}{anim("height",hs)}</rect>')
    for k, b in enumerate(boxes):
        o.append(
            f'<text x="{b[0]:.0f}" y="{b[1]-4:.0f}" fill="{AMBER}" font-size="9" font-weight="700" opacity="0">{b[4]}'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{(k/n)+0.06:.3f};{(k/n)+0.09:.3f};{((k+1)/n)-0.05:.3f};{((k+1)/n)-0.02:.3f};1" dur="4.5s" repeatCount="indefinite"/></text>'
        )
    # scan line
    o.append(f'<line x1="{x}" x2="{x+w}" stroke="{AMBER}" stroke-opacity="0.35"><animate attributeName="y1" values="{y};{y+h};{y}" dur="3s" repeatCount="indefinite"/><animate attributeName="y2" values="{y};{y+h};{y}" dur="3s" repeatCount="indefinite"/></line>')
    return "".join(o)


def viz_autonomy(x, y, w, h):
    o = []
    cols, rows = 9, 6
    cw, ch = w / cols, h / rows
    rng = random.Random(7)
    blocked = {(2, 1), (2, 2), (2, 3), (5, 2), (5, 3), (5, 4), (5, 5), (7, 0), (7, 1)}
    for c in range(cols):
        for r in range(rows):
            if (c, r) in blocked:
                o.append(f'<rect x="{x+c*cw+2:.1f}" y="{y+r*ch+2:.1f}" width="{cw-4:.1f}" height="{ch-4:.1f}" fill="{AMBER_DIM}" opacity="0.7"/>')
            else:
                o.append(f'<circle cx="{x+c*cw+cw/2:.1f}" cy="{y+r*ch+ch/2:.1f}" r="1" fill="{AMBER_DIM}"/>')
    path_cells = [(0, 5), (1, 5), (1, 4), (2, 4), (3, 4), (3, 3), (3, 2), (4, 2), (4, 1), (5, 1), (6, 1), (6, 2), (7, 2), (8, 2), (8, 1), (8, 0)]
    pts = [(x + c * cw + cw / 2, y + r * ch + ch / 2) for c, r in path_cells]
    d = "M" + "L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    o.append(f'<path id="plan" d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.5" stroke-dasharray="3 3" opacity="0.7"/>')
    o.append(f'<circle cx="{pts[0][0]:.1f}" cy="{pts[0][1]:.1f}" r="4" fill="none" stroke="{GREEN}"/>')
    o.append(f'<path d="M{pts[-1][0]-5:.1f} {pts[-1][1]-5:.1f}l10 10m0 -10l-10 10" stroke="{RED}" stroke-width="1.5"/>')
    o.append(f'<g><circle r="4.5" fill="{AMBER}"/><circle r="9" fill="none" stroke="{AMBER}" stroke-opacity="0.4"/><animateMotion dur="5s" repeatCount="indefinite" path="{d}" rotate="auto"/></g>')
    return "".join(o)


def viz_firmware(x, y, w, h):
    o = []
    mid = y + h / 2
    o.append(f'<path d="M{x} {mid}H{x+w}" stroke="{AMBER_FAINT}"/>')
    for k in range(1, 4):
        o.append(f'<path d="M{x+k*w/4:.1f} {y}V{y+h}" stroke="{AMBER_FAINT}"/>')
    # setpoint step + damped response, repeated twice for seamless scroll
    def trace(ox):
        seg = []
        period = w
        for s in range(0, 101):
            t = s / 100
            px = ox + t * period
            if t < 0.15:
                v = 0
            elif t < 0.6:
                tt = (t - 0.15) * 22
                v = 1 - math.exp(-0.55 * tt) * math.cos(1.9 * tt)
            else:
                tt = (t - 0.6) * 22
                v = math.exp(-0.55 * tt) * math.cos(1.9 * tt)
            py = mid + 22 - v * 44
            seg.append(f"{px:.1f} {py:.1f}")
        return seg

    pts = trace(x) + trace(x + w)
    d = "M" + "L".join(pts)
    sp = f"M{x} {mid+22}H{x+0.15*w:.1f}V{mid-22}H{x+0.6*w:.1f}V{mid+22}H{x+1.15*w:.1f}V{mid-22}H{x+1.6*w:.1f}V{mid+22}H{x+2*w:.1f}"
    o.append(f'<clipPath id="fwclip"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
    o.append(f'<g clip-path="url(#fwclip)"><g>')
    o.append(f'<path d="{sp}" fill="none" stroke="{GREY_DIM}" stroke-width="1" stroke-dasharray="3 3"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.8"/>')
    o.append(f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-w} 0" dur="4s" repeatCount="indefinite"/></g></g>')
    o.append(f'<text x="{x+4}" y="{y+12}" fill="{GREY_DIM}" font-size="8">ATT.PITCH</text>')
    o.append(f'<text x="{x+w-4}" y="{y+12}" fill="{AMBER}" font-size="8" text-anchor="end">400 Hz</text>')
    return "".join(o)


def viz_crew(x, y, w, h):
    o = []
    cols, rows = 14, 8  # 112 nodes → "100+"
    sx, sy = w / cols, (h - 22) / rows
    rng = random.Random(3)
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            cx_, cy_ = x + c * sx + sx / 2, y + r * sy + sy / 2 + 2
            begin = f"{idx*0.035:.2f}s"
            o.append(
                f'<circle cx="{cx_:.1f}" cy="{cy_:.1f}" r="2.6" fill="{AMBER_DIM}">'
                f'<animate attributeName="fill" values="{AMBER_DIM};{AMBER};{AMBER}" keyTimes="0;0.1;1" dur="0.6s" begin="{begin}" fill="freeze"/>'
                f'<animate attributeName="r" values="2.6;4;2.6" dur="0.6s" begin="{begin}" fill="freeze"/></circle>'
            )
    o.append(f'<text x="{x+w-4}" y="{y+h-6}" fill="{AMBER}" font-size="11" font-weight="800" text-anchor="end">100+</text>')
    o.append(f'<text x="{x+4}" y="{y+h-6}" fill="{GREY_DIM}" font-size="8">LEARNERS MENTORED</text>')
    return "".join(o)


VIZ = [viz_perception, viz_autonomy, viz_firmware, viz_crew]


# ───────────────────────────── FLIGHT LOG ─────────────────────────────
def flightlog():
    W, H = 840, 360
    base = 182
    xs = [86 + i * 111 for i in range(7)]
    ys = [base - 18, base + 18, base - 10, base + 20, base - 20, base + 12, base - 6]
    wps = [
        ("WP-01 · 2022", "SCHOOL RANK 1", ["ICSE · 1st among boys", "Head Boy · council lead"]),
        ("WP-02 · 2024", "GNDU AMRITSAR", ["Int. B.Tech + M.Tech", "AI &amp; Robotics"]),
        ("WP-03 · DEC 24", "IIT MANDI · CAIR", ["ArduCopter → ArduSub", "Submarine field trials", "First first-year intern"]),
        ("WP-04 · JUN 25", "IIIT ALLAHABAD", ["AI &amp; Robotics trainee", "Letter of Excellence"]),
        ("WP-05 · MAY 26", "IIT ROPAR", ["Vicharnshala Lab", "Research intern"]),
        ("WP-06 · 2026", "AI INSTRUCTOR", ["Synaptix Technologies", "Ram Ashram Public Sch."]),
        ("WP-07", "NEXT", ["[ REDACTED ]", "eta: one by one"]),
    ]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">', f"<defs>{defs_common()}</defs>"]
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity="0.7"/>')
    o.append(f'<text x="28" y="34" fill="{AMBER}" font-size="11" letter-spacing="3">◢ FLIGHT LOG · MISSION TRAJECTORY</text>')
    o.append(f'<text x="{W-28}" y="34" fill="{GREY_DIM}" font-size="10" letter-spacing="2" text-anchor="end">WAYPOINTS 07 · 2022 → NOW</text>')

    # smooth path through waypoints (Catmull-Rom → Bezier)
    P = [(xs[0] - 60, ys[0] + 8)] + list(zip(xs, ys)) + [(xs[-1] + 60, ys[-1])]
    def seg(i):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        return f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    done = f"M{P[1][0]} {P[1][1]}" + "".join(seg(i) for i in range(1, 6))
    nxt = f"M{P[6][0]} {P[6][1]}" + seg(6)
    full = done + "".join(seg(i) for i in (6,))
    o.append(f'<path d="{done}" fill="none" stroke="{AMBER}" stroke-opacity="0.18" stroke-width="10"/>')
    o.append(f'<path d="{done}" fill="none" stroke="{AMBER}" stroke-width="2"/>')
    o.append(f'<path d="{nxt}" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="5 5"><animate attributeName="stroke-dashoffset" from="20" to="0" dur="1s" repeatCount="indefinite"/></path>')

    # labels
    for i, ((code, title, lines), x, y) in enumerate(zip(wps, xs, ys)):
        up = i % 2 == 0
        last = i == 6
        col = RED if last else AMBER
        anchor = "middle"
        if up:
            ty = 72
            o.append(f'<line x1="{x}" y1="{ty + 14 + 15*len(lines)}" x2="{x}" y2="{y-12}" stroke="{AMBER_DIM}" stroke-dasharray="2 3"/>')
        else:
            ty = 248
            o.append(f'<line x1="{x}" y1="{y+12}" x2="{x}" y2="{ty-14}" stroke="{AMBER_DIM}" stroke-dasharray="2 3"/>')
        o.append(f'<text x="{x}" y="{ty-1}" fill="{col}" font-size="9" letter-spacing="2" text-anchor="{anchor}">{code}</text>')
        o.append(f'<text x="{x}" y="{ty+15}" fill="{RED if last else INK}" font-size="12" font-weight="800" text-anchor="{anchor}">{title}</text>')
        for k, line in enumerate(lines):
            fill = RED if (last and k == 0) else GREY
            extra = '<animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/>' if last and k == 0 else ""
            o.append(f'<text x="{x}" y="{ty+31+k*14}" fill="{fill}" font-size="10" text-anchor="{anchor}" font-weight="{700 if last and k==0 else 400}">{line}{extra}</text>')
        # marker
        if last:
            o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BG}" stroke="{RED}" stroke-width="2"/>')
            o.append(f'<circle cx="{x}" cy="{y}" r="7" fill="none" stroke="{RED}"><animate attributeName="r" values="7;20" dur="1.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="1.6s" repeatCount="indefinite"/></circle>')
        else:
            o.append(f'<rect x="{x-6}" y="{y-6}" width="12" height="12" transform="rotate(45 {x} {y})" fill="{BG}" stroke="{AMBER}" stroke-width="2"/>')
            o.append(f'<rect x="{x-2.5}" y="{y-2.5}" width="5" height="5" transform="rotate(45 {x} {y})" fill="{AMBER}"/>')

    # drone flying the route
    drone = (
        f'<g><path d="M-9 -9L9 9M9 -9L-9 9" stroke="{INK}" stroke-width="2"/>'
        + "".join(f'<circle cx="{a}" cy="{b}" r="4" fill="none" stroke="{AMBER}" stroke-width="1.5"/>' for a, b in ((-9, -9), (9, -9), (-9, 9), (9, 9)))
        + f'<rect x="-3" y="-3" width="6" height="6" fill="{AMBER}"/>'
        + f'<animateMotion dur="11s" repeatCount="indefinite" rotate="auto" path="{full}"/>'
        + "</g>"
    )
    o.append(drone)
    o.append(f'<text x="28" y="{H-20}" fill="{GREY_DIM}" font-size="9" letter-spacing="2">◇ LOGGED  ○ PENDING  — ACTUAL  - - PLANNED</text>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#scan)" opacity="0.6"/>')
    o.append(brackets(W, H, color=AMBER_DIM))
    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────────── RESEARCH ─────────────────────────────
def research():
    W, H = 840, 300
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">', f"<defs>{defs_common()}"]
    o.append(f'<radialGradient id="core" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="{INK}" stop-opacity="0.9"/><stop offset="0.25" stop-color="{AMBER}" stop-opacity="0.45"/><stop offset="1" stop-color="{AMBER}" stop-opacity="0"/></radialGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity="0.6"/>')
    # galaxy viewport
    gx, gy = 150, 150
    o.append(f'<rect x="24" y="24" width="252" height="252" fill="none" stroke="{AMBER_FAINT}"/>')
    o.append(f'<text x="32" y="40" fill="{GREY_DIM}" font-size="8" letter-spacing="1">FIELD-07 · r-BAND</text>')
    rng = random.Random(11)
    for _ in range(40):
        o.append(f'<circle cx="{rng.uniform(30,270):.1f}" cy="{rng.uniform(46,270):.1f}" r="{rng.choice([0.6,0.8,1.1])}" fill="{GREY}" opacity="{rng.uniform(0.3,0.8):.2f}"/>')
    arms = []
    for arm in range(2):
        for k in range(150):
            t = k / 150
            ang = arm * math.pi + t * 3.6 * math.pi / 1.3
            rad = 6 + t * 88
            jitter = rng.gauss(0, 3 + 6 * t)
            px = rad * math.cos(ang) + jitter
            py = (rad * math.sin(ang) + rng.gauss(0, 3 + 6 * t)) * 0.62
            arms.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{rng.choice([0.7,1,1.3])}" fill="{AMBER}" opacity="{max(0.15, 0.9 - t*0.7):.2f}"/>')
    o.append(f'<g transform="translate({gx},{gy}) rotate(-24)"><ellipse rx="34" ry="22" fill="url(#core)"/><g>{"".join(arms)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="120s" repeatCount="indefinite"/></g></g>')
    # photometry apertures
    for r_, dash, col in ((26, "", AMBER), (52, "3 3", AMBER_DIM), (66, "3 3", AMBER_DIM)):
        o.append(f'<circle cx="{gx}" cy="{gy}" r="{r_}" fill="none" stroke="{col}" stroke-dasharray="{dash}"/>')
    o.append(f'<circle cx="{gx}" cy="{gy}" r="26" fill="none" stroke="{AMBER}" stroke-width="1.5"><animate attributeName="r" values="22;30;22" dur="3s" repeatCount="indefinite"/></circle>')
    o.append(f'<text x="{gx+70}" y="{gy-56}" fill="{AMBER}" font-size="9">m = 16.42</text>')
    o.append(f'<text x="268" y="268" fill="{GREY_DIM}" font-size="8" text-anchor="end">APERTURE PHOTOMETRY</text>')
    # text column
    X = 312
    o.append(f'<text x="{X}" y="44" fill="{AMBER}" font-size="11" letter-spacing="3">◢ PRIMARY PAYLOAD · LEAD RESEARCHER</text>')
    for k, line in enumerate(["Artificial Intelligence for Astronomy:", "Enhancing Instrument Reliability", "and Galaxy Photometry"]):
        o.append(f'<text x="{X}" y="{78+k*24}" fill="{INK}" font-size="17" font-weight="800">{line}</text>')
    o.append(f'<rect x="{X}" y="138" width="186" height="22" rx="3" fill="{AMBER}" fill-opacity="0.12" stroke="{AMBER}"/>')
    o.append(f'<circle cx="{X+13}" cy="149" r="4" fill="{AMBER}">{blink("1.4s")}</circle>')
    o.append(f'<text x="{X+24}" y="153" fill="{AMBER}" font-size="11" font-weight="800" letter-spacing="2">UNDER PEER REVIEW</text>')
    o.append(f'<text x="{X+198}" y="153" fill="{GREY}" font-size="11">target · high-impact journal</text>')
    o.append(f'<line x1="{X}" y1="182" x2="{W-28}" y2="182" stroke="{AMBER_DIM}" stroke-dasharray="2 4"/>')
    rows = [
        ("SELECTED", "Journey of Yeast: From Leavening Bread to Gene Cloning", "Teach for Science · Prayas GNDU &amp; INYAS, IIT Hyderabad"),
        ("DRAFTING", "Review articles in AI &amp; robotics applications", "Autonomous systems · machine learning · robotics"),
    ]
    for k, (tag, title, sub) in enumerate(rows):
        y = 210 + k * 44
        o.append(f'<text x="{X}" y="{y}" fill="{GREEN if k==0 else GREY_DIM}" font-size="9" letter-spacing="2" font-weight="700">{tag}</text>')
        o.append(f'<text x="{X+80}" y="{y}" fill="{INK}" font-size="12" font-weight="700">{title}</text>')
        o.append(f'<text x="{X+80}" y="{y+17}" fill="{GREY}" font-size="10">{sub}</text>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#scan)" opacity="0.6"/>')
    o.append(brackets(W, H, color=AMBER_DIM))
    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────────── DIVIDER + FOOTER ─────────────────────────────
def section(num, title, sub):
    W, H = 840, 56
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">']
    o.append(f'<text x="0" y="34" fill="{AMBER}" font-size="13" font-weight="700" letter-spacing="2">{num}</text>')
    o.append(f'<text x="38" y="34" fill="{INK}" font-size="20" font-weight="800" letter-spacing="3">{title}</text>')
    tw = 38 + len(title.replace("&amp;","&")) * 15.0
    o.append(f'<line x1="{tw+14:.0f}" y1="29" x2="{W - len(sub)*8.6 - 34:.0f}" y2="29" stroke="{AMBER_DIM}" stroke-dasharray="2 4"/>')
    o.append(f'<text x="{W}" y="33" fill="{GREY_DIM}" font-size="10" letter-spacing="2" text-anchor="end">{sub}</text>')
    o.append(f'<rect x="{W - len(sub)*8.6 - 20:.0f}" y="25" width="8" height="8" fill="{AMBER}">{blink("1.4s")}</rect>')
    o.append("</svg>")
    return "\n".join(o)


def footer():
    W, H = 840, 170
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}">', f"<defs>{defs_common()}"]
    o.append(f'<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="1"/><stop offset="0.15" stop-color="{BG}" stop-opacity="0"/><stop offset="0.85" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity="1"/></linearGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity="0.6"/>')
    mid = 62
    pts = []
    for s in range(0, 841 * 2, 4):
        t = s / 840
        v = math.sin(t * math.pi * 2 * 6) * (0.4 + 0.6 * abs(math.sin(t * math.pi * 2)))
        v += 0.25 * math.sin(t * math.pi * 2 * 23)
        pts.append(f"{s:.0f} {mid - v*26:.1f}")
    d = "M" + "L".join(pts)
    o.append(f'<g><path d="{d}" fill="none" stroke="{AMBER}" stroke-width="1.6"/><path d="{d}" fill="none" stroke="{AMBER}" stroke-opacity="0.15" stroke-width="7"/><animateTransform attributeName="transform" type="translate" from="0 0" to="-840 0" dur="7s" repeatCount="indefinite"/></g>')
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="url(#fade)"/>')
    o.append(f'<text x="{W/2}" y="122" fill="{INK}" font-size="13" font-weight="800" letter-spacing="5" text-anchor="middle">PASSIONATE · HARDWORKING · FULL OF GRATITUDE</text>')
    o.append(f'<text x="{W/2}" y="146" fill="{GREY_DIM}" font-size="10" letter-spacing="4" text-anchor="middle">— END OF TRANSMISSION · GS-13 STANDING BY —</text>')
    o.append(brackets(W, H, color=AMBER_DIM))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = {
        "header.svg": header(),
        "subsystems.svg": subsystems(),
        "flight-log.svg": flightlog(),
        "footer.svg": footer(),
        "sec-01.svg": section("01", "MISSION BRIEF", "WHO IS FLYING"),
        "sec-02.svg": section("02", "SUBSYSTEMS", "WHAT I BUILD"),
        "sec-03.svg": section("03", "FLIGHT LOG", "WHERE I'VE BEEN"),
        "sec-04.svg": section("04", "ONBOARD SYSTEMS", "TOOLS I FLY WITH"),
        "sec-05.svg": section("05", "COMMAND &amp; HONORS", "LEADERSHIP · AWARDS"),
        "sec-06.svg": section("06", "TELEMETRY", "LIVE FROM GITHUB"),
        "sec-07.svg": section("07", "OPEN CHANNELS", "ESTABLISH CONTACT"),
    }
    for name, svg in out.items():
        with open(f"assets/{name}", "w") as f:
            f.write(svg)
    print("wrote", len(out), "files")
