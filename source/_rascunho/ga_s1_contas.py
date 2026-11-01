# -*- coding: utf-8 -*-
# Confere as contas do lote ga_s1 (Lista 1 de Geometria Analitica, Semana 1).
# Refaz a resposta certa, cada alternativa errada (a conta descrita no "erro"),
# as contas citadas nos jeitos e as coordenadas das figuras. Depois abre os
# JSON gerados e confere o texto da alternativa certa, a copia da Q3,
# a distribuicao das letras e bytes de controle.
# Uso: python -I ga_s1_contas.py
import json, math, os, sys
from fractions import Fraction as Fr

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
GER = os.path.dirname(AQUI)
DADOS = os.path.join(GER, "dados")

falhas = []
n_ok = 0


def chk(nome, cond):
    global n_ok
    if cond:
        n_ok += 1
    else:
        falhas.append(nome)
        print("FALHA", nome)


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def k(e, a):
    return tuple(e * x for x in a)


def n2(a):
    return sum(x * x for x in a)


def perto(a, b, tol=1e-9):
    return len(a) == len(b) and all(abs(x - y) < tol for x, y in zip(a, b))


ZERO2 = (0, 0)

# ---------------- Q1 ----------------
u = (1, 1, -1); v = (2, 3, 4); w = (1, 2, -4)
chk("1a certa", add(u, w) == (2, 3, -5))
chk("1a A u-w", sub(u, w) == (0, -1, 3))
chk("1a C u+v", add(u, v) == (3, 4, 3))
chk("1a D sinal do z", (u[0] + w[0], u[1] + w[1], u[2] + abs(w[2])) == (2, 3, 3))
chk("1a E produto", tuple(a * b for a, b in zip(u, w)) == (1, 2, 4))
chk("1a confira volta", sub((2, 3, -5), w) == u)
chk("1a confira soma coords", sum((2, 3, -5)) == 0 and sum(u) == 1 and sum(w) == -1)

p = add(k(-1, u), v)
chk("1b parentese", p == (1, 2, 5))
chk("1b 3w", k(3, w) == (3, 6, -12))
chk("1b certa", sub(p, k(3, w)) == (-2, -4, 17))
chk("1b A somou 3w", add(p, k(3, w)) == (4, 8, -7))
chk("1b B sem menos em u", sub(add(u, v), k(3, w)) == (0, -2, 15))
chk("1b C 5-12", (p[0] - 3 * w[0], p[1] - 3 * w[1], p[2] - 12) == (-2, -4, -7))
chk("1b E sem o 3", sub(p, w) == (0, 0, 9))
chk("1b confira direto", (-1 + 2 - 3, -1 + 3 - 6, 1 + 4 + 12) == (-2, -4, 17))

chk("1c parentese", sub(w, u) == (0, 1, -3))
chk("1c certa", sub(k(2, v), k(3, sub(w, u))) == (4, 3, 17))
chk("1c B ordem invertida", sub(k(2, v), k(3, sub(u, w))) == (4, 9, -1))
chk("1c C so w vezes 3", add(sub(k(2, v), k(3, w)), u) == (2, 1, 19))
chk("1c D sinal de u", sub(sub(k(2, v), k(3, w)), k(3, u)) == (-2, -3, 23))
chk("1c E sem o 2", sub(v, k(3, sub(w, u))) == (2, 0, 13))
chk("1c confira aberto", add(sub(k(2, v), k(3, w)), k(3, u)) == (4, 3, 17))

q = sub(u, k(2, v))
chk("1d parentese", q == (-3, -5, -9))
chk("1d certa", sub(w, q) == (4, 7, 5))
chk("1d A troca pela metade", sub(sub(w, u), k(2, v)) == (-4, -5, -11))
chk("1d B sem o 2", add(sub(w, u), v) == (2, 4, 1))
chk("1d C ordem invertida", sub(q, w) == (-4, -7, -5))
chk("1d D z errado", (w[0] - q[0], w[1] - q[1], w[2] + q[2]) == (4, 7, -13))
chk("1d confira", add((4, 7, 5), q) == w)
chk("1d conversa z", -4 - (-1) + 8 == 5)

