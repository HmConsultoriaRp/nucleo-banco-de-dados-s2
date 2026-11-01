# Revisor adversarial do lote ga_s6 (rodada 2).
# Refaz do zero, com Fraction, cada questao (p01 a p12): resposta certa, a conta de cada
# alternativa errada (o valor que o "erro" promete), os numeros citados nos jeitos,
# as figuras (pontos contra a equacao da curva/superficie), a teoria da semana,
# tamanhos, bytes de controle e distribuicao.
# Uso: python -I rev_ga_s6_r2_contas.py
import json, os, re, sys, math
from fractions import Fraction as F
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
M = "−"  # sinal de menos tipografico

falhas = []
n_ok = 0


def ok(cond, msg):
    global n_ok
    if cond:
        n_ok += 1
    else:
        falhas.append(msg)
        print("FALHA", msg)


docs = {}
for nome in ("ga_s6_p1.json", "ga_s6_p2.json"):
    with open(os.path.join(DADOS, nome), "rb") as f:
        bruto = f.read()
    ctrl = [b for b in bruto if b < 32 and b not in (10, 13)]
    ok(not ctrl, nome + ": bytes de controle " + str(ctrl[:5]))
    ok(b"\\" not in bruto, nome + ": tem barra invertida (conferir escapes)")
    docs[nome] = json.loads(bruto.decode("utf-8"))

Q = {}
for nome, d in docs.items():
    for q in d["questoes"]:
        ok(q["id"] not in Q, "id repetido " + q["id"])
        Q[q["id"]] = q


# ---------------- utilitarios ----------------
def fmt(x):
    x = F(x)
    s = M if x < 0 else ""
    x = abs(x)
    if x.denominator == 1:
        return s + str(x.numerator)
    return s + str(x.numerator) + "/" + str(x.denominator)


def pt(*c):
    return "(" + ", ".join(fmt(v) for v in c) + ")"


def raiz_exata(x):
    x = F(x)
    if x < 0:
        return None
    n, d = x.numerator, x.denominator
    rn, rd = math.isqrt(n), math.isqrt(d)
    if rn * rn == n and rd * rd == d:
        return F(rn, rd)
    return None


def raiz_txt(n):
    """inteiro n -> texto simplificado da raiz: 28 -> 2√7, 313 -> √313, 25 -> 5"""
    k = 1
    m = n
    for f in range(2, int(math.isqrt(n)) + 1):
        while m % (f * f) == 0:
            m //= f * f
            k *= f
    if m == 1:
        return str(k)
    return ("" if k == 1 else str(k)) + "√" + str(m)


def textos(qid):
    return [a["t"] for a in Q[qid]["alternativas"]]


def idx_certa(qid):
    c = [i for i, a in enumerate(Q[qid]["alternativas"]) if a.get("certa") is True]
    ok(len(c) == 1, qid + ": numero de certas " + str(len(c)))
    return c[0]


def confere_alts(qid, esperado, certa):
    """esperado: lista de 5 textos (A..E) recalculados aqui; certa: indice da certa recalculada."""
    t = textos(qid)
    for i in range(5):
        ok(t[i] == esperado[i], qid + " alt " + "ABCDE"[i] + ": arquivo '" + t[i] + "' x conta '" + esperado[i] + "'")
    ok(idx_certa(qid) == certa, qid + ": certa no arquivo e " + "ABCDE"[idx_certa(qid)] + ", conta da " + "ABCDE"[certa])
    ok(len(set(esperado)) == 5, qid + ": valores das alternativas nao sao todos diferentes")


def texto_q(qid):
    """todo o texto da questao, para procurar numeros citados."""
    q = Q[qid]
    partes = [q["enunciado"], q["dica"], q["resposta"]]
    partes += [a.get("erro", "") for a in q["alternativas"]]
    j = q["jeitos"]
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        partes.append(j[k])
    partes += j["receita"]
    partes += [c["fala"] for c in j["conversa"]]
    if "figura" in q:
        partes.append(q["figura"].get("legenda", ""))
    return "\n".join(partes)


def cita(qid, trecho):
    ok(trecho in texto_q(qid), qid + ": trecho esperado nao encontrado: '" + trecho + "'")


def itens(qid, tipo=None):
    return [it for it in Q[qid]["figura"]["itens"] if tipo is None or it["tipo"] == tipo]


def resid_max(pts, g):
    return max(abs(g(*[float(v) for v in p])) for p in pts)


def dist(a, b):
    return math.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b)))


# polinomio em x, y, z: dict {(i,j,k): Fraction}
def P(d):
    return {k: F(v) for k, v in d.items() if v != 0}


def padd(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) + v
    return {k: v for k, v in r.items() if v != 0}


