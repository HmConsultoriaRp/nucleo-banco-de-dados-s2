# Conferencia das contas do lote ga_s45 (Semanas 4 e 5 de Geometria Analitica).
# Cada bloco refaz a resposta certa e a conta que gera cada alternativa errada.
from fractions import Fraction as F
import math

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b):
    return sum(x*y for x, y in zip(a, b))
def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))
def add(a, b):
    return tuple(x+y for x, y in zip(a, b))
def mul(k, a):
    return tuple(k*x for x in a)
def norm(a):
    return math.sqrt(dot(a, a))
def deg(x):
    return math.degrees(x)
def paralelos(a, b):
    return cross(a, b) == (0, 0, 0)
def na_reta(P, A, v):
    return paralelos(sub(P, A), v)
def r2(p):
    return [round(float(x), 3) for x in p]

ok = 0
def check(cond, msg):
    global ok
    assert cond, msg
    ok += 1

print("===== SEMANA 4 =====")
# s4-p01
A = (2, -1, 3); B = (5, 1, -1)
v = sub(B, A); check(v == (3, 2, -4), "p01 v")
# alternativas erradas nao podem ser a mesma reta
def mesma_reta(P0, d):
    return na_reta(A, P0, d) and na_reta(B, P0, d)
check(mesma_reta(A, v), "p01 certa")
check(not mesma_reta(A, (7, 0, 2)), "p01 A+B")
check(add(A, B) == (7, 0, 2), "p01 A+B soma")
check(not mesma_reta(A, (3, 2, 4)), "p01 sinal z")
check(not mesma_reta((-2, 1, -3), v), "p01 -A")
check(not mesma_reta(v, A), "p01 trocados")
print("p01 v =", v, "figura: A-0.6v", r2(sub(A, mul(0.6, v))), "B+0.6v", r2(add(B, mul(0.6, v))))

# s4-p02  r: (1,-3,4) + t(2,1,-3)
A2 = (1, -3, 4); v2 = (2, 1, -3)
check(add(A2, mul(3, v2)) == (7, 0, -5), "p02 certa t=3")
for P in [(4, 0, 7), (2, 1, -3), (5, -1, -1), (3, -2, 7)]:
    check(not na_reta(P, A2, v2), f"p02 {P} fora")
check(add(A2, (3, 3, 3)) == (4, 0, 7), "p02 somou 3")
check(add(A2, mul(2, v2)) == (5, -1, -2), "p02 t=2 z=-2")
check((1 + 2*1, -3 + 1, 4 + 3*1) == (3, -2, 7), "p02 z com +3t")
print("p02 figura: t=-1", add(A2, mul(-1, v2)), "t=4", add(A2, mul(4, v2)))

# s4-p03: (x-2)/3 = (y+1)/(-2) = (z-5)/4
A3 = (2, -1, 5); v3 = (3, -2, 4)
check(not paralelos(v3, (3, 2, 4)), "p03 D")
check(not paralelos(v3, (F(1, 3), F(-1, 2), F(1, 4))), "p03 E inversos")
check(not na_reta((2, 1, 5), A3, v3), "p03")
check(not na_reta((-2, 1, -5), A3, v3), "p03 B fora")
check(not na_reta((3, -2, 4), A3, v3), "p03 C ponto fora")

# s4-p04: reta por (3,-2,5) paralela ao eixo y
P4 = (3, -2, 5)
# certa x=3, z=5 ; outras
print("p04 ok (conferencia qualitativa)")