# ---------------- Q2 ----------------
u1 = (-1, -2, 3); u2 = (2, 1, 2); u3 = (-1, 2, 1)
vv = add(u1, u2, u3)
chk("2 certa", vv == (0, 1, 6))
chk("2 equacao fecha", sub(add(u1, u2), sub(vv, u3)) == (0, 0, 0))
chk("2 A", sub(add(u1, u2), u3) == (2, -3, 4))
chk("2 B", k(-1, vv) == (0, -1, -6))
chk("2 D", add(u1, u2) == (1, -1, 5))
chk("2 E", sub(sub(u3, u1), u2) == (-2, 3, -4))
for nome, d in [("A", (2, -3, 4)), ("B", (0, -1, -6)), ("D", (1, -1, 5)), ("E", (-2, 3, -4))]:
    chk("2 " + nome + " nao satisfaz", sub(add(u1, u2), sub(d, u3)) != (0, 0, 0))
chk("2 confira v-u3", sub(vv, u3) == (1, -1, 5))
chk("2 figura cadeia", add(u1) == (-1, -2, 3) and add(u1, u2) == (1, -1, 5) and add(u1, u2, u3) == (0, 1, 6))

# ---------------- Q3 ----------------
A3 = (1, 1, 3); B3 = (-3, 1, 5); AB3 = sub(B3, A3)
chk("3 AB", AB3 == (-4, 0, 2))
chk("3 certa", add(A3, k(3, AB3)) == (-11, 1, 9))
chk("3 A dobro", add(A3, k(2, AB3)) == (-7, 1, 7) and add(B3, AB3) == (-7, 1, 7))
chk("3 B de B", add(B3, k(3, AB3)) == (-15, 1, 11))
chk("3 D sentido", sub(A3, k(3, AB3)) == (13, 1, -3))
chk("3 E vetor", k(3, AB3) == (-12, 0, 6))

# ---------------- Q4 ----------------
A4 = (1, -2, 3); B4 = (1, 1, -3); C4 = (-1, 1, -2)
D4 = sub(add(A4, C4), B4)
chk("4 certa", D4 == (-1, -2, 4))
chk("4 BC", sub(C4, B4) == (-2, 0, 1) and add(A4, sub(C4, B4)) == D4)
chk("4 paralelogramo AB = DC", sub(B4, A4) == sub(C4, D4))
chk("4 B CB", add(A4, sub(B4, C4)) == (3, -2, 2))
chk("4 C C+AB", add(C4, sub(B4, A4)) == (-1, 4, -8))
mAC = tuple(Fr(a + c, 2) for a, c in zip(A4, C4))
mBD = tuple(Fr(b + d, 2) for b, d in zip(B4, D4))
chk("4 D ponto medio", mAC == (0, Fr(-1, 2), Fr(1, 2)))
chk("4 confira diagonais", mAC == mBD)
chk("4 E z errado", (A4[0] + C4[0] - B4[0], A4[1] + C4[1] - B4[1], 3 + (-2) - 3) == (-1, -2, -2))

# ---------------- Q5 ----------------
A5 = (0, 0, 0); B5 = (3, 0, 0); C5 = (3, 2, 0); D5 = (0, 2, 0)
E5 = (0, 0, 2); F5 = (3, 0, 2); G5 = (3, 2, 2); H5 = (0, 2, 2)
U5 = sub(B5, A5); V5 = sub(D5, A5); W5 = sub(E5, A5)
chk("5 caixa", C5 == add(U5, V5) and F5 == add(U5, W5) and G5 == add(U5, V5, W5) and H5 == add(V5, W5))


def comb(a, b, c):
    return add(k(a, U5), k(b, V5), k(c, W5))


HB = sub(B5, H5)
chk("5a certa", HB == comb(1, -1, -1) and HB == (3, -2, -2))
chk("5a A = BH", comb(-1, 1, 1) == sub(H5, B5))
chk("5a B = AG", comb(1, 1, 1) == sub(G5, A5))
chk("5a C = DF", comb(1, -1, 1) == sub(F5, D5))
chk("5a E = EC", comb(1, 1, -1) == sub(C5, E5))
for t in [(-1, 1, 1), (1, 1, 1), (1, -1, 1), (1, 1, -1)]:
    chk("5a distrator diferente " + str(t), comb(*t) != HB)
CH = sub(H5, C5)
chk("5b certa", CH == comb(-1, 0, 1) and CH == (-3, 0, 2))
chk("5b A = HC", comb(1, 0, -1) == sub(C5, H5))
chk("5b C = BH", comb(-1, 1, 1) == sub(H5, B5))
chk("5b D = AF", comb(1, 0, 1) == sub(F5, A5))
chk("5b E = CE", comb(-1, -1, 1) == sub(E5, C5))
for t in [(1, 0, -1), (-1, 1, 1), (1, 0, 1), (-1, -1, 1)]:
    chk("5b distrator diferente " + str(t), comb(*t) != CH)

