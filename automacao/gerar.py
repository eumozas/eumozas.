#!/usr/bin/env python3
"""
Gerador de artes do Instagram @moisesbsilvaa.

Uso:
    python3 automacao/gerar.py automacao/dias/AAAA-MM-DD.json [--push]

Lê uma lista de posts em JSON, gera as artes em 1080x1350 (4:5, o máximo que a
API do Instagram aceita) em posts/AAAA-MM-DD/ e, com --push, envia ao GitHub e
imprime a URL pública de cada imagem (para usar no Metricool).

Tipos de post e campos (use <em>palavra</em> para destacar em dourado):
  noticia : tag, destaque, destaque_label, foto (opcional), titulo, topicos[], categoria, fontes
  frase   : foto, eyebrow, titulo, texto (opcional)
  ia      : numero, titulo, texto
  servico : eyebrow, titulo, itens[], cta
  boanoite: titulo, texto
Campos comuns: hora ("HH:MM"), legenda, alt
"""
import json, os, re, subprocess, sys, html
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
AUTO = RAIZ / "automacao"
FONTES_DIR = AUTO / ".fontes"
FOTOS = AUTO / "fotos"
REPO_RAW = "https://raw.githubusercontent.com/eumozas/eumozas./main/"

# Enquadramento de cada foto quando usada como fundo (background-position).
FOCO = {
    "retrato-pb.jpg": "50% 22%",
    "notebook-sofa.jpg": "70% 42%",
    "aviao.jpg": "50% 55%",
    "pensativo.jpg": "40% 30%",
    "selfie-mesa.jpg": "65% 40%",
    "cidade.jpg": "50% 50%",
}


def garantir_fontes():
    b = FONTES_DIR / "node_modules/@fontsource/bebas-neue/files/bebas-neue-latin-400-normal.woff2"
    if not b.exists():
        FONTES_DIR.mkdir(parents=True, exist_ok=True)
        subprocess.run(["npm", "i", "--silent", "--prefix", str(FONTES_DIR),
                        "@fontsource/bebas-neue@5.0.21", "@fontsource/source-sans-3@5.0.21"], check=True)
    nm = FONTES_DIR / "node_modules/@fontsource"
    return f"""
@font-face{{font-family:'B';src:url('file://{nm}/bebas-neue/files/bebas-neue-latin-400-normal.woff2')}}
@font-face{{font-family:'S';font-weight:400;src:url('file://{nm}/source-sans-3/files/source-sans-3-latin-400-normal.woff2')}}
@font-face{{font-family:'S';font-weight:600;src:url('file://{nm}/source-sans-3/files/source-sans-3-latin-600-normal.woff2')}}
@font-face{{font-family:'S';font-weight:700;src:url('file://{nm}/source-sans-3/files/source-sans-3-latin-700-normal.woff2')}}
"""


def t(s):
    """Escapa texto mas preserva <em>…</em> e <br>."""
    s = html.escape(s or "")
    for tag in ("em", "b", "br"):
        s = s.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return s


def plain(s):
    return re.sub(r"<[^>]+>", "", s or "")


def foto_url(nome):
    if not nome:
        return ""
    p = Path(nome)
    if not p.is_absolute():
        p = FOTOS / nome
    return p.as_uri()


