# Conferencia das contas do lote ga_s3 (Semana 3, Lista 3 + construidas).
# Uso: python -I ga_s3_contas.py
import json, os, re, sys
from fractions import Fraction as F
from math import sqrt, isclose, degrees, acos

sys.stdout.reconfigure(encoding="utf-8")
falhas = []

def ok(cond, msg):
    print(("OK   " if cond else "FALHA") + " " + msg)
    if not cond:
        falhas.append(msg)

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def det(u, v, w):
    return dot(u, cross(v, w))

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def esc(k, a):
    return tuple(k*x for x in a)

def norma2(a):
    return dot(a, a)

def sarrus(u, v, w):
    a, b, c = u; d, e, f = v; g, h, i = w
    desce = [a*e*i, b*f*g, c*d*h]
    sobe = [c*e*g, a*f*h, b*d*i]
    return desce, sobe, sum(desce) - sum(sobe)

def det_meio_sem_menos(u, v, w):
    a, b, c = u
    return a*(v[1]*w[2] - v[2]*w[1]) + b*(v[0]*w[2] - v[2]*w[0]) + c*(v[0]*w[1] - v[1]*w[0])

def termo_a_termo(u, v, w):
    return sum(x*y*z for x, y, z in zip(u, v, w))

# ---------------- Q1 ----------------
u = (F(1), F(4), F(3)); v = (F(-1), F(1), F(-1)); w = (F(-2), F(-1, 2), F(5)); z = (F(-1), F(2), F(-3))
vw = cross(v, w)
ok(vw == (F(9, 2), F(7), F(5, 2)), f"q1a v x w = {vw}")
ok(det(u, v, w) == 40, "q1a u.(v x w) = 40")
ok(det(u, w, v) == -40, "q1a distrator -40 (ordem trocada)")
ok(dot(u, (vw[0], -vw[1], vw[2])) == -16, "q1a distrator -16 (sinal da 2a coordenada)")
w_mais = (F(-2), F(1, 2), F(5))
ok(cross(v, w_mais) == (F(11, 2), F(7), F(3, 2)) and det(u, v, w_mais) == 38, "q1a distrator 38 (+1/2)")
ok(termo_a_termo(u, v, w) == -15, "q1a distrator -15 (termo a termo)")
ds, ss, d = sarrus(u, v, w)
ok(sum(ds) == F(29, 2) and sum(ss) == F(-51, 2) and d == 40, f"q1a Sarrus desce {ds} sobe {ss}")
ok(dot(vw, v) == 0, "q1a v x w perpendicular a v")

vz = cross(v, z)
ok(vz == (-1, -2, -1), f"q1b v x z = {vz}")
ok(det(u, v, z) == -12, "q1b u.(v x z) = -12")
ok(det(u, z, v) == 12, "q1b distrator 12")
ok(dot(u, (-1, 2, -1)) == 4, "q1b distrator 4 (2a coordenada invertida)")
ok(v[2]*z[0] - v[0]*z[2] == -2 and v[0]*z[2] - v[2]*z[0] == 2, "q1b 2a coordenada certa -2, invertida 2")
ok(termo_a_termo(u, v, z) == 18, "q1b distrator 18 (termo a termo)")
ok(v[0]*z[1] - v[1]*z[0] == -1 and v[1]*z[0] - v[0]*z[1] == 1, "q1b 3a coordenada certa -1, invertida 1")
ok(dot(u, (-1, -2, 1)) == -6, "q1b distrator -6")
ds, ss, d = sarrus(u, v, z)
ok(sum(ds) == -5 and sum(ss) == 7 and d == -12, f"q1b Sarrus desce {ds} sobe {ss}")
ok(dot(vz, z) == 0, "q1b v x z perpendicular a z")

