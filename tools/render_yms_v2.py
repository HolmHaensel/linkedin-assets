import json, sys, html, pathlib, base64, os
from playwright.sync_api import sync_playwright

# YMS "Der Kreis" style (v2). Usage: FONTDIR=tools/fonts-yms python3 tools/render_yms_v2.py spec.json outdir
# Style rules: yms/STYLE.md. Circles use carousel coordinates (x across all slides), so they run over the swipe seam.
L, W, R, K, M = "#f0f4f5", "#ffffff", "#e05252", "#2c3e50", "#607080"
spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
SW, SH = spec.get("canvas", [1080, 1350])
FD = os.environ.get("FONTDIR", "tools/fonts-yms")
def ff(name, f, w):
    b = base64.b64encode(open(f"{FD}/{f}", "rb").read()).decode()
    return f"@font-face{{font-family:'{name}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"
FONTS = "".join([ff("Raleway", f"raleway-latin-{w}-normal.woff2", w) for w in (700, 800, 900)] + [ff("Lato", f"lato-latin-{w}-normal.woff2", w) for w in (400, 700)])
CSS = FONTS + f"""*{{box-sizing:border-box;margin:0}}body{{width:{SW}px;height:{SH}px;font-family:Lato,sans-serif}}
.s{{position:relative;overflow:hidden;width:{SW}px;height:{SH}px}}
.c{{position:absolute;border-radius:50%}}
.a{{position:absolute;left:88px}}
.d{{font-family:Raleway;font-weight:900;text-transform:uppercase;letter-spacing:.002em;line-height:1.04;font-feature-settings:'lnum' 1}}
.b{{font-size:46px;line-height:1.32;font-feature-settings:'lnum' 1}}
.k{{font-weight:700;font-size:26px;letter-spacing:.2em;text-transform:uppercase}}
.f{{position:absolute;left:88px;right:88px;bottom:72px;display:flex;justify-content:space-between;align-items:center;font-size:26px;font-weight:700;letter-spacing:.04em}}
.h{{color:var(--hi)}}"""
e = lambda s: html.escape(str(s))
def rich(s):  # **word** marks the highlight color
    p = e(s).split("**")
    return "".join(f'<span class="h">{x}</span>' if i % 2 else x for i, x in enumerate(p))
PAL = {"light": (L, K, R), "white": (W, K, R), "dark": (K, W, R), "coral": (R, W, K)}

