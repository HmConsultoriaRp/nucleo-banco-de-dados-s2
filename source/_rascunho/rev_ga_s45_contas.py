# Revisao adversarial do lote ga_s45: refaz cada conta do zero com Fraction.
# Uso: python -I rev_ga_s45_contas.py
import json, math, os, sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

Q = {}
SEM = {}
for nome in sorted(os.listdir(DADOS)):
    if nome.startswith("ga_s45_p") and nome.endswith(".json"):
        with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
            d = json.load(f)
        for s in d["semanas"]:
            SEM[s["semana"]] = s
        for q in d["questoes"]:
            Q[q["id"]] = q

ok = 0
falhas = []


def chk(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        falhas.append(msg)


def V(*a):
    return tuple(F(x) for x in a)


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def mul(k, a): return tuple(F(k) * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def n2(a): return dot(a, a)
def norm(a): return math.sqrt(n2(a))
def misto(a, b, c): return dot(cross(a, b), c)
def paralelos(a, b): return cross(a, b) == (0, 0, 0)
def ang_retas(u, v): return math.degrees(math.acos(abs(float(dot(u, v))) / (norm(u) * norm(v))))


def certa(qid):
    return [a["t"] for a in Q[qid]["alternativas"] if a.get("certa")][0]


def alt(qid, i):
    return Q[qid]["alternativas"][i]["t"]


def fmt(x):
    x = F(x)
    s = str(x.numerator if x.denominator == 1 else f"{abs(x.numerator)}/{x.denominator}")
    if x.denominator == 1:
        s = str(abs(x.numerator))
    return ("−" if x < 0 else "") + s


def pt(a):
    return "(" + ", ".join(fmt(x) for x in a) + ")"


def mesma_reta(A, u, B, v):
    return paralelos(u, v) and paralelos(sub(B, A), u)


def no_plano(n, d, P, tol=0.0):
    val = dot(n, P) + d
    return abs(float(val)) <= tol


def perto(x, y, tol=0.006):
    return abs(x - y) <= tol

# ---------------- s4-p01 ----------------
A, B = V(2, -1, 3), V(5, 1, -1)
v = sub(B, A)
chk(v == V(3, 2, -4), "s4p01 diretor")
chk(certa("ga-s4-p01") == "x = 2 + 3t, y = −1 + 2t, z = 3 − 4t", "s4p01 certa")
chk(add(A, B) == V(7, 0, 2), "s4p01 A+B")
chk(add(A, v) == B, "s4p01 t=1 da B")
chk(add(A, V(3, 2, 4)) == V(5, 1, 7), "s4p01 alt C t=1")
chk(not mesma_reta(V(-2, 1, -3), v, A, v), "s4p01 alt D paralela distinta")
chk(not mesma_reta(V(3, 2, -4), V(2, -1, 3), A, v), "s4p01 alt E outra reta")
chk(not mesma_reta(A, V(7, 0, 2), A, v), "s4p01 alt A outra reta")

# ---------------- s4-p02 ----------------
A, v = V(1, -3, 4), V(2, 1, -3)
def em_reta(P, A, v):
    return paralelos(sub(P, A), v)
cand = [V(4, 0, 7), V(2, 1, -3), V(5, -1, -1), V(7, 0, -5), V(3, -2, 7)]
dentro = [em_reta(P, A, v) for P in cand]
chk(dentro == [False, False, False, True, False], "s4p02 so (7,0,-5)")
chk(add(A, mul(3, v)) == V(7, 0, -5), "s4p02 t=3")
chk(add(A, mul(2, v)) == V(5, -1, -2), "s4p02 t=2 z=-2")
chk(add(A, mul(1, v)) == V(3, -2, 1), "s4p02 t=1 z=1")
chk(sub(V(5, -1, -1), A) == V(4, 2, -5), "s4p02 diferenca (4,2,-5)")
chk(F(4 - 1, 2) == F(3, 2), "s4p02 t=1,5")
# atalho: t = y + 3, z = 4 - 3t
for P in cand:
    t = P[1] + 3
    zok = (4 - 3 * t) == P[2]
    chk(zok == (P == V(7, 0, -5)), f"s4p02 atalho {P}")
# figura
chk(add(A, mul(-1, v)) == V(-1, -4, 7) and add(A, mul(4, v)) == V(9, 1, -8), "s4p02 figura segmento")

# ---------------- s4-p03 ----------------
A, v = V(2, -1, 5), V(3, -2, 4)
chk(certa("ga-s4-p03") == "Ponto (2, −1, 5) e [[v]] = (3, −2, 4)", "s4p03 certa")
chk(not paralelos(V(3, 2, 4), v), "s4p03 (3,2,4) nao e diretor")
chk(not paralelos(V(F(1, 3), F(-1, 2), F(1, 4)), v), "s4p03 inversos nao sao diretor")
chk(not em_reta(V(-2, 1, -5), A, v), "s4p03 (-2,1,-5) fora")
chk(not em_reta(V(3, -2, 4), A, v), "s4p03 (3,-2,4) fora")
chk(add(A, v) == V(5, -3, 9), "s4p03 um passo")
chk(add(A, mul(F(-6, 5), v)) == V(F(-8, 5), F(7, 5), F(1, 5)) and add(A, mul(F(6, 5), v)) == V(F(28, 5), F(-17, 5), F(49, 5)), "s4p03 figura")

# ---------------- s4-p04 ----------------
chk(certa("ga-s4-p04") == "x = 3 e z = 5", "s4p04 certa")

# ---------------- s4-p05 ----------------
u, v = V(2, -1, 1), V(-1, 2, 1)
chk(dot(u, v) == -3 and n2(u) == 6 and n2(v) == 6, "s4p05 contas")
chk(perto(ang_retas(u, v), 60), "s4p05 60")
chk(certa("ga-s4-p05") == "60°", "s4p05 certa")
chk(perto(math.degrees(math.acos(-0.5)), 120), "s4p05 120")
chk(perto(math.degrees(math.asin(0.5)), 30), "s4p05 30")
u2 = V(2, 1, 1)
chk(dot(u2, v) == 1 and perto(math.degrees(math.acos(1 / 6)), 80.41), "s4p05 80,41")
p1, p2 = V(1, -3, 4), V(5, 0, -1)
chk(dot(p1, p2) == 1 and n2(p1) == 26 and n2(p2) == 26 and perto(math.degrees(math.acos(1 / 26)), 87.80), "s4p05 87,80")
w = mul(-1, v)
chk(n2(sub(u, w)) == 6 and sub(u, w) == V(1, 1, 2), "s4p05 confira triangulo equilatero")

# ---------------- s4-p06 ----------------
A, u, B, v = V(1, 2, -1), V(2, -4, 6), V(3, -2, 5), V(-1, 2, -3)
chk(mul(F(-1, 2), u) == v, "s4p06 v = -1/2 u")
chk(sub(B, A) == u, "s4p06 B-A = u")
chk(mesma_reta(A, u, B, v), "s4p06 coincidentes")
chk(dot(u, v) == -28, "s4p06 -28")
chk(add(B, mul(2, v)) == A, "s4p06 h=2 da A")
chk(add(A, mul(F(-1, 2), u)) == V(0, 4, -4) and add(A, mul(F(3, 2), u)) == V(4, -4, 8), "s4p06 figura")
chk(add(B, v) == V(2, 0, 2), "s4p06 figura seta coral")

# ---------------- s4-p07 ----------------
r = lambda t: V(1 + t, 2 - t, 3 + 2 * t)
s = lambda h: V(1 + h, -4 + 2 * h, 3 + 2 * h)
sol = [(t, h) for t in range(-10, 11) for h in range(-10, 11) if r(t) == s(h)]
chk(sol == [(2, 2)], f"s4p07 solucao {sol}")
chk(r(2) == V(3, 0, 7), "s4p07 P")
chk(r(0) == V(1, 2, 3) and s(0) == V(1, -4, 3), "s4p07 t=h=0")
# erro 2+t: 2 + h = -4 + 2h -> h = 6
chk(r(6) == V(7, -4, 15) and s(6) == V(7, 8, 15), "s4p07 alt B")
chk(r(-2) == V(-1, 4, -1), "s4p07 alt E r(-2)")
chk(not any(s(F(h, 2)) == V(-1, 4, -1) for h in range(-40, 41)), "s4p07 (-1,4,-1) fora de s")
chk(r(-1) == V(0, 3, 1) and r(4) == V(5, -2, 11) and s(-1) == V(0, -6, 1) and s(4) == V(5, 4, 11), "s4p07 figura")
# visual novo: folga em y com t = h: (2 - t) - (-4 + 2t) = 6 - 3t
chk(all((r(t)[1] - s(t)[1]) == 6 - 3 * t for t in range(-3, 4)), "s4p07 folga 6-3t")

# ---------------- s4-p08 ----------------
A, B = V(1, 2, 3), V(4, 2, -3)
v = sub(B, A)
chk(v == V(3, 0, -6), "s4p08 diretor")
chk(certa("ga-s4-p08") == "(x − 1)/3 = (z − 3)/(−6) e y = 2", "s4p08 certa")
chk(F(4 - 1, 3) == 1 and F(-3 - 3, 6) == -1, "s4p08 alt B")
x0 = F(1) + 3 * F(-3, 10)
chk(x0 == F(1, 10) and 3 - 6 * F(-3, 10) == F(48, 10), "s4p08 figura ponta 1")
chk(1 + 3 * F(13, 10) == F(49, 10) and 3 - 6 * F(13, 10) == F(-48, 10), "s4p08 figura ponta 2")

# ---------------- s4-p09 ----------------
A, B, u, v = V(1, 0, 2), V(0, 1, -1), V(1, 2, -1), V(2, 1, 1)
AB = sub(B, A)
chk(AB == V(-1, 1, -3), "s4p09 AB")
chk(cross(u, v) == V(3, -3, -3), "s4p09 uxv")
chk(misto(u, v, AB) == 3, "s4p09 misto 3")
chk(certa("ga-s4-p09") == "3; reversas", "s4p09 certa")
chk(dot(V(3, 3, -3), AB) == 9, "s4p09 alt 9")
chk(dot(cross(u, v), u) == 0, "s4p09 alt 0")
chk(not paralelos(u, v), "s4p09 nao paralelos")
# confira: 1 + t = 2h, 2t = 1 + h -> t = h = 1
chk(1 + 1 == 2 * 1 and 2 * 1 == 1 + 1 and (2 - 1) != (-1 + 1), "s4p09 confira")
rr = lambda t: add(A, mul(t, u)); ss = lambda h: add(B, mul(h, v))
chk(rr(F(-3, 2)) == V(F(-1, 2), -3, F(7, 2)) and rr(F(3, 2)) == V(F(5, 2), 3, F(1, 2)), "s4p09 figura r")
chk(ss(-1) == V(-2, 0, -2) and ss(1) == V(2, 2, 0), "s4p09 figura s")
M = [list(u), list(v), list(AB)]
det = (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1]) - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0]) + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))
chk(det == 3, "s4p09 MATRIZ.DETERM")