# ---------------- Q6 ----------------
s3 = math.sqrt(3)
P6 = {"B": (0, 2), "A": (s3, 1), "F": (s3, -1), "E": (0, -2), "D": (-s3, -1), "C": (-s3, 1), "O": (0, 0)}


def V6(par):
    return sub(P6[par[1]], P6[par[0]])


ordem = ["B", "A", "F", "E", "D", "C"]
for i in range(6):
    a, b = ordem[i], ordem[(i + 1) % 6]
    chk("6 lado " + a + b + " = 2", abs(math.sqrt(n2(V6(a + b))) - 2) < 1e-9)
    chk("6 raio " + a + " = 2", abs(math.sqrt(n2(P6[a])) - 2) < 1e-9)

s6a = add(V6("AB"), V6("BE"), V6("EF"), V6("FC"))
chk("6a certa AC", perto(s6a, V6("AC")))
chk("6a AF = AB+BE+EF", perto(add(V6("AB"), V6("BE"), V6("EF")), V6("AF")))
chk("6a BC = BE+EF+FC", perto(add(V6("BE"), V6("EF"), V6("FC")), V6("BC")))
for d in [V6("CA"), V6("AF"), ZERO2, V6("BC")]:
    chk("6a distrator diferente", not perto(d, s6a))
chk("6a confira setas", perto(V6("AB"), (-s3, 1)) and perto(V6("BE"), (0, -4)) and perto(V6("EF"), (s3, 1)) and perto(V6("FC"), (-2 * s3, 2)))
chk("6a confira soma", perto(s6a, (-2 * s3, 0)))

s6b = add(V6("FC"), V6("CD"), V6("DE"), V6("EF"))
chk("6b certa zero", perto(s6b, ZERO2))
chk("6b FE", perto(add(V6("FC"), V6("CD"), V6("DE")), V6("FE")))
chk("6b CF", perto(add(V6("CD"), V6("DE"), V6("EF")), V6("CF")))
chk("6b FD", perto(add(V6("FC"), V6("CD")), V6("FD")))
for d in [V6("FE"), k(2, V6("FC")), V6("CF"), V6("FD")]:
    chk("6b distrator diferente", not perto(d, s6b))
chk("6b confira setas", perto(V6("CD"), (0, -2)) and perto(V6("DE"), (s3, -1)))

s6c = add(V6("DC"), V6("CB"), V6("BA"), V6("AF"), V6("FE"))
chk("6c certa DE", perto(s6c, V6("DE")))
chk("6c DF", perto(add(V6("DC"), V6("CB"), V6("BA"), V6("AF")), V6("DF")))
chk("6c CE", perto(add(V6("CB"), V6("BA"), V6("AF"), V6("FE")), V6("CE")))
chk("6c volta completa", perto(add(s6c, V6("ED")), ZERO2))
for d in [V6("ED"), V6("DF"), ZERO2, V6("CE")]:
    chk("6c distrator diferente", not perto(d, s6c))

s6d = add(V6("CB"), V6("AB"), V6("AF"), V6("OE"))
chk("6d certa AF", perto(s6d, V6("AF")))
chk("6d AF = OE", perto(V6("AF"), V6("OE")))
chk("6d AB = OC", perto(V6("AB"), V6("OC")))
chk("6d OC + CB = OB", perto(add(V6("OC"), V6("CB")), V6("OB")))
chk("6d CB + AB = OB", perto(add(V6("CB"), V6("AB")), V6("OB")))
chk("6d OB + OE = 0", perto(add(V6("OB"), V6("OE")), ZERO2))
chk("6d losango OABC", perto(V6("OA"), V6("CB")) and all(abs(math.sqrt(n2(V6(x))) - 2) < 1e-9 for x in ["OA", "AB", "BC", "CO"]))
chk("6d A: sem OE da zero", perto(add(V6("CB"), V6("AB"), V6("AF")), ZERO2))
chk("6d B: AF + OE = BE", perto(add(V6("AF"), V6("OE")), V6("BE")))
chk("6d C: CB + AB = OB", perto(add(V6("CB"), V6("AB")), V6("OB")))
for d in [ZERO2, V6("BE"), V6("OB"), V6("CE")]:
    chk("6d distrator diferente", not perto(d, s6d))
chk("6d confira", perto(V6("CB"), (s3, 1)) and perto(V6("AB"), (-s3, 1)) and perto(s6d, (0, -2)))