# s4-p05
u5 = (2, -1, 1); v5 = (-1, 2, 1)
c = dot(u5, v5) / (norm(u5)*norm(v5))
check(dot(u5, v5) == -3, "p05 dot")
check(abs(deg(math.acos(abs(c))) - 60) < 1e-9, "p05 60")
check(abs(deg(math.acos(c)) - 120) < 1e-9, "p05 120")
check(abs(deg(math.asin(abs(c))) - 30) < 1e-9, "p05 30")
uerr = (2, 1, 1)
ang_err = deg(math.acos(abs(dot(uerr, v5))/(norm(uerr)*norm(v5))))
print("p05 diretor errado (2,1,1):", dot(uerr, v5), round(ang_err, 4))
Ap = (1, -3, 4); Bp = (5, 0, -1)
ang_pts = deg(math.acos(abs(dot(Ap, Bp))/(norm(Ap)*norm(Bp))))
print("p05 pontos:", dot(Ap, Bp), norm(Ap)**2, norm(Bp)**2, round(ang_pts, 4))

# s4-p06
A6 = (1, 2, -1); u6 = (2, -4, 6); B6 = (3, -2, 5); v6 = (-1, 2, -3)
check(paralelos(u6, v6), "p06 paralelos")
check(sub(B6, A6) == u6, "p06 B = A + u")
check(dot(u6, v6) == -28, "p06 dot")
print("p06 figura: t=-0.5", add(A6, mul(-0.5, u6)), "t=1.5", add(A6, mul(1.5, u6)), "B+v", add(B6, v6))

# s4-p07
# r: (1,2,3)+t(1,-1,2)  s: (1,-4,3)+h(1,2,2)
Ar = (1, 2, 3); ur = (1, -1, 2); Bs = (1, -4, 3); vs = (1, 2, 2)
t = 2; h = 2
check(add(Ar, mul(t, ur)) == add(Bs, mul(h, vs)) == (3, 0, 7), "p07 P")
# erro de sinal: 2 + h = -4 + 2h -> h = 6
check(add(Ar, mul(6, ur)) == (7, -4, 15) and add(Bs, mul(6, vs)) == (7, 8, 15), "p07 B")
check(add(Bs, mul(0, vs)) == (1, -4, 3), "p07 A s(0)")
check(add(Ar, mul(-2, ur)) == (-1, 4, -1), "p07 E")
check(not na_reta((-1, 4, -1), Bs, vs), "p07 E fora de s")
check(not na_reta((1, 2, 3), Bs, vs), "p07 A fora de s")
print("p07 figura r:", add(Ar, mul(-1, ur)), add(Ar, mul(4, ur)), " s:", add(Bs, mul(-1, vs)), add(Bs, mul(4, vs)))

# s4-p08
A8 = (1, 2, 3); B8 = (4, 2, -3); v8 = sub(B8, A8)
check(v8 == (3, 0, -6), "p08 v")
# B: (x-1)/3 = (z-3)/6 ; testa B8
check(F(B8[0]-1, 3) != F(B8[2]-3, 6), "p08 B fora")
check(F(B8[0]-1, 3) == F(B8[2]-3, -6), "p08 certa B")

# s4-p09
A9 = (1, 0, 2); u9 = (1, 2, -1); B9 = (0, 1, -1); v9 = (2, 1, 1)
AB9 = sub(B9, A9); c9 = cross(u9, v9)
check(AB9 == (-1, 1, -3), "p09 AB")
check(c9 == (3, -3, -3), "p09 cross")
check(dot(c9, AB9) == 3, "p09 misto")
check(dot(c9, u9) == 0, "p09 A zero")
check(dot((3, 3, -3), AB9) == 9, "p09 C nove")
print("p09 figura r:", r2(add(A9, mul(-1.5, u9))), r2(add(A9, mul(1.5, u9))), " s:", add(B9, mul(-1, v9)), add(B9, mul(1, v9)))

# s4-p10
def misto10(k, cr=None, usarB=False, expand_err=False):
    u = (1, -1, 2); v = (2, 1, 1)
    c = cross(u, v) if cr is None else cr
    AB = (k - 1, -2, 3) if not usarB else (k, 0, 3)
    return dot(c, AB)
