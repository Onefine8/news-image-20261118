#!/usr/bin/env python3
"""Render the front page for 18 November 2026: one image, 45 stories.

Builds entry.png (1024x1024) from sheet.webp, a 4x4 contact sheet of the
13 original editorial illustrations drawn for this page. Run:
    python3 render.py            # writes entry.png beside this file
The sheet lives beside this file too, so the page rebuilds anywhere.
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (247, 243, 232)
INK = (25, 25, 25)
MUTED = (107, 98, 87)
RED = (179, 35, 27)
RULE = (25, 25, 25)
SLATE = (58, 74, 90)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"

REGION_COLORS = {
    "Europe": (47, 93, 138),
    "Middle East": (179, 35, 27),
    "Asia": (217, 138, 31),
    "Africa": (90, 125, 58),
    "Americas": (106, 74, 138),
    "Oceania": (42, 138, 138),
    "World": (119, 119, 119),
}
FIELD_COLORS = {
    "War & security": (179, 35, 27),
    "Politics & diplomacy": (47, 93, 138),
    "Economy & labour": (217, 138, 31),
    "Society & culture": (106, 74, 138),
    "Health": (194, 90, 138),
    "Disasters & weather": (42, 138, 138),
    "Tech & science": (85, 85, 85),
    "Climate & space": (90, 125, 58),
}

# (number, sheet cell, kicker, headline, deck, region, field, map pin lon/lat)
LEADS = [
    (1, 0, "MIDDLE EAST \u00b7 WAR & SECURITY",
     "Iran fires drones at US bases in the Gulf",
     "Kuwait and Bahrain say they shot down the drones before dawn, hours "
     "after US jets struck a missile site on Qeshm Island.",
     "Middle East", "War & security", (48.0, 29.5)),
    (2, 1, "ASIA \u00b7 POLITICS & DIPLOMACY",
     "Xi greets Trump as APEC opens in Shenzhen",
     "Xi and Putin meet ahead of Thursday\u2019s three-way summit, as Xi "
     "vows to resist trade protectionism.",
     "Asia", "Politics & diplomacy", (114.0, 22.5)),
    (3, 2, "WORLD \u00b7 CLIMATE & SPACE",
     "COP31 splits over fossil-fuel phase-out",
     "Draft calls for a faster phase-out and $120bn a year in adaptation "
     "finance; the EU envoy warns it could make the talks \u2018untenable\u2019.",
     "World", "Climate & space", (30.7, 36.9)),
]

# (number, sheet cell, headline, deck, region, field, map pin lon/lat or None)
SMALL = [
    (4, 3, "Voyager 1, one light-day from Earth",
     "NASA\u2019s 1977 probe passes 25.9bn km.",
     "World", "Climate & space", None),
    (5, 4, "Russia fires 141 drones at Ukraine",
     "126 downed; at least 5 killed.",
     "Europe", "War & security", (30.5, 50.4)),
    (6, 5, "Wage protests shut 535 garment factories",
     "Workers want Tk30,000 a month.",
     "Asia", "Economy & labour", (90.4, 23.8)),
    (7, 6, "GTA VI goes on sale at midnight",
     "New Zealand first; ~17m pre-orders.",
     "Americas", "Society & culture", (174.8, -36.8)),
    (8, 7, "Democrats pick Jeffries for Speaker",
     "Caucus votes 251\u201311.",
     "Americas", "Politics & diplomacy", (-77.0, 38.9)),
    (9, 8, "Ethiopia and Eritrea mass troops on border",
     "Armies within striking distance.",
     "Africa", "War & security", (37.8, 14.7)),
    (10, 9, "Cyclone Akvan bears down on India",
     "Red alert; landfall expected Friday.",
     "Asia", "Disasters & weather", (82.0, 16.0)),
    (11, 10, "Gaza truce may collapse, Board of Peace warns",
     "Report faults Israel and Hamas.",
     "Middle East", "War & security", (34.5, 31.5)),
    (12, 11, "Ebola passes 11,000 cases in DR Congo",
     "Second-largest outbreak on record.",
     "Africa", "Health", (25.0, -2.0)),
    (13, 12, "US loses measles-free status after 26 years",
     "5,412 cases in 2026; 10 deaths.",
     "Americas", "Health", (-98.0, 39.5)),
]

# (place, text, region, field)
BRIEFS = [
    ("Riyadh", "Saudi-led coalition downs Houthi cruise missile.",
     "Middle East", "War & security"),
    ("Knesset", "approves nine deputy speakers, two of them Arab.",
     "Middle East", "Politics & diplomacy"),
    ("Berlin", "coalition to cut power tax and cap fuel prices.",
     "Europe", "Economy & labour"),
    ("Germany", "accuses Russia of chemical-weapons breaches.",
     "Europe", "War & security"),
    ("Cambridge", "\u2018human\u2019 named word of the year.",
     "Europe", "Society & culture"),
    ("Shenzhen", "Xi and Lee conclude FTA services talks.",
     "Asia", "Economy & labour"),
    ("Manila", "Trump claims a trade deal; Manila says none signed.",
     "Asia", "Politics & diplomacy"),
    ("Tokyo", "Japan posts sixth straight monthly trade deficit.",
     "Asia", "Economy & labour"),
    ("London", "UK inflation rises to 3.6%, highest in a year.",
     "Europe", "Economy & labour"),
    ("Brussels", "EU proposes a \u20ac45bn loan for Ukraine in 2027.",
     "Europe", "Economy & labour"),
    ("Gold", "sinks below $3,800 an ounce, lowest in over a year.",
     "World", "Economy & labour"),
    ("Canberra", "Australia sanctions settler leader Daniella Weiss.",
     "Middle East", "Politics & diplomacy"),
    ("El Obeid", "Amnesty: RSF drones killed 37 civilians.",
     "Africa", "War & security"),
    ("Quad", "leaders meet in Manila, first time in two years.",
     "Asia", "Politics & diplomacy"),
    ("Caracas", "US and Venezuela sign a military pact.",
     "Americas", "War & security"),
    ("Sudan", "2,230 civilians killed this year, UN says.",
     "Africa", "War & security"),
    ("Naypyidaw", "Myanmar to review its ties with ASEAN.",
     "Asia", "Politics & diplomacy"),
    ("Stockholm", "Europe off track on antibiotic resistance, ECDC warns.",
     "Europe", "Health"),
    ("Lahore", "world\u2019s most polluted big city again, AQI 339.",
     "Asia", "Disasters & weather"),
    ("Oil", "Brent crude slips to about $92 a barrel.",
     "World", "Economy & labour"),
    ("Tencent", "revenue up 8%, below forecasts.",
     "Asia", "Economy & labour"),
    ("Cook Islands", "Cyclone Xavier reaches Category 5.",
     "Oceania", "Disasters & weather"),
    ("Wellington", "tsunami advisory lifted after 60cm surges.",
     "Oceania", "Disasters & weather"),
    ("Sydney", "Tame Impala sweeps the ARIA Awards.",
     "Oceania", "Society & culture"),
    ("Ottawa", "Carney says China trade no worry for Trump.",
     "Americas", "Politics & diplomacy"),
    ("Lima", "M5.9 quake off south coast, no damage reported.",
     "Americas", "Disasters & weather"),
    ("Cincinnati", "USA beat Haiti 2\u20130, into Nations League semis.",
     "Americas", "Society & culture"),
    ("Monterrey", "Mexico edge Jamaica, semi vs USA.",
     "Americas", "Society & culture"),
    ("Los Angeles", "Grimes scores 47 as Lakers win ninth straight.",
     "Americas", "Society & culture"),
    ("Buenos Aires", "deputies debate Malvinas sovereignty bill.",
     "Americas", "Politics & diplomacy"),
    ("Washington", "NSA confirms outage on classified network.",
     "Americas", "Tech & science"),
    ("Pretoria", "South Africa inflation jumps to 5.2%.",
     "Africa", "Economy & labour"),
]

NUMBERS = [
    ("141", "drones at Ukraine"),
    ("535", "factories shut"),
    ("25.9bn km", "to Voyager 1"),
    ("17.0m", "GTA VI pre-orders"),
    ("5,412", "measles cases"),
]

DATE_CHECK = (
    "Left out on purpose \u2014 first reported Tue 17 Nov: Peltola\u2019s Alaska "
    "Senate win; Nvidia\u2019s $115.8bn quarter; the Kerch Bridge span "
    "collapse; the Prague train crash; Mongolia\u2019s president resigning; "
    "the Knesset speaker vote. Cyclone Akvan formed 16 Nov \u2014 today is "
    "its approach. The Qeshm strike (Tue night) appears only as the cause "
    "of today\u2019s drones."
)

FOOTER = (
    "Every story here happened, or was first reported, on Wednesday, "
    "18 November 2026. Contested claims are attributed. Sources: Reuters, "
    "AP, AFP, BBC, Al Jazeera, Bloomberg, NASA, WHO, ONS. Original illustrations."
)

# World map as a 96 x 24 dotted grid, equirectangular, lon -180..180,
# lat 78..-56. Each row lists the land intervals (first, last) in columns.
# Drawn from the continents' rough outlines.
MAP_LAND = [
    [(23, 26), (36, 39)],
    [(6, 12), (18, 31), (35, 41), (66, 92)],
    [(6, 14), (17, 34), (37, 39), (42, 43), (50, 56), (57, 93)],
    [(9, 16), (21, 38), (46, 47), (52, 55), (59, 90)],
    [(23, 39), (46, 60), (62, 86)],
    [(14, 37), (47, 61), (62, 89)],
    [(13, 38), (47, 59), (59, 66), (68, 86)],
    [(14, 36), (48, 57), (59, 68), (70, 84)],
    [(15, 33), (44, 57), (59, 68), (70, 84)],
    [(18, 24), (43, 60), (61, 65), (69, 73), (74, 82)],
    [(20, 25), (43, 59), (62, 64), (69, 72), (76, 82)],
    [(24, 27), (44, 48), (50, 61), (76, 84)],
    [(29, 34), (45, 48), (51, 61), (77, 86), (87, 90)],
    [(30, 37), (50, 59), (81, 87), (88, 91)],
    [(31, 37), (51, 57)],
    [(31, 36), (52, 56)],
    [(32, 36), (52, 55), (58, 59)],
    [(32, 34), (52, 55), (80, 89)],
    [(32, 34), (53, 55), (80, 89)],
    [(31, 33), (82, 87)],
    [(30, 32), (83, 86), (93, 94)],
    [(30, 30), (93, 94)],
    [],
    [],
]


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit in width px."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def crop_to(image, tw, th):
    """Centre-crop to the target aspect, then resize to tw x th."""
    sw, sh = image.size
    target = tw / th
    src = sw / sh
    if src > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        box = (x0, 0, x0 + nw, sh)
    else:
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        box = (0, y0, sw, y0 + nh)
    return image.crop(box).resize((tw, th), Image.LANCZOS)


def sheet_cell(sheet, idx):
    """Cell idx of the 4x4 sheet (480x320 cells)."""
    return sheet.crop(((idx % 4) * 480, (idx // 4) * 320,
                       (idx % 4 + 1) * 480, (idx // 4 + 1) * 320))


def badge(draw, x, y, num, size=17):
    """Red disc with a white story number, top-left of a picture."""
    r = size // 2
    draw.ellipse((x, y, x + size, y + size), fill=RED)
    f = font(SANS_B, 11)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (size - tw) / 2, y + 2), t, font=f, fill=(255, 255, 255))


def count_bar(draw, x, y, width, counts, colors, order):
    """One stacked horizontal bar; returns the legend line for it."""
    total = sum(counts[k] for k in order)
    bx = x
    for k in order:
        wseg = max(0, round(width * counts[k] / total))
        if wseg:
            draw.rectangle((bx, y, bx + wseg - 1, y + 10), fill=colors[k])
        bx += wseg
    return "   ".join("%s %d" % (k, counts[k]) for k in order)


def map_point(lon, lat, mx, my, mw, mh):
    """Project lon/lat onto the map box (mx, my, mw, mh)."""
    px = mx + (lon + 180.0) / 360.0 * mw
    py = my + (78.0 - lat) / 134.0 * mh
    return px, py


def draw_map(draw, x, y, w, h):
    """Dotted continents plus numbered pins for the illustrated stories."""
    draw.rectangle((x, y, x + w, y + h), outline=RULE, width=1)
    cw, ch = w / 96.0, h / 24.0
    for r, intervals in enumerate(MAP_LAND):
        for c0, c1 in intervals:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cw
                cy = y + (r + 0.5) * ch
                draw.ellipse((cx - 1.3, cy - 1.3, cx + 1.3, cy + 1.3),
                             fill=SLATE)
    note = "4 \u2014 Voyager 1 \u2014 is 25.9bn km away, off this map."
    d_note = font(SANS, 9)
    draw.text((x + 6, y + h - 12), note, font=d_note, fill=MUTED)
    pins = [(lead[0], lead[7]) for lead in LEADS]
    pins += [(s[0], s[6]) for s in SMALL]
    pins = [(n, pin) for (n, pin) in pins if pin is not None]
    f = font(SANS_B, 8)
    # Small nudges so pins that are neighbours in reality stay readable.
    nudge = {1: (7, 5), 3: (-8, -6), 11: (-3, 8), 10: (6, 6)}
    for num, (lon, lat) in pins:
        px, py = map_point(lon, lat, x + 4, y + 4, w - 8, h - 8)
        dx, dy = nudge.get(num, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse((px - 6, py - 6, px + 6, py + 6), fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((px - tw / 2, py - 5), t, font=f, fill=(255, 255, 255))


def draw_runs(draw, x, y, runs):
    """Draw (text, font, fill) runs left to right; returns end x."""
    for text, fnt, fill in runs:
        draw.text((x, y), text, font=fnt, fill=fill)
        x += draw.textlength(text, font=fnt)
    return x


def draw_legend(draw, x, y, counts, colors, order):
    """Coloured squares + 'Label n' items in one row; returns end x."""
    f = font(SANS, 10)
    for k in order:
        draw.rectangle((x, y + 1, x + 8, y + 9), fill=colors[k])
        x += 12
        t = "%s %d" % (k, counts[k])
        draw.text((x, y), t, font=f, fill=INK)
        x += draw.textlength(t, font=f) + 16
    return x


def build(out_path):
    sheet = Image.open(os.path.join(HERE, "sheet.webp")).convert("RGB")
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle((6, 6, W - 7, H - 7), outline=INK, width=2)

    x0, x1 = 18, W - 18
    cw = x1 - x0
    y = 14

    # ---- Masthead ----
    f_kick = font(SERIF_B, 15)
    f_right = font(SANS_B, 11)
    d.text((x0, y), "THE WORLD IN ONE DAY", font=f_kick, fill=INK)
    rt = "45 STORIES \u00b7 13 PICTURES"
    d.text((x1 - d.textlength(rt, font=f_right), y + 2), rt,
           font=f_right, fill=INK)
    y += 24
    d.rectangle((x0, y, x1, y + 2), fill=RULE)
    d.rectangle((x0, y + 5, x1, y + 6), fill=RULE)
    y += 12
    f_date = font(SERIF_B, 42)
    dt = "Wednesday 18 November 2026"
    d.text(((W - d.textlength(dt, font=f_date)) / 2, y), dt,
           font=f_date, fill=INK)
    y += 52
    f_sub = font(SERIF, 13)
    st = "Every story below happened, or was first reported, on this one day."
    d.text(((W - d.textlength(st, font=f_sub)) / 2, y), st,
           font=f_sub, fill=MUTED)
    y += 22
    d.rectangle((x0, y, x1, y), fill=RULE)
    y += 7

    # ---- Counts: stacked bars by region and by field, then the numbers ----
    stories = ([(l[5], l[6]) for l in LEADS] + [(s[4], s[5]) for s in SMALL]
               + [(b[2], b[3]) for b in BRIEFS])
    rc = {k: 0 for k in REGION_COLORS}
    fc = {k: 0 for k in FIELD_COLORS}
    for region, field in stories:
        rc[region] += 1
        fc[field] += 1
    count_bar(d, x0, y, cw, rc, REGION_COLORS, list(REGION_COLORS))
    y += 15
    draw_legend(d, x0, y, rc, REGION_COLORS, list(REGION_COLORS))
    y += 16
    count_bar(d, x0, y, cw, fc, FIELD_COLORS, list(FIELD_COLORS))
    y += 15
    draw_legend(d, x0, y, fc, FIELD_COLORS, list(FIELD_COLORS))
    y += 18
    size = 10
    while True:
        f_num_l = font(SANS_B, size)
        f_num = font(SANS_B, size)
        f_txt = font(SANS, size)
        runs = [("THE DAY IN NUMBERS   ", f_num_l, RED)]
        for num, txt in NUMBERS:
            runs.append((num + " ", f_num, RED))
            runs.append((txt + "    \u00b7    ", f_txt, INK))
        runs[-1] = (runs[-1][0].rstrip("    \u00b7    "), f_txt, INK)
        total_w = sum(d.textlength(t, font=f) for t, f, _ in runs)
        if total_w <= cw or size <= 8:
            break
        size -= 1
    draw_runs(d, (W - total_w) / 2, y, runs)
    y += 15

    # ---- Leads: three big pictures ----
    y += 4
    lead_y = y
    col_w, gap = 322, 11
    f_lead_k = font(SANS_B, 10)
    f_lead_h = font(SERIF_B, 17)
    f_lead_d = font(SANS, 10)
    for i, (num, cell, kicker, head, deck, _r, _f, _p) in enumerate(LEADS):
        lx = x0 + i * (col_w + gap)
        img = crop_to(sheet_cell(sheet, cell), col_w, 128)
        page.paste(img, (lx, lead_y))
        badge(d, lx + 4, lead_y + 4, num)
        ty = lead_y + 134
        d.text((lx, ty), kicker, font=f_lead_k, fill=RED)
        ty += 15
        ty = draw_wrapped(d, lx, ty, head, f_lead_h, col_w, leading=20)
        ty += 2
        draw_wrapped(d, lx, ty, deck, f_lead_d, col_w, leading=13)
    y = lead_y + 228

    # ---- Small pictures: ten more, five across, two rows ----
    y += 4
    small_y = y
    sw, sgap = 195, 2
    f_sm_h = font(SERIF_B, 11)
    f_sm_d = font(SANS, 9)
    for i, (num, cell, head, deck, _r, _f, _p) in enumerate(SMALL):
        row, col = divmod(i, 5)
        sx = x0 + col * (sw + sgap)
        sy = small_y + row * 120
        img = crop_to(sheet_cell(sheet, cell), sw, 76)
        page.paste(img, (sx, sy))
        badge(d, sx + 3, sy + 3, num, size=15)
        ty = sy + 80
        ty = draw_wrapped(d, sx, ty, head, f_sm_h, sw, leading=13)
        draw_wrapped(d, sx, ty, deck, f_sm_d, sw, leading=11)
    y = small_y + 240

    # ---- Also on Wednesday: the remaining briefs, three columns ----
    y += 2
    f_also = font(SANS_B, 11)
    d.text((x0, y), "ALSO ON WEDNESDAY 18 NOVEMBER", font=f_also, fill=INK)
    d.line((x0 + 250, y + 6, x1, y + 6), fill=RULE, width=1)
    y += 17
    brief_y = y
    bw = 322
    f_b = font(SANS, 10)
    f_bp = font(SANS_B, 10)
    cols = [BRIEFS[i::3] for i in range(3)]
    for ci, col_items in enumerate(cols):
        bx = x0 + ci * (bw + 11)
        by = brief_y
        for place, text, _r, _f in col_items:
            line = place + " \u2014 " + text
            lines = wrap(d, line, f_b, bw)
            for li, ln in enumerate(lines):
                if li == 0:
                    pw = d.textlength(place + " ", font=f_bp)
                    d.text((bx, by), place + " ", font=f_bp, fill=INK)
                    d.text((bx + pw, by), ln[len(place) + 1:], font=f_b,
                           fill=INK)
                else:
                    d.text((bx, by), ln, font=f_b, fill=INK)
                by += 12
            by += 2
    y = brief_y + 180

    # ---- Map and date check ----
    y += 2
    map_w, box_h = 600, 82
    date_w = cw - map_w - 12
    dx = x0 + map_w + 12
    f_sec = font(SANS_B, 10)
    d.text((x0, y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.text((dx, y), "DATE CHECK \u2014 WHAT WE LEFT OUT", font=f_sec, fill=RED)
    y += 13
    draw_map(d, x0, y, map_w, box_h - 13)
    d.rectangle((dx, y, dx + date_w, y + box_h - 13), outline=RULE, width=1)
    f_dc = font(SANS, 9)
    draw_wrapped(d, dx + 6, y + 5, DATE_CHECK, f_dc, date_w - 12, leading=11)
    y += box_h + 4

    # ---- Footer ----
    d.rectangle((x0, y, x1, y), fill=RULE)
    y += 5
    draw_wrapped(d, x0, y, FOOTER, font(SANS, 8), cw, fill=MUTED, leading=10)

    page.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
