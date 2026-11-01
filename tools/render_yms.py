import json, sys, html, pathlib, base64, os
from playwright.sync_api import sync_playwright

# YOGA MACHT STARK renderer (CI V1.0). Usage: FONTDIR=tools/fonts-yms python3 tools/render_yms.py spec.json outdir
# spec: {"label":"...","slides":[{"type":"hook|split|quote|list|versus|text|cta|html", "bg":"light|white|red|dark|teal" (optional), ...}]}
# CI fixed: dominant accent coral red #e05252, white #ffffff, light mint-grey #f0f4f5, text #2c3e50 / #607080, teal #4db8b0 / #3a9e97 only as secondary.
# Headlines Raleway in ALLCAPS, text Lato. Signature element: large circle in the accent color.
# html type: body HTML using classes h1,h2,p,lab,box,item,n,acc,circle and colors var(--l),var(--w),var(--t),var(--td),var(--r),var(--k),var(--m).
L, Wh, T, TD, R, K, M = "#f0f4f5", "#ffffff", "#4db8b0", "#3a9e97", "#e05252", "#2c3e50", "#607080"
FD = os.environ.get('FONTDIR', 'fonts-yms')
def ff(name, f, w):
    b = base64.b64encode(open(f'{FD}/{f}', 'rb').read()).decode()
    return f"@font-face{{font-family:'{name}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
FONTS = ''.join([ff('Raleway', f'raleway-latin-{w}-normal.woff2', w) for w in (700, 800, 900)] + [ff('Lato', f'lato-latin-{w}-normal.woff2', w) for w in (400, 700)])
CSS = FONTS + f""":root{{--l:{L};--w:{Wh};--t:{T};--td:{TD};--r:{R};--k:{K};--m:{M}}}*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1350px;font-family:'Lato',sans-serif;font-feature-settings:'lnum' 1}}
.s{{position:relative;overflow:hidden;width:1080px;height:1350px;padding:88px;display:flex;flex-direction:column;justify-content:space-between}}
.s>*{{position:relative;z-index:1}}
.circle{{position:absolute!important;z-index:0!important;border-radius:50%}}
.top{{display:flex;justify-content:space-between;align-items:center;font-family:'Lato';font-weight:700;font-size:24px;letter-spacing:.16em;text-transform:uppercase}}
.h1{{font-family:'Raleway';font-size:100px;line-height:1.02;font-weight:900;letter-spacing:.005em;text-transform:uppercase}}
.h2{{font-family:'Raleway';font-size:64px;line-height:1.08;font-weight:900;letter-spacing:.01em;text-transform:uppercase}}
.p{{font-size:44px;line-height:1.35;font-weight:400}}
.lab{{font-weight:700;font-size:24px;letter-spacing:.16em;text-transform:uppercase}}
.box{{border-radius:24px;padding:56px}}
.item{{display:flex;gap:32px;align-items:center;background:{Wh};border-radius:24px;padding:36px 40px}}
.n{{font-family:'Raleway';font-size:60px;font-weight:900;min-width:96px;color:{R}}}
.acc{{display:inline-block;width:96px;height:10px;border-radius:5px;background:{R}}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;padding-top:28px;border-top:3px solid currentColor}}
.name{{font-family:'Raleway';font-size:30px;font-weight:900;letter-spacing:.06em}}.role{{font-size:24px;font-weight:400;opacity:.85}}"""
e = lambda s: html.escape(str(s))
# bg, text, accent
PAL = {"light": (L, K, R), "white": (Wh, K, R), "red": (R, Wh, Wh), "dark": (K, Wh, R), "teal": (T, K, K)}
DEF = {"hook": "light", "split": "white", "quote": "white", "list": "light", "versus": "white", "text": "white", "cta": "red", "html": "light"}

