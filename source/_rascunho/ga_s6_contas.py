# Confere as contas do lote ga_s6 (Geometria Analitica, semana 6, previa).
# Refaz cada resposta, cada valor de alternativa errada citado no "erro",
# cada numero usado nos jeitos e cada ponto das figuras.
# Uso: python -I ga_s6_contas.py
import json
import math
import os
import re
from fractions import Fraction as F

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
falhas = []
n_ok = 0


def ok(cond, msg):
    global n_ok
    if cond:
        n_ok += 1
    else:
        falhas.append(msg)


def perto(a, b, tol=1e-9):
    return abs(a - b) <= tol


def dist(p, q):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))


# polinomio em x, y como dict {(i, j): coef}
def pmul(p, q):
    r = {}
    for (a, b), c in p.items():
        for (d, e), g in q.items():
            r[(a + d, b + e)] = r.get((a + d, b + e), 0) + c * g
    return {k: v for k, v in r.items() if v != 0}


def padd(*ps):
    r = {}
    for p in ps:
        for k, v in p.items():
            r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def pesc(p, s):
    return {k: v * s for k, v in p.items()}


def lin_x(h):  # (x - h)
    return {(1, 0): 1, (0, 0): -h}


def lin_y(k):  # (y - k)
    return {(0, 1): 1, (0, 0): -k}


def quad(p):
    return pmul(p, p)


def const(c):
    return {(0, 0): c}


def geral(**kw):
    # A x2 + B y2 + D x + E y + G
    m = {"A": (2, 0), "B": (0, 2), "D": (1, 0), "E": (0, 1), "G": (0, 0), "XY": (1, 1)}
    return {m[k]: v for k, v in kw.items() if v != 0}


def centro_geral(A, B, D, E):
    return (F(-D, 2 * A), F(-E, 2 * B))


# ---------------- p01: y^2 = 12x ----------------
p = F(12, 4)
ok(p == 3, "p01 p")
foco, diretriz = (3, 0), -3
ok(F(12, 1) != p, "p01 alt A usa 12 como p")
# alt D: forma y^2 = 2px -> p = 6; foco correto nessa forma = (p/2, 0) = (3, 0)
p2 = F(12, 2)
ok(p2 == 6 and p2 / 2 == 3, "p01 alt D")
P = (3, 6)
ok(P[1] ** 2 == 12 * P[0], "p01 P na curva")
ok(dist(P, foco) == 6 and P[0] - diretriz == 6, "p01 distancias de P")
ok(perto(dist(P, (12, 0)), math.sqrt(117)) and P[0] + 12 == 15, "p01 foco errado 12")
for y in range(-6, 7):  # colunas do Excel
    x = y * y / 12
    ok(perto(dist((x, y), foco), x + 3), "p01 Excel C=D em y=%d" % y)

# ---------------- p02: x^2/169 + y^2/144 = 1 ----------------
a2, b2 = 169, 144
c2 = a2 - b2
ok(c2 == 25, "p02 c2")
a, b, c = 13, 12, 5
ok(a * a == a2 and b * b == b2 and c * c == c2, "p02 raizes")
ok(F(c, a) == F(5, 13), "p02 e")
ok(perto(5 / 13, 0.3846, 1e-4), "p02 e decimal 0,385")
ok(a2 + b2 == 313 and perto(math.sqrt(313), 17.69, 0.01), "p02 alt B 313")
ok(F(5, 12) != F(5, 13), "p02 alt D")
ok(F(25, 13) > 1, "p02 alt E e>1")
ok(dist((0, 12), (5, 0)) == 13 and dist((0, 12), (-5, 0)) == 13, "p02 confira 13+13")

# ---------------- p03: x^2/64 - y^2/36 = 1 ----------------
a, b = 8, 6
c = math.sqrt(64 + 36)
ok(c == 10, "p03 c")
ok(F(b, a) == F(3, 4), "p03 inclinacao")
ok(64 - 36 == 28 and perto(math.sqrt(28), 2 * math.sqrt(7)) and perto(2 * math.sqrt(7), 5.29, 0.01), "p03 alt A")
ok(F(a, b) == F(4, 3), "p03 alt B")
ok(F(36, 64) == F(9, 16), "p03 alt D")
y16 = math.sqrt(36 * (256 / 64 - 1))
ok(perto(y16, 6 * math.sqrt(3)) and perto(y16, 10.39, 0.005), "p03 ponto x=16")
d1, d2 = dist((16, y16), (10, 0)), dist((16, y16), (-10, 0))
ok(perto(d1, 12) and perto(d2, 28) and perto(d2 - d1, 16), "p03 distancias 12 e 28")
ok(perto(math.sqrt(36 + 108), 12) and perto(math.sqrt(676 + 108), 28), "p03 contas do confira")
ok(perto(math.hypot(8, 6), 10), "p03 meia diagonal")

