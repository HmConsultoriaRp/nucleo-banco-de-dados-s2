# Conferencia das contas do lote ga_s2b (Lista 2, Q2 a Q12) e dos distratores.
from fractions import Fraction as F
import math

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

def add(a, b):
    return tuple(x + y for x, y in zip(a, b))

def esc(k, a):
    return tuple(k * x for x in a)

def norma2(a):
    return dot(a, a)

def fr(t):
    return "(" + ", ".join(str(x) for x in t) + ")"

def titulo(s):
    print("\n=== " + s + " ===")

# ---------------- Q2 ----------------
titulo("Q2")
u = (1, 4, 3); v = (-1, 1, -1); w = (-2, F(-1, 2), 5); z = (-1, 2, -3)
nomes = {"u": u, "v": v, "w": w, "z": z}
for a in "uvwz":
    for b in "uvwz":
        if a < b:
            print(a, ".", b, "=", dot(nomes[a], nomes[b]))
print("u x v =", fr(cross(u, v)))
# distrator u.z com 1*(-1) virando +1
print("u.z com sinal trocado no primeiro produto:", 1 + 4 * 2 + 3 * (-3))
# distrator v.z com (-1)(-3) virando -3
print("v.z com (-1)(-3) = -3:", (-1) * (-1) + 1 * 2 - 3)
print("v x w =", fr(cross(v, w)), " w x v =", fr(cross(w, v)))

# ---------------- Q3 ----------------
titulo("Q3")
u = (1, 2, 3); v = (-1, 0, 3); w = (-1, -1, -1)
r = (-1, 2, -3)
print("r.u, r.v, r.w =", dot(r, u), dot(r, v), dot(r, w))
for cand in [(1, -2, 3), (11, -10, 1), (-6, -8, 2), (2, -1, -2)]:
    print("candidato", cand, "->", dot(cand, u), dot(cand, v), dot(cand, w))
# distrator (11,-10,1): terceira equacao montada como x + y + z = 2
c = (11, -10, 1)
print("(11,-10,1) em x+y+z=2:", sum(c), " em x+2y+3z:", dot(c, u), " em -x+3z:", dot(c, v))
# distrator (1,-2,3): sinais dos segundos membros trocados
print("(1,-2,3) produtos:", dot((1, -2, 3), u), dot((1, -2, 3), v), dot((1, -2, 3), w))
print("u x v =", fr(cross(u, v)))

# ---------------- Q4 ----------------
titulo("Q4 exemplo da figura")
a = (3, 0, 0); b = (0, 2, 0); c = (0, 0, 2)
s = add(add(a, b), c)
print("soma", s, "norma2", norma2(s), "soma das normas2", norma2(a) + norma2(b) + norma2(c))
print("produtos dois a dois", dot(a, b), dot(a, c), dot(b, c))
print("(norma a + norma b + norma c)^2 =", (3 + 2 + 2) ** 2)

# ---------------- Q5 ----------------
titulo("Q5")
def pontos5(m):
    A = (2 * m, -1, 1); B = (m, 2 * m, 1); C = (1, -1, 2)
    return A, B, C
for m in [F(0), F(1, 2), F(-1, 2)]:
    A, B, C = pontos5(m)
    AB = sub(B, A); AC = sub(C, A)
    cr = cross(AB, AC)
    print("m =", m, "A", fr(A), "B", fr(B), "AB", fr(AB), "AC", fr(AC), "AB.AC", dot(AB, AC),
          "|ABxAC|^2", norma2(cr), "area", math.sqrt(norma2(cr)) / 2)
# conferencia simbolica por amostragem: AB.AC = 2m^2 - m
for m in [F(-2), F(1, 3), F(3)]:
    A, B, C = pontos5(m)
    print("m", m, "AB.AC", dot(sub(B, A), sub(C, A)), "2m^2-m", 2 * m * m - m)
# angulo reto em B: BA.BC = 3m^2 + 5m + 1
for m in [F(-2), F(1, 3), F(3)]:
    A, B, C = pontos5(m)
    print("m", m, "BA.BC", dot(sub(A, B), sub(C, B)), "3m^2+5m+1", 3 * m * m + 5 * m + 1)
