# Revisor adversarial - lote ga_s2b (Lista 2, Q2 a Q12).
# Refaz cada conta do zero com fracoes exatas. Nao le o campo "resposta".
import math
import sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
falhas = []


def ok(cond, msg):
    if not cond:
        falhas.append(msg)
        print("FALHA:", msg)
    else:
        print("ok   :", msg)


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def esc(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def n2(a):
    return dot(a, a)


def raiz_simpl(q):
    # q inteiro >= 0 -> (k, r) com sqrt(q) = k*sqrt(r)
    q = int(q)
    k, r = 1, q
    d = 2
    while d * d <= r:
        while r % (d * d) == 0:
            r //= d * d
            k *= d
        d += 1
    return k, r


def proj(v, u):
    return esc(dot(u, v) / n2(u), u)


print("== Q2 ==")
u = (F(1), F(4), F(3)); v = (F(-1), F(1), F(-1)); w = (F(-2), F(-1, 2), F(5)); z = (F(-1), F(2), F(-3))
nomes = {"u": u, "v": v, "w": w, "z": z}
pares = [("u", "v"), ("u", "w"), ("u", "z"), ("v", "w"), ("v", "z"), ("w", "z")]
zeros = []
for a, b in pares:
    d = dot(nomes[a], nomes[b])
    print(f"  {a}.{b} = {d}")
    if d == 0:
        zeros.append(a + b)
ok(zeros == ["uv"], "Q2: unico par ortogonal e u,v")
ok(dot(u, w) == 11 and dot(u, z) == -2 and dot(v, w) == F(-7, 2) and dot(v, z) == 6 and dot(w, z) == -14, "Q2: valores da receita")
ok(1 + 8 - 9 == 0, "Q2 altA: com 1*(-1) como +1, u.z vira 1+8-9=0")
ok(cross(u, v) == (-7, -2, 5), "Q2 altC: u x v = (-7,-2,5)")
ok(1 + 2 - 3 == 0, "Q2 altD: (-1)(-3) escrito -3 da 1+2-3=0")
ok(cross(w, v) == esc(-1, cross(v, w)), "Q2 altE: w x v = -(v x w)")
# confira (versao nova): Pitagoras
s = add(u, v)
ok(s == (0, 5, 2) and n2(s) == 29 and n2(u) == 26 and n2(v) == 3, "Q2 confira: u+v=(0,5,2), 29 = 26 + 3")
ok(n2(cross(u, v)) == 78 and n2(u) * n2(v) == 78, "Q2 confira alt: |u x v|^2 = |u|^2|v|^2 = 78")
# atalho: positivos/negativos de u.w
ok(15 - 4 == dot(u, w), "Q2 confira antigo: 15 - 4 = 11")

print("== Q3 ==")
uu = (F(1), F(2), F(3)); vv = (F(-1), F(0), F(3)); ww = (F(-1), F(-1), F(-1))


def resolve3(M, b):
    # Cramer
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    D = det(M)
    sol = []
    for j in range(3):
        Mj = [list(r) for r in M]
        for i in range(3):
            Mj[i][j] = b[i]
        sol.append(det(Mj) / D)
    return tuple(sol), D


r, D = resolve3([uu, vv, ww], [F(-6), F(-8), F(2)])
print("  r =", r, " det =", D)
ok(r == (-1, 2, -3), "Q3: r = (-1, 2, -3)")
ok(D != 0, "Q3: u, v, w nao coplanares")
alt = (F(1), F(-2), F(3))
ok((dot(alt, uu), dot(alt, vv), dot(alt, ww)) == (6, 8, -2), "Q3 altA: produtos 6, 8, -2")
rB, _ = resolve3([uu, vv, (F(1), F(1), F(1))], [F(-6), F(-8), F(2)])
ok(rB == (11, -10, 1), "Q3 altB: x+y+z=2 leva a (11,-10,1)")
alt = (F(-6), F(-8), F(2))
ok(dot(alt, uu) == -16, "Q3 altC: (-6,-8,2).u = -16")
alt = (F(2), F(-1), F(-2))
ok(dot(alt, uu) == -6 and dot(alt, vv) == -8 and dot(alt, ww) == 1, "Q3 altE: cumpre 1a e 2a, 3a da 1")
# reta das duas primeiras: x = 3z+8, y = -7-3z ; r.w = -1 - z
for zz in [F(-3), F(-2), F(0)]:
    p = (3 * zz + 8, -7 - 3 * zz, zz)
    ok(dot(p, uu) == -6 and dot(p, vv) == -8 and dot(p, ww) == -1 - zz, f"Q3 reta: z={zz} p={p} r.w = -1 - z")
# perder o -1: -z = 2 -> z = -2 -> (2,-1,-2)
zz = F(-2)
ok((3 * zz + 8, -7 - 3 * zz, zz) == (2, -1, -2), "Q3 altE nova: -z = 2 da (2,-1,-2)")
# receita
zz = F(-3)
ok((3 * zz + 8) + 2 * (-4 * zz - 10) + 3 * zz == -6, "Q3 receita: z = -3 cumpre a 1a")
ok(-2 * zz - 12 == -6, "Q3 receita: -2z - 12 = -6")
# atalho
ok(dot((1, -2, 3), vv) == 8 and dot((-6, -8, 2), vv) == 12, "Q3 atalho: 8 e 12")
ok(dot((11, -10, 1), vv) == -8 and dot((2, -1, -2), vv) == -8, "Q3 atalho: restantes passam em v")
ok(dot((11, -10, 1), ww) == -2 and dot((2, -1, -2), ww) == 1, "Q3 atalho: w decide")
# conferir via matriz: M * r
ok(tuple(dot(row, r) for row in [uu, vv, ww]) == (-6, -8, 2), "Q3 trabalho: MATRIZ.MULT(M; r) = (-6,-8,2)")

print("== Q4 ==")
a4 = (F(3), 0, 0); b4 = (0, F(2), 0); c4 = (0, 0, F(2))
s4 = add(add(a4, b4), c4)
ok(n2(s4) == 17 == n2(a4) + n2(b4) + n2(c4), "Q4: 9+4+4 = 17")
ok(abs(math.sqrt(17) - 4.123) < 0.001, "Q4: sqrt17 ~ 4,1")
ok(3 + 2 + 2 == 7, "Q4 conversa: soma das normas 7")
a = (F(1), 0, 0); b = (F(1), 0, 0); c = (0, 0, 0)
ok(n2(add(add(a, b), c)) - (n2(a) + n2(b) + n2(c)) == 2 * dot(a, b) == 2, "Q4 confira: diferenca 2 = 2 u.v")
# caso geral numerico com vetores ortogonais quaisquer
p1 = (F(1), F(1), F(0)); p2 = (F(1), F(-1), F(2)); p3 = cross(p1, p2)
ok(dot(p1, p2) == 0 and dot(p1, p3) == 0 and dot(p2, p3) == 0, "Q4: trio ortogonal de teste")
ok(n2(add(add(p1, p2), p3)) == n2(p1) + n2(p2) + n2(p3), "Q4: identidade vale no trio de teste")
ok(n2(cross(p1, p2)) == n2(p1) * n2(p2), "Q4 altD: |u x v| = |u||v| para ortogonais")

print("== Q5 ==")


def pts5(m):
    return (2 * m, F(-1), F(1)), (m, 2 * m, F(1)), (F(1), F(-1), F(2))


def f5(m):
    A, B, C = pts5(m)
    return dot(sub(B, A), sub(C, A))


# 2m^2 - m
for m in [F(0), F(1, 2), F(-1, 2), F(1), F(3)]:
    ok(f5(m) == 2 * m * m - m, f"Q5: AB.AC = 2m^2 - m em m={m}")
ok(f5(F(0)) == 0 and f5(F(1, 2)) == 0, "Q5a: m = 0 e m = 1/2 zeram")
# altA: -m - 2m^2 = 0 -> m=0 ou -1/2
ok(-F(-1, 2) - 2 * F(-1, 2) ** 2 == 0, "Q5a altA: -m - 2m^2 zera em -1/2")
# altC: AB x AC nulo para nenhum m -> componentes (2m+1, m, ...)
for m in [F(0), F(1, 2), F(-1, 2)]:
    A, B, C = pts5(m)
    cr = cross(sub(B, A), sub(C, A))
    ok(cr != (0, 0, 0), f"Q5a altC: AB x AC nao nulo em m={m}: {cr}")
# simbolico: AB x AC = (2m+1, m, -(2m+1)(1-2m)) -> zero exige m=0 e m=-1/2
for m in [F(0), F(1, 2), F(-1, 2), F(2)]:
    A, B, C = pts5(m)
    ok(cross(sub(B, A), sub(C, A)) == (2 * m + 1, m, -(2 * m + 1) * (1 - 2 * m)), f"Q5a altC formula m={m}")
# altD: BA.BC = 3m^2 + 5m + 1
for m in [F(0), F(1), F(-2), F(1, 3)]:
    A, B, C = pts5(m)
    ok(dot(sub(A, B), sub(C, B)) == 3 * m * m + 5 * m + 1, f"Q5a altD: BA.BC = 3m^2+5m+1 em m={m}")
disc = 25 - 12
ok(disc == 13, "Q5a altD: raizes (-5 +- sqrt13)/6")
for sgn in (1, -1):
    mm = (-5 + sgn * math.sqrt(13)) / 6
    ok(abs(3 * mm * mm + 5 * mm + 1) < 1e-12, f"Q5a altD: raiz {mm:.4f}")
    ok(abs(2 * mm * mm - mm) > 0.1, f"Q5a altD: {mm:.4f} nao zera AB.AC")
# confira m=-1/2
A, B, C = pts5(F(-1, 2))
ok(sub(B, A) == (F(1, 2), 0, 0) and sub(C, A) == (2, 0, 1) and f5(F(-1, 2)) == 1, "Q5a confira: m=-1/2 da 1")
# areas
A, B, C = pts5(F(0))
AB0, AC0 = sub(B, A), sub(C, A)
ok(AB0 == (0, 1, 0) and AC0 == (1, 0, 1), "Q5b: m=0 vetores")
ok(n2(cross(AB0, AC0)) == 2 and cross(AB0, AC0) == (1, 0, -1), "Q5b: m=0 |AB x AC|^2 = 2 -> area sqrt2/2")
A, B, C = pts5(F(1, 2))
AB1, AC1 = sub(B, A), sub(C, A)
ok(A == (1, -1, 1) and B == (F(1, 2), 1, 1), "Q5b: pontos m=1/2")
ok(AB1 == (F(-1, 2), 2, 0) and AC1 == (0, 0, 1), "Q5b: m=1/2 vetores")
ok(cross(AB1, AC1) == (2, F(1, 2), 0) and n2(cross(AB1, AC1)) == F(17, 4), "Q5b: m=1/2 |AB x AC|^2 = 17/4 -> area sqrt17/4")
ok(n2(AB1) == F(17, 4) and n2(AC1) == 1, "Q5b: catetos sqrt17/2 e 1")
ok(n2(AB1) * n2(AC1) / 2 == F(17, 8), "Q5b altB: 17/8")
ok(n2(AB0) * n2(AC0) / 2 == 1, "Q5b altB: 1 com m=0")
ok(F(-1, 4) + 4 == F(15, 4), "Q5b altE: -1/4 + 4 = 15/4")
ok(abs(math.sqrt(17) / 4 - 1.03) < 0.005 and abs(math.sqrt(2) / 2 - 0.71) < 0.005, "Q5b atalho: 1,03 e 0,71")

print("== Q6 ==")
A6 = (F(-1), F(2), F(3)); B6 = (F(-2), F(3), F(4))


def area2_6(C):
    # quadrado de |AB x AC|
    return n2(cross(sub(B6, A6), sub(C, A6)))


for c in [F(1), F(2)]:
    ok(area2_6((0, 0, c)) == 2, f"Q6: C=(0,0,{c}) da |AB x AC|^2 = 2 (area sqrt2/2)")
for c in [F(k, 2) for k in range(-10, 11)]:
    val = area2_6((0, 0, c))
    ok(val == 2 * c * c - 6 * c + 6, f"Q6: formula 2c^2-6c+6 em c={c}")
# so c=1 e c=2: c^2 - 3c + 2 = 0
ok((1 - 3 + 2) == 0 and (4 - 6 + 2) == 0, "Q6: raizes 1 e 2")
ok(cross(sub(B6, A6), sub((0, 0, F(5)), A6)) == (4, 3, 1), "Q6: AB x AC = (c-1, c-2, 1) em c=5")
for c in [F(-1), F(-2)]:
    ok(area2_6((0, 0, c)) != 2, f"Q6 altA: C=(0,0,{c}) nao serve")
ok(area2_6((1, 0, 0)) == 2 and area2_6((2, 0, 0)) == 2, "Q6 altC: (1,0,0) e (2,0,0) tambem dao area sqrt2/2 (eixo OX)")
# altD: AC com c+3 -> (c+5, c+4, 1)
for c in [F(-4), F(-5)]:
    ACw = (F(1), F(-2), c + 3)
    ok(n2(cross(sub(B6, A6), ACw)) == 2, f"Q6 altD: c={c} com c+3 da 2")
# altE: 2c^2-6c+6 = 1/2 sem raiz
ok(36 - 4 * 2 * F(11, 2) < 0, "Q6 altE: discriminante negativo")
# minimo em c=3/2
ok(area2_6((0, 0, F(3, 2))) == F(3, 2), "Q6 visual: minimo em 3/2")
for c, esp in [(0, 1.22), (0.5, 0.94), (1, 0.71), (1.5, 0.61), (2, 0.71), (2.5, 0.94), (3, 1.22)]:
    val = math.sqrt((c - 1) ** 2 + (c - 2) ** 2 + 1) / 2
    ok(round(val, 2) == esp, f"Q6 trabalho: c={c} area {val:.4f} ~ {esp}")
# confira por B
BA6 = sub(A6, B6)
ok(BA6 == (1, -1, -1), "Q6 confira: BA")
ok(sub((0, 0, F(2)), B6) == (2, -3, -2) and cross(BA6, sub((0, 0, F(2)), B6)) == (-1, 0, -1), "Q6 confira: C=(0,0,2)")
ok(sub((0, 0, F(1)), B6) == (2, -3, -3) and cross(BA6, sub((0, 0, F(1)), B6)) == (0, 1, -1), "Q6 confira: C=(0,0,1)")
ok((-1 - 1) ** 2 + (-1 - 2) ** 2 + 1 == 14, "Q6 atalho: c=-1 da 14")

print("== Q7 ==")
w7 = (F(1), F(2), F(0)); u7 = (F(1), F(-1), F(2)); v7 = (F(8), F(-4), F(-6))
for t in [F(1), F(2), F(-2), F(4)]:
    ok(cross(esc(t, w7), u7) == (4 * t, -2 * t, -3 * t), f"Q7: x x u = (4t,-2t,-3t) em t={t}")
ok(cross(esc(F(2), w7), u7) == v7, "Q7: t=2 -> x=(2,4,0)")
ok(cross(u7, esc(F(-2), w7)) == v7, "Q7 altA: u x x = v com t=-2")
ok(cross(w7, u7) == (4, -2, -3), "Q7 altB: t=1 da metade")
ok(cross((4, 8, 0), u7) == (16, -8, -12), "Q7 altC: (4,8,0) da o dobro")
ok(dot(v7, (2, 4, 0)) == 0 and dot(v7, u7) == 0, "Q7: v perpendicular a x e u")

print("== Q8 ==")
A8 = (1, 2, 3); B8 = (5, 2, 3); C8 = (1, 2, 6)


def ang(p, q):
    return math.degrees(math.acos(dot(p, q) / math.sqrt(n2(p) * n2(q))))


aA = ang(sub(B8, A8), sub(C8, A8)); aB = ang(sub(A8, B8), sub(C8, B8)); aC = ang(sub(A8, C8), sub(B8, C8))
print(f"  A={aA:.4f} B={aB:.4f} C={aC:.4f} soma={aA + aB + aC:.6f}")
ok(round(aA, 2) == 90 and round(aB, 2) == 36.87 and round(aC, 2) == 53.13, "Q8: 90, 36,87, 53,13")
ok(dot(sub(A8, B8), sub(C8, B8)) == 16 and dot(sub(A8, C8), sub(B8, C8)) == 9, "Q8: 16 e 9")
ok(round(ang(sub(B8, A8), sub(C8, B8)), 2) == 143.13, "Q8 altC: AB com BC da 143,13")
ok(round(math.acos(0.8), 4) == 0.6435 and round(math.acos(0.6), 4) == 0.9273, "Q8 altE: radianos 0,6435 e 0,9273")
ok(round(math.degrees(math.atan(0.75)), 2) == 36.87, "Q8 confira: arctg 0,75")

print("== Q9 ==")
casos = {
    "a": ((F(-1), F(2), F(3)), (F(2), F(0), F(1)), (F(-1, 14), F(1, 7), F(3, 14)), (F(29, 14), F(-1, 7), F(11, 14))),
    "b": ((F(1), F(1), F(1)), (F(-1), F(2), F(3)), (F(4, 3), F(4, 3), F(4, 3)), (F(-7, 3), F(2, 3), F(5, 3))),
    "c": ((F(1), F(2), F(0)), (F(-3), F(-6), F(0)), (F(-3), F(-6), F(0)), (F(0), F(0), F(0))),
}
for k, (uu9, vv9, e1, e2) in casos.items():
    v1 = proj(vv9, uu9); v2 = sub(vv9, v1)
    ok(v1 == e1 and v2 == e2, f"Q9{k}: v1={v1} v2={v2}")
    ok(dot(v2, uu9) == 0 and add(v1, v2) == vv9, f"Q9{k}: v2 perp u e soma = v")
# 9a distratores
u9, v9 = casos["a"][0], casos["a"][1]
pA = proj(u9, v9)
ok(pA == (F(2, 5), 0, F(1, 5)) and sub(v9, pA) == (F(8, 5), 0, F(4, 5)), "Q9a altA")
ok(sub(v9, u9) == (3, -2, -2) and dot(sub(v9, u9), u9) == -13, "Q9a altB")
ok(sub(casos["a"][2], v9) == (F(-29, 14), F(1, 7), F(-11, 14)), "Q9a altD")
v1E = esc(F(5, 14), u9)
ok(v1E == (F(-5, 14), F(5, 7), F(15, 14)) and sub(v9, v1E) == (F(33, 14), F(-5, 7), F(-1, 14)), "Q9a altE")
ok(dot(sub(v9, v1E), u9) == -4, "Q9a atalho: altE falha no teste perp (-4)")
ok(round(math.degrees(math.acos(1 / math.sqrt(70))), 1) == 83.1, "Q9a visual: angulo ~83 graus (quase 90)")
# 9b distratores
u9, v9 = casos["b"][0], casos["b"][1]
pA = proj(u9, v9)
ok(pA == (F(-2, 7), F(4, 7), F(6, 7)) and sub(v9, pA) == (F(-5, 7), F(10, 7), F(15, 7)), "Q9b altA")
ok(dot(sub(v9, pA), u9) != 0 and dot(pA, u9) != 0, "Q9b altA: nenhuma parte perp a u")
ok(sub(v9, esc(4, u9)) == (-5, -2, -1) and dot(sub(v9, esc(4, u9)), u9) == -8, "Q9b altB")
v1C = esc(F(4, 14), u9)
ok(v1C == (F(2, 7),) * 3 and sub(v9, v1C) == (F(-9, 7), F(12, 7), F(19, 7)), "Q9b altC")
ok(sum(sub(v9, v1C)) == F(22, 7), "Q9b atalho: 22/7")
ok(sub(v9, (2, 2, 2)) == (-3, 0, 1), "Q9b altD")
# 9c distratores
u9, v9 = casos["c"][0], casos["c"][1]
ok(dot(u9, v9) == -15 and n2(u9) == 5, "Q9c: -15 e 5")
ok(sub(v9, (3, 6, 0)) == (-6, -12, 0) and dot((-6, -12, 0), u9) == -30, "Q9c altA")
ok(sub(v9, (-15, -30, 0)) == (12, 24, 0), "Q9c altC")

print("== Q10 ==")
A10 = (F(0), F(3), F(-4)); B10 = (F(3), F(0), F(5)); C10 = (F(-1), F(-1), F(-2)); D10 = (F(4), F(1), F(-4))
AB10 = sub(B10, A10); CD10 = sub(D10, C10)
ok(AB10 == (3, -3, 9) and CD10 == (5, 2, -2), "Q10: vetores")
p10 = proj(AB10, CD10)
ok(p10 == (F(-15, 11), F(-6, 11), F(6, 11)), f"Q10: proj = {p10}")
ok(proj(CD10, AB10) == (F(-3, 11), F(3, 11), F(-9, 11)) and n2(AB10) == 99, "Q10 altA")
ok(proj(sub(A10, B10), CD10) == (F(15, 11), F(6, 11), F(-6, 11)), "Q10 altB")
ok(esc(dot(AB10, CD10), CD10) == (-45, -18, 18), "Q10 altC")
ok(esc(F(-9, 25), CD10) == (F(-9, 5), F(-18, 25), F(18, 25)), "Q10 altE")
ok(proj(AB10, esc(-1, CD10)) == p10, "Q10: DC no lugar de CD da o mesmo")
res = sub(AB10, p10)
ok(res == (F(48, 11), F(-27, 11), F(93, 11)) and dot(res, CD10) == 0, "Q10 confira")
ok(round(-9 / 33, 4) == -0.2727, "Q10 trabalho: -0,2727")
ok(add(C10, AB10) == (2, -4, 7), "Q10 figura: ponta de AB transportado")
tip = add(C10, p10)
ok(all(abs(float(a) - b) < 0.001 for a, b in zip(tip, (-2.364, -1.545, -1.455))), f"Q10 figura: ponta da proj {tuple(float(x) for x in tip)}")

print("== Q11 ==")
M = (F(-1), F(2), F(-3)); N = (F(-3), F(1), F(2)); P = (F(1), F(1), F(2))
MN, MP = sub(N, M), sub(P, M)
cr = cross(MN, MP)
ok(MN == (-2, -1, 5) and MP == (2, -1, 5) and cr == (0, 20, 4), "Q11: MN x MP = (0,20,4)")
ok(n2(cr) == 416 and raiz_simpl(416) == (4, 26), "Q11: |MN x MP| = 4 sqrt26")
A11 = sub(add(M, P), N); B11 = sub(add(M, N), P); C11 = sub(add(N, P), M)
ok(A11 == (3, 2, -3) and B11 == (-5, 2, -3) and C11 == (-1, 0, 7), "Q11: vertices")
ok(esc(F(1, 2), add(A11, B11)) == M and esc(F(1, 2), add(B11, C11)) == N and esc(F(1, 2), add(C11, A11)) == P, "Q11: pontos medios conferem")
crA = cross(sub(B11, A11), sub(C11, A11))
ok(crA == (0, 80, 16) and n2(crA) == 6656 and raiz_simpl(6656) == (16, 26), "Q11: |AB x AC| = 16 sqrt26 -> area 8 sqrt26")
ok(cross(MN, MP)[1] == 5 * 2 - (-2) * 5 == 20, "Q11 altE: segunda coord 10 + 10")
ok(n2((0, 0, 4)) == 16, "Q11 altE: (0,0,4) -> norma 4 -> MNP 2 -> ABC 8")

print("== Q12 ==")
c120 = F(-1, 2)
uv = 2 * 3 * c120
ok(uv == -3, "Q12a: u.v = -3")
ok(2 * 3 * F(1, 2) == 3, "Q12a altA: 3")
# b: |u x v|^2 = |u|^2|v|^2 - (u.v)^2
nb2 = 4 * 9 - uv * uv
ok(nb2 == 27 and raiz_simpl(27) == (3, 3), "Q12b: 3 sqrt3")
ok(abs(6 * math.sin(math.radians(120)) - 5.196) < 0.001, "Q12b trabalho: 5,196")
s120rad = 6 * math.sin(120)
print(f"  6*sin(120 rad) = {s120rad:.4f}")
ok(round(s120rad, 2) == 3.48, "Q12b trabalho: 6*SEN(120) ~ 3,48")
# c
nc2 = 4 + 2 * uv + 9
ok(nc2 == 7, "Q12c: |u+v|^2 = 7")
ok(4 + 9 + 6 == 19 and 4 + 9 - 3 == 10, "Q12c altC/E: 19 e 10")
ok(F(1, 4) + F(27, 4) == 7, "Q12c confira: 1/4 + 27/4 = 7")
ok(13 - 2 * 2 * 3 * F(1, 2) == 7, "Q12c confira: lei dos cossenos com 60")
ok(abs(math.sqrt(7) - 2.65) < 0.005, "Q12c: sqrt7 ~ 2,65")
# d: u x (v - u) = u x v
nvu2 = 9 - 2 * uv + 4
udvu = uv - 4
ok(nvu2 == 19 and udvu == -7, "Q12d: |v-u|^2 = 19 e u.(v-u) = -7")
ok(4 * nvu2 - udvu * udvu == 27, "Q12d: Lagrange 4*19 - 49 = 27")
# coordenadas concretas
sq3 = math.sqrt(3)
uc = (2.0, 0.0, 0.0); vc = (-1.5, 1.5 * sq3, 0.0)
ok(abs(dot(uc, vc) + 3) < 1e-12, "Q12 coords: u.v = -3")
ok(abs(math.sqrt(n2(cross(uc, vc))) - 3 * sq3) < 1e-12, "Q12 coords: |u x v| = 3 sqrt3")
ok(abs(n2(add(uc, vc)) - 7) < 1e-12, "Q12 coords: |u+v|^2 = 7")
ok(abs(math.sqrt(n2(cross(uc, sub(vc, uc)))) - 3 * sq3) < 1e-12, "Q12 coords: |u x (v-u)| = 3 sqrt3")
ok(abs(math.sqrt(n2(sub(vc, uc))) - math.sqrt(19)) < 1e-12, "Q12d altC: |v-u| = sqrt19")
ok(abs(1.5 * sq3 - 2.598) < 0.001, "Q12 figura: 2,598")

print()
print("FALHAS:", len(falhas))
for f in falhas:
    print("  ", f)
