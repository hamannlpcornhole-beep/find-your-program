"""Build every person's print sheet and their how-it-works handout.

Reads the QR codes in qrcodes/ and writes into
  Development Program/People/<group>/<Name>/

Usage:
  python3 -m venv .venv && .venv/bin/pip install pillow
  .venv/bin/python scripts/make_sheets.py

Fonts: Barlow Condensed and Barlow, the same pair the site uses. Point FONTS at a
folder holding the .ttf files, or the script falls back to Arial.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parent.parent
PEOPLE_ROOT = REPO.parent / "People"
QRS = REPO / "qrcodes"
FONTS = Path("/private/tmp/claude-501/-Users-gavinhamann-Desktop-Level-Up-Cornhole/"
             "f1a79b69-d649-4c18-9b55-affa24ad3f19/scratchpad/fonts")
SYS = Path("/System/Library/Fonts/Supplemental")
BASE = "https://hamannlpcornhole-beep.github.io/find-your-program/"
SHOP = "levelupcornhole.shop"

# letter at 300 dpi
W, H = 2550, 3300
M = 210  # page margin

ORANGE = (243, 108, 33)
INK = (11, 11, 14)
PAPER = (255, 255, 255)
SOFT = (246, 244, 241)
LINE = (223, 219, 212)
MUTED = (122, 122, 130)
WHITE = (255, 255, 255)


def _font(name, sys_fallback, size):
    p = FONTS / name
    return ImageFont.truetype(str(p if p.exists() else SYS / sys_fallback), size)


disp = lambda s: _font("BarlowCondensed-Black.ttf", "Arial Black.ttf", s)          # headlines
dispb = lambda s: _font("BarlowCondensed-Bold.ttf", "Arial Bold.ttf", s)           # sub heads
body = lambda s: _font("Barlow-Regular.ttf", "Arial.ttf", s)
bodym = lambda s: _font("Barlow-Medium.ttf", "Arial.ttf", s)
bodyb = lambda s: _font("Barlow-Bold.ttf", "Arial Bold.ttf", s)

LOGO = Image.open(REPO / "assets/source/level_up_logo_original.png").convert("RGBA")

PEOPLE = [
    ("brandie", "Brandie McCuen", "Development players", "Development player"),
    ("kenneth", "Kenneth Boucher", "Development players", "Development player"),
    ("simon", "Simon Ballard", "Development players", "Development player"),
    ("rylan", "Rylan Brockett", "Development players", "Development player"),
    ("colt", "Colt Kenner", "Development players", "Development player"),
    ("richard", "Richard Nyberg", "Coaches", "Coach. Complete game development"),
    ("colin", "Colin Hodet", "Coaches", "Coach. Precision and shot making"),
    ("aj", "AJ Sims", "Coaches", "Coach. Competition focused"),
    ("hunter", "Hunter Thorson", "Coaches", "Coach. One on one sessions"),
    ("peyton", "Peyton Haynes", "Coaches", "Coach"),
    ("general", "General code", "General", "No name on it"),
]


# ---------------------------------------------------------------- helpers
def fit(im, w, h):
    r = min(w / im.width, h / im.height)
    return im.resize((max(1, int(im.width * r)), max(1, int(im.height * r))), Image.LANCZOS)


def tw(d, s, f):
    return d.textbbox((0, 0), s, font=f)[2]


def center(d, y, s, f, fill, x0=0, x1=W):
    d.text((x0 + (x1 - x0 - tw(d, s, f)) // 2, y), s, font=f, fill=fill)


def wrap(d, s, f, width):
    out, line = [], ""
    for word in s.split():
        t = (line + " " + word).strip()
        if tw(d, t, f) <= width:
            line = t
        else:
            out.append(line); line = word
    if line:
        out.append(line)
    return out


def para(d, x, y, s, f, fill, width, lead):
    for ln in wrap(d, s, f, width):
        d.text((x, y), ln, font=f, fill=fill); y += lead
    return y


def shadow_card(im, box, radius=44, fill=WHITE, line=LINE):
    """A card with a soft drop shadow, drawn by stacking fading rounded rects."""
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ds = ImageDraw.Draw(sh)
    for i in range(18, 0, -1):
        a = int(3 + (18 - i) * 1.4)
        ds.rounded_rectangle([x0 - i, y0 - i + 14, x1 + i, y1 + i + 14], radius=radius + i,
                             fill=(11, 11, 14, a))
    im.alpha_composite(sh)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=line, width=3)


def qr_for(key, side):
    """Scale a code to whole pixels per module so the squares stay crisp in print."""
    src = Image.open(QRS / f"{key}_qr.png").convert("RGB")
    mods = src.width // 16 if src.width % 16 == 0 else src.width
    px = max(1, side // mods)
    return src.resize((mods * px, mods * px), Image.NEAREST)


def brackets(d, box, arm=90, wgt=16, color=ORANGE):
    x0, y0, x1, y1 = box
    for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        d.line([cx, cy, cx + arm * dx, cy], fill=color, width=wgt)
        d.line([cx, cy, cx, cy + arm * dy], fill=color, width=wgt)


def header(im, d, kicker):
    d.rectangle([0, 0, W, 470], fill=INK)
    d.rectangle([0, 470, W, 492], fill=ORANGE)
    lg = fit(LOGO, 300, 250)
    im.paste(lg, (M, (470 - lg.height) // 2), lg)
    f = dispb(58)
    d.text((W - M - tw(d, kicker, f), (470 - 58) // 2 + 4), kicker, font=f, fill=WHITE)


def footer(im, d, right=""):
    d.rectangle([0, H - 210, W, H], fill=INK)
    d.rectangle([0, H - 210, W, H - 190], fill=ORANGE)
    f = disp(64)
    d.text((M, H - 150), SHOP.upper(), font=f, fill=WHITE)
    if right:
        g = body(44)
        d.text((W - M - tw(d, right, g), H - 138), right, font=g, fill=(168, 168, 176))


# ---------------------------------------------------------------- print sheet
def print_sheet(key, name, role, out):
    im = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    header(im, d, "DEVELOPMENT PROGRAM")

    center(d, 600, "FIND YOUR", disp(230), INK)
    center(d, 800, "PROGRAM.", disp(230), ORANGE)
    center(d, 1055, "Scan the code. Answer five quick questions.", body(56), MUTED)
    center(d, 1127, "You get the plan and the coach that fit your game.", body(56), MUTED)

    # code card
    qr = qr_for(key, 860)
    pad = 110
    cw = qr.width + pad * 2
    x0, y0 = (W - cw) // 2, 1290
    shadow_card(im, [x0, y0, x0 + cw, y0 + cw])
    d = ImageDraw.Draw(im)
    im.paste(qr, (x0 + pad, y0 + pad))
    brackets(d, [x0 + 46, y0 + 46, x0 + cw - 46, y0 + cw - 46])

    # who sent it, name over role on one dark plate
    label = "SENT BY " + name.upper() if key != "general" else "LEVEL UP CORNHOLE"
    f = disp(86)
    while tw(d, label, f) > W - M * 2 - 240:
        f = disp(f.size - 4)
    sub = role if key != "general" else "No name on it. Use it anywhere."
    pw = max(tw(d, label, f), tw(d, sub, body(42))) + 230
    px0, py = (W - pw) // 2, 2470
    d.rounded_rectangle([px0, py, px0 + pw, py + 230], radius=48, fill=INK)
    d.ellipse([px0 + 70, py + 76, px0 + 100, py + 106], fill=ORANGE)
    d.text((px0 + 134, py + 42), label, font=f, fill=WHITE)
    g = body(42)
    d.text(((W - tw(d, sub, g)) // 2, py + 150), sub, font=g, fill=(170, 170, 178))

    # three steps
    d.line([M, 2790, W - M, 2790], fill=LINE, width=3)
    steps = [("1", "Scan it"), ("2", "Five questions"), ("3", "Your plan and coach")]
    colw = (W - M * 2) // 3
    for i, (n, t) in enumerate(steps):
        cx = M + colw * i + colw // 2
        d.ellipse([cx - 42, 2860, cx + 42, 2944], fill=ORANGE)
        nf = disp(52)
        d.text((cx - tw(d, n, nf) // 2, 2872), n, font=nf, fill=WHITE)
        tf = dispb(54)
        d.text((cx - tw(d, t, tf) // 2, 2966), t, font=tf, fill=INK)

    footer(im, d, f"{BASE}?ref={key}".replace("https://", ""))
    im.convert("RGB").save(out, "PDF", resolution=300.0)


# ---------------------------------------------------------------- handout
def handout(key, name, role, out):
    url = f"{BASE}?ref={key}"
    who = name if key != "general" else "Level Up Cornhole"

    # ---- page 1
    p1 = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(p1)
    header(p1, d, "HOW YOUR CODE WORKS")

    y = 600
    d.text((M, y), "YOUR QR CODE", font=dispb(56), fill=ORANGE)
    y += 78
    f = disp(190)
    t = name.upper()
    while tw(d, t, f) > W - M * 2 - 620:
        f = disp(f.size - 8)
    d.text((M, y), t, font=f, fill=INK)
    y += int(f.size * 1.06)
    d.text((M, y), role, font=bodym(52), fill=MUTED)

    # link card with the code beside it
    y += 130
    card = [M, y, W - M, y + 470]
    shadow_card(p1, card, radius=40, fill=SOFT)
    d = ImageDraw.Draw(p1)
    qr = qr_for(key, 400)
    p1.paste(qr, (W - M - 70 - qr.width, y + (470 - qr.height) // 2))
    tx = M + 70
    d.text((tx, y + 62), "YOUR LINK", font=dispb(52), fill=ORANGE)
    lf = bodyb(44)
    ly = y + 132
    for ln in wrap(d, url, lf, W - M * 2 - 220 - qr.width):
        d.text((tx, ly), ln, font=lf, fill=INK); ly += 58
    ly += 24
    para(d, tx, ly, "No code to type in. The scan is what tells us you sent them.",
         body(44), MUTED, W - M * 2 - 260 - qr.width, 56)

    # what happens
    y = card[3] + 120
    d.text((M, y), "WHAT HAPPENS WHEN SOMEONE SCANS IT", font=dispb(62), fill=INK)
    d.line([M, y + 92, M + 260, y + 92], fill=ORANGE, width=8)
    y += 150
    steps = [
        ("Their phone opens the page", "It goes straight to Find Your Program. No app, no login."),
        (f"The page says {who} sent them", "Your name sits right at the top of the screen."),
        ("They tap Find My Program", "Five quick questions about their game and their goals."),
        ("They get one plan and one coach", "Elite, Compete or Pro, or a one time video breakdown or call."),
        ("Your name rides along to checkout", "Every buy button carries it, so the sale traces back to you."),
    ]
    for i, (t, s) in enumerate(steps, 1):
        d.ellipse([M, y + 4, M + 74, y + 78], outline=ORANGE, width=6)
        nf = disp(48)
        d.text((M + 37 - tw(d, str(i), nf) // 2, y + 14), str(i), font=nf, fill=ORANGE)
        d.text((M + 124, y), t, font=bodyb(52), fill=INK)
        para(d, M + 124, y + 68, s, body(46), MUTED, W - M * 2 - 140, 56)
        y += 150
    y += 45
    d.text((M, y), "WHERE TO PUT IT", font=dispb(62), fill=INK)
    d.line([M, y + 92, M + 260, y + 92], fill=ORANGE, width=8)
    y += 150
    for it in ["Save the code to your phone so you can pull it up fast.",
               "Print the sheet in this folder for your bag, your board, the tent or the wall at league.",
               "Post the image in your story or drop it in your bio link."]:
        d.rounded_rectangle([M, y + 18, M + 26, y + 44], radius=13, fill=ORANGE)
        y = para(d, M + 70, y, it, body(50), (60, 60, 68), W - M * 2 - 90, 60) + 22
    footer(p1, d, f"{who} - page 1 of 2")

    # ---- page 2
    p2 = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(p2)
    header(p2, d, "HOW YOUR CODE WORKS")

    y = 620
    blocks = [
        ("HOW YOU GET THE CREDIT", [
            "It is tracking only. There is no discount code and nothing for them to type.",
            "Your link carries your name to the store, so Gavin can see which sales came off your code.",
            "If they type the plain web address instead of scanning, the credit is gone. Have them scan.",
        ]),
        ("WHAT IT IS NOT", [
            "It is not a discount. Nobody gets money off for scanning your code.",
            "It is not a login. The page works on any phone with no app and no account.",
            "You do not have to sell anything. Point at the code and let the page work.",
        ]),
    ]
    for title, items in blocks:
        d.text((M, y), title, font=dispb(62), fill=INK)
        d.line([M, y + 92, M + 260, y + 92], fill=ORANGE, width=8)
        y += 150
        for it in items:
            d.rounded_rectangle([M, y + 18, M + 26, y + 44], radius=13, fill=ORANGE)
            y = para(d, M + 70, y, it, body(50), (60, 60, 68), W - M * 2 - 90, 62) + 34
        y += 70

    # the pitch
    box = [M, y, W - M, y + 440]
    d.rounded_rectangle(box, radius=44, fill=INK)
    d.text((M + 80, y + 60), "WHAT TO SAY", font=dispb(56), fill=ORANGE)
    qy = y + 150
    for ln in wrap(d, '"Scan this. It asks you a few questions and tells you which coach '
                      'and plan fit your game."', dispb(78), W - M * 2 - 160):
        d.text((M + 80, qy), ln, font=dispb(78), fill=WHITE); qy += 92
    d.text((M + 80, qy + 16), "Keep it short. The page does the selling.", font=body(46),
           fill=(168, 168, 176))

    y = box[3] + 130
    d.text((M, y), "IF SOMETHING LOOKS WRONG", font=dispb(62), fill=INK)
    d.line([M, y + 92, M + 260, y + 92], fill=ORANGE, width=8)
    para(d, M, y + 150, "Text Gavin. The page and the code can be fixed in about a minute.",
         body(50), (60, 60, 68), W - M * 2, 62)

    # a short checklist to close the page out
    y = H - 830
    d.rounded_rectangle([M, y, W - M, H - 300], radius=44, fill=SOFT, outline=LINE, width=3)
    d.text((M + 80, y + 60), "BEFORE YOUR NEXT EVENT", font=dispb(56), fill=ORANGE)
    cy = y + 160
    for it in ["The code is saved on your phone",
               "A printed sheet is in your bag",
               "You know the one line to say"]:
        d.rounded_rectangle([M + 80, cy, M + 132, cy + 52], radius=12, outline=INK, width=5)
        d.text((M + 180, cy - 6), it, font=body(50), fill=(60, 60, 68))
        cy += 92

    footer(p2, d, f"{who} - page 2 of 2")
    import os
    if os.environ.get("SHEETPNG"):
        p1.convert("RGB").save(Path(os.environ["SHEETPNG"]) / f"{name}-p1.png")
        p2.convert("RGB").save(Path(os.environ["SHEETPNG"]) / f"{name}-p2.png")
    p1.convert("RGB").save(out, "PDF", resolution=300.0, save_all=True,
                           append_images=[p2.convert("RGB")])


# ---------------------------------------------------------------- all codes
def contact_sheet(out):
    im = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    header(im, d, "DEVELOPMENT PROGRAM")

    center(d, 620, "EVERY CODE.", disp(190), INK)
    center(d, 840, "One per person. Every scan tracks back to them.", body(52), MUTED)

    cols, side = 4, 400
    colw = (W - M * 2) // cols
    y0, pitch = 960, 620
    for i, (key, name, grp, role) in enumerate(PEOPLE):
        cx = M + colw * (i % cols) + colw // 2
        cy = y0 + pitch * (i // cols)
        qr = qr_for(key, side)
        box = [cx - qr.width // 2 - 40, cy - 40, cx + qr.width // 2 + 40, cy + qr.height + 40]
        d.rounded_rectangle(box, radius=30, fill=WHITE, outline=LINE, width=3)
        im.paste(qr, (cx - qr.width // 2, cy))
        f = disp(58)
        t = name.upper()
        while tw(d, t, f) > colw - 40:
            f = disp(f.size - 4)
        d.text((cx - tw(d, t, f) // 2, cy + qr.height + 72), t, font=f, fill=INK)
        sub = {"Development players": "Development player", "Coaches": "Coach"}.get(grp, "No name on it")
        g = body(42)
        d.text((cx - tw(d, sub, g) // 2, cy + qr.height + 136), sub, font=g, fill=MUTED)

    footer(im, d, "Print a person's own sheet from their folder")
    import os
    if os.environ.get("SHEETPNG"):
        im.convert("RGB").save(Path(os.environ["SHEETPNG"]) / "all-codes.png")
    im.convert("RGB").save(out, "PDF", resolution=300.0)


def section(d, x, y, title, width):
    d.text((x, y), title, font=dispb(62), fill=INK)
    d.line([x, y + 92, x + 260, y + 92], fill=ORANGE, width=8)
    return y + 150


def bullets(d, x, y, items, width, size=50, lead=60, gap=22):
    for it in items:
        d.rounded_rectangle([x, y + 18, x + 26, y + 44], radius=13, fill=ORANGE)
        y = para(d, x + 70, y, it, body(size), (60, 60, 68), width - 90, lead) + gap
    return y


def overview(out):
    """The START HERE guide that sits at the top of the Development Program folder."""
    p1 = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(p1)
    header(p1, d, "START HERE")

    d.text((M, 600), "LEVEL UP CORNHOLE", font=dispb(56), fill=ORANGE)
    d.text((M, 678), "DEVELOPMENT", font=disp(200), fill=INK)
    d.text((M, 868), "PROGRAM.", font=disp(200), fill=ORANGE)
    y = para(d, M, 1110,
             "Every development player and every coach has their own QR code. All of them open the "
             "same page. That page runs a short quiz and matches someone with a plan and a coach. "
             "Every buy button carries the name of whoever's code got scanned.",
             body(54), (60, 60, 68), W - M * 2 - 200, 68)

    y = section(d, M, y + 80, "WHAT IS IN HERE", W - M * 2)
    y = bullets(d, M, y, [
        "People. One folder per person, split into development players, coaches and the general code. "
        "Each folder holds their QR code, a print sheet to tape up and a how it works handout.",
        "All links and QR codes. Every link in one text file, ready to copy and paste.",
        "All QR codes on one page. Every code on a single sheet.",
        "Graphics. Loose images for the program.",
        "find-your-program. The website itself. Do not rename it. The printed codes point at that address.",
    ], W - M * 2)

    y = section(d, M, y + 60, "HOW A SCAN TURNS INTO A SALE", W - M * 2)
    steps = [
        "Someone scans a code at a tournament, at league or off a story.",
        "The page opens and says who sent them.",
        "They answer five quick questions.",
        "They get one plan and one coach, or a one time video breakdown or call.",
        "The link to the store carries that person's name on it.",
        "You look the campaign name up in Shopify to see which sales came from who.",
    ]
    for i, t in enumerate(steps, 1):
        d.ellipse([M, y + 4, M + 74, y + 78], outline=ORANGE, width=6)
        nf = disp(48)
        d.text((M + 37 - tw(d, str(i), nf) // 2, y + 14), str(i), font=nf, fill=ORANGE)
        y = para(d, M + 124, y + 6, t, body(50), (60, 60, 68), W - M * 2 - 140, 60) + 34

    footer(p1, d, "page 1 of 2")

    p2 = Image.new("RGBA", (W, H), PAPER)
    d = ImageDraw.Draw(p2)
    header(p2, d, "START HERE")

    y = section(d, M, 600, "WHERE THE CREDIT HOLDS UP", W - M * 2)
    y = bullets(d, M, y, [
        "First purchase after a scan: Shopify saves the landing page and the campaign name on the order.",
        "Open the order in Shopify and read the conversion summary, or group the sales reports by campaign.",
        "Monthly renewals come in through the subscription app with nothing attached, so month two is not tagged.",
        "Someone who scans on their phone and buys on a laptop later shows up as direct.",
        "Orders you build by hand lose the link too.",
    ], W - M * 2)

    box = [M, y + 40, W - M, y + 400]
    d.rounded_rectangle(box, radius=44, fill=INK)
    d.text((M + 80, y + 100), "THE FIX FOR RENEWALS", font=dispb(56), fill=ORANGE)
    para(d, M + 80, y + 190,
         "Set a Shopify Flow rule that tags the order and the customer with the campaign name. "
         "The tag sticks to that customer, so every renewal traces back to whoever sent them.",
         body(48), WHITE, W - M * 2 - 160, 60)

    y = section(d, M, box[3] + 110, "ADDING SOMEONE NEW", W - M * 2)
    y = bullets(d, M, y, [
        "Add their short name to the PLAYERS list in scripts/make_qr.py and run it. It checks the code scans.",
        "Add the name to the PLAYERS list in index.html so the page greets them.",
        "Add them to PEOPLE in scripts/make_sheets.py and run it. That builds their folder, sheet and handout.",
        "Push to main. The live page updates in about a minute.",
    ], W - M * 2)

    y = section(d, M, y + 60, "STILL OPEN", W - M * 2)
    bullets(d, M, y, [
        "The welcome video on the page is a placeholder.",
        "The footer has no social links yet.",
        "The two testimonials are not attributed to anyone.",
    ], W - M * 2)

    footer(p2, d, "page 2 of 2")
    p1.convert("RGB").save(out, "PDF", resolution=300.0, save_all=True,
                           append_images=[p2.convert("RGB")])
    import os
    if os.environ.get("SHEETPNG"):
        p1.convert("RGB").save(Path(os.environ["SHEETPNG"]) / "start-p1.png")
        p2.convert("RGB").save(Path(os.environ["SHEETPNG"]) / "start-p2.png")


def main():
    for key, name, grp, role in PEOPLE:
        folder = PEOPLE_ROOT / grp / name
        folder.mkdir(parents=True, exist_ok=True)
        Image.open(QRS / f"{key}_qr.png").save(folder / f"{name} QR code.png")
        print_sheet(key, name, role, folder / f"{name} print sheet.pdf")
        handout(key, name, role, folder / f"{name} - how it works.pdf")
        old = folder / f"{name} - how it works.txt"
        if old.exists():
            old.unlink()
        print("built", folder)
    contact_sheet(PEOPLE_ROOT.parent / "All QR codes - one page.pdf")
    overview(PEOPLE_ROOT.parent / "START HERE - How this works.pdf")
    old_txt = PEOPLE_ROOT.parent / "START HERE - How this works.txt"
    if old_txt.exists():
        old_txt.unlink()
    print("built the all codes sheet and the start here guide")


if __name__ == "__main__":
    main()