for sinal in (1, -1):
    mb = (-5 + sinal * math.sqrt(13)) / 6
    A = (2 * mb, -1, 1); B = (mb, 2 * mb, 1); C = (1, -1, 2)
    print("m =", round(mb, 6), "BA.BC =", round(dot(sub(A, B), sub(C, B)), 12))
# AB x AC nulo?
for m in [F(0), F(1, 2), F(-1, 2)]:
    A, B, C = pontos5(m)
    print("m", m, "AB x AC", fr(cross(sub(B, A), sub(C, A))))
print("areas certas: m=0 ->", math.sqrt(2) / 2, " m=1/2 ->", math.sqrt(17) / 4)
print("sem dividir por 2:", math.sqrt(2), math.sqrt(17) / 2)
print("normas ao quadrado: m=0 ->", F(1) * 2 / 2, " m=1/2 ->", F(17, 4) * 1 / 2)
print("(-1/2)^2 errado como -1/4: norma AB =", math.sqrt(-0.25 + 4), "= sqrt(15)/2 =", math.sqrt(15) / 2,
      " area", math.sqrt(15) / 4)

# ---------------- Q6 ----------------
titulo("Q6")
A = (-1, 2, 3); B = (-2, 3, 4)
for cz in [1, 2, -1, -2, -4, -5, 0, 3]:
    C = (0, 0, cz)
    cr = cross(sub(B, A), sub(C, A))
    print("C =", C, "AB x AC =", cr, "|.|^2 =", norma2(cr), "area =", math.sqrt(norma2(cr)) / 2)
for cx in [1, 2]:
    C = (cx, 0, 0)
    cr = cross(sub(B, A), sub(C, A))
    print("C (eixo OX) =", C, "|.|^2 =", norma2(cr), "area =", math.sqrt(norma2(cr)) / 2)
print("alvo area sqrt(2)/2 =", math.sqrt(2) / 2)
# (c-1)^2 + (c-2)^2 + 1 = 2c^2 - 6c + 6 (conferido por amostragem)
for cz in [F(0), F(1, 2), F(3), F(-2)]:
    print("c", cz, "(c-1)^2+(c-2)^2+1 =", (cz - 1) ** 2 + (cz - 2) ** 2 + 1, " 2c^2-6c+6 =", 2 * cz * cz - 6 * cz + 6)
# sem o 1/2: 2c^2 - 6c + 6 = 1/2 -> 2c^2 - 6c + 11/2 = 0
print("discriminante sem o 1/2:", 36 - 4 * 2 * F(11, 2), "(negativo = sem raiz real)")
print("minimo de |ABxAC|^2 em c = 3/2:", 2 * F(9, 4) - 9 + 6, " area minima", math.sqrt(1.5) / 2)
print("tabela de areas:", [(c / 2, round(math.sqrt((c / 2 - 1) ** 2 + (c / 2 - 2) ** 2 + 1) / 2, 4)) for c in range(0, 7)])
# conferencia por B
for cz in [1, 2]:
    C = (0, 0, cz)
    BA = sub(A, B); BC = sub(C, B)
    print("C", C, "BA", BA, "BC", BC, "BA x BC", cross(BA, BC), "|.|^2", norma2(cross(BA, BC)))
# AC com c+3: (c+5)^2 + (c+4)^2 + 1 = 2
for cz in [-4, -5]:
    print("c =", cz, "(c+5)^2+(c+4)^2+1 =", (cz + 5) ** 2 + (cz + 4) ** 2 + 1)
print("(c+1)(c+2) expandido = c^2 + 3c + 2; raizes -1 e -2")

# ---------------- Q7 ----------------
titulo("Q7")
u = (1, -1, 2); v = (8, -4, -6); w = (1, 2, 0)
for t in [2, -2, 1, 4]:
    x = esc(t, w)
    print("t =", t, "x =", x, "x x u =", cross(x, u), "u x x =", cross(u, x))
print("x x u para t generico: (4t, -2t, -3t); com t=1:", cross(w, u))

