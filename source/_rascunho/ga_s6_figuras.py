# Gera os itens das figuras do lote ga_s6 (Geometria Analitica, semana 6).
# Saida: ga_s6_figuras_saida.txt na mesma pasta, um bloco "itens" por questao.
import json
import math
import os

AQUI = os.path.dirname(os.path.abspath(__file__))


def r(v):
    v = round(v, 3)
    if v == 0:
        v = 0.0
    if abs(v - round(v)) < 1e-9:
        return int(round(v))
    return v


def pt(*c):
    return [r(x) for x in c]


def ida_volta(pts):
    # curva aberta desenhada como poligono de ida e volta pelos mesmos pontos,
    # para o fechamento do poligono nao criar uma corda falsa
    return pts + pts[-2:0:-1]


def lin(a, b, n):
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def elipse2d(h, k, ax, by, n=40):
    return [pt(h + ax * math.cos(2 * math.pi * i / n), k + by * math.sin(2 * math.pi * i / n)) for i in range(n)]


def poli(pts, cor=1):
    return {"tipo": "poligono", "pts": pts, "cor": cor}


def ponto(c, rot):
    return {"tipo": "ponto", "em": pt(*c), "rot": rot}


def seg(a, b, cor=3, tracejado=False):
    d = {"tipo": "segmento", "de": pt(*a), "ate": pt(*b), "cor": cor}
    if tracejado:
        d["tracejado"] = True
    return d


fig = {}

# p01: parabola y^2 = 12x
par = [pt(y * y / 12, y) for y in lin(-7.2, 7.2, 21)]
fig["ga-s6-p01"] = [
    poli(ida_volta(par), 1),
    seg((-3, -7.5), (-3, 7.5), 3, True),
    ponto((0, 0), "V"),
    ponto((3, 0), "F"),
    ponto((3, 6), "P"),
    seg((3, 6), (3, 0), 2),
    seg((3, 6), (-3, 6), 2),
]

# p02: elipse x^2/169 + y^2/144 = 1
fig["ga-s6-p02"] = [
    poli(elipse2d(0, 0, 13, 12), 1),
    ponto((-5, 0), "F₁"),
    ponto((5, 0), "F₂"),
    ponto((0, 12), "B"),
    seg((0, 0), (0, 12), 3, True),
    seg((0, 0), (5, 0), 3, True),
    seg((0, 12), (5, 0), 3, True),
]

# p03: hiperbole x^2/64 - y^2/36 = 1
ts = lin(-1.3, 1.3, 21)
dir3 = [pt(8 * math.cosh(t), 6 * math.sinh(t)) for t in ts]
esq3 = [pt(-8 * math.cosh(t), 6 * math.sinh(t)) for t in ts]
fig["ga-s6-p03"] = [
    poli(ida_volta(dir3), 1),
    poli(ida_volta(esq3), 1),
    poli([pt(8, 6), pt(-8, 6), pt(-8, -6), pt(8, -6)], 3),
    seg((-16, -12), (16, 12), 3, True),
    seg((-16, 12), (16, -12), 3, True),
    ponto((-10, 0), "F₁"),
    ponto((10, 0), "F₂"),
]

# p04: elipse (x+2)^2/4 + (y-1)^2/9 = 1
s5 = math.sqrt(5)
fig["ga-s6-p04"] = [
    poli(elipse2d(-2, 1, 2, 3), 1),
    ponto((-2, 1), "C"),
    ponto((-2, 1 - s5), "F₁"),
    ponto((-2, 1 + s5), "F₂"),
]

# p05: elipse x^2/100 + y^2/64 = 1
fig["ga-s6-p05"] = [
    poli(elipse2d(0, 0, 10, 8), 1),
    seg((-10, 0), (10, 0), 3, True),
    ponto((-10, 0), "A₁"),
    ponto((10, 0), "A₂"),
    ponto((-6, 0), "F₁"),
    ponto((6, 0), "F₂"),
]

# p06: parabola (y-2)^2 = 8(x+1)
par6 = [pt(-1 + (y - 2) ** 2 / 8, y) for y in lin(-5, 9, 21)]
fig["ga-s6-p06"] = [
    poli(ida_volta(par6), 1),
    seg((-3, -5.5), (-3, 9.5), 3, True),
    ponto((-1, 2), "V"),
    ponto((1, 2), "F"),
    ponto((1, 6), "P"),
    seg((1, 6), (1, 2), 2),
    seg((1, 6), (-3, 6), 2),
]

