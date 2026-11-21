#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up Saturday 21 November 2026.

35 sourced stories across 8 regions: 3 illustrated leads, 6 illustrated
secondary stories, 26 numbered briefs, plus a stat strip, a region tally,
a real world map with numbered pins, a UTC timeline, a markets strip and
a date check. Every story is a verified 21 Nov 2026 fact (events that
happened, or were first reported, on that day) with a named source.

The design follows the model Ale approved: the illustrated 20 Nov front
page (stat strip, tally bar, drawn lead scenes, illustrated tiles, world
map with pins, briefs, date check).

Deterministic: fixed text, fixed geometry, no randomness, no clock, no
network. Run: python3 generate.py  ->  writes news.png next to this file.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 24                      # page margin
CW = W - 2 * M              # content width = 976
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (190, 26, 26)
DARKRED = (140, 20, 20)
BLUE = (20, 55, 110)
NAVY = (13, 27, 48)
GREY = (96, 96, 96)
FAINT = (205, 199, 184)
GOLD = (255, 210, 120)
MAP_BG = (196, 216, 232)
LAND = (203, 188, 148)
LAND_EDGE = (150, 132, 96)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")

EDITION = "Saturday 21 November 2026"
SOURCES = ("Reuters", "AP", "AFP", "BBC", "Al Jazeera", "UKMTO", "USGS", "WHO",
           "ATP Tour")


def font(path, size):
    return ImageFont.truetype(path, size)


class Page:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def text(self, x, y, s, f, fill=INK, anchor="la"):
        self.d.text((x, y), s, font=f, fill=fill, anchor=anchor)

    def width(self, s, f):
        return self.d.textlength(s, font=f)

    def wrap(self, s, f, max_w):
        """Word wrap; never splits a word across lines."""
        lines, cur = [], ""
        for word in s.split():
            trial = (cur + " " + word).strip()
            if self.width(trial, f) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def rule(self, x0, x1, y, color=INK, width=2):
        self.d.line([(x0, y), (x1, y)], fill=color, width=width)

    def chip(self, x, y, s, size=14, bg=RED, fg=(255, 255, 255), pad=7):
        """Red label chip with white bold text; returns chip width."""
        f = font(SANS_B, size)
        w = int(self.width(s, f)) + 2 * pad
        self.d.rectangle([x, y, x + w, y + size + 9], fill=bg)
        self.text(x + pad, y + 3, s, f, fg)
        return w

    def tag(self, x, y, s, size=9):
        """Small dark source tag, bottom-left style of the model scenes."""
        f = font(SANS_B, size)
        w = int(self.width(s, f)) + 10
        self.d.rectangle([x, y, x + w, y + size + 7], fill=(24, 24, 24))
        self.text(x + 5, y + 3, s, f, (240, 240, 240))
        return w

    def numdot(self, x, y, num, r=9, bg=BLUE):
        """Numbered circle marker, as used by kickers and map pins."""
        self.d.ellipse([x - r, y - r, x + r, y + r], fill=bg,
                       outline=(255, 255, 255), width=2)
        self.text(x, y - 1, str(num), font(SANS_B, r), (255, 255, 255), "ma")

    def kicker(self, x, y, num, label, size=12):
        self.numdot(x + 9, y + 8, num)
        self.text(x + 24, y + 1, label, font(SANS_B, size), INK)
        return y + size + 8

    def headline(self, x, y, w, s, size=20, lh=23, max_lines=2):
        f = font(SERIF_B, size)
        lines = self.wrap(s, f, w)
        assert len(lines) <= max_lines, "headline too long: " + s
        for ln in lines:
            self.text(x, y, ln, f)
            y += lh
        return y

    def body(self, x, y, w, s, size=11, lh=14, max_lines=4):
        f = font(SANS, size)
        lines = self.wrap(s, f, w)
        assert len(lines) <= max_lines, "body too long: " + s[:40]
        for ln in lines:
            self.text(x, y, ln, f, (40, 40, 40))
            y += lh
        return y

    def save(self):
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
        self.img.save(out, optimize=True)
        print(out, os.path.getsize(out))


# ------------------------------------------------------------------ content
STATS = [
    ("148", "drones fired at Ukraine overnight; 87 jet-powered"),
    ("58", "injured at Kryvyi Rih, six of them children"),
    ("05:00", "GMT — first tanker hit off Khasab, Oman"),
    ("−5.3%", "Nasdaq's fall wipes out all of its 2026 gains"),
    ("128", "nations agree killer-robot rules in Geneva"),
    ("M6.7", "quake near Junín, Peru — 129 km deep, felt in Lima"),
]

TALLY = [
    ("Europe", 8, (36, 93, 171)),
    ("North America", 8, (0, 128, 128)),
    ("Asia", 7, (190, 26, 26)),
    ("Middle East", 5, (217, 119, 6)),
    ("Africa", 4, (90, 140, 60)),
    ("Lat. Am.", 1, (120, 80, 160)),
    ("Oceania", 1, (200, 170, 90)),
    ("Antarct.", 1, (90, 90, 90)),
]

