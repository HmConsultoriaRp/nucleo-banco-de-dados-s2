# Segunda revisao adversarial do lote ga_s45 (Semanas 4 e 5 de Geometria Analitica).
# Refaz do zero cada resposta, cada conta de distrator e cada figura, sem usar o campo "resposta".
# Uso: python -I rev_ga_s45_r2_contas.py
import json, math, os, sys, re
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

Q = {}
SEM = {}
ARQ = {}
for nome in sorted(os.listdir(DADOS)):
    if nome.startswith("ga_s45_p") and nome.endswith(".json"):
        with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
            d = json.load(f)
        for s in d["semanas"]:
            SEM[s["semana"]] = s
        for q in d["questoes"]:
            Q[q["id"]] = q
            ARQ[q["id"]] = nome

ok = 0
falhas = []


def chk(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        falhas.append(msg)


def add(a, b): return tuple(x + y for x, y in zip(a, b))
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def mul(k, a): return tuple(k * x for x in a)
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def n2(a): return dot(a, a)
def paralelos(a, b): return cross(a, b) == (0, 0, 0)
def misto(a, b, c): return dot(cross(a, b), c)
def graus(c): return math.degrees(math.acos(c))
def graus_sen(s): return math.degrees(math.asin(s))


def certa(qid):
    q = Q[qid]
    cs = [(i, a["t"]) for i, a in enumerate(q["alternativas"]) if a.get("certa")]
    return cs[0]


def alt(qid, i):
    return Q[qid]["alternativas"][i]


def certa_eh(qid, letra, texto):
    i, t = certa(qid)
    chk("ABCDE"[i] == letra and t == texto, f"{qid}: certa esperada {letra} '{texto}', achei {'ABCDE'[i]} '{t}'")


def figura_itens(qid):
    return Q[qid].get("figura", {}).get("itens", [])


def perto(a, b, tol=0.006):
    return all(abs(float(x) - float(y)) <= tol for x, y in zip(a, b))


def na_reta(P, A, v, tol=0.006):
    # P - A paralelo a v, com tolerancia para coordenadas arredondadas
    w = [float(x) for x in sub(P, A)]
    vv = [float(x) for x in v]
    c = cross(w, vv)
    return math.sqrt(sum(x * x for x in c)) / math.sqrt(sum(x * x for x in vv)) <= tol


def no_plano(P, n, d, tol=0.006):
    return abs(sum(float(a) * float(b) for a, b in zip(n, P)) + float(d)) / math.sqrt(float(n2(n))) <= tol


# ------------------------------------------------------------------ s4-p01
qid = "ga-s4-p01"
A, B = (2, -1, 3), (5, 1, -1)
v = sub(B, A)
chk(v == (3, 2, -4), f"{qid}: diretor {v}")
certa_eh(qid, "B", "x = 2 + 3t, y = −1 + 2t, z = 3 − 4t")
chk(add(A, B) == (7, 0, 2), f"{qid}: A+B")
# alt A: reta A + t(7,0,2) passa por B?
chk(not paralelos(sub(B, A), (7, 0, 2)), f"{qid}: alt A passaria por B")
chk(add(A, (3, 2, 4)) == (5, 1, 7), f"{qid}: alt C t=1")
chk(not paralelos(sub(A, (-2, 1, -3)), v), f"{qid}: alt D passa por A")
chk(not paralelos((2, -1, 3), v), f"{qid}: alt E com diretor paralelo")
# texto do "erro" geral: as duas que nao partem de A (D e E) nunca passam por A
chk(not paralelos(sub(A, (3, 2, -4)), (2, -1, 3)), f"{qid}: alt E passa por A")
# figura
for it in figura_itens(qid):
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: segmento fora da reta")
    if it["tipo"] == "vetor":
        chk(tuple(it["de"]) == A and tuple(it["ate"]) == B, f"{qid}: vetor da figura")
# atalho: so B e D tem -4t no z
zs = {"A": "3 + 2t", "B": "3 − 4t", "C": "3 + 4t", "D": "−3 − 4t", "E": "−4 + 3t"}
for i, a in enumerate(Q[qid]["alternativas"]):
    chk(("z = " + zs["ABCDE"[i]]) in a["t"], f"{qid}: z da alternativa {'ABCDE'[i]}")

# ------------------------------------------------------------------ s4-p02
qid = "ga-s4-p02"
A, v = (1, -3, 4), (2, 1, -3)
def pert(P): return paralelos(sub(P, A), v)
cands = {"A": (4, 0, 7), "B": (2, 1, -3), "C": (5, -1, -1), "D": (7, 0, -5), "E": (3, -2, 7)}
for L, P in cands.items():
    chk(pert(P) == (L == "D"), f"{qid}: pertinencia de {L}")
certa_eh(qid, "D", "(7, 0, −5)")
chk(add(A, mul(3, v)) == (7, 0, -5), f"{qid}: t=3")
chk(F(4 - 1, 2) == F(3, 2) and 0 + 3 == 3, f"{qid}: alt A t's")
chk(F(2 - 1, 2) == F(1, 2) and 1 + 3 == 4, f"{qid}: alt B t's")
chk(4 - 3 * 2 == -2, f"{qid}: alt C z")
chk(4 + 3 == 7 and 4 - 3 * 1 == 1, f"{qid}: alt E z")
chk(sub((5, -1, -1), A) == (4, 2, -5), f"{qid}: confira (4,2,-5)")
# atalho: t = y + 3, testar no z
for L, P in cands.items():
    t = P[1] + 3
    chk((4 - 3 * t == P[2]) == (L == "D"), f"{qid}: atalho z de {L}")
for it in figura_itens(qid):
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: segmento")
    if it["tipo"] == "ponto" and it["rot"] == "fora":
        chk(not pert(tuple(it["em"])), f"{qid}: ponto fora")
    if it["tipo"] == "ponto" and it["rot"] == "t = 3":
        chk(tuple(it["em"]) == (7, 0, -5), f"{qid}: ponto t=3")

# ------------------------------------------------------------------ s4-p03
qid = "ga-s4-p03"
A, v = (2, -1, 5), (3, -2, 4)
certa_eh(qid, "A", "Ponto (2, −1, 5) e [[v]] = (3, −2, 4)")
chk(not paralelos((3, 2, 4), v), f"{qid}: alt D")
chk(not paralelos((F(1, 3), F(-1, 2), F(1, 4)), v), f"{qid}: alt E seria multiplo")
chk(F(1, 3) / 3 == F(1, 9) and F(1, 4) / 4 == F(1, 16), f"{qid}: alt E contas")
# (-2,1,-5) nao esta na reta; (3,-2,4) nao esta na reta
chk(not paralelos(sub((-2, 1, -5), A), v), f"{qid}: alt B ponto na reta")
chk(not paralelos(sub((3, -2, 4), A), v), f"{qid}: alt C ponto na reta")
chk(add(A, v) == (5, -3, 9), f"{qid}: confira passo")
for it in figura_itens(qid):
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: segmento")

# ------------------------------------------------------------------ s4-p04
qid = "ga-s4-p04"
P = (3, -2, 5)
certa_eh(qid, "E", "x = 3 e z = 5")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("cor") == 3:
        chk(it["de"][0] == 0 and it["de"][2] == 0 and it["ate"][0] == 0 and it["ate"][2] == 0, f"{qid}: eixo y")
    elif it["tipo"] == "segmento" and it["de"] == [3, -5, 5]:
        chk(it["ate"][0] == 3 and it["ate"][2] == 5, f"{qid}: reta x=3 z=5")

# ------------------------------------------------------------------ s4-p05
qid = "ga-s4-p05"
u, v = (2, -1, 1), (-1, 2, 1)
c = F(abs(dot(u, v))) ** 2 / (n2(u) * n2(v))
chk(dot(u, v) == -3 and n2(u) == 6 and n2(v) == 6 and c == F(1, 4), f"{qid}: cos^2")
chk(round(graus(0.5), 6) == 60, f"{qid}: 60")
certa_eh(qid, "C", "60°")
chk(round(graus(-0.5)) == 120, f"{qid}: alt A")
chk(round(math.degrees(math.asin(0.5))) == 30, f"{qid}: alt B")
u2 = (2, 1, 1)
chk(dot(u2, v) == 1 and n2(u2) == 6, f"{qid}: alt D conta")
chk(f"{graus(1/6):.2f}" == "80.41", f"{qid}: alt D {graus(1/6):.4f}")
p1, p2 = (1, -3, 4), (5, 0, -1)
chk(dot(p1, p2) == 1 and n2(p1) == 26 and n2(p2) == 26, f"{qid}: alt E conta")
chk(f"{graus(1/26):.2f}" == "87.80", f"{qid}: alt E {graus(1/26):.4f}")
mv = mul(-1, v)
chk(sub(u, mv) == (1, 1, 2) and n2((1, 1, 2)) == 6, f"{qid}: confira triangulo")

# ------------------------------------------------------------------ s4-p06
qid = "ga-s4-p06"
A, u, B, v = (1, 2, -1), (2, -4, 6), (3, -2, 5), (-1, 2, -3)
chk(paralelos(u, v) and paralelos(sub(B, A), u), f"{qid}: coincidentes")
chk(mul(F(-1, 2), u) == v, f"{qid}: -1/2")
chk(sub(B, A) == u, f"{qid}: B - A = u")
chk(dot(u, v) == -28, f"{qid}: alt E -28")
chk(add(B, mul(2, v)) == A, f"{qid}: confira h=2")
certa_eh(qid, "B", "Coincidentes")
for it in figura_itens(qid):
    if it["tipo"] in ("segmento", "vetor"):
        chk(na_reta(it["de"], A, u) and na_reta(it["ate"], A, u), f"{qid}: figura fora da reta")

# ------------------------------------------------------------------ s4-p07
qid = "ga-s4-p07"
A, u, B, v = (1, 2, 3), (1, -1, 2), (1, -4, 3), (1, 2, 2)
# resolve A + t u = B + h v pelas duas primeiras coordenadas (Cramer)
det = u[0] * (-v[1]) - (-v[0]) * u[1]
bx, by = B[0] - A[0], B[1] - A[1]
t = F(bx * (-v[1]) - (-v[0]) * by, det)
h = F(u[0] * by - u[1] * bx, det)
chk(add(A, mul(t, u)) == add(B, mul(h, v)), f"{qid}: interseccao")
chk((t, h) == (2, 2) and add(A, mul(t, u)) == (3, 0, 7), f"{qid}: P")
chk(not paralelos(u, v) and misto(u, v, sub(B, A)) == 0, f"{qid}: concorrentes")
certa_eh(qid, "C", "(3, 0, 7)")
# alt B: 2 + t = -4 + 2h com t = h -> h = 6
chk(F(6) == F(2 + 4, 1) and add(A, mul(6, u)) == (7, -4, 15) and add(B, mul(6, v)) == (7, 8, 15), f"{qid}: alt B")
chk(add(A, mul(-2, u)) == (-1, 4, -1) and add(B, mul(-2, v)) != (-1, 4, -1), f"{qid}: alt E")
chk(not paralelos(sub((-1, 4, -1), B), v), f"{qid}: alt E em s")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("cor") == 1:
        chk(na_reta(it["de"], A, u) and na_reta(it["ate"], A, u), f"{qid}: r")
    if it["tipo"] == "segmento" and it.get("cor") == 2:
        chk(na_reta(it["de"], B, v) and na_reta(it["ate"], B, v), f"{qid}: s")

# ------------------------------------------------------------------ s4-p08
qid = "ga-s4-p08"
A, B = (1, 2, 3), (4, 2, -3)
v = sub(B, A)
chk(v == (3, 0, -6), f"{qid}: diretor")
certa_eh(qid, "E", "(x − 1)/3 = (z − 3)/(−6) e y = 2")
chk(F(4 - 1, 3) == 1 and F(-3 - 3, 6) == -1, f"{qid}: alt B")
chk(F(4 - 1, 3) == F(-3 - 3, -6) == 1, f"{qid}: confira B")
for it in figura_itens(qid):
    if it["tipo"] in ("segmento", "vetor"):
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: figura")
    if it["tipo"] == "poligono":
        chk(all(p[1] == 2 for p in it["pts"]), f"{qid}: plano y=2")

# ------------------------------------------------------------------ s4-p09
qid = "ga-s4-p09"
A, u, B, v = (1, 0, 2), (1, 2, -1), (0, 1, -1), (2, 1, 1)
AB = sub(B, A)
chk(AB == (-1, 1, -3) and cross(u, v) == (3, -3, -3) and misto(u, v, AB) == 3, f"{qid}: misto")
chk(not paralelos(u, v), f"{qid}: nao paralelos")
certa_eh(qid, "B", "3; reversas")
chk(dot(cross(u, v), u) == 0, f"{qid}: alt A")
chk(dot((3, 3, -3), AB) == 9, f"{qid}: alt C")
# confira: x e y
t = F(1); h = F(1)
chk(1 + t == 2 * h and 2 * t == 1 + h and 2 - t == 1 and -1 + h == 0, f"{qid}: confira")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("cor") == 1:
        chk(na_reta(it["de"], A, u) and na_reta(it["ate"], A, u), f"{qid}: r")
    if it["tipo"] == "segmento" and it.get("cor") == 2:
        chk(na_reta(it["de"], B, v) and na_reta(it["ate"], B, v), f"{qid}: s")

# ------------------------------------------------------------------ s4-p10
qid = "ga-s4-p10"
A, u, v = (1, 2, 0), (1, -1, 2), (2, 1, 1)
uv = cross(u, v)
chk(uv == (-3, 3, 3), f"{qid}: u x v")
def mk(k, w=uv, usaPonto=False):
    AB = (k, 0, 3) if usaPonto else sub((k, 0, 3), A)
    return dot(w, AB)
# linear em k: a k + b
def raiz(fun):
    b = fun(F(0)); a = fun(F(1)) - b
    return F(-b, 1) / a
chk(raiz(lambda k: mk(k)) == 2, f"{qid}: k=2")
certa_eh(qid, "D", "k = 2")
chk(raiz(lambda k: mk(k, (-3, -3, 3))) == 6, f"{qid}: alt A")
chk(raiz(lambda k: -3 * k - 3 - 6 + 9) == 0, f"{qid}: alt B")
chk(raiz(lambda k: mk(k, uv, True)) == 3, f"{qid}: alt C")
chk(raiz(lambda k: mk(k, (-3, 3, -1))) == -2, f"{qid}: alt E")
B = (2, 0, 3)
chk(add(A, mul(F(5, 3), u)) == add(B, mul(F(1, 3), v)) == (F(8, 3), F(1, 3), F(10, 3)), f"{qid}: ponto comum")
# confira novo: determinante com k = 2 expandido pela primeira linha
AB2 = sub(B, A)
chk(AB2 == (1, -2, 3), f"{qid}: AB com k=2")
t1 = 1 * (1 * 3 - 1 * (-2)); t2 = -(-1) * (2 * 3 - 1 * 1); t3 = 2 * (2 * (-2) - 1 * 1)
chk((t1, t2, t3) == (5, 5, -10) and t1 + t2 + t3 == 0 == dot(u, cross(v, AB2)), f"{qid}: determinante")
# atalho novo: y e z sem k
tt = F(5, 3); hh = F(1, 3)
chk(2 - tt == hh and 2 * tt == 3 + hh and 1 + tt - 2 * hh == 2, f"{qid}: atalho sistema")
# conversa nova: produto misto com o ponto B
chk(dot(uv, (0, 0, 3)) == 9 and dot(uv, (1, 0, 0)) == -3, f"{qid}: conversa -3k + 9")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("cor") == 1:
        chk(na_reta(it["de"], A, u) and na_reta(it["ate"], A, u), f"{qid}: r")
    if it["tipo"] == "segmento" and it.get("cor") == 2:
        chk(na_reta(it["de"], B, v) and na_reta(it["ate"], B, v), f"{qid}: s")
    if it["tipo"] == "ponto" and it["rot"] == "P":
        chk(perto(it["em"], (F(8, 3), F(1, 3), F(10, 3))), f"{qid}: P")

# ------------------------------------------------------------------ s4-p11
qid = "ga-s4-p11"
P, A, v = (3, 3, -2), (1, 0, 0), (1, 1, 1)
t = F(dot(sub(P, A), v), n2(v))
Qp = add(A, mul(t, v))
w = sub(P, Qp)
chk(t == 1 and Qp == (2, 1, 1) and w == (1, 2, -3) and dot(w, v) == 0, f"{qid}: pe e diretor")
certa_eh(qid, "A", "X = (3, 3, −2) + h(1, 2, −3)")
chk(dot((2, 3, -2), v) == 3 and sub(P, A) == (2, 3, -2), f"{qid}: alt C")
# alt D: reta P + h(1,-1,0) corta r?  3+h = 1+t, 3-h = t, -2 = t
tD = -2; hD1 = 1 + tD - 3; hD2 = 3 - tD
chk(hD1 == -4 and hD2 == 5, f"{qid}: alt D sistema")
chk(misto((1, -1, 0), v, sub(A, P)) != 0, f"{qid}: alt D seria concorrente")
tE = F(dot(sub(A, P), v), n2(v))
QE = add(A, mul(tE, v))
chk(tE == -1 and QE == (0, -1, -1) and sub(P, QE) == (3, 4, -1) and dot((3, 4, -1), v) == 6, f"{qid}: alt E")
chk(paralelos(sub(P, A), v) is False, f"{qid}: alt B: P em r")
chk(n2(w) == 14, f"{qid}: sqrt14")
for it in figura_itens(qid):
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: r")

# ------------------------------------------------------------------ s4-p12
qid = "ga-s4-p12"
u = (1, 2, 1)
def cos2(m, pe=None, nv=None):
    vv = (m, 1, -1)
    p = dot(u, vv) if pe is None else pe(m)
    nn = n2(vv) if nv is None else nv(m)
    return F(p * p) / (n2(u) * nn)
chk(cos2(F(2)) == F(1, 4), f"{qid}: m=2")
# raizes de 4(m+1)^2 = 6(m^2+2) -> 2m^2 - 8m + 8 = 0
chk(all(cos2(F(m)) != F(1, 4) for m in range(-20, 21) if m != 2), f"{qid}: outra raiz inteira")
certa_eh(qid, "C", "m = 2")
# alt A: produto m - 1 -> (m+2)^2 = 0
chk(F((-2 - 1) ** 2) / (6 * ((-2) ** 2 + 2)) == F(1, 4), f"{qid}: alt A")
chk(-F(1, 2) + 1 == F(1, 2), f"{qid}: alt B")
# alt D: norma m^2 + 1 -> m^2 - 4m + 1 = 0 -> 2 +- sqrt3
for s in (1, -1):
    m = 2 + s * math.sqrt(3)
    chk(abs(4 * (m + 1) ** 2 - 6 * (m * m + 1)) < 1e-9, f"{qid}: alt D")
# alt E: cos = sqrt3/2 -> 4(m+1)^2 = 18(m^2+2) -> 14m^2 - 8m + 32 = 0
chk((-8) ** 2 - 4 * 14 * 32 < 0, f"{qid}: alt E sem raiz")
# maximo do cosseno em m = 2
melhor = max((float(cos2(F(i, 100))), i / 100) for i in range(-2000, 2001))
chk(abs(melhor[1] - 2) < 1e-9, f"{qid}: maximo em {melhor}")
chk(cos2(F(-2)) == F(1, 36), f"{qid}: confira m=-2 cos 1/6")
chk(sub(u, (2, 1, -1)) == (-1, 1, 2), f"{qid}: lado do triangulo")

# ------------------------------------------------------------------ s5-p01
qid = "ga-s5-p01"
P, n = (2, -1, 3), (3, 1, -2)
d = -dot(n, P)
chk(d == 1, f"{qid}: d")
certa_eh(qid, "D", "3x + y − 2z + 1 = 0")
chk(dot(n, P) - 1 == -2, f"{qid}: alt A")
chk(-dot(P, n) == 1 and 2 * 3 - 1 * 1 + 3 * (-2) == -1, f"{qid}: alt B troca de papeis d = 1")
chk(6 - 1 + 6 == 11, f"{qid}: alt C")
chk(dot(n, sub((0, 1, 1), P)) == 0 and dot(n, (0, 1, 1)) + d == 0, f"{qid}: confira")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, d) for p in it["pts"]), f"{qid}: poligono fora do plano")
    if it["tipo"] == "vetor":
        chk(tuple(it["de"]) == P and sub(tuple(it["ate"]), P) == n, f"{qid}: normal")