# ---------------- Q8 ----------------
titulo("Q8")
A = (1, 2, 3); B = (5, 2, 3); C = (1, 2, 6)
def ang(p, q):
    return math.degrees(math.acos(dot(p, q) / math.sqrt(norma2(p) * norma2(q))))
aA = ang(sub(B, A), sub(C, A)); aB = ang(sub(A, B), sub(C, B)); aC = ang(sub(A, C), sub(B, C))
print("lados AB, AC, BC:", math.sqrt(norma2(sub(B, A))), math.sqrt(norma2(sub(C, A))), math.sqrt(norma2(sub(C, B))))
print("angulos:", round(aA, 2), round(aB, 2), round(aC, 2), "soma", round(aA + aB + aC, 6))
print("B com AB e BC:", round(ang(sub(B, A), sub(C, B)), 2))
print("radianos:", round(math.acos(0.8), 4), round(math.acos(0.6), 4))
print("cosB =", dot(sub(A, B), sub(C, B)), "/", math.sqrt(norma2(sub(A, B)) * norma2(sub(C, B))))

# ---------------- Q9 ----------------
titulo("Q9")
def decomp(u, v, k=None):
    if k is None:
        k = F(dot(u, v), norma2(u))
    v1 = esc(k, u)
    v2 = sub(v, v1)
    return v1, v2
casos = {"a": ((-1, 2, 3), (2, 0, 1)), "b": ((1, 1, 1), (-1, 2, 3)), "c": ((1, 2, 0), (-3, -6, 0))}
for nome, (u, v) in casos.items():
    v1, v2 = decomp(u, v)
    print(nome, "u.v =", dot(u, v), "|u|^2 =", norma2(u), "v1 =", fr(v1), "v2 =", fr(v2),
          "v2.u =", dot(v2, u), "v1+v2 =", fr(add(v1, v2)))
# distratores 9a
u, v = casos["a"]
k = F(dot(u, v), norma2(v)); pv = esc(k, v)
print("9a proj de u sobre v:", fr(pv), " v - isso:", fr(sub(v, pv)))
v1, v2 = decomp(u, v)
print("9a v1 - v:", fr(sub(v1, v)))
print("9a sem dividir: v1 =", fr(esc(dot(u, v), u)), " v2 =", fr(sub(v, esc(dot(u, v), u))))
print("9a u.v errado = 5: v1 =", fr(esc(F(5, 14), u)), " v2 =", fr(sub(v, esc(F(5, 14), u))))
# distratores 9b
u, v = casos["b"]
k = F(dot(u, v), norma2(v)); pv = esc(k, v)
print("9b proj de u sobre v:", fr(pv), " v - isso:", fr(sub(v, pv)))
print("9b sem dividir: v1 =", fr(esc(dot(u, v), u)), " v2 =", fr(sub(v, esc(dot(u, v), u))))
print("9b dividindo por |v|^2 = 14: v1 =", fr(esc(F(4, 14), u)), " v2 =", fr(sub(v, esc(F(4, 14), u))))
print("9b u.v errado = 6: v1 =", fr(esc(F(6, 3), u)), " v2 =", fr(sub(v, esc(F(6, 3), u))))
# distratores 9c
u, v = casos["c"]
print("9c sinal perdido: v1 =", fr(esc(F(15, 5), u)), " v2 =", fr(sub(v, esc(F(15, 5), u))))
print("9c sem dividir: v1 =", fr(esc(-15, u)), " v2 =", fr(sub(v, esc(-15, u))))
print("9c papeis trocados: v.u =", dot(v, u))

# ---------------- Q10 ----------------
titulo("Q10")
A = (0, 3, -4); B = (3, 0, 5); C = (-1, -1, -2); D = (4, 1, -4)
AB = sub(B, A); CD = sub(D, C)
print("AB =", AB, "CD =", CD, "AB.CD =", dot(AB, CD), "|CD|^2 =", norma2(CD), "|AB|^2 =", norma2(AB))
proj = esc(F(dot(AB, CD), norma2(CD)), CD)
print("proj_CD AB =", fr(proj))
print("proj_AB CD =", fr(esc(F(dot(AB, CD), norma2(AB)), AB)))
print("com BA:", fr(esc(F(dot(sub(A, B), CD), norma2(CD)), CD)))
print("sem dividir:", fr(esc(dot(AB, CD), CD)))
print("|CD|^2 errado (25+4-4=25):", fr(esc(F(dot(AB, CD), 25), CD)))
DC = sub(C, D)
print("proj sobre DC:", fr(esc(F(dot(AB, DC), norma2(DC)), DC)))
print("AB - proj, perpendicular a CD?", fr(sub(AB, proj)), dot(sub(AB, proj), CD))
print("ponta da proj a partir de C:", [float(x) for x in add(C, proj)], " C+AB:", add(C, AB))

