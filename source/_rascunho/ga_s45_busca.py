# Busca de numeros "limpos" para duas questoes da Semana 5 (ponto-reta e retas reversas).
from fractions import Fraction as F
from itertools import product
import math

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))

def n2(a):
    return dot(a, a)

print("== ponto-reta: v=(2,1,-2), A=(1,-1,2) ==")
v = (2, 1, -2)
A = (1, -1, 2)
achados = []
for P in product(range(-2, 5), repeat=3):
    AP = sub(P, A)
    c = cross(AP, v)
    if n2(c) == 0:
        continue
    if n2(c) in (36, 81, 144) and dot(AP, v) != 0 and n2(AP) not in (36, 81, 144):
        achados.append((P, AP, c, n2(c), dot(AP, v), n2(AP)))
for a in achados[:15]:
    print(a)

print("== reversas: u x v com norma 3 ==")
cands = []
vals = range(-2, 3)
for u in product(vals, repeat=3):
    for w in product(vals, repeat=3):
        c = cross(u, w)
        if n2(c) == 9 and 0 not in c and n2(u) <= 6 and n2(w) <= 6:
            cands.append((u, w, c))
for c in cands[:12]:
    print(c)
