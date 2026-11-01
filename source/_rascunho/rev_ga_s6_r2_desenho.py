# Revisor ga_s6, rodada 2: desenha as figuras 2d (p01 a p08) com matplotlib, imitando o
# figura.js (poligono fechado com preenchimento leve, "aberto" sem fechar), para olhar o efeito.
# Uso: python -I rev_ga_s6_r2_desenho.py
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
COR = {1: "#356b73", 2: "#d4643f", 3: "#b5871f", 4: "#20251f"}

qs = []
for nome in ("ga_s6_p1.json", "ga_s6_p2.json"):
    with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
        qs += json.load(f)["questoes"]
qs = [q for q in qs if q["figura"]["modo"] == "2d"]

fig, eixos = plt.subplots(2, 4, figsize=(20, 10))
for ax, q in zip(eixos.flat, qs):
    for it in q["figura"]["itens"]:
        c = COR.get(it.get("cor", 4 if it["tipo"] == "ponto" else 1))
        if it["tipo"] == "poligono":
            xs = [p[0] for p in it["pts"]]
            ys = [p[1] for p in it["pts"]]
            if not it.get("aberto"):
                xs.append(xs[0]); ys.append(ys[0])
                ax.fill(xs, ys, color=c, alpha=0.10)
            ax.plot(xs, ys, color=c, lw=1.6)
        elif it["tipo"] == "segmento":
            ax.plot([it["de"][0], it["ate"][0]], [it["de"][1], it["ate"][1]], color=c if it.get("cor") else "#6a6f67",
                    lw=1.4, ls="--" if it.get("tracejado") else "-")
        elif it["tipo"] == "ponto":
            ax.plot([it["em"][0]], [it["em"][1]], "o", color=c)
            if it.get("rot"):
                ax.annotate(it["rot"], it["em"], xytext=(8, 8), textcoords="offset points")
    ax.axhline(0, color="#999", lw=0.8)
    ax.axvline(0, color="#999", lw=0.8)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    ax.set_title(q["id"] + ": " + q["enunciado"][:48], fontsize=9)
saida = os.path.join(AQUI, "rev_ga_s6_r2_figuras2d.png")
fig.tight_layout()
fig.savefig(saida, dpi=70)
print("gerado:", saida)
