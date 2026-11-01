# Confere, lendo os JSON do lote ga_s45: coordenadas das figuras, alternativa certa,
# contas citadas nos textos (confira/atalho), tamanhos de texto e bytes de controle.
import json, math, os, re, sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(BASE, "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("ga_s45_p") and f.endswith(".json"))

def dot(a, b): return sum(x*y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def add(a, b): return tuple(x+y for x, y in zip(a, b))
def mul(k, a): return tuple(k*x for x in a)
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def norm(a): return math.sqrt(dot(a, a))

TOL = 0.02  # figuras usam 3 casas decimais
falhas = []
n_ok = 0
def check(c, msg):
    global n_ok
    if c:
        n_ok += 1
    else:
        falhas.append(msg)

def no_plano(p, n, d):
    return abs(dot(n, p) + d) < TOL * max(1, norm(n))
def na_reta(p, A, v):
    c = cross(sub(p, A), v)
    return norm(c) < TOL * norm(v) * 3
def perto(a, b):
    return norm(sub(a, b)) < TOL

Q = {}
semanas = []
bruto = b""
for a in arqs:
    caminho = os.path.join(DADOS, a)
    with open(caminho, "rb") as f:
        bruto += f.read()
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)
    semanas += d["semanas"]
    for q in d["questoes"]:
        Q[q["id"]] = q

# bytes de controle (fora \n \r \t)
ctrl = [b for b in bruto if b < 32 and b not in (9, 10, 13)]
check(not ctrl, f"bytes de controle encontrados: {ctrl[:10]}")
check("\\b" not in bruto.decode("utf-8") and "\\f" not in bruto.decode("utf-8"), "escape \\b ou \\f no JSON")

def itens(qid, tipo):
    return [i for i in Q[qid].get("figura", {}).get("itens", []) if i["tipo"] == tipo]
def certa(qid):
    return [x["t"] for x in Q[qid]["alternativas"] if x.get("certa")][0]

# ---------- alternativa certa esperada ----------
esperado = {
    "ga-s4-p01": "x = 2 + 3t, y = −1 + 2t, z = 3 − 4t",
    "ga-s4-p02": "(7, 0, −5)",
    "ga-s4-p03": "Ponto (2, −1, 5) e [[v]] = (3, −2, 4)",
    "ga-s4-p04": "x = 3 e z = 5",
    "ga-s4-p05": "60°",
    "ga-s4-p06": "Coincidentes",
    "ga-s4-p07": "(3, 0, 7)",
    "ga-s4-p08": "(x − 1)/3 = (z − 3)/(−6) e y = 2",
    "ga-s4-p09": "3; reversas",
    "ga-s4-p10": "k = 2",
    "ga-s4-p11": "X = (3, 3, −2) + λ(1, 2, −3)",
    "ga-s4-p12": "m = 2",
    "ga-s5-p01": "3x + y − 2z + 1 = 0",
    "ga-s5-p02": "7/3",
    "ga-s5-p03": "60°",
    "ga-s5-p04": "(3, 3, 1)",
    "ga-s5-p05": "3x − y + 5z − 13 = 0",
    "ga-s5-p06": "r está contida em π",
    "ga-s5-p07": "30°",
    "ga-s5-p08": "5/2",
    "ga-s5-p09": "2",
    "ga-s5-p10": "3",
    "ga-s5-p11": "X = (1, 1, 0) + t(0, 1, 1)",
    "ga-s5-p12": "k = 7 ou k = −11",
}
for k, v in esperado.items():
    check(certa(k) == v, f"{k}: certa no JSON = {certa(k)!r}, esperado {v!r}")
check(len(Q) == 24, f"total de questoes {len(Q)}")
niveis = {}
for k, q in Q.items():
    niveis.setdefault((q["semana"], q["nivel"]), []).append(k)
for s in (4, 5):
    for n in (1, 2, 3):
        check(len(niveis.get((s, n), [])) == 4, f"semana {s} nivel {n}: {len(niveis.get((s, n), []))} questoes")

# ---------- figuras: semana 4 ----------
# p01: reta por A e B
A, v = (2, -1, 3), (3, 2, -4)
for s in itens("ga-s4-p01", "segmento"):
    check(na_reta(tuple(s["de"]), A, v) and na_reta(tuple(s["ate"]), A, v), "s4p01 segmento fora da reta")
# p02
A, v = (1, -3, 4), (2, 1, -3)
s = itens("ga-s4-p02", "segmento")[0]
check(na_reta(tuple(s["de"]), A, v) and na_reta(tuple(s["ate"]), A, v), "s4p02 segmento")
pts = {p["rot"]: tuple(p["em"]) for p in itens("ga-s4-p02", "ponto")}
check(na_reta(pts["t = 3"], A, v) and not na_reta(pts["fora"], A, v), "s4p02 pontos")
# p03
A, v = (2, -1, 5), (3, -2, 4)
s = itens("ga-s4-p03", "segmento")[0]
check(na_reta(tuple(s["de"]), A, v) and na_reta(tuple(s["ate"]), A, v), "s4p03 segmento")
vv = itens("ga-s4-p03", "vetor")[0]
check(sub(tuple(vv["ate"]), tuple(vv["de"])) == v, "s4p03 vetor")
# p04
s = itens("ga-s4-p04", "segmento")[0]
check(s["de"][0] == 3 and s["ate"][0] == 3 and s["de"][2] == 5 and s["ate"][2] == 5, "s4p04 reta x=3 z=5")
# p05
vs = itens("ga-s4-p05", "vetor")
check(tuple(vs[0]["ate"]) == (2, -1, 1) and tuple(vs[1]["ate"]) == (-1, 2, 1), "s4p05 vetores")
# p06
A, u = (1, 2, -1), (2, -4, 6)
s = itens("ga-s4-p06", "segmento")[0]
check(na_reta(tuple(s["de"]), A, u) and na_reta(tuple(s["ate"]), A, u), "s4p06 segmento")
vb = itens("ga-s4-p06", "vetor")[1]
check(sub(tuple(vb["ate"]), tuple(vb["de"])) == (-1, 2, -3), "s4p06 vetor v")
# p07
sr, ss = itens("ga-s4-p07", "segmento")
check(na_reta(tuple(sr["de"]), (1, 2, 3), (1, -1, 2)) and na_reta(tuple(sr["ate"]), (1, 2, 3), (1, -1, 2)), "s4p07 r")
check(na_reta(tuple(ss["de"]), (1, -4, 3), (1, 2, 2)) and na_reta(tuple(ss["ate"]), (1, -4, 3), (1, 2, 2)), "s4p07 s")
# p08
pol = itens("ga-s4-p08", "poligono")[0]
check(all(p[1] == 2 for p in pol["pts"]), "s4p08 plano y=2")
s = itens("ga-s4-p08", "segmento")[0]
check(na_reta(tuple(s["de"]), (1, 2, 3), (3, 0, -6)) and na_reta(tuple(s["ate"]), (1, 2, 3), (3, 0, -6)), "s4p08 segmento")
# p09
sr, ss, sab = itens("ga-s4-p09", "segmento")
check(na_reta(tuple(sr["de"]), (1, 0, 2), (1, 2, -1)) and na_reta(tuple(sr["ate"]), (1, 0, 2), (1, 2, -1)), "s4p09 r")
check(na_reta(tuple(ss["de"]), (0, 1, -1), (2, 1, 1)) and na_reta(tuple(ss["ate"]), (0, 1, -1), (2, 1, 1)), "s4p09 s")
# texto do confira: 1 + t = 2h, 2t = 1 + h -> t = 1, h = 1; z: 1 e 0
t, h = 1, 1
check(1 + t == 2*h and 2*t == 1 + h and 2 - t == 1 and -1 + h == 0, "s4p09 confira")
# p10 (k = 2)
sr, ss = itens("ga-s4-p10", "segmento")
check(na_reta(tuple(sr["de"]), (1, 2, 0), (1, -1, 2)) and na_reta(tuple(sr["ate"]), (1, 2, 0), (1, -1, 2)), "s4p10 r")
check(na_reta(tuple(ss["de"]), (2, 0, 3), (2, 1, 1)) and na_reta(tuple(ss["ate"]), (2, 0, 3), (2, 1, 1)), "s4p10 s")
P = [p for p in itens("ga-s4-p10", "ponto") if p["rot"] == "P"][0]["em"]
check(perto(tuple(P), (8/3, 1/3, 10/3)), "s4p10 P")
# p11
s = itens("ga-s4-p11", "segmento")[0]
check(na_reta(tuple(s["de"]), (1, 0, 0), (1, 1, 1)) and na_reta(tuple(s["ate"]), (1, 0, 0), (1, 1, 1)), "s4p11 r")
vq = itens("ga-s4-p11", "vetor")[1]
dq = sub(tuple(vq["ate"]), tuple(vq["de"]))
check(dq == (1, 2, -3) and dot(dq, (1, 1, 1)) == 0, "s4p11 QP")
check(abs(norm((1, 2, -3)) - math.sqrt(14)) < 1e-12, "s4p11 raiz 14")
# p12: cos maximo em m = 2
def cos12(m):
    u = (1, 2, 1); w = (m, 1, -1)
    return abs(dot(u, w)) / (norm(u) * norm(w))
melhor = max((cos12(m/1000), m/1000) for m in range(-20000, 20001))
check(abs(melhor[1] - 2) < 0.01 and abs(melhor[0] - 0.5) < 1e-9, f"s4p12 maximo do cosseno {melhor}")
check(abs(norm(sub((1, 2, 1), (2, 1, -1))) - math.sqrt(6)) < 1e-12, "s4p12 triangulo equilatero")
check(abs(cos12(-2) - 1/6) < 1e-12, "s4p12 m=-2 da 1/6")

# ---------- figuras: semana 5 ----------
# p01
n, dd = (3, 1, -2), 1
pol = itens("ga-s5-p01", "poligono")[0]
check(all(no_plano(tuple(p), n, dd) for p in pol["pts"]), "s5p01 poligono")
vn = itens("ga-s5-p01", "vetor")[0]
check(sub(tuple(vn["ate"]), tuple(vn["de"])) == n, "s5p01 normal")
check(dot(n, (0, 1, 1)) + dd == 0 and dot(sub((0, 1, 1), (2, -1, 3)), n) == 0, "s5p01 confira")
# p02
n, dd = (2, -1, 2), -5
pol = itens("ga-s5-p02", "poligono")[0]
check(all(no_plano(tuple(p), n, dd) for p in pol["pts"]), "s5p02 poligono")
Qp = [p for p in itens("ga-s5-p02", "ponto") if p["rot"] == "Q"][0]["em"]
check(no_plano(tuple(Qp), n, dd) and abs(norm(sub((1, -2, 4), tuple(Qp))) - 7/3) < TOL, "s5p02 pe")
Qex = sub((1, -2, 4), mul(F(7, 9), n))
check(Qex == (F(-5, 9), F(-11, 9), F(22, 9)) and dot(n, Qex) + dd == 0, "s5p02 confira")
# p03
polA, polB = itens("ga-s5-p03", "poligono")
check(all(no_plano(tuple(p), (1, -1, 0), 3) for p in polA["pts"]), "s5p03 poligono pi1")
check(all(no_plano(tuple(p), (0, 1, -1), -1) for p in polB["pts"]), "s5p03 poligono pi2")
check(cross((1, -1, 0), (0, 1, -1)) == (1, 1, 1), "s5p03 confira cruz")
# p04
n4, A4 = (-1, 1, 1), (1, 0, 2)
pol = itens("ga-s5-p04", "poligono")[0]
check(all(abs(dot(n4, sub(tuple(p), A4))) < TOL for p in pol["pts"]), "s5p04 poligono")
for P in [(3, 3, 1), (2, 3, -1), (1, 1, 0), (3, 3, 3), (2, 1, 1)]:
    ok_atalho = (P[1] + P[2] == P[0] + 1)
    ok_plano = dot(n4, sub(P, A4)) == 0
    check(ok_atalho == ok_plano, f"s5p04 atalho y+z=x+1 em {P}")
# p05
n5, d5 = (3, -1, 5), -13
pol = itens("ga-s5-p05", "poligono")[0]
check(all(no_plano(tuple(p), n5, d5) for p in pol["pts"]), "s5p05 triangulo")
vn = itens("ga-s5-p05", "vetor")[2]
dn = sub(tuple(vn["ate"]), tuple(vn["de"]))
check(norm(cross(dn, n5)) < TOL * 10, "s5p05 seta normal paralela a n")
for alt, (nn, d0) in {"3x + y + 5z − 13 = 0": ((3, 1, 5), -13), "3x − y + 5z + 13 = 0": ((3, -1, 5), 13),
                      "2x + y − z = 0": ((2, 1, -1), 0), "−2x + 5y + z = 0": ((-2, 5, 1), 0)}.items():
    check(dot(nn, (0, 2, 3)) + d0 != 0, f"s5p05 atalho C elimina {alt}")
# p06
n6, d6 = (1, 3, 1), -7
pol = itens("ga-s5-p06", "poligono")[0]
check(all(no_plano(tuple(p), n6, d6) for p in pol["pts"]), "s5p06 poligono")
s = itens("ga-s5-p06", "segmento")[0]
check(no_plano(tuple(s["de"]), n6, d6) and no_plano(tuple(s["ate"]), n6, d6), "s5p06 reta no plano")
# p07
n7, d7 = (1, 0, 1), -4
pol = itens("ga-s5-p07", "poligono")[0]
check(all(no_plano(tuple(p), n7, d7) for p in pol["pts"]), "s5p07 poligono")
s = itens("ga-s5-p07", "segmento")[0]
check(na_reta(tuple(s["de"]), (2, 1, -1), (1, 1, 0)) and na_reta(tuple(s["ate"]), (2, 1, -1), (1, 1, 0)), "s5p07 reta")
sombra = sub((1, 1, 0), mul(0.5, n7))
check(dot(sombra, n7) == 0, "s5p07 sombra no plano")
cs = dot((1, 1, 0), sombra) / (norm((1, 1, 0)) * norm(sombra))
check(abs(cs - math.cos(math.radians(30))) < 1e-9, "s5p07 cos 30 da sombra")
# p08
polP, polQ = itens("ga-s5-p08", "poligono")
check(all(no_plano(tuple(p), (2, -2, 1), -3) for p in polP["pts"]), "s5p08 pi1")
check(all(no_plano(tuple(p), (4, -4, 2), 9) for p in polQ["pts"]), "s5p08 pi2")
s = itens("ga-s5-p08", "segmento")[0]
check(abs(norm(sub(tuple(s["de"]), tuple(s["ate"]))) - 2.5) < TOL, "s5p08 segmento 5/2")
# p09
pol = itens("ga-s5-p09", "poligono")[0]
check([tuple(p) for p in pol["pts"]] == [(1, -1, 2), (3, 0, 0), (5, -1, 0), (3, -2, 2)], "s5p09 paralelogramo")
check(norm(cross((2, -1, 0), (2, 1, -2))) == 6, "s5p09 area")
Qp = [p for p in itens("ga-s5-p09", "ponto") if p["rot"] == "Q"][0]["em"]
check(na_reta(tuple(Qp), (1, -1, 2), (2, 1, -2)) and abs(norm(sub((3, -2, 2), tuple(Qp))) - 2) < TOL, "s5p09 pe")
s = itens("ga-s5-p09", "segmento")[0]
check(na_reta(tuple(s["de"]), (1, -1, 2), (2, 1, -2)) and na_reta(tuple(s["ate"]), (1, -1, 2), (2, 1, -2)), "s5p09 reta")
# p10
sr, ss, sperp, sab = itens("ga-s5-p10", "segmento")
check(na_reta(tuple(sr["de"]), (1, 0, 2), (2, 1, 0)) and na_reta(tuple(sr["ate"]), (1, 0, 2), (2, 1, 0)), "s5p10 r")
check(na_reta(tuple(ss["de"]), (4, -1, 4), (0, 1, 1)) and na_reta(tuple(ss["ate"]), (4, -1, 4), (0, 1, 1)), "s5p10 s")
dp = sub(tuple(sperp["ate"]), tuple(sperp["de"]))
check(dot(dp, (2, 1, 0)) == 0 and dot(dp, (0, 1, 1)) == 0 and norm(dp) == 3, "s5p10 perpendicular comum")
check(dp == cross((2, 1, 0), (0, 1, 1)), "s5p10 RS = u x v")
# p11
polA, polB = itens("ga-s5-p11", "poligono")
check(all(no_plano(tuple(p), (1, 1, -1), -2) for p in polA["pts"]), "s5p11 pi1")
check(all(no_plano(tuple(p), (2, -1, 1), -1) for p in polB["pts"]), "s5p11 pi2")
s = itens("ga-s5-p11", "segmento")[0]
for p in (tuple(s["de"]), tuple(s["ate"])):
    check(no_plano(p, (1, 1, -1), -2) and no_plano(p, (2, -1, 1), -1), "s5p11 reta nos dois planos")
# p12
pol = itens("ga-s5-p12", "poligono")[0]
check(all(no_plano(tuple(p), (2, 1, -2), 4) for p in pol["pts"]), "s5p12 poligono")
for sg in itens("ga-s5-p12", "segmento"):
    check(no_plano(tuple(sg["ate"]), (2, 1, -2), 4) and abs(norm(sub(tuple(sg["de"]), tuple(sg["ate"]))) - 3) < 1e-9, "s5p12 perpendiculares")
for a, b in [(7, -11), (1, -5), (25, -29), (-1, -19)]:
    sim = (a + b) == -4
    check(sim == ((a, b) != (-1, -19)), f"s5p12 atalho simetria {a},{b}")

# ---------- tamanhos de texto (alvos do roteiro) ----------
def np(s): return len(re.findall(r"\S+", s))
for s in semanas:
    for b in s["blocos"]:
        w = np(b["texto"])
        check(40 <= w <= 120, f"semana {s['semana']} bloco '{b['titulo']}': {w} palavras")
    for k, t in s["jeitos"].items():
        w = np(t)
        check(50 <= w <= 120, f"semana {s['semana']} jeito {k}: {w} palavras")
fora = []
for k, q in Q.items():
    for lente in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        w = np(q["jeitos"][lente])
        if not 35 <= w <= 110:
            fora.append((k, lente, w))
    check(3 <= len(q["jeitos"]["receita"]) <= 7, f"{k} receita {len(q['jeitos']['receita'])}")
    check(4 <= len(q["jeitos"]["conversa"]) <= 8, f"{k} conversa")
check(not fora, f"jeitos fora de 35 a 110 palavras: {fora}")

print("checagens ok:", n_ok)
if falhas:
    print("FALHAS:")
    for f in falhas:
        print(" -", f)
else:
    print("FIGURAS E CONTAS DOS TEXTOS: OK")