def pmul(a, b):
    r = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(x + y for x, y in zip(k1, k2))
            r[k] = r.get(k, 0) + v1 * v2
    return {k: v for k, v in r.items() if v != 0}


def pesc(c, a):
    return {k: F(c) * v for k, v in a.items() if c != 0}


def lin(cx=0, cy=0, cz=0, c0=0):
    return P({(1, 0, 0): cx, (0, 1, 0): cy, (0, 0, 1): cz, (0, 0, 0): c0})


def sq(p):
    return pmul(p, p)


def pval(p, x=0, y=0, z=0):
    return sum(v * F(x) ** i * F(y) ** j * F(z) ** k for (i, j, k), v in p.items())


X, Y, Z = lin(cx=1), lin(cy=1), lin(cz=1)

# ================= p01: x² = 12y =================
qid = "ga-s6-p01"
ok("x² = 12y" in Q[qid]["enunciado"], qid + ": enunciado nao e x² = 12y")
K = F(12)
p = K / 4
esp = [
    "Foco " + pt(0, K) + " e diretriz y = " + fmt(-K),            # A: p = 12
    "Foco " + pt(p, 0) + " e diretriz x = " + fmt(-p),            # B: par de y² = 12x
    "Foco " + pt(0, p) + " e diretriz y = " + fmt(-p),            # C: certa
    "Foco " + pt(0, K / 2) + " e diretriz y = " + fmt(-K / 2),    # D: 2p = 12 e foco (0, p)
    "Foco " + pt(0, -p) + " e diretriz y = " + fmt(p),            # E: sinais trocados
]
confere_alts(qid, esp, 2)
ok((K / 2) / 2 == p, qid + ": na forma x² = 2py o foco (0, p/2) nao coincide")
P1 = (6, 3)
ok(F(P1[0]) ** 2 == K * P1[1], qid + ": P fora da curva")
ok(dist(P1, (0, p)) == 6 and P1[1] - (-p) == 6, qid + ": distancias de P")
ok((6 - 0) ** 2 + (3 - 12) ** 2 == 117 and 3 - (-12) == 15, qid + ": √117 e 15")
for xx in range(-6, 7):
    yy = F(xx * xx, 12)
    ok(F(xx) ** 2 + (yy - 3) ** 2 == (yy + 3) ** 2, qid + ": colunas C e D do Excel nao batem em x=" + str(xx))
for t in ("p = 12/4 = 3", "4p = 12, então p = 3", "(0, p) = (0, 3)", "y = −p = −3", "√117", "daria 15", "y = 36/12 = 3", "3 − (−3) = 6"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 41 and pol.get("aberto") is True, qid + ": parabola com 41 pontos e aberta")
ok(resid_max(pol["pts"], lambda x, y: y - x * x / 12) <= 0.0006, qid + ": pontos fora de y = x²/12")
seg = itens(qid, "segmento")
ok(seg[0]["de"][1] == -3 and seg[0]["ate"][1] == -3, qid + ": diretriz da figura")
pts_fig = {it["rot"]: tuple(it["em"]) for it in itens(qid, "ponto")}
ok(pts_fig == {"V": (0, 0), "F": (0, 3), "P": (6, 3)}, qid + ": pontos da figura " + str(pts_fig))
ok(dist(seg[1]["de"], seg[1]["ate"]) == 6 and dist(seg[2]["de"], seg[2]["ate"]) == 6, qid + ": segmentos coral de 6")

# ================= p02: x²/169 + y²/144 = 1 =================
qid = "ga-s6-p02"
a2, b2 = F(169), F(144)
c2 = a2 - b2
a, b, c = raiz_exata(a2), raiz_exata(b2), raiz_exata(c2)
ok((a, b, c) == (13, 12, 5), qid + ": a, b, c")
e = c / a
esp = [
    "Focos (±" + fmt(c) + ", 0) e e = " + fmt(e),                                        # certa
    "Focos (±" + raiz_txt(int(a2 + b2)) + ", 0) e e = " + raiz_txt(int(a2 + b2)) + "/" + fmt(a),  # soma
    "Focos (0, ±" + fmt(c) + ") e e = " + fmt(e),                                       # eixo trocado
    "Focos (±" + fmt(c) + ", 0) e e = " + fmt(c / b),                                   # c/b
    "Focos (±" + fmt(c2) + ", 0) e e = " + fmt(c2 / a),                                 # sem raiz
]
confere_alts(qid, esp, 0)
ok(c2 / a > 1 and 0 < e < 1, qid + ": 25/13 > 1 e 5/13 em (0,1)")
ok(f"{float(e):.3f}" == "0.385", qid + ": 5/13 ≈ 0,385")
ok(f"{math.sqrt(313):.1f}" == "17.7" and math.sqrt(313) > 17, qid + ": √313 ≈ 17,7")
ok(dist((0, 12), (5, 0)) == 13 and dist((0, 12), (-5, 0)) == 13, qid + ": topo a 13 dos focos")
for t in ("169 − 144 = 25", "e = c/a = 5/13", "≈ 0,385", "√(25 + 144) = √169 = 13", "Soma 26 = 2a", "≈ ±17,7"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 40, qid + ": 40 pontos")
ok(resid_max(pol["pts"], lambda x, y: x * x / 169 + y * y / 144 - 1) < 0.0005, qid + ": pontos fora da elipse")
ok({tuple(it["em"]) for it in itens(qid, "ponto")} == {(-5, 0), (5, 0), (0, 12)}, qid + ": pontos da figura")