BASE_CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;overflow:hidden;position:relative;font-family:S,sans-serif}
em{font-style:normal;color:#e8b44f}
.av{display:flex;align-items:center;gap:18px}
.av img{width:84px;height:84px;border-radius:50%;object-fit:cover;object-position:center 22%;filter:grayscale(1)}
.av b{display:block;font-size:34px;font-weight:700;line-height:1.1}
.av span{font-size:25px}
.dk .av img{box-shadow:0 0 0 3px #0d0d0d,0 0 0 6px #d9d9d9}.dk .av span{color:#9a9a9a}
.lt .av img{box-shadow:0 0 0 3px #f6f3ee,0 0 0 6px #1a1a1a}.lt .av span{color:#6b6b6b}
"""


def avatar():
    return (f'<div class="av"><img src="{foto_url("retrato-pb.jpg")}"><div><b>Moises Silva</b>'
            f'<span>@moisesbsilvaa</span></div></div>')


def tam(texto, regras):
    n = len(plain(texto))
    for limite, px in regras:
        if n <= limite:
            return px
    return regras[-1][1]


def html_noticia(p):
    foto = p.get("foto")
    topo = (f'background:linear-gradient(180deg,rgba(13,13,13,.25),rgba(13,13,13,.55) 60%,#0d0d0d),'
            f'url({foto_url(foto)}) {FOCO.get(foto,"50% 30%")}/cover' if foto else
            'background:radial-gradient(circle at 50% 45%,#3a3a3a,#141414 75%)')
    topicos = "".join(f'<div class="f"><i></i><div>{t(x)}</div></div>' for x in p.get("topicos", [])[:3])
    fs = tam(p["titulo"], [(60, 70), (85, 62), (110, 56), (999, 50)])
    return f"""<body class="dk" style="background:#0d0d0d;color:#fff">
<style>
.top{{position:absolute;left:0;right:0;top:0;height:560px;{topo}}}
.grid{{position:absolute;inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px),repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px)}}
.tag{{position:absolute;top:44px;left:50%;transform:translateX(-50%);font-size:20px;font-weight:700;letter-spacing:.22em;color:#ddd;background:rgba(0,0,0,.5);padding:9px 18px;border-radius:999px;white-space:nowrap;text-transform:uppercase}}
.dest{{position:absolute;left:0;right:0;top:120px;text-align:center}}
.dest b{{display:block;font-family:B;font-size:230px;line-height:.85;text-shadow:0 10px 40px rgba(0,0,0,.5)}}
.dest span{{display:block;font-family:B;font-size:46px;letter-spacing:.04em;color:#e8b44f;margin-top:6px}}
.fade{{position:absolute;left:0;right:0;top:440px;height:130px;background:linear-gradient(180deg,rgba(13,13,13,0),#0d0d0d)}}
.corpo{{position:absolute;left:84px;right:84px;top:540px}}
h1{{font-size:{fs}px;font-weight:700;line-height:1.08}}
.fx{{margin-top:26px;display:grid;gap:12px}}
.f{{display:flex;gap:16px;font-size:28px;line-height:1.35;color:#cfcfcf}}
.f i{{flex:none;width:12px;height:12px;margin-top:12px;background:#e8b44f}}
.f b{{color:#fff}}
.cat{{position:absolute;left:84px;bottom:180px;font-size:30px;font-weight:600;letter-spacing:.04em;display:flex;align-items:center;gap:14px;text-transform:uppercase}}
.cat::before{{content:"";width:3px;height:30px;background:#e8b44f}}
.av{{position:absolute;right:84px;bottom:155px}}
.q{{position:absolute;left:84px;right:84px;bottom:52px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid #333;padding-top:20px}}
.q b{{font-family:B;font-size:50px;color:#e8b44f}}
.q span{{font-size:17px;color:#8a8a8a;text-align:right;max-width:430px;line-height:1.35}}
</style>
<div class="top"><div class="grid"></div>
 <div class="dest"><b>{t(p.get("destaque",""))}</b><span>{t(p.get("destaque_label",""))}</span></div>
 <div class="fade"></div></div>
<div class="tag">{t(p.get("tag","Notícia"))}</div>
<div class="corpo"><h1>{t(p["titulo"])}</h1>
<div class="fx">{topicos}</div></div>
<div class="cat">{t(p.get("categoria","Brasil"))}</div>
{avatar()}
<div class="q"><b>O que você acha disso?</b><span>Fontes: {t(p.get("fontes",""))}</span></div>
</body>"""


def html_frase(p):
    foto = p.get("foto", "notebook-sofa.jpg")
    fs = tam(p["titulo"], [(30, 150), (55, 120), (85, 100), (999, 84)])
    texto = f'<p>{t(p["texto"])}</p>' if p.get("texto") else ""
    return f"""<body class="dk" style="background:#0d0d0d;color:#fff">
<style>
.ph{{position:absolute;inset:0;background:url({foto_url(foto)}) {FOCO.get(foto,"50% 40%")}/cover}}
.ph::after{{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,13,13,.55) 0%,rgba(13,13,13,0) 22%,rgba(13,13,13,.15) 40%,rgba(13,13,13,.85) 62%,#0d0d0d 82%)}}
.brand{{position:absolute;left:76px;top:62px;font-family:B;font-size:44px;letter-spacing:.02em}}
.brand em{{color:#e8b44f}}
.box{{position:absolute;left:76px;right:76px;bottom:200px}}
.eb{{font-family:B;font-size:40px;letter-spacing:.06em;color:#e8b44f}}
h1{{font-family:B;font-size:{fs}px;line-height:.92;letter-spacing:.005em;margin-top:6px;text-transform:uppercase}}
p{{font-size:32px;line-height:1.38;color:rgba(255,255,255,.82);margin-top:20px;max-width:880px}}
.av{{position:absolute;left:76px;bottom:62px}}
.sv{{position:absolute;right:76px;bottom:88px;font-size:24px;font-weight:600;color:rgba(255,255,255,.7)}}
</style>
<div class="ph"></div>
<div class="brand">Moises <em>Silva</em></div>
<div class="box"><div class="eb">{t(p.get("eyebrow",""))}</div><h1>{t(p["titulo"])}</h1>{texto}</div>
{avatar()}<div class="sv">Salve e compartilhe 🔖</div>
</body>"""


def html_ia(p):
    fs = tam(p["titulo"], [(35, 130), (60, 110), (90, 92), (999, 80)])
    return f"""<body class="dk" style="background:#000;color:#f4efe6">
<style>
body{{display:flex;flex-direction:column;justify-content:center;padding:0 90px}}
.tag{{position:absolute;top:70px;left:90px;font-family:B;font-size:36px;letter-spacing:.08em;color:#e8b44f}}
.tag b{{color:#000;background:#e8b44f;padding:0 10px;border-radius:6px;margin-left:8px;font-weight:400}}
.av{{margin-bottom:40px}}
h1{{font-family:B;font-size:{fs}px;line-height:.95;letter-spacing:.005em;text-transform:uppercase}}
p{{margin-top:34px;font-size:34px;line-height:1.42;color:#b9b2a5}}
.foot{{position:absolute;left:90px;right:90px;bottom:64px;display:flex;justify-content:space-between;font-size:24px;font-weight:600;color:#6f6a61}}
</style>
<div class="tag">IA no dia a dia <b>#{int(p.get("numero",1)):02d}</b></div>
{avatar()}
<h1>{t(p["titulo"])}</h1>
<p>{t(p.get("texto",""))}</p>
<div class="foot"><span>Salve para lembrar 🔖</span><span>moisessilva.netlify.app</span></div>
</body>"""


def html_servico(p):
    itens = "".join(f'<div class="it"><i>✓</i><div>{t(x)}</div></div>' for x in p.get("itens", [])[:4])
    fs = tam(p["titulo"], [(30, 140), (55, 112), (999, 92)])
    return f"""<body class="lt" style="background:#f6f3ee;color:#15130f">
<style>
.brand{{position:absolute;left:76px;top:62px;font-family:B;font-size:44px}}
.brand em{{color:#c9853a}}
.main{{position:absolute;left:76px;right:76px;top:180px}}
.eb{{font-family:B;font-size:40px;letter-spacing:.06em;color:#c9853a}}
h1{{font-family:B;font-size:{fs}px;line-height:.92;text-transform:uppercase;margin-top:6px}}
h1 em{{color:#c9853a}}
.items{{margin-top:36px;display:grid;gap:16px}}
.it{{display:flex;align-items:center;gap:22px;padding:24px 28px;border-radius:24px;background:#fff;border:2px solid #e2dcd2;font-size:30px;font-weight:600}}
.it i{{font-style:normal;flex:none;width:52px;height:52px;border-radius:50%;background:#15130f;color:#e8b44f;display:grid;place-items:center;font-size:26px;font-weight:800}}
.cta{{position:absolute;left:76px;right:76px;bottom:190px;display:flex;justify-content:space-between;align-items:center;padding:28px 34px;border-radius:26px;background:#15130f;color:#fff}}
.cta b{{font-family:B;font-size:46px;letter-spacing:.02em}}
.cta span{{font-size:24px;color:#e8b44f;font-weight:700}}
.av{{position:absolute;left:76px;bottom:62px}}
</style>
<div class="brand">Moises <em>Silva</em></div>
<div class="main"><div class="eb">{t(p.get("eyebrow","Serviços"))}</div>
<h1>{t(p["titulo"])}</h1>
<div class="items">{itens}</div></div>
<div class="cta"><b>{t(p.get("cta","Diagnóstico grátis"))}</b><span>moisessilva.netlify.app</span></div>
{avatar()}
</body>"""


def html_boanoite(p):
    fs = tam(p["titulo"], [(40, 110), (70, 92), (999, 80)])
    return f"""<body class="dk" style="background:#05070d;color:#fff">
<style>
.sky{{position:absolute;inset:0;background:radial-gradient(circle at 75% 18%,rgba(232,180,79,.22),transparent 30%),linear-gradient(180deg,#0b1430,#05070d 70%)}}
.moon{{position:absolute;right:120px;top:120px;width:170px;height:170px;border-radius:50%;background:radial-gradient(circle at 38% 35%,#fff8e1,#f1dca4 60%,#d9bd78);box-shadow:0 0 90px rgba(243,227,184,.45)}}
.stars{{position:absolute;inset:0;background-image:radial-gradient(2px 2px at 10% 20%,#fff,transparent),radial-gradient(2px 2px at 30% 8%,#fff,transparent),radial-gradient(1.5px 1.5px at 55% 25%,#fff,transparent),radial-gradient(2px 2px at 20% 40%,#fff,transparent),radial-gradient(1.5px 1.5px at 45% 12%,#fff,transparent),radial-gradient(2px 2px at 62% 38%,#fff,transparent),radial-gradient(1.5px 1.5px at 88% 45%,#fff,transparent),radial-gradient(2px 2px at 8% 55%,#fff,transparent);opacity:.8}}
.box{{position:absolute;left:84px;right:84px;top:440px}}
.eb{{font-family:B;font-size:170px;line-height:.9;color:#e8b44f}}
h1{{font-size:{fs*0.7:.0f}px;font-weight:700;line-height:1.15;margin-top:34px}}
p{{font-size:34px;line-height:1.4;color:#b7bfd6;margin-top:26px}}
.av{{position:absolute;left:84px;bottom:70px}}
</style>
<div class="sky"></div><div class="stars"></div><div class="moon"></div>
<div class="box"><div class="eb">Boa noite</div><h1>{t(p["titulo"])}</h1><p>{t(p.get("texto",""))}</p></div>
{avatar()}
</body>"""


MODELOS = {"noticia": html_noticia, "frase": html_frase, "ia": html_ia, "servico": html_servico, "boanoite": html_boanoite}


def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    arq = Path(sys.argv[1]).resolve()
    dia = arq.stem
    posts = json.loads(arq.read_text(encoding="utf-8"))
    css_fontes = garantir_fontes()
    saida = RAIZ / "posts" / dia
    saida.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageCms
    srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
    tmp = AUTO / ".tmp"; tmp.mkdir(exist_ok=True)
    gerados = []
    with sync_playwright() as pw:
        nav = pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        for p in posts:
            corpo = MODELOS[p["tipo"]](p)
            doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{css_fontes}{BASE_CSS}</style></head>{corpo}</html>"
            h = tmp / "post.html"; h.write_text(doc, encoding="utf-8")
            pg.goto(h.as_uri(), wait_until="load")
            pg.evaluate("Promise.all([document.fonts.ready,...[...document.images].map(i=>i.decode().catch(()=>{}))])")
            pg.wait_for_timeout(400)
            png = tmp / "post.png"; pg.screenshot(path=str(png))
            nome = f'{p["hora"].replace(":","")}-{p["tipo"]}.jpg'
            Image.open(png).convert("RGB").resize((1080, 1350), Image.LANCZOS).save(
                saida / nome, quality=95, subsampling=0, icc_profile=srgb)
            gerados.append((p["hora"], f"posts/{dia}/{nome}"))
        nav.close()
    if "--push" in sys.argv:
        subprocess.run(["git", "-C", str(RAIZ), "add", f"posts/{dia}"], check=True)
        subprocess.run(["git", "-C", str(RAIZ), "-c", "user.name=Moises Silva", "-c", "user.email=moisesueli@gmail.com",
                        "commit", "-qm", f"Artes do dia {dia}"], check=False)
        subprocess.run(["git", "-C", str(RAIZ), "pull", "-q", "--rebase", "origin", "main"], check=False)
        subprocess.run(["git", "-C", str(RAIZ), "push", "-q", "origin", "main"], check=True)
    for hora, caminho in gerados:
        print(f"{hora}\t{REPO_RAW}{caminho}")


if __name__ == "__main__":
    main()