# p07: hiperbole (x-1)^2/4 - (y+2)^2/5 = 1
ts7 = lin(-1.5, 1.5, 21)
dir7 = [pt(1 + 2 * math.cosh(t), -2 + s5 * math.sinh(t)) for t in ts7]
esq7 = [pt(1 - 2 * math.cosh(t), -2 + s5 * math.sinh(t)) for t in ts7]
m = s5 / 2 * 5
fig["ga-s6-p07"] = [
    poli(ida_volta(dir7), 1),
    poli(ida_volta(esq7), 1),
    seg((-4, -2 - m), (6, -2 + m), 3, True),
    seg((-4, -2 + m), (6, -2 - m), 3, True),
    ponto((1, -2), "C"),
    ponto((-2, -2), "F₁"),
    ponto((4, -2), "F₂"),
]

# p08: circunferencia (x-3)^2 + (y+4)^2 = 4
fig["ga-s6-p08"] = [
    poli(elipse2d(3, -4, 2, 2), 1),
    ponto((3, -4), "C"),
    ponto((5, -4), ""),
    seg((3, -4), (5, -4), 3),
]


def elipse3d_z(a, b, z0, n=32):
    return [pt(a * math.cos(2 * math.pi * i / n), b * math.sin(2 * math.pi * i / n), z0) for i in range(n)]


# p09: hiperboloide de uma folha x^2/4 + y^2/9 - z^2/16 = 1
s2 = math.sqrt(2)
T9 = math.asinh(1)
t9 = lin(-T9, T9, 11)
fig["ga-s6-p09"] = [
    poli(elipse3d_z(2, 3, 0), 1),
    poli(elipse3d_z(2 * s2, 3 * s2, 4), 1),
    poli(elipse3d_z(2 * s2, 3 * s2, -4), 1),
    poli(ida_volta([pt(2 * math.cosh(t), 0, 4 * math.sinh(t)) for t in t9]), 2),
    poli(ida_volta([pt(-2 * math.cosh(t), 0, 4 * math.sinh(t)) for t in t9]), 2),
    poli(ida_volta([pt(0, 3 * math.cosh(t), 4 * math.sinh(t)) for t in t9]), 2),
    poli(ida_volta([pt(0, -3 * math.cosh(t), 4 * math.sinh(t)) for t in t9]), 2),
]

# p10: cone x^2/4 + y^2/9 = z^2
fig["ga-s6-p10"] = [
    poli(elipse3d_z(4, 6, 2), 1),
    poli(elipse3d_z(2, 3, 1), 1),
    poli(elipse3d_z(2, 3, -1), 1),
    poli(elipse3d_z(4, 6, -2), 1),
    seg((0, -6, -2), (0, 6, 2), 2),
    seg((0, 6, -2), (0, -6, 2), 2),
    seg((-4, 0, -2), (4, 0, 2), 2),
    seg((4, 0, -2), (-4, 0, 2), 2),
    ponto((0, 0, 0), "V"),
]


# p11: cilindro x^2/9 + z^2/4 = 1, ao longo de y
def elipse3d_y(a, c, y0, n=32):
    return [pt(a * math.cos(2 * math.pi * i / n), y0, c * math.sin(2 * math.pi * i / n)) for i in range(n)]


fig["ga-s6-p11"] = [
    poli(elipse3d_y(3, 2, -4), 1),
    poli(elipse3d_y(3, 2, 0), 1),
    poli(elipse3d_y(3, 2, 4), 1),
    seg((3, -4, 0), (3, 4, 0), 3),
    seg((-3, -4, 0), (-3, 4, 0), 3),
    seg((0, -4, 2), (0, 4, 2), 3),
    seg((0, -4, -2), (0, 4, -2), 3),
]

# p12: sela z - 3 = (x-1)^2 - (y-2)^2
fig["ga-s6-p12"] = [
    poli(ida_volta([pt(x, 2, 3 + (x - 1) ** 2) for x in lin(-1, 3, 21)]), 1),
    poli(ida_volta([pt(1, y, 3 - (y - 2) ** 2) for y in lin(0, 4, 21)]), 2),
    seg((-1, 0, 3), (3, 4, 3), 3),
    seg((-1, 4, 3), (3, 0, 3), 3),
    ponto((1, 2, 3), "S"),
]

saida = []
for qid, itens in fig.items():
    saida.append("### " + qid)
    linhas = [json.dumps(it, ensure_ascii=False, separators=(", ", ": ")) for it in itens]
    saida.append("[\n  " + ",\n  ".join(linhas) + "\n]")
    npts = sum(len(it["pts"]) for it in itens if it["tipo"] == "poligono")
    saida.append("# pontos em poligonos: " + str(npts))

with open(os.path.join(AQUI, "ga_s6_figuras_saida.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(saida) + "\n")
print("ok", len(fig))
