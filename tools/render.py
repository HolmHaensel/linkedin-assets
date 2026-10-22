import json, sys, html, pathlib, base64, os
from playwright.sync_api import sync_playwright

# Usage: python3 render.py spec.json outdir
# spec: {"label":"...","slides":[{"type":"hook|text|list|stat|cta|quote|split|versus|number|html", "bg":"yellow|white|black" (optional), ...}]}
# Colors and fonts are fixed (CI). Layout may vary via types or "html" (body HTML using var(--y),var(--k),var(--w) and classes h1,h2,p,big,lab,box,item,n).
Y, K, W, G = "#F4D84A", "#121212", "#FAFAF7", "#555555"
FD = os.environ.get('FONTDIR','fonts')
def ff(name, path, w):
    b = base64.b64encode(open(path,'rb').read()).decode()
    return f"@font-face{{font-family:'{name}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
FONTS = ''.join([ff('Archivo', f'{FD}/fontsource-archivo/files/archivo-latin-{w}-normal.woff2', w) for w in (500,800,900)] + [ff('JBM', f'{FD}/fontsource-jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2', 500)])
CSS = FONTS + f""":root{{--y:{Y};--k:{K};--w:{W}}}*{{box-sizing:border-box;margin:0}}body{{width:1080px;height:1350px;font-family:'Archivo',sans-serif}}
.s{{width:1080px;height:1350px;padding:88px;display:flex;flex-direction:column;justify-content:space-between}}
.top{{display:flex;justify-content:space-between;font-family:'JBM',monospace;font-size:24px;letter-spacing:.06em;text-transform:uppercase}}
.h1{{font-size:128px;line-height:.95;font-weight:900;letter-spacing:-.035em}}
.h2{{font-size:84px;line-height:1;font-weight:800;letter-spacing:-.03em}}
.p{{font-size:46px;line-height:1.25;font-weight:500}}
.big{{font-size:230px;line-height:.9;font-weight:800;letter-spacing:-.05em}}
.box{{border-radius:10px;padding:56px}}
.item{{display:flex;gap:32px;align-items:center;border:3px solid {K};border-radius:10px;padding:36px 40px}}
.n{{font-size:76px;font-weight:800;min-width:110px}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;border-top:3px solid currentColor;padding-top:28px}}
.name{{font-size:32px;font-weight:700}}.role{{font-size:26px;font-weight:500}}
.lab{{font-family:'JBM',monospace;font-size:24px;letter-spacing:.06em;text-transform:uppercase}}"""
e = lambda s: html.escape(str(s))