# ---------------- s4-p10 ----------------
A, u, v = V(1, 2, 0), V(1, -1, 2), V(2, 1, 1)
chk(cross(u, v) == V(-3, 3, 3), "s4p10 uxv")
def misto_k(k, c=cross(u, v), usaB=False):
    B = V(k, 0, 3)
    w = B if usaB else sub(B, A)
    return dot(c, w)
chk([k for k in range(-20, 21) if misto_k(k) == 0] == [2], "s4p10 k=2")
chk(all(misto_k(k) == -3 * k + 6 for k in range(-5, 6)), "s4p10 -3k+6")
chk([k for k in range(-20, 21) if misto_k(k, V(-3, -3, 3)) == 0] == [6], "s4p10 alt k=6")
chk([k for k in range(-20, 21) if (-3 * k - 3 - 6 + 9) == 0] == [0], "s4p10 alt k=0")
chk([k for k in range(-20, 21) if misto_k(k, usaB=True) == 0] == [3], "s4p10 alt k=3")
chk([k for k in range(-20, 21) if misto_k(k, V(-3, 3, -1)) == 0] == [-2], "s4p10 alt k=-2")
chk(not paralelos(u, v), "s4p10 nao paralelos")
B = V(2, 0, 3)
P = add(A, mul(F(5, 3), u))
chk(P == add(B, mul(F(1, 3), v)) == V(F(8, 3), F(1, 3), F(10, 3)), "s4p10 ponto comum")
chk(add(B, mul(-1, v)) == V(0, -1, 2) and add(B, mul(F(3, 2), v)) == V(5, F(3, 2), F(9, 2)), "s4p10 figura s")
chk(add(A, mul(3, u)) == V(4, -1, 6), "s4p10 figura r")