# ------------------------------------------------------------------ s5-p02
qid = "ga-s5-p02"
P, n, d = (1, -2, 4), (2, -1, 2), -5
val = dot(n, P) + d
chk(val == 7 and n2(n) == 9, f"{qid}: valor")
certa_eh(qid, "A", "7/3")
chk(abs(2 + 2 + 8 + 5) == 17 and 2 - 2 + 8 - 5 == 3, f"{qid}: alt D E")
Qp = sub(P, mul(F(val, n2(n)), n))
chk(Qp == (F(-5, 9), F(-11, 9), F(22, 9)) and dot(n, Qp) + d == 0, f"{qid}: pe")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, d) for p in it["pts"]), f"{qid}: poligono")
    if it["tipo"] == "ponto" and it["rot"] == "Q":
        chk(perto(it["em"], Qp), f"{qid}: Q")

# ------------------------------------------------------------------ s5-p03
qid = "ga-s5-p03"
n1, n2_ = (1, -1, 0), (0, 1, -1)
chk(dot(n1, n2_) == -1 and n2(n1) == 2 and n2(n2_) == 2, f"{qid}: contas")
certa_eh(qid, "E", "60°")
nn = (1, -1, 3)
cD = abs(dot(nn, n2_)) / math.sqrt(n2(nn) * n2(n2_))
chk(f"{graus(cD):.2f}" == "31.48", f"{qid}: alt D {graus(cD):.4f}")
chk(cross(n1, n2_) == (1, 1, 1), f"{qid}: reta comum")
a, b = (1, 1, -2), (2, -1, -1)
chk(dot(a, n1) == 0 and dot(a, (1, 1, 1)) == 0 and dot(b, n2_) == 0 and dot(b, (1, 1, 1)) == 0 and dot(a, b) == 3, f"{qid}: confira")
for it in figura_itens(qid):
    if it["tipo"] == "poligono" and it["cor"] == 1:
        chk(all(no_plano(p, n1, 3) for p in it["pts"]), f"{qid}: pi1")
    if it["tipo"] == "poligono" and it["cor"] == 2:
        chk(all(no_plano(p, n2_, -1) for p in it["pts"]), f"{qid}: pi2")
    if it["tipo"] == "ponto":
        chk(no_plano(it["em"], n1, 3) and no_plano(it["em"], n2_, -1), f"{qid}: Q nos dois")

