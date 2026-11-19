#!/usr/bin/env python3
"""Render the v2 front page for 18 November 2026: one image, 52 stories.

A dense front page in the winning pattern (navy masthead with NOV 18 box,
three big heroes, a UTC timeline, a numbers strip, a dotted world map and a
numbered ALSO ON list), but a composition of its own. Builds entry.png
(1024x1024) from sheet.webp (the 13 original editorial illustrations) plus
three flat data-graphics drawn here in code. Run:
    python3 render.py            # writes entry.png beside this file
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
NAVY = (16, 32, 54)
NAVY_LT = (38, 58, 86)
GOLD = (200, 164, 60)
GOLD_DK = (176, 138, 38)
RULE = (25, 25, 25)
SLATE = (58, 74, 90)
BAND = (232, 236, 240)

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

# (number, sheet cell or 'chart', kicker, headline, deck, region, field,
#  proof, caption or chip, map pin lon/lat or None)
HEROES = [
    (1, 1, "ASIA \u00b7 APEC SUMMIT",
     "Xi greets Trump as APEC opens in Shenzhen",
     "A rare honour from China's leader; Trump and Putin meet at the "
     "banquet, their three-way talks on Thursday.",
     "Asia", "Politics & diplomacy", "AP",
     "SHENZHEN \u00b7 APEC LEADERS' WEEK", (114.0, 22.5)),
    (2, 0, "MIDDLE EAST \u00b7 IRAN WAR",
     "Bahrain and Kuwait intercept Iran's drones",
     "Iran says it aimed at a US radar in Bahrain and Patriot batteries "
     "in Kuwait after a US strike on Qeshm.",
     "Middle East", "War & security", "AL JAZEERA",
     "BAHRAIN \u00b7 KUWAIT \u00b7 THE GULF", (48.0, 29.5)),
    (3, 3, "WORLD \u00b7 SPACE",
     "Voyager 1 reaches one light-day from Earth",
     "The first craft to get 25.9 billion km away; a command sent today "
     "takes a full day to arrive.",
     "World", "Climate & space", "NASA",
     "INTERSTELLAR SPACE \u00b7 NASA", None),
]

MEDIUM = [
    (4, 4, "EUROPE \u00b7 UKRAINE WAR",
     "Russia fires 141 drones at Ukraine; 126 downed",
     "Hits at seven sites overnight; four killed in Donetsk, its "
     "governor says.",
     "Europe", "War & security", "UK AIR FORCE",
     "141 FIRED \u00b7 126 DOWNED", (30.5, 50.4)),
    (5, 5, "ASIA \u00b7 LABOUR",
     "Bangladesh wage protests shut garment factories",
     "Workers want Tk30,000 a month; police report about 300 arrests.",
     "Asia", "Economy & labour", "DAILY STAR",
     "WAGE DEMAND TK 30,000", (90.4, 23.8)),
    (6, 6, "AMERICAS \u00b7 GAMES",
     "GTA VI goes on sale at midnight",
     "New Zealand first; the launch rolls out time zone by time zone.",
     "Americas", "Society & culture", "SENSOR TOWER",
     "00:00 THU \u00b7 NZ FIRST", (174.8, -36.8)),
    (7, 7, "AMERICAS \u00b7 US POLITICS",
     "Democrats pick Jeffries for Speaker",
     "A 251\u201311 caucus vote puts him on course to be the first Black "
     "Speaker.",
     "Americas", "Politics & diplomacy", "NPR \u00b7 CBS",
     "251\u201311 CAUCUS VOTE", (-77.0, 38.9)),
]

SMALL = [
    (8, 8, "AFRICA \u00b7 HORN",
     "Ethiopia and Eritrea mass troops on border",
     "Armies within striking distance.",
     "Africa", "War & security", "REUTERS", (37.8, 14.7)),
    (9, 9, "ASIA \u00b7 WEATHER",
     "Cyclone Akvan veers north toward Odisha",
     "Landfall due 20 Nov; evacuations begin.",
     "Asia", "Disasters & weather", "IMD", (82.0, 16.0)),
    (10, 10, "MIDDLE EAST \u00b7 GAZA",
     "Israeli tanks roll into central Gaza",
     "Near Nuseirat; three killed.",
     "Middle East", "War & security", "REUTERS", (34.5, 31.5)),
    (11, 11, "AFRICA \u00b7 HEALTH",
     "Ebola passes 11,000 cases in DR Congo",
     "Second-largest outbreak on record.",
     "Africa", "Health", "WHO", (25.0, -2.0)),
    (12, 12, "AMERICAS \u00b7 HEALTH",
     "US loses measles-free status after 26 years",
     "5,412 cases in 2026; 10 deaths.",
     "Americas", "Health", "CDC", (-98.0, 39.5)),
]

# (number, chart kind, kicker, headline, deck, region, field, proof, pin)
CHARTS = [
    (13, "dow", "AMERICAS \u00b7 MARKETS",
     "Fed minutes: almost all officials see more hikes",
     "Dow falls 1.1%; the Nasdaq gains.",
     "Americas", "Economy & labour", "FED \u00b7 AP", (-77.0, 38.9)),
    (14, "cpi", "EUROPE \u00b7 ECONOMY",
     "UK inflation climbs to 3.6%, a one-year high",
     "October CPI up from 3.5%, ONS says.",
     "Europe", "Economy & labour", "ONS", (-0.1, 51.5)),
    (15, "ipo", "AMERICAS \u00b7 BUSINESS",
     "Anthropic prices the biggest IPO ever",
     "$83 a share; $83.1bn raised.",
     "Americas", "Economy & labour", "AL JAZEERA", (-122.4, 37.8)),
    (16, 2, "WORLD \u00b7 CLIMATE",
     "COP31 still split over a fossil-fuel phase-out",
     "Ministers face a Friday deadline in Antalya.",
     "World", "Climate & space", "AFP", (30.7, 36.9)),
]

# (number, place, text) -- one line each, kept short on purpose.
BRIEFS = [
    (17, "Riyadh", "Houthi missile downed"),
    (18, "Knesset", "nine deputies, two Arab"),
    (19, "Berlin", "power tax cut, fuel cap"),
    (20, "Germany", "Russia chemical breach"),
    (21, "Cambridge", "'human' word of the year"),
    (22, "Shenzhen", "Xi, Lee end FTA talks"),
    (23, "Manila", "Trump deal claim denied"),
    (24, "Tokyo", "sixth monthly trade deficit"),
    (25, "Brussels", "\u20ac45bn Ukraine loan for 2027"),
    (26, "Gold", "below $3,800, a one-year low"),
    (27, "Canberra", "settler leader sanctioned"),
    (28, "El Obeid", "RSF drones kill 37, Amnesty"),
    (29, "Quad", "leaders meet in Manila"),
    (30, "Caracas", "US\u2013Venezuela military pact"),
    (31, "Sudan", "2,230 civilians killed in 2026"),
    (32, "Naypyidaw", "Myanmar-ASEAN review"),
    (33, "Stockholm", "antibiotic goal missed"),
    (34, "Lahore", "most polluted city, AQI 339"),
    (35, "Oil", "Brent slips to about $92"),
    (36, "Tencent", "revenue up 8%, miss"),
    (37, "Cook Islands", "Xavier hits Cat 5"),
    (38, "Wellington", "tsunami advisory lifted"),
    (39, "Sydney", "Tame Impala sweeps ARIAs"),
    (40, "Ottawa", "Carney: China trade no worry"),
    (41, "Lima", "M5.9 quake, no damage"),
    (42, "Cincinnati", "USA beat Haiti 2\u20130"),
    (43, "Monterrey", "Mexico edge Jamaica"),
    (44, "Los Angeles", "Grimes scores 47 in win"),
    (45, "Buenos Aires", "Malvinas bill debated"),
    (46, "Washington", "NSA classified outage"),
    (47, "Pretoria", "inflation jumps to 5.2%"),
    (48, "Haiti", "troops raid gang boss home"),
    (49, "Pew", "Muslims top Christians by 2035"),
    (50, "Alcaraz", "beats Medvedev in Turin"),
    (51, "Nvidia", "shares fall 2.9% on results"),
    (52, "Board of Peace", "Gaza truce at risk"),
]

NUMBERS = [
    ("141", "drones at Ukraine"),
    ("25.9bn km", "to Voyager 1"),
    ("$3,792", "gold an ounce"),
    ("251\u201311", "Jeffries vote"),
    ("2,230", "killed in Sudan"),
]

TIMELINE = [
    ("OVERNIGHT", "Drones over Gulf"),
    ("07:00", "UK inflation 3.6%"),
    ("MORNING", "Xi greets Trump"),
    ("10:16", "Voyager 1 light-day"),
    ("11:00", "GTA VI in NZ"),
    ("19:00", "Fed: more hikes"),
    ("21:00", "Dow \u2212561"),
]

DATE_CHECK = (
    "Left out on purpose \u2014 first reported Tue 17 Nov: Peltola\u2019s "
    "Alaska Senate win; Nvidia\u2019s $115.8bn quarter; the Kerch Bridge "
    "span collapse; the Prague train crash; Mongolia\u2019s president "
    "resigning; the Knesset speaker vote. Cyclone Akvan formed 16 Nov "
    "\u2014 today is its approach. The Qeshm strike (Tue night) appears "
    "only as the cause of today\u2019s drones."
)

FOOTER = (
    "Every story here happened, or was first reported, on Wednesday, "
    "18 November 2026. Contested claims are attributed. Sources: Reuters, "
    "AP, AFP, BBC, Al Jazeera, Bloomberg, NASA, WHO, ONS. Original "
    "illustrations and charts."
)

# World map as a 96 x 24 dotted grid, equirectangular, lon -180..180,
# lat 78..-56. Each row lists the land intervals (first, last) in columns.
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


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None,
                 max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    if leading is None:
        leading = int(fnt.size * 1.28)
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
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


def gold_badge(draw, x, y, num, size=20):
    """Gold disc with a navy story number."""
    r = size // 2
    draw.ellipse((x, y, x + size, y + size), fill=GOLD,
                 outline=(255, 255, 255), width=1)
    f = font(SANS_B, 11)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (size - tw) / 2, y + 3), t, font=f, fill=NAVY)


def red_badge(draw, x, y, num, size=16):
    """Red disc with a white story number."""
    draw.ellipse((x, y, x + size, y + size), fill=RED)
    f = font(SANS_B, 10)
    t = str(num)
    tw = draw.textlength(t, font=f)
    draw.text((x + (size - tw) / 2, y + 2), t, font=f, fill=(255, 255, 255))


def kicker_line(draw, x, y, num, kicker, proof, width, badge_size=16,
                gold=False):
    """Number badge + red kicker + right-aligned proof tag."""
    if gold:
        gold_badge(draw, x, y - 3, num, size=badge_size)
    else:
        red_badge(draw, x, y - 2, num, size=badge_size)
    kx = x + badge_size + 6
    f_k = font(SANS_B, 10)
    draw.text((kx, y), kicker, font=f_k, fill=RED)
    f_p = font(SANS_B, 8)
    pw = draw.textlength(proof, font=f_p)
    draw.text((x + width - pw, y + 1), proof, font=f_p, fill=MUTED)


def map_point(lon, lat, mx, my, mw, mh):
    """Project lon/lat onto the map box (mx, my, mw, mh)."""
    px = mx + (lon + 180.0) / 360.0 * mw
    py = my + (78.0 - lat) / 134.0 * mh
    return px, py


def draw_map(draw, x, y, w, h, pins):
    """Dotted continents plus numbered pins for the illustrated stories."""
    draw.rectangle((x, y, x + w, y + h), outline=RULE, width=1)
    cw, ch = w / 96.0, h / 24.0
    for r, intervals in enumerate(MAP_LAND):
        for c0, c1 in intervals:
            for c in range(c0, c1 + 1):
                cx = x + (c + 0.5) * cw
                cy = y + (r + 0.5) * ch
                draw.ellipse((cx - 1.2, cy - 1.2, cx + 1.2, cy + 1.2),
                             fill=SLATE)
    f = font(SANS_B, 7)
    nudge = {2: (9, 4), 7: (-7, -7), 10: (-4, 7), 13: (8, 7), 16: (7, -6)}
    for num, (lon, lat) in pins:
        px, py = map_point(lon, lat, x + 4, y + 4, w - 8, h - 8)
        dx, dy = nudge.get(num, (0, 0))
        px, py = px + dx, py + dy
        draw.ellipse((px - 5, py - 5, px + 5, py + 5), fill=RED,
                     outline=(255, 255, 255), width=1)
        t = str(num)
        tw = draw.textlength(t, font=f)
        draw.text((px - tw / 2, py - 4), t, font=f, fill=(255, 255, 255))


def draw_chart(kind, w, h):
    """Flat data-graphic card (PIL-drawn) for the chart-row stories."""
    img = Image.new("RGB", (w, h), (16, 32, 54))
    d = ImageDraw.Draw(img)
    if kind == "dow":
        # Falling line, Dow -561 (-1.1%).
        pts = [(14, 12), (40, 16), (66, 14), (92, 22), (118, 20),
               (144, 28), (170, 26), (196, 34), (222, 40)]
        for i in range(len(pts) - 1):
            d.line((pts[i], pts[i + 1]), fill=(255, 255, 255), width=2)
        for px, py in pts:
            d.ellipse((px - 2, py - 2, px + 2, py + 2), fill=GOLD)
        d.text((14, h - 20), "DOW \u2212561  \u00b7  \u22121.1%",
               font=font(SANS_B, 11), fill=(255, 255, 255))
    elif kind == "cpi":
        # Big-number card: 3.6%, up from 3.5% in September.
        d.text((14, 4), "3.6%", font=font(SERIF_B, 28), fill=GOLD)
        d.text((14, h - 18), "UK INFLATION \u00b7 UP FROM 3.5%",
               font=font(SANS_B, 9), fill=(255, 255, 255))
        d.rectangle((w - 52, 10, w - 14, h - 24), outline=GOLD, width=2)
        d.text((w - 46, 14), "ONS", font=font(SANS_B, 11), fill=GOLD)
    elif kind == "ipo":
        d.text((14, 6), "$83", font=font(SERIF_B, 30), fill=GOLD)
        d.text((14, h - 20), "A SHARE \u00b7 $83.1BN RAISED",
               font=font(SANS_B, 10), fill=(255, 255, 255))
        bars = [10, 16, 13, 22, 30]
        bx = w - 78
        for i, bh in enumerate(bars):
            d.rectangle((bx + i * 14, h - 8 - bh, bx + i * 14 + 9, h - 8),
                        fill=(120, 140, 170) if i < 4 else GOLD)
    return img


def build(out_path):
    sheet = Image.open(os.path.join(HERE, "sheet.webp")).convert("RGB")
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    d.rectangle((6, 6, W - 7, H - 7), outline=INK, width=2)

    x0, x1 = 18, W - 18
    cw = x1 - x0
    y = 14

    # ---- Masthead: navy band, NOV 18 box, giant date, story counts ----
    band_y, band_h = 14, 80
    d.rectangle((x0, band_y, x1, band_y + band_h), fill=NAVY)
    # Calendar box.
    bx, by, bw, bh = x0 + 10, band_y + 9, 62, 66
    d.rectangle((bx, by, bx + bw, by + bh), fill=(255, 255, 255))
    d.rectangle((bx, by, bx + bw, by + 18), fill=RED)
    f_nov = font(SANS_B, 11)
    t = "NOV"
    d.text((bx + (bw - d.textlength(t, font=f_nov)) / 2, by + 3), t,
           font=f_nov, fill=(255, 255, 255))
    f_day = font(SERIF_B, 32)
    t = "18"
    d.text((bx + (bw - d.textlength(t, font=f_day)) / 2, by + 18), t,
           font=f_day, fill=NAVY)
    f_wd = font(SANS_B, 8)
    t = "WED \u00b7 2026"
    d.text((bx + (bw - d.textlength(t, font=f_wd)) / 2, by + 52), t,
           font=f_wd, fill=NAVY)
    # Date, centred between the box and the right counts.
    f_date = font(SERIF_B, 40)
    dt = "Wednesday 18 November 2026"
    cx = (x0 + bw + 24 + x1 - 190) / 2
    d.text((cx - d.textlength(dt, font=f_date) / 2, band_y + 10), dt,
           font=f_date, fill=(255, 255, 255))
    f_tag = font(SERIF, 12)
    tg = "Everything on this page happened, or was first reported, today."
    d.text((cx - d.textlength(tg, font=f_tag) / 2, band_y + 58), tg,
           font=f_tag, fill=(200, 210, 220))
    # Right counts.
    f_c1 = font(SANS_B, 13)
    f_c2 = font(SANS, 10)
    rt1 = "52 STORIES"
    rt2 = "7 REGIONS \u00b7 16 PICTURES"
    d.text((x1 - 10 - d.textlength(rt1, font=f_c1), band_y + 22), rt1,
           font=f_c1, fill=GOLD)
    d.text((x1 - 10 - d.textlength(rt2, font=f_c2), band_y + 42), rt2,
           font=f_c2, fill=(255, 255, 255))
    y = band_y + band_h + 4
    d.rectangle((x0, y, x1, y + 3), fill=GOLD)
    y += 9

    # ---- The day in numbers: five big figures in one row ----
    # Shrink until the row fits the page width.
    num_size = 22
    while True:
        f_nl = font(SANS_B, 11)
        f_nn = font(SERIF_B, num_size)
        f_nt = font(SANS, 10)
        runs = [("THE DAY IN NUMBERS   ", f_nl, RED)]
        for num, txt in NUMBERS:
            runs.append((num + " ", f_nn, RED))
            runs.append((txt + "    \u00b7    ", f_nt, INK))
        runs[-1] = (runs[-1][0].rstrip("    \u00b7    "), f_nt, INK)
        total_w = sum(d.textlength(t, font=f) for t, f, _ in runs)
        if total_w <= cw or num_size <= 16:
            break
        num_size -= 1
    rx = (W - total_w) / 2
    for text, fnt, fill in runs:
        # Numbers sit on the baseline of the label text.
        dy = 4 if fnt is f_nn else 10
        d.text((rx, y + dy), text, font=fnt, fill=fill)
        rx += d.textlength(text, font=fnt)
    y += 30

    # ---- The day in UTC: seven timed beats on a slate band ----
    f_tll = font(SANS_B, 10)
    d.text((x0, y), "THE DAY IN UTC", font=f_tll, fill=RED)
    y += 14
    tl_y, tl_h = y, 26
    d.rectangle((x0, tl_y, x1, tl_y + tl_h), fill=BAND)
    f_tt = font(SANS_B, 9)
    f_tx = font(SANS, 9)
    seg_w = (cw - 16) / len(TIMELINE)
    for i, (tm, tx) in enumerate(TIMELINE):
        sx = x0 + 8 + i * seg_w
        d.text((sx, tl_y + 8), tm, font=f_tt, fill=NAVY)
        d.text((sx + d.textlength(tm + " ", font=f_tt), tl_y + 8), tx,
               font=f_tx, fill=INK)
    y = tl_y + tl_h + 4

    # ---- Heroes: three big pictures with caption bars ----
    hero_y = y
    col_w, gap = 322, 11
    f_hh = font(SERIF_B, 19)
    f_hd = font(SANS, 10)
    img_h = 124
    for i, (num, cell, kicker, head, deck, _r, _f, proof, cap, _p) in \
            enumerate(HEROES):
        lx = x0 + i * (col_w + gap)
        img = crop_to(sheet_cell(sheet, cell), col_w, img_h)
        page.paste(img, (lx, hero_y))
        d.rectangle((lx, hero_y + img_h - 18, lx + col_w,
                     hero_y + img_h), fill=NAVY)
        f_cap = font(SANS_B, 9)
        d.text((lx + (col_w - d.textlength(cap, font=f_cap)) / 2,
                hero_y + img_h - 14), cap, font=f_cap,
               fill=(255, 255, 255))
        ty = hero_y + img_h + 5
        kicker_line(d, lx, ty, num, kicker, proof, col_w, badge_size=20,
                    gold=True)
        ty += 20
        ty = draw_wrapped(d, lx, ty, head, f_hh, col_w, leading=22,
                          max_lines=2)
        ty += 2
        draw_wrapped(d, lx, ty, deck, f_hd, col_w, leading=13,
                     max_lines=2)
    y = hero_y + 222

    # ---- Medium row: four illustrated stories with overlay chips ----
    y += 4
    med_y = y
    mw, mgap = 242, 10
    f_mh = font(SERIF_B, 14)
    f_md = font(SANS, 9)
    for i, (num, cell, kicker, head, deck, _r, _f, proof, chip, _p) in \
            enumerate(MEDIUM):
        mx = x0 + i * (mw + mgap)
        img = crop_to(sheet_cell(sheet, cell), mw, 88)
        page.paste(img, (mx, med_y))
        f_chip = font(SANS_B, 8)
        cw_chip = d.textlength(chip, font=f_chip) + 10
        d.rectangle((mx, med_y, mx + cw_chip, med_y + 14), fill=NAVY)
        d.text((mx + 5, med_y + 3), chip, font=f_chip,
               fill=(255, 255, 255))
        ty = med_y + 92
        kicker_line(d, mx, ty, num, kicker, proof, mw, badge_size=16)
        ty += 17
        ty = draw_wrapped(d, mx, ty, head, f_mh, mw, leading=16,
                          max_lines=2)
        ty += 1
        draw_wrapped(d, mx, ty, deck, f_md, mw, leading=12, max_lines=2)
    y = med_y + 166

    # ---- Small row: five illustrated stories ----
    y += 4
    sm_y = y
    sw, sgap = 195, 2
    f_sh = font(SERIF_B, 11)
    f_sd = font(SANS, 9)
    for i, (num, cell, kicker, head, deck, _r, _f, proof, _p) in \
            enumerate(SMALL):
        sx = x0 + i * (sw + sgap)
        img = crop_to(sheet_cell(sheet, cell), sw, 60)
        page.paste(img, (sx, sm_y))
        ty = sm_y + 63
        kicker_line(d, sx, ty, num, kicker, proof, sw, badge_size=15)
        ty += 15
        ty = draw_wrapped(d, sx, ty, head, f_sh, sw, leading=13,
                          max_lines=2)
        draw_wrapped(d, sx, ty, deck, f_sd, sw, leading=11, max_lines=2)
    y = sm_y + 116

    # ---- Chart row: three data-graphics plus COP31 ----
    y += 4
    ch_y = y
    cw2, cgap = 242, 10
    f_ch = font(SERIF_B, 13)
    f_cd = font(SANS, 9)
    for i, (num, kind, kicker, head, deck, _r, _f, proof, _p) in \
            enumerate(CHARTS):
        cx2 = x0 + i * (cw2 + cgap)
        if isinstance(kind, int):
            img = crop_to(sheet_cell(sheet, kind), cw2, 49)
        else:
            img = draw_chart(kind, cw2, 49)
        page.paste(img, (cx2, ch_y))
        ty = ch_y + 52
        kicker_line(d, cx2, ty, num, kicker, proof, cw2, badge_size=15)
        ty += 15
        ty = draw_wrapped(d, cx2, ty, head, f_ch, cw2, leading=15,
                          max_lines=2)
        draw_wrapped(d, cx2, ty, deck, f_cd, cw2, leading=11,
                     max_lines=1)
    y = ch_y + 108

    # ---- Bottom: world map + numbered ALSO ON list ----
    y += 4
    bot_y = y
    map_w = 372
    f_sec = font(SANS_B, 11)
    d.text((x0, bot_y), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    ax = x0 + map_w + 12
    aw = x1 - ax
    d.text((ax, bot_y), "ALSO ON WEDNESDAY 18 NOVEMBER", font=f_sec,
           fill=INK)
    d.line((ax + 252, bot_y + 6, x1, bot_y + 6), fill=RULE, width=1)
    my = bot_y + 16
    pins = [(s[0], s[9]) for s in HEROES + MEDIUM]
    pins += [(s[0], s[8]) for s in SMALL + CHARTS]
    pins = [(n, pin) for (n, pin) in pins if pin is not None]
    draw_map(d, x0, my, map_w, 122, pins)
    f_note = font(SANS, 8)
    d.text((x0 + 4, my + 126),
           "3 \u2014 Voyager 1 \u2014 is 25.9bn km away, off this map.",
           font=f_note, fill=MUTED)
    f_leg = font(SANS, 8)
    lx2 = x0 + 4
    for region in ("Asia", "Middle East", "Europe", "Africa", "Americas",
                   "Oceania"):
        d.ellipse((lx2, my + 140, lx2 + 7, my + 147),
                  fill=REGION_COLORS[region])
        lx2 += 10
        t = region
        d.text((lx2, my + 138), t, font=f_leg, fill=INK)
        lx2 += d.textlength(t, font=f_leg) + 9
    # ALSO ON: three columns of one-line briefs.
    f_b = font(SANS, 9)
    f_bp = font(SANS_B, 9)
    f_bn = font(SANS_B, 9)
    col_w2 = (aw - 16) // 3
    cols = [BRIEFS[i::3] for i in range(3)]
    overflow = []
    for ci, col_items in enumerate(cols):
        bx2 = ax + ci * (col_w2 + 8)
        by2 = my
        for num, place, text in col_items:
            line = "%d %s \u2014 %s" % (num, place, text)
            if d.textlength(line, font=f_b) > col_w2:
                overflow.append(line)
            d.text((bx2, by2), str(num) + " ", font=f_bn, fill=RED)
            nw = d.textlength(str(num) + " ", font=f_bn)
            pw = d.textlength(place + " ", font=f_bp)
            d.text((bx2 + nw, by2), place + " ", font=f_bp, fill=INK)
            d.text((bx2 + nw + pw, by2),
                   "\u2014 " + text, font=f_b, fill=INK)
            by2 += 12
    if overflow:
        print("BRIEF OVERFLOW (%d):" % len(overflow))
        for line in overflow:
            print("  ", line)
    y = bot_y + 160

    # ---- Date check strip ----
    y += 2
    d.rectangle((x0, y, x0 + 5, y + 26), fill=RED)
    f_dc = font(SANS, 9)
    f_dcl = font(SANS_B, 10)
    d.text((x0 + 10, y + 2), "DATE CHECK", font=f_dcl, fill=RED)
    dw = d.textlength("DATE CHECK  ", font=f_dcl)
    draw_wrapped(d, x0 + 10 + dw, y + 2, DATE_CHECK, f_dc,
                 cw - 10 - dw, leading=11, max_lines=2)
    y += 28

    # ---- Footer ----
    d.rectangle((x0, y, x1, y), fill=RULE)
    y += 5
    draw_wrapped(d, x0, y, FOOTER, font(SANS, 8), cw, fill=MUTED,
                 leading=10)
    y += 10
    print("final y:", y, "(limit 1018)")

    page.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "entry.png")
    build(out)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