s6e = add(V6("BO"), V6("BA"), V6("FB"))
chk("6e certa zero", perto(s6e, ZERO2))
chk("6e FO", perto(add(V6("FB"), V6("BO")), V6("FO")))
chk("6e FA", perto(add(V6("FB"), V6("BA")), V6("FA")))
chk("6e FA = -BO", perto(V6("FA"), k(-1, V6("BO"))))
chk("6e BE = 2BO", perto(k(2, V6("BO")), V6("BE")))
chk("6e BO + BA = BF", perto(add(V6("BO"), V6("BA")), V6("BF")))
chk("6e com BF dobra", perto(add(V6("BO"), V6("BA"), V6("BF")), k(2, V6("BF"))))
for d in [V6("FO"), V6("FA"), V6("BE"), k(2, V6("BF"))]:
    chk("6e distrator diferente", not perto(d, s6e))
chk("6e confira", perto(V6("BO"), (0, -2)) and perto(V6("BA"), (s3, -1)) and perto(V6("FB"), (-s3, 3)))

# ---------------- Q7 ----------------
W7 = (-4, 1, 0)


def lados7(x, y, z):
    u7 = (2, -z, 1); v7 = (-x, 3, y + 2)
    return sub(u7, k(2, v7)), k(3, W7)


x7 = Fr(-12 - 2, 2); z7 = Fr(-(3 + 6)); y7 = Fr(1 - 4, 2)
chk("7 solucao", (x7, y7, z7) == (-7, Fr(-3, 2), -9))
e, d = lados7(x7, y7, z7)
chk("7 certa", e == d == (-12, 3, 0))
chk("7 A: 2 - 2x = -12", 2 - 2 * 7 == -12)
chk("7 B: 1 - (2y+2) = 0", 1 - (2 * Fr(-1, 2) + 2) == 0)
e, d = lados7(-3, Fr(-3, 2), -7)
chk("7 C: igualou a w", e == W7)
chk("7 E: z - 6 = 3", 9 - 6 == 3)
for t in [(7, Fr(-3, 2), -9), (-7, Fr(-1, 2), -9), (-3, Fr(-3, 2), -7), (-7, Fr(-3, 2), 9)]:
    e, d = lados7(*t)
    chk("7 distrator falha " + str(t), e != d)
chk("7 confira u e v", (2, 9, 1) == (2, -z7, 1) and (7, 3, Fr(1, 2)) == (-x7, 3, y7 + 2))
chk("7 atalho y+2", y7 + 2 == Fr(1, 2))

# ---------------- Q8 ----------------
u8 = (-2, 1, -2); v8 = (1, 2, 1); w8 = (-3, 2, 0)
r8 = sub(sub(k(5, v8), k(2, w8)), u8)
chk("8a certa", r8 == (13, 5, 7))
chk("8a equacao", add(sub(u8, k(2, v8)), r8) == sub(k(3, v8), k(2, w8)) == (9, 2, 3))
chk("8a receita", k(5, v8) == (5, 10, 5) and k(2, w8) == (-6, 4, 0) and sub(k(5, v8), k(2, w8)) == (11, 6, 5))
chk("8a A", sub(sub(v8, k(2, w8)), u8) == (9, -3, 3))
chk("8a C", add(sub(k(5, v8), k(2, w8)), u8) == (9, 7, 3))
chk("8a D", sub(add(k(5, v8), k(2, w8)), u8) == (1, 13, 7))
chk("8a E", sub(sub(k(3, v8), k(2, w8)), u8) == (11, 1, 5))


def det3(m):
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def cramer(m, b):
    dt = Fr(det3(m))
    res = []
    for j in range(3):
        mj = [list(row) for row in m]
        for i in range(3):
            mj[i][j] = b[i]
        res.append(Fr(det3(mj)) / dt)
    return tuple(res)


linhas = [[u8[i], v8[i], w8[i]] for i in range(3)]
alvo = (2, -3, 1)
sol = cramer(linhas, alvo)
chk("8b certa", sol == (Fr(-13, 15), Fr(-11, 15), Fr(-1, 3)))
chk("8b combinacao", add(k(sol[0], u8), k(sol[1], v8), k(sol[2], w8)) == alvo)


def eqs(a):
    return tuple(sum(linhas[i][j] * a[j] for j in range(3)) for i in range(3))