# ------------------------------------------------------------------ s5-p04
qid = "ga-s5-p04"
A, u, v = (1, 0, 2), (1, 1, 0), (0, 1, -1)
n = cross(u, v); d = -dot(n, A)
chk(n == (-1, 1, 1) and d == -1, f"{qid}: plano")
cands = {"A": (2, 3, -1), "B": (3, 3, 1), "C": (1, 1, 0), "D": (3, 3, 3), "E": (2, 1, 1)}
for L, X in cands.items():
    chk((dot(n, X) + d == 0) == (L == "B"), f"{qid}: alternativa {L}")
    chk((X[1] + X[2] == X[0] + 1) == (L == "B"), f"{qid}: atalho {L}")
certa_eh(qid, "B", "(3, 3, 1)")
chk(add(mul(2, u), v) == (2, 3, -1) and add(A, add(mul(2, u), v)) == (3, 3, 1), f"{qid}: lambda mu")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, d) for p in it["pts"]), f"{qid}: poligono")

# ------------------------------------------------------------------ s5-p05
qid = "ga-s5-p05"
A, B, C = (1, 0, 2), (3, 1, 1), (0, 2, 3)
n = cross(sub(B, A), sub(C, A)); d = -dot(n, A)
chk(n == (3, -1, 5) and d == -13, f"{qid}: plano")
chk(all(dot(n, X) + d == 0 for X in (A, B, C)), f"{qid}: tres pontos")
certa_eh(qid, "C", "3x − y + 5z − 13 = 0")
chk(dot((3, 1, 5), B) - 13 == 2, f"{qid}: alt A")
chk(dot((2, 1, -1), B) == 6 and dot((2, 1, -1), A) == 0, f"{qid}: alt D")
chk(cross(A, B) == (-2, 5, 1) and dot((-2, 5, 1), C) == 13 and dot((-2, 5, 1), A) == 0 and dot((-2, 5, 1), B) == 0, f"{qid}: alt E")
G = mul(F(1, 3), add(add(A, B), C))
for it in figura_itens(qid):
    if it["tipo"] == "vetor" and it["rot"] == "n":
        chk(perto(it["de"], G) and perto(sub(it["ate"], it["de"]), mul(F(1, 2), n)), f"{qid}: n desenhado")