wz = cross(w, z)
ok(wz == (F(-17, 2), F(-11), F(-9, 2)), f"q1c w x z = {wz}")
ok(det(v, w, z) == 2, "q1c v.(w x z) = 2")
ok(det(v, z, w) == -2, "q1c distrator -2")
wz_b = (F(-3, 2) - 10, wz[1], wz[2])
ok(wz_b[0] == F(-23, 2) and dot(v, wz_b) == 5, "q1c distrator 5 ((-1/2)(-3) com sinal errado)")
wz_c = (wz[0], F(11), wz[2])
ok(w[0]*z[2] - w[2]*z[0] == 11 and dot(v, wz_c) == 24, "q1c distrator 24 (2a coordenada invertida)")
ok(termo_a_termo(v, w, z) == 12, "q1c distrator 12 (termo a termo)")
wz_3 = (wz[0], wz[1], F(-4) - F(-1, 2))
ok(dot(v, wz_3) == 1, "q1c texto do erro: sinal trocado no 2o produto com fracao leva a 1")
ok(det(v, w_mais, z) == 4, "q1c trabalho: -0,5 digitado como 0,5 da 4")
ok(sqrt(float(norma2(wz))) > 14.5 and sqrt(float(norma2(wz))) < 14.7, f"q1c norma de w x z = {sqrt(float(norma2(wz))):.3f}")
ok(dot(wz, w) == 0, "q1c w x z perpendicular a w")
ds, ss, d = sarrus(v, w, z)
ok(sum(ds) == F(-5, 2) and sum(ss) == F(-9, 2) and d == 2, f"q1c Sarrus desce {sum(ds)} sobe {sum(ss)}")
zv = cross(z, v)
ok(zv == (1, 2, 1) and dot(w, zv) == 2, "q1c atalho: z x v = (1, 2, 1) e w.(z x v) = 2")

# ---------------- Q2 ----------------
A = (-1, 2, -1); B = (5, 1, 1); C = (-2, -1, 1); D = (6, -1, -3)
AB, AC, AD = sub(B, A), sub(C, A), sub(D, A)
ok((AB, AC, AD) == ((6, -1, 2), (-1, -3, 2), (7, -3, -2)), "q2 vetores a partir de A")
ok(cross(AC, AD) == (12, 12, 24), "q2 AC x AD = (12, 12, 24)")
p = det(AB, AC, AD)
ok(p == 108 and F(abs(p), 6) == 18, "q2 produto misto 108, volume 18")
ok(F(108, 2) == 54 and F(108, 3) == 36 and det(AC, AB, AD) == -108, "q2 distratores 54, 36, -18")
BA, BC, BD = sub(A, B), sub(C, B), sub(D, B)
ok((BA, BC, BD) == ((-6, 1, -2), (-7, -2, 0), (1, -2, -4)) and det(BA, BC, BD) == -108, "q2 confira: a partir de B da -108")

# ---------------- Q3 ----------------
def q3_det(m):
    A3 = (F(1), m, F(-2)); B3 = (1, -2, 3); C3 = (-1, 1, -1); D3 = (5, -1, 2)
    return det(sub(A3, B3), sub(C3, B3), sub(D3, B3))
ok(q3_det(F(0)) == 34 and q3_det(F(1)) - q3_det(F(0)) == -18, "q3 produto misto = 34 - 18m")
ok(q3_det(F(17, 9)) == 0, "q3 m = 17/9 zera")
ok(q3_det(F(-17, 9)) != 0 and q3_det(F(9, 17)) != 0 and q3_det(F(1, 2)) != 0 and q3_det(F(-53, 9)) != 0, "q3 distratores nao zeram")
# erro do sinal do meio: 18(m+2) + 70 = 0
ok(F(-106, 18) == F(-53, 9), "q3 distrator -53/9")
# usar A, B, C como vetores: det = 1 - 2m
def detABC(m):
    return det((F(1), m, F(-2)), (1, -2, 3), (-1, 1, -1))
ok(detABC(F(0)) == 1 and detABC(F(1)) == -1 and detABC(F(1, 2)) == 0, "q3 distrator 1/2 (det de A, B, C = 1 - 2m)")
ok(F(17, 9) + 2 == F(35, 9) and F(35, 9) * 18 == 70, "q3 confira 35/9 e 70")
# A com m = 17/9 em A, B, C, D: tambem via A como origem
def q3_det_A(m):
    A3 = (F(1), m, F(-2))
    return det(sub((1, -2, 3), A3), sub((-1, 1, -1), A3), sub((5, -1, 2), A3))
ok(q3_det_A(F(17, 9)) == 0, "q3 tambem zera partindo de A")