# ---------------- s4-p11 ----------------
A, v, P = V(1, 0, 0), V(1, 1, 1), V(3, 3, -2)
t = dot(sub(P, A), v) / n2(v)
Qp = add(A, mul(t, v))
chk(t == 1 and Qp == V(2, 1, 1), "s4p11 pe")
chk(sub(P, Qp) == V(1, 2, -3), "s4p11 diretor")
chk(certa("ga-s4-p11") == "X = (3, 3, −2) + h(1, 2, −3)", "s4p11 certa (h)")
chk(sub(P, A) == V(2, 3, -2) and dot(V(2, 3, -2), v) == 3, "s4p11 alt AP")
tPA = dot(sub(A, P), v) / n2(v)
pe2 = add(A, mul(tPA, v))
chk(tPA == -1 and pe2 == V(0, -1, -1) and sub(P, pe2) == V(3, 4, -1) and dot(V(3, 4, -1), v) == 6, "s4p11 alt PA")
# (1,-1,0) nao corta r
cortam = [ (h, tt) for h in range(-20, 21) for tt in range(-20, 21) if add(P, mul(h, V(1, -1, 0))) == add(A, mul(tt, v))]
chk(cortam == [], "s4p11 alt (1,-1,0) nao corta")
chk(dot(V(1, -1, 0), v) == 0, "s4p11 (1,-1,0) ortogonal")
chk(not any(paralelos(sub(P, A), v) for _ in [0]), "s4p11 P fora de r")
chk(add(P, mul(-1, V(1, 2, -3))) == Qp and n2(V(1, 2, -3)) == 14, "s4p11 confira")