def slide(s, i, n, circles):
    bg, fg, hi = PAL[s.get("bg", "light")]
    x0 = i * SW
    deco = "".join(f'<div class="c" style="left:{c["x"]-c["r"]-x0}px;top:{c["y"]-c["r"]}px;width:{2*c["r"]}px;height:{2*c["r"]}px;background:{R}"></div>' for c in circles)
    body = ""
    top = s.get("top", 560)
    if s.get("kicker"):
        body += f'<div class="a k" style="top:{s.get("kickerTop", top-64)}px;color:{hi}">{e(s["kicker"])}</div>'
    if s["type"] == "statement":
        body += f'<div class="a" style="top:{top}px;width:{s.get("w",904)}px"><div class="d" style="font-size:{s.get("size",96)}px">{rich(s["title"])}</div>' + (f'<div class="b" style="margin-top:36px;width:{s.get("subw",s.get("w",904))}px">{rich(s["sub"])}</div>' if s.get("sub") else "") + "</div>"
    elif s["type"] == "scene":
        lines = "".join(f'<div class="d" style="font-size:{s.get("size",72)}px;margin-bottom:14px">{rich(x)}</div>' for x in s["lines"])
        body += f'<div class="a" style="top:{top}px;width:904px">{lines}<div class="b" style="margin-top:44px">{rich(s["sub"])}</div></div>'
    elif s["type"] == "fb":
        rows = "".join(f'<div style="padding:38px 0;border-top:3px solid {K}"><div class="k" style="color:{R};margin-bottom:12px">{e(r["stage"])}</div><div style="font-size:44px;font-weight:700;line-height:1.22;margin-bottom:10px">{e(r["benefit"])}</div><div style="font-size:36px;line-height:1.28;color:{M}">{e(r["feature"])}</div></div>' for r in s["rows"])
        body += f'<div class="a" style="top:{top}px;width:904px"><div class="d" style="font-size:{s.get("size",68)}px;margin-bottom:44px">{rich(s["title"])}</div>{rows}</div>'
    elif s["type"] == "timeline":
        def step(mark, head, sub):
            return f'<div style="display:flex;gap:36px;align-items:flex-start;padding:26px 0;border-top:3px solid {K}">{mark}<div><div style="font-size:42px;font-weight:700;line-height:1.2;margin-bottom:6px">{e(head)}</div><div style="font-size:36px;line-height:1.28;color:{M}">{e(sub)}</div></div></div>'
        ring = f'<div style="flex:none;width:56px;height:56px;border-radius:50%;border:10px solid {R}"></div>'
        rows = ""
        for r in s["steps"]:
            if r.get("dots"):
                dots = "".join(f'<div style="width:82px;height:82px;border-radius:50%;background:{R};color:{W};display:flex;align-items:center;justify-content:center;font-family:Raleway;font-weight:900;font-size:32px;font-feature-settings:\'lnum\' 1">{k+1}</div>' for k in range(r["dots"]))
                rows += f'<div style="padding:26px 0;border-top:3px solid {K}"><div style="display:flex;justify-content:space-between;margin-bottom:22px">{dots}</div><div style="font-size:42px;font-weight:700;line-height:1.2;margin-bottom:6px">{e(r["head"])}</div><div style="font-size:36px;line-height:1.28;color:{M}">{e(r["sub"])}</div></div>'
            else:
                rows += step(ring, r["head"], r["sub"])
        body += f'<div class="a" style="top:{top}px;width:{s.get("w",904)}px"><div class="d" style="font-size:{s.get("size",76)}px;margin-bottom:36px">{rich(s["title"])}</div>{rows}</div>'
    elif s["type"] == "html":
        body += s["html"]
    elif s["type"] == "grid":
        c = "".join(f'<div style="width:58px;height:58px;border-radius:50%;background:{R}"></div>' for _ in range(s["cols"] * s["rows"]))
        grid = f'<div style="display:grid;grid-template-columns:repeat({s["cols"]},58px);gap:14px">{c}</div>'
        side = f'<div style="width:300px"><div class="d" style="font-size:96px;color:{R}">{e(s["big"])}</div><div class="b" style="font-size:38px;margin-top:10px">{e(s["bigsub"])}</div></div>'
        body += f'<div class="a" style="top:{top}px;width:904px"><div class="d" style="font-size:{s.get("size",76)}px;margin-bottom:40px">{rich(s["title"])}</div><div class="k" style="color:{M};margin-bottom:18px">{e(s["xlabel"])}</div><div style="display:flex;justify-content:space-between;align-items:flex-end">{grid}{side}</div><div class="k" style="color:{M};margin-top:18px">{e(s["ylabel"])}</div><div class="b" style="margin-top:30px;font-size:40px">{rich(s["sub"])}</div></div>'
    elif s["type"] == "close":
        cy, r = s.get("cy", 640), s.get("r", 300)
        body += f'<div class="a" style="top:96px;width:904px"><div class="d" style="font-size:68px">{rich(s["title"])}</div></div>'
        body += f'<div class="c" style="left:{540-r}px;top:{cy-r}px;width:{2*r}px;height:{2*r}px;background:{R};display:flex;align-items:center;justify-content:center"><span class="d" style="font-size:{s.get("wordsize",150)}px;color:{W};text-align:center">{e(s["word"])}</span></div>'
        body += f'<div class="a b" style="top:{cy+r+44}px;width:904px;font-size:42px">{rich(s["sub"])}</div>'
    arrow = "→" if i < n - 1 else ""
    foot = f'<div class="f"><span><span style="font-family:Raleway;font-weight:900;font-size:30px;letter-spacing:.02em">Holm Hänsel</span><span style="font-weight:400;opacity:.8"> · YOGA MACHT STARK</span></span><span style="font-size:44px;color:{hi}">{arrow}</span></div>'
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="s" style="background:{bg};color:{fg};--hi:{hi}">{deco}{body}{foot}</div></body></html>'

out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": SW, "height": SH})
    n = len(spec["slides"])
    for i, s in enumerate(spec["slides"]):
        pg.set_content(slide(s, i, n, spec.get("circles", []))); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(200)
        pg.screenshot(path=str(out / f"slide{i+1:02d}.png"))
    b.close()
print("\n".join(str(x) for x in sorted(out.glob("*.png"))))
