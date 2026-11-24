#!/usr/bin/env python3
"""THE HARBOUR POST — NI23 G4 compose v2 (akun16).

1024x1024 front page, Monday 23 November 2026. Layout A: lead trio on
top, three rows of three, last row card 13 + DATE CHECK, numbers strip,
map + flowing ALSO ON, footer. Layout B: numbers rail on the left.
Flat harbour palette: white paper, sea-blue ink, coral accent.
All story data from the locked ni23 pool.
"""
import math
import sys
from PIL import Image, ImageDraw, ImageFont

FONTS = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts/"
W = H = 1024
INK = (11, 61, 92)
INK_DARK = (7, 38, 58)
CORAL = (228, 87, 46)
PAPER = (255, 255, 255)
GREY = (90, 100, 108)
LIGHT = (232, 240, 244)
RED = (178, 34, 34)

REGION_COLORS = {
    "EUROPE": (38, 92, 140), "MIDDLE EAST": (196, 110, 30),
    "N. AMERICA": (150, 40, 60), "S. ASIA": (30, 130, 110),
    "SE ASIA": (110, 70, 160), "ASIA-PACIFIC": (40, 140, 170),
    "GLOBAL": (110, 110, 110),
}


def F(name, size):
    return ImageFont.truetype(FONTS + name, size)


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, font, maxw, maxlines):
    lines = wrap(d, text, font, maxw)
    if len(lines) > maxlines:
        lines = lines[:maxlines]
        last = lines[-1]
        while last and d.textlength(last + "…", font=font) > maxw:
            last = last[:-1].rsplit(" ", 1)[0]
        lines[-1] = last + "…"
    return lines


# num, loc, region, chip, cat, title, facts, source, scene
CARDS = [
    (1, "WASHINGTON · USA", "N. AMERICA", "OFFICIAL", "INVESTIGATION",
     "FBI Probes Hack of Its Justice Database",
     "A suspected breach of its criminal-justice database.",
     "Source: AP wire", "database"),
    (2, "STRAIT OF HORMUZ", "MIDDLE EAST", "REPORTED", "WAR AT SEA",
     "Tankers Burn in the Strait of Hormuz",
     "Tankers ablaze as the Iran–US war widens into the Gulf.",
     "Source: AP live", "ship"),
    (3, "BAHRAIN", "MIDDLE EAST", "CLAIM", "WAR",
     "IRGC Claims Two Patriot Radars Hit in Bahrain",
     "Tehran says both radars destroyed; US unconfirmed.",
     "Source: AFP / AP", "radar"),
    (4, "ANTALYA · TÜRKIYE", "EUROPE", "OFFICIAL", "CLIMATE",
     "COP31 Ends Without a Deal",
     "Final Turkish draft omits 'fossil fuels'.",
     "Source: BBC / AP", "leaf"),
    (5, "KYIV · UKRAINE", "EUROPE", "REPORTED", "WAR",
     "Kyiv Boy, 7, Pulled Alive From Rubble",
     "Freed after hours under debris; six killed.",
     "Source: BBC", "rubble"),
    (6, "KYIV REGION", "EUROPE", "ON RECORD", "WAR",
     "14 Missing After Kyiv Strike, Zelenskiy Says",
     "Russian drone hit a Kyiv-region block.",
     "Source: JagranJosh", "drone"),
    (7, "GULF OF FINLAND", "EUROPE", "ONGOING", "SEA",
     "Russian Cargo Ship Still Burns Off Finland",
     "Still burns after attack; second ship towed.",
     "Source: BBC", "shipfire"),
    (8, "WASHINGTON · USA", "N. AMERICA", "CONFIRMED", "POLITICS",
     "Democrats Take the House, 258–173",
     "Largest since 1992, sealed in N. Carolina.",
     "Source: BBC", "ballot"),
    (9, "WELLINGTON · NZ", "S. ASIA", "REPORTED", "CRICKET",
     "India Declare on a Record 720/9",
     "Highest Test total ever made in NZ.",
     "Source: ObserverVoice", "cricket"),
    (10, "GLOBAL MARKETS", "GLOBAL", "REPORTED", "MONEY",
     "Gold Slides to $3,538 an Ounce",
     "Down $2,000+ from the $5,595 record.",
     "Source: ObserverVoice", "gold"),
    (11, "THE HAGUE", "SE ASIA", "OFFICIAL", "LAW",
     "ICJ Rules Myanmar Guilty of Genocide",
     "Rohingya campaign of 2017; 700,000+ fled.",
     "Source: Guardian / NYT", "gavel"),
    (12, "IOWA · USA", "N. AMERICA", "REPORTED", "SAFETY",
     "Army to Detonate Unstable Explosives in Iowa",
     "Blast planned despite a court order.",
     "Source: BBC", "blast"),
    (13, "TURIN · ITALY", "EUROPE", "REPORTED", "TENNIS",
     "Alcaraz Beats Zverev for First ATP Finals Title",
     "A first ATP Finals crown, won in Turin.",
     "Source: BBC", "trophy"),
]

