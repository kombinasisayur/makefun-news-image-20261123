#!/usr/bin/env python3
"""THE HARBOUR POST — NI23 G4 entry builder (akun16, @kombinasisayur0566).

One 1024x1024 front page for Monday 23 November 2026, drawn with PIL
in a flat harbour palette: white paper, sea-blue ink, coral accent.
Layout A: lead trio, three mini rows, a closing row with the DATE
CHECK box, the numbers box and a dotted_map, then ALSO ON briefs and
the HOW SURE footer. Layout B moves the numbers into a left rail.
All story data comes from the locked ni23 pool; contested claims are
framed as claims in the headlines themselves.
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

# grid: (num, region, topic, src, head, deck, kind)
grid = [
    (1, "N. AMERICA", "INVESTIGATION", "AP wire",
     "FBI Probes Hack of Its Justice Database",
     "Agents probe a suspected hack of the FBI justice database, AP reports.",
     "database"),
    (2, "MIDDLE EAST", "WAR AT SEA", "AP live",
     "Tankers Burn in the Strait of Hormuz",
     "Tankers ablaze as the Iran-US war widens into the Gulf.",
     "ship"),
    (3, "MIDDLE EAST", "WAR", "AFP / AP",
     "IRGC Claims Radars Hit in Bahrain",
     "Tehran says 2 Patriot radars destroyed; Washington has not confirmed it.",
     "radar"),
    (4, "EUROPE", "CLIMATE", "BBC / AP",
     "COP31 Ends Without a Deal",
     "The final Turkish draft omits 'fossil fuels'; no pact in Antalya.",
     "leaf"),
    (5, "EUROPE", "WAR", "BBC",
     "Kyiv Boy, 7, Pulled Alive From Rubble",
     "Freed after hours under Kyiv debris; 6 killed in the Russian strike.",
     "rubble"),
    (6, "EUROPE", "WAR", "JagranJosh",
     "14 Missing in Kyiv, Zelenskiy Says",
     "A Russian drone hit a Kyiv block; 14 missing, Zelenskiy says.",
     "drone"),
    (7, "EUROPE", "SEA", "BBC",
     "Russian Ship Still Burns Off Finland",
     "Still burns after an attack in the Gulf of Finland.",
     "shipfire"),
    (8, "N. AMERICA", "POLITICS", "BBC",
     "Democrats Take the House, 258-173",
     "Largest majority since 1992, sealed in North Carolina.",
     "ballot"),
    (9, "S. ASIA", "CRICKET", "ObserverVoice",
     "India Declare on a Record 720/9",
     "Highest Test total made in New Zealand, at Wellington.",
     "cricket"),
    (10, "GLOBAL", "MONEY", "ObserverVoice",
     "Gold Slides to $3,538 an Ounce",
     "Down $2,000+ from the $5,595 record of 2026.",
     "gold"),
    (11, "SE ASIA", "LAW", "Guardian / NYT",
     "ICJ Rules Myanmar Guilty of Genocide",
     "Rohingya campaign of 2017; 700,000+ fled Myanmar.",
     "gavel"),
    (12, "N. AMERICA", "SAFETY", "BBC",
     "Army to Detonate Explosives in Iowa",
     "The US Army defies a court order over explosives in Iowa.",
     "blast"),
]

LOC = {1: "WASHINGTON · USA", 2: "STRAIT OF HORMUZ", 3: "BAHRAIN",
       4: "ANTALYA · TÜRKIYE", 5: "KYIV · UKRAINE", 6: "KYIV REGION",
       7: "GULF OF FINLAND", 8: "WASHINGTON · USA", 9: "WELLINGTON · NZ",
       10: "GLOBAL MARKETS", 11: "THE HAGUE", 12: "IOWA · USA"}

CHIP = {1: "OFFICIAL", 2: "REPORTED", 3: "CLAIM", 4: "OFFICIAL",
        5: "REPORTED", 6: "ON RECORD", 7: "ONGOING", 8: "CONFIRMED",
        9: "REPORTED", 10: "REPORTED", 11: "OFFICIAL", 12: "REPORTED"}

NUMS = [
    ("258-173", "US House split"),
    ("720/9", "India's record total"),
    ("$3,538", "gold per ounce"),
    ("14", "missing in Kyiv"),
    ("50", "missing, fire update"),
    ("₹28,000 cr", "Tata pipe-unit sale"),
]

TL = [
    ("00:02 UTC", "AI talks go on"),
    ("02:00 UTC", "Sydney: COP31 reaction"),
    ("MORNING", "FBI hack probe opens"),
    ("MIDDAY", "ICJ: Myanmar guilty"),
    ("EVENING", "House confirmed 258-173"),
]

BRIEFS = [
    "14. Houthi missile downed over Saudi west",
    "15. Swimmer crosses the Strait of Hormuz",
    "16. UN talks on killer AI to continue",
    "17. US releases more UFO footage files",
    "18. Albanese: COP31 failure stings",
    "19. Ship towed after Gulf of Finland attack",
    "20. UK-EU Brexit reset called a landmark",
    "21. Thousands march in Lisbon on living costs",
    "22. Myanmar junta calls ASEAN ruling unfair",
    "23. Escaped lion frightens a Turkish town",
    "24. Nepal PM Shah meets Modi in Delhi",
    "25. India and Bulgaria talk IMEC and Black Sea",
    "26. Guru Nanak Jayanti marked across India",
    "27. UP runs air-raid drills in 75 districts",
    "28. Indonesia factory fire update: 7 found, 50 missing",
    "29. NZ 119/2 as India chase a famous win",
    "30. India win the ODI series in NZ, 3-2",
    "31. Anupama defends her IBSF snooker crown",
    "32. World Chess Championship draws fans",
    "33. Rajya Sabha MP Wadkute dies in Delhi",
    "34. Kota pilgrim bus crash kills 9",
    "35. Tata Steel pipe unit sold, 28,000 crore rupees",
    "36. SpiceJet pilots seek audit; IndiGo holds 65.9%",
    "37. Modi opens an AI centre at IIT Patna",
    "38. Trump attacks Schumer over Dem push",
    "39. Miley Cyrus marries Maxx Morando in California",
    "40. Alcaraz beats Zverev in Turin for the ATP title",
]

# short drawn titles for the ALSO ON index (same stories as BRIEFS)
ALSO_DRAW = [
    (14, "Houthi missile downed"), (15, "Swimmer crosses Hormuz"),
    (16, "UN: killer-AI talks go on"), (17, "US releases UFO files"),
    (18, "Albanese: COP31 stings"), (19, "Ship towed off Finland"),
    (20, "UK-EU reset: 'landmark'"), (21, "Lisbon marches on costs"),
    (22, "Myanmar: ASEAN 'unfair'"), (23, "Escaped lion scares town"),
    (24, "Nepal's Shah meets Modi"), (25, "India-Bulgaria IMEC talks"),
    (26, "Guru Nanak Jayanti"), (27, "UP drills: 75 districts"),
    (28, "Fire: 7 found, 50 missing"), (29, "NZ 119/2; India chase"),
    (30, "India win ODI series 3-2"), (31, "Anupama's snooker crown"),
    (32, "World Chess draws fans"), (33, "MP Wadkute dies, Delhi"),
    (34, "Kota bus crash kills 9"), (35, "Tata sale: 28,000 cr"),
    (36, "IndiGo: 65.9% of skies"), (37, "Modi opens Patna AI hub"),
    (38, "Trump attacks Schumer"), (39, "Miley Cyrus marries Morando"),
    (40, "Alcaraz beats Zverev"),
]

dc = ("Xi-Trump-Putin summit - 19 Nov 2026 · Russian missiles fell in Poland - 20 Nov 2026 · "
      "Paolo Bulgari died - reported 22 Nov 2026 · Kim Jong-un 'security, not supremacy' - 22 Nov 2026 · "
      "Bolsonaro stable in ICU - 22 Nov 2026 · S. Korea education minister quit - first reported 22 Nov 2026 · "
      "Indonesia candy-factory fire itself - 22 Nov 2026 (only its 23 Nov toll update is today's news)")

REGIONS_STRIP = [("EUROPE", 10), ("S. ASIA", 12), ("N. AMERICA", 6),
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
        10: (-74, 40), 11: (4, 52), 12: (-93, 42)}


def fb(n):
    return ImageFont.truetype(FONTS + "Archivo-Bold.ttf", n)


def fr(n):
    return ImageFont.truetype(FONTS + "Archivo.ttf", n)


def fsr(n):
    return ImageFont.truetype(FONTS + "Archivo.ttf", n)


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


def draw_scene(d, x, y, w, h, scene, color):
    d.rectangle([x, y, x + w, y + h], fill=color)
    cx, cy = x + w // 2, y + h // 2
    wh = (255, 255, 255)
    gold = (255, 200, 70)
    s = h / 40.0

    def P(dx, dy):
        return (cx + dx * s, cy + dy * s)

    if scene in ("ship", "shipfire"):
        d.polygon([P(-24, 3), P(24, 3), P(17, 11), P(-17, 11)], fill=wh)
        d.rectangle([cx - 11 * s, cy - 4 * s, cx + 7 * s, cy + 3 * s], fill=wh)
        if scene == "shipfire":
            d.polygon([P(-4, -16), P(3, -6), P(-8, -6)], fill=gold)
            d.polygon([P(8, -12), P(13, -5), P(4, -5)], fill=gold)
    elif scene == "database":
        d.ellipse([cx - 14 * s, cy - 10 * s, cx + 14 * s, cy - 2 * s], outline=wh, width=2)
        d.rectangle([cx - 14 * s, cy - 10 * s, cx + 14 * s, cy + 8 * s], outline=wh, width=2)
        d.ellipse([cx - 14 * s, cy, cx + 14 * s, cy + 8 * s], outline=wh, width=2)
    elif scene == "radar":
        d.line([P(-16, 10), P(3, -10)], fill=wh, width=3)
        d.arc([cx - 2 * s, cy - 16 * s, cx + 25 * s, cy + 11 * s], 200, 330, fill=wh, width=3)
        d.arc([cx + 4 * s, cy - 21 * s, cx + 35 * s, cy + 11 * s], 200, 330, fill=gold, width=2)
    elif scene == "leaf":
        d.ellipse([cx - 13 * s, cy - 10 * s, cx + 12 * s, cy + 10 * s], fill=wh)
        d.line([P(-11, 8), P(13, -10)], fill=color, width=2)
    elif scene == "rubble":
        d.polygon([P(-22, 10), P(-6, -5), P(4, 10)], outline=wh, width=3)
        d.polygon([P(-3, 10), P(10, -10), P(22, 10)], outline=wh, width=3)
        d.ellipse([cx - 3 * s, cy - 2 * s, cx + 4 * s, cy + 5 * s], fill=gold)
    elif scene == "drone":
        d.rectangle([cx - 13 * s, cy - 3 * s, cx + 13 * s, cy + 3 * s], fill=wh)
        for dx in (-18, 18):
            d.ellipse([cx + (dx - 5) * s, cy - 10 * s, cx + (dx + 5) * s, cy - 3 * s], outline=wh, width=2)
            d.ellipse([cx + (dx - 5) * s, cy + 3 * s, cx + (dx + 5) * s, cy + 10 * s], outline=wh, width=2)
    elif scene == "ballot":
        d.rectangle([cx - 15 * s, cy - 5 * s, cx + 15 * s, cy + 11 * s], outline=wh, width=3)
        d.rectangle([cx - 6 * s, cy - 11 * s, cx + 6 * s, cy - 3 * s], fill=wh)
        d.line([P(-8, 2), P(-3, 8)], fill=gold, width=3)
        d.line([P(-3, 8), P(9, -1)], fill=gold, width=3)
    elif scene == "cricket":
        d.polygon([P(-13, -11), P(-6, -10), P(2, 10), P(-5, 11)], fill=wh)
        d.ellipse([cx + 6 * s, cy - 2 * s, cx + 17 * s, cy + 9 * s], fill=gold)
    elif scene == "gold":
        for i, (dx, dy) in enumerate([(-16, 3), (2, 3), (-7, -6)]):
            d.polygon([P(dx, dy), P(dx + 15, dy), P(dx + 12, dy - 6), P(dx + 3, dy - 6)],
                      fill=gold if i == 2 else wh)
    elif scene == "gavel":
        d.rectangle([cx - 16 * s, cy + 6 * s, cx + 16 * s, cy + 10 * s], fill=wh)
        d.polygon([P(-3, -11), P(13, 3), P(6, 8), P(-10, -6)], fill=wh)
        d.line([P(8, 1), P(18, 11)], fill=wh, width=3)
    elif scene == "blast":
        for ang in range(0, 360, 45):
            x1 = cx + 4 * s * math.cos(math.radians(ang))
            y1 = cy + 4 * s * math.sin(math.radians(ang))
            x2 = cx + 15 * s * math.cos(math.radians(ang))
            y2 = cy + 15 * s * math.sin(math.radians(ang))
            d.line([x1, y1, x2, y2], fill=gold, width=3)
        d.ellipse([cx - 4 * s, cy - 4 * s, cx + 4 * s, cy + 4 * s], fill=wh)
    elif scene == "trophy":
        d.polygon([P(-10, -11), P(10, -11), P(10, -2), P(4, 3), P(-4, 3), P(-10, -2)], fill=gold)


def _card_base(d, x, y, w, c):
    num, region, topic, src, head, deck, kind = c
    rc = REGION_COLORS[region]
    d.rectangle([x, y, x + w, y + 15], fill=rc)
    lf = fb(12)
    d.text((x + 6, y + 1), "%d · %s" % (num, LOC[num]), font=lf, fill=(255, 255, 255))
    sf = fr(10)
    srctxt = "Source: " + src
    d.text((x + w - 6 - d.textlength(srctxt, font=sf), y + 2), srctxt, font=sf,
           fill=(255, 255, 255))
    draw_scene(d, x + 2, y + 17, w - 4, 14, kind, rc)
    yy = y + 33
    cf = fb(11)
    chip = CHIP[num]
    cw = d.textlength(chip, font=cf) + 9
    d.rectangle([x + 6, yy, x + 6 + cw, yy + 14], fill=CORAL)
    d.text((x + 10, yy + 1), chip, font=cf, fill=(255, 255, 255))
    d.text((x + 13 + cw, yy + 1), "%s · %s" % (region, topic), font=cf, fill=GREY)
    return yy + 16


def lead(d, x, y, w, h, c):
    num, region, topic, src, head, deck, kind = c
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    yy = _card_base(d, x, y, w, c)
    tf = fb(30)
    for ln in fit_lines(d, head, tf, w - 12, 2):
        d.text((x + 6, yy), ln, font=tf, fill=INK_DARK)
        yy += 28
    ff = fr(15)
    for ln in fit_lines(d, deck, ff, w - 12, 2):
        d.text((x + 6, yy), ln, font=ff, fill=(40, 40, 40))
        yy += 16


def mini(d, x, y, w, h, c):
    num, region, topic, src, head, deck, kind = c
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    yy = _card_base(d, x, y, w, c)
    tf = fb(28)
    for ln in fit_lines(d, head, tf, w - 12, 2):
        d.text((x + 6, yy), ln, font=tf, fill=INK_DARK)
        yy += 26
    ff = fr(15)
    for ln in fit_lines(d, deck, ff, w - 12, 2):
        d.text((x + 6, yy), ln, font=ff, fill=(40, 40, 40))
        yy += 16


def header_block(d):
    d.rectangle([0, 0, W, 24], fill=INK)
    d.text((14, 4), "THE HARBOUR POST", font=fb(15), fill=(255, 255, 255))
    kick = "39 STORIES · 7 REGIONS · EVERY ONE FROM 23 NOVEMBER 2026"
    kf = fb(13)
    d.text((W - 14 - d.textlength(kick, font=kf), 5), kick, font=kf,
           fill=(255, 190, 120))
    d.text((14, 28), "THE HARBOUR POST", font=F("PlayfairDisplay-Black.ttf", 26),
           fill=INK)
    sub = "FBI probe · Hormuz tankers burn · COP31 ends with no deal"
    sf = fb(15)
    d.text((W - 14 - d.textlength(sub, font=sf), 36), sub, font=sf, fill=CORAL)
    d.text((14, 50), "Monday 23 November 2026",
           font=F("PlayfairDisplay-Black.ttf", 72), fill=INK_DARK)
    d.line([14, 130, W - 14, 130], fill=INK, width=3)
    x, y = 14, 135
    for name, n in REGIONS_STRIP:
        c = REGION_COLORS[name]
        label = "%s %d" % (name, n)
        f = fb(13)
        tw = d.textlength(label, font=f)
        d.rectangle([x, y, x + tw + 14, y + 19], fill=c)
        d.text((x + 7, y + 2), label, font=f, fill=(255, 255, 255))
        x += tw + 22
    y = 158
    d.rectangle([14, y, W - 14, y + 22], fill=LIGHT)
    x = 22
    tf, ef = fb(12), fr(12)
    for t, ev in TL:
        d.text((x, y + 4), t, font=tf, fill=CORAL)
        x += d.textlength(t, font=tf) + 5
        d.text((x, y + 4), ev, font=ef, fill=INK_DARK)
        x += d.textlength(ev, font=ef) + 18
    return 186


def numbers_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=INK)
    d.text((x + 10, y + 6), "THE DAY IN NUMBERS", font=fb(14),
           fill=(255, 190, 120))
    cw = (w - 20) // 2
    ch = (h - 30) // 3
    bf = fb(20)
    lf = fr(10)
    for i, (big, small) in enumerate(NUMS):
        cx = x + 12 + (i % 2) * cw
        cy = y + 28 + (i // 2) * ch
        d.text((cx, cy), big, font=bf, fill=(255, 255, 255))
        d.text((cx, cy + 22), small, font=lf, fill=(200, 220, 235))


def datecheck_box(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RED, width=2)
    d.rectangle([x, y, x + w, y + 17], fill=RED)
    d.text((x + 7, y + 2), "DATE CHECK — checked and left out: not 23 November news",
           font=fb(12), fill=(255, 255, 255))
    f = fr(11)
    yy = y + 22
    for item in dc.split(" · "):
        for ln in fit_lines(d, "· " + item, f, w - 14, 2):
            d.text((x + 7, yy), ln, font=f, fill=(60, 20, 20))
            yy += 13


def dotted_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    d.text((x + 7, y + 3), "DOTTED MAP — marks numbered by card",
           font=fb(11), fill=INK)
    rows = MAP_ROWS
    gh, gw = len(rows), len(rows[0])
    cell = min((w - 14) / gw, (h - 22) / gh)
    ox = x + (w - gw * cell) / 2
    oy = y + 18
    for r, row in enumerate(rows):
        for cc, ch in enumerate(row):
            if ch == "#":
                px, py = ox + cc * cell, oy + r * cell
                d.ellipse([px, py, px + cell * 0.85, py + cell * 0.85],
                          fill=(170, 195, 210))
    pf = fb(8)
    for num, (lon, lat) in PINS.items():
        px = ox + (lon + 168) / 336.0 * gw * cell
        py = oy + (78 - lat) / 148.0 * gh * cell
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=CORAL)
        s = str(num)
        d.text((px - d.textlength(s, font=pf) / 2, py - 4), s, font=pf,
               fill=(255, 255, 255))


def also_cols(d, x, y, w, cols=5):
    d.text((x, y), "ALSO ON MONDAY — STORIES 14–40",
           font=fb(13), fill=INK)
    d.line([x, y + 17, x + w, y + 17], fill=CORAL, width=2)
    colw = w // cols
    per = (len(ALSO_DRAW) + cols - 1) // cols
    f = fsr(13)
    nf = fb(13)
    for i, (num, t) in enumerate(ALSO_DRAW):
        cx = x + (i // per) * colw
        cy = y + 22 + (i % per) * 13
        d.text((cx, cy), "%d" % num, font=nf, fill=CORAL)
        for ln in fit_lines(d, t, f, colw - 24, 1):
            d.text((cx + 22, cy), ln, font=f, fill=(30, 30, 30))
    return y + 22 + per * 13


def footer_block(d, y):
    f = fr(11)
    bf = fb(11)
    d.text((14, y), "HOW SURE:", font=bf, fill=INK)
    x = 14 + d.textlength("HOW SURE: ", font=bf)
    txt = ("REPORTED = named wire or broadcaster · CLAIM = one side's account, "
           "labelled · ONGOING = still developing · OFFICIAL / ON RECORD = "
           "said by the body or person named.")
    for ln in fit_lines(d, txt, f, W - 14 - x, 1):
        d.text((x, y), ln, font=f, fill=(40, 40, 40))
    d.text((14, y + 13),
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
        lead(d, x, y, wd, 140, grid[i])
        x += wd + 8
    y += 146
    for r in range(3):
        x = 14
        for c in grid[3 + r * 3: 6 + r * 3]:
            mini(d, x, y, 328, 134, c)
            x += 336
        y += 140
    datecheck_box(d, 14, y, 380, 130)
    numbers_box(d, 402, y, 300, 130)
    dotted_map(d, 710, y, 300, 130)
    y += 136
    y = also_cols(d, 14, y, W - 28)
    footer_block(d, y + 3)
    return img


def layout_b():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = header_block(d)
    # left rail: numbers + map + date check stacked
    numbers_box(d, 14, y, 250, 250)
    dotted_map(d, 14, y + 258, 250, 170)
    datecheck_box(d, 14, y + 436, 250, 200)
    # right: lead wide, pair, then minis in pairs
    lead(d, 272, y, 738, 128, grid[0])
    y2 = y + 134
    lead(d, 272, y2, 365, 124, grid[1])
    lead(d, 645, y2, 365, 124, grid[2])
    y2 += 130
    rest = grid[3:]
    for r in range(3):
        x = 272
        for c in rest[r * 3:(r + 1) * 3]:
            mini(d, x, y2, 240, 124, c)
            x += 248
        y2 += 130
    y = y2 + 2
    y = also_cols(d, 272, y, W - 272 - 14, cols=3)
    footer_block(d, y + 3)
    return img


if __name__ == "__main__":
    variant = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ni23g4-akun16/entry.png"
    img = layout_a() if variant == "A" else layout_b()
    img = img.quantize(colors=256, method=Image.MEDIANCUT)
    img.save(out, optimize=True, compress_level=9)
    print(out, img.size)
