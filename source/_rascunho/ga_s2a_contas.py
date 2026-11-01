# Confere as contas do lote ga_s2a (Lista 2, Q1 a..n) e os distratores.
# Uso: python -I ga_s2a_contas.py
from fractions import Fraction as F
import math

u = (F(1), F(4), F(3))
v = (F(-1), F(1), F(-1))
w = (F(-2), F(-1, 2), F(5))
z = (F(-1), F(2), F(-3))

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])

def comp(a, b):
    return tuple(x * y for x, y in zip(a, b))

def neg(a):
    return tuple(-x for x in a)

def soma(a, b):
    return tuple(x + y for x, y in zip(a, b))

def norma(a):
    return math.sqrt(float(dot(a, a)))

def ang(a, b):
    c = float(dot(a, b)) / (norma(a) * norma(b))
    return math.degrees(math.acos(c)), c

def fmt(x):
    if isinstance(x, tuple):
        return "(" + ", ".join(fmt(t) for t in x) + ")"
    return str(x)

def cruz_sem_menos_meio(a, b):
    # erro: esquece de trocar o sinal do componente do meio
    return (a[1] * b[2] - a[2] * b[1],
            a[0] * b[2] - a[2] * b[0],
            a[0] * b[1] - a[1] * b[0])

ok = True
def confere(nome, obtido, esperado):
    global ok
    bate = obtido == esperado
    ok = ok and bate
    print(("OK   " if bate else "ERRO ") + nome + ": " + fmt(obtido) + ("" if bate else "  esperado " + fmt(esperado)))

print("== Gabarito ==")
confere("a u.v", dot(u, v), F(0))
confere("b u.w", dot(u, w), F(11))
confere("c u.z", dot(u, z), F(-2))
confere("d v.w", dot(v, w), F(-7, 2))
confere("e v.z", dot(v, z), F(6))
confere("f w.z", dot(w, z), F(-14))
confere("g u.u", dot(u, u), F(26))
confere("h v.v", dot(v, v), F(3))
confere("i w.w", dot(w, w), F(117, 4))
confere("j z.z", dot(z, z), F(14))
confere("k uxv", cross(u, v), (F(-7), F(-2), F(5)))
confere("l uxw", cross(u, w), (F(43, 2), F(-11), F(15, 2)))
confere("m vxw", cross(v, w), (F(9, 2), F(7), F(5, 2)))
confere("n wxv", cross(w, v), (F(-9, 2), F(-7), F(-5, 2)))