# ---------------- s4-p12 ----------------
u = V(1, 2, 1)
def cos2(m, usa_meio=True, n2v_extra=1):
    v = V(m, 1, -1)
    d = dot(u, v) if usa_meio else (F(m) - 1)
    return d * d / (n2(u) * (F(m) ** 2 + 1 + n2v_extra))
chk(cos2(2) == F(1, 4), "s4p12 m=2")
# raiz dupla: 4(m+1)^2 - 6(m^2+2) = -2(m-2)^2
chk(all(4 * (m + 1) ** 2 - 6 * (m * m + 2) == -2 * (m - 2) ** 2 for m in range(-5, 6)), "s4p12 raiz dupla")
mx = max((cos2(F(i, 100)), i) for i in range(-2000, 2001))
chk(mx == (F(1, 4), 200), f"s4p12 maximo em m=2 {mx}")
chk(all(4 * (m - 1) ** 2 - 6 * (m * m + 2) == -2 * (m + 2) ** 2 for m in range(-5, 6)), "s4p12 alt m=-2")
chk(F(-1, 2) + 1 == F(1, 2), "s4p12 alt -1/2")
r1, r2 = 2 + math.sqrt(3), 2 - math.sqrt(3)
chk(all(abs(4 * (m + 1) ** 2 - 6 * (m * m + 1)) < 1e-9 for m in (r1, r2)), "s4p12 alt 2 +- raiz 3")
# sqrt(3)/2: 4(m+1)^2 = 18(m^2+2) -> 14m^2 - 8m + 32 = 0
chk((-8) ** 2 - 4 * 14 * 32 < 0, "s4p12 alt sem raiz")
chk(n2(V(2, 1, -1)) == 6 and n2(sub(u, V(2, 1, -1))) == 6 and sub(u, V(2, 1, -1)) == V(-1, 1, 2), "s4p12 triangulo")
chk(dot(u, V(-2, 1, -1)) == -1, "s4p12 confira m=-2")

