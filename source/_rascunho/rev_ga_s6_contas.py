# Revisao adversarial do lote ga_s6 (Geometria Analitica, semana 6, previa).
# Refaz cada conta do zero, sem olhar o campo "resposta", e confere alternativas,
# numeros dos jeitos e figuras. Uso: python -I rev_ga_s6_contas.py
import json, os, re, sys, math
from fractions import Fraction as Fr

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

falhas = []
ok = 0


def confere(cond, msg):
    global ok
    if cond:
        ok += 1
    else:
        falhas.append(msg)
        print("FALHA", msg)


def carrega():
    qs, semanas = {}, []
    for nome in sorted(os.listdir(DADOS)):
        if nome.startswith("ga_s6_p") and nome.endswith(".json"):
            with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
                bruto = f.read()
            for ch in bruto:
                if ord(ch) < 32 and ch not in "\n\r\t":
                    falhas.append(f"{nome}: byte de controle {ord(ch)}")
            d = json.loads(bruto)
            semanas += d.get("semanas", [])
            for q in d["questoes"]:
                qs[q["id"]] = q
    return qs, semanas


def frac_txt(x):
    """Fraction -> texto no padrao do lote (menos tipografico)."""
    x = Fr(x)
    s = "−" if x < 0 else ""
    x = abs(x)
    return s + (str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}")


def certa(q):
    return [a for a in q["alternativas"] if a.get("certa")][0]["t"]


def alt(q, letra):
    return q["alternativas"]["ABCDE".index(letra)]


def todos_textos(q):
    j = q["jeitos"]
    partes = [q["enunciado"], q["dica"], q["resposta"]]
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        partes.append(j[k])
    partes += j["receita"]
    partes += [c["fala"] for c in j["conversa"]]
    for a in q["alternativas"]:
        partes.append(a["t"])
        partes.append(a.get("erro", ""))
    if q.get("figura"):
        partes.append(q["figura"].get("legenda", ""))
    return " ".join(partes)


def residuo_max(pts, f):
    return max(abs(f(*p)) for p in pts)


def poligonos(q):
    return [it for it in q["figura"]["itens"] if it["tipo"] == "poligono"]


def pontos(q):
    return {it.get("rot", ""): tuple(it["em"]) for it in q["figura"]["itens"] if it["tipo"] == "ponto"}


qs, semanas = carrega()
ids = [f"ga-s6-p{i:02d}" for i in range(1, 13)]
confere(sorted(qs) == ids, f"ids: {sorted(qs)}")

# ---------------------------------------------------------------- p01
q = qs["ga-s6-p01"]
p = Fr(12, 4)                          # y^2 = 4px com 4p = 12
confere(certa(q) == f"Foco ({p}, 0) e diretriz x = −{p}", "p01 certa")
confere(alt(q, "A")["t"] == "Foco (12, 0) e diretriz x = −12", "p01 A")      # 12 tomado como p
confere(alt(q, "B")["t"] == f"Foco (0, {p}) e diretriz y = −{p}", "p01 B")   # x^2 = 12y
p2 = Fr(12, 2)                         # convencao y^2 = 2px: p = 6, foco (p/2, 0)
confere(alt(q, "D")["t"] == f"Foco ({p2}, 0) e diretriz x = −{p2}" and p2 / 2 == p, "p01 D")
confere(alt(q, "E")["t"] == f"Foco (−{p}, 0) e diretriz x = {p}", "p01 E")
P = (3, 6)
confere(P[1] ** 2 == 12 * P[0], "p01 P na curva")
confere(math.dist(P, (3, 0)) == 6 and P[0] - (-3) == 6, "p01 distancias 6 e 6")
confere((3 - 12) ** 2 + 6 ** 2 == 117 and 3 - (-12) == 15, "p01 confira foco errado")
pol = poligonos(q)[0]["pts"]
confere(residuo_max(pol, lambda x, y: x - y * y / 12) < 0.003, "p01 figura parabola")
confere(pontos(q)["F"] == (3, 0) and pontos(q)["V"] == (0, 0) and pontos(q)["P"] == (3, 6), "p01 pontos")

