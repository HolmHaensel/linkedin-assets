import json, sys, html, pathlib, base64, os
from playwright.sync_api import sync_playwright

# YMS page style (v3), follows Holm's GoHighLevel landing page. Rules: yms/STYLE.md
# Usage: FONTDIR=tools/fonts-yms python3 tools/render_yms_v3.py spec.json outdir
spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
SW, SH = spec.get("canvas", [1080, 1350])
POLAR, NAVY, TEAL, TEALD, CTA, CREAM, BODY, ONDARK, LINE, W = "#0e161c", "#162932", "#4db8b0", "#3a9e97", "#e05252", "#f0f4f5", "#57666b", "#c7d0d1", "#d7e0e2", "#ffffff"
FD = os.environ.get("FONTDIR", "tools/fonts-yms")
def b64(p): return base64.b64encode(open(p, "rb").read()).decode()
def ff(n, f, w): return f"@font-face{{font-family:'{n}';font-weight:{w};src:url(data:font/woff2;base64,{b64(f'{FD}/{f}')}) format('woff2')}}"
FONTS = "".join([ff("Raleway", f"raleway-latin-{w}-normal.woff2", w) for w in (700, 800)] + [ff("Lato", f"lato-latin-{w}-normal.woff2", w) for w in (400, 700)])
PHOTO = "data:image/jpeg;base64," + b64("tools/brand/holm-portrait.jpg")
CSS = FONTS + f"""*{{box-sizing:border-box;margin:0}}body{{width:{SW}px;height:{SH}px;font-family:Lato,sans-serif;font-feature-settings:'lnum' 1}}
.s{{position:relative;overflow:hidden;width:{SW}px;height:{SH}px;padding:84px 80px 150px;display:flex;flex-direction:column;justify-content:center}}
.e{{font-weight:700;font-size:28px;letter-spacing:.14em;text-transform:uppercase;margin-bottom:24px}}
.h{{font-family:Raleway;font-weight:800;line-height:1.14;letter-spacing:-.005em}}
.b{{font-size:44px;line-height:1.38}}
.card{{background:{W};border:2px solid {LINE};border-radius:24px;padding:34px 38px}}
.t1{{font-size:42px;font-weight:700;line-height:1.22;color:{NAVY}}}
.t2{{font-size:36px;line-height:1.3;color:{BODY};margin-top:8px}}
.dot{{border-radius:50%;background:{TEAL}}}
.f{{position:absolute;left:80px;right:80px;bottom:56px;display:flex;align-items:center;gap:20px;font-size:28px}}
.f img{{width:64px;height:64px;border-radius:50%;object-fit:cover}}"""
e = lambda s: html.escape(str(s))
PAL = {"cream": (CREAM, NAVY, BODY, TEALD, TEALD), "white": (W, NAVY, BODY, TEALD, TEALD), "dark": (POLAR, W, ONDARK, TEAL, TEAL)}
def rich(s, hi):
    p = e(s).split("**")
    return "".join(f'<span style="color:{hi}">{x}</span>' if i % 2 else x for i, x in enumerate(p))

def slide(s, i, n):
    bg, fg, body_c, eye, hi = PAL[s.get("bg", "cream")]
    eyebrow = f'<div class="e" style="color:{eye}">{e(s["eyebrow"])}</div>' if s.get("eyebrow") else ""
    size = s.get("size", 84)
    head = f'<div class="h" style="font-size:{size}px;color:{fg}">{rich(s["title"], hi)}</div>' if s.get("title") else ""
    sub = f'<div class="b" style="color:{body_c};margin-top:32px">{rich(s["sub"], hi)}</div>' if s.get("sub") else ""
    t = s["type"]; mid = ""; top = ""
    if t == "person":
        d = s.get("photo", 420)
        top = f'<img src="{PHOTO}" style="width:{d}px;height:{d}px;border-radius:50%;object-fit:cover;border:10px solid {TEAL};margin-bottom:48px">'
    elif t == "side":
        d = s.get("photo", 340)
        c = f'<div style="flex:1">{eyebrow}{head}{sub}</div><img src="{PHOTO}" style="flex:none;width:{d}px;height:{d}px;border-radius:50%;object-fit:cover;border:8px solid {TEAL}">'
        return page(bg, fg, body_c, f'<div style="display:flex;align-items:center;gap:56px">{c}</div>', i, n)
    elif t == "timeline":
        rows = ""
        for r in s["steps"]:
            if r.get("dots"):
                ds = "".join(f'<div class="dot" style="width:78px;height:78px;color:{NAVY};display:flex;align-items:center;justify-content:center;font-family:Raleway;font-weight:800;font-size:32px">{k+1}</div>' for k in range(r["dots"]))
                rows += f'<div class="card"><div style="display:flex;justify-content:space-between;margin-bottom:22px">{ds}</div><div class="t1">{e(r["head"])}</div><div class="t2">{e(r["sub"])}</div></div>'
            else:
                rows += f'<div class="card"><div class="t1">{e(r["head"])}</div><div class="t2">{e(r["sub"])}</div></div>'
        mid = f'<div style="display:flex;flex-direction:column;gap:18px;margin-top:{s.get("gap",36)}px">{rows}</div>'
    elif t == "grid":
        c = "".join(f'<div class="dot" style="width:46px;height:46px"></div>' for _ in range(s["cols"] * s["rows"]))
        grid = f'<div><div style="font-size:28px;color:{BODY};margin-bottom:14px">{e(s["xlabel"])}</div><div style="display:grid;grid-template-columns:repeat({s["cols"]},46px);gap:10px">{c}</div><div style="font-size:28px;color:{BODY};margin-top:14px">{e(s["ylabel"])}</div></div>'
        side = f'<div style="width:340px;padding-left:24px"><div class="h" style="font-size:100px;color:{NAVY}">{e(s["big"])}</div><div class="b" style="font-size:38px;color:{BODY};margin-top:8px">{e(s["bigsub"])}</div></div>'
        mid = f'<div class="card" style="margin-top:36px;display:flex;justify-content:space-between;align-items:center">{grid}{side}</div>'
    elif t == "cards":
        rows = "".join(f'<div class="card"><div class="t1">{e(r["benefit"])}</div><div class="t2">{e(r["feature"])}</div></div>' for r in s["rows"])
        mid = f'<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px">{rows}</div>'
    elif t == "cta":
        mid = f'<div style="margin-top:48px"><span style="display:inline-block;background:{CTA};color:{W};font-weight:700;font-size:42px;padding:32px 52px;border-radius:999px">{e(s["button"])}</span></div><div class="b" style="font-size:36px;color:{body_c};margin-top:32px">{e(s["url"])}</div>'
    return page(bg, fg, body_c, top + eyebrow + head + sub + mid, i, n)

def page(bg, fg, body_c, inner, i, n):
    arrow = f'<span style="margin-left:auto;font-size:48px;color:{body_c}">→</span>' if i < n - 1 else ""
    foot = f'<div class="f"><img src="{PHOTO}"><span style="color:{fg};font-weight:700">Holm Hänsel</span><span style="color:{body_c}">YOGA MACHT STARK</span>{arrow}</div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s" style="background:{bg};color:{fg}">{inner}{foot}</div></body></html>'

out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": SW, "height": SH})
    n = len(spec["slides"])
    for i, s in enumerate(spec["slides"]):
        pg.set_content(slide(s, i, n)); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / f"slide{i+1:02d}.png"))
    b.close()
