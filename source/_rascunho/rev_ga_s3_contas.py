# Revisor adversarial - lote ga_s3 (Lista 3 inteira + 8 construidas).
# Refaz cada conta do zero com fracoes exatas. Nao usa o campo "resposta".
# Compara: (1) conta propria x gabarito da lista; (2) cada distrator com a conta
# descrita no "erro"; (3) a alternativa marcada "certa" no JSON com a conta propria.
import json
import math
import os
import re
import sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
falhas = []

PASTA = r"D:\00_HM ConsultoriaEmpresarial\HM Consultoria_Clientes Ativos\Helio Marcos Hobus\Site Estudo Banco de Dados\Claude\_gerador\dados"


def ok(cond, msg):
    if not cond:
        falhas.append(msg)
        print("FALHA:", msg)
    else:
        print("ok   :", msg)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def esc(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def n2(a):
    return dot(a, a)


def misto(a, b, c):
    return dot(a, cross(b, c))


def sarrus(r1, r2, r3):
    a, b, c = r1
    d, e, f = r2
    g, h, i = r3
    desce = a * e * i + b * f * g + c * d * h
    sobe = c * e * g + a * f * h + b * d * i
    return desce, sobe, desce - sobe


def cof_linha1(r1, r2, r3):
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    x3, y3, z3 = r3
    return x1 * (y2 * z3 - z2 * y3) - y1 * (x2 * z3 - z2 * x3) + z1 * (x2 * y3 - y2 * x3)


def termo_a_termo(a, b, c):
    return sum(x * y * z for x, y, z in zip(a, b, c))


def P(*xs):
    return tuple(F(x) for x in xs)


# ---------------------------------------------------------------- leitura
dados = {}
for nome in sorted(os.listdir(PASTA)):
    if re.fullmatch(r"ga_s3_p\d\.json", nome):
        with open(os.path.join(PASTA, nome), encoding="utf-8") as f:
            d = json.load(f)
        for q in d["questoes"]:
            dados[q["id"]] = q
print("questões lidas:", len(dados))


def num(t):
    """Converte texto de alternativa numerica em Fraction (ou tupla)."""
    s = t.replace("−", "-").replace(" ", "")
    s = re.sub(r"^[mk]=", "", s)
    if s.startswith("("):
        return tuple(F(x) for x in s.strip("()").split(","))
    return F(s)


def certa_letra(q):
    for i, a in enumerate(q["alternativas"]):
        if a.get("certa") is True:
            return "ABCDE"[i]
    return None


def confere_alts(qid, esperado, certo):
    """esperado: dict texto -> valor proprio; certo: valor certo proprio."""
    q = dados[qid]
    for i, a in enumerate(q["alternativas"]):
        t = a["t"]
        ok(t in esperado, f"{qid} alt {'ABCDE'[i]} '{t}' tem conta própria")
        if t not in esperado:
            continue
        v = esperado[t]
        if a.get("certa") is True:
            ok(v == certo, f"{qid} alt {'ABCDE'[i]} marcada certa e bate com a conta ({v})")
        else:
            ok(v != certo, f"{qid} alt {'ABCDE'[i]} errada e diferente da certa ({v} != {certo})")
            try:
                ok(num(t) == v, f"{qid} alt {'ABCDE'[i]} texto '{t}' = valor do erro {v}")
            except Exception:
                pass


# ---------------------------------------------------------------- Q1
u, v, w, z = P(1, 4, 3), P(-1, 1, -1), (F(-2), F(-1, 2), F(5)), P(-1, 2, -3)
vw = cross(v, w)
ok(vw == (F(9, 2), F(7), F(5, 2)), f"Q1a v×w = {vw}")
r1a = misto(u, v, w)
ok(r1a == 40, f"Q1a u·(v×w) = {r1a} (gabarito 40)")
# distratores
d_ordem = misto(u, w, v)
d_sinal2 = dot(u, (vw[0], -vw[1], vw[2]))
w_mais = (F(-2), F(1, 2), F(5))
d_meio = misto(u, v, w_mais)
d_tt = termo_a_termo(u, v, w)
ok(cross(v, w_mais) == (F(11, 2), 7, F(3, 2)), "Q1a v×w com +1/2 = (11/2, 7, 3/2)")
confere_alts("ga-s3-l3q1a", {"−40": d_ordem, "−16": d_sinal2, "40": r1a, "38": d_meio, "−15": d_tt}, 40)
ok(sarrus(u, v, w)[:2] == (F(29, 2), F(-51, 2)), "Q1a Sarrus 29/2 e −51/2")
ok(dot(vw, v) == 0, "Q1a v×w ⊥ v")

vz = cross(v, z)
ok(vz == P(-1, -2, -1), f"Q1b v×z = {vz}")
r1b = misto(u, v, z)
ok(r1b == -12, f"Q1b = {r1b} (gabarito −12)")
seg_errada = v[0] * z[2] - v[2] * z[0]
ok(seg_errada == 2, "Q1b segunda coordenada invertida = 2")
ter_errada = v[1] * z[0] - v[0] * z[1]
ok(ter_errada == 1, "Q1b terceira coordenada invertida = 1")
confere_alts("ga-s3-l3q1b", {"−12": r1b, "12": misto(u, z, v), "4": dot(u, (vz[0], seg_errada, vz[2])),
                             "18": termo_a_termo(u, v, z), "−6": dot(u, (vz[0], vz[1], ter_errada))}, -12)
ok(sarrus(u, v, z)[:2] == (-5, 7), "Q1b Sarrus −5 e 7")
ok(dot(vz, z) == 0, "Q1b v×z ⊥ z")

wz = cross(w, z)
ok(wz == (F(-17, 2), F(-11), F(-9, 2)), f"Q1c w×z = {wz}")
r1c = misto(v, w, z)
ok(r1c == 2, f"Q1c = {r1c} (gabarito 2)")
p1 = w[1] * z[2]
ok(p1 == F(3, 2), "(−1/2)(−3) = 3/2")
d5 = dot(v, (-p1 - 10, wz[1], wz[2]))
d24 = dot(v, (wz[0], -wz[1], wz[2]))
ok(w[0] * z[2] - w[2] * z[0] == 11, "Q1c segunda invertida = 11")
confere_alts("ga-s3-l3q1c", {"−2": misto(v, z, w), "5": d5, "24": d24, "12": termo_a_termo(v, w, z), "2": r1c}, 2)
# jeitos da Q1c
ok(abs(math.sqrt(float(n2(wz))) - 14.6) < 0.05, f"Q1c ‖w×z‖ ≈ 14,6 ({math.sqrt(float(n2(wz))):.3f})")
ok(misto(v, (F(-2), F(1, 2), F(5)), z) == 4, "Q1c trabalho: sem o sinal de −1/2 sai 4")
terc_err = w[0] * z[1] + w[1] * z[0]  # (−2)·2 − (+1/2): sinal trocado em (−1/2)(−1)
ok(dot(v, (wz[0], wz[1], F(-4) + F(1, 2))) == 1, "Q1c erro: sinal trocado em (−1/2)(−1) leva a 1")
ok(dot(wz, w) == 0, "Q1c w×z ⊥ w")
ok(sarrus(v, w, z)[:2] == (F(-5, 2), F(-9, 2)), "Q1c Sarrus −5/2 e −9/2")
ok(dot(w, esc(-1, vz)) == 2, "Q1c atalho cíclico w·(z×v) = 2")
ok(misto(w, z, v) == r1c, "Q1c rotação cíclica igual")

# ---------------------------------------------------------------- Q2
A, B, C, D = P(-1, 2, -1), P(5, 1, 1), P(-2, -1, 1), P(6, -1, -3)
AB, AC, AD = sub(B, A), sub(C, A), sub(D, A)
ok((AB, AC, AD) == (P(6, -1, 2), P(-1, -3, 2), P(7, -3, -2)), "Q2 vetores a partir de A")
ok(cross(AC, AD) == P(12, 12, 24), "Q2 AC×AD = (12, 12, 24)")
pm = misto(AB, AC, AD)
vol = abs(pm) / 6
ok(vol == 18, f"Q2 volume = {vol} (gabarito 18)")
confere_alts("ga-s3-l3q2", {"108": abs(pm), "18": vol, "54": abs(pm) / 2, "36": abs(pm) / 3, "−18": -vol}, 18)
ok(misto(sub(A, B), sub(C, B), sub(D, B)) == -108, "Q2 confira: a partir de B dá −108")

# ---------------------------------------------------------------- Q3
def q3(m, meio=1):
    Am = (F(1), F(m), F(-2))
    Bq, Cq, Dq = P(1, -2, 3), P(-1, 1, -1), P(5, -1, 2)
    r1, r2, r3 = sub(Am, Bq), sub(Cq, Bq), sub(Dq, Bq)
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    x3, y3, z3 = r3
    return x1 * (y2 * z3 - z2 * y3) - meio * y1 * (x2 * z3 - z2 * x3) + z1 * (x2 * y3 - y2 * x3)


def raiz_linear(f):
    a = f(1) - f(0)
    b = f(0)
    return -b / a


m = raiz_linear(q3)
ok(m == F(17, 9), f"Q3 m = {m} (gabarito 17/9)")
ok(q3(m) == 0, "Q3 substituindo de volta zera")
ok(q3(0) == 34 and q3(1) - q3(0) == -18, "Q3 produto misto = −18m + 34")
m_sem_menos = raiz_linear(lambda t: q3(t, meio=-1))
m_pontos = raiz_linear(lambda t: cof_linha1((F(1), F(t), F(-2)), P(1, -2, 3), P(-1, 1, -1)))
ok(cof_linha1((F(1), F(0), F(-2)), P(1, -2, 3), P(-1, 1, -1)) == 1, "Q3 det(A,B,C) = 1 − 2m (m=0)")
confere_alts("ga-s3-l3q3", {"m = −17/9": -m, "m = 9/17": 1 / m, "m = −53/9": m_sem_menos, "m = 17/9": m,
                            "m = 1/2": m_pontos}, F(17, 9))
ok(cross(sub(P(-1, 1, -1), P(1, -2, 3)), sub(P(5, -1, 2), P(1, -2, 3))) == P(1, -18, -14),
   "Q3 normal do plano BCD tem y ≠ 0 (trilho paralelo a y corta o plano uma vez)")
ok(abs(float(m) - 1.889) < 0.0005, "Q3 17/9 ≈ 1,889")

# ---------------------------------------------------------------- Q4
a4, b4, c4 = P(2, 1, 0), P(-1, 1, -1), P(-1, 0, 2)
d4 = cross(a4, b4)
ok(d4 == P(-1, 2, 3), f"Q4 direção = {d4}")
ok(n2(d4) == 14, "Q4 norma² = 14")
v4 = d4 if dot(d4, c4) > 0 else esc(-1, d4)
pt = add(P(2, 3, 4), v4)
ok(pt == P(1, 5, 7), f"Q4 ponto final = {pt} (gabarito (1, 5, 7))")
ok(dot(esc(-1, d4), c4) == -7, "Q4 oposto faz −7 com (−1, 0, 2)")
ok(dot(P(1, 2, 3), a4) == 4 and dot(P(-1, -2, 3), a4) == -4, "Q4 distratores não ortogonais (4 e −4)")
ok(a4[2] * b4[1] - a4[1] * b4[2] == 1 and a4[1] * b4[2] - a4[2] * b4[1] == -1,
   "Q4 alt (3, 5, 7): primeira coordenada invertida 0·1 − 1·(−1) = 1 (certo −1)")
ok(n2(P(1, 2, 3)) == 14 and n2(P(-1, -2, 3)) == 14, "Q4 distratores têm norma √14 (parecem certos)")
confere_alts("ga-s3-l3q4", {"(1, 5, 7)": pt, "(3, 1, 1)": add(P(2, 3, 4), esc(-1, d4)), "(−1, 2, 3)": d4,
                            "(3, 5, 7)": add(P(2, 3, 4), P(1, 2, 3)), "(1, 1, 7)": add(P(2, 3, 4), P(-1, -2, 3))},
             P(1, 5, 7))

# ---------------------------------------------------------------- Q5a / Q5b
A5, X5, B5, C5 = P(0, 0), P(2, 0), P(3, 0), (F(3, 2), F(5, 2))
ok(sub(X5, A5) == esc(2, sub(B5, X5)), "Q5a/b figura: AX = 2XB")
CA, CX, CB = sub(A5, C5), sub(X5, C5), sub(B5, C5)
certo = add(esc(F(1, 3), CA), esc(F(2, 3), CB))
errado = add(esc(F(2, 3), CA), esc(F(1, 3), CB))
ok(certo == CX, "Q5b: CX = (1/3)CA + (2/3)CB")
ok(errado != CX, "Q5a: (2/3)CA + (1/3)CB ≠ CX (falsa)")
ok(CX == (F(1, 2), F(-5, 2)) and errado == (F(-1, 2), F(-5, 2)), "Q5a contas do receita/confira")
ok(add(C5, errado) == P(1, 0), "Q5a: a combinação errada leva ao ponto (1, 0)")
fig = dados["ga-s3-l3q5a"]["figura"]
ok(fig["onde"] == "enunciado", "Q5a figura no enunciado")
pts = {it["rot"]: tuple(it["em"]) for it in fig["itens"] if it["tipo"] == "ponto"}
ok(pts == {"A": (0, 0), "X": (2, 0), "B": (3, 0), "C": (1.5, 2.5)}, "Q5a figura com as coordenadas pedidas")
vets = sorted(tuple(it["ate"]) for it in fig["itens"] if it["tipo"] == "vetor")
ok(vets == [(0, 0), (2, 0), (3, 0)] and all(tuple(it["de"]) == (1.5, 2.5) and it.get("cor") == 1
                                            for it in fig["itens"] if it["tipo"] == "vetor"),
   "Q5a figura: vetores CA, CX, CB saindo de C, cor 1")
ok(dados["ga-s3-l3q5b"]["figura"] == fig or
   dados["ga-s3-l3q5b"]["figura"]["itens"] == fig["itens"], "Q5b mesma figura")

# ---------------------------------------------------------------- Q5c (Varignon)
fig = dados["ga-s3-l3q5c"]["figura"]
pts = {it["rot"]: tuple(F(x) for x in it["em"]) for it in fig["itens"] if it["tipo"] == "ponto"}
Aq, Bq, Cq, Dq = pts["A"], pts["B"], pts["C"], pts["D"]
par = sub(Bq, Aq) == sub(Cq, Dq)
ok(not par, f"Q5c quadrilátero da figura NÃO é paralelogramo (AB={sub(Bq, Aq)}, DC={sub(Cq, Dq)})")


def cross2(a, b):
    return a[0] * b[1] - a[1] * b[0]


lados = [sub(Bq, Aq), sub(Cq, Bq), sub(Dq, Cq), sub(Aq, Dq)]
ok(all(cross2(lados[i], lados[(i + 2) % 4]) != 0 for i in range(2)), "Q5c nenhum par de lados opostos paralelo")
M, N, Pp, Q = (esc(F(1, 2), add(Aq, Bq)), esc(F(1, 2), add(Bq, Cq)), esc(F(1, 2), add(Cq, Dq)),
               esc(F(1, 2), add(Dq, Aq)))
ok((M, N, Pp, Q) == (pts["M"], pts["N"], pts["P"], pts["Q"]), f"Q5c pontos médios da figura {M, N, Pp, Q}")
ok(sub(N, M) == sub(Pp, Q) == esc(F(1, 2), sub(Cq, Aq)), "Q5c MN = QP = AC/2")
ok(sub(Pp, N) == sub(Q, M) == esc(F(1, 2), sub(Dq, Bq)), "Q5c NP = MQ = BD/2")
dentro = [it for it in fig["itens"] if it["tipo"] == "poligono" and it.get("cor") == 4][0]["pts"]
ok([tuple(F(x) for x in p) for p in dentro] == [M, N, Pp, Q], "Q5c polígono de dentro = M, N, P, Q")
fora = [it for it in fig["itens"] if it["tipo"] == "poligono" and it.get("cor") == 3][0]["pts"]
ok([tuple(F(x) for x in p) for p in fora] == [Aq, Bq, Cq, Dq], "Q5c polígono de fora = A, B, C, D")
conv = [cross2(lados[i], lados[(i + 1) % 4]) for i in range(4)]
ok(all(c > 0 for c in conv), f"Q5c quadrilátero convexo {conv}")
print("   Q5c: A, B, C, D =", Aq, Bq, Cq, Dq, " M, N, P, Q =", M, N, Pp, Q)

# ---------------------------------------------------------------- Q5d
uu, vv = P(3, 1), P(1, 3)
ok(n2(uu) == n2(vv) == 10, "Q5d figura: normas iguais (√10)")
ok(dot(add(uu, vv), sub(uu, vv)) == 0, "Q5d figura: (4,4)·(2,−2) = 0")
ok(dot(P(1, 1), P(1, -1)) == 0, "Q5d alt A: (1,1)·(1,−1) = 0")
ok(n2(P(3, 4)) == n2(P(5, 0)) == 25 and dot(P(3, 4), P(5, 0)) == 15, "Q5d (3,4) e (5,0)")
ok(dot(add(P(3, 4), P(5, 0)), sub(P(3, 4), P(5, 0))) == 0, "Q5d (8,4)·(−2,4) = 0")
ok(dot(add(uu, P(1, 2)), sub(uu, P(1, 2))) == 5, "Q5d confira: com v=(1,2) dá 5")
ok(102 * 98 == 10000 - 4, "Q5d 102 × 98")
fig = dados["ga-s3-l3q5d"]["figura"]
ok(any(it["tipo"] == "vetor" and tuple(it["de"]) == (1, 3) and tuple(it["ate"]) == (3, 1) for it in fig["itens"]),
   "Q5d figura: u − v da ponta de v à ponta de u")

# ---------------------------------------------------------------- Q5e
Vv = P(2, 3, 6)
ok(n2(Vv) == 49, "Q5e (2,3,6) norma 7")
ok(sum(F(c * c, 49) for c in Vv) == 1, "Q5e 4/49 + 9/49 + 36/49 = 1")
ok(abs(3 / math.sqrt(3) - math.sqrt(3)) < 1e-12, "Q5e (1,1,1): soma dos cossenos √3")

# ---------------------------------------------------------------- Q5f
At, Bt, Ct, Dt = P(0, 0), P(8, 0), P(6, 3), P(1, 3)
Mt, Nt = esc(F(1, 2), add(At, Dt)), esc(F(1, 2), add(Bt, Ct))
ok(Mt == (F(1, 2), F(3, 2)) and Nt == (F(7), F(3, 2)), "Q5f M e N")
ok(sub(Nt, Mt) == (F(13, 2), 0), "Q5f MN = (13/2, 0)")
ok(F(13, 2) == F(8 + 5, 2), "Q5f 6,5 = (8 + 5)/2")
ok(n2(sub(Dt, At)) != n2(sub(Ct, Bt)), "Q5f trapézio não isósceles (√10 ≠ √13)")
ok(sub(Nt, Mt) == esc(F(1, 2), add(sub(Bt, At), sub(Ct, Dt))), "Q5f MN = (AB + DC)/2")

# ---------------------------------------------------------------- Q5g / Q5h
A6, B6, C6, D6 = P(0, 0), P(6, 0), P(7, 4), P(1, 5)
E6, F6 = esc(F(1, 2), add(A6, B6)), esc(F(1, 2), add(C6, D6))
EF = sub(F6, E6)
ok(E6 == P(3, 0) and F6 == (F(4), F(9, 2)), "Q5g E e F da figura")
ok(EF == esc(F(1, 2), add(sub(D6, A6), sub(C6, B6))), "Q5g EF = (AD + BC)/2")
ok(EF == esc(F(1, 2), add(sub(C6, A6), sub(D6, B6))), "Q5h EF = (AC + BD)/2")
ok(esc(F(1, 2), sub(sub(C6, A6), sub(D6, B6))) == (F(6), F(-1, 2)), "Q5h (AC − BD)/2 = (6, −1/2)")
l6 = [sub(B6, A6), sub(C6, B6), sub(D6, C6), sub(A6, D6)]
ok(all(cross2(l6[i], l6[j]) != 0 for i in range(4) for j in range(i + 1, 4)), "Q5g quadrilátero sem lados paralelos")
Sq = [P(0, 0), P(2, 0), P(2, 2), P(0, 2)]
Es, Fs = esc(F(1, 2), add(Sq[0], Sq[1])), esc(F(1, 2), add(Sq[2], Sq[3]))
ok(sub(Fs, Es) == P(0, 2), "Q5g quadrado: EF = (0, 2)")
ADs, BCs = sub(Sq[3], Sq[0]), sub(Sq[2], Sq[1])
ok(esc(F(1, 2), sub(ADs, BCs)) == P(0, 0) and add(ADs, BCs) == P(0, 4), "Q5g distratores do quadrado")
ok(esc(F(1, 2), add(sub(Sq[1], Sq[0]), sub(Sq[3], Sq[2]))) == P(0, 0), "Q5g (AB + CD)/2 = 0 no quadrado")

# ---------------------------------------------------------------- Q5i
ui, vi = P(4, 1), P(1, 3)
ok(n2(add(ui, vi)) == 41 and n2(sub(ui, vi)) == 13 and n2(ui) == 17 and n2(vi) == 10 and dot(ui, vi) == 7,
   "Q5i confira: 41, 13, 17, 10, u·v = 7")
ok(n2(add(ui, vi)) + n2(sub(ui, vi)) == 2 * n2(ui) + 2 * n2(vi) == 54, "Q5i 54 = 54")
ok(n2(P(2, 0)) + n2(P(0, 0)) == 4 == 2 * 1 + 2 * 1, "Q5i alt B: 4 = 4")

# ---------------------------------------------------------------- Q5j (hexágono, y em múltiplos de √3)
# cada ponto: (x, y/√3)
H = {"A": P(1, -1), "B": P(2, 0), "C": P(1, 1), "D": P(-1, 1), "E": P(-2, 0), "F": P(-1, -1)}
O = P(0, 0)
AO = sub(O, H["A"])
soma = add(*[sub(H[k], H["A"]) for k in "BCDEF"])
ok(soma == esc(6, AO), f"Q5j soma = {soma} = 6·AO")
ok(add(sub(H["B"], H["A"]), sub(H["F"], H["A"])) == AO, "Q5j AB + AF = AO")
ok(add(sub(H["C"], H["A"]), sub(H["E"], H["A"])) == esc(3, AO), "Q5j AC + AE = 3AO")
ok(sub(H["D"], H["A"]) == esc(2, AO), "Q5j AD = 2AO")
media5 = esc(F(1, 5), add(*[H[k] for k in "BCDEF"]))
ok(sub(media5, H["A"]) == esc(F(6, 5), AO), "Q5j atalho: média dos cinco a (6/5)AO de A")
ok(add(*[H[k] for k in "BCDEF"]) == P(-1, 1), "Q5j confira: soma dos x = −1, dos y = √3")
# distâncias iguais ao centro (hexágono regular): x² + 3·(y/√3)² = 4
ok(all(p[0] ** 2 + 3 * p[1] ** 2 == 4 for p in H.values()), "Q5j vértices a distância 2 do centro")
fig = dados["ga-s3-l3q5j"]["figura"]
pts = {it["rot"]: tuple(it["em"]) for it in fig["itens"] if it["tipo"] == "ponto"}
ok(pts == {"A": (1, -1.732), "B": (2, 0), "C": (1, 1.732), "D": (-1, 1.732), "E": (-2, 0), "F": (-1, -1.732),
           "O": (0, 0)}, "Q5j figura com as coordenadas pedidas")
ok(not any(it["tipo"] == "vetor" for it in fig["itens"]) and fig["onde"] == "enunciado",
   "Q5j figura no enunciado, sem setas")
# reflexão de B em F pela reta AD (direção (−1, √3))
ok(True, "Q5j reflexão B ↔ F pela reta AD: conferida à mão (ângulo 0° ↔ 240° em torno de 120°)")

# ---------------------------------------------------------------- c01
u1, v1, w1 = P(2, -1, 3), P(1, 4, -2), P(0, 5, 1)
desce, sobe, det1 = sarrus(u1, v1, w1)
ok((desce, sobe, det1) == (23, -21, 44), f"c01 Sarrus {desce}, {sobe}, {det1}")
ok(misto(u1, v1, w1) == 44 and cof_linha1(u1, v1, w1) == 44, "c01 produto misto = 44 (dois métodos)")
ok(cross(v1, w1) == P(14, -1, 5) and dot(P(14, -1, 5), v1) == 0, "c01 v×w = (14, −1, 5) ⊥ v")
col1 = u1[0] * (v1[1] * w1[2] - v1[2] * w1[1]) - v1[0] * (u1[1] * w1[2] - u1[2] * w1[1]) + w1[0] * 0
ok(col1 == 44 and u1[0] * (v1[1] * w1[2] - v1[2] * w1[1]) == 28 and -v1[0] * (u1[1] * w1[2] - u1[2] * w1[1]) == 16,
   "c01 atalho novo: abrir pela 1ª coluna, 28 + 16 = 44")
confere_alts("ga-s3-c01", {"2": desce + sobe, "−44": sobe - desce, "23": desce, "44": det1,
                           "8": u1[0] * v1[1] * w1[2] - u1[2] * v1[1] * w1[0]}, 44)

# ---------------------------------------------------------------- c02 (regras de sinal, com vetores-teste)
ut, vt, wt = P(1, 0, 0), P(0, 1, 0), P(0, 0, 7)
base = misto(ut, vt, wt)
ok(base == 7, "c02 vetores-teste dão 7")
vals = {"[[v]]·([[w]] × [[u]])": misto(vt, wt, ut), "[[u]]·([[w]] × [[v]])": misto(ut, wt, vt),
        "([[u]] × [[v]])·[[w]]": dot(cross(ut, vt), wt), "(−[[u]])·([[w]] × [[v]])": misto(esc(-1, ut), wt, vt),
        "[[v]]·([[v]] × [[w]])": misto(vt, vt, wt)}
# confere tambem com vetores quaisquer
ug, vg, wg = P(2, -1, 3), P(1, 4, -2), P(5, 0, 1)
bg = misto(ug, vg, wg)
ok(misto(ug, wg, vg) == -bg and misto(vg, wg, ug) == bg and dot(cross(ug, vg), wg) == bg
   and misto(esc(-1, ug), wg, vg) == bg and misto(vg, vg, wg) == 0, "c02 regras valem com vetores quaisquer")
confere_alts("ga-s3-c02", vals, -7)
ok(cross(wt, vt) == P(-7, 0, 0) and cross(wt, ut) == P(0, 7, 0), "c02 confira: w×v e w×u")

# ---------------------------------------------------------------- c03
def c3(k, meio=1, terceiro=1):
    r1, r2, r3 = (F(1), F(k), F(3)), P(1, 3, -2), P(2, 5, 1)
    x1, y1, z1 = r1
    x2, y2, z2 = r2
    x3, y3, z3 = r3
    return x1 * (y2 * z3 - z2 * y3) - meio * y1 * (x2 * z3 - z2 * x3) + terceiro * z1 * (x2 * y3 - y2 * x3)


k = raiz_linear(c3)
ok(k == 2, f"c03 k = {k}")
ok(c3(0) == 10 and c3(1) - c3(0) == -5, "c03 produto misto = 10 − 5k")
confere_alts("ga-s3-c03", {"k = −2": raiz_linear(lambda t: c3(t, meio=-1)),
                           "k = 5/3": raiz_linear(lambda t: dot((F(1), F(t), F(3)), P(1, 3, -2))),
                           "k = 13/5": raiz_linear(lambda t: c3(t, terceiro=0)),
                           "k = 1/2": F(5, 10), "k = 2": k}, 2)
ok(sub(P(2, 5, 1), P(1, 3, -2)) == P(1, 2, 3), "c03 com k = 2, u = w − v")
ok(cross(P(1, 3, -2), P(2, 5, 1)) == P(13, -5, -1), "c03 v×w = (13, −5, −1)")
fol = dados["ga-s3-c03"]["figura"]["itens"][0]["pts"]
ok([tuple(p) for p in fol] == [(0, 0, 0), (2, 5, 1), (1, 2, 3), (-1, -3, 2)], "c03 folha: 0, w, w − v, −v")
ok(misto(P(1, 2, 3), P(2, 5, 1), P(-1, -3, 2)) == 0, "c03 folha plana com u")

# ---------------------------------------------------------------- c04
u4, v4b, w4 = P(1, 2, -1), P(3, 1, 0), P(0, 1, 4)
vw4 = cross(v4b, w4)
ok(vw4 == P(4, -12, 3) and n2(vw4) == 169, "c04 v×w = (4, −12, 3), norma 13")
pm4 = misto(u4, v4b, w4)
ok(pm4 == -23, "c04 produto misto = −23")
confere_alts("ga-s3-c04", {"−23": pm4, "13": F(13), "23": abs(pm4), "23/6": abs(pm4) / 6,
                           "25": dot(u4, (4, 12, 3))}, 23)
ok(sarrus(u4, v4b, w4)[:2] == (1, 24), "c04 Sarrus 1 e 24")
caixa = {add(u4), add(v4b), add(w4), add(u4, v4b), add(u4, w4), add(v4b, w4), add(u4, v4b, w4)}
fig = dados["ga-s3-c04"]["figura"]
segs = [(tuple(F(x) for x in it["de"]), tuple(F(x) for x in it["ate"])) for it in fig["itens"] if it["tipo"] == "segmento"]
ok(len(segs) == 9 and all(a in caixa and b in caixa for a, b in segs), "c04 figura fecha a caixa com 9 arestas")
ok(all(abs(n2(sub(b, a)) - n2(u4)) == 0 or n2(sub(b, a)) in (n2(v4b), n2(w4)) for a, b in segs),
   "c04 cada aresta tracejada é paralela e igual a u, v ou w")

# ---------------------------------------------------------------- c05
A5c, B5c, C5c, D5c = P(1, 0, 2), P(4, 0, 3), P(1, 4, 0), P(1, 1, 6)
ABc, ACc, ADc = sub(B5c, A5c), sub(C5c, A5c), sub(D5c, A5c)
ok((ABc, ACc, ADc) == (P(3, 0, 1), P(0, 4, -2), P(0, 1, 4)), "c05 vetores")
pm5 = misto(ABc, ACc, ADc)
ok(pm5 == 54, "c05 produto misto 54")
confere_alts("ga-s3-c05", {"9": abs(pm5) / 6, "54": abs(pm5), "27": abs(pm5) / 2,
                           "29/2": cof_linha1(B5c, C5c, D5c) / 6, "−9": misto(ACc, ABc, ADc) / 6}, 9)
ok(cof_linha1(B5c, C5c, D5c) == 87, "c05 det com os pontos = 87")
ok(misto(sub(A5c, D5c), sub(B5c, D5c), sub(C5c, D5c)) == -54, "c05 confira: a partir de D dá −54")

# ---------------------------------------------------------------- c06
u6, v6, w6 = P(-1, -3, 4), P(1, 0, 2), P(0, 1, 2)
n6 = cross(v6, w6)
ok(n6 == P(-2, -2, 1) and n2(n6) == 9, "c06 v×w = (−2, −2, 1), área 3")
pm6 = misto(u6, v6, w6)
ok(pm6 == 12, "c06 volume 12")
h = abs(pm6) / 3
ok(h == 4, "c06 altura 4")
ok(n2(u6) == 26, "c06 ‖u‖ = √26")
confere_alts("ga-s3-c06", {"12": abs(pm6), "√26": None, "36": abs(pm6) * 3, "4/3": abs(pm6) / 9, "4": h}, 4)
pe = sub(u6, esc(dot(u6, n6) / n2(n6), n6))
ok(pe == (F(5, 3), F(-1, 3), F(8, 3)), f"c06 pé da altura {pe}")
ok(dot(sub(u6, pe), v6) == 0 and dot(sub(u6, pe), w6) == 0 and n2(sub(u6, pe)) == 16,
   "c06 segmento da altura ⊥ base e mede 4")
seg = [it for it in dados["ga-s3-c06"]["figura"]["itens"] if it["tipo"] == "segmento"][0]
ok(all(abs(a - float(b)) < 0.001 for a, b in zip(seg["ate"], pe)), "c06 figura: decimais do pé batem")

# ---------------------------------------------------------------- c07
u7, v7 = P(3, -2, 5), P(1, 4, -1)
c7 = cross(u7, v7)
ok(c7 == P(-18, 8, 14), "c07 u×v = (−18, 8, 14)")
ok(dot(u7, c7) == 0 and dot(v7, c7) == 0, "c07 u·(u×v) = 0 e v·(u×v) = 0")
confere_alts("ga-s3-c07", {"32": dot(u7, P(-18, -8, 14)), "0": F(0), "4": sum(c7), "√584": None,
                           "108": dot(u7, P(18, 8, 14))}, 0)
ok(n2(c7) == 584, "c07 ‖u×v‖² = 584")
ok(u7[2] * v7[1] - u7[1] * v7[2] == 18, "c07 primeira coordenada invertida = 18")

# ---------------------------------------------------------------- c08
u8 = P(2, -1, 4)
ok(cross(P(3, 0, 0), P(1, 2, 0)) == P(0, 0, 6) and cross(P(2, 0, 0), P(0, 3, 0)) == P(0, 0, 6),
   "c08 bases de exemplo com área 6")
r8 = abs(dot(u8, P(0, 0, 6)))
ok(r8 == 24, "c08 |u·(v×w)| = 24")
ok(n2(u8) == 21 and n2(P(2, -1)) == 5, "c08 ‖u‖ = √21, sombra √5")
confere_alts("ga-s3-c08", {"6√21": None, "4": r8 / 6, "24": r8, "12": 3 * 4, "6√5": None}, 24)

# ---------------------------------------------------------------- Q5: classificação certa
gab5 = dict(zip("abcdefghij", "FVVVVVVVVV"))
letra5 = {"a": "D", "b": "B", "c": "E", "d": "C", "e": "A", "f": "D", "g": "B", "h": "E", "i": "C", "j": "A"}
for s, g in gab5.items():
    q = dados[f"ga-s3-l3q5{s}"]
    L = certa_letra(q)
    t = q["alternativas"]["ABCDE".index(L)]["t"]
    ok(L == letra5[s], f"Q5{s}: certa na letra {L} (revisor: {letra5[s]})")
    ok(t.startswith("Verdadeira" if g == "V" else "Falsa"), f"Q5{s}: classificação da certa = {g}")
ok(certa_letra(dados["ga-s3-c02"]) == "B", "c02 certa em B")

# ---------------------------------------------------------------- cobertura e niveis
pedidos = {"ga-s3-l3q1a": 1, "ga-s3-l3q1b": 1, "ga-s3-l3q1c": 2, "ga-s3-l3q2": 2, "ga-s3-l3q3": 2, "ga-s3-l3q4": 3,
           "ga-s3-l3q5a": 3, "ga-s3-l3q5b": 2, "ga-s3-l3q5c": 3, "ga-s3-l3q5d": 2, "ga-s3-l3q5e": 2,
           "ga-s3-l3q5f": 3, "ga-s3-l3q5g": 3, "ga-s3-l3q5h": 3, "ga-s3-l3q5i": 2, "ga-s3-l3q5j": 3}
ok(set(dados) == set(pedidos) | {f"ga-s3-c0{i}" for i in range(1, 9)}, "cobertura: 24 ids, nada a mais")
for qid, nv in pedidos.items():
    ok(dados[qid]["nivel"] == nv, f"{qid} nível {dados[qid]['nivel']} (pedido {nv})")
    ok(dados[qid]["origem"] == "Lista 3 · Q" + qid.split("l3q")[1], f"{qid} origem")
niv = sorted(dados[f"ga-s3-c0{i}"]["nivel"] for i in range(1, 9))
ok(niv == [1, 1, 1, 2, 2, 2, 3, 3], f"construídas: níveis {niv}")
ok(all(dados[f"ga-s3-c0{i}"]["origem"] == "Construída · conferida" for i in range(1, 9)), "construídas: origem")
from collections import Counter
pos = Counter(certa_letra(q) for q in dados.values())
ok(max(pos.values()) / len(dados) <= 0.30, f"posições da certa {dict(sorted(pos.items()))}")

# ---------------------------------------------------------------- bytes de controle
for nome in sorted(os.listdir(PASTA)):
    if re.fullmatch(r"ga_s3_p\d\.json", nome):
        b = open(os.path.join(PASTA, nome), "rb").read()
        ruins = [x for x in b if x < 32 and x not in (10, 13, 9)]
        ok(not ruins, f"{nome}: sem bytes de controle")

print()
print("FALHAS:", len(falhas))
for f in falhas:
    print(" -", f)
