# Revisor adversarial - lote ga_s2a (Lista 2, Q1 a-n).
# Refaz do zero cada resposta e cada distrator com Fraction e compara
# com o texto exato das alternativas nos JSON. Confere tambem os numeros
# citados nos jeitos, as figuras e o tamanho dos textos.
import json, os, re, sys, math
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
ARQS = [os.path.join(DADOS, "ga_s2a_p%d.json" % i) for i in (1, 2, 3)]

MENOS = "−"
falhas = []


def ok(cond, msg):
    if not cond:
        falhas.append(msg)
        print("FALHA:", msg)


def fmt(x):
    x = F(x)
    s = str(abs(x.numerator)) if x.denominator == 1 else "%d/%d" % (abs(x.numerator), x.denominator)
    return (MENOS + s) if x < 0 else s


def fv(v):
    return "(" + ", ".join(fmt(c) for c in v) + ")"


def dot(a, b):
    return sum(F(x) * F(y) for x, y in zip(a, b))


def cross(a, b):
    a = [F(x) for x in a]; b = [F(x) for x in b]
    return (a[1] * b[2] - a[2] * b[1],
            -(a[0] * b[2] - a[2] * b[0]),
            a[0] * b[1] - a[1] * b[0])


def comp(a, b):
    return tuple(F(x) * F(y) for x, y in zip(a, b))


def add(a, b):
    return tuple(F(x) + F(y) for x, y in zip(a, b))


def sub(a, b):
    return tuple(F(x) - F(y) for x, y in zip(a, b))


def esc(k, a):
    return tuple(F(k) * F(x) for x in a)


def norma(a):
    return math.sqrt(float(dot(a, a)))


def ang(a, b):
    return math.degrees(math.acos(float(dot(a, b)) / (norma(a) * norma(b))))


u = (F(1), F(4), F(3))
v = (F(-1), F(1), F(-1))
w = (F(-2), F(-1, 2), F(5))
z = (F(-1), F(2), F(-3))

# ---------------------------------------------------------------
# 1. Gabarito do PDF (pagina 2), digitado a partir da leitura do PDF
GAB_PDF = {
    "a": F(0), "b": F(11), "c": F(-2), "d": F(-7, 2), "e": F(6), "f": F(-14),
    "g": F(26), "h": F(3), "i": F(117, 4), "j": F(14),
    "k": (F(-7), F(-2), F(5)), "l": (F(43, 2), F(-11), F(15, 2)),
    "m": (F(9, 2), F(7), F(5, 2)), "n": (F(-9, 2), F(-7), F(-5, 2)),
}
MINHA = {
    "a": dot(u, v), "b": dot(u, w), "c": dot(u, z), "d": dot(v, w), "e": dot(v, z),
    "f": dot(w, z), "g": dot(u, u), "h": dot(v, v), "i": dot(w, w), "j": dot(z, z),
    "k": cross(u, v), "l": cross(u, w), "m": cross(v, w), "n": cross(w, v),
}
for k in GAB_PDF:
    ok(GAB_PDF[k] == MINHA[k], "gabarito %s: PDF %s x conta %s" % (k, GAB_PDF[k], MINHA[k]))


def fx(x):
    return fv(x) if isinstance(x, tuple) else fmt(x)


# ---------------------------------------------------------------
# 2. Alternativas esperadas, cada uma refeita pela conta descrita no "erro"
def meio_trocado(c):
    return (c[0], -c[1], c[2])


def soma_abs(a, b):
    return sum(abs(p) for p in comp(a, b))


w_y_pos = (F(-2), F(1, 2), F(5))       # y de w copiado com +1/2
w_y_m2 = (F(-2), F(-2), F(5))          # -1/2 lido como -2

# item m, alternativa D: (-1)*(-1/2) feito como -1/2 nos dois produtos com a fracao
m_x_err = v[1] * w[2] - (F(-1, 2))     # 1*5 - (-1/2)
m_z_err = F(-1, 2) - v[1] * w[0]       # (-1/2) - 1*(-2)