# ---------------- Q4 ----------------
a4, b4 = (2, 1, 0), (-1, 1, -1)
n4 = cross(a4, b4)
ok(n4 == (-1, 2, 3) and norma2(n4) == 14, "q4 produto vetorial (-1, 2, 3), norma raiz 14")
ok(dot(n4, (-1, 0, 2)) == 7 and dot(esc(-1, n4), (-1, 0, 2)) == -7, "q4 angulo: 7 e -7")
P = (2, 3, 4)
ok(add(P, n4) == (1, 5, 7), "q4 ponto final (1, 5, 7)")
ok(add(P, esc(-1, n4)) == (3, 1, 1), "q4 distrator (3, 1, 1)")
ok(a4[2]*b4[1] - a4[1]*b4[2] == 1 and add(P, (1, 2, 3)) == (3, 5, 7) and dot((1, 2, 3), a4) == 4 and norma2((1, 2, 3)) == 14, "q4 distrator (3, 5, 7)")
ok(a4[0]*b4[2] - a4[2]*b4[0] == -2 and add(P, (-1, -2, 3)) == (1, 1, 7) and dot((-1, -2, 3), a4) == -4, "q4 distrator (1, 1, 7)")
ok(dot(sub((3, 1, 1), P), a4) == 0 and dot(sub((-1, 2, 3), P), a4) == -7, "q4 atalho: (3,1,1) passa no teste, (-1,2,3) nao")

# ---------------- Q5a e Q5b ----------------
A5, X5, B5, C5 = (F(0), F(0)), (F(2), F(0)), (F(3), F(0)), (F(3, 2), F(5, 2))
ok(sub(X5, A5) == esc(2, sub(B5, X5)), "q5ab figura: AX = 2 XB")
CA, CB, CX = sub(A5, C5), sub(B5, C5), sub(X5, C5)
ok(CA == (F(-3, 2), F(-5, 2)) and CB == (F(3, 2), F(-5, 2)) and CX == (F(1, 2), F(-5, 2)), "q5ab vetores CA, CB, CX")
certo = add(esc(F(1, 3), CA), esc(F(2, 3), CB))
errado = add(esc(F(2, 3), CA), esc(F(1, 3), CB))
ok(certo == CX, "q5b (1/3)CA + (2/3)CB = CX")
ok(errado == (F(-1, 2), F(-5, 2)) and errado != CX and add(C5, errado) == (1, 0), "q5a contraexemplo (2/3)CA + (1/3)CB leva a (1, 0)")
ok(add(esc(F(2, 3), CA), esc(F(-1, 3), CB)) != CX, "q5a distrator com sinal de menos nao da CX")

# ---------------- Q5c ----------------
Aq, Bq, Cq, Dq = (F(0), F(0)), (F(6), F(-1)), (F(7), F(4)), (F(1), F(5))
mid = lambda p, q: esc(F(1, 2), add(p, q))
M, N, Pm, Q = mid(Aq, Bq), mid(Bq, Cq), mid(Cq, Dq), mid(Dq, Aq)
ok((M, N, Pm, Q) == ((3, F(-1, 2)), (F(13, 2), F(3, 2)), (4, F(9, 2)), (F(1, 2), F(5, 2))), "q5c pontos medios")
ok(sub(N, M) == sub(Pm, Q) == esc(F(1, 2), sub(Cq, Aq)) == (F(7, 2), 2), "q5c MN = QP = AC/2 = (7/2, 2)")
ok(norma2(sub(N, M)) != norma2(sub(Pm, N)), "q5c lados vizinhos com tamanhos diferentes (nao e losango)")

# ---------------- Q5d ----------------
ok(dot((1, 1), (1, -1)) == 0, "q5d distrator A: (1,1).(1,-1) = 0")
ok(norma2((3, 4)) == norma2((5, 0)) == 25 and dot((3, 4), (5, 0)) == 15 and dot((8, 4), (-2, 4)) == 0, "q5d (3,4) e (5,0)")
ok(norma2((8, 4)) != norma2((-2, 4)), "q5d soma e diferenca com tamanhos diferentes")
uu, vv = (3, 1), (1, 3)
ok(norma2(uu) == norma2(vv) == 10 and dot(add(uu, vv), sub(uu, vv)) == 0, "q5d figura (3,1) e (1,3)")
ok(dot(add(uu, (1, 2)), sub(uu, (1, 2))) == 5 == norma2(uu) - norma2((1, 2)), "q5d confira com v = (1, 2) da 5")
ok(102 * 98 == 10000 - 4, "q5d 102 x 98")

