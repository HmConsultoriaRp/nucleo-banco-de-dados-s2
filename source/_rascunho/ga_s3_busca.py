# Busca de numeros para as questoes construidas da Semana 3 (produto misto).
from fractions import Fraction as F
from itertools import product

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def det(u, v, w):
    return dot(u, cross(v, w))

def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))

# c03: coplanares, u = (1, k, 2)? procurar k inteiro bonito
print("c03 candidatos")
for a in [(2, -1, 3), (1, 3, -2), (3, 1, 2)]:
    for b in [(1, 2, -1), (4, 1, 1), (2, 5, 1), (1, -1, 4)]:
        # u = (1, k, 3): det linear em k
        d0 = det((1, 0, 3), a, b)
        d1 = det((1, 1, 3), a, b) - d0
        if d1 != 0:
            k = F(-d0, d1)
            if k.denominator == 1 and k != 0 and abs(k) <= 9:
                print(" v=", a, "w=", b, "det = ", d0, "+", d1, "k ; k =", k)

# c05: tetraedro com 4 pontos, volume inteiro
print("c05 candidatos")
A = (1, 0, 2)
for B in [(3, 1, 2), (2, 3, 1), (4, 0, 3)]:
    for C in [(1, 4, 0), (0, 2, 5), (2, -1, 4)]:
        for D in [(2, 2, 5), (3, 3, 0), (1, 1, 6)]:
            d = det(sub(B, A), sub(C, A), sub(D, A))
            if d != 0 and d % 6 == 0:
                print(" A", A, "B", B, "C", C, "D", D, "det", d, "vol", F(abs(d), 6))