ALSO = [
    (14, "Houthi missile downed over Saudi west"),
    (15, "Swimmer crosses Hormuz for Iran's wildlife"),
    (16, "UN: talks on killer AI to continue"),
    (17, "US releases more UFO footage files"),
    (18, "Albanese: COP31 failure, hard times"),
    (19, "Ship towed after Gulf of Finland attack"),
    (20, "UK–EU Brexit reset called 'landmark'"),
    (21, "Thousands march in Lisbon on living costs"),
    (22, "Myanmar junta: ASEAN ruling 'unfair'"),
    (23, "Escaped lion frightens Turkish town"),
    (24, "Nepal's Shah meets Modi in Delhi"),
    (25, "India, Bulgaria talk IMEC, Black Sea"),
    (26, "Guru Nanak Jayanti marked across India"),
    (27, "UP runs air-raid drills in 75 districts"),
    (28, "Factory fire update: 7 found, 50 missing"),
    (29, "NZ 119/2 as India chase famous win"),
    (30, "India win NZ ODI series 3–2"),
    (31, "Anupama keeps IBSF snooker crown"),
    (32, "World Chess Championship draws fans"),
    (33, "Rajya Sabha MP Wadkute dies in Delhi"),
    (34, "Kota pilgrim bus crash kills 9"),
    (35, "Tata Steel pipe unit sold, ₹28,000 cr"),
    (36, "IndiGo holds 65.9% of India's skies"),
    (37, "Modi opens AI centre at IIT Patna"),
    (38, "Trump attacks Schumer over Dem push"),
]

NUMBERS = [
    ("258–173", "US House split"),
    ("720/9", "India's record total"),
    ("$3,538", "gold per ounce"),
    ("14", "missing in Kyiv"),
    ("50", "missing, fire update"),
    ("₹28,000 cr", "Tata pipe-unit sale"),
]

DATECHECK = [
    "Xi–Trump–Putin summit — 19 Nov 2026",
    "Russian missiles fell in Poland — 20 Nov 2026",
    "Paolo Bulgari died — reported 22 Nov 2026",
    "Kim Jong-un 'security, not supremacy' — 22 Nov 2026",
    "Bolsonaro stable in ICU — 22 Nov 2026",
    "S. Korea education minister quit — first reported 22 Nov 2026",
    "Indonesia candy-factory fire itself — 22 Nov 2026 (only its 23 Nov toll update is today's news)",
]

TIMELINE = [
    ("00:02 UTC", "AI talks go on"),
    ("02:00 UTC", "Sydney: COP31 reaction"),
    ("MORNING", "FBI hack probe opens"),
    ("MIDDAY", "ICJ: Myanmar guilty"),
    ("EVENING", "House confirmed 258–173"),
]

REGIONS_STRIP = [("EUROPE", 10), ("S. ASIA", 12), ("N. AMERICA", 5),
                 ("MIDDLE EAST", 4), ("SE ASIA", 3), ("GLOBAL", 3),
                 ("ASIA-PACIFIC", 1)]