LEADS = [
    dict(num=1, chip="KRYVYI RIH", sub="148 drones overnight",
         tag="Ukraine Air Force",
         kick="KRYVYI RIH, UKRAINE · WAR",
         head="Overnight blitz kills two in Kryvyi Rih",
         body="Russia fired three ballistic missiles and 148 drones at Ukraine "
              "overnight — 87 of them jet-powered. Two missiles struck near a "
              "restaurant in Kryvyi Rih, killing a boy of seven and a paramedic, "
              "20, and injuring 58. (Ukraine Air Force, UNITED24)"),
    dict(num=2, chip="HORMUZ", sub="First hit · 05:00 GMT",
         tag="UKMTO reports",
         kick="KHASAB, OMAN · GULF",
         head="Two tankers hit off Oman",
         body="Two tankers leaving the Strait of Hormuz were hit by "
              "unidentified projectiles off Khasab — one on the stern at "
              "05:00 GMT, one in the engine room at 05:50. No casualties. "
              "(UKMTO, Reuters, Al Jazeera)"),
    dict(num=3, chip="WALL ST ROUT", sub="Friday's close, New York",
         tag="Closing prices",
         kick="NEW YORK, USA · MARKETS",
         head="Wall St rout puts S&P and Dow in correction",
         body="US stocks plunged: Nasdaq −5.3% to 22,618, wiping out its 2026 "
              "gains; the S&P 500 fell 3.7% to 6,910. Nvidia fell 14% on an "
              "SEC probe report. (Reuters, AP)"),
]

TILES = [
    dict(num=4, chip="RIYADH: DOWNED", tag="Defence ministry",
         kick="RIYADH · GULF", art="riyadh",
         head="Houthi missiles downed over Riyadh",
         body="Saudi defences downed three Houthi missiles early on Saturday "
              "— a third straight day of alerts. No one was hurt. (Reuters, AFP)"),
    dict(num=5, chip="COP31: OVERTIME", tag="UN talks",
         kick="ANTALYA · CLIMATE", art="cop31",
         head="COP31 in overtime in fossil-fuel row",
         body="UN talks in Turkey ran past the Friday deadline after a draft "
              "dropped all mention of fossil fuels. (AP, BBC, Guardian)"),
    dict(num=6, chip="GENEVA: ROBOT RULES", tag="128 nations",
         kick="GENEVA · EUROPE", art="geneva",
         head="Killer-robot rules: 128 nations agree",
         body="Delegates agreed in Geneva to keep working on rules for lethal "
              "autonomous weapons, aiming at a 2028 accord. (Reuters)"),
    dict(num=7, chip="DENMARK: EXPELS", tag="Seven days to leave",
         kick="COPENHAGEN · EUROPE", art="denmark",
         head="Denmark to expel Russian attaché",
         body="Copenhagen gives the defence attaché seven days over an "
              "alleged plot against a rapper's concert. (AP, BBC)"),
    dict(num=8, chip="TURIN: SEMI-FINAL", tag="14:30 CET today",
         kick="TURIN · SPORT", art="turin",
         head="ATP Finals: Alcaraz v Shelton today",
         body="First semi-final at 14:30 CET; Alcaraz leads Shelton 4–1. "
              "Zverev faces Medvedev at 20:30. (ATP Tour, Flashscore)"),
    dict(num=9, chip="PERU: M6.7 QUAKE", tag="USGS · no deaths",
         kick="JUNÍN · QUAKES", art="peru",
         head="M6.7 quake shakes Peru, felt in Lima",
         body="The quake struck near Junín at 00:09 GMT, about 129 km deep. "
              "It rattled Lima; no deaths were reported. (AFP, USGS, IGP)"),
]

TIMELINE = [
    ("00:09", "M6.7 quake shakes Junín, Peru; felt in Lima"),
    ("05:00", "First tanker hit off Khasab, Oman"),
    ("06:00", "Kyiv: water down in 5 districts after strikes"),
    ("10:46", "COP31 deadlock reported from Antalya"),
    ("13:30", "Alcaraz–Shelton semi-final starts in Turin"),
]

MARKETS = ("MARKETS — S&P 500 −3.7% · 6,910  |  Nasdaq −5.3% · 22,618  |  "
           "Dow −1.9% · 48,147  |  Gold $3,539  |  Brent $92.49  |  "
           "Bitcoin ~$57,200")

