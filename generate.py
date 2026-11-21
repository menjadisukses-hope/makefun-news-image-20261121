#!/usr/bin/env python3
"""Draw a 1024x1024 newspaper front page summing up Saturday 21 November 2026.

35 sourced stories across 8 regions: 3 leads, 6 secondary stories, 26 briefs,
plus a UTC timeline, a schematic world map with numbered pins, a markets strip,
a region tally and a date check. Every story is a verified 21 Nov 2026 fact
(events that happened, or were first reported, on that day) with a named source.

Deterministic: fixed text, fixed geometry, no randomness, no clock, no network.
Run: python3 generate.py  ->  writes news.png next to this file.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (250, 247, 238)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (20, 55, 110)
GREY = (96, 96, 96)
FAINT = (205, 199, 184)
MAP_BG = (214, 228, 238)
LAND = (168, 188, 150)

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

    def kicker(self, x, y, label, size=14):
        self.text(x, y, label, font(SANS_B, size), RED)
        return y + size + 6

    def story(self, x, y, w, head, body, src, hsize=18, bsize=13, max_body=6):
        """Headline (bold) + body + source tag, returns y below the block."""
        for ln in self.wrap(head, font(SANS_B, hsize), w):
            self.text(x, y, ln, font(SANS_B, hsize))
            y += hsize + 3
        for ln in self.wrap(body, font(SANS, bsize), w)[:max_body]:
            self.text(x, y, ln, font(SANS, bsize), (40, 40, 40))
            y += bsize + 4
        self.text(x, y, "Source: " + src, font(SANS, 10), GREY)
        return y + 14

    def save(self):
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
        self.img.save(out, optimize=True)
        print(out, os.path.getsize(out))


p = Page()
d = p.d

# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 90], fill=INK)
p.text(W // 2, 8, "THE  WORLD  TODAY", font(SERIF_B, 44), (255, 255, 255), "ma")
p.text(W // 2, 60, "Saturday 21 November 2026  •  35 stories  •  8 regions  •  One page",
       font(SANS_B, 15), (255, 210, 120), "ma")
p.rule(24, W - 24, 100, RED, 4)
p.text(24, 108, "DATE CHECK: Saturday 21 November 2026 — today's news, as reported today; "
                 "earlier events are dated in the text.",
       font(SANS_B, 12), BLUE)
p.text(24, 124, "STORIES BY REGION — Europe 8  •  North America 8  •  Asia 7  •  "
                 "Middle East 5  •  Africa 4  •  Latin America 1  •  Oceania 1  •  Antarctica 1",
       font(SANS_B, 11), GREY)
p.rule(24, W - 24, 140, GREY, 1)

# ---------------------------------------------------------------- lead + rail
y = 150
y = p.kicker(24, y, "1  WAR • UKRAINE")
y = p.story(24, y, 640,
            "OVERNIGHT BLITZ KILLS TWO IN KRYVYI RIH",
            "Russia fired three ballistic missiles and 148 drones at Ukraine overnight "
            "— 87 of them jet-powered. Two missiles struck near a restaurant in Kryvyi "
            "Rih, killing a seven-year-old boy and a 20-year-old paramedic and injuring "
            "58, six of them children. A drone hit a block in Solonytsivka, injuring 11.",
            "Ukraine Air Force • UNITED24 • TRT",
            hsize=27, bsize=15, max_body=6)
p.rule(24, 664, y + 4, GREY, 1)

rx = 688
ry = 150
ry = p.kicker(rx, ry, "2  GULF • HORMUZ")
ry = p.story(rx, ry, 312,
             "TWO TANKERS HIT OFF OMAN",
             "Two tankers leaving the Strait of Hormuz were hit by unidentified "
             "projectiles off Khasab — one on the stern at 05:00 GMT, one in the "
             "engine room at 05:50. No casualties.",
             "UKMTO • Reuters • Al Jazeera",
             hsize=18, bsize=13, max_body=4)
p.rule(rx, W - 24, 296, GREY, 1)
ry = p.kicker(rx, 306, "3  MARKETS • USA")
p.story(rx, ry, 312,
        "WALL ST ROUT: S&P AND DOW INTO CORRECTION",
        "US stocks plunged: Nasdaq −5.3% to 22,618, wiping out its 2026 gains; "
        "S&P 500 −3.7% to 6,910. Nvidia fell 14% on an SEC probe report.",
        "Reuters • AP",
        hsize=17, bsize=13, max_body=5)

# ---------------------------------------------------------------- map band
my = 330
d.rectangle([24, my, 664, my + 112], fill=MAP_BG, outline=BLUE, width=2)
p.text(36, my + 8, "WHERE IT HAPPENED (SCHEMATIC)", font(SANS_B, 15), BLUE)
land_polys = [
    [(60, 398), (150, 378), (205, 390), (200, 420), (160, 428), (120, 428), (70, 428)],
    [(185, 428), (212, 428), (216, 430), (198, 428), (182, 430)],
    [(330, 382), (385, 376), (408, 392), (392, 420), (350, 416), (328, 398)],
    [(340, 420), (400, 416), (416, 428), (390, 428), (356, 428)],
    [(420, 378), (530, 372), (592, 396), (572, 428), (495, 424), (436, 412)],
    [(535, 428), (582, 428), (594, 430), (566, 428), (542, 428)],
]
for poly in land_polys:
    d.polygon(poly, fill=LAND, outline=(120, 140, 110))
pins = [
    (345, 395, "1"),   # Kryvyi Rih
    (512, 425, "2"),   # Khasab
    (140, 398, "3"),   # New York
    (478, 412, "4"),   # Riyadh
    (448, 400, "5"),   # Antalya
    (395, 375, "6"),   # Geneva
    (365, 360, "7"),   # Copenhagen
    (418, 395, "8"),   # Turin
    (105, 425, "9"),   # Junin
]
for px, py, num in pins:
    d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
    p.text(px, py - 1, num, font(SANS_B, 11), (255, 255, 255), "ma")
p.text(24, my + 116,
       "1 Kryvyi Rih  •  2 Khasab  •  3 New York  •  4 Riyadh  •  5 Antalya  •  "
       "6 Geneva  •  7 Copenhagen  •  8 Turin  •  9 Junín",
       font(SANS_B, 10), BLUE)

# ---------------------------------------------------------------- UTC timeline
ty = 460
p.text(24, ty, "THE DAY IN UTC", font(SANS_B, 15), BLUE)
timeline = [
    ("00:09", "M6.7 quake shakes Junín, Peru; felt in Lima"),
    ("05:00", "First tanker hit off Khasab, Oman"),
    ("06:00", "Kyiv: water down in 5 districts after strikes"),
    ("10:46", "COP31 deadlock reported from Antalya"),
    ("13:30", "Alcaraz–Shelton semi-final starts in Turin"),
]
xx = 24
for t, label in timeline:
    p.text(xx, ty + 22, t, font(SANS_B, 12), RED)
    ly = ty + 40
    for ln in p.wrap(label, font(SANS, 11), 185):
        p.text(xx, ly, ln, font(SANS, 11), (40, 40, 40))
        ly += 14
    xx += 196
p.rule(24, W - 24, ty + 68, GREY, 1)

# ---------------------------------------------------------------- middle grid
gy = 534
cols = [(24, 320), (352, 320), (680, 320)]
grid = [
    ("4  GULF • RIYADH", "HOUTHI MISSILES DOWNED OVER RIYADH",
     "Saudi defences downed three Houthi missiles over Riyadh early on Saturday "
     "— the third straight day of air-raid alerts. No one was hurt.",
     "Reuters • AFP"),
    ("5  CLIMATE • ANTALYA", "COP31 IN OVERTIME IN FOSSIL-FUEL ROW",
     "UN climate talks in Turkey ran past their Friday deadline with no deal "
     "after a draft dropped all mention of fossil fuels. Talks get an extra day.",
     "AP • BBC • Guardian"),
    ("6  EUROPE • GENEVA", "KILLER-ROBOT RULES: 128 NATIONS AGREE",
     "Delegates from 128 countries agreed in Geneva to keep working on rules for "
     "lethal autonomous weapons, aiming for a 2028 accord. No binding limits.",
     "Washington Post • Reuters"),
    ("7  EUROPE • COPENHAGEN", "DENMARK TO EXPEL RUSSIAN ATTACHÉ",
     "Denmark will expel Russia's defence attaché within seven days over an "
     "alleged Russian plot to kill rapper Kyivstoner at a Copenhagen concert.",
     "AP • BBC"),
    ("8  SPORT • TURIN", "ATP FINALS: ALCARAZ v SHELTON TODAY",
     "Carlos Alcaraz meets Ben Shelton at 14:30 CET in the first ATP Finals "
     "semi-final in Turin; Alexander Zverev faces Daniil Medvedev at 20:30. "
     "Alcaraz leads Shelton 4–1.",
     "ATP Tour • Flashscore"),
    ("9  QUAKES • PERU", "M6.7 QUAKE SHAKES PERU, FELT IN LIMA",
     "A magnitude 6.7 earthquake struck near Junín in central Peru at 00:09 GMT "
     "on Saturday, about 129 km deep. It rattled Lima; no deaths were reported.",
     "AFP • USGS • IGP"),
]
for i, (kick, head, body, src) in enumerate(grid):
    cx, cw = cols[i % 3]
    cy = gy if i < 3 else gy + 116
    p.kicker(cx, cy, kick, size=12)
    p.story(cx, cy + 18, cw, head, body, src, hsize=15, bsize=11, max_body=3)
    if i % 3 != 2:
        d.line([(cx + cw + 14, cy), (cx + cw + 14, cy + 100)], fill=FAINT, width=1)
p.rule(24, W - 24, gy + 114, GREY, 1)
p.rule(24, W - 24, gy + 230, GREY, 1)

# ---------------------------------------------------------------- markets strip
my2 = gy + 234
d.rectangle([24, my2, W - 24, my2 + 28], fill=INK)
strip = ("MARKETS — S&P 500 −3.7% · 6,910  |  Nasdaq −5.3% · 22,618  |  "
         "Dow −1.9% · 48,147  |  Gold $3,539  |  Brent $92.49  |  Bitcoin ~$57,200")
for sz in (12, 11, 10):
    if p.width(strip, font(SANS_B, sz)) <= W - 48:
        break
p.text(W // 2, my2 + 7, strip, font(SANS_B, sz), (255, 255, 255), "ma")

# ---------------------------------------------------------------- briefs
by = my2 + 36
p.text(24, by, "ALSO ON SATURDAY — 26 MORE STORIES, ONE LINE EACH", font(SANS_B, 14), BLUE)
briefs = [
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
assert len(briefs) == 26
# two columns of 13; check every brief fits one line at 11px
for b in briefs:
    assert p.width("•  " + b, font(SANS, 11)) <= 472, "brief too long: " + b
yy = by + 20
for row in range(13):
    p.text(24, yy, "•  " + briefs[row], font(SANS, 11), (35, 35, 35))
    p.text(528, yy, "•  " + briefs[row + 13], font(SANS, 11), (35, 35, 35))
    yy += 12.25

# ---------------------------------------------------------------- date check (bottom) + footer
p.text(24, yy + 4,
       "DATE CHECK — NOT SHOWN: Fri: Shenzhen declaration • ICJ Myanmar ruling • "
       "PIF Tower hit • Nikkei −5.1%.  NOT YET: ATP final (Sun) • COP31 deal • "
       "Zverev–Medvedev semi.",
       font(SANS_B, 10), BLUE)
d.rectangle([0, H - 26, W, H], fill=INK)
p.text(W // 2, H - 20,
       "All the day's news, in one image — " + EDITION +
       "  •  Sources: " + ", ".join(SOURCES),
       font(SANS, 11), (255, 255, 255), "ma")

p.save()
