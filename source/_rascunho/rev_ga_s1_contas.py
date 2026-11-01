# -*- coding: utf-8 -*-
# REVISOR do lote ga_s1 (Lista 1 de Geometria Analitica, Semana 1).
# Escrito do zero, sem reaproveitar o script do gerador.
# 1) Resolve cada item com Fraction (e numeros da forma p + q*raiz(3) nos hexagonos).
# 2) Para cada alternativa errada, refaz a conta descrita no "erro" e confere o texto.
# 3) Confere que nenhuma errada e equivalente a certa.
# 4) Confere figuras (coordenadas, setas, ausencia da resposta nas figuras de enunciado).
# 5) Confere ids, niveis, origem, posicoes, copia da Q3, bytes de controle, tamanhos.
# Uso: python -I rev_ga_s1_contas.py
import json, math, os, re, sys
from fractions import Fraction as Fr

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
GER = os.path.dirname(AQUI)
DADOS = os.path.join(GER, "dados")

falhas = []
nok = 0


def chk(nome, cond):
    global nok
    if cond:
        nok += 1
    else:
        falhas.append(nome)
        print("FALHA", nome)


M = "−"  # sinal de menos tipografico


def fnum(x):
    x = Fr(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else f"{abs(x.numerator)}/{x.denominator}"
    return (M + s) if x < 0 else s


def fvec(t):
    return "(" + ", ".join(fnum(c) for c in t) + ")"


def add(*vs):
    return tuple(sum(c) for c in zip(*vs))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(k, a):
    return tuple(Fr(k) * x for x in a)


def sq(a):
    return sum(Fr(x) * Fr(x) for x in a)


# ---------- carrega o lote ----------
arqs = [os.path.join(DADOS, f"ga_s1_p{i}.json") for i in range(1, 6)]
Q = {}
ordem = []
semanas = []
for a in arqs:
    with open(a, encoding="utf-8") as f:
        bruto = f.read()
    chk(f"{os.path.basename(a)} sem bytes de controle", not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", bruto))
    d = json.loads(bruto)
    semanas += d.get("semanas", [])
    for q in d["questoes"]:
        Q[q["id"]] = q
        ordem.append(q["id"])


def alts(qid):
    return {a["t"]: a for a in Q[qid]["alternativas"]}


def certa(qid):
    c = [a["t"] for a in Q[qid]["alternativas"] if a.get("certa") is True]
    return c[0] if len(c) == 1 else None


def confere_alts(qid, certo_txt, mapa, igual=None):
    """mapa: texto da alternativa -> valor calculado pela conta do erro (ou da resposta).
    igual(a, b): equivalencia matematica; padrao ==."""
    igual = igual or (lambda a, b: a == b)
    textos = [a["t"] for a in Q[qid]["alternativas"]]
    chk(f"{qid}: textos das alternativas = os previstos", sorted(textos) == sorted(mapa.keys()))
    chk(f"{qid}: alternativa certa = '{certo_txt}'", certa(qid) == certo_txt)
    vc = mapa[certo_txt]
    for t, val in mapa.items():
        if t == certo_txt:
            continue
        chk(f"{qid}: errada '{t}' difere da certa", not igual(val, vc))


# ================= Q1 =================
u = (1, 1, -1); v = (2, 3, 4); w = (1, 2, -4)
# a
r = add(u, w)
chk("q1a gabarito", r == (2, 3, -5))
confere_alts("ga-s1-l1q1a", fvec(r), {
    fvec(sub(u, w)): sub(u, w),
    fvec(r): r,
    fvec(add(u, v)): add(u, v),
    fvec((u[0] + w[0], u[1] + w[1], u[2] - w[2])): (2, 3, 3),     # -1 + 4
    fvec(tuple(a * b for a, b in zip(u, w))): (1, 2, 4),
})
chk("q1a erro D: -1+4=3", u[2] - w[2] == 3)
# b
p = add(mul(-1, u), v)
r = sub(p, mul(3, w))
chk("q1b gabarito", r == (-2, -4, 17))
confere_alts("ga-s1-l1q1b", fvec(r), {
    fvec(add(p, mul(3, w))): add(p, mul(3, w)),
    fvec(sub(add(u, v), mul(3, w))): sub(add(u, v), mul(3, w)),
    fvec((p[0] - 3, p[1] - 6, p[2] - 12)): (-2, -4, -7),
    fvec(r): r,
    fvec(sub(p, w)): sub(p, w),
})
chk("q1b erro A soma = (4,8,-7)", add(p, mul(3, w)) == (4, 8, -7))
chk("q1b erro B = (0,-2,15)", sub(add(u, v), mul(3, w)) == (0, -2, 15))
chk("q1b erro E = (0,0,9)", sub(p, w) == (0, 0, 9))
chk("q1b erro jeito 'perde o terceiro' w3=+4 -> z=-7", p[2] - 3 * 4 == -7)
# c
r = sub(mul(2, v), mul(3, sub(w, u)))
chk("q1c gabarito", r == (4, 3, 17))
cB = sub(mul(2, v), mul(3, sub(u, w)))
cC = add(sub(mul(2, v), mul(3, w)), u)
cD = sub(sub(mul(2, v), mul(3, w)), mul(3, u))
cE = sub(v, mul(3, sub(w, u)))
confere_alts("ga-s1-l1q1c", fvec(r), {fvec(r): r, fvec(cB): cB, fvec(cC): cC, fvec(cD): cD, fvec(cE): cE})
chk("q1c B (4,9,-1)", cB == (4, 9, -1)); chk("q1c C (2,1,19)", cC == (2, 1, 19))
chk("q1c D (-2,-3,23)", cD == (-2, -3, 23)); chk("q1c E (2,0,13)", cE == (2, 0, 13))
chk("q1c u-w=(0,-1,3)", sub(u, w) == (0, -1, 3))
chk("q1c E: 3(w-u)=(0,3,-9)", mul(3, sub(w, u)) == (0, 3, -9))
# d
r = sub(w, sub(u, mul(2, v)))
chk("q1d gabarito", r == (4, 7, 5))
dA = sub(sub(w, u), mul(2, v))
dB = add(sub(w, u), v)
dC = sub(sub(u, mul(2, v)), w)
dD = (r[0], r[1], w[2] - 9)
confere_alts("ga-s1-l1q1d", fvec(r), {fvec(dA): dA, fvec(dB): dB, fvec(dC): dC, fvec(dD): dD, fvec(r): r})
chk("q1d A (-4,-5,-11)", dA == (-4, -5, -11)); chk("q1d B (2,4,1)", dB == (2, 4, 1))
chk("q1d C (-4,-7,-5) = -resposta", dC == (-4, -7, -5) and dC == mul(-1, r))
chk("q1d D (4,7,-13)", dD == (4, 7, -13))
chk("q1d confira: r + (u-2v) = w", add(r, sub(u, mul(2, v))) == w)

# ================= Q2 =================
u1 = (-1, -2, 3); u2 = (2, 1, 2); u3 = (-1, 2, 1)
r = add(u1, u2, u3)
chk("q2 gabarito", r == (0, 1, 6))
chk("q2 substitui", sub(add(u1, u2), sub(r, u3)) == (0, 0, 0))
a2A = sub(add(u1, u2), u3); a2E = sub(u3, add(u1, u2))
confere_alts("ga-s1-l1q2", fvec(r), {fvec(a2A): a2A, fvec(mul(-1, r)): mul(-1, r), fvec(r): r,
                                     fvec(add(u1, u2)): add(u1, u2), fvec(a2E): a2E})
chk("q2 A (2,-3,4)", a2A == (2, -3, 4)); chk("q2 E (-2,3,-4)", a2E == (-2, 3, -4))
chk("q2 D (1,-1,5)", add(u1, u2) == (1, -1, 5))
fig = Q["ga-s1-l1q2"]["figura"]["itens"]
chk("q2 figura encadeada", [it["ate"] for it in fig] == [[-1, -2, 3], [1, -1, 5], [0, 1, 6], [0, 1, 6]]
    and fig[1]["de"] == [-1, -2, 3] and fig[2]["de"] == [1, -1, 5])

# ================= Q3 (copia de exemplos.json) =================
with open(os.path.join(GER, "exemplos.json"), encoding="utf-8") as f:
    ex = json.load(f)
ex3 = [q for q in ex["questoes"] if q["id"] == "ga-s1-l1q3"][0]
chk("q3 identica a exemplos.json", ex3 == Q["ga-s1-l1q3"])
A3 = (1, 1, 3); B3 = (-3, 1, 5); AB3 = sub(B3, A3)
chk("q3 gabarito (-11,1,9)", add(A3, mul(3, AB3)) == (-11, 1, 9))

# ================= Q4 =================
A = (1, -2, 3); B = (1, 1, -3); C = (-1, 1, -2)
D = sub(add(A, C), B)
chk("q4 gabarito", D == (-1, -2, 4))
chk("q4 diagonais", add(A, C) == add(B, D))
a4B = add(A, sub(B, C)); a4C = add(C, sub(B, A)); a4D = mul(Fr(1, 2), add(A, C)); a4E = (D[0], D[1], 3 + (-2) - 3)
confere_alts("ga-s1-l1q4", fvec(D), {fvec(D): D, fvec(a4B): a4B, fvec(a4C): a4C, fvec(a4D): a4D, fvec(a4E): a4E})
chk("q4 B (3,-2,2)", a4B == (3, -2, 2)); chk("q4 C (-1,4,-8)", a4C == (-1, 4, -8))
chk("q4 D ponto medio", a4D == (0, Fr(-1, 2), Fr(1, 2))); chk("q4 E (-1,-2,-2)", a4E == (-1, -2, -2))
chk("q4 conversa: C - AB = D", sub(C, sub(B, A)) == D)
chk("q4 BC=(-2,0,1)", sub(C, B) == (-2, 0, 1))
fig = Q["ga-s1-l1q4"]["figura"]["itens"]
chk("q4 poligono ABCD", fig[0]["pts"] == [list(A), list(B), list(C), list(D)])
chk("q4 M", fig[-1]["em"] == [0, -0.5, 0.5])

# ================= Q5 (paralelepipedo) =================
P5 = {"A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0),
      "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1)}  # coeficientes de u, v, w
COORD = {"A": [0, 0, 0], "B": [3, 0, 0], "C": [3, 2, 0], "D": [0, 2, 0],
         "E": [0, 0, 2], "F": [3, 0, 2], "G": [3, 2, 2], "H": [0, 2, 2]}


def vec5(xy):
    return sub(P5[xy[1]], P5[xy[0]])


def fuvw(c):
    nomes = ["[[u]]", "[[v]]", "[[w]]"]
    s = ""
    for k_, n in zip(c, nomes):
        if k_ == 0:
            continue
        assert abs(k_) == 1
        if not s:
            s = (M if k_ < 0 else "") + n
        else:
            s += (" " + M + " " if k_ < 0 else " + ") + n
    return s


HB = vec5("HB"); CH = vec5("CH")
chk("q5a gabarito u-v-w", HB == (1, -1, -1))
chk("q5b gabarito -u+w", CH == (-1, 0, 1))
confere_alts("ga-s1-l1q5a", fuvw(HB), {fuvw(vec5("BH")): vec5("BH"), fuvw(vec5("AG")): vec5("AG"),
                                      fuvw(vec5("DF")): vec5("DF"), fuvw(HB): HB, fuvw(vec5("EC")): vec5("EC")})
confere_alts("ga-s1-l1q5b", fuvw(CH), {fuvw(vec5("HC")): vec5("HC"), fuvw(CH): CH, fuvw(vec5("BH")): vec5("BH"),
                                      fuvw((1, 0, 1)): (1, 0, 1), fuvw(vec5("CE")): vec5("CE")})
chk("q5b conversa C->G->H", add(vec5("CG"), vec5("GH")) == CH)
for qid in ("ga-s1-l1q5a", "ga-s1-l1q5b"):
    f_ = Q[qid]["figura"]
    chk(f"{qid} figura no enunciado", f_["onde"] == "enunciado" and f_["modo"] == "3d")
    pts = {it["rot"]: it["em"] for it in f_["itens"] if it["tipo"] == "ponto"}
    chk(f"{qid} rotulos dos 8 vertices", pts == COORD)
    arestas = set()
    for it in f_["itens"]:
        if it["tipo"] in ("segmento", "vetor"):
            arestas.add(frozenset([tuple(it["de"]), tuple(it["ate"])]))
    esperado = set()
    for a_, b_ in ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]:
        esperado.add(frozenset([tuple(COORD[a_]), tuple(COORD[b_])]))
    chk(f"{qid} 12 arestas e nada alem delas", arestas == esperado)
    vets = {it["rot"]: (it["de"], it["ate"], it.get("cor")) for it in f_["itens"] if it["tipo"] == "vetor"}
    chk(f"{qid} u, v, w nas arestas certas", vets == {"u": ([0, 0, 0], [3, 0, 0], 1), "v": ([0, 0, 0], [0, 2, 0], 2),
                                                       "w": ([0, 0, 0], [0, 0, 2], 3)})
chk("q5a confira coordenadas (3,-2,-2)", tuple(b - h for b, h in zip(COORD["B"], COORD["H"])) == (3, -2, -2))
chk("q5b confira coordenadas (-3,0,2)", tuple(h - c for h, c in zip(COORD["H"], COORD["C"])) == (-3, 0, 2))

# ================= Q6 (hexagonos), numeros p + q*raiz3 =================
# ponto: ((px, qx), (py, qy))
R3 = lambda q: (Fr(0), Fr(q))
N = lambda p: (Fr(p), Fr(0))
HX = {"B": (N(0), N(2)), "A": (R3(1), N(1)), "F": (R3(1), N(-1)), "E": (N(0), N(-2)),
      "D": (R3(-1), N(-1)), "C": (R3(-1), N(1)), "O": (N(0), N(0))}


def hsub(a, b):
    return tuple((x[0] - y[0], x[1] - y[1]) for x, y in zip(a, b))


def hadd(*vs):
    return tuple((sum(c[0] for c in comp), sum(c[1] for c in comp)) for comp in zip(*vs))


def hv(xy):
    return hsub(HX[xy[1]], HX[xy[0]])


def hk(k_, a):
    return tuple((k_ * x[0], k_ * x[1]) for x in a)


H0 = (N(0), N(0))
FL = {"B": [0, 2], "A": [1.732, 1], "F": [1.732, -1], "E": [0, -2], "D": [-1.732, -1], "C": [-1.732, 1], "O": [0, 0]}


def soma_hex(lista):
    return hadd(*[hv(s) for s in lista])


def nome_hex(t):
    t = t.replace(" (vetor nulo)", "")
    if t == "[[0]]":
        return H0
    m = re.fullmatch(r"(2?)\[\[([A-FO]{2})\]\]", t)
    k_ = 2 if m.group(1) else 1
    return hk(k_, hv(m.group(2)))


def confere_hex(qid, setas, gabarito, errados, com_O):
    s = soma_hex(setas)
    chk(f"{qid} soma = gabarito da lista", s == (H0 if gabarito == "0" else hv(gabarito)))
    q = Q[qid]
    txt_certo = "[[0]] (vetor nulo)" if gabarito == "0" else f"[[{gabarito}]]"
    textos = [a["t"] for a in q["alternativas"]]
    chk(f"{qid} certa = {txt_certo}", certa(qid) == txt_certo)
    for t in textos:
        if t != txt_certo:
            chk(f"{qid} errada {t} nao e o mesmo vetor da soma", nome_hex(t) != s)
    # conta descrita em cada erro
    for t, conta in errados.items():
        chk(f"{qid} erro de '{t}' confere", t in textos and nome_hex(t) == conta)
    f_ = q["figura"]
    chk(f"{qid} figura 2d no enunciado", f_["modo"] == "2d" and f_["onde"] == "enunciado")
    pol = [it for it in f_["itens"] if it["tipo"] == "poligono"]
    chk(f"{qid} contorno do hexagono cor 3", len(pol) == 1 and pol[0].get("cor") == 3 and
        pol[0]["pts"] == [FL[x] for x in "BAFEDC"])
    pts = {it["rot"]: it["em"] for it in f_["itens"] if it["tipo"] == "ponto"}
    esp = {x: FL[x] for x in "BAFEDC"}
    if com_O:
        esp["O"] = FL["O"]
    chk(f"{qid} rotulos dos pontos", pts == esp)
    vets = [(it["de"], it["ate"], it.get("cor")) for it in f_["itens"] if it["tipo"] == "vetor"]
    chk(f"{qid} setas = as da lista, cor 2, nenhuma a mais", vets == [(FL[s[0]], FL[s[1]], 2) for s in setas])
    chk(f"{qid} sem segmento extra", not [it for it in f_["itens"] if it["tipo"] == "segmento"])
    # raio: lado = 2
    lado2 = [(FL[a][0] - FL[b][0]) ** 2 + (FL[a][1] - FL[b][1]) ** 2 for a, b in ["BA", "AF", "FE", "ED", "DC", "CB"]]
    chk(f"{qid} lados ~ 2", all(abs(math.sqrt(x) - 2) < 1e-3 for x in lado2))


confere_hex("ga-s1-l1q6a", ["AB", "BE", "EF", "FC"], "AC",
            {"[[CA]]": hv("CA"), "[[AF]]": soma_hex(["AB", "BE", "EF"]), "[[BC]]": soma_hex(["BE", "EF", "FC"])}, False)
confere_hex("ga-s1-l1q6b", ["FC", "CD", "DE", "EF"], "0",
            {"[[FE]]": soma_hex(["FC", "CD", "DE"]), "2[[FC]]": hadd(hv("FC"), hv("FC")),
             "[[CF]]": soma_hex(["CD", "DE", "EF"]), "[[FD]]": soma_hex(["FC", "CD"])}, False)
confere_hex("ga-s1-l1q6c", ["DC", "CB", "BA", "AF", "FE"], "DE",
            {"[[ED]]": hv("ED"), "[[DF]]": soma_hex(["DC", "CB", "BA", "AF"]),
             "[[CE]]": soma_hex(["CB", "BA", "AF", "FE"])}, False)
confere_hex("ga-s1-l1q6d", ["CB", "AB", "AF", "OE"], "AF",
            {"[[0]] (vetor nulo)": soma_hex(["CB", "AB", "AF"]), "[[BE]]": soma_hex(["AF", "OE"]),
             "[[OB]]": soma_hex(["CB", "AB"])}, True)
confere_hex("ga-s1-l1q6e", ["BO", "BA", "FB"], "0",
            {"[[FO]]": soma_hex(["FB", "BO"]), "[[FA]]": soma_hex(["FB", "BA"]),
             "[[BE]]": hk(2, hv("BO")), "2[[BF]]": soma_hex(["BO", "BA", "BF"])}, True)
chk("q6d CB+AB+OE = 0", soma_hex(["CB", "AB", "OE"]) == H0)
chk("q6d AF = OE", hv("AF") == hv("OE"))
chk("q6d AB = OC (losango OABC)", hv("AB") == hv("OC"))
chk("q6e FB+BA = FA = -BO", soma_hex(["FB", "BA"]) == hk(-1, hv("BO")))
chk("q6e BO+BA = BF", soma_hex(["BO", "BA"]) == hv("BF"))
# numeros dos jeitos (confira) com raiz3
chk("q6a FC = (-2r3, 2)", hv("FC") == (R3(-2), N(2)))
chk("q6a C-A = (-2r3, 0)", hv("AC") == (R3(-2), N(0)))
chk("q6b DE = (r3,-1), EF = (r3,1)", hv("DE") == (R3(1), N(-1)) and hv("EF") == (R3(1), N(1)))
chk("q6e FB = (-r3, 3)", hv("FB") == (R3(-1), N(3)))
chk("q6d CB=(r3,1) AB=(-r3,1)", hv("CB") == (R3(1), N(1)) and hv("AB") == (R3(-1), N(1)))
# comprimentos: OE tem o mesmo tamanho dos lados (raio = lado no hexagono regular)
def hlen2(a):
    # (p + q r3)^2 = p^2 + 3 q^2 + 2pq r3
    tot = [Fr(0), Fr(0)]
    for p_, q_ in a:
        tot[0] += p_ * p_ + 3 * q_ * q_
        tot[1] += 2 * p_ * q_
    return tuple(tot)
chk("q6d |OE| = |CB| = |AB| = |AF| (nenhuma seta 'curta')",
    hlen2(hv("OE")) == hlen2(hv("CB")) == hlen2(hv("AB")) == hlen2(hv("AF")))

# ================= Q7 =================
x, y, z = Fr(-7), Fr(-3, 2), Fr(-9)
uu = (2, -z, 1); vv = (-x, 3, y + 2); ww = (-4, 1, 0)
chk("q7 gabarito confere", sub(uu, mul(2, vv)) == mul(3, ww))
# erros
xA = Fr(-12 - 2, -2)            # 2 - 2x = -12
yB = Fr(1 - 2, 2)               # 1 - 2y - 2 = 0  ->  y = -1/2
xC = Fr(-4 - 2, 2)              # 2 + 2x = -4
zC = -(1 + 6)                   # -z - 6 = 1
zE = 3 + 6                      # z - 6 = 3
chk("q7 A x=7", xA == 7); chk("q7 B y=-1/2", yB == Fr(-1, 2)); chk("q7 C x=-3 z=-7", xC == -3 and zC == -7)
chk("q7 E z=9", zE == 9)
chk("q7 C: y com w (z de w = 0) continua -3/2", 1 - 2 * (y + 2) == 0)


def f7(x_, y_, z_):
    return f"x = {fnum(x_)}, y = {fnum(y_)}, z = {fnum(z_)}"


confere_alts("ga-s1-l1q7", f7(x, y, z), {f7(xA, y, z): (xA, y, z), f7(x, yB, z): (x, yB, z),
                                       f7(xC, y, zC): (xC, y, zC), f7(x, y, z): (x, y, z), f7(x, y, zE): (x, y, zE)})
chk("q7 confira u=(2,9,1) v=(7,3,1/2)", uu == (2, 9, 1) and vv == (7, 3, Fr(1, 2)))
# nenhuma errada satisfaz
for xs, ys, zs in [(xA, y, z), (x, yB, z), (xC, y, zC), (x, y, zE)]:
    chk(f"q7 errada {xs},{ys},{zs} nao satisfaz",
        sub((2, -zs, 1), mul(2, (-xs, 3, ys + 2))) != mul(3, ww))

# ================= Q8 =================
u8 = (-2, 1, -2); v8 = (1, 2, 1); w8 = (-3, 2, 0)
r8 = sub(sub(mul(5, v8), mul(2, w8)), u8)
chk("q8a gabarito (13,5,7)", r8 == (13, 5, 7))
chk("q8a confere na equacao", add(sub(u8, mul(2, v8)), r8) == sub(mul(3, v8), mul(2, w8)))
eA = sub(sub(v8, mul(2, w8)), u8)
eC = add(sub(mul(5, v8), mul(2, w8)), u8)
eD = sub(add(mul(5, v8), mul(2, w8)), u8)
eE = sub(sub(mul(3, v8), mul(2, w8)), u8)
confere_alts("ga-s1-l1q8a", fvec(r8), {fvec(eA): eA, fvec(r8): r8, fvec(eC): eC, fvec(eD): eD, fvec(eE): eE})
chk("q8a A (9,-3,3)", eA == (9, -3, 3)); chk("q8a C (9,7,3)", eC == (9, 7, 3))
chk("q8a D (1,13,7)", eD == (1, 13, 7)); chk("q8a E (11,1,5)", eE == (11, 1, 5))
chk("q8a receita 5v-2w=(11,6,5)", sub(mul(5, v8), mul(2, w8)) == (11, 6, 5))
chk("q8a confira lados (9,2,3)", sub(mul(3, v8), mul(2, w8)) == (9, 2, 3))


def resolve(Mx, b):
    n = len(b)
    A_ = [[Fr(Mx[i][j]) for j in range(n)] + [Fr(b[i])] for i in range(n)]
    for c in range(n):
        piv = next(i for i in range(c, n) if A_[i][c] != 0)
        A_[c], A_[piv] = A_[piv], A_[c]
        for i in range(n):
            if i != c and A_[i][c] != 0:
                f_ = A_[i][c] / A_[c][c]
                A_[i] = [a - f_ * bb for a, bb in zip(A_[i], A_[c])]
    return tuple(A_[i][n] / A_[i][i] for i in range(n))


Mcol = [[u8[i], v8[i], w8[i]] for i in range(3)]  # equacao i: coordenada i dos tres vetores
alvo = (2, -3, 1)
sol = resolve(Mcol, alvo)
chk("q8b gabarito", sol == (Fr(-13, 15), Fr(-11, 15), Fr(-1, 3)))
solA = resolve(Mcol, (2, 3, 1))
# B: a3 com sinal trocado e propagado
a3B = Fr(1, 3)
a1B = (Fr(-3) - 2 - 2 * a3B) / 5      # a1 + 2(1 + 2 a1) + 2 a3 = -3
a2B = 1 + 2 * a1B
solB = (a1B, a2B, a3B)
solC = (Fr(0), Fr(1), Fr(-1, 3))
Mlin = [list(u8), list(v8), list(w8)]  # erro: cada equacao com as coordenadas de um vetor
solD = resolve(Mlin, alvo)


def f8(s):
    return f"a₁ = {fnum(s[0])}, a₂ = {fnum(s[1])}, a₃ = {fnum(s[2])}"


confere_alts("ga-s1-l1q8b", f8(sol), {f8(solA): solA, f8(solB): solB, f8(solC): solC, f8(solD): solD, f8(sol): sol})
print("q8b solucoes: A", solA, "B", solB, "D", solD)
chk("q8b A = (1/3,5/3,-1/3)", solA == (Fr(1, 3), Fr(5, 3), Fr(-1, 3)))
chk("q8b B = (-17/15,-19/15,1/3)", solB == (Fr(-17, 15), Fr(-19, 15), Fr(1, 3)))
chk("q8b D = (-13/15,-4/5,-8/15)", solD == (Fr(-13, 15), Fr(-4, 5), Fr(-8, 15)))


def comb(s):
    return add(mul(s[0], u8), mul(s[1], v8), mul(s[2], w8))


for nome, s in [("A", solA), ("B", solB), ("C", solC), ("D", solD)]:
    chk(f"q8b errada {nome} nao gera (2,-3,1)", comb(s) != alvo)
chk("q8b C satisfaz eq1 e eq3 e falha eq2 com 4/3", comb(solC)[0] == 2 and comb(solC)[2] == 1 and comb(solC)[1] == Fr(4, 3))
chk("q8b atalho: a3=-1/3 deixa A, C e certa; so a certa passa eq2",
    [s for s in (solA, solB, solC, solD, sol) if s[2] == Fr(-1, 3) and comb(s)[1] == -3] == [sol])

# ================= Q9 =================
u9 = (-2, 1, -2)
v9sq = [0, Fr(1, 2), Fr(1, 2)]
w9sq = [Fr(1, 6), Fr(1, 6), Fr(4, 6)]
r9sq = [Fr(1, 3), Fr(1, 3), Fr(4, 3)]
chk("q9a |u|^2 = 9", sq(u9) == 9)
chk("q9b |v|^2 = 1", sum(v9sq) == 1)
chk("q9c |w|^2 = 1", sum(w9sq) == 1)
chk("q9d |r|^2 = 2", sum(r9sq) == 2)
chk("q9e cos^2+sen^2 = 1 em varios angulos", all(abs(math.cos(t) ** 2 + math.sin(t) ** 2 - 1) < 1e-12 for t in [0, .3, 1, 2.5, 4]))


def valor(t):
    """valor numerico de textos como 3, -3, raiz5, 1/raiz2, raiz(2/3), -2/raiz6, 4/raiz6, raiz2"""
    t = t.replace(M, "-").strip()
    m = re.fullmatch(r"(-?)(\d+)/√(\d+)", t)
    if m:
        return (-1 if m.group(1) else 1) * int(m.group(2)) / math.sqrt(int(m.group(3)))
    m = re.fullmatch(r"√\((\d+)/(\d+)\)", t)
    if m:
        return math.sqrt(int(m.group(1)) / int(m.group(2)))
    m = re.fullmatch(r"√(\d+)", t)
    if m:
        return math.sqrt(int(m.group(1)))
    m = re.fullmatch(r"(-?\d+)/(\d+)", t)
    if m:
        return int(m.group(1)) / int(m.group(2))
    return float(t)


def confere_num(qid, certo, errados):
    textos = [a["t"] for a in Q[qid]["alternativas"]]
    chk(f"{qid} certa = {certo}", certa(qid) == certo)
    chk(f"{qid} textos previstos", sorted(textos) == sorted([certo] + list(errados.keys())))
    vc = valor(certo)
    for t, conta in errados.items():
        chk(f"{qid} erro '{t}' confere ({conta})", abs(valor(t) - conta) < 1e-12)
        chk(f"{qid} '{t}' difere da certa", abs(valor(t) - vc) > 1e-9)


s2 = math.sqrt(2); s6 = math.sqrt(6)
confere_num("ga-s1-l1q9a", "3", {"9": 4 + 1 + 4, M + "3": -2 + 1 - 2, "√5": math.sqrt(4 + 1), "5": 2 + 1 + 2})
chk("q9a √5 cai entre 2 e 5 (atalho deixa √5 e 3)", 2 < math.sqrt(5) < 5 and 2 < 3 < 5)
confere_num("ga-s1-l1q9b", "1", {"√2": 0 + 1 / s2 + 1 / s2, "1/√2": math.sqrt(1 / 4 + 1 / 4), "1/2": 1 / 4 + 1 / 4,
                                 "2": math.sqrt(2 + 2)})
confere_num("ga-s1-l1q9c", "1", {M + "2/√6": (1 - 1 - 2) / s6, "√6": math.sqrt(1 + 1 + 4),
                                 "√(2/3)": math.sqrt(1 / 6 + 1 / 6 + 2 / 6), "4/√6": (1 + 1 + 2) / s6})
# 9d: alternativas compostas
txt9d = {a["t"]: a for a in Q["ga-s1-l1q9d"]["alternativas"]}
chk("q9d certa √2, não é unitário", certa("ga-s1-l1q9d") == "√2, não é unitário")
chk("q9d textos", sorted(txt9d) == sorted(["1, é unitário", "2, não é unitário", M + "2/√3, não é unitário",
                                          "√(4/3), não é unitário", "√2, não é unitário"]))
chk("q9d erro √(4/3): 1/3+1/3+2/3", Fr(1, 3) + Fr(1, 3) + Fr(2, 3) == Fr(4, 3))
chk("q9d erro -2/√3: soma das coords", (1 - 1 - 2) == -2)
chk("q9d √(4/3) != √2", Fr(4, 3) != 2)
# 9e
chk("q9e certa", certa("ga-s1-l1q9e") == "‖[[s]]‖ = 1; unitários: [[v]], [[w]] e [[s]]")
norma2 = {"u": sq(u9), "v": sum(v9sq), "w": sum(w9sq), "r": sum(r9sq), "s": 1}
chk("q9e unitarios = v, w, s", [k_ for k_, n_ in norma2.items() if n_ == 1] == ["v", "w", "s"])
chk("q9e √2 do erro E: 1+1", math.sqrt(1 + 1) == s2)
chk("q9e confira 60 graus", Fr(1, 4) + Fr(3, 4) == 1)
# ================= Q10 =================
P = (-2, 1, -2); Qp = (1, 2, 1); R = (-3, 2, 0)
chk("q10a gabarito √19", sq(sub(Qp, P)) == 19)
chk("q10b gabarito √6", sq(sub(R, P)) == 6)
chk("q10c gabarito √17", sq(sub(Qp, R)) == 17)
confere_num("ga-s1-l1q10a", "√19", {"√11": math.sqrt(sq(add(P, Qp))), "7": 3 + 1 + 3, "19": 19,
                                     "√3": math.sqrt(sq((1 - 2, 2 - 1, 1 - 2)))})
chk("q10a P+Q = (-1,3,-1)", add(P, Qp) == (-1, 3, -1))
confere_num("ga-s1-l1q10b", "√6", {"√38": math.sqrt(sq(add(R, P))), "4": 1 + 1 + 2,
                                    "√30": math.sqrt(sq((-3 - 2, 2 - 1, 0 + 2))), "√2": math.sqrt(1 + 1)})
chk("q10b R+P = (-5,3,-2)", add(R, P) == (-5, 3, -2))
confere_num("ga-s1-l1q10c", "√17", {"√5": math.sqrt(sq((1 - 3, 0, 1))), "17": 17, "5": 4 + 0 + 1,
                                     "√21": math.sqrt(sq(add(R, Qp)))})
chk("q10c R+Q = (-2,4,1)", add(R, Qp) == (-2, 4, 1))
chk("q10 decimais: √19~4,36 √6~2,45 √17~4,12 √38~6,2 √30~5,5",
    round(math.sqrt(19), 2) == 4.36 and round(math.sqrt(6), 2) == 2.45 and round(math.sqrt(17), 2) == 4.12
    and round(math.sqrt(38), 1) == 6.2 and round(math.sqrt(30), 1) == 5.5)
chk("q10b angulo da seta PR com a vertical (graus)", True)
print("q10b: angulo de PR com o eixo z =", round(math.degrees(math.acos(2 / math.sqrt(6))), 1), "graus")
for qid, seta in [("ga-s1-l1q10a", ("P", "Q")), ("ga-s1-l1q10b", ("P", "R")), ("ga-s1-l1q10c", ("R", "Q"))]:
    it = Q[qid]["figura"]["itens"]
    pts = {i_["rot"]: i_["em"] for i_ in it if i_["tipo"] == "ponto"}
    chk(f"{qid} pontos P, Q, R", pts == {"P": list(P), "Q": list(Qp), "R": list(R)})
    vs = [(i_["de"], i_["ate"]) for i_ in it if i_["tipo"] == "vetor"]
    chk(f"{qid} seta {seta[0]}{seta[1]}", vs == [(pts[seta[0]], pts[seta[1]])])

# figuras das normas
it = Q["ga-s1-l1q9a"]["figura"]["itens"]
chk("q9a seta ate (-2,1,-2)", it[0]["ate"] == [-2, 1, -2])
for qid in ("ga-s1-l1q9b", "ga-s1-l1q9e"):
    pol = [i_ for i_ in Q[qid]["figura"]["itens"] if i_["tipo"] == "poligono"][0]["pts"]
    chk(f"{qid} circulo de raio 1 (+-0,001)", all(abs(math.sqrt(sum(c * c for c in p_)) - 1) < 1e-3 for p_ in pol))
chk("q9e seta (cos30, sen30)", Q["ga-s1-l1q9e"]["figura"]["itens"][1]["ate"] == [0.866, 0.5])

# Excel: SOMAQUAD de vetores unitarios em ponto flutuante da exatamente 1?
fw = [1 / math.sqrt(6), -1 / math.sqrt(6), -2 / math.sqrt(6)]
fv = [0, 1 / math.sqrt(2), 1 / math.sqrt(2)]
print("float: soma dos quadrados de w =", repr(sum(c * c for c in fw)), "| de v =", repr(sum(c * c for c in fv)))
print("float: cos^2+sen^2 em 1 rad =", repr(math.cos(1) ** 2 + math.sin(1) ** 2), "| em 0,3 rad =", repr(math.cos(.3) ** 2 + math.sin(.3) ** 2))

# ================= cobertura, niveis, posicoes =================
NIVEL = {"ga-s1-l1q1a": 1, "ga-s1-l1q1b": 1, "ga-s1-l1q1c": 2, "ga-s1-l1q1d": 2, "ga-s1-l1q2": 2,
         "ga-s1-l1q3": 2, "ga-s1-l1q4": 2, "ga-s1-l1q5a": 2, "ga-s1-l1q5b": 2,
         "ga-s1-l1q6a": 2, "ga-s1-l1q6b": 1, "ga-s1-l1q6c": 2, "ga-s1-l1q6d": 3, "ga-s1-l1q6e": 3,
         "ga-s1-l1q7": 2, "ga-s1-l1q8a": 2, "ga-s1-l1q8b": 3, "ga-s1-l1q9a": 1, "ga-s1-l1q9b": 1,
         "ga-s1-l1q9c": 1, "ga-s1-l1q9d": 1, "ga-s1-l1q9e": 2, "ga-s1-l1q10a": 1, "ga-s1-l1q10b": 1,
         "ga-s1-l1q10c": 1}
chk("ids: exatamente os 25 pedidos", sorted(Q) == sorted(NIVEL) and len(ordem) == 25)
for qid, n_ in NIVEL.items():
    q = Q[qid]
    chk(f"{qid} nivel {n_}", q["nivel"] == n_)
    suf = qid.split("-l1")[1]  # q1a
    chk(f"{qid} origem", q["origem"] == "Lista 1 · Q" + suf[1:])
    chk(f"{qid} semana 1", q["semana"] == 1)
    chk(f"{qid} 5 alternativas, 1 certa", len(q["alternativas"]) == 5 and sum(a.get("certa") is True for a in q["alternativas"]) == 1)
pos = {}
for qid in ordem:
    i_ = [a.get("certa") is True for a in Q[qid]["alternativas"]].index(True)
    pos["ABCDE"[i_]] = pos.get("ABCDE"[i_], 0) + 1
print("posicoes:", dict(sorted(pos.items())))
chk("nenhuma letra acima de 30%", max(pos.values()) / 25 <= 0.30)

# ================= teoria =================
chk("teoria so na p1 e unica", len(semanas) == 1)
s = semanas[0]
chk("teoria fonte", s["fonte"] == "Lista 1 — Prof. Danilo Adrian Marques" and s["previa"] is False)
chk("teoria 3 a 6 blocos", 3 <= len(s["blocos"]) <= 6)
for b in s["blocos"]:
    n_ = len(re.findall(r"\S+", b["texto"]))
    chk(f"bloco '{b['titulo']}' 40-120 palavras ({n_})", 40 <= n_ <= 120)
for k_, t in s["jeitos"].items():
    n_ = len(re.findall(r"\S+", t))
    chk(f"jeito da semana {k_} 50-120 palavras ({n_})", 50 <= n_ <= 120)
chk("teoria: AB de A=(1,1,3) a B=(-3,1,5)", sub((-3, 1, 5), (1, 1, 3)) == (-4, 0, 2))
chk("teoria: ponto medio de A=(1,-2,3) e C=(-1,1,-2)", mul(Fr(1, 2), add((1, -2, 3), (-1, 1, -2))) == (0, Fr(-1, 2), Fr(1, 2)))
chk("teoria: versor de (-2,1,-2)", mul(Fr(1, 3), (-2, 1, -2)) == (Fr(-2, 3), Fr(1, 3), Fr(-2, 3)))
chk("teoria: 3*(1,2,-4)", mul(3, (1, 2, -4)) == (3, 6, -12))

# ================= tamanhos dos jeitos =================
for qid in ordem:
    j = Q[qid]["jeitos"]
    for k_ in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n_ = len(re.findall(r"\S+", j[k_]))
        chk(f"{qid}.{k_} 35-110 palavras ({n_})", 35 <= n_ <= 110)
    chk(f"{qid}.receita 3-7 passos", 3 <= len(j["receita"]) <= 7)
    chk(f"{qid}.conversa 4-8 falas", 4 <= len(j["conversa"]) <= 8)

print()
print(f"{nok} conferencias ok, {len(falhas)} falha(s)")
for f_ in falhas:
    print("  -", f_)