# ---------------- Q5e ----------------
V = (2, 3, 6)
ok(norma2(V) == 49, "q5e norma de (2,3,6) = 7")
ok(sum(F(c * c, 49) for c in V) == 1, "q5e soma dos cos^2 = 1")
ok(isclose((1 / sqrt(3)) * 3, sqrt(3)), "q5e (1,1,1): soma dos cossenos = raiz 3")
ok(isclose(degrees(acos(1 / sqrt(3))), 54.7356, abs_tol=1e-3), "q5e angulo de (1,1,1) com os eixos")

# ---------------- Q5f ----------------
At, Bt, Ct, Dt = (F(0), F(0)), (F(8), F(0)), (F(6), F(3)), (F(1), F(3))
Mt, Nt = mid(At, Dt), mid(Bt, Ct)
ok(Mt == (F(1, 2), F(3, 2)) and Nt == (7, F(3, 2)), "q5f M e N")
MN = sub(Nt, Mt)
ok(MN == (F(13, 2), 0) and MN == esc(F(1, 2), add(sub(Bt, At), sub(Ct, Dt))), "q5f MN = (13/2, 0) = (AB + DC)/2")
ok(F(8 + 5, 2) == F(13, 2), "q5f media das bases 6,5")
ok(norma2(sub(Dt, At)) != norma2(sub(Ct, Bt)), "q5f trapezio nao isosceles")
ok(abs(esc(F(1, 2), add(sub(Bt, At), sub(Dt, Ct)))[0]) == F(3, 2), "q5f (AB + CD)/2 mede metade da diferenca")

# ---------------- Q5g e Q5h ----------------
Ag, Bg, Cg, Dg = (F(0), F(0)), (F(6), F(0)), (F(7), F(4)), (F(1), F(5))
E, Fp = mid(Ag, Bg), mid(Cg, Dg)
EF = sub(Fp, E)
ok(E == (3, 0) and Fp == (4, F(9, 2)) and EF == (1, F(9, 2)), "q5g E, F e EF")
ok(esc(F(1, 2), add(sub(Dg, Ag), sub(Cg, Bg))) == EF, "q5g EF = (AD + BC)/2")
ok(esc(F(1, 2), add(sub(Cg, Ag), sub(Dg, Bg))) == EF, "q5h EF = (AC + BD)/2")
ok(esc(F(1, 2), sub(sub(Cg, Ag), sub(Dg, Bg))) == (6, F(-1, 2)), "q5h distrator (AC - BD)/2 = (6, -1/2)")
ok(sub(Bg, Ag) != sub(Cg, Dg), "q5h quadrilatero nao e paralelogramo")
ok(sub(Dg, Ag) != esc(F(1), sub(Cg, Bg)) and cross((1, 5, 0), (1, 4, 0))[2] != 0, "q5g AD e BC nao paralelos")
Aqd, Bqd, Cqd, Dqd = (0, 0), (2, 0), (2, 2), (0, 2)
Eq, Fq = mid(Aqd, Bqd), mid(Cqd, Dqd)
EFq = sub(Fq, Eq)
ok(EFq == (0, 2), "q5g quadrado: EF = (0, 2)")
ok(esc(F(1, 2), add(sub(Dqd, Aqd), sub(Cqd, Bqd))) == (0, 2), "q5g quadrado: (AD + BC)/2 = (0, 2)")
ok(esc(F(1, 2), sub(sub(Dqd, Aqd), sub(Cqd, Bqd))) == (0, 0), "q5g quadrado: (AD - BC)/2 = (0, 0)")
ok(add(sub(Dqd, Aqd), sub(Cqd, Bqd)) == (0, 4), "q5g quadrado: AD + BC = (0, 4)")
ok(esc(F(1, 2), add(sub(Bqd, Aqd), sub(Dqd, Cqd))) == (0, 0), "q5g quadrado: (AB + CD)/2 = (0, 0)")

# ---------------- Q5i ----------------
ui, vi = (4, 1), (1, 3)
ok(norma2(add(ui, vi)) == 41 and norma2(sub(ui, vi)) == 13 and 2*norma2(ui) + 2*norma2(vi) == 54 and dot(ui, vi) == 7, "q5i figura 41 + 13 = 54")
ok(norma2((2, 0)) + norma2((0, 0)) == 4 == 2*1 + 2*1, "q5i distrator (1,0),(1,0): 4 = 4")
ok(norma2(add(ui, vi)) - norma2(sub(ui, vi)) == 4*dot(ui, vi), "q5i diferenca das normas = 4u.v")

