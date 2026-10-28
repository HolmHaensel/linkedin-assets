import base64, sys
from playwright.sync_api import sync_playwright

LAV, D, W, CARD, RED, RED2 = "#B9A9DC", "#17142B", "#FAFAF7", "#F2EFE8", "#B8423A", "#C2574E"
OUT = sys.argv[1] if len(sys.argv) > 1 else "v3.png"
FD = "/home/claude/linkedin-assets/tools/fonts"

def ff(name, path, w):
    b = base64.b64encode(open(path, 'rb').read()).decode()
    return f"@font-face{{font-family:'{name}';font-weight:{w};src:url(data:font/woff2;base64,{b}) format('woff2')}}"

FONTS = ''.join([ff('Archivo', f'{FD}/fontsource-archivo/files/archivo-latin-{w}-normal.woff2', w) for w in (500, 800, 900)]
                + [ff('JBM', f'{FD}/fontsource-jetbrains-mono/files/jetbrains-mono-latin-500-normal.woff2', 500)])

def drop(w, h, hl=True):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 76 96"><path d="M38 2 C38 2 4 44 4 62 a34 34 0 0 0 68 0 C72 44 38 2 38 2Z" fill="{RED}"/>'
            + (f'<path d="M22 60 q0 -12 8 -20" stroke="#E79A92" stroke-width="5" fill="none" stroke-linecap="round"/>' if hl else '') + '</svg>')

items = [("01", "One lab report. Five audiences.", "Doctors, coaches, partners, apps, customers."),
         ("02", "Clear first. Depth second.", "The deep work stays with the partner."),
         ("03", "AI drafts. An expert approves.", "Never the other way round.")]
rows = ''.join(f'<div class="item"><div class="n">{drop(26,33,False)}<span>{n}</span></div><div><div class="t">{t}</div><div class="d">{d}</div></div></div>' for n, t, d in items)
dots = ''.join(f'<div class="ring"><div class="dot" style="background:{c}"></div></div>' for c in (RED, RED2, RED2, RED))

HTML = f"""<!doctype html><html><head><meta charset="utf-8"><style>{FONTS}
*{{box-sizing:border-box;margin:0}}
body{{width:1080px;height:1350px;font-family:'Archivo',sans-serif;background:{W};color:{D}}}
.top{{height:660px;background:{LAV};padding:80px 88px;position:relative}}
.lab{{font-family:'JBM',monospace;font-size:24px;letter-spacing:.08em;text-transform:uppercase}}
.h1{{font-size:84px;line-height:.98;font-weight:900;letter-spacing:-.035em;margin-top:72px;width:640px}}
.ill{{position:absolute;right:88px;top:170px;width:250px}}
.ill .dr{{display:flex;justify-content:center}}
.card{{margin-top:22px;background:{CARD};border-radius:18px;padding:22px 20px;border:3px solid {D}}}
.card .ct{{font-family:'JBM',monospace;font-size:15px;letter-spacing:.14em;padding-bottom:12px;border-bottom:2px solid #DDD8CE}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:18px 4px 14px}}
.ring{{width:92px;height:92px;border:2px dashed #BDB7AC;border-radius:50%;display:flex;align-items:center;justify-content:center}}
.dot{{width:62px;height:62px;border-radius:50%}}
.kit{{font-family:'JBM',monospace;font-size:14px;color:#6C6779;letter-spacing:.08em}}
.bot{{height:690px;padding:44px 88px 72px;display:flex;flex-direction:column;justify-content:space-between}}
.item{{display:flex;gap:30px;align-items:center;border-bottom:3px solid {LAV};padding:24px 0}}
.n{{display:flex;align-items:center;gap:12px;font-family:'JBM',monospace;font-size:30px;min-width:100px}}
.t{{font-size:44px;font-weight:800;letter-spacing:-.02em}}
.d{{font-size:29px;font-weight:500;margin-top:6px;opacity:.72}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;border-top:3px solid {D};padding-top:24px}}
.name{{font-size:32px;font-weight:800}}.role{{font-size:26px;font-weight:500}}
</style></head><body>
<div class="top"><div class="lab">In the making &middot; HealthBioCare &times; Holm H&auml;nsel</div>
<div class="h1">A few drops<br>of blood.<br>A result people<br>can act on.</div>
<div class="ill"><div class="dr">{drop(84,106)}</div>
<div class="card"><div class="ct">SAMPLE CARD</div><div class="grid">{dots}</div><div class="kit">KIT &middot; XXX-XXX-XXX</div></div></div>
</div>
<div class="bot"><div>{rows}</div>
<div class="foot"><div><div class="name">Holm H&auml;nsel</div><div class="role">I design products that cannot afford to fail.</div></div><div class="lab">Vienna &middot; 2026</div></div></div>
</body></html>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1080, "height": 1350})
    pg.set_content(HTML)
    pg.wait_for_timeout(300)
    pg.screenshot(path=OUT)
    b.close()
print(OUT)