# ---------------- p04: 9x2 + 4y2 + 36x - 8y + 4 = 0 ----------------
eq4 = geral(A=9, B=4, D=36, E=-8, G=4)
red4 = padd(pesc(quad(lin_x(-2)), 9), pesc(quad(lin_y(1)), 4), const(-36))
ok(eq4 == red4, "p04 forma reduzida 9(x+2)2 + 4(y-1)2 = 36")
ok(centro_geral(9, 4, 36, -8) == (-2, 1), "p04 centro por -D/2A")
ok((F(-36, 2), F(8, 2)) == (-18, 4), "p04 alt C centro (-18, 4)")
c2 = 9 - 4
ok(c2 == 5 and perto(math.sqrt(5), 2.236, 0.001), "p04 c = raiz 5")


def val4(x, y):
    return 9 * x * x + 4 * y * y + 36 * x - 8 * y + 4


ok(val4(0, 1) == 0 and val4(-2, 4) == 0, "p04 pontos (0,1) e (-2,4)")
ok(9 * 4 + 4 * 16 - 72 - 32 + 4 == 0, "p04 conta escrita (-2,4)")
ok(val4(4, -1) == 304 and 144 + 4 + 144 + 8 + 4 == 304, "p04 ponto (4,-1) = 304")

# ---------------- p05: eixo maior 20, e = 3/5 ----------------
a = 10
c = F(3, 5) * a
b2 = a * a - c * c
ok(c == 6 and b2 == 64, "p05 c e b2")
ok(F(3, 5) * 20 == 12 and 400 - 144 == 256, "p05 alt C (a=20)")
ok(100 + 36 == 136, "p05 alt D")
ok(F(3, 5) * 5 == 3, "p05 cotidiano eixo 10 -> foco a 3")
ok(dist((0, 8), (6, 0)) == 10 and dist((0, 8), (-6, 0)) == 10, "p05 confira (0,8)")

# ---------------- p06: y2 - 4y - 8x - 4 = 0 ----------------
eq6 = geral(B=1, E=-4, D=-8, G=-4)
red6 = padd(quad(lin_y(2)), pesc(lin_x(-1), -8))
ok(eq6 == red6, "p06 (y-2)2 = 8(x+1)")
p = F(8, 4)
V = (-1, 2)
Fo = (V[0] + p, V[1])
ok(Fo == (1, 2) and V[0] - p == -3, "p06 foco e diretriz")
ok((V[0] + 4, V[0] - 4) == (3, -5), "p06 alt C (p=4)")
ok((1 + 2, 1 - 2) == (3, -1), "p06 alt D")
ok((V[0], V[1] + p, V[1] - p) == (-1, 4, 0), "p06 alt E")
ok((2, 0) == (p, 0), "p06 alt B foco de y2=8x")
P = (1, 6)
ok((P[1] - 2) ** 2 == 8 * (P[0] + 1), "p06 P na curva")
ok(dist(P, Fo) == 4 and P[0] - (-3) == 4, "p06 distancias de P")
ok(36 - 24 - 8 - 4 == 0, "p06 conta escrita")

# ---------------- p07: 5x2 - 4y2 - 10x - 16y - 31 = 0 ----------------
eq7 = geral(A=5, B=-4, D=-10, E=-16, G=-31)
red7 = padd(pesc(quad(lin_x(1)), 5), pesc(quad(lin_y(-2)), -4), const(-20))
ok(eq7 == red7, "p07 5(x-1)2 - 4(y+2)2 = 20")
ok(centro_geral(5, -4, -10, -16) == (1, -2), "p07 centro")
a2, b2 = 4, 5
c = math.sqrt(a2 + b2)
ok(c == 3, "p07 c")
focos = {(1 + 3, -2), (1 - 3, -2)}
ok(focos == {(4, -2), (-2, -2)}, "p07 focos")
ok({(1 + 1, -2), (1 - 1, -2)} == {(2, -2), (0, -2)}, "p07 alt A")
ok({(1 + 2, -2), (1 - 2, -2)} == {(3, -2), (-1, -2)}, "p07 alt B")
ok({(1, -2 + 3), (1, -2 - 3)} == {(1, 1), (1, -5)}, "p07 alt C")
ok({(-1 + 3, 2), (-1 - 3, 2)} == {(2, 2), (-4, 2)}, "p07 alt E")
ok(31 + 5 - 16 == 20 and 31 + 5 + 16 == 52, "p07 caminho com -16 da 52")
# -4(y2 - 4y) erraria o centro para y = 2
ok(F(4, 2) == 2, "p07 centro errado y=2")