# atalho: so a certa zera com C
eqs = [((3, 1, 5), -13), ((3, -1, 5), 13), ((3, -1, 5), -13), ((2, 1, -1), 0), ((-2, 5, 1), 0)]
chk([dot(a_, C) + b_ == 0 for a_, b_ in eqs] == [False, False, True, False, False], f"{qid}: atalho C")

# ------------------------------------------------------------------ s5-p06
qid = "ga-s5-p06"
A, v, n, d = (1, 2, 0), (2, -1, 1), (1, 3, 1), -7
chk(dot(v, n) == 0 and dot(n, A) + d == 0, f"{qid}: contida")
certa_eh(qid, "D", "r está contida em π")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, d) for p in it["pts"]), f"{qid}: poligono")
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: reta")

# ------------------------------------------------------------------ s5-p07
qid = "ga-s5-p07"
v, n = (1, 1, 0), (1, 0, 1)
s_ = abs(dot(v, n)) / math.sqrt(n2(v) * n2(n))
chk(abs(graus_sen(s_) - 30) < 1e-9, f"{qid}: 30")
certa_eh(qid, "A", "30°")
chk(f"{graus_sen(2 / math.sqrt(6)):.2f}" == "54.74", f"{qid}: alt C")
chk(f"{graus_sen(1 / math.sqrt(12)):.2f}" == "16.78", f"{qid}: alt D")
chk(f"{graus_sen(0.25):.2f}" == "14.48", f"{qid}: alt E")
I = (5, 4, -1)
chk(I[0] + I[2] - 4 == 0 and na_reta(I, (2, 1, -1), v), f"{qid}: I")
sombra = sub(v, mul(F(1, 2), n))
chk(sombra == (F(1, 2), 1, F(-1, 2)) and dot(sombra, n) == 0, f"{qid}: sombra")
cs = dot(v, sombra) / math.sqrt(float(n2(v) * n2(sombra)))
chk(abs(cs - math.cos(math.radians(30))) < 1e-12, f"{qid}: cos sombra")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, -4) for p in it["pts"]), f"{qid}: poligono")
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], (2, 1, -1), v) and na_reta(it["ate"], (2, 1, -1), v), f"{qid}: reta")

