# Monta uma pagina de teste que desenha as 12 figuras do lote ga_s6 com o proprio
# figura.js do site, para conferir o desenho (curvas abertas, preenchimento, focos).
# Uso: python -I rev_ga_s6_figuras_html.py "<html de saida>"
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
GER = os.path.dirname(AQUI)


def ler(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


figs = []
for nome in ("ga_s6_p1.json", "ga_s6_p2.json"):
    d = json.loads(ler(os.path.join(GER, "dados", nome)))
    for q in d["questoes"]:
        figs.append({"id": q["id"], "fig": q["figura"]})

js = ler(os.path.join(GER, "site", "figura.js"))
dados = json.dumps(figs, ensure_ascii=False).replace("</", "<\\/")
html = """<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Figuras s6</title>
<style>body{font-family:system-ui;background:#fffdf8;margin:16px}
.g{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.c{border:1px solid #d9d2c5;padding:6px}canvas{width:100%;height:300px;display:block}
p{margin:4px 0;font-size:13px}</style></head><body><div class="g" id="g"></div>
<script>""" + js.replace("</script", "<\\/script") + """</script>
<script>var F = """ + dados + """;
F.forEach(function (f) {
  var d = document.createElement('div'); d.className = 'c';
  d.innerHTML = '<p><b>' + f.id + '</b> ' + (f.fig.legenda || '') + '</p><canvas></canvas>';
  document.getElementById('g').appendChild(d);
  Figura.montar(d.querySelector('canvas'), f.fig);
});</script></body></html>"""
with open(sys.argv[1], "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print("gerado:", sys.argv[1], len(figs), "figuras")