def slide(s, label, i, n):
    t = s["type"]
    bg, fg = {"hook": (Y, K), "stat": (K, W), "cta": (K, W), "number": (Y, K), "quote": (W, K)}.get(t, (W, K))
    if s.get("bg"): bg, fg = {"yellow": (Y, K), "white": (W, K), "black": (K, W)}[s["bg"]]
    acc = Y if bg == K else K
    top = f'<div class="top"><span>{e(label)}</span><span>{f"{i:02d} / {n:02d}" if n > 1 else ""}</span></div>'
    foot = f'<div class="foot"><div><div class="name">Holm Hänsel</div><div class="role">{e(s.get("sign","Senior Product Strategist"))}</div></div><div class="lab">{e(s.get("cue","Swipe →" if i < n else ""))}</div></div>'
    if t == "hook":
        mid = f'<div style="display:flex;flex-direction:column;gap:44px"><div class="h1">{e(s["title"])}</div><div class="p" style="font-size:56px">{e(s.get("sub",""))}</div></div>'
        body = top + mid + foot
    elif t == "text":
        paras = "".join(f'<div class="p">{e(p)}</div>' for p in s.get("paras", []))
        box = f'<div class="box" style="background:{K};color:{W}"><div class="lab" style="color:{Y};margin-bottom:24px">{e(s.get("kicker",""))}</div><div class="h2" style="color:{W}">{e(s["title"])}</div></div>' if s.get("title") else ""
        body = top + f'<div style="display:flex;flex-direction:column;gap:40px">{paras}</div>' + box
    elif t == "list":
        items = "".join(f'<div class="item"><span class="n">{k+1:02d}</span><span class="p" style="font-size:42px">{e(x)}</span></div>' for k, x in enumerate(s["items"]))
        tail = f'<div class="box" style="background:{Y}"><div class="h2" style="font-size:58px">{e(s["punch"])}</div></div>' if s.get("punch") else ""
        body = top + (f'<div class="h2">{e(s["title"])}</div>' if s.get("title") else "") + f'<div style="display:flex;flex-direction:column;gap:22px">{items}</div>' + tail
    elif t == "stat":
        mid = f'<div><div class="big" style="color:{Y}">{e(s["number"])}</div><div class="p" style="margin-top:16px">{e(s["caption"])}</div></div>'
        lesson = f'<div style="border-top:3px solid {W};padding-top:40px"><div class="lab" style="color:{Y};margin-bottom:20px">{e(s.get("kicker","The lesson"))}</div><div class="h2" style="font-size:66px">{e(s["lesson"])}</div></div>'
        body = top + mid + lesson + foot
    elif t == "quote":
        mid = f'<div style="display:flex;flex-direction:column;gap:30px"><div style="font-size:260px;line-height:.6;font-weight:900;color:{Y if bg != Y else K};height:150px">&#8220;</div><div class="h2" style="font-size:78px">{e(s["text"])}</div><div class="lab">{e(s.get("by",""))}</div></div>'
        body = top + mid + foot
    elif t == "split":
        return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div style="width:1080px;height:1350px;display:flex;flex-direction:column"><div class="s" style="height:760px;background:{Y};color:{K};justify-content:space-between">{top}<div class="h1" style="font-size:112px">{e(s["title"])}</div></div><div class="s" style="height:590px;background:{K};color:{W};padding-top:56px"><div class="p">{e(s.get("sub",""))}</div><div class="foot" style="border-color:{W}"><div><div class="name">Holm Hänsel</div><div class="role">{e(s.get("sign","Senior Product Strategist"))}</div></div><div class="lab" style="color:{Y}">{e(s.get("cue","Swipe →" if i < n else ""))}</div></div></div></div></body></html>'
    elif t == "versus":
        L, R = s["before"], s["after"]
        mid = f'<div class="h2">{e(s.get("title",""))}</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:24px"><div class="box" style="border:3px solid {fg}"><div class="lab" style="margin-bottom:20px;opacity:.7">{e(s.get("left","Before"))}</div><div class="p" style="font-size:40px">{e(L)}</div></div><div class="box" style="background:{K if bg != K else Y};color:{W if bg != K else K}"><div class="lab" style="margin-bottom:20px;color:{Y if bg != K else K}">{e(s.get("right","After"))}</div><div class="p" style="font-size:40px">{e(R)}</div></div></div>'
        tail = f'<div class="box" style="background:{Y if bg != Y else K};color:{K if bg != Y else W}"><div class="lab" style="margin-bottom:16px">{e(s.get("kicker","The key move"))}</div><div class="h2" style="font-size:56px">{e(s["punch"])}</div></div>' if s.get("punch") else ""
        body = top + mid + tail
    elif t == "number":
        mid = f'<div><div class="big" style="font-size:300px">{e(s["number"])}</div><div class="p" style="font-size:52px;margin-top:20px">{e(s["caption"])}</div></div><div class="h2" style="font-size:64px">{e(s.get("lesson",""))}</div>'
        body = top + mid + foot
    elif t == "html":
        body = top + f'<div style="flex:1;display:flex;flex-direction:column;justify-content:center">{s["html"]}</div>' + foot
    else:  # cta
        mid = f'<div style="display:flex;flex-direction:column;gap:36px"><div class="lab" style="color:{Y}">{e(s.get("kicker",""))}</div><div class="h2">{e(s["title"])}</div><div class="p">{e(s.get("sub",""))}</div></div>'
        body = top + mid + foot
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s" style="background:{bg};color:{fg}">{body}</div></body></html>'

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
