# Busca de vetores para c04 (volume do paralelepipedo, produto misto negativo).
from math import sqrt

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])

def dot(a, b):
    return sum(x*y for x, y in zip(a, b))

def det(u, v, w):
    return dot(u, cross(v, w))

def det_meio_errado(u, v, w):
    # erro: cofator do meio sem o sinal de menos
    a, b, c = u
    return a*(v[1]*w[2] - v[2]*w[1]) + b*(v[0]*w[2] - v[2]*w[0]) + c*(v[0]*w[1] - v[1]*w[0])

cands = [(3, 1, 0), (1, 2, -1), (0, 2, 3), (2, 0, 1), (1, -1, 2), (0, 1, 4), (2, 3, 1)]
for u in cands:
    for v in cands:
        for w in cands:
            if len({u, v, w}) < 3:
                continue
            d = det(u, v, w)
            if -30 <= d <= -12:
                e = det_meio_errado(u, v, w)
                if abs(e) != abs(d) and e != 0:
                    print(u, v, w, "det", d, "meio errado", e, "area base", sqrt(dot(cross(v, w), cross(v, w))))