# ================= p03: x²/64 − y²/36 = 1 =================
qid = "ga-s6-p03"
a2, b2 = F(64), F(36)
a, b = raiz_exata(a2), raiz_exata(b2)
c2 = a2 + b2
c = raiz_exata(c2)
ok(c == 10, qid + ": c")
m = b / a
esp = [
    "Focos (±" + raiz_txt(int(a2 - b2)) + ", 0); assíntotas y = ±(" + fmt(m) + ")x",     # relacao da elipse
    "Focos (±" + fmt(c) + ", 0); assíntotas y = ±(" + fmt(a / b) + ")x",                # fracao invertida
    "Focos (±" + fmt(a) + ", 0); assíntotas y = ±(" + fmt(m) + ")x",                     # vertices
    "Focos (±" + fmt(c) + ", 0); assíntotas y = ±(" + fmt(b2 / a2) + ")x",              # quadrados
    "Focos (±" + fmt(c) + ", 0); assíntotas y = ±(" + fmt(m) + ")x",                     # certa
]
confere_alts(qid, esp, 4)
yy2 = b2 * (F(16) ** 2 / a2 - 1)
ok(yy2 == 108 and f"{math.sqrt(108):.2f}" == "10.39", qid + ": y = 6√3 ≈ 10,39 em x = 16")
ok((16 - 10) ** 2 + 108 == 144 and (16 + 10) ** 2 + 108 == 784, qid + ": distancias 12 e 28")
ok(28 - 12 == 2 * a, qid + ": diferenca 2a")
ok(f"{2 * math.sqrt(7):.1f}" == "5.3", qid + ": 2√7 ≈ 5,3")
for t in ("64 + 36 = 100", "√(64 + 36) = 10", "6√3 ≈ 10,39", "√(36 + 108) = 12", "√(676 + 108) = 28", "28 − 12 = 16 = 2a", "2√7 ≈ 5,3", "64 − 36 = 28", "6/8 = 3/4"):
    cita(qid, t)
ramos = itens(qid, "poligono")[:2]
for r in ramos:
    ok(len(r["pts"]) == 41 and r.get("aberto") is True, qid + ": ramo com 41 pontos e aberto")
    ok(resid_max(r["pts"], lambda x, y: x * x / 64 - y * y / 36 - 1) < 0.003, qid + ": ramo fora da hiperbole")
caixa = itens(qid, "poligono")[2]
ok(sorted(map(tuple, caixa["pts"])) == sorted([(8, 6), (-8, 6), (-8, -6), (8, -6)]), qid + ": caixa 16 x 12")
for s in itens(qid, "segmento"):
    (x1, y1), (x2, y2) = s["de"], s["ate"]
    ok(abs(abs(F(y2 - y1) / F(x2 - x1)) - m) == 0 and F(y1) * x2 == F(y2) * x1, qid + ": assintota da figura")
ok({tuple(it["em"]) for it in itens(qid, "ponto")} == {(-10, 0), (10, 0)}, qid + ": focos da figura")

