import re, sys, base64, pathlib
from playwright.sync_api import sync_playwright
# Renders the canvas artboards to PNG for Metricool. Usage: export_design.py <project dir> <out dir> <repo root>
proj, out, repo = map(pathlib.Path, sys.argv[1:4])
out.mkdir(parents=True, exist_ok=True)
def b64(p): return base64.b64encode(pathlib.Path(p).read_bytes()).decode()
fd = repo / "tools/fonts-yms"
faces = "".join(f"@font-face{{font-family:'Raleway';font-weight:{w};src:url(data:font/woff2;base64,{b64(fd / f'raleway-latin-{w}-normal.woff2')}) format('woff2')}}" for w in (700, 800, 900))
faces += "".join(f"@font-face{{font-family:'Lato';font-weight:{w};src:url(data:font/woff2;base64,{b64(fd / f'lato-latin-{w}-normal.woff2')}) format('woff2')}}" for w in (400, 700))
photo = "data:image/jpeg;base64," + b64(repo / "tools/brand/holm-portrait.jpg")
with sync_playwright() as p:
    b = p.chromium.launch()
    for f in sys.argv[4:]:
        t = (proj / f"{f}.dc.html").read_text()
        body = re.search(r"<x-dc>(.*)</x-dc>", t, re.S).group(1)
        body = re.sub(r"<helmet>.*?</helmet>", "", body, flags=re.S)
        body = re.sub(r"/_blob/[0-9a-f]+", photo, body)
        w, h = map(int, re.search(r'"width":(\d+),"height":(\d+)', t).groups())
        pg = b.new_page(viewport={"width": w, "height": h})
        pg.set_content(f'<!doctype html><html lang="de"><head><meta charset="utf-8"><style>{faces}*{{box-sizing:content-box}}body{{margin:0}}</style></head><body>{body}</body></html>')
        pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(250)
        pg.screenshot(path=str(out / f"{f}.png")); pg.close()
    b.close()
