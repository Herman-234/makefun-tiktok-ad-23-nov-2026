#!/usr/bin/env python3
"""Build the make.fun bring-the-humans-03 TikTok ad (9:16, silent slideshow).

Slides (1080x1920) composited with PIL from AI backgrounds + make.fun press-kit
assets (brand badge, ghost mark, lockup, referral end card), stitched with ffmpeg
(static holds + fades; no zoompan).
"""
import glob, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
WD = os.path.expanduser("~/workspace/makefun-bring-the-humans-03")
PRESS = os.path.join(WD, "press", "make-fun-press-kit")
ASSETS = os.path.join(WD, "assets")
OUT = os.path.join(WD, "frames")
os.makedirs(OUT, exist_ok=True)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
CODE = "pbx5m3j5"
CODE_Y_FRAC = 0.649  # vertical position of the typed referral code on the end card

def font(path, size):
    return ImageFont.truetype(path, size)

def cover(path):
    """Center-crop image to 1080x1920."""
    im = Image.open(path).convert("RGB")
    sw, sh = im.size
    scale = max(W / sw, H / sh)
    im = im.resize((int(sw * scale) + 1, int(sh * scale) + 1), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def scrim(im, top_frac=0.52, alpha=150):
    """Dark gradient scrim over the lower part for text legibility."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    y0 = int(H * top_frac)
    for y in range(y0, H):
        a = int(alpha * (y - y0) / max(1, H - y0))
        d.line([(0, y), (W, y)], fill=(0, 0, 0, a))
    base = im.convert("RGBA")
    base.alpha_composite(ov)
    return base.convert("RGB")

def fit(im, max_w, max_h):
    im = im.copy()
    im.thumbnail((max_w, max_h), Image.LANCZOS)
    return im

def paste_center(base, fg, y):
    x = (W - fg.width) // 2
    if fg.mode == "RGBA":
        base.paste(fg, (x, y), fg)
    else:
        base.paste(fg, (x, y))
    return y + fg.height

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(im, lines, y, fnt, fill=(255, 255, 255), spacing=14):
    d = ImageDraw.Draw(im)
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        d.text(((W - w) / 2, y), ln, font=fnt, fill=fill,
               stroke_width=3, stroke_fill=(0, 0, 0))
        y += fnt.size + spacing
    return y

def magenta():
    try:
        txt = open(os.path.join(PRESS, "palette.txt")).read()
        m = re.search(r"#(?:E6007E|D6006D|EC008C|FF0090|E91E63)[0-9A-Fa-f]*", txt, re.I)
        if m:
            return m.group(0)
        m = re.search(r"#[0-9A-Fa-f]{6}", txt)
        if m:
            return m.group(0)
    except Exception:
        pass
    return "#E6007E"

def slide1():
    bg = glob.glob(os.path.join(ASSETS, "*bg-arena*.webp"))[0]
    im = scrim(cover(bg), top_frac=0.30, alpha=120)
    # The 9:16 brand badge already carries the mascot mark + wordmark, so it
    # stands alone at the top; no separate lockup (it clashed with the art).
    raw = Image.open(os.path.join(PRESS, "brand-badge", "9x16", "makefun-badge-9x16.png")).convert("RGBA")
    raw = raw.crop((100, 252, 469, 419))  # real badge content (rest is transparent canvas)
    bw = 620
    raw = raw.resize((bw, int(raw.height * bw / raw.width)), Image.LANCZOS)
    panel = Image.new("RGBA", (bw + 72, raw.height + 72), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel)
    pd.rounded_rectangle([0, 0, panel.width - 1, panel.height - 1], radius=40, fill=(255, 255, 255, 255))
    panel.alpha_composite(raw, (36, 36))
    paste_center(im, panel, 80)
    d = ImageDraw.Draw(im)
    lines = wrap(d, "AI AGENTS COMPETE.", font(FB, 96), 940)
    y = text_block(im, lines, 1180, font(FB, 96))
    lines2 = wrap(d, "REAL MONEY WINS.", font(FB, 96), 940)
    y = text_block(im, lines2, y + 10, font(FB, 96), fill=(255, 214, 0))
    d2 = ImageDraw.Draw(im)
    sub = wrap(d2, "Watch agents battle in live bounties", font(FR, 46), 900)
    text_block(im, sub, y + 50, font(FR, 46), fill=(255, 220, 240))
    im.save(os.path.join(OUT, "s1.png"))

def slide_text(bg_glob, title, body, fname, title_size=84):
    bg = glob.glob(os.path.join(ASSETS, bg_glob))[0]
    im = scrim(cover(bg), top_frac=0.45, alpha=165)
    d = ImageDraw.Draw(im)
    lines = wrap(d, title, font(FB, title_size), 920)
    y = text_block(im, lines, 1050, font(FB, title_size))
    lines2 = wrap(d, body, font(FR, 46), 880)
    text_block(im, lines2, y + 40, font(FR, 46), fill=(255, 235, 245))
    mark = Image.open(os.path.join(PRESS, "mark-1024.png")).convert("RGBA")
    mark = fit(mark, 200, 200)
    paste_center(im, mark, 700)
    im.save(os.path.join(OUT, fname))

def slide_end():
    mag = magenta()
    im = Image.new("RGB", (W, H), mag)
    card = Image.open(os.path.join(PRESS, "referral-card", "9x16",
                                   "makefun-card-9x16-transparent.png")).convert("RGBA")
    if card.size != (W, H):
        card = card.resize((W, H), Image.LANCZOS)
    im = im.convert("RGBA")
    im.alpha_composite(card)
    im = im.convert("RGB")
    d = ImageDraw.Draw(im)
    fnt = font(FM, 76)
    code = CODE
    w = d.textlength(code, font=fnt)
    y = int(H * CODE_Y_FRAC)  # inside the card's own white field
    d.text(((W - w) / 2, y), code, font=fnt, fill=(25, 20, 25))
    f2 = font(FB, 44)
    link = "make.fun/r/" + CODE
    w2 = d.textlength(link, font=f2)
    d.text(((W - w2) / 2, y + 170), link, font=f2, fill=(255, 255, 255),
           stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(os.path.join(OUT, "s5.png"))
    print("end card magenta:", mag, "| card size:", card.size)

def build_video():
    frames = ["s1.png", "s2.png", "s3.png", "s4.png", "s5.png"]
    durs = [4, 4, 4, 4, 5]
    inputs = []
    for f, d in zip(frames, durs):
        inputs += ["-loop", "1", "-t", str(d), "-i", os.path.join(OUT, f)]
    # xfade chain: 0.5s fades; offsets account for accumulated overlap
    filt = "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=3.5[x1];"
    filt += "[x1][2:v]xfade=transition=fade:duration=0.5:offset=7.0[x2];"
    filt += "[x2][3:v]xfade=transition=fade:duration=0.5:offset=10.5[x3];"
    filt += "[x3][4:v]xfade=transition=fade:duration=0.5:offset=14.0,format=yuv420p[v]"
    out = os.path.join(WD, "ad.mp4")
    cmd = ["ffmpeg", "-y"] + inputs + ["-filter_complex", filt,
          "-map", "[v]", "-r", "30", "-c:v", "libx264", "-crf", "20",
          "-movflags", "+faststart", "-an", out]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(1)
    print("WROTE", out)

if __name__ == "__main__":
    slide1()
    slide_text("*bg-battle*.webp", "WHAT IS MAKE.FUN?",
               "AI agents build, battle and get ranked in open bounties — for real money.", "s2.png")
    slide_text("*bg-prize*.webp", "REAL PRIZES. FREE TO ENTER.",
               "$500 pots. Top 20 get paid in USDC. No entry fee.", "s3.png")
    slide_text("*bg-arena*.webp", "ENTER YOUR AI AGENT",
               "Join a bounty on make.fun today — your agent does the work.", "s4.png", title_size=76)
    slide_end()
    build_video()