# ================= p04: 9x² + 4y² + 36x − 8y + 4 = 0 =================
qid = "ga-s6-p04"
A_, C_, D_, E_, F0 = F(9), F(4), F(36), F(-8), F(4)
orig = padd(padd(pesc(A_, sq(X)), pesc(C_, sq(Y))), padd(padd(pesc(D_, X), pesc(E_, Y)), P({(0, 0, 0): F0})))
h, k = -D_ / (2 * A_), -E_ / (2 * C_)
dir_ = A_ * h * h + C_ * k * k - F0
ok((h, k, dir_) == (-2, 1, 36), qid + ": centro e lado direito")
red = padd(padd(pesc(A_, sq(lin(cx=1, c0=-h))), pesc(C_, sq(lin(cy=1, c0=-k)))), P({(0, 0, 0): -dir_}))
ok(red == orig, qid + ": forma reduzida 9(x+2)² + 4(y−1)² = 36 nao reproduz a original")
ok(dir_ / A_ == 4 and dir_ / C_ == 9, qid + ": denominadores 4 e 9")
esp = [
    "Circunferência de centro " + pt(h, k),
    "Elipse de centro " + pt(-h, -k),
    "Elipse de centro " + pt(-D_ / 2, -E_ / 2),   # metade de 36 e de −8 sem o coeficiente
    "Elipse de centro " + pt(h, k),
    "Hipérbole de centro " + pt(h, k),
]
confere_alts(qid, esp, 3)
ok(A_ != C_ and A_ * C_ > 0, qid + ": coeficientes distintos e de mesmo sinal")
c = math.sqrt(float(dir_ / C_ - dir_ / A_))
ok(abs(c - math.sqrt(5)) < 1e-12, qid + ": c = √5")
ok(pval(orig, 0, 1) == 0 and pval(orig, -2, 4) == 0 and pval(orig, 4, -1) == 304, qid + ": substituicoes do confira")
ok(9 * 4 == 36 and 4 * 1 == 4, qid + ": ajustes 36 e 4")
for t in ("9(x² + 4x) + 4(y² − 2y) = −4", "9(x + 2)² − 36 + 4(y − 1)² − 4 = −4", "9(x + 2)² + 4(y − 1)² = 36",
          "(x + 2)²/4 + (y − 1)²/9 = 1", "h = −36/18 = −2", "k = 8/8 = 1", "= 304", "9 × 4 = 36"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 40, qid + ": 40 pontos")
ok(resid_max(pol["pts"], lambda x, y: (x + 2) ** 2 / 4 + (y - 1) ** 2 / 9 - 1) < 0.0005, qid + ": pontos fora da elipse")
pf = {it["rot"]: it["em"] for it in itens(qid, "ponto")}
ok(pf["C"] == [-2, 1] and abs(pf["F₂"][1] - (1 + math.sqrt(5))) < 0.0006 and abs(pf["F₁"][1] - (1 - math.sqrt(5))) < 0.0006, qid + ": focos da figura")

# ================= p05: eixo maior 20, e = 3/5 =================
qid = "ga-s6-p05"
a = F(20) / 2
e = F(3, 5)
c = e * a
b2 = a * a - c * c
ok((a, c, b2) == (10, 6, 64), qid + ": a, c, b²")
a_err = F(20)
c_err = e * a_err
esp = [
    "x²/" + fmt(b2) + " + y²/" + fmt(a * a) + " = 1",
    "x²/" + fmt(a * a) + " + y²/" + fmt(b2) + " = 1",
    "x²/" + fmt(a_err ** 2) + " + y²/" + fmt(a_err ** 2 - c_err ** 2) + " = 1",
    "x²/" + fmt(a * a) + " + y²/" + fmt(a * a + c * c) + " = 1",
    "x²/" + fmt(a * a) + " + y²/" + fmt(c * c) + " = 1",
]
confere_alts(qid, esp, 1)
ok(c_err == 12 and a_err ** 2 - c_err ** 2 == 256, qid + ": c = 12 e b² = 256 com a = 20")
ok(e * 5 == 3, qid + ": eixo maior 10 -> foco a 3")
ok(dist((0, 8), (6, 0)) == 10, qid + ": (0, 8) a 10 do foco")
for t in ("(3/5) · 10 = 6", "100 − 36 = 64", "400 − 144 = 256", "100 + 36 = 136", "√(100 − 64) = 6", "6/10 = 3/5", "√(36 + 64) = 10", "a 3 do centro"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 40 and resid_max(pol["pts"], lambda x, y: x * x / 100 + y * y / 64 - 1) < 0.0005, qid + ": elipse da figura")
ok({tuple(it["em"]) for it in itens(qid, "ponto")} == {(-10, 0), (10, 0), (-6, 0), (6, 0)}, qid + ": pontos da figura")