# ------------------------------------------------------------------ s5-p08
qid = "ga-s5-p08"
n, d1, d2 = (2, -2, 1), F(-3), F(9, 2)
dist = abs(d1 - d2) / math.sqrt(n2(n))
chk(abs(d1 - d2) == F(15, 2) and n2(n) == 9 and abs(dist - 2.5) < 1e-12, f"{qid}: 5/2")
certa_eh(qid, "E", "5/2")
chk(F(12, 3) == 4 and F(12, 6) == 2 and abs(d1 + d2) / 3 == F(1, 2) and dot((4, -4, 2), (0, 0, 3)) + 9 == 15, f"{qid}: distratores")
P1 = mul(F(1, 3), n); P2 = mul(F(-1, 2), n)
chk(dot(n, P1) + d1 == 0 and dot(n, P2) + d2 == 0, f"{qid}: pes")
for it in figura_itens(qid):
    if it["tipo"] == "poligono" and it["cor"] == 1:
        chk(all(no_plano(p, n, d1) for p in it["pts"]), f"{qid}: pi1")
    if it["tipo"] == "poligono" and it["cor"] == 2:
        chk(all(no_plano(p, n, d2) for p in it["pts"]), f"{qid}: pi2")
    if it["tipo"] == "segmento":
        chk(perto(it["de"], P1) and perto(it["ate"], P2), f"{qid}: segmento")

