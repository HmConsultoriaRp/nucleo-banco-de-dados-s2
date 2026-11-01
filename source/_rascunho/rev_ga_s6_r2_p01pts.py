# Revisor ga_s6, rodada 2: gera os pontos da parabola x^2 = 12y para a nova p01
# (x de -7,2 a 7,2, passo 0,36; y = x^2/12), arredondados a 3 casas.
# Uso: python -I rev_ga_s6_r2_p01pts.py
import json, sys
from fractions import Fraction as Fr

sys.stdout.reconfigure(encoding="utf-8")


def num(v):
    r = round(float(v), 3)
    if r == 0:
        return 0
    return int(r) if r == int(r) else r


xs = [Fr(-72, 10) + i * Fr(36, 100) for i in range(41)]
pts = [[num(x), num(x * x / 12)] for x in xs]
print(len(pts), "pontos")
print(json.dumps(pts))