# ================= p06: y² − 4y − 8x − 4 = 0 =================
qid = "ga-s6-p06"
orig = padd(padd(sq(Y), pesc(-4, Y)), padd(pesc(-8, X), P({(0, 0, 0): -4})))
k = F(4) / 2          # metade de 4 (y² − 4y)
h = -1
red = padd(sq(lin(cy=1, c0=-k)), pesc(-8, lin(cx=1, c0=-h)))
ok(red == orig, qid + ": (y − 2)² = 8(x + 1) nao reproduz a original")
p = F(8) / 4
V = (h, k)
Fo = (h + p, k)
dr = h - p
esp = [
    "V = " + pt(*V) + ", F = " + pt(*Fo) + ", diretriz x = " + fmt(dr),
    "V = (0, 0), F = " + pt(p, 0) + ", diretriz x = " + fmt(-p),                       # so y² = 8x
    "V = " + pt(*V) + ", F = " + pt(h + 4, k) + ", diretriz x = " + fmt(h - 4),         # p = 4 somado inteiro
    "V = " + pt(-h, -k) + ", F = " + pt(-h + p, -k) + ", diretriz x = " + fmt(-h - p),  # sinais do vertice
    "V = " + pt(*V) + ", F = " + pt(h, k + p) + ", diretriz y = " + fmt(k - p),         # p na vertical
]
confere_alts(qid, esp, 0)
ok(pval(orig, 1, 6) == 0 and dist((1, 6), Fo) == 4 and 1 - dr == 4, qid + ": ponto P do confira")
ok(36 - 24 - 8 - 4 == 0, qid + ": 36 − 24 − 8 − 4")
for t in ("y² − 4y = 8x + 4", "y² − 4y + 4 = 8x + 4 + 4", "(y − 2)² = 8x + 8", "(y − 2)² = 8(x + 1)", "4p = 8, então p = 2",
          "(−1 + 2, 2) = (1, 2)", "x = −1 − 2 = −3", "36 − 24 − 8 − 4 = 0", "1 − (−3) = 4", "p = 8/4 = 2"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 41 and pol.get("aberto") is True, qid + ": parabola 41 pontos aberta")
ok(resid_max(pol["pts"], lambda x, y: x - ((y - 2) ** 2 / 8 - 1)) <= 0.0006, qid + ": pontos fora da parabola")
ok({it["rot"]: tuple(it["em"]) for it in itens(qid, "ponto")} == {"V": (-1, 2), "F": (1, 2), "P": (1, 6)}, qid + ": pontos da figura")
ok(itens(qid, "segmento")[0]["de"][0] == -3 and itens(qid, "segmento")[0]["ate"][0] == -3, qid + ": diretriz da figura")

# ================= p07: 5x² − 4y² − 10x − 16y − 31 = 0 =================
qid = "ga-s6-p07"
A_, C_, D_, E_, F0 = F(5), F(-4), F(-10), F(-16), F(-31)
orig = padd(padd(pesc(A_, sq(X)), pesc(C_, sq(Y))), padd(padd(pesc(D_, X), pesc(E_, Y)), P({(0, 0, 0): F0})))
h, k = -D_ / (2 * A_), -E_ / (2 * C_)
dir_ = A_ * h * h + C_ * k * k - F0
ok((h, k, dir_) == (1, -2, 20), qid + ": centro e lado direito")
red = padd(padd(pesc(A_, sq(lin(cx=1, c0=-h))), pesc(C_, sq(lin(cy=1, c0=-k)))), P({(0, 0, 0): -dir_}))
ok(red == orig, qid + ": 5(x − 1)² − 4(y + 2)² = 20 nao reproduz a original")
a2, b2 = dir_ / A_, -dir_ / C_
ok((a2, b2) == (4, 5), qid + ": a² = 4 e b² = 5")
c = raiz_exata(a2 + b2)
a = raiz_exata(a2)
ok(c == 3, qid + ": c = 3")
c_el = raiz_exata(b2 - a2)


def par(p1, p2):
    return pt(*p1) + " e " + pt(*p2)


esp = [
    par((h + c_el, k), (h - c_el, k)),   # c² = 5 − 4
    par((h + a, k), (h - a, k)),         # vertices
    par((h, k + c), (h, k - c)),         # vertical
    par((h + c, k), (h - c, k)),         # certa
    par((-h + c, -k), (-h - c, -k)),     # centro com sinais trocados
]
confere_alts(qid, esp, 3)
ok(31 + 5 + 16 == 52, qid + ": 52 com o −16")
ok(pval(orig, 3, -2) == 0 and 45 - 16 - 30 + 32 - 31 == 0, qid + ": vertice (3, −2)")
ok(pval(orig, 4, F(1, 2)) == 0, qid + ": (4, 1/2) na curva")
d1 = raiz_exata((4 - 4) ** 2 + (F(1, 2) + 2) ** 2)
d2 = raiz_exata((4 + 2) ** 2 + (F(1, 2) + 2) ** 2)
ok(d1 == F(5, 2) and d2 == F(13, 2) and d2 - d1 == 2 * a, qid + ": distancias 5/2 e 13/2")
# erro: −4(y² − 4y) manda o centro para y = 2
k_err = -(F(16)) / (2 * F(-4))
ok(k_err == 2, qid + ": com +16y o centro iria para y = 2")
for t in ("5(x² − 2x) − 4(y² + 4y) = 31", "5(x − 1)² − 5 − 4(y + 2)² + 16 = 31", "5(x − 1)² − 4(y + 2)² = 20",
          "(x − 1)²/4 − (y + 2)²/5 = 1", "c² = a² + b² = 9", "= 52", "45 − 16 − 30 + 32 − 31 = 0", "√(36 + 25/4) = 13/2",
          "13/2 − 5/2 = 4", "h = −(−10)/(2·5) = 1", "k = −(−16)/(2·(−4)) = −2", "−4 × (−4) = +16"):
    cita(qid, t)