# ---------------- Q5j ----------------
s3 = sqrt(3)
H = {"A": (1, -s3), "B": (2, 0), "C": (1, s3), "D": (-1, s3), "E": (-2, 0), "F": (-1, -s3)}
AO = (-1, s3)
def proxv(a, b):
    return all(isclose(x, y, abs_tol=1e-9) for x, y in zip(a, b))
for X in "BCDEF":
    ok(isclose(sqrt(norma2(H[X])), 2) , f"q5j vertice {X} a distancia 2 do centro")
soma = (0.0, 0.0)
for X in "BCDEF":
    soma = add(soma, sub(H[X], H["A"]))
ok(proxv(soma, esc(6, AO)), "q5j soma dos cinco AX = 6 AO")
ok(proxv(add(sub(H["B"], H["A"]), sub(H["F"], H["A"])), AO), "q5j AB + AF = AO")
ok(proxv(add(sub(H["C"], H["A"]), sub(H["E"], H["A"])), esc(3, AO)), "q5j AC + AE = 3 AO")
ok(proxv(sub(H["D"], H["A"]), esc(2, AO)), "q5j AD = 2 AO")
ok(proxv(sub(H["B"], H["A"]), (1, s3)) and proxv(sub(H["F"], H["A"]), (-2, 0)), "q5j AB = (1, raiz3), AF = (-2, 0)")
mx = sum(H[X][0] for X in "BCDEF"); my = sum(H[X][1] for X in "BCDEF")
ok(isclose(mx, -1) and isclose(my, s3), "q5j confira: somas de x e y dos cinco vertices")
media5 = esc(1/5, (mx, my))
ok(proxv(sub(media5, H["A"]), esc(6/5, AO)), "q5j atalho: media dos cinco fica a (6/5)AO de A")
# lados iguais na figura com 1.732
Hf = [(1, -1.732), (2, 0), (1, 1.732), (-1, 1.732), (-2, 0), (-1, -1.732)]
lados = [sqrt(norma2(sub(Hf[i], Hf[(i+1) % 6]))) for i in range(6)]
ok(max(lados) - min(lados) < 1e-3, f"q5j figura: lados {[round(x, 4) for x in lados]}")

# ---------------- c01 ----------------
u1, v1, w1 = (2, -1, 3), (1, 4, -2), (0, 5, 1)
ds, ss, d = sarrus(u1, v1, w1)
ok(ds == [8, 0, 15] and ss == [0, -20, -1] and d == 44, f"c01 Sarrus desce {ds} sobe {ss} det {d}")
ok(det(u1, v1, w1) == 44, "c01 produto misto 44")
ok(sum(ds) + sum(ss) == 2 and sum(ss) - sum(ds) == -44 and sum(ds) == 23, "c01 distratores 2, -44, 23")
ok(2*4*1 - 3*4*0 == 8, "c01 distrator 8 (regra do 2x2)")
ok(cross(v1, w1) == (14, -1, 5) and dot(cross(v1, w1), v1) == 0, "c01 v x w = (14, -1, 5) perpendicular a v")
ok(2*(4*1 - (-2)*5) - (-1)*(1*1 - (-2)*0) + 3*(1*5 - 4*0) == 44, "c01 cofatores 28 + 1 + 15")

# ---------------- c02 ----------------
uc, vc, wc = (1, 0, 0), (0, 1, 0), (0, 0, 7)
ok(det(uc, vc, wc) == 7, "c02 exemplo u.(v x w) = 7")
ok(det(vc, wc, uc) == 7, "c02 A v.(w x u) = 7")
ok(det(uc, wc, vc) == -7, "c02 B u.(w x v) = -7 (certa)")
ok(dot(cross(uc, vc), wc) == 7, "c02 C (u x v).w = 7")
ok(det(esc(-1, uc), wc, vc) == 7, "c02 D (-u).(w x v) = 7")
ok(det(vc, vc, wc) == 0, "c02 E v.(v x w) = 0")
ok(cross(wc, vc) == (-7, 0, 0) and cross(wc, uc) == (0, 7, 0), "c02 confira w x v e w x u")
# vetores genericos
import random
random.seed(3)
for _ in range(5):
    a = tuple(random.randint(-5, 5) for _ in range(3)); b = tuple(random.randint(-5, 5) for _ in range(3)); c = tuple(random.randint(-5, 5) for _ in range(3))
    t = det(a, b, c)
    assert det(b, c, a) == t and det(c, a, b) == t and det(a, c, b) == -t and dot(cross(a, b), c) == t and det(esc(-1, a), c, b) == t