BRIEFS = [
    "WASHINGTON: FBI probes breach of its NCIC police database. (CNN)",
    "WASHINGTON: Trump orders contractors to report Congress requests. (Reuters)",
    "WASHINGTON: 2nd judge blocks Trump's 250-ft triumphal arch. (AP)",
    "SINALOA: Mexico captures cartel chief 'El Chapo Isidro'. (CNN)",
    "GAZA: Israeli drone strike kills 3 in Gaza City; 4th shot dead. (QNA)",
    "FLORIDA: 28 in of rain floods Brevard Co.; Palm Coast emergency. (WESH)",
    "EUROPE: Drones over Sigonella, Roissy-CDG airport. (Itamilradar/Actu.fr)",
    "KINSHASA: DR Congo Ebola at 11,613 cases, 5,678 deaths. (WHO)",
    "DHAKA: Paramilitary deployed as Hasina's return stirs tension. (Asia Times)",
    "AMERICAN SAMOA: US leases seabed for mining; court called it illegal. (BBC)",
    "MOROCCO: 10-year carbon deal with Norway; 2,000 MW renewables. (Monolith)",
    "BHUTAN: 20 GW more hydro and solar by 2040, over $26bn. (BBS)",
    "EGYPT: Targets 42% renewables share of power capacity. (Egypt Ind.)",
    "JAKARTA: Indonesia targets global carbon trade under Art. 6. (Antara)",
    "SRI LANKA: Extreme rain floods coastal city; drains vanish. (Monolith)",
    "S. AFRICA: 5,590 murders Jul–Sep, down 204 on last quarter. (Police)",
    "GENEVA: CERN finds first evidence of ultra-rare decay. (ScienceDaily)",
    "HAMBURG: Record X-ray laser flashes, about 0.04 nm. (DESY/XFEL)",
    "ANTARCTICA: Himalaya-tall ranges found under the ice. (One Turn)",
    "MONTANA: Blue sucker fish found to live over 100 years. (One Turn)",
    "GAZA: Aid groups say peace plan failing; 2m in under 130 sq km. (Al Jazeera)",
    "JIZAN: Two more Houthi missiles downed; power station targeted. (AFP)",
    "JAKARTA: IHSG −0.9% to 5,146 as Asia follows Wall St. (Traderforum)",
    "KAZAKHSTAN: $1.2bn in COP31 deals signed in Antalya. (Monolith)",
    "NEW DELHI: SCO forum calls climate change a 'threat' to civilisation. (Monolith)",
    "BERING SEA: Heatwave that killed 10bn crabs spawns hybrid crab. (Guardian)",
]
assert len(BRIEFS) == 26

DATECHECK = ("NOT SHOWN: Fri — Shenzhen declaration • ICJ Myanmar ruling • "
             "PIF Tower hit • Nikkei −5.1%.   NOT YET: ATP final (Sun) • "
             "COP31 deal • Zverev–Medvedev semi.")


# ------------------------------------------------------------- illustrations
def gradient(w, h, top, bot):
    """Vertical gradient canvas (deterministic, pure arithmetic)."""
    img = Image.new("RGB", (w, h), top)
    dr = ImageDraw.Draw(img)
    for yy in range(h):
        t = yy / max(1, h - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        dr.line([(0, yy), (w, yy)], fill=c)
    return img


def dash_curve(dr, p0, p1, p2, fill, step=7, r=2):
    """Dashed quadratic bezier (missile trails in the model)."""
    pts = []
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    for i in range(0, len(pts) - 1, step):
        x, y = pts[i]
        dr.ellipse([x - r, y - r, x + r, y + r], fill=fill)


def burst(dr, cx, cy, r, fill=(255, 170, 40)):
    """Explosion / interceptor burst star."""
    pts = []
    for i in range(16):
        ang = i * math.pi / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    dr.polygon(pts, fill=fill)
    dr.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
               fill=(255, 230, 150))


def scene_kryvyi(w, h):
    img = gradient(w, h, (9, 16, 36), (30, 48, 84))
    dr = ImageDraw.Draw(img)
    for i in range(46):  # stars, fixed arithmetic pattern
        x = (i * 73 + 19) % w
        y = (i * 37 + 11) % max(20, h - 52)
        dr.point((x, y), fill=(210, 220, 240))
    # missile trails arcing in from top right
    dash_curve(dr, (w - 18, 6), (w - 120, 2), (w - 150, h - 40), (255, 214, 130))
    dash_curve(dr, (w - 70, 2), (w - 190, 10), (w - 235, h - 38), (255, 190, 110))
    dash_curve(dr, (w - 8, 44), (w - 90, 40), (w - 96, h - 42), (255, 224, 160))
    # skyline silhouette
    base = h - 16
    bx = -4
    i = 0
    while bx < w:
        bw = 18 + (i * 29) % 26
        bh = 22 + (i * 41) % 30
        dr.rectangle([bx, base - bh, bx + bw, base], fill=(8, 11, 20))
        for k in range(3):  # lit windows
            wx = bx + 4 + (k * 17 + i * 7) % max(6, bw - 8)
            wy = base - bh + 5 + (k * 11 + i * 5) % max(6, bh - 10)
            dr.rectangle([wx, wy, wx + 2, wy + 3], fill=(255, 205, 110))
        bx += bw + 3
        i += 1
    dr.rectangle([0, base, w, h], fill=(5, 8, 15))  # ground / river band
    burst(dr, w - 150, base - 6, 13)
    burst(dr, w - 235, base - 4, 10, (255, 140, 50))
    burst(dr, w - 96, base - 5, 9, (255, 190, 80))
    return img