for r in itens(qid, "poligono"):
    ok(len(r["pts"]) == 41 and r.get("aberto") is True, qid + ": ramo 41 pontos aberto")
    ok(resid_max(r["pts"], lambda x, y: (x - 1) ** 2 / 4 - (y + 2) ** 2 / 5 - 1) < 0.003, qid + ": ramo fora da hiperbole")
inc = math.sqrt(5) / 2
for s in itens(qid, "segmento"):
    for q_ in (s["de"], s["ate"]):
        ok(abs(abs(q_[1] + 2) - inc * abs(q_[0] - 1)) < 0.006, qid + ": assintota da figura " + str(q_))
ok({it["rot"]: tuple(it["em"]) for it in itens(qid, "ponto")} == {"C": (1, -2), "F₁": (-2, -2), "F₂": (4, -2)}, qid + ": pontos da figura")

# ================= p08: x² + y² − 6x + 8y + k = 0, raio 2 =================
qid = "ga-s6-p08"
soma = F(6, 2) ** 2 + F(8, 2) ** 2
ok(soma == 25, qid + ": 9 + 16 = 25")
r = F(2)
k_ok = soma - r * r
esp = ["k = " + fmt(soma - r), "k = " + fmt(k_ok), "k = " + fmt(soma + r * r), "k = " + fmt(-k_ok), "k = " + fmt(-r * r)]
confere_alts(qid, esp, 1)
ok(soma - (-k_ok) == 46, qid + ": com k = −21, r² = 46")
ok(soma - (soma - r) == 2, qid + ": com k = 23, r² = 2")


def circ(x, y, kk):
    return F(x) ** 2 + F(y) ** 2 - 6 * F(x) + 8 * F(y) + kk


ok(circ(5, -4, k_ok) == 0 and circ(3, -2, k_ok) == 0, qid + ": pontos do confira")
ok(25 + 16 - 30 - 32 + 21 == 0 and 9 + 4 - 18 - 16 + 21 == 0, qid + ": somas do confira")
ok(raiz_exata(soma) == 5, qid + ": raio 5 com k = 0")
for t in ("x² − 6x = (x − 3)² − 9", "y² + 8y = (y + 4)² − 16", "9 + 16 − k = 25 − k", "25 − k = 4", "k = 25 − 4 = 21",
          "25 + 16 − 30 − 32 + 21 = 0", "9 + 4 − 18 − 16 + 21 = 0", "25 − 23 = 2", "√46", "25 + 4 = 29", "(6/2)² + (8/2)² − k = 9 + 16 − k"):
    cita(qid, t)
pol = itens(qid, "poligono")[0]
ok(len(pol["pts"]) == 40 and resid_max(pol["pts"], lambda x, y: (x - 3) ** 2 + (y + 4) ** 2 - 4) < 0.003, qid + ": circunferencia da figura")

# ================= p09: x²/4 + y²/9 − z²/16 = 1 =================
qid = "ga-s6-p09"
sinais = [1, 1, -1]
neg = sinais.count(-1)
tipo = {0: "Elipsoide", 1: "Hiperboloide de uma folha", 2: "Hiperboloide de duas folhas"}[neg]
ok(textos(qid)[idx_certa(qid)] == tipo, qid + ": certa")
ok(textos(qid) == ["Elipsoide", "Hiperboloide de duas folhas", "Cone elíptico", "Paraboloide hiperbólico", "Hiperboloide de uma folha"], qid + ": textos")
g9 = lambda x, y, z: x * x / 4 + y * y / 9 - z * z / 16 - 1
for pol in itens(qid, "poligono"):
    ok(resid_max(pol["pts"], g9) < 0.003, qid + ": figura fora da superficie")
ok(F(1) + F(16, 16) == 2, qid + ": corte z = 4 da 2")
ok(abs(2 * math.sqrt(2) - 2.828) < 0.0005 and abs(3 * math.sqrt(2) - 4.243) < 0.0005, qid + ": semieixos em z = ±4")
for t in ("x²/4 + y²/9 = 1 + k²/16", "x²/4 − z²/16 = 1", "x²/4 + y²/9 = 2", "−z²/16 = 1"):
    cita(qid, t)

# ================= p10: cone pelos tracos =================
qid = "ga-s6-p10"


def traco_z(fz, kz):
    """para superficie x²/4 + y²/9 = fz(z): devolve o lado direito no plano z = kz"""
    return fz(F(kz))