ESPERADO = {
    "a": ["(−1, 4, −3); os vetores são ortogonais",
          "0; os vetores são ortogonais",
          "0; os vetores são paralelos",
          fmt(F(-1) + 4 + 3) + "; o ângulo entre eles é agudo",
          fv(cross(u, v)) + "; os vetores são ortogonais"],
    "b": [fmt(dot(u, (F(-2), F(1, 2), F(5)))), fv(comp(u, w)), fmt(dot(u, w_y_m2)), fmt(dot(u, w)), fmt(soma_abs(u, w))],
    "c": [fmt(dot(u, z)), fmt(F(-1) + 8 + 9), fv(comp(u, z)), fmt(soma_abs(u, z)), fmt(sum(add(u, z)))],
    "d": [fmt(F(2) + F(1, 2) - 5), fv(comp(v, w)), fmt(F(-2) - F(1, 2) - 5), fmt(F(-3 - 1, 2)), fmt(dot(v, w))],
    "e": [fmt(F(-1) + 2 - 3), fv(comp(v, z)), fmt(dot(v, z)), fmt(sum(add(v, z))), fmt(F(1) + 2 - 3)],
    "f": [fmt(F(2) + 1 - 15), fmt(dot(w, z)), fv(comp(w, z)), fmt(F(-2) - 1 - 15), fmt(sum(add(w, z)))],
    "g": ["√26", fv(comp(u, u)), fmt(sum(u) ** 2), fmt(sum(u)), fmt(dot(u, u))],
    "h": [fmt(dot(v, v)), fmt(F(-1) + 1 - 1), "√3", fmt(sum(v) ** 2), fv(comp(v, v))],
    "i": [fmt(F(4) - F(1, 4) + 25), fmt(F(4) + F(1, 2) + 25), fmt(dot(w, w)), "√117/2", fv(comp(w, w))],
    "j": [fmt(F(-1) + 4 - 9), "√14", fv(comp(z, z)), fmt(dot(z, z)), fmt(sum(z) ** 2)],
    "k": [fv(meio_trocado(cross(u, v))), fv(cross(v, u)), fv(cross(u, v)), fv(comp(u, v)), fmt(dot(u, v))],
    "l": [fv(meio_trocado(cross(u, w))), fv(comp(u, w)), fv(cross(w, u)), fv(cross(u, w)), fv(cross(u, w_y_pos))],
    "m": [fv(cross(v, w)), fv(meio_trocado(cross(v, w))), fv(comp(v, w)), fv((m_x_err, cross(v, w)[1], m_z_err)), fv(cross(w, v))],
    "n": [fv(cross(v, w)), fv(cross(w, v)), fv(meio_trocado(cross(w, v))), fmt(dot(w, v)), fv(comp(w, v))],
}
# posicoes depois da revisao (g, j, k, n reordenados para quebrar o ciclo B-D-A)
CERTA = {"a": 1, "b": 3, "c": 0, "d": 4, "e": 2, "f": 1, "g": 4, "h": 0, "i": 2, "j": 3,
         "k": 2, "l": 3, "m": 0, "n": 1}
from collections import Counter
cont = Counter("ABCDE"[i] for i in CERTA.values())
print("posições:", "".join("ABCDE"[CERTA[c]] for c in "abcdefghijklmn"), dict(sorted(cont.items())))
ok(max(cont.values()) / 14 <= 0.30, "letra acima de 30%")

# conferencias pontuais de valores que entram nas alternativas
ok(math.isclose(math.sqrt(26), norma(u)), "norma u")
ok(math.isclose(math.sqrt(3), norma(v)), "norma v")
ok(math.isclose(math.sqrt(117) / 2, norma(w)), "norma w = √117/2")
ok(math.isclose(math.sqrt(14), norma(z)), "norma z")

qs = {}
semana = None
for p in ARQS:
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    for s in d.get("semanas", []):
        semana = s
    for q in d["questoes"]:
        qs[q["id"]] = q