def val7(x, y):
    return 5 * x * x - 4 * y * y - 10 * x - 16 * y - 31


ok(val7(3, -2) == 0 and 45 - 16 - 30 + 32 - 31 == 0, "p07 vertice (3,-2)")
Q = (4, F(1, 2))
ok(F((Q[0] - 1) ** 2, 4) - F((Q[1] + 2) ** 2, 5) == 1, "p07 (4, 1/2) na curva")
ok(perto(dist((4, 0.5), (4, -2)), 2.5) and perto(dist((4, 0.5), (-2, -2)), 6.5), "p07 distancias 5/2 e 13/2")
ok(F(13, 2) - F(5, 2) == 4, "p07 diferenca 2a")
ok(F(10, 2 * 5) == 1 and F(16, 2 * -4) == -2, "p07 atalho h,k")
ok(perto(5 * math.sqrt(5) / 2, 5.590, 0.001), "p07 extremos das assintotas")

# ---------------- p08: x2 + y2 - 6x + 8y + k = 0, r = 2 ----------------
k = 25 - 4
ok(k == 21, "p08 k")
ok(25 - 2 == 23 and 25 + 4 == 29 and 25 - (-21) == 46, "p08 alts A, C, D")
ok(25 - (-4) == 29, "p08 alt E daria r2 = 29")


def val8(x, y, kk):
    return x * x + y * y - 6 * x + 8 * y + kk


ok(val8(5, -4, 21) == 0 and val8(3, -2, 21) == 0, "p08 pontos (5,-4) e (3,-2)")
ok(25 + 16 - 30 - 32 + 21 == 0 and 9 + 4 - 18 - 16 + 21 == 0, "p08 contas escritas")
ok(25 - 23 == 2, "p08 k=23 da r2=2")
eq8 = geral(A=1, B=1, D=-6, E=8, G=21)
red8 = padd(quad(lin_x(3)), quad(lin_y(-4)), const(-4))
ok(eq8 == red8, "p08 forma reduzida")


# ---------------- quadricas: classificacao por sinais ----------------
def classe(neg, lado):
    if lado == 0:
        return "cone"
    return {0: "elipsoide", 1: "uma folha", 2: "duas folhas"}[neg]


ok(classe(1, 1) == "uma folha", "p09 classe")
ok(classe(0, 1) == "elipsoide" and classe(2, 1) == "duas folhas", "p09 alts")
# p09: traco z=4
ok(1 + 16 / 16 == 2, "p09 traco z=4")
ok(perto(2 * math.sqrt(2), 2.828, 0.001) and perto(3 * math.sqrt(2), 4.243, 0.001), "p09 semieixos em z=4")

# ---------------- p10: cone x2/4 + y2/9 = z2 ----------------
# z=2: x2/4 + y2/9 = 4 -> x2/16 + y2/36 = 1
ok(4 * 4 == 16 and 9 * 4 == 36, "p10 traco z=2")
ok(math.sqrt(9) == 3, "p10 x=0 -> y = 3z")
ok(4 * 2 == 8 and 9 * 2 == 18, "p10 alt A paraboloide em z=2")
ok(math.sqrt(36) == 6, "p10 alt E cilindro x=0 -> y=6")

# ---------------- p11: cilindro 4x2 + 9z2 = 36 ----------------
for (x, y, z) in [(3, 0, 0), (3, 5, 0), (3, -8, 0), (0, 2, 2), (3, 7, 0), (3, -100, 0)]:
    ok(4 * x * x + 9 * z * z == 36, "p11 ponto %s" % str((x, y, z)))
ok(4 * 0 + 9 * 9 == 81, "p11 (0,0,3) da 81")
ok(F(36, 4) == 9 and F(36, 9) == 4, "p11 semieixos 3 e 2")

# ---------------- p12: z = x2 - y2 - 2x + 4y ----------------
eq12 = geral(A=1, B=-1, D=-2, E=4)
red12 = padd(quad(lin_x(1)), pesc(quad(lin_y(2)), -1), const(3))
ok(eq12 == red12, "p12 forma reduzida")