# ------------------------------------------------------------------ s5-p09
qid = "ga-s5-p09"
P, A, v = (3, -2, 2), (1, -1, 2), (2, 1, -2)
AP = sub(P, A)
cr = cross(AP, v)
chk(AP == (2, -1, 0) and cr == (2, 4, 4) and n2(cr) == 36 and n2(v) == 9, f"{qid}: contas")
certa_eh(qid, "B", "2")
chk(dot(AP, v) == 3 and n2(AP) == 5, f"{qid}: alt D E")
Qp = add(A, mul(F(dot(AP, v), n2(v)), v))
chk(Qp == (F(5, 3), F(-2, 3), F(4, 3)) and n2(sub(P, Qp)) == 4, f"{qid}: pe")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("tracejado"):
        chk(na_reta(it["de"], A, v) and na_reta(it["ate"], A, v), f"{qid}: reta")
    if it["tipo"] == "poligono":
        chk([tuple(p) for p in it["pts"]] == [A, add(A, v), add(add(A, v), AP), P], f"{qid}: paralelogramo")

# ------------------------------------------------------------------ s5-p10
qid = "ga-s5-p10"
A, u, B, v = (1, 0, 2), (2, 1, 0), (4, -1, 4), (0, 1, 1)
uv = cross(u, v); AB = sub(B, A); m = dot(uv, AB)
chk(uv == (1, -2, 2) and n2(uv) == 9 and AB == (3, -1, 2) and m == 9, f"{qid}: contas")
certa_eh(qid, "D", "3")
chk(n2(AB) == 14 and n2(u) * n2(v) == 10 and dot(u, v) == 1, f"{qid}: distratores")
R = add(A, mul(1, u)); S = add(B, mul(0, v))
RS = sub(S, R)
chk(dot(RS, u) == 0 and dot(RS, v) == 0 and RS == uv, f"{qid}: perpendicular comum")
for it in figura_itens(qid):
    if it["tipo"] == "segmento" and it.get("cor") == 1:
        chk(na_reta(it["de"], A, u) and na_reta(it["ate"], A, u), f"{qid}: r")
    if it["tipo"] == "segmento" and it.get("cor") == 2:
        chk(na_reta(it["de"], B, v) and na_reta(it["ate"], B, v), f"{qid}: s")
    if it["tipo"] == "segmento" and it.get("cor") == 4:
        chk(tuple(it["de"]) == R and tuple(it["ate"]) == S, f"{qid}: RS")