def tanker(dr, x, y, s, flip=False):
    """Side-view tanker silhouette; s = length scale."""
    hull = [(x, y), (x + 118 * s, y), (x + 106 * s, y + 13 * s),
            (x + 12 * s, y + 13 * s)]
    if flip:
        hull = [(2 * x + 118 * s - px, py) for px, py in hull]
    dr.polygon(hull, fill=(26, 28, 34))
    dr.rectangle([x + 8 * s, y - 3 * s, x + 112 * s, y], fill=(190, 40, 40))
    dr.rectangle([x + 78 * s, y - 16 * s, x + 96 * s, y - 3 * s],
                 fill=(225, 228, 232))                       # superstructure
    dr.rectangle([x + 98 * s, y - 13 * s, x + 104 * s, y - 3 * s],
                 fill=(60, 60, 66))                          # funnel
    for k in range(4):                                       # deck tanks
        dr.rectangle([x + (14 + k * 15) * s, y - 6 * s,
                      x + (24 + k * 15) * s, y - 3 * s], fill=(70, 74, 82))


def scene_hormuz(w, h):
    img = gradient(w, h, (126, 172, 205), (196, 220, 233))
    dr = ImageDraw.Draw(img)
    sea_y = int(h * 0.52)
    dr.rectangle([0, sea_y, w, h], fill=(33, 96, 138))
    for i in range(9):  # wave glints
        x = (i * 47 + 13) % (w - 30)
        y = sea_y + 8 + (i * 23) % max(10, h - sea_y - 14)
        dr.line([(x, y), (x + 14, y)], fill=(170, 205, 228), width=1)
    # Omani coast, top right — dry mountains above the strait
    dr.polygon([(w * 0.55, 0), (w, 0), (w, sea_y - 6), (w * 0.86, sea_y - 16),
                (w * 0.74, sea_y - 4), (w * 0.64, sea_y - 14), (w * 0.55, sea_y - 2)],
               fill=(186, 158, 112), outline=(150, 124, 84))
    dr.polygon([(0, sea_y + 2), (w * 0.16, sea_y - 8), (w * 0.3, sea_y + 4),
                (w * 0.2, sea_y + 12), (0, sea_y + 14)], fill=(172, 146, 104))
    tanker(dr, 26, sea_y + 26, 1.05)
    tanker(dr, w - 148, sea_y + 8, 0.72)
    # projectile trail to the big tanker's stern + burst
    dash_curve(dr, (6, 4), (70, 0), (30, sea_y + 22), (255, 240, 200), step=5, r=2)
    burst(dr, 30, sea_y + 24, 11)
    return img


def scene_wallst(w, h):
    img = gradient(w, h, (10, 15, 30), (16, 24, 44))
    dr = ImageDraw.Draw(img)
    for gx in range(0, w, 30):
        dr.line([(gx, 0), (gx, h)], fill=(30, 42, 66), width=1)
    for gy in range(8, h, 24):
        dr.line([(0, gy), (w, gy)], fill=(30, 42, 66), width=1)
    bars = [0.42, 0.5, 0.46, 0.6, 0.72, 0.86]
    for i, bh in enumerate(bars):  # descending red bars
        x0 = 14 + i * 27
        dr.rectangle([x0, h - 12 - bh * (h - 40), x0 + 18, h - 12],
                     fill=(120, 26, 30))
    pts = [(12, 18), (62, 32), (112, 28), (162, 48), (208, 60), (248, 78)]
    dr.line(pts, fill=(255, 60, 50), width=3)
    for px, py in pts:
        dr.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 120, 100))
    dr.polygon([(248, 78), (236, 74), (244, 64)], fill=(255, 60, 50))  # arrowhead
    f1 = font(SANS_B, 13)
    rows = [("S&P 500", "−3.7%"), ("Nasdaq", "−5.3%"), ("Dow", "−1.9%")]
    for i, (a, b) in enumerate(rows):
        yy = 14 + i * 24
        dr.rectangle([w - 122, yy - 3, w - 8, yy + 17], fill=(8, 12, 24))
        dr.text((w - 116, yy), a, font=f1, fill=(235, 238, 245))
        dr.text((w - 14, yy), b, font=f1, fill=(255, 90, 80), anchor="ra")
    return img


def tile_canvas(top, bot):
    return gradient(318, 56, top, bot)