cone = lambda z: z * z
parab = lambda z: z
um = lambda z: 1 + z * z
dois = lambda z: z * z - 1
# corte z = 2 deve ser x²/16 + y²/36 = 1, ou x²/4 + y²/9 = 4
ok(traco_z(cone, 2) == 4, qid + ": cone em z = 2")
ok(traco_z(parab, 2) == 2 and F(4) * 2 == 8 and F(9) * 2 == 18, qid + ": paraboloide em z = 2 da x²/8 + y²/18 = 1")
ok(traco_z(cone, 0) == 0 and traco_z(parab, 0) == 0, qid + ": cone e paraboloide dao ponto em z = 0")
ok(traco_z(um, 0) == 1 and traco_z(dois, 0) == -1, qid + ": hiperboloides em z = 0")
ok(traco_z(um, 2) > 0 and traco_z(dois, 2) > 0, qid + ": hiperboloides dao elipse em z = 2")
# x = 0: cone y²/9 = z² -> y = ±3z
ok(raiz_exata(9) == 3, qid + ": y = ±3z")
ok(raiz_exata(36) == 6, qid + ": cilindro em x = 0 da y = ±6")
ok(textos(qid)[idx_certa(qid)] == "Cone elíptico x²/4 + y²/9 = z²", qid + ": certa")
gc = lambda x, y, z: x * x / 4 + y * y / 9 - z * z
for pol in itens(qid, "poligono"):
    ok(resid_max(pol["pts"], gc) < 0.003, qid + ": elipse fora do cone")
for s in itens(qid, "segmento"):
    for tt in (0, 0.25, 0.5, 0.75, 1):
        q_ = [s["de"][i] + tt * (s["ate"][i] - s["de"][i]) for i in range(3)]
        ok(abs(gc(*q_)) < 1e-9, qid + ": reta da figura fora do cone")
ok(itens(qid, "ponto")[0]["em"] == [0, 0, 0], qid + ": vertice")
for t in ("x²/8 + y²/18 = 1", "y² = 9z", "x²/(4a²) + y²/36 = 1", "4a² = 16", "y = 6 e y = −6"):
    cita(qid, t)

# ================= p11: 4x² + 9z² = 36 =================
qid = "ga-s6-p11"
g11 = lambda x, y, z: 4 * x * x + 9 * z * z
for p_ in ((3, 7, 0), (3, -100, 0), (3, 0, 0), (3, 5, 0), (3, -8, 0), (0, 2, 2)):
    ok(g11(*p_) == 36, qid + ": ponto " + str(p_))
ok(g11(0, 0, 3) == 81, qid + ": (0, 0, 3) da 81")
ok(F(36, 4) == 9 and F(36, 9) == 4, qid + ": x²/9 + z²/4 = 1")
ok(raiz_exata(36) == 6, qid + ": raio 6 do distrator")
ok(textos(qid)[idx_certa(qid)] == "Cilindro elíptico com geratrizes paralelas ao eixo y", qid + ": certa")
for pol in itens(qid, "poligono"):
    ok(resid_max(pol["pts"], lambda x, y, z: x * x / 9 + z * z / 4 - 1) < 0.0006, qid + ": elipse da figura")
for s in itens(qid, "segmento"):
    ok(s["de"][0] == s["ate"][0] and s["de"][2] == s["ate"][2] and abs(g11(*s["de"]) - 36) < 1e-9, qid + ": geratriz da figura")

# ================= p12: z = x² − y² − 2x + 4y =================
qid = "ga-s6-p12"
orig = padd(padd(sq(X), pesc(-1, sq(Y))), padd(pesc(-2, X), pesc(4, Y)))
red = padd(padd(sq(lin(cx=1, c0=-1)), pesc(-1, sq(lin(cy=1, c0=-2)))), P({(0, 0, 0): 3}))
ok(red == orig, qid + ": z = (x − 1)² − (y − 2)² + 3 nao reproduz a original")
S = (1, 2, pval(orig, 1, 2))
ok(S == (1, 2, 3), qid + ": ponto de sela")
esp = [
    "Paraboloide hiperbólico com ponto de sela " + pt(-1, -2, 3),
    "Paraboloide elíptico com vértice " + pt(*S),
    "Cone com vértice " + pt(*S),
    "Paraboloide hiperbólico com ponto de sela " + pt(*S),
    "Paraboloide hiperbólico com ponto de sela " + pt(1, 2, -3),
]
confere_alts(qid, esp, 3)
ok(-1 - 4 == -5, qid + ": constante errada −5 da conversa")
lin_y2 = [pval(orig, x, 2) for x in range(-1, 4)]
col_x1 = [pval(orig, 1, y) for y in range(0, 5)]
ok(min(lin_y2) == 3 and lin_y2.index(3) == 2 and lin_y2.count(3) == 1, qid + ": linha y = 2 minima em x = 1: " + str(lin_y2))
ok(max(col_x1) == 3 and col_x1.index(3) == 2 and col_x1.count(3) == 1, qid + ": coluna x = 1 maxima em y = 2: " + str(col_x1))
ok(1 - 4 - 2 + 8 == 3, qid + ": 1 − 4 − 2 + 8")
gz = lambda x, y, z: z - (x * x - y * y - 2 * x + 4 * y)
for pol in itens(qid, "poligono"):
    ok(resid_max(pol["pts"], gz) < 1e-9, qid + ": curva fora da sela")