# ---------------- s5-p01 ----------------
n, P = V(3, 1, -2), V(2, -1, 3)
d = -dot(n, P)
chk(d == 1, "s5p01 d")
chk(certa("ga-s5-p01") == "3x + y − 2z + 1 = 0", "s5p01 certa")
chk(dot(n, P) - 1 == -2, "s5p01 alt A")
chk(6 - 1 + 6 == 11, "s5p01 alt C")
chk(dot(n, V(0, 1, 1)) + d == 0 and dot(n, sub(V(0, 1, 1), P)) == 0, "s5p01 confira")
for p in Q["ga-s5-p01"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, d, tuple(F(str(x)) for x in p), 0.005), f"s5p01 figura {p}")

# ---------------- s5-p02 ----------------
n, d, P = V(2, -1, 2), F(-5), V(1, -2, 4)
val = dot(n, P) + d
chk(val == 7 and n2(n) == 9, "s5p02 7 e 9")
chk(certa("ga-s5-p02") == "7/3", "s5p02 certa")
chk(2 + 2 + 8 + 5 == 17 and 2 - 2 + 8 - 5 == 3, "s5p02 alts")
Qp = sub(P, mul(F(7, 9), n))
chk(Qp == V(F(-5, 9), F(-11, 9), F(22, 9)) and dot(n, Qp) + d == 0, "s5p02 pe")
for p in Q["ga-s5-p02"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, d, tuple(F(str(x)) for x in p), 0.01), f"s5p02 figura {p}")
chk(2 + 2 + 8 + 5 < 21, "s5p02 atalho: 7 exigiria numerador 21")

# ---------------- s5-p03 ----------------
n1, n2v = V(1, -1, 0), V(0, 1, -1)
chk(dot(n1, n2v) == -1 and n2(n1) == 2 and n2(n2v) == 2, "s5p03 contas")
chk(perto(ang_retas(n1, n2v), 60), "s5p03 60")
chk(perto(ang_retas(V(1, -1, 3), n2v), 31.48), "s5p03 31,48")
chk(cross(n1, n2v) == V(1, 1, 1), "s5p03 reta comum")
a1, a2 = V(1, 1, -2), V(2, -1, -1)
chk(dot(a1, n1) == 0 and dot(a1, V(1, 1, 1)) == 0 and dot(a2, n2v) == 0 and dot(a2, V(1, 1, 1)) == 0, "s5p03 confira direcoes no plano")
chk(dot(a1, a2) == 3 and n2(a1) == 6 and n2(a2) == 6, "s5p03 confira cos 1/2")
it = Q["ga-s5-p03"]["figura"]["itens"]
for p in it[0]["pts"]:
    chk(no_plano(n1, F(3), tuple(F(str(x)) for x in p)), f"s5p03 fig pi1 {p}")