print("== Distratores ==")
# a
confere("a comp a comp", comp(u, v), (F(-1), F(4), F(-3)))
confere("a sinal no 3o produto", F(-1) + F(4) + F(3), F(6))
confere("a vetorial", cross(u, v), (F(-7), F(-2), F(5)))
# b
confere("b sem sinal da fracao", u[0]*w[0] + u[1]*F(1, 2) + u[2]*w[2], F(15))
confere("b comp a comp", comp(u, w), (F(-2), F(-2), F(15)))
confere("b leu -1/2 como -2", u[0]*w[0] + u[1]*F(-2) + u[2]*w[2], F(5))
confere("b ignorou sinais", sum(abs(x * y) for x, y in zip(u, w)), F(19))
# c
confere("c sinal no 3o produto", F(-1) + F(8) + F(9), F(16))
confere("c comp a comp", comp(u, z), (F(-1), F(8), F(-9)))
confere("c ignorou sinais", sum(abs(x * y) for x, y in zip(u, z)), F(18))
confere("c somou em vez de multiplicar", sum(soma(u, z)), F(6))
# d
confere("d sinal da fracao", v[0]*w[0] + v[1]*F(1, 2) + v[2]*w[2], F(-5, 2))
confere("d comp a comp", comp(v, w), (F(2), F(-1, 2), F(-5)))
confere("d menos com menos deu menos", F(-2) + F(-1, 2) + F(-5), F(-15, 2))
confere("d (-3 - 1)/2", F(-3 - 1, 2), F(-2))
# e
confere("e menos com menos deu menos", F(-1) + F(2) + F(-3), F(-2))
confere("e comp a comp", comp(v, z), (F(1), F(2), F(3)))
confere("e somou em vez de multiplicar", sum(soma(v, z)), F(-3))
confere("e sinal no 3o produto", F(1) + F(2) + F(-3), F(0))
# f
confere("f sinal da fracao", w[0]*z[0] + F(1, 2)*z[1] + w[2]*z[2], F(-12))
confere("f comp a comp", comp(w, z), (F(2), F(-1), F(-15)))
confere("f menos com menos deu menos", F(-2) + F(-1) + F(-15), F(-18))
confere("f somou em vez de multiplicar", sum(soma(w, z)), F(1, 2))
# g
confere("g soma dos componentes", sum(u), F(8))
confere("g soma ao quadrado", sum(u) ** 2, F(64))
confere("g comp a comp", comp(u, u), (F(1), F(16), F(9)))
print("     g norma de u = sqrt(26) =", round(norma(u), 4))
# h
confere("h menos com menos deu menos", F(-1) + F(1) + F(-1), F(-1))
confere("h soma ao quadrado", sum(v) ** 2, F(1))
confere("h comp a comp", comp(v, v), (F(1), F(1), F(1)))
# i
confere("i (-1/2)^2 = -1/4", F(4) + F(-1, 4) + F(25), F(115, 4))
confere("i so o numerador", F(4) + F(1, 2) + F(25), F(59, 2))
confere("i comp a comp", comp(w, w), (F(4), F(1, 4), F(25)))
print("     i norma de w = sqrt(117)/2 =", round(math.sqrt(117) / 2, 4), " sqrt(117/4) =", round(norma(w), 4))
print("     i 117/4 em decimal =", float(F(117, 4)))
# j
confere("j menos com menos deu menos", F(-1) + F(4) + F(-9), F(-6))
confere("j soma ao quadrado", sum(z) ** 2, F(4))
confere("j comp a comp", comp(z, z), (F(1), F(4), F(9)))
# k
confere("k sem menos no meio", cruz_sem_menos_meio(u, v), (F(-7), F(2), F(5)))
confere("k ordem trocada v x u", cross(v, u), (F(7), F(2), F(-5)))
confere("k comp a comp", comp(u, v), (F(-1), F(4), F(-3)))
confere("k escalar", dot(u, v), F(0))
# l
w_mais = (F(-2), F(1, 2), F(5))
confere("l sem menos no meio", cruz_sem_menos_meio(u, w), (F(43, 2), F(11), F(15, 2)))
confere("l comp a comp", comp(u, w), (F(-2), F(-2), F(15)))
confere("l ordem trocada w x u", cross(w, u), (F(-43, 2), F(11), F(-15, 2)))
confere("l copiou +1/2", cross(u, w_mais), (F(37, 2), F(-11), F(17, 2)))
# m
confere("m sem menos no meio", cruz_sem_menos_meio(v, w), (F(9, 2), F(-7), F(5, 2)))
confere("m comp a comp", comp(v, w), (F(2), F(-1, 2), F(-5)))
# erro: nos dois produtos com -1/2, (-1)(-1/2) virou -1/2
mx = v[1] * w[2] - F(-1, 2)          # 5 - (-1/2)
mz = F(-1, 2) - v[1] * w[0]          # -1/2 - (1)(-2)
confere("m (-1)(-1/2) = -1/2", (mx, v[2] * w[0] - v[0] * w[2], mz), (F(11, 2), F(7), F(3, 2)))
confere("m ordem trocada w x v", cross(w, v), (F(-9, 2), F(-7), F(-5, 2)))
# n
confere("n ignorou a ordem", cross(v, w), (F(9, 2), F(7), F(5, 2)))
confere("n sem menos no meio", cruz_sem_menos_meio(w, v), (F(-9, 2), F(7), F(-5, 2)))
confere("n escalar", dot(w, v), F(-7, 2))
confere("n comp a comp", comp(w, v), (F(2), F(-1, 2), F(-5)))
confere("n anticomutatividade", cross(w, v), neg(cross(v, w)))