chk("8b A alvo (2,3,1)", cramer(linhas, (2, 3, 1)) == (Fr(1, 3), Fr(5, 3), Fr(-1, 3)))
bB = (Fr(-17, 15), Fr(-19, 15), Fr(1, 3))
chk("8b B eq2 e eq3 com a3 = 1/3", eqs(bB)[1] == -3 and eqs(bB)[2] == 1 and eqs(bB)[0] != 2)
a1B = Fr(-3 - 2 - Fr(2, 3), 5)
chk("8b B caminho 3a3 = 1", a1B == Fr(-17, 15) and 1 + 2 * a1B == Fr(-19, 15))
bC = (0, 1, Fr(-1, 3))
chk("8b C eq1 e eq3 ok, eq2 = 4/3", eqs(bC)[0] == 2 and eqs(bC)[2] == 1 and eqs(bC)[1] == Fr(4, 3))
transp = [list(u8), list(v8), list(w8)]
chk("8b D transposto", cramer(transp, alvo) == (Fr(-13, 15), Fr(-4, 5), Fr(-8, 15)))
for t in [(Fr(1, 3), Fr(5, 3), Fr(-1, 3)), bB, bC, (Fr(-13, 15), Fr(-4, 5), Fr(-8, 15))]:
    chk("8b distrator falha " + str(t), eqs(t) != alvo)
chk("8b receita a3", Fr(2 - 1, -3) == Fr(-1, 3))
chk("8b receita 5a1", -3 - 2 + Fr(2, 3) == Fr(-13, 3))
chk("8b receita a2", 1 + 2 * Fr(-13, 15) == Fr(-11, 15))
chk("8b confira 1", Fr(26, 15) - Fr(11, 15) + Fr(15, 15) == 2)
chk("8b confira 2", Fr(-13, 15) - Fr(22, 15) - Fr(10, 15) == -3)
chk("8b confira 3", Fr(26, 15) - Fr(11, 15) == 1)
chk("8b atalho eq2 elimina A e C", eqs((Fr(1, 3), Fr(5, 3), Fr(-1, 3)))[1] != -3 and eqs(bC)[1] != -3)

# ---------------- Q9 ----------------
ua = (-2, 1, -2)
chk("9a certa", n2(ua) == 9 and math.isqrt(9) == 3)
chk("9a C soma", sum(ua) == -3)
chk("9a D duas coords", n2(ua[:2]) == 5)
chk("9a E abs", sum(abs(x) for x in ua) == 5)
chk("9a confira versor", n2(tuple(Fr(x, 3) for x in ua)) == 1)
chk("9a visual", n2((-2, 1, 0)) == 5 and 5 + 4 == 9)
r2 = 1 / math.sqrt(2)
vb = (0, r2, r2)
chk("9b certa", abs(n2(vb) - 1) < 1e-12)
chk("9b A soma", abs(sum(vb) - math.sqrt(2)) < 1e-12)
chk("9b B 1/4+1/4 com raiz", abs(math.sqrt(0.25 + 0.25) - r2) < 1e-12)
chk("9b C 1/4+1/4 sem raiz", 0.25 + 0.25 == 0.5)
chk("9b E (raiz2)^2 + (raiz2)^2 = 4", abs(math.sqrt(2) ** 2 + math.sqrt(2) ** 2 - 4) < 1e-12)
chk("9b 0,7071", abs(r2 - 0.7071) < 0.0001)
chk("9b atalho n=2", 2 * Fr(1, 2) == 1)
sq6 = [Fr(1, 6), Fr(1, 6), Fr(4, 6)]
chk("9c certa", sum(sq6) == 1)
chk("9c A soma", (1 - 1 - 2) == -2)
chk("9c B numeradores", 1 + 1 + 4 == 6)
chk("9c D 2/6", Fr(1, 6) + Fr(1, 6) + Fr(2, 6) == Fr(2, 3))
chk("9c E abs", 1 + 1 + 2 == 4)
wc = (1 / math.sqrt(6), -1 / math.sqrt(6), -2 / math.sqrt(6))
chk("9c float", abs(n2(wc) - 1) < 1e-12)
sq3 = [Fr(1, 3), Fr(1, 3), Fr(4, 3)]
chk("9d certa", sum(sq3) == 2)
chk("9d D 2/3", Fr(1, 3) + Fr(1, 3) + Fr(2, 3) == Fr(4, 3))
chk("9d raiz6/raiz3", abs(math.sqrt(6) / math.sqrt(3) - math.sqrt(2)) < 1e-12)
chk("9d 1,41", abs(math.sqrt(2) - 1.41) < 0.005)
for g in [0, 17, 30, 45, 60, 90, 133, 250]:
    t = math.radians(g)
    chk("9e cos2+sen2 " + str(g), abs(math.cos(t) ** 2 + math.sin(t) ** 2 - 1) < 1e-12)