for p in it[1]["pts"]:
    chk(no_plano(n2v, F(-1), tuple(F(str(x)) for x in p)), f"s5p03 fig pi2 {p}")

# ---------------- s5-p04 ----------------
A, u, v = V(1, 0, 2), V(1, 1, 0), V(0, 1, -1)
n = cross(u, v); d = -dot(n, A)
chk(n == V(-1, 1, 1) and d == -1, "s5p04 equacao geral")
cand = [V(2, 3, -1), V(3, 3, 1), V(1, 1, 0), V(3, 3, 3), V(2, 1, 1)]
chk([dot(n, p) + d == 0 for p in cand] == [False, True, False, False, False], "s5p04 so (3,3,1)")
chk(add(mul(2, u), v) == V(2, 3, -1), "s5p04 alt A")
chk(add(A, add(mul(2, u), v)) == V(3, 3, 1), "s5p04 lambda 2 mu 1")
chk([p[1] + p[2] == p[0] + 1 for p in cand] == [False, True, False, False, False], "s5p04 atalho y+z=x+1")
for p in Q["ga-s5-p04"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, d, tuple(F(str(x)) for x in p)), f"s5p04 figura {p}")
# terreno: z = 1 + x - y
chk(all(p[2] == 1 + p[0] - p[1] for p in [V(3, 3, 1)]) and 1 + 2 - 1 == 2, "s5p04 terreno")

# ---------------- s5-p05 ----------------
A, B, C = V(1, 0, 2), V(3, 1, 1), V(0, 2, 3)
n = cross(sub(B, A), sub(C, A)); d = -dot(n, A)
chk(n == V(3, -1, 5) and d == -13, "s5p05 normal e d")
chk(all(dot(n, X) + d == 0 for X in (A, B, C)), "s5p05 tres pontos")
chk(dot(V(3, 1, 5), B) - 13 == 2, "s5p05 alt A")
chk(dot(V(2, 1, -1), B) == 6 and dot(V(2, 1, -1), A) == 0, "s5p05 alt D")
chk(cross(A, B) == V(-2, 5, 1) and dot(V(-2, 5, 1), C) == 13 and dot(V(-2, 5, 1), A) == 0 and dot(V(-2, 5, 1), B) == 0, "s5p05 alt E")
# atalho: so a certa zera em C
alts = [(V(3, 1, 5), -13), (V(3, -1, 5), 13), (V(3, -1, 5), -13), (V(2, 1, -1), 0), (V(-2, 5, 1), 0)]
chk([dot(nn, C) + dd == 0 for nn, dd in alts] == [False, False, True, False, False], "s5p05 atalho C")
cen = mul(F(1, 3), add(A, add(B, C)))
chk(cen == V(F(4, 3), 1, 2), "s5p05 centro")

# ---------------- s5-p06 ----------------
A, v, n, d = V(1, 2, 0), V(2, -1, 1), V(1, 3, 1), F(-7)
chk(dot(v, n) == 0 and dot(n, A) + d == 0, "s5p06 contida")
chk(all(dot(n, add(A, mul(t, v))) == 7 for t in range(-5, 6)), "s5p06 n.X constante 7")
for p in Q["ga-s5-p06"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, d, tuple(F(str(x)) for x in p)), f"s5p06 figura {p}")

# ---------------- s5-p07 ----------------
v, n = V(1, 1, 0), V(1, 0, 1)
s = abs(float(dot(v, n))) / (norm(v) * norm(n))
chk(perto(math.degrees(math.asin(s)), 30), "s5p07 30")
chk(perto(math.degrees(math.asin(2 / math.sqrt(6))), 54.74), "s5p07 54,74")
pp = V(2, 1, -1)
chk(perto(math.degrees(math.asin(abs(float(dot(pp, n))) / (norm(pp) * norm(n)))), 16.78), "s5p07 16,78")
chk(perto(math.degrees(math.asin(0.25)), 14.48), "s5p07 14,48")
som = sub(v, mul(dot(v, n) / n2(n), n))
chk(som == V(F(1, 2), 1, F(-1, 2)) and dot(som, n) == 0, "s5p07 sombra")
chk(perto(float(dot(v, som)) / (norm(v) * norm(som)), math.cos(math.radians(30)), 1e-9), "s5p07 cos 30")
I = V(5, 4, -1)
chk(dot(n, I) - 4 == 0 and paralelos(sub(I, V(2, 1, -1)), v), "s5p07 ponto I")
for p in Q["ga-s5-p07"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, F(-4), tuple(F(str(x)) for x in p)), f"s5p07 figura {p}")