def z12(x, y):
    return x * x - y * y - 2 * x + 4 * y


ok(z12(1, 2) == 3 and 1 - 4 - 2 + 8 == 3, "p12 ponto de sela")
ok(-1 - 4 == -5, "p12 constante errada -5")
linha = {x: z12(x, 2) for x in range(-1, 4)}
coluna = {y: z12(1, y) for y in range(0, 5)}
ok(min(linha, key=linha.get) == 1 and linha[1] == 3, "p12 Excel linha y=2")
ok(max(coluna, key=coluna.get) == 2 and coluna[2] == 3, "p12 Excel coluna x=1")
ok(sorted(linha.values()).count(3) == 1 and sorted(coluna.values()).count(3) == 1, "p12 unico 3")
ok(F(2, 2) == 1 and F(4, 2) == 2, "p12 atalho centro")

# ---------------- figuras ----------------
curvas = {
    "ga-s6-p01": lambda x, y: y * y - 12 * x,
    "ga-s6-p02": lambda x, y: x * x / 169 + y * y / 144 - 1,
    "ga-s6-p03": lambda x, y: x * x / 64 - y * y / 36 - 1,
    "ga-s6-p04": lambda x, y: (x + 2) ** 2 / 4 + (y - 1) ** 2 / 9 - 1,
    "ga-s6-p05": lambda x, y: x * x / 100 + y * y / 64 - 1,
    "ga-s6-p06": lambda x, y: (y - 2) ** 2 - 8 * (x + 1),
    "ga-s6-p07": lambda x, y: (x - 1) ** 2 / 4 - (y + 2) ** 2 / 5 - 1,
    "ga-s6-p08": lambda x, y: (x - 3) ** 2 + (y + 4) ** 2 - 4,
    "ga-s6-p09": lambda x, y, z: x * x / 4 + y * y / 9 - z * z / 16 - 1,
    "ga-s6-p10": lambda x, y, z: x * x / 4 + y * y / 9 - z * z,
    "ga-s6-p11": lambda x, y, z: x * x / 9 + z * z / 4 - 1,
    "ga-s6-p12": lambda x, y, z: x * x - y * y - 2 * x + 4 * y - z,
}
pontos_esperados = {
    "ga-s6-p01": {"V": (0, 0), "F": (3, 0), "P": (3, 6)},
    "ga-s6-p02": {"F₁": (-5, 0), "F₂": (5, 0), "B": (0, 12)},
    "ga-s6-p03": {"F₁": (-10, 0), "F₂": (10, 0)},
    "ga-s6-p04": {"C": (-2, 1), "F₁": (-2, 1 - math.sqrt(5)), "F₂": (-2, 1 + math.sqrt(5))},
    "ga-s6-p05": {"A₁": (-10, 0), "A₂": (10, 0), "F₁": (-6, 0), "F₂": (6, 0)},
    "ga-s6-p06": {"V": (-1, 2), "F": (1, 2), "P": (1, 6)},
    "ga-s6-p07": {"C": (1, -2), "F₁": (-2, -2), "F₂": (4, -2)},
    "ga-s6-p08": {"C": (3, -4), "": (5, -4)},
    "ga-s6-p10": {"V": (0, 0, 0)},
    "ga-s6-p12": {"S": (1, 2, 3)},
}
maior_res = {}
qs = {}
semanas = []
for nome in ("ga_s6_p1.json", "ga_s6_p2.json"):
    with open(os.path.join(DADOS, nome), "rb") as fb:
        bruto = fb.read()
    ctrl = [bt for bt in bruto if bt < 0x20 and bt not in (0x0A, 0x0D, 0x09)]
    ok(not ctrl, "%s tem bytes de controle: %s" % (nome, ctrl[:5]))
    d = json.loads(bruto.decode("utf-8"))
    semanas += d["semanas"]
    for q in d["questoes"]:
        qs[q["id"]] = q

ok(len(qs) == 12 and sorted(qs) == ["ga-s6-p%02d" % i for i in range(1, 13)], "ids p01..p12")
for qid, q in qs.items():
    f = q.get("figura")
    ok(f is not None, qid + " sem figura")
    if not f:
        continue
    fn = curvas[qid]
    res = 0.0
    for it in f["itens"]:
        if it["tipo"] == "poligono" and it.get("cor") in (1, 2):
            for pt in it["pts"]:
                res = max(res, abs(fn(*pt)))
        if it["tipo"] == "ponto" and qid in pontos_esperados:
            esp = pontos_esperados[qid].get(it["rot"])
            ok(esp is not None and all(perto(u, v, 0.001) for u, v in zip(it["em"], esp)),
               "%s ponto %s em %s" % (qid, it["rot"], it["em"]))
    maior_res[qid] = res
    ok(res < 0.01, "%s: ponto de curva fora da equacao (residuo %.4f)" % (qid, res))