ids_pedidos = ["ga-s2-l2q1" + c for c in "abcdefghijklmn"]
ok(sorted(qs) == sorted(ids_pedidos), "ids: %s" % sorted(qs))

NIVEL = {c: 1 for c in "abcdefghj"}
NIVEL.update({c: 2 for c in "iklmn"})

for c in "abcdefghijklmn":
    q = qs["ga-s2-l2q1" + c]
    alts = q["alternativas"]
    textos = [a["t"] for a in alts]
    certas = [i for i, a in enumerate(alts) if a.get("certa")]
    ok(certas == [CERTA[c]], "%s: posição da certa %s" % (c, certas))
    ok(textos == ESPERADO[c], "%s: alternativas\n  json %s\n  esp. %s" % (c, textos, ESPERADO[c]))
    # a certa bate com o gabarito do PDF (sem o sufixo de leitura no item a)
    tc = textos[certas[0]].split(";")[0]
    ok(tc == fx(GAB_PDF[c]), "%s: certa %s x PDF %s" % (c, tc, fx(GAB_PDF[c])))
    # nenhuma errada equivale à certa (comparação numérica)
    for i, t in enumerate(textos):
        if i == certas[0]:
            continue
        ok(t != textos[certas[0]], "%s: errada igual à certa" % c)
    ok(q["nivel"] == NIVEL[c], "%s: nível %s" % (c, q["nivel"]))
    ok(q["origem"] == "Lista 2 · Q1" + c, "%s: origem" % c)
    ok(q["semana"] == 2, "%s: semana" % c)
    ok(q["enunciado"].startswith("Sendo [[u]] = (1, 4, 3), [[v]] = (−1, 1, −1), [[w]] = (−2, −1/2, 5) e [[z]] = (−1, 2, −3). Calcular: " + c + ") "), "%s: enunciado" % c)

# equivalencias que o texto pode esconder: √117/2 x 117/4 etc.
ok(not math.isclose(math.sqrt(117) / 2, 117 / 4), "√117/2 ≠ 117/4")
ok(not math.isclose(math.sqrt(26), 26), "√26 ≠ 26")

# ---------------------------------------------------------------
# 3. Numeros citados nos jeitos e na teoria
print("ângulos:")
for nome, a, b, citado in [("u,w", u, w, 66.49), ("u,z", u, z, 96.02), ("v,w", v, w, 111.94),
                           ("v,z", v, z, 22.21), ("w,z", w, z, 133.78), ("u,v", u, v, 90.0)]:
    t = ang(a, b)
    print("  %s = %.4f" % (nome, t))
    ok(round(t, 2) == citado, "ângulo %s: %.4f x citado %s" % (nome, t, citado))