# ---------------- Q11 ----------------
titulo("Q11")
M = (-1, 2, -3); N = (-3, 1, 2); P = (1, 1, 2)
MN = sub(N, M); MP = sub(P, M)
cr = cross(MN, MP)
print("MN", MN, "MP", MP, "MN x MP", cr, "|.|^2", norma2(cr), "=16*26?", 16 * 26)
print("area MNP = |.|/2 =", math.sqrt(norma2(cr)) / 2, " 2*sqrt(26) =", 2 * math.sqrt(26))
Av = sub(add(M, P), N); Bv = sub(add(M, N), P); Cv = sub(add(N, P), M)
print("vertices A, B, C:", Av, Bv, Cv)
print("medios:", esc(F(1, 2), add(Av, Bv)), esc(F(1, 2), add(Bv, Cv)), esc(F(1, 2), add(Cv, Av)))
cr2 = cross(sub(Bv, Av), sub(Cv, Av))
print("AB x AC", cr2, "|.|^2", norma2(cr2), "area ABC", math.sqrt(norma2(cr2)) / 2, " 8*sqrt(26) =", 8 * math.sqrt(26))
# distrator: segunda coordenada com sinal errado (10 - 10 = 0)
print("produto com 2a coord zerada: (0, 0, 4) -> area MNP 2 -> ABC 8")
print("16*sqrt(26) =", 16 * math.sqrt(26), " 4*sqrt(26) =", 4 * math.sqrt(26))

# ---------------- Q12 ----------------
titulo("Q12")
nu, nv, th = 2, 3, math.radians(120)
uv = nu * nv * math.cos(th)
print("u.v =", uv)
print("|u x v| =", nu * nv * math.sin(th), " 3*sqrt(3) =", 3 * math.sqrt(3))
print("|u+v|^2 =", nu ** 2 + nv ** 2 + 2 * uv, " |u+v| =", math.sqrt(nu ** 2 + nv ** 2 + 2 * uv))
print("distratores c: sem 2 ->", nu ** 2 + nv ** 2 + uv, " sinal + ->", nu ** 2 + nv ** 2 - 2 * uv)
# coordenadas da figura
U = (2.0, 0.0, 0.0); V = (3 * math.cos(th), 3 * math.sin(th), 0.0)
print("V =", [round(x, 3) for x in V], " U+V =", [round(x, 3) for x in add(U, V)], " norma", math.sqrt(norma2(add(U, V))))
VmU = sub(V, U)
print("V - U =", [round(x, 3) for x in VmU], " |V-U|^2 =", norma2(VmU))
print("|U x (V-U)| =", math.sqrt(norma2(cross(U, VmU))), " |U x V| =", math.sqrt(norma2(cross(U, V))))
print("U.V numerico =", dot(U, V))
print("distratores d: 3sqrt3 - 4 =", 3 * math.sqrt(3) - 4, " 2*sqrt(19) =", 2 * math.sqrt(19),
      " |v|-|u| com sen120 ->", 2 * 1 * math.sin(th))
print("|v-u| real =", math.sqrt(norma2(VmU)), " sqrt(19) =", math.sqrt(19))
print("Excel SEN(120) em radianos:", math.sin(120), " 6*SEN(120):", 6 * math.sin(120), " ACOS(0,8) rad:", math.acos(0.8))