chk("9e 60 graus", Fr(1, 4) + Fr(3, 4) == 1)
chk("9e cos+sen varia", abs((math.cos(0) + math.sin(0)) - (math.cos(math.radians(45)) + math.sin(math.radians(45)))) > 0.1)
normas = {"u": 9, "v": 1, "w": 1, "r": 2, "s": 1}
chk("9e unitarios v w s", sorted(x for x, n in normas.items() if n == 1) == ["s", "v", "w"])

# ---------------- Q10 ----------------
P = (-2, 1, -2); Q = (1, 2, 1); R = (-3, 2, 0)
chk("10a certa", sub(Q, P) == (3, 1, 3) and n2(sub(Q, P)) == 19)
chk("10a A soma", add(P, Q) == (-1, 3, -1) and n2(add(P, Q)) == 11)
chk("10a C", sum(abs(x) for x in sub(Q, P)) == 7)
chk("10a E sem sinal", (1 - 2, 2 - 1, 1 - 2) == (-1, 1, -1) and n2((-1, 1, -1)) == 3)
chk("10a confira", n2(sub(P, Q)) == 19)
chk("10a 4,3", 4.3 < math.sqrt(19) < 4.4)
chk("10a atalho", 3 < math.sqrt(11) < 7 and 3 < math.sqrt(19) < 7 and math.sqrt(3) < 3 and 9 + 9 == 18)
chk("10b certa", sub(R, P) == (-1, 1, 2) and n2(sub(R, P)) == 6)
chk("10b A soma", add(R, P) == (-5, 3, -2) and n2(add(R, P)) == 38)
chk("10b B abs", sum(abs(x) for x in sub(R, P)) == 4)
chk("10b C x errado", n2((-3 - 2, 1, 2)) == 30)
chk("10b E sem z", n2((-1, 1)) == 2)
chk("10b decimais", round(math.sqrt(6), 2) == 2.45 and round(math.sqrt(38), 1) == 6.2 and round(math.sqrt(30), 1) == 5.5 and round(math.sqrt(2), 1) == 1.4)
chk("10c certa", sub(Q, R) == (4, 0, 1) and n2(sub(Q, R)) == 17)
chk("10c A x errado", n2((1 - 3, 0, 1)) == 5)
chk("10c D abs", sum(abs(x) for x in sub(Q, R)) == 5)
chk("10c E soma", add(R, Q) == (-2, 4, 1) and n2(add(R, Q)) == 21)
chk("10c decimais", round(math.sqrt(17), 2) == 4.12 and round(math.sqrt(5), 2) == 2.24)

# ---------------- JSON gerados ----------------
M = "−"
esperado = {
    "ga-s1-l1q1a": "(2, 3, " + M + "5)",
    "ga-s1-l1q1b": "(" + M + "2, " + M + "4, 17)",
    "ga-s1-l1q1c": "(4, 3, 17)",
    "ga-s1-l1q1d": "(4, 7, 5)",
    "ga-s1-l1q2": "(0, 1, 6)",
    "ga-s1-l1q3": "(" + M + "11, 1, 9)",
    "ga-s1-l1q4": "(" + M + "1, " + M + "2, 4)",
    "ga-s1-l1q5a": "[[u]] " + M + " [[v]] " + M + " [[w]]",
    "ga-s1-l1q5b": M + "[[u]] + [[w]]",
    "ga-s1-l1q6a": "[[AC]]",
    "ga-s1-l1q6b": "[[0]] (vetor nulo)",
    "ga-s1-l1q6c": "[[DE]]",
    "ga-s1-l1q6d": "[[AF]]",
    "ga-s1-l1q6e": "[[0]] (vetor nulo)",
    "ga-s1-l1q7": "x = " + M + "7, y = " + M + "3/2, z = " + M + "9",
    "ga-s1-l1q8a": "(13, 5, 7)",
    "ga-s1-l1q8b": "a₁ = " + M + "13/15, a₂ = " + M + "11/15, a₃ = " + M + "1/3",
    "ga-s1-l1q9a": "3",
    "ga-s1-l1q9b": "1",
    "ga-s1-l1q9c": "1",
    "ga-s1-l1q9d": "√2, não é unitário",
    "ga-s1-l1q9e": "‖[[s]]‖ = 1; unitários: [[v]], [[w]] e [[s]]",
    "ga-s1-l1q10a": "√19",
    "ga-s1-l1q10b": "√6",
    "ga-s1-l1q10c": "√17",
}
niveis = {"ga-s1-l1q1a": 1, "ga-s1-l1q1b": 1, "ga-s1-l1q1c": 2, "ga-s1-l1q1d": 2, "ga-s1-l1q2": 2,
          "ga-s1-l1q4": 2, "ga-s1-l1q5a": 2, "ga-s1-l1q5b": 2, "ga-s1-l1q6a": 2, "ga-s1-l1q6b": 1,
          "ga-s1-l1q6c": 2, "ga-s1-l1q6d": 3, "ga-s1-l1q6e": 3, "ga-s1-l1q7": 2, "ga-s1-l1q8a": 2,
          "ga-s1-l1q8b": 3, "ga-s1-l1q9a": 1, "ga-s1-l1q9b": 1, "ga-s1-l1q9c": 1, "ga-s1-l1q9d": 1,
          "ga-s1-l1q9e": 2, "ga-s1-l1q10a": 1, "ga-s1-l1q10b": 1, "ga-s1-l1q10c": 1}