def art_riyadh():
    img = tile_canvas((96, 70, 124), (206, 118, 66))
    dr = ImageDraw.Draw(img)
    bx = 0
    i = 0
    while bx < 318:
        bw = 22 + (i * 23) % 20
        bh = 12 + (i * 31) % 16
        if i == 3:
            bh = 40  # the tall tower
        dr.rectangle([bx, 56 - bh, bx + bw, 56], fill=(16, 14, 26))
        bx += bw + 4
        i += 1
    dash_curve(dr, (300, 2), (200, 0), (128, 26), (255, 230, 170), step=5, r=2)
    dash_curve(dr, (250, 0), (170, 4), (96, 30), (255, 210, 140), step=5, r=2)
    burst(dr, 128, 26, 8, (255, 240, 200))
    burst(dr, 96, 30, 6, (255, 240, 200))
    return img


def art_cop31():
    img = tile_canvas((96, 156, 205), (168, 205, 230))
    dr = ImageDraw.Draw(img)
    dr.ellipse([16, 6, 60, 50], fill=(52, 110, 180), outline=(30, 80, 140), width=2)
    dr.polygon([(24, 18), (34, 12), (40, 20), (32, 26), (24, 24)], fill=(96, 170, 90))
    dr.polygon([(38, 32), (50, 30), (52, 40), (42, 44), (36, 38)], fill=(96, 170, 90))
    dr.ellipse([238, 6, 282, 50], fill=(245, 245, 240), outline=(120, 120, 120), width=2)
    dr.line([(260, 28), (260, 13)], fill=(30, 30, 30), width=3)   # past the hour
    dr.line([(260, 28), (274, 33)], fill=(200, 30, 30), width=3)
    dr.text((159, 33), "+1 DAY", font=font(SANS_B, 14), fill=(178, 24, 24),
            anchor="ma")
    return img


def art_geneva():
    img = tile_canvas((66, 80, 100), (96, 112, 132))
    dr = ImageDraw.Draw(img)
    dr.rounded_rectangle([118, 10, 178, 48], 9, fill=(168, 178, 190),
                         outline=(40, 46, 56), width=2)
    dr.rectangle([143, 2, 147, 10], fill=(40, 46, 56))
    dr.ellipse([143, 0, 151, 6], fill=(255, 80, 70))
    dr.rectangle([128, 24, 142, 31], fill=(30, 200, 220))   # eyes
    dr.rectangle([154, 24, 168, 31], fill=(30, 200, 220))
    dr.line([(132, 41), (164, 41)], fill=(40, 46, 56), width=2)
    for i in range(8):  # gear, right side
        ang = i * math.pi / 4
        x = 262 + 15 * math.cos(ang)
        y = 28 + 15 * math.sin(ang)
        dr.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(140, 148, 160))
    dr.ellipse([248, 14, 276, 42], fill=(170, 178, 190), outline=(40, 46, 56), width=2)
    dr.ellipse([257, 23, 267, 33], fill=(66, 80, 100))
    return img


def art_denmark():
    img = Image.new("RGB", (318, 56), (198, 12, 48))
    dr = ImageDraw.Draw(img)
    dr.rectangle([86, 0, 104, 56], fill=(245, 245, 245))     # white cross
    dr.rectangle([0, 20, 318, 36], fill=(245, 245, 245))
    dr.rectangle([0, 0, 10, 56], fill=(60, 40, 30))           # flagpole
    for i in range(5):  # shading waves
        x = 40 + i * 58
        dr.line([(x, 0), (x - 12, 56)], fill=(170, 8, 40), width=7)
    dr.rectangle([86, 0, 104, 56], fill=(245, 245, 245))
    dr.rectangle([0, 20, 318, 36], fill=(245, 245, 245))
    return img


def art_turin():
    img = tile_canvas((40, 110, 70), (52, 130, 84))
    dr = ImageDraw.Draw(img)
    dr.polygon([(58, 6), (260, 6), (292, 50), (26, 50)], fill=(52, 96, 168))
    dr.polygon([(74, 12), (244, 12), (262, 44), (56, 44)], fill=(64, 116, 190),
               outline=(240, 240, 240), width=2)
    dr.line([(159, 12), (159, 44)], fill=(240, 240, 240), width=2)
    dr.rectangle([52, 24, 266, 30], fill=(20, 20, 20))       # net
    dash_curve(dr, (30, 4), (150, -14), (238, 20), (240, 240, 240), step=6, r=2)
    dr.ellipse([232, 16, 244, 28], fill=(214, 228, 60), outline=(150, 160, 30))
    return img