cosvz = float(dot(v, z)) / (norma(v) * norma(z))
ok(round(cosvz, 4) == 0.9258, "cos(v,z) %.5f" % cosvz)
ok(round(math.sqrt(78), 2) == 8.83, "√78")
ok(round(math.sqrt(78) / 2, 2) == 4.42, "√78/2 %.4f" % (math.sqrt(78) / 2))
ok(dot(cross(u, v), cross(u, v)) == 78, "|u×v|² = 78")
nuw = math.sqrt(float(dot(cross(u, w), cross(u, w))))
nvw = math.sqrt(float(dot(cross(v, w), cross(v, w))))
print("  |u×w| = %.4f   |v×w| = %.4f" % (nuw, nvw))
ok(round(nuw, 2) == 25.29, "|u×w|")
ok(round(nvw, 2) == 8.69, "|v×w|")
ok(norma(u) * norma(w) > 27, "|u||w| > 27: %.4f" % (norma(u) * norma(w)))
# item c confira
ok(round(math.sqrt(26), 2) == 5.10 and round(math.sqrt(14), 2) == 3.74, "normas c")
ok(round(-2 / (5.10 * 3.74), 3) == -0.105, "cos c %.5f" % (-2 / (5.10 * 3.74)))
ok(round(16 / (norma(u) * norma(z)), 2) == 0.84, "cos 16 c")
ok(dot(add(u, z), add(u, z)) == 26 + 2 * (-2) + 14, "‖u+z‖² regra")
# item e confira
ok(add(v, z) == (-2, 3, -4) and dot(add(v, z), add(v, z)) == 29 == 3 + 12 + 14, "e confira 29")
ok(3 + 0 + 14 == 17, "e confira 17")
ok(sum(v) * sum(z) == 2, "e trabalho SUM*SUM")
# item f confira
ok(sub(w, z) == (-1, F(-5, 2), 8), "w - z")
ok(dot(sub(w, z), sub(w, z)) == F(285, 4) == F(117, 4) + 28 + 14, "f confira 285/4")
# item b/d/i confira pelo dobro
ok(esc(2, w) == (-4, -1, 10), "2w")
ok(dot(u, esc(2, w)) == 22, "u·2w = 22")
ok(dot(v, esc(2, w)) == -7, "v·2w = -7")
ok(dot(esc(2, w), esc(2, w)) == 117, "2w·2w = 117")
# item d e i decimais
ok(float(F(-7, 2)) == -3.5 and float(F(117, 4)) == 29.25, "decimais")
ok(float(F(59, 2)) == 29.5 and float(F(115, 4)) == 28.75, "decimais distratores i")
# item g cotidiano / confira
ok(25 < 26 and dot((3, 4, 0), (3, 4, 0)) == 25, "g caixa")
ok(5 < math.sqrt(26) < 6, "g √26 entre 5 e 6")
# item j
ok(math.sqrt(14) < 4, "√14 < 4")
ok(dot(esc(-1, z), esc(-1, z)) == 14, "(-z)·(-z)")
# item k
ok(dot((-7, 2, 5), u) == 16 and dot((-1, 4, -3), u) == 6, "k atalho")
ok(dot(cross(u, v), u) == 0 and dot(cross(u, v), v) == 0, "k perp")
# determinantes 2x2 do trabalho do item k
ok(4 * (-1) - 3 * 1 == -7 and 1 * 1 - 4 * (-1) == 5 and 1 * (-1) - 3 * (-1) == 2, "k MATRIZ.DETERM")
# item l
cl = cross(u, w)
ok(dot(cl, u) == 0 and dot(cl, w) == 0, "l perp")
e37 = cross(u, w_y_pos)
ok(dot(e37, u) == 0 and dot(e37, w) == 11, "l distrator E: ·u=%s ·w=%s" % (dot(e37, u), dot(e37, w)))
ok(cross(u, esc(2, w)) == (43, -22, 15), "u × 2w")
ok(F(3) * (-2) - 1 * 5 == -11, "l trabalho y ciclico")
# item m
em = (m_x_err, F(7), m_z_err)
ok(dot(em, v) == 0 and dot(em, w) == -7, "m distrator D: ·v=%s ·w=%s" % (dot(em, v), dot(em, w)))
ok(dot(cross(v, w), v) == 0 and dot(cross(v, w), w) == 0, "m perp")
# item n
ok(add(cross(v, w), cross(w, v)) == (0, 0, 0), "m + n = 0")
ok(dot(cross(w, v), v) == 0 and dot(cross(w, v), w) == 0, "n perp")
# teoria: projecao de z sobre v
p = esc(dot(z, v) / dot(v, v), v)
ok(p == (-2, 2, -2), "proj z sobre v %s" % (p,))
ok(sub(z, p) == (1, 0, -1) and dot(sub(z, p), v) == 0, "z - proj")
ok(dot(u, w) == 11 and comp(u, w) == (-2, -2, 15), "teoria bloco 1")

# ---------------------------------------------------------------
# 4. Figuras
def pts_fig(q):
    return q.get("figura", {}).get("itens", []) if q.get("figura") else []


def flt(t):
    return tuple(float(x) for x in t)


VET = {"u": u, "v": v, "w": w, "z": z,
       "u × v": cross(u, v), "u × w": cross(u, w), "v × w": cross(v, w), "w × v": cross(w, v)}