# ---------------------------------------------------------------- p02
q = qs["ga-s6-p02"]
a2, b2 = Fr(169), Fr(144)
c2 = a2 - b2
a, c = Fr(13), Fr(5)
confere(a * a == a2 and c * c == c2, "p02 a e c")
confere(certa(q) == f"Focos (±{c}, 0) e e = {frac_txt(c / a)}", "p02 certa")
confere(a2 + b2 == 313 and alt(q, "B")["t"] == "Focos (±√313, 0) e e = √313/13", "p02 B")
confere(alt(q, "C")["t"] == "Focos (0, ±5) e e = 5/13", "p02 C")
confere(alt(q, "D")["t"] == f"Focos (±5, 0) e e = {frac_txt(c / 12)}", "p02 D")
confere(alt(q, "E")["t"] == f"Focos (±{c2}, 0) e e = {frac_txt(c2 / a)}", "p02 E")
confere(round(float(c / a), 3) == 0.385, "p02 0,385")
confere(math.dist((0, 12), (5, 0)) == 13, "p02 B ate F2 = 13")
confere(round(math.sqrt(313), 1) == 17.7, "p02 17,7")
pol = poligonos(q)[0]["pts"]
confere(len(pol) == 40 and residuo_max(pol, lambda x, y: x * x / 169 + y * y / 144 - 1) < 0.003, "p02 figura")

# ---------------------------------------------------------------- p03
q = qs["ga-s6-p03"]
a, b = 8, 6
c = math.isqrt(a * a + b * b)
confere(c * c == 100, "p03 c")
confere(certa(q) == f"Focos (±{c}, 0); assíntotas y = ±(3/4)x" and Fr(b, a) == Fr(3, 4), "p03 certa")
confere(64 - 36 == 28 and 4 * 7 == 28, "p03 A 2√7")
confere(Fr(a, b) == Fr(4, 3), "p03 B")
confere(Fr(36, 64) == Fr(9, 16), "p03 D")
y = math.sqrt(36 * (256 / 64 - 1))
confere(abs(y - 6 * math.sqrt(3)) < 1e-12 and round(y, 2) == 10.39, "p03 y = 6√3")
d1, d2 = math.hypot(16 - 10, y), math.hypot(16 + 10, y)
confere(abs(d1 - 12) < 1e-9 and abs(d2 - 28) < 1e-9 and abs(d2 - d1 - 16) < 1e-9, "p03 confira 12 e 28")
confere(round(2 * math.sqrt(7), 1) == 5.3, "p03 2√7 ≈ 5,3")
for pol in poligonos(q)[:2]:
    confere(residuo_max(pol["pts"], lambda x, y: x * x / 64 - y * y / 36 - 1) < 0.003, "p03 figura ramo")
for it in q["figura"]["itens"]:
    if it["tipo"] == "segmento":
        for pt in (it["de"], it["ate"]):
            confere(abs(abs(pt[1]) - 0.75 * abs(pt[0])) < 1e-9, "p03 assintota")