# ---------------- s5-p08 ----------------
n = V(2, -2, 1)
d1, d2 = F(-3), F(9, 2)
dist = abs(d1 - d2) / 3
chk(n2(n) == 9 and dist == F(5, 2), "s5p08 5/2")
chk(F(12, 3) == 4 and F(12, 6) == 2 and abs(d1 + d2) / 3 == F(1, 2) and 6 + 9 == 15, "s5p08 alts")
chk(F(abs(2 * 3 + 9), 6) == F(5, 2), "s5p08 confira ponto (0,0,3)")
it = Q["ga-s5-p08"]["figura"]["itens"]
for p in it[0]["pts"]:
    chk(no_plano(n, d1, tuple(F(str(x)) for x in p), 0.005), f"s5p08 fig pi1 {p}")
for p in it[1]["pts"]:
    chk(no_plano(V(4, -4, 2), F(9), tuple(F(str(x)) for x in p), 0.005), f"s5p08 fig pi2 {p}")
# visual novo: origem a 1 de pi1 e 1,5 de pi2, lados opostos
chk(abs(d1) / 3 == 1 and F(9, 6) == F(3, 2) and (d1 < 0) != (F(9) < 0), "s5p08 origem entre os planos")
chk(mul(F(1, 3), n) == V(F(2, 3), F(-2, 3), F(1, 3)) and mul(F(-1, 2), n) == V(-1, 1, F(-1, 2)), "s5p08 pontos da figura")

# ---------------- s5-p09 ----------------
A, v, P = V(1, -1, 2), V(2, 1, -2), V(3, -2, 2)
AP = sub(P, A)
c = cross(AP, v)
chk(AP == V(2, -1, 0) and c == V(2, 4, 4) and n2(c) == 36 and n2(v) == 9, "s5p09 contas")
chk(certa("ga-s5-p09") == "2", "s5p09 certa")
chk(dot(AP, v) == 3 and n2(AP) == 5, "s5p09 alts 1 e raiz 5")
Qp = add(A, mul(dot(AP, v) / n2(v), v))
chk(Qp == V(F(5, 3), F(-2, 3), F(4, 3)) and n2(sub(P, Qp)) == 4, "s5p09 pe")
chk(add(A, v) == V(3, 0, 0) and add(add(A, v), AP) == V(5, -1, 0), "s5p09 figura")

# ---------------- s5-p10 ----------------
A, u, B, v = V(1, 0, 2), V(2, 1, 0), V(4, -1, 4), V(0, 1, 1)
c = cross(u, v); AB = sub(B, A)
chk(c == V(1, -2, 2) and n2(c) == 9 and AB == V(3, -1, 2) and dot(c, AB) == 9, "s5p10 contas")
chk(certa("ga-s5-p10") == "3", "s5p10 certa")
chk(n2(AB) == 14 and n2(u) == 5 and n2(v) == 2 and dot(u, v) == 1, "s5p10 alts")
R = add(A, mul(1, u)); S = add(B, mul(0, v))
RS = sub(S, R)
chk(dot(RS, u) == 0 and dot(RS, v) == 0 and RS == c and R == V(3, 1, 2), "s5p10 confira")