def slide(s, label, i, n):
    t = s["type"]
    key = s.get("bg") or DEF.get(t, "light")
    bg, fg, ac = PAL[key]
    num = f"{i:02d} / {n:02d}" if n > 1 else ""
    top = f'<div class="top"><span>{e(label)}</span><span>{num}</span></div>'
    cue = s.get("cue", "Swipe →" if i < n else "")
    foot = f'<div class="foot"><div><div class="name">YOGA MACHT STARK</div><div class="role">{e(s.get("sign","@yoga.macht.stark"))}</div></div><div class="lab" style="color:{ac}">{e(cue)}</div></div>'
    def wrap(body, b=bg, f=fg, deco=""):
        return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s" style="background:{b};color:{f}">{deco}{body}</div></body></html>'
    circ_col = R if key in ("light", "white") else (Wh if key == "red" else R)
    if t == "hook":
        deco = f'<div class="circle" style="width:760px;height:760px;right:-260px;top:-240px;background:{circ_col};opacity:{".18" if key=="red" else "1"}"></div>'
        top2 = f'<div class="top"><span>{e(label)}</span><span style="color:{Wh if key in ("light","white") else fg}">{num}</span></div>'
        mid = f'<div style="display:flex;flex-direction:column;gap:40px;margin-top:300px"><div class="h1">{e(s["title"])}</div><div class="p" style="font-size:50px">{e(s.get("sub",""))}</div></div>'
        return wrap(top2 + mid + foot, deco=deco)
    if t == "split":
        return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;display:flex;flex-direction:column"><div class="s" style="height:760px;background:{R};color:{Wh}"><div class="circle" style="width:520px;height:520px;right:-180px;bottom:-200px;background:{Wh};opacity:.16"></div>{top}<div class="h1" style="font-size:92px">{e(s["title"])}</div></div><div class="s" style="height:590px;background:{Wh};color:{K};padding-top:56px"><div class="p">{e(s.get("sub",""))}</div><div class="foot"><div><div class="name">YOGA MACHT STARK</div><div class="role">{e(s.get("sign","@yoga.macht.stark"))}</div></div><div class="lab" style="color:{R}">{e(cue)}</div></div></div></div></body></html>'
    if t == "quote":
        qc = Wh if key in ("light", "white") else bg
        mid = f'<div style="display:flex;flex-direction:column;gap:44px"><div style="width:200px;height:200px;border-radius:50%;background:{circ_col};display:flex;align-items:center;justify-content:center"><span style="font-family:Raleway;font-size:240px;font-weight:900;line-height:1;color:{qc};margin-top:120px">&#8220;</span></div><div class="h2" style="font-size:70px">{e(s["text"])}</div><div class="lab" style="color:{ac}">{e(s.get("by",""))}</div></div>'
        return wrap(top + mid + foot)
    if t == "list":
        items = "".join(f'<div class="item" style="color:{K}"><span class="n">{k+1:02d}</span><span class="p" style="font-size:40px">{e(x)}</span></div>' for k, x in enumerate(s["items"]))
        tail = f'<div class="box" style="background:{R};color:{Wh}"><div class="h2" style="font-size:48px">{e(s["punch"])}</div></div>' if s.get("punch") else ""
        return wrap(top + (f'<div class="h2">{e(s["title"])}</div>' if s.get("title") else "") + f'<div style="display:flex;flex-direction:column;gap:22px">{items}</div>' + tail)
    if t == "versus":
        mid = f'<div class="h2">{e(s.get("title",""))}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px"><div class="box" style="background:{L};color:{M}"><div class="lab" style="margin-bottom:20px">{e(s.get("left","Vorher"))}</div><div class="p" style="font-size:40px;color:{K}">{e(s["before"])}</div></div><div class="box" style="background:{R};color:{Wh}"><div class="lab" style="margin-bottom:20px">{e(s.get("right","Nachher"))}</div><div class="p" style="font-size:40px">{e(s["after"])}</div></div></div>'
        tail = f'<div class="box" style="background:{K};color:{Wh}"><div class="lab" style="margin-bottom:16px;color:{R}">{e(s.get("kicker","Der Unterschied"))}</div><div class="h2" style="font-size:48px">{e(s["punch"])}</div></div>' if s.get("punch") else ""
        return wrap(top + mid + tail)
    if t == "text":
        paras = "".join(f'<div class="p">{e(p)}</div>' for p in s.get("paras", []))
        box = f'<div class="box" style="background:{R};color:{Wh}"><div class="lab" style="margin-bottom:24px">{e(s.get("kicker",""))}</div><div class="h2">{e(s["title"])}</div></div>' if s.get("title") else ""
        return wrap(top + f'<div style="display:flex;flex-direction:column;gap:40px">{paras}</div>' + box)
    if t == "html":
        return wrap(top + f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">{s["html"]}</div>' + foot)
    # cta
    deco = f'<div class="circle" style="width:640px;height:640px;left:-220px;bottom:-260px;background:{Wh if key=="red" else R};opacity:{".16" if key=="red" else "1"}"></div>'
    mid = f'<div style="display:flex;flex-direction:column;gap:36px"><div class="lab">{e(s.get("kicker",""))}</div><div class="h2">{e(s["title"])}</div><div class="p">{e(s.get("sub",""))}</div></div>'
    return wrap(top + mid + foot, deco=deco)

spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1350})
    n = len(spec["slides"])
    for i, s in enumerate(spec["slides"], 1):
        pg.set_content(slide(s, spec["label"], i, n)); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / f"slide{i:02d}.png"))
    b.close()
print("\n".join(str(x) for x in sorted(out.glob("*.png"))))