def art_peru():
    img = tile_canvas((168, 188, 205), (214, 222, 226))
    dr = ImageDraw.Draw(img)
    dr.polygon([(0, 44), (50, 16), (92, 38), (140, 8), (188, 34), (236, 14),
                (282, 36), (318, 22), (318, 56), (0, 56)], fill=(110, 100, 92))
    dr.polygon([(140, 8), (128, 20), (152, 20)], fill=(245, 248, 250))
    dr.polygon([(50, 16), (40, 26), (60, 26)], fill=(245, 248, 250))
    dr.polygon([(236, 14), (226, 24), (246, 24)], fill=(245, 248, 250))
    seis = [(8, 50), (44, 44), (80, 51), (116, 45), (152, 51), (188, 45),
            (224, 51), (260, 45), (296, 50), (316, 47)]
    dr.line(seis, fill=(200, 30, 30), width=2)
    for r in (5, 10, 15):
        dr.ellipse([70 - r, 30 - r, 70 + r, 30 + r], outline=(200, 30, 30), width=2)
    return img


TILE_ART = {"riyadh": art_riyadh, "cop31": art_cop31, "geneva": art_geneva,
            "denmark": art_denmark, "turin": art_turin, "peru": art_peru}

# ------------------------------------------------------------- world map
# Simplified continent outlines as (lon, lat) polygons — recognisable
# shapes in equirectangular projection, drawn like the model's map.
CONTINENTS = [
    # North America + Greenland
    [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-110, 68), (-100, 69),
     (-92, 69), (-88, 66), (-84, 66), (-80, 62), (-78, 58), (-72, 56),
     (-65, 52), (-66, 48), (-70, 45), (-74, 40), (-76, 36), (-79, 33),
     (-81, 30), (-81, 26), (-84, 29), (-89, 29), (-94, 29), (-97, 26),
     (-97, 21), (-94, 18), (-90, 15), (-86, 13), (-83, 9), (-79, 9),
     (-82, 14), (-86, 20), (-90, 21), (-92, 18), (-97, 16), (-102, 15),
     (-105, 19), (-108, 22), (-112, 28), (-117, 33), (-122, 37), (-124, 44),
     (-124, 48), (-130, 54), (-138, 59), (-150, 60), (-160, 58), (-166, 61)],
    [(-46, 60), (-38, 64), (-30, 68), (-22, 70), (-19, 74), (-25, 79),
     (-38, 81), (-52, 79), (-58, 75), (-56, 68), (-53, 63)],
    # South America
    [(-79, 9), (-75, 11), (-71, 12), (-64, 11), (-58, 8), (-52, 5),
     (-50, 0), (-44, -3), (-36, -6), (-35, -9), (-39, -14), (-40, -21),
     (-47, -25), (-52, -33), (-57, -38), (-62, -41), (-65, -45), (-67, -50),
     (-68, -54), (-71, -54), (-73, -47), (-73, -38), (-71, -31), (-70, -21),
     (-74, -15), (-77, -11), (-80, -5), (-80, 0), (-78, 3), (-79, 6)],
    # Africa
    [(-6, 35), (0, 36), (6, 37), (10, 37), (12, 34), (19, 32), (27, 31),
     (32, 31), (34, 27), (36, 23), (39, 20), (41, 16), (43, 12), (48, 11),
     (51, 12), (46, 6), (42, -1), (40, -8), (38, -16), (36, -22), (34, -27),
     (30, -31), (25, -34), (19, -35), (17, -31), (15, -26), (13, -18),
     (12, -11), (13, -5), (9, -1), (9, 4), (3, 6), (-3, 5), (-8, 5),
     (-13, 8), (-17, 14), (-17, 19), (-16, 24), (-14, 28), (-10, 31)],
    # Europe (with Scandinavia)
    [(-9, 37), (-9, 43), (-3, 44), (-1, 46), (-4, 48), (0, 49), (2, 51),
     (5, 53), (7, 54), (8, 56), (8, 57), (12, 56), (18, 56), (21, 55),
     (24, 58), (22, 60), (25, 61), (21, 64), (18, 62), (14, 60), (11, 59),
     (6, 58), (5, 60), (8, 63), (13, 67), (18, 69), (25, 71), (31, 70),
     (40, 68), (48, 68), (55, 67), (48, 64), (40, 62), (35, 58), (33, 52),
     (38, 48), (32, 46), (28, 45), (29, 41), (26, 40), (23, 36), (22, 38),
     (19, 40), (19, 42), (14, 42), (13, 45), (10, 44), (8, 44), (6, 43),
     (3, 42), (2, 39), (-1, 37), (-5, 36)],
    # Asia (Siberia, East & South-East Asia, India, Arabia)
    [(40, 48), (48, 46), (55, 47), (62, 50), (72, 52), (85, 55), (95, 58),
     (100, 63), (105, 66), (112, 68), (125, 70), (140, 71), (155, 70),
     (168, 67), (178, 66), (179, 63), (170, 61), (162, 60), (159, 55),
     (152, 51), (143, 50), (141, 45), (137, 40), (131, 38), (128, 39),
     (123, 37), (121, 32), (122, 29), (118, 25), (111, 21), (108, 16),
     (107, 10), (104, 7), (101, 7), (99, 11), (96, 15), (93, 16),
     (90, 22), (87, 21), (83, 18), (80, 14), (77, 8), (75, 11),
     (72, 18), (70, 22), (66, 25), (61, 25), (57, 26), (53, 26),
     (51, 29), (49, 29), (51, 25), (55, 24), (58, 23), (59, 22),
     (56, 19), (53, 17), (49, 14), (44, 13), (43, 12), (41, 15),
     (39, 20), (36, 27), (35, 31), (36, 36), (31, 36), (27, 37),
     (30, 40), (34, 44), (38, 47)],
    # Indonesia / New Guinea (simplified island groups)
    [(95, 5), (99, 1), (103, -3), (106, -6), (103, -5), (99, 0), (96, 3)],
    [(109, 1), (112, 4), (116, 6), (119, 3), (117, -2), (112, -3), (109, -1)],
    [(106, -6), (111, -7), (114, -8), (114, -9), (107, -8)],
    [(131, -1), (137, -2), (142, -3), (147, -6), (150, -9), (146, -9),
     (141, -8), (136, -6), (132, -3)],
    # Japan + UK (small)
    [(130, 31), (133, 34), (137, 35), (140, 36), (141, 40), (142, 44),
     (140, 44), (138, 39), (135, 34), (131, 32)],
    [(-5, 50), (-3, 53), (-4, 56), (-6, 58), (-3, 58), (-1, 56), (0, 53),
     (1, 51)],
    # Australia + New Zealand
    [(113, -22), (114, -28), (115, -34), (118, -35), (124, -33), (130, -32),
     (133, -32), (136, -35), (139, -37), (141, -38), (146, -39), (148, -38),
     (150, -36), (153, -31), (153, -26), (150, -23), (146, -19), (143, -15),
     (142, -11), (144, -14), (142, -18), (140, -20), (136, -15), (135, -12),
     (132, -11), (129, -13), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (172, -41), (174, -39), (176, -37), (174, -41), (170, -44),
     (168, -47)],
]