arquivos = sorted(f for f in os.listdir(DADOS) if f.startswith("ga_s1_p") and f.endswith(".json"))
print("arquivos:", arquivos)
questoes = {}
letras = {}
for nome in arquivos:
    caminho = os.path.join(DADOS, nome)
    with open(caminho, "rb") as fh:
        bruto = fh.read()
    ctrl = [b for b in bruto if b < 32 and b not in (9, 10, 13)]
    chk("sem bytes de controle em " + nome, not ctrl)
    dado = json.loads(bruto.decode("utf-8"))
    chk("disciplina ga em " + nome, dado.get("disciplina") == "ga")
    chk("ate 6 questoes em " + nome, len(dado["questoes"]) <= 6)
    for qq in dado["questoes"]:
        questoes[qq["id"]] = qq
        certas = [i for i, a in enumerate(qq["alternativas"]) if a.get("certa") is True]
        letras[qq["id"]] = "ABCDE"[certas[0]]
with open(os.path.join(AQUI, "ga_s1_contas.py"), "rb") as fh:
    chk("sem bytes de controle no .py", not [b for b in fh.read() if b < 32 and b not in (9, 10, 13)])

chk("25 questoes", len(questoes) == 25)
chk("ids esperados", sorted(questoes) == sorted(esperado))
for qid, txt in esperado.items():
    qq = questoes.get(qid)
    if qq is None:
        chk("existe " + qid, False)
        continue
    certa = [a["t"] for a in qq["alternativas"] if a.get("certa") is True][0]
    chk("texto da certa " + qid, certa == txt)
    if qid in niveis:
        chk("nivel " + qid, qq["nivel"] == niveis[qid])
    chk("semana 1 " + qid, qq["semana"] == 1)

with open(os.path.join(GER, "exemplos.json"), encoding="utf-8") as fh:
    ex = json.load(fh)
q3ex = [qq for qq in ex["questoes"] if qq["id"] == "ga-s1-l1q3"][0]
chk("Q3 identica ao exemplo", questoes.get("ga-s1-l1q3") == q3ex)

contagem = {}
for l in letras.values():
    contagem[l] = contagem.get(l, 0) + 1
print("letras das certas:", dict(sorted(contagem.items())))
chk("nenhuma letra acima de 30%", all(c / 25 <= 0.30 for c in contagem.values()))

# figuras: rotulos dos pontos e setas conferem com as coordenadas
def rotulo(coord, mapa, tol=0.01):
    for nome, c in mapa.items():
        if perto(tuple(coord), tuple(c), tol):
            return nome
    return None


P6fig = {n: (round(c[0], 3), round(c[1], 3)) for n, c in P6.items()}
setas6 = {"ga-s1-l1q6a": ["AB", "BE", "EF", "FC"], "ga-s1-l1q6b": ["FC", "CD", "DE", "EF"],
          "ga-s1-l1q6c": ["DC", "CB", "BA", "AF", "FE"], "ga-s1-l1q6d": ["CB", "AB", "AF", "OE"],
          "ga-s1-l1q6e": ["BO", "BA", "FB"]}
for qid, esperadas in setas6.items():
    fig = questoes[qid]["figura"]
    chk(qid + " figura no enunciado 2d", fig["onde"] == "enunciado" and fig["modo"] == "2d")
    achadas = []
    for it in fig["itens"]:
        if it["tipo"] == "ponto":
            chk(qid + " ponto " + it["rot"], rotulo(it["em"], P6fig) == it["rot"])
        elif it["tipo"] == "vetor":
            chk(qid + " seta cor 2", it.get("cor") == 2)
            achadas.append(rotulo(it["de"], P6fig) + rotulo(it["ate"], P6fig))
        elif it["tipo"] == "poligono":
            chk(qid + " poligono cor 3", it.get("cor") == 3)
            chk(qid + " poligono = hexagono", [rotulo(pt, P6fig) for pt in it["pts"]] == ordem)
    chk(qid + " setas " + str(achadas), achadas == esperadas)
    pts_o = [it for it in fig["itens"] if it["tipo"] == "ponto" and it["rot"] == "O"]
    chk(qid + " ponto O so em d e e", bool(pts_o) == (qid in ("ga-s1-l1q6d", "ga-s1-l1q6e")))