for c in "abcdefghijklmn":
    q = qs["ga-s2-l2q1" + c]
    for it in pts_fig(q):
        if it["tipo"] == "vetor":
            ok(it["de"] == [0, 0, 0], "%s figura: vetor fora da origem" % c)
            ok(flt(it["ate"]) == flt(VET[it["rot"]]), "%s figura: %s ate %s" % (c, it["rot"], it["ate"]))
        if it["tipo"] == "poligono":
            print("  %s polígono %s" % (c, it["pts"]))
    if q.get("figura"):
        ok(q["figura"]["onde"] == "explicacao", "%s figura onde" % c)
par = {"k": (u, v), "l": (u, w), "m": (v, w)}
for c, (a, b) in par.items():
    q = qs["ga-s2-l2q1" + c]
    poli = [it for it in pts_fig(q) if it["tipo"] == "poligono"][0]["pts"]
    esp = [(0, 0, 0), flt(a), flt(add(a, b)), flt(b)]
    ok([flt(x) for x in poli] == esp, "%s paralelogramo %s x %s" % (c, poli, esp))
# caixas tracejadas (g, h, i)
for c, vv in (("g", u), ("h", v), ("i", w), ("j", z)):
    segs = [(flt(it["de"]), flt(it["ate"])) for it in pts_fig(qs["ga-s2-l2q1" + c]) if it["tipo"] == "segmento"]
    x, y, zz = flt(vv)
    for s in [((0, 0, 0), (x, 0, 0)), ((x, 0, 0), (x, y, 0)), ((x, y, 0), (x, y, zz))]:
        ok(s in segs, "%s caixa: falta segmento %s" % (c, s))

# ---------------------------------------------------------------
# 5. Tamanho dos textos e bytes de controle
def npal(s):
    return len(re.findall(r"\S+", s))


for c in "abcdefghijklmn":
    q = qs["ga-s2-l2q1" + c]
    j = q["jeitos"]
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n = npal(j[k])
        ok(35 <= n <= 110, "%s.%s: %d palavras" % (c, k, n))
    ok(3 <= len(j["receita"]) <= 7, "%s receita %d passos" % (c, len(j["receita"])))
    ok(4 <= len(j["conversa"]) <= 8, "%s conversa %d falas" % (c, len(j["conversa"])))
if semana:
    for i, b in enumerate(semana["blocos"]):
        n = npal(b["texto"])
        ok(40 <= n <= 120, "bloco %d: %d palavras" % (i, n))
    for k, t in semana["jeitos"].items():
        n = npal(t)
        ok(50 <= n <= 120, "semana jeito %s: %d palavras" % (k, n))
    ok(semana["fonte"] == "Lista 2 — Prof. Danilo Adrian Marques" and semana["previa"] is False, "fonte/previa")

for p in ARQS:
    with open(p, "rb") as f:
        b = f.read()
    ruins = [x for x in b if x < 32 and x not in (10, 13)]
    ok(not ruins, "%s: bytes de controle %s" % (os.path.basename(p), ruins[:5]))
    txt = b.decode("utf-8")
    # hifen como menos fora de crase, dentro de strings de texto
    sem_codigo = re.sub(r"`[^`]*`", " ", txt)
    sem_coord = re.sub(r"\[[-0-9., \[\]]+\]", " ", sem_codigo)
    for m in re.finditer(r"(^|[\s(,=])-\d", sem_coord):
        trecho = sem_coord[max(0, m.start() - 30): m.end() + 10].replace("\n", " ")
        print("  hífen-menos? %s: ...%s..." % (os.path.basename(p), trecho))
    for proib in ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada",
                  "fascinante", "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente", "!"]:
        ok(proib not in sem_codigo.lower(), "%s: proibida '%s'" % (os.path.basename(p), proib))
    ok("—" not in sem_codigo.replace("Lista 2 — Prof.", ""), "%s: travessão no texto" % os.path.basename(p))

print()
print("TOTAL DE FALHAS:", len(falhas))
print("TUDO OK" if not falhas else "HÁ FALHAS")