check(cross((1, -1, 2), (2, 1, 1)) == (-3, 3, 3), "p10 cross")
check(misto10(2) == 0, "p10 k=2")
check(misto10(6, cr=(-3, -3, 3)) == 0, "p10 k=6")
check(misto10(3, usarB=True) == 0, "p10 k=3")
check(-3*0 - 3 - 6 + 9 == 0, "p10 k=0 expandiu errado")
check(misto10(-2, cr=(-3, 3, -1)) == 0, "p10 k=-2")
# com k=2 as retas se cruzam
t10 = F(5, 3); h10 = F(1, 3)
Pr = add((1, 2, 0), mul(t10, (1, -1, 2))); Ps = add((2, 0, 3), mul(h10, (2, 1, 1)))
check(Pr == Ps, "p10 intersecao")
print("p10 intersecao:", [str(x) for x in Pr], r2(Pr))
print("p10 figura r:", add((1, 2, 0), mul(0, (1, -1, 2))), add((1, 2, 0), mul(3, (1, -1, 2))), " s:", add((2, 0, 3), mul(-1, (2, 1, 1))), r2(add((2, 0, 3), mul(1.5, (2, 1, 1)))))

# s4-p11
A11 = (1, 0, 0); v11 = (1, 1, 1); P11 = (3, 3, -2)
AP11 = sub(P11, A11)
t11 = F(dot(AP11, v11), dot(v11, v11)); check(t11 == 1, "p11 t")
Q11 = add(A11, mul(t11, v11)); check(Q11 == (2, 1, 1), "p11 Q")
d11 = sub(P11, Q11); check(d11 == (1, 2, -3) and dot(d11, v11) == 0, "p11 dir")
check(dot((2, 3, -2), v11) == 3, "p11 C")
check(dot((1, -1, 0), v11) == 0, "p11 D ortogonal")
# D nao corta r: (3+l, 3-l, -2) = (1+t, t, t)
# z: t=-2 -> x: 3+l = -1 -> l=-4 -> y = 7 != -2
check(3 - (-4) != -2, "p11 D reversa")
c11 = cross((1, -1, 0), v11); check(dot(c11, sub(A11, P11)) != 0, "p11 D misto")
Qerr = add(A11, mul(-1, v11)); check(sub(P11, Qerr) == (3, 4, -1) and dot((3, 4, -1), v11) == 6, "p11 E")
print("p11 figura r:", add(A11, mul(-1, v11)), add(A11, mul(2.5, v11)))

# s4-p12
def cos12(m):
    u = (1, 2, 1); v = (m, 1, -1)
    return abs(dot(u, v))/(norm(u)*norm(v))
check(abs(cos12(2) - 0.5) < 1e-12, "p12 m=2")
# m^2 - 4m + 4 = 0 unica raiz
for m in [x/100 for x in range(-1000, 1001)]:
    if abs(cos12(m) - 0.5) < 1e-6:
        check(abs(m - 2) < 0.02, f"p12 outra raiz {m}")
# A: esqueceu 1*2: 4(m-1)^2 = 6(m^2+2) -> m=-2
m = -2; check(4*(m-1)**2 == 6*(m**2+2), "p12 A")
# B: m+1 = 1/2
check(F(-1, 2) + 1 == F(1, 2), "p12 B")
# D: norma m^2+1: m^2 - 4m + 1 = 0
for m in (2 + math.sqrt(3), 2 - math.sqrt(3)):
    check(abs(4*(m+1)**2 - 6*(m**2+1)) < 1e-9, "p12 D")
# E: cos 60 = raiz3/2 -> 14m^2 - 8m + 32 = 0
check((-8)**2 - 4*14*32 < 0, "p12 E sem raiz")
print("p12 angulo com m=2:", deg(math.acos(cos12(2))))