# ---------------------------------------------------------------- p04
q = qs["ga-s6-p04"]
A, C, D, E, F = 9, 4, 36, -8, 4
h, k = Fr(-D, 2 * A), Fr(-E, 2 * C)
rhs = -F + A * h * h + C * k * k
confere((h, k) == (-2, 1) and rhs == 36, "p04 centro e 36")
confere((Fr(rhs, A), Fr(rhs, C)) == (4, 9), "p04 denominadores")
confere(certa(q) == f"Elipse de centro ({frac_txt(h)}, {frac_txt(k)})", "p04 certa")
confere((-D // 2, -E // 2) == (-18, 4) and alt(q, "C")["t"] == "Elipse de centro (−18, 4)", "p04 C")
f = lambda x, y: 9 * x * x + 4 * y * y + 36 * x - 8 * y + 4
confere(f(0, 1) == 0 and f(-2, 4) == 0 and f(4, -1) == 304, "p04 confira")
confere(9 * 4 == 36 and 4 * 1 == 4, "p04 ajustes 36 e 4")
pol = poligonos(q)[0]["pts"]
confere(len(pol) == 40 and residuo_max(pol, lambda x, y: (x + 2) ** 2 / 4 + (y - 1) ** 2 / 9 - 1) < 0.003, "p04 figura")
pp = pontos(q)
confere(abs(pp["F₂"][1] - (1 + math.sqrt(5))) < 1e-3 and abs(pp["F₁"][1] - (1 - math.sqrt(5))) < 1e-3, "p04 focos")

# ---------------------------------------------------------------- p05
q = qs["ga-s6-p05"]
a = Fr(20, 2); c = Fr(3, 5) * a; b2 = a * a - c * c
confere((a, c, b2) == (10, 6, 64), "p05 a c b2")
confere(certa(q) == f"x²/{a * a} + y²/{b2} = 1", "p05 certa")
a20 = 20; c20 = Fr(3, 5) * a20
confere(c20 == 12 and a20 ** 2 - c20 ** 2 == 256, "p05 C")
confere(100 + 36 == 136, "p05 D")
confere(math.hypot(6, 8) == 10, "p05 confira 10")
pol = poligonos(q)[0]["pts"]
confere(len(pol) == 40 and residuo_max(pol, lambda x, y: x * x / 100 + y * y / 64 - 1) < 0.003, "p05 figura")

# ---------------------------------------------------------------- p06
q = qs["ga-s6-p06"]
# y^2 - 4y - 8x - 4 = 0  ->  (y - 2)^2 = 8x + 8 = 8(x + 1)
k = Fr(4, 2); h = Fr(-8, 8); p = Fr(8, 4)
confere((h, k, p) == (-1, 2, 2), "p06 h k p")
confere(certa(q) == f"V = ({frac_txt(h)}, {k}), F = ({frac_txt(h + p)}, {k}), diretriz x = {frac_txt(h - p)}", "p06 certa")
confere(alt(q, "B")["t"] == "V = (0, 0), F = (2, 0), diretriz x = −2", "p06 B")
p4 = Fr(8, 2)
confere(alt(q, "C")["t"] == f"V = (−1, 2), F = ({frac_txt(h + p4)}, 2), diretriz x = {frac_txt(h - p4)}", "p06 C")
confere(alt(q, "D")["t"] == f"V = (1, −2), F = ({1 + p}, −2), diretriz x = {frac_txt(1 - p)}", "p06 D")
confere(alt(q, "E")["t"] == f"V = (−1, 2), F = (−1, {k + p}), diretriz y = {k - p}", "p06 E")
g = lambda x, y: y * y - 4 * y - 8 * x - 4
confere(g(1, 6) == 0 and math.dist((1, 6), (1, 2)) == 4 and 1 - (-3) == 4, "p06 confira P")
pol = poligonos(q)[0]["pts"]
confere(residuo_max(pol, lambda x, y: (y - 2) ** 2 / 8 - 1 - x) < 0.003, "p06 figura")

# ---------------------------------------------------------------- p07
q = qs["ga-s6-p07"]
# 5x^2 - 4y^2 - 10x - 16y - 31 = 0
A, C, D, E, F = 5, -4, -10, -16, -31
h, k = Fr(-D, 2 * A), Fr(-E, 2 * C)
rhs = -F + A * h * h + C * k * k
confere((h, k, rhs) == (1, -2, 20), "p07 centro e 20")
a2, b2 = Fr(rhs, A), Fr(rhs, -C)
confere((a2, b2) == (4, 5), "p07 a2 b2")
c = math.isqrt(int(a2 + b2))
confere(c == 3, "p07 c")
confere(certa(q) == f"({h + c}, {frac_txt(k)}) e ({frac_txt(h - c)}, {frac_txt(k)})", "p07 certa")
confere(alt(q, "A")["t"] == "(2, −2) e (0, −2)" and b2 - a2 == 1, "p07 A")
confere(alt(q, "B")["t"] == "(3, −2) e (−1, −2)", "p07 B vertices")
confere(alt(q, "C")["t"] == "(1, 1) e (1, −5)", "p07 C vertical")
confere(alt(q, "E")["t"] == "(2, 2) e (−4, 2)", "p07 E")
G = lambda x, y: 5 * x * x - 4 * y * y - 10 * x - 16 * y - 31
confere(G(3, -2) == 0 and G(Fr(4), Fr(1, 2)) == 0, "p07 confira pontos")
confere(math.dist((4, 0.5), (4, -2)) == 2.5 and math.dist((4, 0.5), (-2, -2)) == 6.5, "p07 confira 5/2 e 13/2")
confere(-5 + 16 == 11 and 31 + 5 - 16 == 20 and 31 + 5 + 16 == 52, "p07 trabalho 52")
for pol in poligonos(q)[:2]:
    confere(residuo_max(pol["pts"], lambda x, y: (x - 1) ** 2 / 4 - (y + 2) ** 2 / 5 - 1) < 0.003, "p07 figura ramo")
m = math.sqrt(5) / 2
for it in q["figura"]["itens"]:
    if it["tipo"] == "segmento":
        for pt in (it["de"], it["ate"]):
            confere(abs(abs(pt[1] + 2) - m * abs(pt[0] - 1)) < 0.01, "p07 assintota")

# ---------------------------------------------------------------- p08
q = qs["ga-s6-p08"]
r2 = 4
kk = 9 + 16 - r2
confere(certa(q) == f"k = {kk}", "p08 certa")
confere(25 - 23 == 2 and 25 + 4 == 29 and 25 - (-21) == 46 and -r2 == -4, "p08 erradas")
H = lambda x, y: x * x + y * y - 6 * x + 8 * y + 21
confere(H(5, -4) == 0 and H(3, -2) == 0, "p08 confira")
pol = poligonos(q)[0]["pts"]
confere(len(pol) == 40 and residuo_max(pol, lambda x, y: (x - 3) ** 2 + (y + 4) ** 2 - 4) < 0.003, "p08 figura")

# ---------------------------------------------------------------- p09
q = qs["ga-s6-p09"]
sinais = [+1, +1, -1]
confere(sinais.count(-1) == 1 and certa(q) == "Hiperboloide de uma folha", "p09 certa")
S = lambda x, y, z: x * x / 4 + y * y / 9 - z * z / 16 - 1
for pol in poligonos(q):
    confere(residuo_max(pol["pts"], S) < 0.003, "p09 figura")
confere(Fr(1) + Fr(16, 16) == 2, "p09 corte z = 4 da 2")

# ---------------------------------------------------------------- p10
q = qs["ga-s6-p10"]
cone = lambda x, y, z: x * x / 4 + y * y / 9 - z * z
# corte z = 2: x^2/4 + y^2/9 = 4 -> x^2/16 + y^2/36 = 1
confere(Fr(4) * 4 == 16 and Fr(9) * 4 == 36, "p10 z=2")
confere(certa(q) == "Cone elíptico x²/4 + y²/9 = z²", "p10 certa")
confere(4 * 2 == 8 and 9 * 2 == 18, "p10 A paraboloide em z=2: x²/8 + y²/18")
for pol in poligonos(q):
    confere(residuo_max(pol["pts"], cone) < 0.003, "p10 figura elipses")
for it in q["figura"]["itens"]:
    if it["tipo"] == "segmento":
        for t in (0, 0.5, 1):
            pt = [it["de"][i] + t * (it["ate"][i] - it["de"][i]) for i in range(3)]
            confere(abs(cone(*pt)) < 1e-9, "p10 figura retas no cone")

# ---------------------------------------------------------------- p11
q = qs["ga-s6-p11"]
cil = lambda x, y, z: 4 * x * x + 9 * z * z - 36
confere(certa(q) == "Cilindro elíptico com geratrizes paralelas ao eixo y", "p11 certa")
confere(cil(3, 7, 0) == 0 and cil(0, 2, 2) == 0 and cil(0, 0, 3) == 45 and 9 * 9 == 81, "p11 confira")
for pol in poligonos(q):
    confere(residuo_max(pol["pts"], lambda x, y, z: x * x / 9 + z * z / 4 - 1) < 0.003, "p11 figura")
    confere(len({p[1] for p in pol["pts"]}) == 1, "p11 fatia num plano y = k")
for it in q["figura"]["itens"]:
    if it["tipo"] == "segmento":
        confere(cil(*it["de"]) == 0 and cil(*it["ate"]) == 0 and it["de"][0] == it["ate"][0] and it["de"][2] == it["ate"][2], "p11 geratriz")

# ---------------------------------------------------------------- p12
q = qs["ga-s6-p12"]
z = lambda x, y: x * x - y * y - 2 * x + 4 * y
# completar: (x-1)^2 - 1 - [(y-2)^2 - 4] = (x-1)^2 - (y-2)^2 + 3
for x in range(-3, 4):
    for y in range(-3, 4):
        confere(z(x, y) == (x - 1) ** 2 - (y - 2) ** 2 + 3, "p12 forma reduzida")
confere(z(1, 2) == 3, "p12 ponto")
confere(certa(q) == "Paraboloide hiperbólico com ponto de sela (1, 2, 3)", "p12 certa")
# alternativa B: quem troca -y^2 por +y^2 calcula outro ponto
zb = lambda x, y: x * x + y * y - 2 * x + 4 * y
confere(zb(1, -2) == -5, "p12 B: com +y² o vertice seria (1, −2, −5)")
# Excel: linha y = 2 tem minimo em x = 1; coluna x = 1 tem maximo em y = 2
linha = {x: z(x, 2) for x in range(-1, 4)}
coluna = {y: z(1, y) for y in range(0, 5)}
confere(min(linha, key=linha.get) == 1 and max(coluna, key=coluna.get) == 2, "p12 sela na tabela")
confere(-1 - 4 == -5 and -1 + 4 == 3, "p12 conversa")
for pol in poligonos(q):
    confere(residuo_max(pol["pts"], lambda x, y, zz: zz - z(x, y)) < 1e-9, "p12 figura")
for it in q["figura"]["itens"]:
    if it["tipo"] == "segmento":
        for t in (0, 0.25, 0.5, 1):
            pt = [it["de"][i] + t * (it["ate"][i] - it["de"][i]) for i in range(3)]
            confere(abs(pt[2] - z(pt[0], pt[1])) < 1e-9, "p12 X no plano z = 3")

# ---------------------------------------------------------------- teoria
s = semanas[0]
confere(len(semanas) == 1 and s["semana"] == 6 and s["previa"] is True, "teoria previa")
confere(s["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "teoria fonte")
T = lambda x, y: 4 * x * x + y * y - 8 * x + 6 * y + 9
for x in range(-3, 4):
    for y in range(-6, 2):
        confere(T(x, y) == 4 * (x - 1) ** 2 + (y + 3) ** 2 - 4, "teoria bloco 5")
for b in s["blocos"]:
    n = len(b["texto"].split())
    confere(40 <= n <= 120, f"teoria bloco '{b['titulo']}' com {n} palavras")
for kk2, v in s["jeitos"].items():
    n = len(v.split())
    confere(50 <= n <= 120, f"teoria jeito {kk2} com {n} palavras")

# ---------------------------------------------------------------- forma
for qid, q in qs.items():
    j = q["jeitos"]
    for kk2 in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = len(j[kk2].split())
        confere(35 <= n <= 110, f"{qid}.{kk2} com {n} palavras")
    confere(3 <= len(j["receita"]) <= 7, f"{qid} receita")
    confere(4 <= len(j["conversa"]) <= 8, f"{qid} conversa")
    txt = re.sub(r"`[^`]*`", " ", todos_textos(q))
    confere("!" not in txt, f"{qid} exclamação")
    confere("—" not in txt, f"{qid} travessão")
    confere(not re.search(r"(^|[\s(,\[=±])-\d", txt), f"{qid} hífen como menos")
    if q.get("figura", {}).get("onde") == "enunciado":
        falhas.append(f"{qid}: figura no enunciado")
    for pol in poligonos(q):
        if q["figura"]["modo"] == "2d" and pol.get("cor") == 1:
            n = len({tuple(p) for p in pol["pts"]})
            confere(n >= 20, f"{qid} polígono com {n} pontos distintos")

ABERTAS = {"ga-s6-p01": 1, "ga-s6-p03": 2, "ga-s6-p06": 1, "ga-s6-p07": 2, "ga-s6-p09": 4, "ga-s6-p12": 2}
for qid, q in qs.items():
    abertos = [p for p in poligonos(q) if p.get("aberto") is True]
    confere(len(abertos) == ABERTAS.get(qid, 0), f"{qid}: {len(abertos)} curvas abertas")
    for p in abertos:
        confere(len({tuple(x) for x in p["pts"]}) == len(p["pts"]) >= 21, f"{qid}: curva aberta com ponto repetido ou curta")
    for p in poligonos(q):
        if not p.get("aberto") and p.get("cor") == 1:
            confere(len(p["pts"]) >= 32, f"{qid}: curva fechada com {len(p['pts'])} pontos")

pos = [("ABCDE")[[a.get("certa") for a in qs[i]["alternativas"]].index(True)] for i in ids]
niveis = [qs[i]["nivel"] for i in ids]
print("certas:", "".join(pos), {l: pos.count(l) for l in "ABCDE"})
print("niveis:", {n: niveis.count(n) for n in (1, 2, 3)})
print(f"{ok} conferências OK; {len(falhas)} falha(s)")