# segmentos que devem estar sobre a superficie (retas do cone, geratrizes, X da sela)
for qid in ("ga-s6-p10", "ga-s6-p11", "ga-s6-p12"):
    for it in qs[qid]["figura"]["itens"]:
        if it["tipo"] == "segmento":
            for s in [i / 10 for i in range(11)]:
                ptm = [a + (b - a) * s for a, b in zip(it["de"], it["ate"])]
                ok(abs(curvas[qid](*ptm)) < 1e-9, "%s segmento fora da superficie em %s" % (qid, ptm))
# assintotas da p03 e p07: inclinacao certa e passam pelo centro
for it in qs["ga-s6-p03"]["figura"]["itens"]:
    if it["tipo"] == "segmento":
        (x1, y1), (x2, y2) = it["de"], it["ate"]
        ok(perto(abs((y2 - y1) / (x2 - x1)), 0.75) and perto((y1 + y2) / 2, 0) and perto((x1 + x2) / 2, 0), "p03 assintota")
for it in qs["ga-s6-p07"]["figura"]["itens"]:
    if it["tipo"] == "segmento":
        (x1, y1), (x2, y2) = it["de"], it["ate"]
        ok(perto(abs((y2 - y1) / (x2 - x1)), math.sqrt(5) / 2, 0.001) and perto((x1 + x2) / 2, 1) and perto((y1 + y2) / 2, -2), "p07 assintota")

# ---------------- respostas e posicoes ----------------
esperado = {
    "ga-s6-p01": "Foco (3, 0) e diretriz x = −3",
    "ga-s6-p02": "Focos (±5, 0) e e = 5/13",
    "ga-s6-p03": "Focos (±10, 0); assíntotas y = ±(3/4)x",
    "ga-s6-p04": "Elipse de centro (−2, 1)",
    "ga-s6-p05": "x²/100 + y²/64 = 1",
    "ga-s6-p06": "V = (−1, 2), F = (1, 2), diretriz x = −3",
    "ga-s6-p07": "(4, −2) e (−2, −2)",
    "ga-s6-p08": "k = 21",
    "ga-s6-p09": "Hiperboloide de uma folha",
    "ga-s6-p10": "Cone elíptico x²/4 + y²/9 = z²",
    "ga-s6-p11": "Cilindro elíptico com geratrizes paralelas ao eixo y",
    "ga-s6-p12": "Paraboloide hiperbólico com ponto de sela (1, 2, 3)",
}
pos = {}
niveis = {}
for qid, q in qs.items():
    certas = [i for i, a in enumerate(q["alternativas"]) if a.get("certa")]
    ok(len(certas) == 1, qid + " certas")
    ok(q["alternativas"][certas[0]]["t"] == esperado[qid], qid + " alternativa certa diferente do conferido")
    pos[qid] = "ABCDE"[certas[0]]
    niveis.setdefault(q["nivel"], []).append(qid)

# ---------------- tamanhos ----------------
def npal(s):
    return len(re.findall(r"\S+", s))


tam = []
for s in semanas:
    for bl in s["blocos"]:
        n = npal(bl["texto"])
        tam.append(("bloco " + bl["titulo"], n))
        ok(40 <= n <= 120, "bloco '%s' com %d palavras" % (bl["titulo"], n))
    for k, v in s["jeitos"].items():
        n = npal(v)
        tam.append(("semana." + k, n))
        ok(50 <= n <= 120, "jeito da semana %s com %d palavras" % (k, n))
for qid, q in qs.items():
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = npal(q["jeitos"][k])
        ok(35 <= n <= 110, "%s.%s com %d palavras" % (qid, k, n))
        tam.append((qid + "." + k, n))

print("conferencias OK:", n_ok)
print("falhas:", len(falhas))
for fm in falhas:
    print("  FALHA", fm)
print("maior residuo das curvas por questao:")
for qid in sorted(maior_res):
    print("  ", qid, round(maior_res[qid], 5))
print("posicoes das certas:", pos)
print("niveis:", {k: len(v) for k, v in sorted(niveis.items())})
print("menor e maior tamanho de jeito (palavras):", min(t[1] for t in tam), max(t[1] for t in tam))