# ---------------- conferencias citadas nos textos ----------------
titulo("Conferencias dos textos")
u3 = (1, 2, 3); v3 = (-1, 0, 3); w3 = (-1, -1, -1)
print("Q3 produto misto u.(v x w) =", dot(u3, cross(v3, w3)), "(diferente de zero: nao coplanares)")
print("Q3 atalho, r.v das alternativas:", [dot(c, v3) for c in [(1, -2, 3), (11, -10, 1), (-6, -8, 2), (2, -1, -2), (-1, 2, -3)]])
print("Q3 atalho, r.w das alternativas:", [dot(c, w3) for c in [(11, -10, 1), (2, -1, -2), (-1, 2, -3)]])
a = (1, 0, 0); b = (1, 0, 0); c = (0, 0, 0)
s = add(add(a, b), c)
print("Q4 confira: |soma|^2 =", norma2(s), " soma normas2 =", norma2(a) + norma2(b) + norma2(c), " 2u.v =", 2 * dot(a, b))
print("Q4 cotidiano sqrt(17) =", math.sqrt(17))
print("Q5b atalho: sqrt(17)/4 =", math.sqrt(17) / 4, " sqrt(2)/2 =", math.sqrt(2) / 2)
print("Q8 tg: atan(3/4) =", math.degrees(math.atan(0.75)), " atan(4/3) =", math.degrees(math.atan(4 / 3)))
print("Q8 0,6435 rad em graus:", math.degrees(0.6435))
ua = (-1, 2, 3); va = (2, 0, 1)
for v1, v2 in [((F(2, 5), 0, F(1, 5)), (F(8, 5), 0, F(4, 5))), ((-1, 2, 3), (3, -2, -2)),
               ((F(-1, 14), F(1, 7), F(3, 14)), (F(29, 14), F(-1, 7), F(11, 14))),
               ((F(-1, 14), F(1, 7), F(3, 14)), (F(-29, 14), F(1, 7), F(-11, 14))),
               ((F(-5, 14), F(5, 7), F(15, 14)), (F(33, 14), F(-5, 7), F(-1, 14)))]:
    print("Q9a alt: v1+v2 =", fr(add(v1, v2)), " v2.u =", dot(v2, ua), " v1 x u =", fr(cross(v1, ua)))
ub = (1, 1, 1)
for v2 in [(F(-5, 7), F(10, 7), F(15, 7)), (-5, -2, -1), (F(-9, 7), F(12, 7), F(19, 7)), (-3, 0, 1), (F(-7, 3), F(2, 3), F(5, 3))]:
    print("Q9b soma coords v2 =", sum(v2), " v2.u =", dot(v2, ub))
print("Q9c v2 errado (-6,-12,0).u =", dot((-6, -12, 0), (1, 2, 0)))
CD = (5, 2, -2)
for alt in [(F(-3, 11), F(3, 11), F(-9, 11)), (F(15, 11), F(6, 11), F(-6, 11)), (-45, -18, 18), (F(-15, 11), F(-6, 11), F(6, 11)), (F(-9, 5), F(-18, 25), F(18, 25))]:
    print("Q10 alt", fr(alt), " x CD =", fr(cross(alt, CD)), "(nulo = multiplo de CD)", " fator x/5 =", alt[0] / 5)
print("Q10 fator decimal:", -3 / 11)
print("Q10 confira: 240 - 54 - 186 =", 240 - 54 - 186)
print("Q12 Lagrange b: 4*9 - 9 =", 4 * 9 - 9, " sqrt(27) =", math.sqrt(27))
print("Q12 confira c: (1/2)^2 + (3sqrt3/2)^2 =", 0.25 + 27 / 4, " lei dos cossenos:", 4 + 9 - 2 * 2 * 3 * math.cos(math.radians(60)))
print("Q12 d: |v-u|^2 = 9 + 6 + 4 =", 9 + 6 + 4, " u.(v-u) =", -3 - 4, " 4*19 - 49 =", 4 * 19 - 49)
print("Q12 a figura: sombra de v em u =", 3 * math.cos(math.radians(120)), " 2 * sombra =", 2 * 3 * math.cos(math.radians(120)))
print("Q12 altura 3 sen120 =", 3 * math.sin(math.radians(120)))
print("Q12 sqrt(7), sqrt(10), sqrt(13), sqrt(19):", math.sqrt(7), math.sqrt(10), math.sqrt(13), math.sqrt(19))