print("== Detalhes usados nos textos ==")
for nome, a, b in [("u,v", u, v), ("u,w", u, w), ("u,z", u, z), ("v,w", v, w), ("v,z", v, z), ("w,z", w, z)]:
    g, c = ang(a, b)
    print(f"     angulo {nome}: cos = {c:.4f}, theta = {g:.2f} graus")
for nome, a in [("u", u), ("v", v), ("w", w), ("z", z)]:
    print(f"     norma {nome} = {norma(a):.4f}  (quadrado {dot(a, a)})")
# ortogonalidade do vetorial
for nome, a, b in [("uxv", u, v), ("uxw", u, w), ("vxw", v, w), ("wxv", w, v)]:
    c = cross(a, b)
    print(f"     {nome} = {fmt(c)}; .{nome[0]} = {dot(c, a)}; .{nome[2]} = {dot(c, b)}; norma^2 = {dot(c, c)}; norma = {math.sqrt(float(dot(c, c))):.4f}")
# Lagrange: |a x b|^2 = |a|^2|b|^2 - (a.b)^2
for nome, a, b in [("uxv", u, v), ("uxw", u, w), ("vxw", v, w)]:
    lhs = dot(cross(a, b), cross(a, b))
    rhs = dot(a, a) * dot(b, b) - dot(a, b) ** 2
    confere("Lagrange " + nome, lhs, rhs)
# projecao de z sobre v (exemplo da teoria)
k = dot(z, v) / dot(v, v)
z1 = tuple(k * x for x in v)
z2 = tuple(a - b for a, b in zip(z, z1))
confere("teoria proj z sobre v", z1, (F(-2), F(2), F(-2)))
confere("teoria z2 = z - z1", z2, (F(1), F(0), F(-1)))
confere("teoria z2 . v", dot(z2, v), F(0))
print("     teoria: area paralelogramo u,v = sqrt(", dot(cross(u, v), cross(u, v)), ") =", round(math.sqrt(78), 4), "; triangulo =", round(math.sqrt(78) / 2, 4))
# conferencias usadas nos jeitos
print("     k: (-7,-2,5).u =", dot((F(-7), F(-2), F(5)), u), " (-7,2,5).u =", dot((F(-7), F(2), F(5)), u), " (-7,2,5).v =", dot((F(-7), F(2), F(5)), v))
print("     l: (43/2,11,15/2).u =", dot((F(43, 2), F(11), F(15, 2)), u), " (37/2,-11,17/2).w =", dot((F(37, 2), F(-11), F(17, 2)), w), " (37/2,-11,17/2).u =", dot((F(37, 2), F(-11), F(17, 2)), u))
print("     m: (9/2,-7,5/2).v =", dot((F(9, 2), F(-7), F(5, 2)), v), " (11/2,7,3/2).v =", dot((F(11, 2), F(7), F(3, 2)), v), " (11/2,7,3/2).w =", dot((F(11, 2), F(7), F(3, 2)), w))
print("     n: (-9/2,7,-5/2).v =", dot((F(-9, 2), F(7), F(-5, 2)), v), " (-9/2,7,-5/2).w =", dot((F(-9, 2), F(7), F(-5, 2)), w))
print("     dobro de m: 2*(9/2,7,5/2) =", fmt(tuple(2 * x for x in cross(v, w))), "; 2w =", fmt(tuple(2 * x for x in w)), "; v x 2w =", fmt(cross(v, tuple(2 * x for x in w))))
print("     dobro de l: u x 2w =", fmt(cross(u, tuple(2 * x for x in w))))
print("     soma componentes l:", sum(cross(u, w)), " m:", sum(cross(v, w)))
print("     u x u =", fmt(cross(u, u)))

print()
print("TUDO OK" if ok else "HA DIVERGENCIA")