MAP_ROWS = [
    "                                                                        ",
    "        #####                                                           ",
    "      #########        ##    ##########                                 ",
    "     ###########     ################################                   ",
    "      #########       ##################################   ##           ",
    "       #######         ####################################             ",
    "        #####           ################  ################              ",
    "         ###             ##############    ##############               ",
    "        ####              ##########        ##########                  ",
    "       ######              ########          ########        #          ",
    "      ########              ######            ######        ###         ",
    "       ######               #####             #####        #####        ",
    "        ####                ####              ####          ###         ",
    "         ##                 ###               ##                        ",
    "                            ##                                          ",
    "                            #                                           ",
    "                                                                        ",
]

PINS = {1: (-77, 39), 2: (56, 26), 3: (50, 26), 4: (30, 37), 5: (30, 50),
        6: (34, 49), 7: (25, 60), 8: (-73, 42), 9: (175, -41),
        10: (-74, 40), 11: (4, 52), 12: (-93, 42), 13: (8, 45)}


def draw_scene(d, x, y, w, h, scene, color):
    d.rectangle([x, y, x + w, y + h], fill=color)
    cx, cy = x + w // 2, y + h // 2
    wh = (255, 255, 255)
    gold = (255, 200, 70)
    s = h / 44.0  # scale
    def P(dx, dy):
        return (cx + dx * s, cy + dy * s)
    if scene in ("ship", "shipfire"):
        d.polygon([P(-26, 4), P(26, 4), P(18, 12), P(-18, 12)], fill=wh)
        d.rectangle([cx - 12 * s, cy - 4 * s, cx + 8 * s, cy + 4 * s], fill=wh)
        if scene == "shipfire":
            d.polygon([P(-4, -18), P(3, -7), P(-9, -7)], fill=gold)
            d.polygon([P(9, -14), P(14, -6), P(5, -6)], fill=gold)
    elif scene == "database":
        d.ellipse([cx - 16 * s, cy - 11 * s, cx + 16 * s, cy - 2 * s], outline=wh, width=2)
        d.rectangle([cx - 16 * s, cy - 11 * s, cx + 16 * s, cy + 9 * s], outline=wh, width=2)
        d.ellipse([cx - 16 * s, cy, cx + 16 * s, cy + 9 * s], outline=wh, width=2)
    elif scene == "radar":
        d.line([P(-18, 11), P(4, -11)], fill=wh, width=3)
        d.arc([cx - 2 * s, cy - 18 * s, cx + 28 * s, cy + 12 * s], 200, 330, fill=wh, width=3)
        d.arc([cx + 5 * s, cy - 24 * s, cx + 40 * s, cy + 12 * s], 200, 330, fill=gold, width=2)
    elif scene == "leaf":
        d.ellipse([cx - 14 * s, cy - 11 * s, cx + 13 * s, cy + 11 * s], fill=wh)
        d.line([P(-12, 9), P(14, -11)], fill=color, width=2)
    elif scene == "rubble":
        d.polygon([P(-24, 11), P(-7, -6), P(4, 11)], outline=wh, width=3)
        d.polygon([P(-3, 11), P(11, -11), P(24, 11)], outline=wh, width=3)
        d.ellipse([cx - 3 * s, cy - 2 * s, cx + 4 * s, cy + 5 * s], fill=gold)
    elif scene == "drone":
        d.rectangle([cx - 14 * s, cy - 3 * s, cx + 14 * s, cy + 3 * s], fill=wh)
        for dx in (-20, 20):
            d.ellipse([cx + (dx - 5) * s, cy - 11 * s, cx + (dx + 5) * s, cy - 3 * s], outline=wh, width=2)
            d.ellipse([cx + (dx - 5) * s, cy + 3 * s, cx + (dx + 5) * s, cy + 11 * s], outline=wh, width=2)
    elif scene == "ballot":
        d.rectangle([cx - 16 * s, cy - 5 * s, cx + 16 * s, cy + 12 * s], outline=wh, width=3)
        d.rectangle([cx - 7 * s, cy - 12 * s, cx + 7 * s, cy - 3 * s], fill=wh)
        d.line([P(-9, 3), P(-3, 9)], fill=gold, width=3)
        d.line([P(-3, 9), P(10, -1)], fill=gold, width=3)
    elif scene == "cricket":
        d.polygon([P(-14, -12), P(-7, -11), P(2, 11), P(-5, 12)], fill=wh)
        d.ellipse([cx + 7 * s, cy - 2 * s, cx + 19 * s, cy + 10 * s], fill=gold)
    elif scene == "gold":
        for i, (dx, dy) in enumerate([(-18, 4), (2, 4), (-8, -7)]):
            d.polygon([P(dx, dy), P(dx + 16, dy), P(dx + 13, dy - 7), P(dx + 3, dy - 7)],
                      fill=gold if i == 2 else wh)
    elif scene == "gavel":
        d.rectangle([cx - 18 * s, cy + 7 * s, cx + 18 * s, cy + 11 * s], fill=wh)
        d.polygon([P(-4, -12), P(14, 3), P(7, 9), P(-11, -7)], fill=wh)
        d.line([P(9, 1), P(20, 12)], fill=wh, width=3)
    elif scene == "blast":
        for ang in range(0, 360, 45):
            x1 = cx + 5 * s * math.cos(math.radians(ang))
            y1 = cy + 5 * s * math.sin(math.radians(ang))
            x2 = cx + 17 * s * math.cos(math.radians(ang))
            y2 = cy + 17 * s * math.sin(math.radians(ang))
            d.line([x1, y1, x2, y2], fill=gold, width=3)
        d.ellipse([cx - 5 * s, cy - 5 * s, cx + 5 * s, cy + 5 * s], fill=wh)
    elif scene == "trophy":
        d.polygon([P(-11, -12), P(11, -12), P(11, -2), P(4, 3), P(-4, 3), P(-11, -2)], fill=gold)
        d.arc([cx - 20 * s, cy - 12 * s, cx - 9 * s, cy + 2 * s], 90, 270, fill=wh, width=2)
        d.arc([cx + 9 * s, cy - 12 * s, cx + 20 * s, cy + 2 * s], 270, 90, fill=wh, width=2)
        d.rectangle([cx - 7 * s, cy + 7 * s, cx + 7 * s, cy + 11 * s], fill=wh)