for s in itens(qid, "segmento"):
    for tt in (0, 0.25, 0.5, 0.75, 1):
        q_ = [s["de"][i] + tt * (s["ate"][i] - s["de"][i]) for i in range(3)]
        ok(abs(gz(*q_)) < 1e-9, qid + ": reta do X fora da sela")
for t in ("x² − 2x = (x − 1)² − 1", "y² − 4y = (y − 2)² − 4", "z − 3 = (x − 1)² − (y − 2)²", "1 − 4 − 2 + 8 = 3",
          "x² − 2x + 1 − y² + 4y − 4 + 3 = x² − y² − 2x + 4y", "−1 + 4 = 3"):
    cita(qid, t)

# ================= teoria da semana =================
sem = docs["ga_s6_p1.json"]["semanas"]
ok(len(sem) == 1 and sem[0]["semana"] == 6 and sem[0]["previa"] is True, "teoria: semana 6 previa")
ok(sem[0]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "teoria: fonte")
ok(docs["ga_s6_p2.json"]["semanas"] == [], "teoria so na p1")
# bloco 5: 4x² + y² − 8x + 6y + 9 = 0  ->  4(x − 1)² + (y + 3)² = 4
orig = padd(padd(pesc(4, sq(X)), sq(Y)), padd(padd(pesc(-8, X), pesc(6, Y)), P({(0, 0, 0): 9})))
red = padd(padd(pesc(4, sq(lin(cx=1, c0=-1))), sq(lin(cy=1, c0=3))), P({(0, 0, 0): -4}))
ok(red == orig, "teoria: exemplo do bloco 5")
for d_ in (F(-3), F(1, 2), F(4)):
    ok(padd(sq(X), pesc(2 * d_, X)) == padd(sq(lin(cx=1, c0=d_)), P({(0, 0, 0): -d_ * d_})), "teoria: completar quadrado d=" + str(d_))
cs = [math.sqrt(25 - bb * bb) for bb in (1, 2, 3, 4, 5)]
ok(all(cs[i] > cs[i + 1] for i in range(4)) and cs[-1] == 0, "teoria: lab a = 5, b de 1 a 5")


# ================= tamanhos =================
def npal(s):
    return len(re.findall(r"\S+", s))


for b_ in sem[0]["blocos"]:
    n = npal(b_["texto"])
    ok(40 <= n <= 120, "teoria bloco '" + b_["titulo"] + "': " + str(n) + " palavras")
for kk, v in sem[0]["jeitos"].items():
    n = npal(v)
    ok(50 <= n <= 120, "teoria jeito " + kk + ": " + str(n) + " palavras")
for qid, q in sorted(Q.items()):
    j = q["jeitos"]
    for kk in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = npal(j[kk])
        ok(35 <= n <= 110, qid + " " + kk + ": " + str(n) + " palavras")
    ok(3 <= len(j["receita"]) <= 7, qid + ": receita com " + str(len(j["receita"])) + " passos")
    ok(4 <= len(j["conversa"]) <= 8, qid + ": conversa com " + str(len(j["conversa"])) + " falas")
    ok(q["origem"] == "Prévia · ementa" and q["semana"] == 6, qid + ": origem/semana")
    ok(q["figura"]["onde"] == "explicacao", qid + ": figura no enunciado")
    # resposta coerente com a certa (nao vazia, curta)
    ok(len(q["resposta"]) <= 110, qid + ": resposta longa")

# ================= distribuicao =================
ids = ["ga-s6-p%02d" % i for i in range(1, 13)]
ok(sorted(Q) == ids, "ids: " + str(sorted(Q)))
niveis = Counter(Q[i]["nivel"] for i in ids)
ok(niveis == Counter({1: 4, 2: 4, 3: 4}), "niveis " + str(niveis))
pos = Counter("ABCDE"[idx_certa(i)] for i in ids)
ok(max(pos.values()) <= 3, "posicoes " + str(pos))
print("niveis", dict(niveis), "posicoes", dict(sorted(pos.items())))
print("conferencias ok:", n_ok, "falhas:", len(falhas))