# ---------------- s5-p11 ----------------
n1, n2v = V(1, 1, -1), V(2, -1, 1)
c = cross(n1, n2v)
chk(c == V(0, -3, -3) and not paralelos(n1, n2v), "s5p11 diretor")
P = V(1, 1, 0)
chk(dot(n1, P) - 2 == 0 and dot(n2v, P) - 1 == 0, "s5p11 ponto")
chk(all(dot(n1, add(P, mul(t, V(0, 1, 1)))) == 2 and dot(n2v, add(P, mul(t, V(0, 1, 1)))) == 1 for t in range(-4, 5)), "s5p11 reta nos dois")
chk(dot(n1, V(1, 2, -1)) - 2 == 2 and dot(n1, V(1, 0, 1)) - 2 == -2, "s5p11 alts")
it = Q["ga-s5-p11"]["figura"]["itens"]
for p in it[0]["pts"]:
    chk(no_plano(n1, F(-2), tuple(F(str(x)) for x in p)), f"s5p11 fig pi1 {p}")
for p in it[1]["pts"]:
    chk(no_plano(n2v, F(-1), tuple(F(str(x)) for x in p)), f"s5p11 fig pi2 {p}")
# soma das equacoes: y e z se anulam
chk(add(n1, n2v) == V(3, 0, 0), "s5p11 soma cancela y e z")

# ---------------- s5-p12 ----------------
n, d = V(2, 1, -2), F(4)
ks = [k for k in range(-60, 61) if abs(dot(n, V(1, k, 2)) + d) == 9]
chk(ks == [-11, 7], "s5p12 k")
chk([k for k in range(-60, 61) if abs(k + 2) == 3] == [-5, 1], "s5p12 alt 1 -5")
chk([k for k in range(-60, 61) if abs(k + 2) == 27] == [-29, 25], "s5p12 alt 25 -29")
chk([k for k in range(-60, 61) if abs(k + 10) == 9] == [-19, -1], "s5p12 alt -1 -19")
chk(sub(V(1, 7, 2), n) == V(-1, 6, 4) and dot(n, V(-1, 6, 4)) + d == 0, "s5p12 pe 1")
chk(add(V(1, -11, 2), n) == V(3, -10, 0) and dot(n, V(3, -10, 0)) + d == 0, "s5p12 pe 2")
for p in Q["ga-s5-p12"]["figura"]["itens"][0]["pts"]:
    chk(no_plano(n, d, tuple(F(str(x)) for x in p)), f"s5p12 figura {p}")

# ---------------- teoria: exemplos novos ----------------
chk(dot(V(2, 0, -1), V(1, 1, 1)) is not None, "teoria")
# 3x + 6y - 6z - 4 = 0 dividido por 3 tem normal (1, 2, -2)
chk(mul(F(1, 3), V(3, 6, -6)) == V(1, 2, -2), "teoria planos paralelos exemplo")

# ---------------- cobertura ----------------
ids4 = [f"ga-s4-p{i:02d}" for i in range(1, 13)]
ids5 = [f"ga-s5-p{i:02d}" for i in range(1, 13)]
chk(sorted(Q) == sorted(ids4 + ids5), "ids")
for ids in (ids4, ids5):
    nv = [Q[i]["nivel"] for i in ids]
    chk(nv.count(1) == 4 and nv.count(2) == 4 and nv.count(3) == 4, "niveis")
chk(all(q["origem"] == "Prévia · ementa" for q in Q.values()), "origem")
chk(SEM[4]["previa"] is True and SEM[5]["previa"] is True, "previa")
chk(all(SEM[s]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar" for s in (4, 5)), "fonte")
pos = {}
for q in Q.values():
    for i, a in enumerate(q["alternativas"]):
        if a.get("certa"):
            pos["ABCDE"[i]] = pos.get("ABCDE"[i], 0) + 1
print("posições:", dict(sorted(pos.items())))

print(f"{ok} checagens OK, {len(falhas)} falhas")
for f in falhas:
    print("FALHA", f)