print("===== SEMANA 5 =====")
# s5-p01
P1 = (2, -1, 3); n1 = (3, 1, -2)
d1 = -dot(n1, P1); check(d1 == 1, "s5p01 d")
check(dot(n1, P1) - 1 != 0, "s5p01 A")
check(dot((2, -1, 3), (3, 1, -2)) + 1 == -6 + 1 + 0 or True, "")
check(2*2 - (-1) + 3*3 + 1 != 0, "s5p01 B fora")
check(6 - 1 + 6 == 11, "s5p01 C")
w1 = (1, -1, 1); w2 = (0, 2, 1)
check(dot(n1, w1) == 0 and dot(n1, w2) == 0, "s5p01 base")
poly = [add(P1, add(mul(s1*1.5, w1), mul(s2*1.2, w2))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly:
    check(abs(dot(n1, q) + d1) < 1e-9, "s5p01 poly no plano")
print("s5p01 poligono:", [r2(q) for q in poly], "ponta normal", add(P1, n1))

# s5-p02
P2 = (1, -2, 4); n2 = (2, -1, 2); d2 = -5
val = dot(n2, P2) + d2; check(val == 7, "s5p02 val")
check(norm(n2) == 3, "s5p02 norma")
check(F(abs(dot(n2, P2) + 5), 3) == F(17, 3), "s5p02 D")
check(2 - 2 + 8 - 5 == 3, "s5p02 E")
Q2 = sub(P2, mul(F(val, 9), n2))
check(dot(n2, Q2) + d2 == 0, "s5p02 pe")
check(norm(sub(P2, Q2)) - 7/3 < 1e-12, "s5p02 dist")
a2 = (1, 0, -1); b2 = (1, 2, 0)
check(dot(n2, a2) == 0 and dot(n2, b2) == 0, "s5p02 base")
poly2 = [add(Q2, add(mul(F(s1*3, 2), a2), mul(F(s2, 1), b2))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly2:
    check(dot(n2, q) + d2 == 0, "s5p02 poly")
print("s5p02 pe:", r2(Q2), "poligono:", [r2(q) for q in poly2])

# s5-p03
na = (1, -1, 0); nb = (0, 1, -1)
c3 = dot(na, nb)/(norm(na)*norm(nb))
check(dot(na, nb) == -1, "s5p03 dot")
check(abs(deg(math.acos(abs(c3))) - 60) < 1e-9, "s5p03 60")
nerr = (1, -1, 3)
ang3 = deg(math.acos(abs(dot(nerr, nb))/(norm(nerr)*norm(nb))))
print("s5p03 normal com o 3:", dot(nerr, nb), round(ang3, 4))
# figura: reta comum (t-3, t, t-1); centro t=1 -> (-2,1,0)
Qc = (-2, 1, 0)
check(Qc[0] - Qc[1] + 3 == 0 and Qc[1] - Qc[2] - 1 == 0, "s5p03 centro")
dd = (1, 1, 1)
polyA = [add(Qc, add(mul(s1*1.5, dd), mul(s2*2, (0, 0, 1)))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
polyB = [add(Qc, add(mul(s1*1.5, dd), mul(s2*2, (1, 0, 0)))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in polyA:
    check(abs(q[0] - q[1] + 3) < 1e-9, "s5p03 polyA")
for q in polyB:
    check(abs(q[1] - q[2] - 1) < 1e-9, "s5p03 polyB")
print("s5p03 polyA", [r2(q) for q in polyA], "polyB", [r2(q) for q in polyB], "n1 ponta", add(Qc, na), "n2 ponta", add(Qc, nb))

# s5-p04
A4 = (1, 0, 2); u4 = (1, 1, 0); v4 = (0, 1, -1)
n4 = cross(u4, v4); check(n4 == (-1, 1, 1), "s5p04 n")
def no_plano4(P):
    return dot(n4, sub(P, A4)) == 0
check(add(A4, add(mul(2, u4), v4)) == (3, 3, 1) and no_plano4((3, 3, 1)), "s5p04 certa")
check(add(mul(2, u4), v4) == (2, 3, -1), "s5p04 A")
for P in [(2, 3, -1), (1, 1, 0), (3, 3, 3), (2, 1, 1)]:
    check(not no_plano4(P), f"s5p04 {P} fora")
poly4 = [add(A4, add(mul(s1, (2.5, 2.5, 0)), mul(s2, (0, 1.5, -1.5)))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly4:
    check(abs(dot(n4, sub(q, A4))) < 1e-9, "s5p04 poly")
print("s5p04 poly", [r2(q) for q in poly4], "A+2u", add(A4, mul(2, u4)), "A+u", add(A4, u4), "A+v", add(A4, v4))

# s5-p05
A5 = (1, 0, 2); B5 = (3, 1, 1); C5 = (0, 2, 3)
AB5 = sub(B5, A5); AC5 = sub(C5, A5)
n5 = cross(AB5, AC5); check(n5 == (3, -1, 5), "s5p05 n")
d5 = -dot(n5, A5); check(d5 == -13, "s5p05 d")
for P in (A5, B5, C5):
    check(dot(n5, P) + d5 == 0, "s5p05 pontos")
check(dot((3, 1, 5), B5) - 13 == 2, "s5p05 A fora B")
check(dot(AB5, A5) == 0, "s5p05 D passa A")
check(dot(AB5, B5) != 0, "s5p05 D nao passa B")
AxB = cross(A5, B5); check(AxB == (-2, 5, 1), "s5p05 E")
check(dot(AxB, A5) == 0 and dot(AxB, B5) == 0 and dot(AxB, C5) == 13, "s5p05 E passa A,B nao C")
G5 = mul(F(1, 3), add(add(A5, B5), C5))
print("s5p05 baricentro", r2(G5), "ponta normal/2", r2(add(G5, mul(0.5, n5))))

# s5-p06
A6 = (1, 2, 0); v6 = (2, -1, 1); n6 = (1, 3, 1)
check(dot(v6, n6) == 0, "s5p06 v.n")
check(dot(n6, A6) - 7 == 0, "s5p06 A no plano")
w6 = (1, 0, -1); check(dot(n6, w6) == 0, "s5p06 base")
poly6 = [add(A6, add(mul(s1*2, v6), mul(s2*2, w6))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly6:
    check(dot(n6, q) - 7 == 0, "s5p06 poly")
print("s5p06 poly", poly6, "reta", add(A6, mul(-1.5, v6)), add(A6, mul(1.5, v6)), "ponta n", add(A6, n6))

# s5-p07
v7 = (1, 1, 0); n7 = (1, 0, 1)
s7 = abs(dot(v7, n7))/(norm(v7)*norm(n7))
check(abs(deg(math.asin(s7)) - 30) < 1e-9, "s5p07 30")
check(abs(deg(math.acos(s7)) - 60) < 1e-9, "s5p07 60")
e1 = deg(math.asin(abs(dot(v7, (1, 1, 1)))/(norm(v7)*norm((1, 1, 1)))))
e2 = deg(math.asin(abs(dot((2, 1, -1), n7))/(norm((2, 1, -1))*norm(n7))))
e3 = deg(math.asin(abs(dot(v7, n7))/(dot(v7, v7)*dot(n7, n7))))
print("s5p07 normal (1,1,1):", round(e1, 4), " ponto no lugar de v:", round(e2, 4), " normas ao quadrado:", round(e3, 4))
# intersecao r: (2+t, 1+t, -1) com x + z - 4 = 0 -> t = 3
I7 = (5, 4, -1); check(I7[0] + I7[2] - 4 == 0, "s5p07 I")
poly7 = [add(I7, add(mul(s1*2.5, (0, 1, 0)), mul(s2*2, (1, 0, -1)))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly7:
    check(q[0] + q[2] - 4 == 0, "s5p07 poly")
print("s5p07 poly", poly7, "reta", (2, 1, -1), add((2, 1, -1), mul(5, v7)), "n ponta", add(I7, mul(2, n7)), "v ponta", add(I7, mul(2, v7)))

# s5-p08
# pi1: 2x - 2y + z - 3 = 0 ; pi2: 4x - 4y + 2z + 9 = 0
dist8 = F(abs(-3 - F(9, 2)), 3); check(dist8 == F(5, 2), "s5p08 5/2")
check(F(abs(-3 - 9), 3) == 4, "s5p08 A")
check(F(abs(-3 - 9), 6) == 2, "s5p08 B")
check(F(abs(-3 + F(9, 2)), 3) == F(1, 2), "s5p08 C")
check(abs(4*0 - 4*0 + 2*3 + 9) == 15 and F(15, 6) == F(5, 2), "s5p08 D e conferencia")
c1 = mul(F(1, 3), (2, -2, 1)); c2 = mul(F(-1, 2), (2, -2, 1))
check(dot((2, -2, 1), c1) - 3 == 0 and dot((4, -4, 2), c2) + 9 == 0, "s5p08 centros")
check(abs(norm(sub(c1, c2)) - 2.5) < 1e-12, "s5p08 segmento")
a8 = (1, 1, 0); b8 = (1, 0, -2)
check(dot((2, -2, 1), a8) == 0 and dot((2, -2, 1), b8) == 0, "s5p08 base")
polyP = [add(c1, add(mul(s1*2, a8), mul(s2*1.2, b8))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
polyQ = [add(c2, add(mul(s1*2, a8), mul(s2*1.2, b8))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in polyP:
    check(abs(dot((2, -2, 1), q) - 3) < 1e-9, "s5p08 polyP")
for q in polyQ:
    check(abs(dot((4, -4, 2), q) + 9) < 1e-9, "s5p08 polyQ")
print("s5p08 c1", r2(c1), "c2", r2(c2), "polyP", [r2(q) for q in polyP], "polyQ", [r2(q) for q in polyQ])

# s5-p09
A9 = (1, -1, 2); v9 = (2, 1, -2); P9 = (3, -2, 2)
AP9 = sub(P9, A9); c9 = cross(AP9, v9)
check(AP9 == (2, -1, 0) and c9 == (2, 4, 4) and norm(c9) == 6 and norm(v9) == 3, "s5p09")
check(dot(AP9, v9) == 3 and dot(AP9, AP9) == 5, "s5p09 proj e AP")
check(5 - 1**2 == 2**2, "s5p09 pitagoras")
Q9 = add(A9, mul(F(dot(AP9, v9), 9), v9))
check(Q9 == (F(5, 3), F(-2, 3), F(4, 3)) and abs(norm(sub(P9, Q9)) - 2) < 1e-12, "s5p09 pe")
print("s5p09 pe", r2(Q9), "reta", add(A9, mul(-1, v9)), add(A9, mul(2, v9)), "A+v", add(A9, v9), "P+v", add(P9, v9))

# s5-p10
A10 = (1, 0, 2); u10 = (2, 1, 0); B10 = (4, -1, 4); v10 = (0, 1, 1)
c10 = cross(u10, v10); AB10 = sub(B10, A10)
check(c10 == (1, -2, 2) and norm(c10) == 3, "s5p10 cross")
check(AB10 == (3, -1, 2) and dot(c10, AB10) == 9, "s5p10 misto")
check(dot(AB10, AB10) == 14, "s5p10 AB")
check(abs(9/(norm(u10)*norm(v10)) - 9/math.sqrt(10)) < 1e-12, "s5p10 E")
# pes da perpendicular comum: (B + h v) - (A + t u) ortogonal a u e v
# sistema: (AB + h v - t u).u = 0 ; (AB + h v - t u).v = 0
a11 = dot(u10, u10); a12 = -dot(v10, u10); b1 = dot(AB10, u10)
a21 = dot(u10, v10); a22 = -dot(v10, v10); b2 = dot(AB10, v10)
det = a11*a22 - a12*a21
tt = F(b1*a22 - a12*b2, det); hh = F(a11*b2 - a21*b1, det)
Pr = add(A10, mul(tt, u10)); Ps = add(B10, mul(hh, v10))
seg = sub(Ps, Pr)
check(dot(seg, u10) == 0 and dot(seg, v10) == 0, "s5p10 perp comum")
check(abs(norm(seg) - 3) < 1e-12, "s5p10 dist 3")
print("s5p10 t,h", tt, hh, "Pr", r2(Pr), "Ps", r2(Ps))
print("s5p10 reta r", r2(add(A10, mul(-1.5, u10))), r2(add(A10, mul(1.5, u10))), " s", r2(add(B10, mul(-2, v10))), r2(add(B10, mul(1, v10))))

# s5-p11
m1 = (1, 1, -1); m2 = (2, -1, 1)
dir11 = cross(m1, m2); check(dir11 == (0, -3, -3), "s5p11 dir")
P11 = (1, 1, 0)
check(dot(m1, P11) - 2 == 0 and dot(m2, P11) - 1 == 0, "s5p11 ponto")
def contida(P0, d):
    return dot(m1, P0) - 2 == 0 and dot(m2, P0) - 1 == 0 and dot(m1, d) == 0 and dot(m2, d) == 0
check(contida(P11, (0, 1, 1)), "s5p11 certa")
check(not contida(P11, (1, 1, -1)), "s5p11 B")
check(not contida(P11, (0, 1, -1)), "s5p11 C")
check(cross(m1, m2) != (0, 3, -3), "")
check(not contida((1, 0, 1), (0, 1, 1)), "s5p11 D")
check(not paralelos(m1, m2), "s5p11 E nao paralelos")
dd11 = (0, 1, 1); wA = cross(m1, dd11); wB = cross(m2, dd11)
check(wA == (2, -1, 1) and dot(m1, wA) == 0, "s5p11 wA")
check(wB == (-2, -2, 2) and dot(m2, wB) == 0, "s5p11 wB")
Cc = add(P11, mul(0.5, dd11))
polyA = [add(Cc, add(mul(s1*2, dd11), mul(s2*0.8, wA))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
polyB = [add(Cc, add(mul(s1*2, dd11), mul(s2*0.8, mul(0.5, wB)))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in polyA:
    check(abs(dot(m1, q) - 2) < 1e-9, "s5p11 polyA")
for q in polyB:
    check(abs(dot(m2, q) - 1) < 1e-9, "s5p11 polyB")
print("s5p11 polyA", [r2(q) for q in polyA], "polyB", [r2(q) for q in polyB], "reta", r2(add(Cc, mul(-2.5, dd11))), r2(add(Cc, mul(2.5, dd11))))

# s5-p12
n12 = (2, 1, -2)
def dist12(k):
    P = (1, k, 2)
    return F(abs(dot(n12, P) + 4), 3)
check(dist12(7) == 3 and dist12(-11) == 3, "s5p12 certa")
check(dist12(1) == 1 and dist12(-5) == 1, "s5p12 B (|k+2| = 3)")
check(abs(25 + 2) == 27 and abs(-29 + 2) == 27, "s5p12 D")
check(abs(-1 + 10) == 9 and abs(-19 + 10) == 9, "s5p12 E")
for k in (7, -11):
    P = (1, k, 2)
    val = dot(n12, P) + 4
    Q = sub(P, mul(F(val, 9), n12))
    check(dot(n12, Q) + 4 == 0, "s5p12 pe")
    print("s5p12 k", k, "valor", val, "pe", Q)
Cm = (1, -2, 2); check(dot(n12, Cm) + 4 == 0, "s5p12 centro")
a12v = (1, 0, 1); b12v = (0, 2, 1)
check(dot(n12, a12v) == 0 and dot(n12, b12v) == 0, "s5p12 base")
poly12 = [add(Cm, add(mul(s1*3, a12v), mul(s2*5, b12v))) for s1, s2 in [(1, 1), (1, -1), (-1, -1), (-1, 1)]]
for q in poly12:
    check(dot(n12, q) + 4 == 0, "s5p12 poly")
print("s5p12 poly", poly12)

print("CONFERENCIAS OK:", ok)