def header_block(d):
    d.rectangle([0, 0, W, 26], fill=INK)
    d.text((14, 5), "THE HARBOUR POST", font=F("Archivo-Bold.ttf", 15),
           fill=(255, 255, 255))
    kick = "38 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    kf = F("Archivo-Bold.ttf", 13)
    d.text((W - 14 - d.textlength(kick, font=kf), 6), kick, font=kf,
           fill=(255, 190, 120))
    d.text((14, 32), "THE HARBOUR POST", font=F("PlayfairDisplay-Black.ttf", 26),
           fill=INK)
    d.text((14, 58), "Monday 23 November 2026",
           font=F("PlayfairDisplay-Black.ttf", 72), fill=INK_DARK)
    sub = ("FBI probes a hack of its justice database  ·  Tankers burn in the "
           "Strait of Hormuz  ·  COP31 ends with no deal")
    d.text((14, 140), sub, font=F("Archivo-Bold.ttf", 15), fill=CORAL)
    d.line([14, 160, W - 14, 160], fill=INK, width=3)
    x, y = 14, 165
    for name, n in REGIONS_STRIP:
        c = REGION_COLORS[name]
        label = "%s %d" % (name, n)
        f = F("Archivo-Bold.ttf", 13)
        tw = d.textlength(label, font=f)
        d.rectangle([x, y, x + tw + 14, y + 19], fill=c)
        d.text((x + 7, y + 2), label, font=f, fill=(255, 255, 255))
        x += tw + 22
    y = 188
    d.rectangle([14, y, W - 14, y + 24], fill=LIGHT)
    x = 22
    tf, ef = F("Archivo-Bold.ttf", 12), F("Archivo.ttf", 12)
    for t, ev in TIMELINE:
        d.text((x, y + 5), t, font=tf, fill=CORAL)
        x += d.textlength(t, font=tf) + 5
        d.text((x, y + 5), ev, font=ef, fill=INK_DARK)
        x += d.textlength(ev, font=ef) + 18
    return 218