# story pins: (num, lon, lat, dx, dy) — dx/dy nudge the Europe/Gulf cluster
MAP_PINS = [
    (1, 33.4, 47.9, 6, -4),      # Kryvyi Rih
    (2, 56.2, 26.2, 12, -8),     # Khasab / Hormuz
    (3, -74.0, 40.7, 0, 0),      # New York
    (4, 46.7, 24.6, -8, 8),      # Riyadh
    (5, 30.7, 36.9, -4, 12),     # Antalya
    (6, 6.1, 46.2, -10, -6),     # Geneva
    (7, 12.6, 55.7, 2, -8),      # Copenhagen
    (8, 7.7, 45.1, 10, 10),      # Turin
    (9, -75.2, -11.5, 0, 0),     # Junin, Peru
]


p = Page()
d = p.d

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 52], fill=INK)
p.text(W // 2, 3, "THE  WORLD  TODAY", font(SERIF_B, 32), (255, 255, 255), "ma")
p.text(W // 2, 37, "Saturday 21 November 2026  •  35 stories  •  8 regions  •  One page",
       font(SANS_B, 12), GOLD, "ma")
p.rule(M, W - M, 58, RED, 3)

# ---------------------------------------------------------------- stat strip
sy = 64
colw = CW / 6
for i, (num, cap) in enumerate(STATS):
    x = M + i * colw
    if i:
        d.line([(x, sy + 2), (x, sy + 40)], fill=RED, width=2)
    p.text(x + 8, sy, num, font(SERIF_B, 22), INK)
    ly = sy + 27
    for ln in p.wrap(cap, font(SANS, 9), colw - 14)[:2]:
        p.text(x + 8, ly, ln, font(SANS, 9), (60, 60, 60))
        ly += 10

# ---------------------------------------------------------------- region tally
ty = 114
total = sum(n for _, n, _ in TALLY)
mins = [52 if n == 1 else 0 for _, n, _ in TALLY]
rest = CW - sum(mins)
x = M
for (name, n, color), mn in zip(TALLY, mins):
    wdt = mn if mn else rest * n / (total - 3)
    d.rectangle([x, ty, x + wdt, ty + 16], fill=color)
    label = "%s %d" % (name, n)
    fsz = 10 if wdt >= 100 else 8
    while fsz > 6 and p.width(label, font(SANS_B, fsz)) > wdt - 4:
        fsz -= 1
    p.text(x + wdt / 2, ty + 3, label, font(SANS_B, fsz), (255, 255, 255), "ma")
    x += wdt

# ---------------------------------------------------------------- leads
SCENES = [scene_kryvyi, scene_hormuz, scene_wallst]
lead_y = 136
scene_h = 88
for i, lead in enumerate(LEADS):
    x = M + i * 329
    img = SCENES[i](318, scene_h)
    p.img.paste(img, (x, lead_y))
    d.rectangle([x, lead_y, x + 318, lead_y + scene_h], outline=(120, 120, 120), width=1)
    p.chip(x + 8, lead_y + 8, lead["chip"], size=14)
    sub = lead["sub"]
    f = font(SANS_B, 10)
    sw = int(p.width(sub, f)) + 10
    d.rectangle([x + 8, lead_y + 33, x + 8 + sw, lead_y + 49], fill=(245, 242, 235))
    p.text(x + 13, lead_y + 36, sub, f, INK)
    p.tag(x + 8, lead_y + scene_h - 19, lead["tag"])
    ty2 = lead_y + scene_h + 6
    ty2 = p.kicker(x, ty2, lead["num"], lead["kick"])
    ty2 = p.headline(x, ty2 + 2, 318, lead["head"], size=19, lh=22, max_lines=2)
    p.body(x, ty2 + 4, 318, lead["body"], size=10, lh=13, max_lines=4)

# ---------------------------------------------------------------- tiles
tile_y0 = 358
for i, tile in enumerate(TILES):
    x = M + (i % 3) * 329
    y = tile_y0 + (i // 3) * 138
    art = TILE_ART[tile["art"]]()
    p.img.paste(art, (x, y))
    d.rectangle([x, y, x + 318, y + 56], outline=(120, 120, 120), width=1)
    p.chip(x + 6, y + 6, tile["chip"], size=12)
    tg = tile["tag"]
    f = font(SANS_B, 9)
    tw = int(p.width(tg, f)) + 10
    d.rectangle([x + 318 - tw - 6, y + 56 - 16, x + 312, y + 56 - 2], fill=(24, 24, 24))
    p.text(x + 318 - tw - 1, y + 56 - 13, tg, f, (240, 240, 240))
    ky = p.kicker(x, y + 60, tile["num"], tile["kick"], size=11)
    hy = p.headline(x, ky + 1, 318, tile["head"], size=14, lh=16, max_lines=2)
    p.body(x, hy + 2, 318, tile["body"], size=10, lh=12, max_lines=3)

# ---------------------------------------------------------------- map + timeline
my = 640
p.text(M, my, "WHERE IT HAPPENED", font(SANS_B, 13), BLUE)
p.text(640, my, "THE DAY IN UTC", font(SANS_B, 13), BLUE)
map_box = [M, my + 18, M + 596, my + 140]
d.rectangle(map_box, fill=MAP_BG, outline=BLUE, width=2)
mx0, my0, mx1, my1 = map_box
mw, mh = mx1 - mx0, my1 - my0


def ll(lon, lat):
    return (mx0 + (lon + 180) / 360 * mw, my0 + (84 - lat) / 142 * mh)


for poly in CONTINENTS:
    d.polygon([ll(lon, lat) for lon, lat in poly], fill=LAND,
              outline=LAND_EDGE, width=1)
for num, lon, lat, dx, dy in MAP_PINS:
    px, py = ll(lon, lat)
    p.numdot(int(px + dx), int(py + dy), num, r=8, bg=RED)
p.text(mx0 + 6, my1 - 13, "Each number is the story with that number on this page.",
       font(SANS, 8), BLUE)

tly = my + 22
for t, label in TIMELINE:
    p.text(640, tly, t, font(SANS_B, 11), RED)
    p.text(692, tly + 1, label, font(SANS, 10), (40, 40, 40))
    tly += 24

# ---------------------------------------------------------------- markets
ky = 788
d.rectangle([M, ky, W - M, ky + 26], fill=INK)
strip = MARKETS
for sz in (12, 11, 10):
    if p.width(strip, font(SANS_B, sz)) <= CW - 24:
        break
p.text(W // 2, ky + 6, strip, font(SANS_B, sz), (255, 255, 255), "ma")

# ---------------------------------------------------------------- briefs
by = 822
p.text(M, by, "ALSO ON SATURDAY — 26 MORE STORIES", font(SANS_B, 13), BLUE)
yy = by + 18
for row in range(13):
    for colx, b in ((M, BRIEFS[row]), (512, BRIEFS[row + 13])):
        num = row + 10 + (13 if colx > M else 0)
        p.text(colx, yy, str(num), font(SANS_B, 9), RED)
        p.text(colx + 20, yy, b, font(SANS, 9), (35, 35, 35))
    yy += 11.5

# ---------------------------------------------------------------- date check + footer
dy = 992
d.rectangle([M, dy, W - M, dy + 20], outline=RED, width=2)
p.text(M + 8, dy + 5, "DATE CHECK", font(SANS_B, 9), RED)
p.text(M + 78, dy + 5, DATECHECK, font(SANS, 9), (40, 40, 40))
p.text(W // 2, 1014,
       "All the day's news, in one image — " + EDITION +
       "  •  Sources: " + ", ".join(SOURCES),
       font(SANS, 8), GREY, "ma")

p.save()
