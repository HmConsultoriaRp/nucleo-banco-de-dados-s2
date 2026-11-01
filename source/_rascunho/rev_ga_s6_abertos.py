# Troca as curvas abertas do lote ga_s6 (parabolas e ramos de hiperbole), que estavam
# gravadas como poligono de ida e volta, por poligono com "aberto": true, que o figura.js
# do site desenha como linha sem fechar e sem preencher (o laboratorio usa o mesmo campo).
# Substitui so o texto de cada item, sem reformatar o resto do arquivo.
# Uso: python -I rev_ga_s6_abertos.py
import json, os, sys, math
from fractions import Fraction as Fr

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")


def num(v):
    r = round(float(v), 3)
    if r == 0:
        return 0
    return int(r) if r == int(r) else r


def pt(*c):
    return [num(x) for x in c]


def p01():
    return [[pt(y * y / 12, y) for y in [Fr(-72, 10) + i * Fr(36, 100) for i in range(41)]]]


def p03():
    ts = [-1.3 + i * 0.065 for i in range(41)]
    return [[pt(s * 8 * math.cosh(t), 6 * math.sinh(t)) for t in ts] for s in (1, -1)]


def p06():
    ys = [Fr(-5) + i * Fr(35, 100) for i in range(41)]
    return [[pt((y - 2) ** 2 / 8 - 1, y) for y in ys]]


def p07():
    ts = [-1.5 + i * 0.075 for i in range(41)]
    r5 = math.sqrt(5)
    return [[pt(1 + s * 2 * math.cosh(t), -2 + r5 * math.sinh(t)) for t in ts] for s in (1, -1)]


def p09():
    T = math.asinh(1)
    ts = [-T + i * (2 * T / 20) for i in range(21)]
    return [
        [pt(2 * math.cosh(t), 0, 4 * math.sinh(t)) for t in ts],
        [pt(-2 * math.cosh(t), 0, 4 * math.sinh(t)) for t in ts],
        [pt(0, 3 * math.cosh(t), 4 * math.sinh(t)) for t in ts],
        [pt(0, -3 * math.cosh(t), 4 * math.sinh(t)) for t in ts],
    ]


def p12():
    xs = [Fr(-1) + i * Fr(2, 10) for i in range(21)]
    ys = [i * Fr(2, 10) for i in range(21)]
    return [
        [pt(x, 2, (x - 1) ** 2 + 3) for x in xs],
        [pt(1, y, 3 - (y - 2) ** 2) for y in ys],
    ]


PLANO = {
    "ga-s6-p01": ([0], p01),
    "ga-s6-p03": ([0, 1], p03),
    "ga-s6-p06": ([0], p06),
    "ga-s6-p07": ([0, 1], p07),
    "ga-s6-p09": ([3, 4, 5, 6], p09),
    "ga-s6-p12": ([0, 1], p12),
}

trocas = 0
for nome in ("ga_s6_p1.json", "ga_s6_p2.json"):
    caminho = os.path.join(DADOS, nome)
    with open(caminho, encoding="utf-8", newline="") as f:
        bruto = f.read()
    d = json.loads(bruto)
    for q in d["questoes"]:
        if q["id"] not in PLANO:
            continue
        idxs, gera = PLANO[q["id"]]
        novos = gera()
        assert len(novos) == len(idxs)
        for i, novo in zip(idxs, novos):
            it = q["figura"]["itens"][i]
            assert it["tipo"] == "poligono" and "aberto" not in it, (q["id"], i)
            distintos = len({tuple(p) for p in it["pts"]})
            assert distintos < len(it["pts"]), (q["id"], i, "não era ida e volta")
            velho = '{"tipo": "poligono", "pts": ' + json.dumps(it["pts"]) + ', "cor": ' + str(it["cor"]) + "}"
            assert bruto.count(velho) == 1, (q["id"], i, bruto.count(velho))
            assert len({tuple(p) for p in novo}) == len(novo), (q["id"], i, "ponto repetido")
            # a curva nova tem de comecar e terminar nos mesmos extremos da antiga
            ext_velho = {tuple(it["pts"][0]), tuple(it["pts"][len(it["pts"]) // 2])}
            ext_novo = {tuple(novo[0]), tuple(novo[-1])}
            assert ext_velho == ext_novo, (q["id"], i, ext_velho, ext_novo)
            novo_txt = '{"tipo": "poligono", "pts": ' + json.dumps(novo) + ', "cor": ' + str(it["cor"]) + ', "aberto": true}'
            bruto = bruto.replace(velho, novo_txt)
            trocas += 1
            print(q["id"], "item", i, ":", len(it["pts"]), "entradas (", distintos, "distintas ) ->", len(novo), "pontos, aberto")
    json.loads(bruto)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(bruto)
print("trocas:", trocas)