def card(d, x, y, w, h, c, title_size=28, band_h=22):
    num, loc, region, chip, cat, title, facts, source, scene = c
    rc = REGION_COLORS[region]
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.rectangle([x, y, x + w, y + 16], fill=rc)
    lf = F("Archivo-Bold.ttf", 12)
    d.text((x + 6, y + 2), "%d · %s" % (num, loc), font=lf, fill=(255, 255, 255))
    sf = F("Archivo.ttf", 10)
    d.text((x + w - 6 - d.textlength(source, font=sf), y + 3), source, font=sf,
           fill=(255, 255, 255))
    draw_scene(d, x + 2, y + 18, w - 4, band_h, scene, rc)
    yy = y + 20 + band_h
    cf = F("Archivo-Bold.ttf", 11)
    cw = d.textlength(chip, font=cf) + 9
    d.rectangle([x + 6, yy, x + 6 + cw, yy + 14], fill=CORAL)
    d.text((x + 10, yy + 1), chip, font=cf, fill=(255, 255, 255))
    d.text((x + 13 + cw, yy + 1), "%s · %s" % (region, cat), font=cf, fill=GREY)
    yy += 17
    tf = F("Archivo-Bold.ttf", title_size)
    for ln in fit_lines(d, title, tf, w - 12, 2):
        d.text((x + 6, yy), ln, font=tf, fill=INK_DARK)
        yy += title_size + 2
    ff = F("Archivo.ttf", 15)
    for ln in fit_lines(d, facts, ff, w - 12, 2):
        d.text((x + 6, yy), ln, font=ff, fill=(40, 40, 40))
        yy += 18


def numbers_strip(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    d.text((x + 10, y + 4), "THE DAY IN NUMBERS", font=F("Archivo-Bold.ttf", 13),
           fill=(255, 190, 120))
    cw = (w - 16) // 6
    bf = F("Archivo-Bold.ttf", 23)
    lf = F("Archivo.ttf", 10)
    for i, (big, small) in enumerate(NUMBERS):
        cx = x + 12 + i * cw
        d.text((cx, y + 20), big, font=bf, fill=(255, 255, 255))
        d.text((cx, y + h - 13), small, font=lf, fill=(200, 220, 235))


def datecheck_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.rectangle([x, y, x + w, y + 17], fill=RED)
    d.text((x + 7, y + 2), "DATE CHECK — checked and left out: not 23 November news",
           font=F("Archivo-Bold.ttf", 12), fill=(255, 255, 255))
    f = F("Archivo.ttf", 11)
    yy = y + 21
    for item in DATECHECK:
        for ln in fit_lines(d, "· " + item, f, w - 14, 1):
            d.text((x + 7, yy), ln, font=f, fill=(60, 20, 20))
            yy += 13


def map_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 7, y + 3), "WHERE IT HAPPENED — pins = card numbers",
           font=F("Archivo-Bold.ttf", 11), fill=INK)
    rows = MAP_ROWS
    gh, gw = len(rows), len(rows[0])
    cell = min((w - 14) / gw, (h - 24) / gh)
    ox, oy = x + 7, y + 18
    for r, row in enumerate(rows):
        for cc, ch in enumerate(row):
            if ch == "#":
                px, py = ox + cc * cell, oy + r * cell
                d.ellipse([px, py, px + cell * 0.85, py + cell * 0.85],
                          fill=(170, 195, 210))
    pf = F("Archivo-Bold.ttf", 9)
    for num, (lon, lat) in PINS.items():
        px = ox + (lon + 168) / 336.0 * gw * cell
        py = oy + (78 - lat) / 148.0 * gh * cell
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=CORAL)
        s = str(num)
        d.text((px - d.textlength(s, font=pf) / 2, py - 5), s, font=pf,
               fill=(255, 255, 255))