ok(True, "c02 propriedades conferidas em 5 trios aleatorios")

# ---------------- c03 ----------------
v3, w3 = (1, 3, -2), (2, 5, 1)
def c03(k):
    return det((F(1), k, F(3)), v3, w3)
ok(c03(F(0)) == 10 and c03(F(1)) - c03(F(0)) == -5 and c03(F(2)) == 0, "c03 det = 10 - 5k, k = 2")
ok(1*(3*1 - (-2)*5) == 13 and (1*1 - (-2)*2) == 5 and 3*(1*5 - 3*2) == -3, "c03 termos 13, 5, -3")
ok(F(-10, 5) == -2 and 13 + 5*(-2) - 3 == 0, "c03 distrator -2 (sem o menos do meio)")
ok(dot((1, F(5, 3), 3), v3) == 0, "c03 distrator 5/3 (u.v = 0)")
ok(13 - 5*F(13, 5) == 0, "c03 distrator 13/5 (sem o 3o termo)")
ok(c03(F(1, 2)) != 0 and c03(F(-2)) != 0 and c03(F(5, 3)) != 0 and c03(F(13, 5)) != 0, "c03 distratores nao zeram")
ok(sub(w3, v3) == (1, 2, 3) and cross(v3, w3) == (13, -5, -1), "c03 u = w - v e v x w = (13, -5, -1)")
ok(add(esc(-1, v3), w3) == (1, 2, 3), "c03 figura: u na folha (poligono 0, w, w - v, -v)")

# ---------------- c04 ----------------
u4, v4, w4 = (1, 2, -1), (3, 1, 0), (0, 1, 4)
ok(cross(v4, w4) == (4, -12, 3) and norma2(cross(v4, w4)) == 169, "c04 v x w = (4, -12, 3), area 13")
ok(det(u4, v4, w4) == -23, "c04 produto misto -23, volume 23")
ok(dot(u4, (4, 12, 3)) == 25, "c04 distrator 25")
ds, ss, d = sarrus(u4, v4, w4)
ok(sum(ds) == 1 and sum(ss) == 24 and d == -23, f"c04 Sarrus desce {ds} sobe {ss}")
ok(det(v4, w4, u4) == -23, "c04 ciclica tambem -23")
vert = {"u+v": add(u4, v4), "u+w": add(u4, w4), "v+w": add(v4, w4), "u+v+w": add(add(u4, v4), w4)}
ok(vert == {"u+v": (4, 3, -1), "u+w": (1, 3, 3), "v+w": (3, 2, 4), "u+v+w": (4, 4, 3)}, f"c04 vertices da figura {vert}")

# ---------------- c05 ----------------
A6, B6, C6, D6 = (1, 0, 2), (4, 0, 3), (1, 4, 0), (1, 1, 6)
AB6, AC6, AD6 = sub(B6, A6), sub(C6, A6), sub(D6, A6)
ok((AB6, AC6, AD6) == ((3, 0, 1), (0, 4, -2), (0, 1, 4)), "c05 vetores a partir de A")
ok(det(AB6, AC6, AD6) == 54 and F(54, 6) == 9, "c05 produto misto 54, volume 9")
ok(det(AC6, AB6, AD6) == -54, "c05 distrator -9 (ordem AC, AB, AD)")
ok(det(B6, C6, D6) == 87 and F(87, 6) == F(29, 2), "c05 distrator 29/2 (pontos como vetores)")
DA6, DB6, DC6 = sub(A6, D6), sub(B6, D6), sub(C6, D6)
ok((DA6, DB6, DC6) == ((0, -1, -4), (3, -1, -3), (0, 3, -6)) and det(DA6, DB6, DC6) == -54, "c05 confira a partir de D: -54")