# ------------------------------------------------------------------ s5-p11
qid = "ga-s5-p11"
n1, d1, n2v, d2 = (1, 1, -1), -2, (2, -1, 1), -1
dr = cross(n1, n2v)
chk(dr == (0, -3, -3) and not paralelos(n1, n2v), f"{qid}: diretor")
P0 = (1, 1, 0)
chk(dot(n1, P0) + d1 == 0 and dot(n2v, P0) + d2 == 0, f"{qid}: ponto")
certa_eh(qid, "A", "X = (1, 1, 0) + t(0, 1, 1)")
chk(dot(n1, (1, 2, -1)) + d1 == 2, f"{qid}: alt C")
chk(dot(n1, (1, 0, 1)) + d1 == -2, f"{qid}: alt D")
for it in figura_itens(qid):
    if it["tipo"] == "poligono" and it["cor"] == 1:
        chk(all(no_plano(p, n1, d1) for p in it["pts"]), f"{qid}: pi1")
    if it["tipo"] == "poligono" and it["cor"] == 2:
        chk(all(no_plano(p, n2v, d2) for p in it["pts"]), f"{qid}: pi2")
    if it["tipo"] == "segmento":
        chk(na_reta(it["de"], P0, (0, 1, 1)) and na_reta(it["ate"], P0, (0, 1, 1)), f"{qid}: reta")