def also_flow(d, x, y, w):
    d.text((x, y), "ALSO ON MONDAY — STORIES 14–38",
           font=F("Archivo-Bold.ttf", 13), fill=INK)
    d.line([x, y + 17, x + w, y + 17], fill=CORAL, width=2)
    nf, f = F("Archivo-Bold.ttf", 13), F("Archivo.ttf", 13)
    cx, cy = x, y + 22
    for num, t in ALSO:
        seg = "%d " % num
        sw = d.textlength(seg, font=nf)
        tw = d.textlength(t, font=f)
        if cx + sw + tw > x + w:
            cx, cy = x, cy + 16
        d.text((cx, cy), seg, font=nf, fill=CORAL)
        d.text((cx + sw, cy), t, font=f, fill=(30, 30, 30))
        cx += sw + tw
        sep = "  ·  "
        d.text((cx, cy), sep, font=f, fill=GREY)
        cx += d.textlength(sep, font=f)
    return cy + 16


def footer_block(d, y):
    f = F("Archivo.ttf", 11)
    bf = F("Archivo-Bold.ttf", 11)
    d.text((14, y), "HOW SURE:", font=bf, fill=INK)
    x = 14 + d.textlength("HOW SURE: ", font=bf)
    txt = ("REPORTED = carried by a named wire or broadcaster · CLAIM = one "
           "side's account, labelled as such · ONGOING = still developing · "
           "OFFICIAL / ON RECORD = said by the body or person named.")
    for ln in fit_lines(d, txt, f, W - 14 - x, 1):
        d.text((x, y), ln, font=f, fill=(40, 40, 40))
    d.text((14, y + 14),
           "Every story happened, or was first reported, on Monday 23 November "
           "2026. Contested claims are attributed. · Original drawings.",
           font=f, fill=(40, 40, 40))


def layout_a():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = header_block(d)
    widths = [396, 292, 292]
    x = 14
    for i, wd in enumerate(widths):
        card(d, x, y, wd, 146, CARDS[i], title_size=30 if i == 0 else 28,
             band_h=24)
        x += wd + 8
    y += 152
    for r in range(3):
        x = 14
        for c in CARDS[3 + r * 3: 6 + r * 3]:
            card(d, x, y, 328, 122, c)
            x += 336
        y += 128
    # last row: card 13 + date check
    card(d, 14, y, 328, 122, CARDS[12])
    datecheck_box(d, 350, y, W - 350 - 14, 122)
    y += 128
    numbers_strip(d, 14, y, W - 28, 48)
    y += 54
    map_box(d, 14, y, 300, 96)
    also_flow(d, 326, y, W - 326 - 14)
    y += 102
    footer_block(d, y)
    return img


def layout_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = header_block(d)
    # left rail: numbers vertical
    d.rectangle([14, y, 264, y + 300], fill=INK)
    d.text((24, y + 8), "THE DAY IN NUMBERS", font=F("Archivo-Bold.ttf", 14),
           fill=(255, 190, 120))
    yy = y + 34
    for big, small in NUMBERS:
        d.text((24, yy), big, font=F("Archivo-Bold.ttf", 24), fill=(255, 255, 255))
        d.text((24, yy + 27), small, font=F("Archivo.ttf", 11),
               fill=(200, 220, 235))
        yy += 44
    map_box(d, 14, y + 308, 250, 200)
    # right: lead wide + pair
    card(d, 272, y, 738, 130, CARDS[0], title_size=30, band_h=24)
    y2 = y + 136
    card(d, 272, y2, 365, 122, CARDS[1])
    card(d, 645, y2, 365, 122, CARDS[2])
    y2 += 128
    for r in range(3):
        x = 272
        for c in CARDS[3 + r * 3: 6 + r * 3]:
            card(d, x, y2, 240, 122, c, title_size=24)
            x += 248
        y2 += 128
    card(d, 272, y2, 240, 122, CARDS[12], title_size=24)
    datecheck_box(d, 520, y2, W - 520 - 14, 122)
    y = y2 + 128
    also_flow(d, 14, y, W - 28)
    footer_block(d, y + 78)
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun16/entry.png"
    img = layout_a() if variant == "A" else layout_b()
    img.save(out, optimize=True)
    print(out, img.size)