P5fig = {"A": A5, "B": B5, "C": C5, "D": D5, "E": E5, "F": F5, "G": G5, "H": H5}
for qid in ("ga-s1-l1q5a", "ga-s1-l1q5b"):
    fig = questoes[qid]["figura"]
    chk(qid + " figura no enunciado 3d", fig["onde"] == "enunciado" and fig["modo"] == "3d")
    vets = {}
    arestas = set()
    for it in fig["itens"]:
        if it["tipo"] == "ponto":
            chk(qid + " ponto " + it["rot"], rotulo(it["em"], P5fig) == it["rot"])
        elif it["tipo"] == "vetor":
            vets[it["rot"]] = (rotulo(it["de"], P5fig) + rotulo(it["ate"], P5fig), it.get("cor"))
        elif it["tipo"] == "segmento":
            arestas.add("".join(sorted(rotulo(it["de"], P5fig) + rotulo(it["ate"], P5fig))))
    chk(qid + " vetores u v w", vets == {"u": ("AB", 1), "v": ("AD", 2), "w": ("AE", 3)})
    todas = {"AB", "BC", "CD", "AD", "EF", "FG", "GH", "EH", "AE", "BF", "CG", "DH"}
    chk(qid + " arestas", arestas | {"AB", "AD", "AE"} == todas and len(arestas) == 9)
    chk(qid + " nao desenha HB nem CH", not ({"BH", "CH"} & arestas))

fig4 = questoes["ga-s1-l1q4"]["figura"]
P4fig = {"A": A4, "B": B4, "C": C4, "D": D4, "M": (0, -0.5, 0.5)}
for it in fig4["itens"]:
    if it["tipo"] == "ponto":
        chk("4 ponto " + it["rot"], rotulo(it["em"], P4fig) == it["rot"])
    if it["tipo"] == "vetor":
        chk("4 seta " + it["rot"], rotulo(it["de"], P4fig) + rotulo(it["ate"], P4fig) == it["rot"])

fig1 = questoes["ga-s1-l1q1a"]["figura"]
fins = {it["rot"]: tuple(it["ate"]) for it in fig1["itens"] if it["tipo"] == "vetor" and it["rot"]}
chk("1a figura", fins == {"u": u, "w": w, "u + w": (2, 3, -5)})

for qid, de, ate in [("ga-s1-l1q10a", P, Q), ("ga-s1-l1q10b", P, R), ("ga-s1-l1q10c", R, Q)]:
    fig = questoes[qid]["figura"]
    vet = [it for it in fig["itens"] if it["tipo"] == "vetor"][0]
    chk(qid + " seta", tuple(vet["de"]) == de and tuple(vet["ate"]) == ate)
    pts = {it["rot"]: tuple(it["em"]) for it in fig["itens"] if it["tipo"] == "ponto"}
    chk(qid + " pontos", pts == {"P": P, "Q": Q, "R": R})

for qid in ("ga-s1-l1q9b", "ga-s1-l1q9e"):
    fig = questoes[qid]["figura"]
    pol = [it for it in fig["itens"] if it["tipo"] == "poligono"][0]
    chk(qid + " circulo raio 1", all(abs(math.sqrt(n2(pt)) - 1) < 0.002 for pt in pol["pts"]))
vet9b = [it for it in questoes["ga-s1-l1q9b"]["figura"]["itens"] if it["tipo"] == "vetor"][0]
chk("9b seta", perto(tuple(vet9b["ate"]), vb, 0.001))
vet9e = [it for it in questoes["ga-s1-l1q9e"]["figura"]["itens"] if it["tipo"] == "vetor"][0]
chk("9e seta 30 graus", perto(tuple(vet9e["ate"]), (math.cos(math.radians(30)), math.sin(math.radians(30))), 0.001))
vet9a = [it for it in questoes["ga-s1-l1q9a"]["figura"]["itens"] if it["tipo"] == "vetor"][0]
chk("9a seta", tuple(vet9a["ate"]) == ua)

print()
print("conferencias ok:", n_ok, "| falhas:", len(falhas))
print("OK" if not falhas else "FALHOU")
sys.exit(1 if falhas else 0)