# ------------------------------------------------------------------ s5-p12
qid = "ga-s5-p12"
n, d = (2, 1, -2), 4
sol = [k for k in range(-60, 61) if F(abs(dot(n, (1, k, 2)) + d), 3) == 3]
chk(sol == [-11, 7], f"{qid}: {sol}")
certa_eh(qid, "C", "k = 7 ou k = −11")
chk([k for k in range(-60, 61) if abs(k + 2) == 3] == [-5, 1], f"{qid}: alt B")
chk([k for k in range(-60, 61) if abs(k + 2) == 27] == [-29, 25], f"{qid}: alt D")
chk([k for k in range(-60, 61) if abs(k + 10) == 9] == [-19, -1], f"{qid}: alt E")
for it in figura_itens(qid):
    if it["tipo"] == "poligono":
        chk(all(no_plano(p, n, d) for p in it["pts"]), f"{qid}: poligono")
    if it["tipo"] == "segmento" and it.get("cor") == 4:
        de, ate = it["de"], it["ate"]
        chk(no_plano(ate, n, d) and paralelos(sub(tuple(ate), tuple(de)), n) and n2(sub(tuple(ate), tuple(de))) == 9, f"{qid}: perpendicular")
    if it["tipo"] == "segmento" and it.get("tracejado"):
        tem_reta = True
        chk(it["de"][0] == 1 and it["de"][2] == 2 and it["ate"][0] == 1 and it["ate"][2] == 2, f"{qid}: reta x=1 z=2")
chk(any(it["tipo"] == "segmento" and it.get("tracejado") for it in figura_itens(qid)), f"{qid}: falta a reta de P")
# a reta x = 1, z = 2 fura o plano em k = -2
chk(dot(n, (1, -2, 2)) + d == 0, f"{qid}: k = -2 no plano")

# ------------------------------------------------------------------ distribuicao
pos = {}
niv = {}
for qid, q in Q.items():
    i, _ = certa(qid)
    pos["ABCDE"[i]] = pos.get("ABCDE"[i], 0) + 1
    niv[(q["semana"], q["nivel"])] = niv.get((q["semana"], q["nivel"]), 0) + 1
    chk(q["origem"] == "Prévia · ementa", f"{qid}: origem")
esperados = [f"ga-s4-p{i:02d}" for i in range(1, 13)] + [f"ga-s5-p{i:02d}" for i in range(1, 13)]
chk(sorted(Q) == sorted(esperados), f"ids: {sorted(set(Q) ^ set(esperados))}")
chk(all(niv.get((s, n_), 0) == 4 for s in (4, 5) for n_ in (1, 2, 3)), f"niveis {niv}")
chk(max(pos.values()) <= 6, f"posicoes {pos}")
for s in (4, 5):
    chk(SEM[s]["previa"] is True and SEM[s]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", f"semana {s}: fonte")
chk(set(SEM) == {4, 5}, f"semanas {set(SEM)}")
chk(all(len(json.load(open(os.path.join(DADOS, f), encoding="utf-8"))["semanas"]) == 0 for f in os.listdir(DADOS) if f.startswith("ga_s45_p") and f != "ga_s45_p1.json"), "teoria fora da p1")

# ------------------------------------------------------------------ forma
def pal(s): return len(re.findall(r"\S+", s))
for nome in sorted(os.listdir(DADOS)):
    if not (nome.startswith("ga_s45_p") and nome.endswith(".json")):
        continue
    bruto = open(os.path.join(DADOS, nome), "rb").read()
    chk(not [b for b in bruto if b < 32 and b not in (10, 13)], f"{nome}: bytes de controle")
for qid, q in Q.items():
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n_ = pal(q["jeitos"][k])
        chk(35 <= n_ <= 110, f"{qid}.{k}: {n_} palavras")
    chk(3 <= len(q["jeitos"]["receita"]) <= 7, f"{qid}: receita")
    chk(4 <= len(q["jeitos"]["conversa"]) <= 8, f"{qid}: conversa")
for s in SEM.values():
    for i, b in enumerate(s["blocos"]):
        chk(40 <= pal(b["texto"]) <= 120, f"sem{s['semana']} bloco {i}: {pal(b['texto'])}")
    for k, t in s["jeitos"].items():
        chk(50 <= pal(t) <= 120, f"sem{s['semana']} jeito {k}: {pal(t)}")

print(f"{ok} checagens OK")
for f_ in falhas:
    print("FALHA", f_)
print("TUDO OK" if not falhas else f"{len(falhas)} falha(s)")