# ---------------- c06 ----------------
u7, v7, w7 = (-1, -3, 4), (1, 0, 2), (0, 1, 2)
n7 = cross(v7, w7)
ok(n7 == (-2, -2, 1) and norma2(n7) == 9, "c06 v x w = (-2, -2, 1), area 3")
ok(det(u7, v7, w7) == 12 and F(12, 3) == 4, "c06 volume 12, altura 4")
ok(norma2(u7) == 26, "c06 comprimento de u = raiz 26")
ok(F(12, 9) == F(4, 3) and 12 * 3 == 36, "c06 distratores 4/3 e 36")
pe = sub(u7, esc(F(12, 9), n7))
ok(pe == (F(5, 3), F(-1, 3), F(8, 3)) and dot(pe, n7) == 0, f"c06 pe da altura {pe} no plano da base")
ok(isclose(sqrt(float(norma2(sub(u7, pe)))), 4), "c06 distancia da ponta de u ao pe = 4")
ok(add(v7, w7) == (1, 1, 4), "c06 figura: vertice v + w")

# ---------------- c07 ----------------
u8, v8 = (3, -2, 5), (1, 4, -1)
uv8 = cross(u8, v8)
ok(uv8 == (-18, 8, 14), "c07 u x v = (-18, 8, 14)")
ok(dot(u8, uv8) == 0 and dot(v8, uv8) == 0, "c07 u.(u x v) = 0 e v.(u x v) = 0")
ok(dot(u8, (-18, -8, 14)) == 32, "c07 distrator 32")
ok(5*4 - (-2)*(-1) == 18 and dot(u8, (18, 8, 14)) == 108, "c07 distrator 108")
ok(sum(uv8) == 4 and norma2(uv8) == 584, "c07 distratores 4 e raiz 584")

# ---------------- c08 ----------------
u9 = (2, -1, 4)
for vb, wb in [((3, 0, 0), (1, 2, 0)), ((2, 0, 0), (0, 3, 0))]:
    ok(cross(vb, wb) == (0, 0, 6) and abs(det(u9, vb, wb)) == 24, f"c08 base {vb}, {wb}: |produto misto| = 24")
ok(norma2(u9) == 21 and norma2((2, -1)) == 5, "c08 distratores raiz 21 e raiz 5")
ok(F(24, 6) == 4 and 3 * 4 == 12, "c08 distratores 4 e 12")
ok(add((3, 0, 0), (1, 2, 0)) == (4, 2, 0), "c08 figura: vertice v + w = (4, 2, 0)")

# ---------------- Texto: tamanhos, posicoes, hifen ----------------
pasta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")
arqs = [os.path.join(pasta, f"ga_s3_p{i}.json") for i in range(1, 5)]
pos = {}
total = 0
for arq in arqs:
    with open(arq, encoding="utf-8") as fh:
        bruto = fh.read()
    ctrl = [c for c in bruto if ord(c) < 32 and c not in "\n\r\t"]
    ok(not ctrl, f"{os.path.basename(arq)} sem bytes de controle")
    d = json.loads(bruto)
    for s in d["semanas"]:
        for b in s["blocos"]:
            n = len(b["texto"].split())
            ok(40 <= n <= 120, f"semana bloco '{b['titulo']}' com {n} palavras")
        for k, t in s["jeitos"].items():
            n = len(t.split())
            ok(50 <= n <= 120, f"semana jeito {k} com {n} palavras")
    for q in d["questoes"]:
        total += 1
        for i, a in enumerate(q["alternativas"]):
            if a.get("certa"):
                pos["ABCDE"[i]] = pos.get("ABCDE"[i], 0) + 1
            if re.search(r"(^|[\s(,\[=])-\d", re.sub(r"`[^`]*`", " ", a["t"])):
                falhas.append(f"{q['id']} alternativa {i} com hifen como menos")
        for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
            n = len(q["jeitos"][k].split())
            if not (35 <= n <= 110):
                print(f"AVISO {q['id']}.{k}: {n} palavras (alvo 35 a 110)")
        rec = q["jeitos"]["receita"]
        if not (3 <= len(rec) <= 7):
            falhas.append(f"{q['id']} receita com {len(rec)} passos")
ok(total == 24, f"total de questoes {total}")
ok(all(c <= 7 for c in pos.values()), f"posicoes das certas {dict(sorted(pos.items()))}")

print()
print("FALHAS:" if falhas else "TUDO CONFERE", len(falhas))
for f_ in falhas:
    print("  -", f_)
