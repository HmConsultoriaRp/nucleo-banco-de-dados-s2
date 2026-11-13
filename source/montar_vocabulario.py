# Monta o "Vocabulario" de Geometria (semanas 4 e 5) e grava em dados/ga_vocabulario.json.
# Desenho aprovado em 12/11/2026. Texto e contas: este arquivo (para em erro se algo nao bater).
# Cada numero dos exemplos e conferido aqui antes de gravar. Uso: python -I montar_vocabulario.py
import json
import math
import os
import sys
from fractions import Fraction as F

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, "dados", "ga_vocabulario.json")
erros = []


def checa(nome, cond):
    if not cond:
        erros.append(nome)


# ---------------- vetores (iguais ao montar_ideias.py) ----------------
def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def esc(k, a):
    return tuple(k * x for x in a)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norma(a):
    return math.sqrt(float(dot(a, a)))


def unit(a):
    m = norma(a)
    return tuple(float(x) / m for x in a)


def r3(p):
    return [round(float(x), 3) for x in p]


def folha(centro, e1, e2, a, b, cor=1):
    cs = [add(add(centro, esc(sa * a, e1)), esc(sb * b, e2)) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return {"tipo": "poligono", "pts": [r3(c) for c in cs], "cor": cor}


def ponto(p, rot, cor=4):
    return {"tipo": "ponto", "em": r3(p), "rot": rot, "cor": cor}


def vetor(de, ate, rot, cor):
    return {"tipo": "vetor", "de": r3(de), "ate": r3(ate), "rot": rot, "cor": cor}


def reta(p, v, t0, t1, cor, largura=3):
    return {"tipo": "segmento", "de": r3(add(p, esc(t0, v))), "ate": r3(add(p, esc(t1, v))), "cor": cor, "largura": largura}


def trac(de, ate, cor=None):
    it = {"tipo": "segmento", "de": r3(de), "ate": r3(ate), "tracejado": True, "largura": 2.4 if cor else 2}
    if cor:
        it["cor"] = cor
    return it


def fig(itens, angulo=None, sem_eixos=False):
    f = {"modo": "3d", "itens": itens}
    if angulo:
        f["angulo"] = angulo
    if sem_eixos:
        f["semEixos"] = True
    return f


def angulo_para(d):
    d = unit(d)
    if d[2] < 0:
        d = tuple(-x for x in d)
    pitch = min(math.asin(d[2]), 1.35)
    cp = math.cos(pitch)
    yaw = math.atan2(-d[0] / cp, -d[1] / cp)
    return {"yaw": round(yaw, 3), "pitch": round(pitch, 3)}


def angulo_folha(n, graus=60, apoio=(0, 0, 1)):
    nh = unit(n)
    e = cross(n, apoio)
    if norma(e) < 1e-9:
        e = cross(n, (1, 0, 0))
    eh = unit(e)
    t = math.radians(graus)
    return angulo_para(tuple(math.cos(t) * a + math.sin(t) * b for a, b in zip(nh, eh)))


def folha_em(nv, centro, a, b, cor, e1=None):
    ea = unit(e1) if e1 else None
    if ea is None:
        ea = cross(nv, (0, 0, 1))
        if norma(ea) < 1e-9:
            ea = cross(nv, (1, 0, 0))
        ea = unit(ea)
    eb = unit(cross(nv, ea))
    return folha(centro, ea, eb, a, b, cor)


ANG_PADRAO = {"yaw": -0.62, "pitch": 0.42}


# ---------------- termo ----------------
def termo(id_, grupo, nome, frase, conta=None, exemplo=None, nao=None, questoes=None, avaliacoes=None, f=None, nota=None):
    t = {"id": id_, "grupo": grupo, "termo": nome, "frase": frase}
    if conta is None:
        t["esboco"] = True
        return t
    t["conta"] = conta
    fonte, texto, (valor, rotulo) = exemplo
    t["exemplo"] = {"fonte": fonte, "texto": texto, "destaque": {"valor": valor, "rotulo": rotulo}}
    t["naoConfunda"] = [{"id": i, "termo": n, "texto": x} for i, n, x in nao]
    t["questoes"] = questoes or []
    t["avaliacoes"] = avaliacoes or []
    if f:
        t["fig"] = f
    if nota:
        t["nota"] = nota
    return t


GRUPOS = [
    {"id": "retas", "nome": "Duas retas"},
    {"id": "reta-plano", "nome": "Reta e plano"},
    {"id": "planos", "nome": "Dois planos"},
    {"id": "tres-planos", "nome": "Três planos"},
    {"id": "objetos", "nome": "Objetos"},
    {"id": "equacoes", "nome": "Equações"},
    {"id": "angulos", "nome": "Ângulos"},
    {"id": "distancias", "nome": "Distâncias"},
]
T = []
CONV = "Convenção do Prof. Danilo, confirmada pela nota 10 da avaliação 3."

# ======================= DUAS RETAS =======================
# Paralelas distintas (Lista 6, Q5)
pr, vr = (1, 1, 1), (1, -1, 1)
ps, vs = (0, 1, -1), (-2, 2, -2)
checa("paralelas: setas multiplas", vs == esc(-2, vr))
checa("paralelas: AB = (1, 0, 2)", sub(pr, ps) == (1, 0, 2))
checa("paralelas: ponto fora", cross(sub(pr, ps), vs) != (0, 0, 0))
f_par = fig([reta(pr, vr, -2, 2, 1), reta(ps, vs, -1, 1, 2), ponto(pr, "r"), ponto(ps, "s")], ANG_PADRAO)
T.append(termo(
    "paralelas-distintas", "retas", "Paralelas distintas",
    "Duas retas com a mesma direção que nunca se encontram, como dois trilhos.",
    ["Compare as setas: se [[u]] = λ[[v]] (ou [[u]] × [[v]] = [[0]]), as retas têm a mesma direção.",
     "Teste um ponto: pegue A de r e veja se ele está em s.",
     "Se **não** está, são paralelas distintas. Se está, são coincidentes."],
    ("Lista 6, Q5",
     "r passa por (1, 1, 1) com seta (1, −1, 1); s passa por (0, 1, −1) com seta (−2, 2, −2). A seta de s é −2 vezes a de r: mesma direção. Mas (1, 1, 1) não está em s: a seta de (0, 1, −1) até (1, 1, 1) é (1, 0, 2), que não é múltipla de (−2, 2, −2).",
     ("(−2, 2, −2) = −2 · (1, −1, 1)", "setas múltiplas e ponto fora: paralelas distintas")),
    [("coincidentes", "Coincidentes", "Também têm setas múltiplas, mas o ponto de uma está na outra: é a mesma reta."),
     ("paralelos-reta-plano", "Paralelos (reta e plano)", "No feminino é reta com reta. No masculino, o professor fala de reta com plano ou de dois planos.")],
    ["ga-s5-l6q5a"], ["Avaliação 3, Q4 (frase 8)"], f_par))

# Coincidentes (Lista 6, Q6e)
pc, vc = (1, 1, 1), (1, -2, 3)
vs2 = (-2, 4, -6)
checa("coincidentes: multiplas", vs2 == esc(-2, vc))
checa("coincidentes: s passa por (1,1,1)", (1 - pc[0]) / 2 == (pc[1] - 1) / 4 == (1 - pc[2]) / 6)
f_coi = fig([reta(pc, vc, -1.2, 1.2, 2), reta(pc, vc, -1.2, 1.2, 1), vetor(pc, add(pc, vc), "r", 1),
             vetor(pc, add(pc, esc(F(1, 2), vs2)), "s", 2), ponto(pc, "(1, 1, 1)")], ANG_PADRAO)
T.append(termo(
    "coincidentes", "retas", "Coincidentes (duas retas)",
    "É a mesma reta escrita de dois jeitos: todos os pontos em comum.",
    ["As setas são múltiplas: [[u]] = λ[[v]].",
     "Um ponto de r também satisfaz a equação de s.",
     "Com as duas coisas, é a mesma reta, só com outro ponto de partida ou outro tamanho de passo."],
    ("Lista 6, Q6e",
     "r: X = (1, 1, 1) + λ(1, −2, 3). s: (1 − x)/2 = (y − 1)/4 = (1 − z)/6, que passa por (1, 1, 1) com seta (−2, 4, −6). A seta de s é −2 vezes a de r, e o ponto (1, 1, 1) está nas duas.",
     ("(−2, 4, −6) = −2 · (1, −2, 3)", "setas múltiplas e ponto comum: a mesma reta")),
    [("paralelas-distintas", "Paralelas distintas", "Setas múltiplas também, mas sem ponto comum: duas retas diferentes."),
     ("coincidentes-planos", "Coincidentes (dois planos)", "A mesma palavra vale para planos: a mesma equação multiplicada por um número, inclusive o d.")],
    ["ga-s5-l6q6e"], ["Avaliação 3, Q4 (frase 6)"], f_coi))

# Concorrentes (Lista 4, Q6)
r_p, r_v = (-1, 2, 3), (1, 1, 1)
s_p, s_v = (2, 4, 1), (7, 6, 2)
enc = add(r_p, esc(-4, r_v))
checa("concorrentes: encontro", enc == (-5, -2, -1) and add(s_p, esc(-1, s_v)) == enc)
checa("concorrentes: misto 0", dot(sub(s_p, r_p), cross(r_v, s_v)) == 0)
checa("concorrentes: setas nao multiplas", cross(r_v, s_v) != (0, 0, 0))
f_conc = fig([reta(r_p, r_v, -7, -1, 1), reta(s_p, s_v, F(-17, 10), F(-3, 10), 2), ponto(enc, "(−5, −2, −1)")], ANG_PADRAO)
T.append(termo(
    "concorrentes", "retas", "Concorrentes (duas retas)",
    "Duas retas que se cruzam em um único ponto.",
    ["As setas **não** são múltiplas: [[u]] × [[v]] ≠ [[0]].",
     "O produto misto [[AB]] · ([[u]] × [[v]]) dá 0: as duas cabem no mesmo plano.",
     "Direções diferentes no mesmo plano sempre se cruzam: concorrentes."],
    ("Lista 4, Q6",
     "r: X = (−1, 2, 3) + t(1, 1, 1) e s: X = (2, 4, 1) + λ(7, 6, 2). Igualando x e y das duas, sai t = −4 e λ = −1. A terceira coordenada confere: 3 + (−4) = −1 e 1 + 2(−1) = −1.",
     ("(−5, −2, −1)", "ponto onde as duas se cruzam")),
    [("reversas", "Reversas", "Também têm direções diferentes, mas não se cruzam: o produto misto não dá 0."),
     ("concorrentes-reta-plano", "Concorrentes (reta e plano)", "Com reta e plano, o professor usa a mesma palavra para a reta que fura o plano."),
     ("perpendiculares", "Perpendiculares", "Concorrentes que formam 90° ganham o nome de perpendiculares.")],
    ["ga-s4-l4q6"], ["Avaliação 3, Q1, Q4 (frase 5) e Q5"], f_conc))

# Reversas (Lista 6, Q6a)
p1, u = (1, 2, 3), (1, 1, 1)
p2, v = (1, 1, 1), (1, -2, -3)
checa("reversas: u x v", cross(u, v) == (-1, 4, -3))
checa("reversas: AB", sub(p2, p1) == (0, -1, -2))
checa("reversas: misto 2", dot(sub(p2, p1), cross(u, v)) == 2)
w0 = sub(p1, p2)
a_, b_, c_ = dot(u, u), dot(u, v), dot(v, v)
d_, e_ = dot(u, w0), dot(v, w0)
den = a_ * c_ - b_ * b_
sc, tc = F(b_ * e_ - c_ * d_, den), F(a_ * e_ - b_ * d_, den)
q1, q2 = add(p1, esc(sc, u)), add(p2, esc(tc, v))
checa("reversas: perpendicular comum", dot(sub(q1, q2), u) == 0 and dot(sub(q1, q2), v) == 0)
_b = unit(add(unit(u), unit(v)))
_w = unit(cross(u, v))
_t = math.radians(35)
ANG_REV = angulo_para(tuple(math.cos(_t) * x + math.sin(_t) * y for x, y in zip(_b, _w)))
f_rev = fig([reta(p1, u, float(sc) - 0.6, float(sc) + 0.6, 1), reta(p2, v, float(tc) - 0.28, float(tc) + 0.28, 2), trac(q1, q2, 3)], ANG_REV, sem_eixos=True)
T.append(termo(
    "reversas", "retas", "Reversas",
    "Retas que não se cruzam e não cabem num mesmo plano, como uma avenida e um viaduto.",
    ["As setas não são múltiplas: [[u]] × [[v]] ≠ [[0]].",
     "O produto misto [[AB]] · ([[u]] × [[v]]) dá diferente de 0: não estão no mesmo plano.",
     "Se desse 0, seriam concorrentes."],
    ("Lista 6, Q6a",
     "r: X = (1, 2, 3) + λ(1, 1, 1) e s: X = (1, 1, 1) + t(1, −2, −3). [[u]] × [[v]] = (−1, 4, −3), diferente de [[0]]. Com [[AB]] = (0, −1, −2), o produto misto dá 0·(−1) + (−1)·4 + (−2)·(−3) = 2.",
     ("2", "produto misto diferente de 0: reversas")),
    [("concorrentes", "Concorrentes", "Direções diferentes também, mas no mesmo plano: se cruzam."),
     ("ortogonais", "Ortogonais", "Fala só do ângulo. Duas retas reversas podem ser ortogonais (avaliação 3, Q7)."),
     ("paralelas-distintas", "Paralelas distintas", "Também não se encontram, mas têm a mesma direção.")],
    ["ga-s5-l6q6a", "ga-s5-l8q1a"], ["Avaliação 3, Q1, Q4 (frase 2) e Q10", "Avaliação 5, Q4"], f_rev))

# Ortogonais (Avaliacao 3, Q7)
o_r, o_u, o_s, o_v = (0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 1, 0)
checa("ortogonais: u.v = 0", dot(o_u, o_v) == 0)
checa("ortogonais: misto 1", dot(sub(o_s, o_r), cross(o_u, o_v)) == 1)
f_ort = fig([reta(o_r, o_u, -1.6, 1.6, 1), reta(o_s, o_v, -1.6, 1.6, 2), trac(o_r, o_s, 3)], ANG_PADRAO)
T.append(termo(
    "ortogonais", "retas", "Ortogonais (duas retas)",
    "Retas cujas direções formam 90°, se cruzando ou não.",
    ["Faça o produto escalar das setas: [[u]] · [[v]] = 0 quer dizer 90°.",
     "Não precisa testar ponto: o cruzamento não importa para ser ortogonal."],
    ("Avaliação 3, Q7",
     "r: X = t(1, 0, 0) e s: X = (0, 0, 1) + k(0, 1, 0). As setas dão (1, 0, 0) · (0, 1, 0) = 0: ortogonais. O produto misto dá 1: elas não se cruzam. São ortogonais e reversas.",
     ("0", "produto escalar das setas: 90°, mesmo sem cruzar")),
    [("perpendiculares", "Perpendiculares", "Perpendiculares são as ortogonais que também se cruzam. Toda perpendicular é ortogonal; a volta não vale."),
     ("perpendiculares-planos", "Perpendiculares (dois planos)", "Para dois planos, o curso usa ortogonais e perpendiculares como a mesma coisa: [[n1]] · [[n2]] = 0.")],
    [], ["Avaliação 3, Q2 e Q7"], f_ort, CONV))

# Perpendiculares (Avaliacao 3, Q5)
pp_r, pp_u, pp_s, pp_v = (1, 2, 3), (2, 1, -3), (3, 3, 0), (1, 1, 1)
checa("perpendiculares: u.v = 0", dot(pp_u, pp_v) == 0)
checa("perpendiculares: encontro", add(pp_r, pp_u) == pp_s)
f_perp = fig([reta(pp_r, pp_u, 0, 2, 1), reta(pp_s, pp_v, -1.6, 1.6, 2), ponto(pp_s, "(3, 3, 0)")], ANG_PADRAO)
T.append(termo(
    "perpendiculares", "retas", "Perpendiculares (duas retas)",
    "Retas que se cruzam formando 90°, como os traços de uma cruz.",
    ["As setas fazem 90°: [[u]] · [[v]] = 0.",
     "E as retas se cruzam: as setas não são múltiplas e o produto misto dá 0.",
     "Só com as duas coisas são perpendiculares."],
    ("Avaliação 3, Q5",
     "r: X = (1, 2, 3) + k(2, 1, −3) e s: X = (3, 3, 0) + λ(1, 1, 1). As setas dão 2 + 1 − 3 = 0. Com k = 1 e λ = 0, as duas chegam a (3, 3, 0).",
     ("(3, 3, 0)", "ponto comum, com 90° entre as setas")),
    [("ortogonais", "Ortogonais", "Ortogonais não precisam se cruzar. Perpendiculares precisam."),
     ("concorrentes", "Concorrentes", "Toda perpendicular é concorrente. Na avaliação 3, Q5, \"somente concorrentes\" quer dizer concorrentes sem 90°.")],
    [], ["Avaliação 3, Q2, Q5 e Q7"], f_perp, CONV))

# ======================= RETA E PLANO =======================
# Contida (Lista 7, Q8)
P8, v8, n8 = (-2, -1, 1), (6, 0, -3), (2, -3, 4)
checa("contida: v.n = 0", dot(v8, n8) == 0)
checa("contida: ponto no plano", dot(n8, P8) - 3 == 0)
g8 = unit(cross(n8, v8))
fol8 = folha(P8, unit(v8), g8, 2.4, 1.6)
f_cont = fig([fol8, reta(P8, v8, -0.35, 0.35, 4), vetor(P8, add(P8, unit(n8)), "n", 2), vetor(P8, add(P8, esc(0.25, v8)), "v", 1)], angulo_folha(n8, 62), sem_eixos=True)
T.append(termo(
    "contida", "reta-plano", "Contida (reta no plano)",
    "A reta inteira fica dentro do plano: todos os pontos dela satisfazem a equação do plano.",
    ["A seta da reta faz 90° com o prego do plano: [[v]] · [[n]] = 0. Ela corre deitada.",
     "Um ponto da reta satisfaz a equação do plano.",
     "As duas coisas juntas: contida. Só a primeira não basta."],
    ("Lista 7, Q8",
     "r: X = (−2, −1, 1) + λ(6, 0, −3) e π: 2x − 3y + 4z − 3 = 0. [[v]] · [[n]] = 12 + 0 − 12 = 0. O ponto (−2, −1, 1) dá −4 + 3 + 4 − 3 = 0.",
     ("0 e 0", "seta deitada e ponto no plano: contida")),
    [("paralelos-reta-plano", "Paralelos (reta e plano)", "Seta deitada também, mas o ponto fica fora: a reta passa por cima, sem tocar."),
     ("concorrentes-reta-plano", "Concorrentes (reta e plano)", "A seta não é deitada ([[v]] · [[n]] ≠ 0): a reta fura o plano num ponto.")],
    ["ga-s5-l7q8"], ["Avaliação 3, Q4 (frase 1) e Q6", "Avaliação 5, Q3"], f_cont))

# Paralelos, reta e plano (Lista 6, Q6f)
Pf, vf = (1, 1, -1), (1, 1, 1)
nf = cross((0, 1, 0), (1, 1, 1))
checa("paralelos rp: normal (1, 0, -1)", nf == (1, 0, -1))
df = -dot(nf, (1, 1, 1))
checa("paralelos rp: d = 0", df == 0)
checa("paralelos rp: v.n = 0", dot(vf, nf) == 0)
checa("paralelos rp: ponto da 2", dot(nf, Pf) + df == 2)
pe_f = sub(Pf, esc(F(dot(nf, Pf) + df, dot(nf, nf)), nf))
checa("paralelos rp: pe no plano", dot(nf, pe_f) + df == 0)
f_prp = fig([folha_em(nf, pe_f, 2.0, 1.4, 1, e1=vf), reta(Pf, vf, -1.4, 1.4, 4), trac(Pf, pe_f, 3), vetor(pe_f, add(pe_f, unit(nf)), "n", 2)],
            angulo_folha(nf, 70, apoio=vf), sem_eixos=True)
T.append(termo(
    "paralelos-reta-plano", "reta-plano", "Paralelos (reta e plano)",
    "A reta corre ao lado do plano sem tocá-lo, como um fio esticado acima da mesa.",
    ["Seta deitada: [[v]] · [[n]] = 0.",
     "Um ponto da reta **não** satisfaz a equação do plano.",
     "Então a distância entre os dois é a mesma em toda a reta, e maior que 0."],
    ("Lista 6, Q6f",
     "r: X = (1, 1, −1) + k(1, 1, 1). O plano π passa por (1, 1, 1) com setas (0, 1, 0) e (1, 1, 1); o prego é (0, 1, 0) × (1, 1, 1) = (1, 0, −1), e a equação fica x − z = 0. [[v]] · [[n]] = 1 + 0 − 1 = 0, mas o ponto (1, 1, −1) dá 1 − (−1) = 2.",
     ("2", "o ponto da reta não zera a equação: paralelos")),
    [("contida", "Contida", "Mesma seta deitada, mas o ponto zera a equação: a reta está dentro."),
     ("paralelas-distintas", "Paralelas distintas", "No feminino é reta com reta.")],
    ["ga-s5-l6q6f"], ["Avaliação 3, Q4 (frase 4)", "Avaliação 5, Q3"], f_prp))

# Concorrentes, reta e plano (Lista 6, Q6b)
Pb, vb, nb = (1, 2, 3), (1, 1, 1), (1, 1, 1)
checa("conc rp: v.n = 3", dot(vb, nb) == 3)
lb = F(-(dot(nb, Pb) + 1), dot(nb, vb))
checa("conc rp: lambda = -7/3", lb == F(-7, 3))
Hb = add(Pb, esc(lb, vb))
checa("conc rp: ponto", Hb == (F(-4, 3), F(-1, 3), F(2, 3)) and dot(nb, Hb) + 1 == 0)
folb = folha(Hb, unit((1, -1, 0)), unit((1, 1, -2)), 2.0, 2.0)
f_crp = fig([folb, reta(Hb, vb, -1.6, 1.6, 4), ponto(Hb, "")], angulo_folha(nb, 70), sem_eixos=True)
T.append(termo(
    "concorrentes-reta-plano", "reta-plano", "Concorrentes (reta e plano)",
    "A reta fura o plano em um único ponto. Alguns livros chamam de transversal.",
    ["A seta não é deitada: [[v]] · [[n]] ≠ 0.",
     "Para achar o ponto, troque x, y e z da reta na equação do plano e resolva o λ."],
    ("Lista 6, Q6b",
     "r: X = (1, 2, 3) + λ(1, 1, 1) e π: x + y + z + 1 = 0. [[v]] · [[n]] = 3, diferente de 0. Trocando: (1 + λ) + (2 + λ) + (3 + λ) + 1 = 0, então 7 + 3λ = 0 e λ = −7/3.",
     ("(−4/3, −1/3, 2/3)", "ponto onde a reta fura o plano")),
    [("transversais", "Transversais", "Para dois planos que se cortam, o professor usa transversais (avaliação 3, Q4)."),
     ("perpendicular-reta-plano", "Perpendicular (reta e plano)", "Caso especial: a seta da reta tem a direção do prego."),
     ("concorrentes", "Concorrentes (duas retas)", "Com duas retas, concorrentes quer dizer que se cruzam num ponto.")],
    ["ga-s5-l6q6b"], ["Avaliação 3, Q4 (frase 7)", "Avaliação 4, Q1"], f_crp))

# Perpendicular, reta e plano (Lista 6, Q6b e Lista 7, Q1b)
checa("perp rp: v multiplo de n", cross(vb, nb) == (0, 0, 0))
f_prp2 = fig([folb, reta(Hb, vb, -1.6, 1.6, 4), vetor(Hb, add(Hb, unit(nb)), "n", 2), ponto(Hb, "")], angulo_folha(nb, 70), sem_eixos=True)
T.append(termo(
    "perpendicular-reta-plano", "reta-plano", "Perpendicular (reta e plano)",
    "A reta fura o plano em pé, como um prego: a seta da reta tem a direção do vetor normal.",
    ["A seta da reta é múltipla do prego: [[v]] = λ[[n]], ou [[v]] × [[n]] = [[0]].",
     "É um caso de concorrentes: fura num ponto, com 90°.",
     "Cuidado: aqui o teste é múltiplo. [[v]] · [[n]] = 0 diz o contrário (seta deitada)."],
    ("Lista 6, Q6b",
     "r tem seta (1, 1, 1) e π: x + y + z + 1 = 0 tem prego (1, 1, 1): é a mesma direção. O gabarito diz \"Concorrentes (e perpendiculares)\", e na Lista 7, Q1b, o ângulo dá 90°.",
     ("90°", "ângulo entre a reta e o plano")),
    [("paralelos-reta-plano", "Paralelos (reta e plano)", "Seta deitada ([[v]] · [[n]] = 0) é o oposto: reta junto ao plano."),
     ("ortogonais", "Ortogonais", "Ortogonais compara duas retas, não reta com plano.")],
    ["ga-s5-l6q6b", "ga-s5-l7q1b"], [], f_prp2))

# ======================= DOIS PLANOS =======================
# Coincidentes (Lista 8, Q10e)
c1, c2 = (1, 1, -4, 2), (-3, -3, 12, -6)
checa("coinc planos: tudo -3 vezes", c2 == tuple(-3 * x for x in c1))
nco = c1[:3]
Pco = (-2, 0, 0)
checa("coinc planos: ponto no plano", dot(nco, Pco) + c1[3] == 0)
f_cop = fig([folha_em(nco, Pco, 1.8, 1.4, 2), folha_em(nco, Pco, 1.8, 1.4, 1), vetor(Pco, add(Pco, unit(nco)), "n", 4)], angulo_folha(nco, 60), sem_eixos=True)
T.append(termo(
    "coincidentes-planos", "planos", "Coincidentes (dois planos)",
    "É o mesmo plano escrito com outros números: uma equação é a outra multiplicada por um número.",
    ["Pregos múltiplos: [[n1]] = λ[[n2]].",
     "O termo solto acompanha o **mesmo** λ: d1 = λd2.",
     "Com as duas coisas, é o mesmo plano."],
    ("Lista 8, Q10e",
     "π1: x + y − 4z + 2 = 0 e π2: −3x − 3y + 12z − 6 = 0. Tudo em π2 é −3 vezes π1: −3·1 = −3, −3·1 = −3, −3·(−4) = 12 e −3·2 = −6.",
     ("λ = −3", "vale para x, y, z e para o d: mesmo plano")),
    [("paralelos-distintos", "Paralelos distintos", "Pregos múltiplos também, mas o d não acompanha: dois andares diferentes."),
     ("coincidentes", "Coincidentes (duas retas)", "Para duas retas, coincidentes também quer dizer a mesma reta.")],
    ["ga-s5-l8q10e"], ["Avaliação 3, Q4 (frase 3)"], f_cop))

# Paralelos distintos (Lista 6, Q6c)
n1c, d1c = (1, 1, 1), 1
n2c, d2c = (-1, -1, -1), 7
checa("par dist: lambda -1", n2c == esc(-1, n1c))
checa("par dist: d nao acompanha", d2c != -1 * d1c)
dist_c = abs(d1c - (-d2c)) / norma(n1c)
checa("par dist: 8/raiz3", abs(dist_c - 8 * math.sqrt(3) / 3) < 1e-12 and round(dist_c, 2) == 4.62)
cen1 = esc(F(-d1c, 3), n1c)
cen2 = esc(F(d2c, 3), n1c)
checa("par dist: centros nos planos", dot(n1c, cen1) + d1c == 0 and dot(n2c, cen2) + d2c == 0)
f_pdi = fig([folha_em(n1c, cen1, 1.6, 1.1, 1), folha_em(n1c, cen2, 1.6, 1.1, 2), trac(cen1, cen2, 3)], angulo_folha(n1c, 80), sem_eixos=True)
T.append(termo(
    "paralelos-distintos", "planos", "Paralelos distintos (dois planos)",
    "Dois planos com o mesmo prego e alturas diferentes, como dois andares de um prédio.",
    ["Pregos múltiplos: [[n1]] = λ[[n2]].",
     "O d não acompanha: d1 ≠ λd2. São planos diferentes que nunca se tocam.",
     "Com o mesmo prego nos dois, a distância é |d1 − d2| / ‖[[n]]‖."],
    ("Lista 6, Q6c",
     "π1: x + y + z + 1 = 0 e π2: −x − y − z + 7 = 0. O prego de π2 é −1 vez o de π1, mas −1·1 = −1, e não 7. Reescrevendo π2 como x + y + z − 7 = 0, a distância é |1 − (−7)| / √3 = 8/√3.",
     ("8√3/3 ≈ 4,62", "distância entre os dois andares")),
    [("coincidentes-planos", "Coincidentes (dois planos)", "Se o d acompanhasse o mesmo λ, seria o mesmo plano."),
     ("paralelas-distintas", "Paralelas distintas", "No feminino é reta com reta.")],
    ["ga-s5-l6q6c"], ["Avaliação 3, Q4 (frase 10)", "Avaliação 4, Q6", "Avaliação 5, Q2 e Q5"], f_pdi))

# Transversais (Lista 6, Q6d)
n1d, d1d = (1, 1, -1), 3
n2d, d2d = (3, -1, 1), 0
dird = cross(n1d, n2d)
checa("transv: n1 x n2", dird == (0, -4, -4))
P0d = (F(-3, 4), 0, F(9, 4))
checa("transv: ponto nos dois", dot(n1d, P0d) + d1d == 0 and dot(n2d, P0d) + d2d == 0)
cosd = abs(dot(n1d, n2d)) / (norma(n1d) * norma(n2d))
checa("transv: angulo ~ 80", round(math.degrees(math.acos(cosd))) == 80)
f_tra = fig([folha_em(n1d, P0d, 1.8, 1.2, 1, e1=dird), folha_em(n2d, P0d, 1.8, 1.2, 2, e1=dird), reta(P0d, unit(dird), -1.8, 1.8, 4)],
            angulo_para(add(add(unit(n1d), unit(n2d)), esc(0.6, unit(dird)))), sem_eixos=True)
T.append(termo(
    "transversais", "planos", "Transversais (dois planos)",
    "Dois planos que se cortam numa reta, como duas paredes que se encontram na quina.",
    ["Pregos **não** múltiplos: [[n1]] × [[n2]] ≠ [[0]].",
     "A reta da quina tem a direção [[n1]] × [[n2]]."],
    ("Lista 6, Q6d",
     "π1: x + y − z + 3 = 0 e π2: 3x − y + z = 0. [[n1]] × [[n2]] = (1, 1, −1) × (3, −1, 1) = (0, −4, −4), diferente de [[0]]: os planos se cortam numa reta com essa direção.",
     ("(0, −4, −4)", "direção da reta da quina")),
    [("concorrentes-reta-plano", "Concorrentes (reta e plano)", "Com reta e plano, o professor usa concorrentes, não transversais (avaliação 3, Q4)."),
     ("perpendiculares-planos", "Perpendiculares (dois planos)", "Transversais que se cortam a 90° são perpendiculares.")],
    ["ga-s5-l6q6d", "ga-s5-l7q1d"], ["Avaliação 3, Q4 (frase 9)", "Avaliação 4, Q2"], f_tra))

# Perpendiculares, dois planos (Avaliacao 3, Q9)
n1e, d1e = (-2, -1, 4), -1
n2e, d2e = (-18, 12, -6), -2
checa("perp planos: n1.n2 = 0", dot(n1e, n2e) == 0)
dire = cross(n1e, n2e)
checa("perp planos: direcao (1,2,1)", cross(dire, (1, 2, 1)) == (0, 0, 0))
P0e = (0, F(1, 3), F(1, 3))
checa("perp planos: ponto nos dois", dot(n1e, P0e) + d1e == 0 and dot(n2e, P0e) + d2e == 0)
f_ppl = fig([folha_em(n1e, P0e, 1.8, 1.2, 1, e1=dire), folha_em(n2e, P0e, 1.8, 1.2, 2, e1=dire), reta(P0e, unit(dire), -1.8, 1.8, 4)],
            angulo_para(add(add(unit(n1e), unit(n2e)), esc(0.6, unit(dire)))), sem_eixos=True)
T.append(termo(
    "perpendiculares-planos", "planos", "Perpendiculares (dois planos)",
    "Planos que se cortam em ângulo reto, como o chão e a parede.",
    ["Os pregos fazem 90°: [[n1]] · [[n2]] = 0.",
     "Para planos, o curso usa ortogonais com o mesmo sentido (avaliação 3, Q8)."],
    ("Avaliação 3, Q9",
     "π1: −2x − y + 4z − 1 = 0 e π: −18x + 12y − 6z − 2 = 0. Pregos: (−2, −1, 4) · (−18, 12, −6) = 36 − 12 − 24 = 0.",
     ("0", "produto escalar dos pregos: planos perpendiculares")),
    [("transversais", "Transversais", "Todo par perpendicular é transversal, mas transversais podem se cortar em outro ângulo (80° na Lista 7, Q1d)."),
     ("paralelos-distintos", "Paralelos distintos", "Pregos múltiplos são o oposto: planos que não se cortam.")],
    [], ["Avaliação 3, Q8 e Q9"], f_ppl))

# ======================= DEMAIS GRUPOS: frase de cada termo =======================
FRASES = [
    ("ponto-unico", "tres-planos", "Um único ponto em comum", "Os três planos se encontram num ponto só, como o canto de uma sala. O produto misto dos três pregos é diferente de 0."),
    ("reta-comum", "tres-planos", "Uma reta em comum (feixe)", "Os três passam pela mesma reta, como páginas de um livro presas na lombada."),
    ("calha", "tres-planos", "Retas paralelas dois a dois", "Cada par se corta numa reta, as três retas são paralelas e nenhum ponto é dos três, como as faces de uma barraca."),
    ("dois-paralelos", "tres-planos", "Dois paralelos e um que corta", "Dois planos paralelos e um terceiro que corta os dois em retas paralelas."),
    ("paralelos-tres", "tres-planos", "Paralelos ou coincidentes", "Os três pregos são múltiplos: planos empilhados como andares, ou alguns iguais."),
    ("vetor-diretor", "objetos", "Vetor diretor", "A seta que dá a direção da reta: para onde ela anda."),
    ("vetor-normal", "objetos", "Vetor normal", "O prego em pé no plano: faz 90° com tudo o que está deitado nele."),
    ("ponto-partida", "objetos", "Ponto de partida", "Um ponto conhecido da reta ou do plano, de onde se começa a andar."),
    ("parametro", "objetos", "Parâmetro (t, λ)", "O contador de passos: cada valor de t dá um ponto diferente da reta."),
    ("multiplo", "objetos", "Múltiplo (u = λv)", "Duas setas na mesma direção: uma é a outra esticada, encolhida ou virada."),
    ("colineares", "objetos", "Colineares", "Pontos que ficam na mesma reta."),
    ("coplanares", "objetos", "Coplanares", "Pontos, setas ou retas que cabem num mesmo plano. O teste é o produto misto dar 0."),
    ("pe-perpendicular", "objetos", "Pé da perpendicular", "O ponto do plano ou da reta mais perto de um ponto de fora."),
    ("eq-vetorial", "equacoes", "Equação vetorial da reta", "X = A + t[[v]]: comece em A e ande t passos na direção de [[v]]."),
    ("eq-parametricas", "equacoes", "Equações paramétricas", "A equação vetorial separada em x, y e z, cada uma com o t."),
    ("eq-simetricas", "equacoes", "Equações simétricas", "Isola o t de cada coordenada e iguala. Só existe se nenhuma coordenada da seta for 0."),
    ("eq-geral-plano", "equacoes", "Equação geral do plano", "ax + by + cz + d = 0: os números a, b e c formam o prego."),
    ("eq-param-plano", "equacoes", "Equações paramétricas do plano", "Um ponto e duas setas deitadas: X = A + t[[u]] + s[[v]]."),
    ("feixe", "equacoes", "Feixe de planos", "Todos os planos que passam por uma mesma reta: misturas α·π1 + β·π2."),
    ("ang-vetores", "angulos", "Ângulo entre vetores", "Vai de 0° a 180°, porque a seta tem sentido."),
    ("ang-retas", "angulos", "Ângulo entre retas", "Usa o cosseno com módulo, então fica entre 0° e 90°."),
    ("ang-reta-plano", "angulos", "Ângulo entre reta e plano", "Usa o seno, porque o prego fica de pé: é o que falta para 90°."),
    ("ang-planos", "angulos", "Ângulo entre planos", "É o ângulo entre os pregos, com módulo: entre 0° e 90°."),
    ("cossenos-diretores", "angulos", "Cossenos diretores", "Os cossenos dos ângulos da seta com os eixos x, y e z. Os quadrados somam 1."),
    ("dist-ponto-plano", "distancias", "Distância de ponto a plano", "Troque o ponto na equação, tire o módulo e divida pelo tamanho do prego."),
    ("dist-ponto-reta", "distancias", "Distância de ponto a reta", "A área do paralelogramo dividida pela base: ‖[[AP]] × [[v]]‖ / ‖[[v]]‖."),
    ("dist-retas-paralelas", "distancias", "Distância entre retas paralelas", "É a distância de um ponto de uma reta até a outra."),
    ("dist-reversas", "distancias", "Distância entre reversas", "O volume da caixa dividido pela área da base: a altura do viaduto."),
    ("dist-planos", "distancias", "Distância entre planos paralelos", "Com o mesmo prego nos dois: |d1 − d2| / ‖[[n]]‖."),
    ("lugar-geometrico", "distancias", "Lugar geométrico", "O conjunto de todos os pontos que cumprem uma condição, como ficar à mesma distância de A e de B."),
    ("plano-mediador", "distancias", "Plano mediador", "Os pontos à mesma distância de A e de B: é um plano, e não uma reta (avaliação 5, Q10)."),
    ("equidistante", "distancias", "Equidistante", "À mesma distância de dois pontos ou de dois objetos."),
]
FR = {id_: (g, nome, frase) for id_, g, nome, frase in FRASES}


def completo(id_, conta, exemplo, nao, questoes, avaliacoes, f=None, nota=None):
    g, nome, frase = FR[id_]
    T.append(termo(id_, g, nome, frase, conta, exemplo, nao, questoes, avaliacoes, f, nota))


def resolve3(ns, cs):
    """Cramer em fracoes: n . p = c para os tres planos."""
    det = dot(ns[0], cross(ns[1], ns[2]))
    sol = []
    for i in range(3):
        m = [list(r) for r in ns]
        for k in range(3):
            m[k][i] = cs[k]
        sol.append(F(dot(m[0], cross(m[1], m[2])), det))
    return tuple(sol)


# ---------- TRES PLANOS (Lista 8, Q10 e Q11) ----------
na = [(-1, 3, -4), (-4, -1, 8), (1, -1, 4)]
ca = [-2, -4, -1]
checa("3p a: misto 48", dot(na[0], cross(na[1], na[2])) == 48)
Pa = resolve3(na, ca)
checa("3p a: ponto nos tres", all(dot(n, Pa) == c for n, c in zip(na, ca)))
f_3a = fig([folha_em(n, Pa, 1.2, 1.2, cor) for n, cor in zip(na, (1, 2, 3))] + [ponto(Pa, "")], ANG_PADRAO, sem_eixos=True)
completo("ponto-unico",
         ["Nenhum par de pregos é múltiplo.",
          "O produto misto dos três pregos dá diferente de 0.",
          "Então o sistema dos três planos tem uma solução só: um ponto."],
         ("Lista 8, Q10a",
          "π1: −x + 3y − 4z + 2 = 0, π2: −4x − y + 8z + 4 = 0 e π3: x − y + 4z + 1 = 0. Nenhum prego é múltiplo de outro, e o produto misto dos três pregos dá 48.",
          ("48", "produto misto diferente de 0: um ponto só")),
         [("reta-comum", "Uma reta em comum", "Quando o produto misto dá 0, não há ponto único: ou os três passam por uma reta, ou formam a barraca."),
          ("calha", "Retas paralelas dois a dois", "Produto misto 0 e nenhum ponto dos três.")],
         ["ga-s5-l8q10a", "ga-s5-l8q10f"], [], f_3a)

nj_ = [(1, 1, -2, 2), (-3, -3, 1, -6), (4, 4, -3, 8)]
checa("3p j: pi3 = pi1 - pi2", nj_[2] == tuple(a - b for a, b in zip(nj_[0], nj_[1])))
dj = cross(nj_[0][:3], nj_[1][:3])
checa("3p j: direcao (-5, 5, 0)", dj == (-5, 5, 0))
P0j = (0, -2, 0)
checa("3p j: ponto nos tres", all(dot(p[:3], P0j) + p[3] == 0 for p in nj_))
f_3j = fig([folha_em(p[:3], P0j, 1.6, 1.0, cor, e1=dj) for p, cor in zip(nj_, (1, 2, 3))] + [reta(P0j, unit(dj), -1.8, 1.8, 4)],
           angulo_para(add(unit(dj), (0.2, 0.2, 0.9))), sem_eixos=True)
completo("reta-comum",
         ["O produto misto dos três pregos dá 0.",
          "Um dos planos é mistura dos outros dois, inclusive no termo solto: π3 = απ1 + βπ2.",
          "Então todo ponto da reta de π1 e π2 também está em π3."],
         ("Lista 8, Q10j",
          "π1: x + y − 2z + 2 = 0, π2: −3x − 3y + z − 6 = 0 e π3: 4x + 4y − 3z + 8 = 0. Fazendo π1 − π2: (1 + 3)x + (1 + 3)y + (−2 − 1)z + (2 + 6) = 4x + 4y − 3z + 8, que é o π3.",
          ("π3 = π1 − π2", "os três passam pela mesma reta")),
         [("feixe", "Feixe de planos", "É o nome da família de planos que passam por uma mesma reta."),
          ("calha", "Retas paralelas dois a dois", "Produto misto 0 também, mas o termo solto não acompanha a mistura.")],
         ["ga-s5-l8q10j", "ga-s5-l8q11"], ["Avaliação 5, Q9"], f_3j)

ni = [(2, 2, -4), (-1, -1, 1), (-2, -2, -8)]
ci = [-4, 6, -4]
eixo_i = (1, -1, 0)
checa("3p i: misto 0", dot(ni[0], cross(ni[1], ni[2])) == 0)
checa("3p i: direcao comum", all(dot(n, eixo_i) == 0 for n in ni))


def ponto_par(i, j):
    return resolve3([ni[i], ni[j], eixo_i], [ci[i], ci[j], 0])


P12, P13, P23 = ponto_par(0, 1), ponto_par(0, 2), ponto_par(1, 2)
checa("3p i: sem ponto comum", dot(ni[2], P12) != ci[2])
ue = unit(eixo_i)


def faixa(pa, pb, cor):
    m = esc(F(1, 2), add(pa, pb))
    meia = esc(0.65, sub(pb, pa))
    return folha(m, ue, unit(meia), 3.0, norma(meia), cor)


f_3i = fig([faixa(P12, P13, 1), faixa(P12, P23, 2), faixa(P13, P23, 3)] + [reta(pp, ue, -3.0, 3.0, 4, 2) for pp in (P12, P13, P23)],
           angulo_para((0.6, -0.6, 0.53)), sem_eixos=True)
completo("calha",
         ["Nenhum par de pregos é múltiplo, e o produto misto dá 0.",
          "Teste um ponto da reta de dois planos no terceiro: não serve.",
          "Então cada par se corta numa reta, e as três retas são paralelas."],
         ("Lista 8, Q10i",
          "π1: 2x + 2y − 4z + 4 = 0, π2: −x − y + z − 6 = 0 e π3: −2x − 2y − 8z + 4 = 0. O produto misto dá 0, e os três pregos fazem 90° com (1, −1, 0). O ponto (−5, −5, −4), que está em π1 e em π2, dá 56 em π3, e não 0.",
          ("(1, −1, 0)", "direção das três retas paralelas")),
         [("reta-comum", "Uma reta em comum", "Produto misto 0 também, mas lá o ponto serve nos três."),
          ("dois-paralelos", "Dois paralelos e um que corta", "Lá dois pregos são múltiplos.")],
         ["ga-s5-l8q10i", "ga-s5-l8q11"], ["Avaliação 5, Q1"], f_3i)
checa("3p i: P12 = (-5,-5,-4)", P12 == (-5, -5, -4))
checa("3p i: P12 em pi1 e pi2", 2 * P12[0] + 2 * P12[1] - 4 * P12[2] + 4 == 0 and -P12[0] - P12[1] + P12[2] - 6 == 0)
checa("3p i: P12 em pi3 da 56", -2 * P12[0] - 2 * P12[1] - 8 * P12[2] + 4 == 56)

nb_ = [(-1, 1, -4, 2), (-2, 2, 8, 4), (1, -1, 4, 1)]
checa("3p b: pi3 paralelo a pi1", nb_[2][:3] == esc(-1, nb_[0][:3]) and nb_[2][3] != -1 * nb_[0][3])
db_ = cross(nb_[0][:3], nb_[1][:3])
checa("3p b: retas na direcao (1,1,0)", cross(db_, (1, 1, 0)) == (0, 0, 0))
cb = [esc(F(-p[3], dot(p[:3], p[:3])), p[:3]) for p in nb_]
checa("3p b: centros nos planos", all(dot(p[:3], c) + p[3] == 0 for p, c in zip(nb_, cb)))
f_3b = fig([folha_em(nb_[0][:3], cb[0], 1.4, 0.9, 1, e1=(1, 1, 0)), folha_em(nb_[2][:3], cb[2], 1.4, 0.9, 3, e1=(1, 1, 0)),
            folha_em(nb_[1][:3], cb[1], 1.4, 1.3, 2, e1=(1, 1, 0))], angulo_para((0.7, -0.7, 0.35)), sem_eixos=True)
completo("dois-paralelos",
         ["Dois pregos são múltiplos e o termo solto não acompanha: esses dois são paralelos distintos.",
          "O terceiro prego não é múltiplo dos outros: ele corta os dois.",
          "As duas retas de corte saem paralelas."],
         ("Lista 8, Q10b",
          "π1: −x + y − 4z + 2 = 0 e π3: x − y + 4z + 1 = 0 têm pregos múltiplos, (1, −1, 4) = −1 · (−1, 1, −4), mas −1 · 2 = −2, e não 1: são paralelos distintos. π2: −2x + 2y + 8z + 4 = 0 corta os dois.",
          ("(1, −1, 4) = −1 · (−1, 1, −4)", "dois pregos múltiplos: dois planos paralelos")),
         [("calha", "Retas paralelas dois a dois", "Lá nenhum par de pregos é múltiplo."),
          ("paralelos-tres", "Paralelos ou coincidentes", "Lá os três pregos são múltiplos.")],
         ["ga-s5-l8q10b", "ga-s5-l8q10g", "ga-s5-l8q10h"], [])

nc = (1, 1, -4)
const_c = [F(-2), F(4, 3), F(-1)]
checa("3p c: pi2/(-3) da -4/3", F(4, -3) == F(-4, 3))
ea_c = unit((1, -1, 0))
eb_c = unit(cross(nc, ea_c))
f_3c = fig([folha(esc(c / dot(nc, nc), nc), ea_c, eb_c, 1.6, 1.0, cor) for c, cor in zip(const_c, (1, 2, 3))], angulo_folha(nc, 80), sem_eixos=True)
completo("paralelos-tres",
         ["Os três pregos são múltiplos de um mesmo prego.",
          "Escreva os três com o mesmo prego e compare os termos soltos.",
          "Todos diferentes: três andares. Dois iguais: dois coincidem. Três iguais: o mesmo plano."],
         ("Lista 8, Q10c",
          "π1: x + y − 4z + 2 = 0, π2: −3x − 3y + 12z + 4 = 0 e π3: x + y − 4z + 1 = 0. Dividindo π2 por −3: x + y − 4z − 4/3 = 0. Com o prego (1, 1, −4) nos três, os termos soltos ficam 2, −4/3 e 1, todos diferentes.",
          ("2, −4/3 e 1", "termos soltos diferentes: paralelos dois a dois")),
         [("dois-paralelos", "Dois paralelos e um que corta", "Lá só dois pregos são múltiplos."),
          ("coincidentes-planos", "Coincidentes (dois planos)", "Termo solto igual com o mesmo prego: o mesmo plano.")],
         ["ga-s5-l8q10c", "ga-s5-l8q10d", "ga-s5-l8q10e"], [], f_3c)

# ---------- OBJETOS ----------
P5, v5 = (1, 0, -1), (-2, 1, 7)
checa("diretor: ponto e seta batem com a simetrica", all(F(1 - (P5[0] + k * v5[0]), 2) == P5[1] + k * v5[1] == F(P5[2] + k * v5[2] + 1, 7) == k for k in (0, 1, -2)))
completo("vetor-diretor",
         ["Na equação vetorial X = A + t[[v]], é o [[v]] que multiplica o t.",
          "Nas paramétricas, são os números que acompanham o t em x, y e z.",
          "Na simétrica, são os números de baixo, depois de deixar x, y e z com sinal +."],
         ("Lista 4, Q5",
          "r: (1 − x)/2 = y = (z + 1)/7. Como (1 − x)/2 = (x − 1)/(−2), o vetor diretor é (−2, 1, 7), e um ponto é (1, 0, −1).",
          ("(−2, 1, 7)", "vetor diretor lido na simétrica")),
         [("vetor-normal", "Vetor normal", "O diretor fica deitado na reta; o normal fica em pé no plano."),
          ("eq-simetricas", "Equações simétricas", "O sinal de x, y e z precisa ficar + antes de ler o diretor.")],
         ["ga-s4-l4q5", "ga-s4-l4q1a", "ga-s5-l7q1e"], ["Avaliação 1, Q3"])

A1, n1 = (-1, 2, 3), (1, 1, 1)
checa("normal: x + y + z - 4", -dot(n1, A1) == -4)
f_nor = fig([folha_em(n1, A1, 1.6, 1.2, 1), vetor(A1, add(A1, unit(n1)), "n", 2), ponto(A1, "A")], angulo_folha(n1, 60), sem_eixos=True)
completo("vetor-normal",
         ["Na equação geral ax + by + cz + d = 0, o normal é (a, b, c).",
          "Por três pontos ou duas setas do plano, o normal sai do produto vetorial.",
          "Toda seta deitada no plano dá produto escalar 0 com o normal."],
         ("Lista 5, Q1a",
          "Plano por A = (−1, 2, 3) com normal (1, 1, 1): 1(x + 1) + 1(y − 2) + 1(z − 3) = 0, que dá x + y + z − 4 = 0.",
          ("x + y + z − 4 = 0", "os números de x, y e z são o prego")),
         [("vetor-diretor", "Vetor diretor", "O diretor dá o caminho da reta; o normal fica em pé no plano."),
          ("perpendicular-reta-plano", "Perpendicular (reta e plano)", "Reta com a direção do normal fura o plano em pé.")],
         ["ga-s5-l5q1a", "ga-s5-l5q1b", "ga-s5-l5q1c", "ga-s5-l6q4"], ["Avaliação 2, Q2 e Q4"], f_nor)

A6, d6 = (-1, 4, -2), (2, -2, 5)
B6 = add(A6, esc(3, d6))
checa("partida: B = (5, -2, 13)", B6 == (5, -2, 13))
completo("ponto-partida",
         ["Na equação X = A + t[[v]], o A é o ponto de partida (t = 0).",
          "Qualquer ponto da reta serve como partida: a reta é a mesma.",
          "Por isso uma reta tem infinitas equações vetoriais."],
         ("Exemplo construído",
          "X = (−1, 4, −2) + t(2, −2, 5). Com t = 3 chega a (5, −2, 13). Começando de lá, X = (5, −2, 13) + s(2, −2, 5) descreve a mesma reta.",
          ("(5, −2, 13)", "outro ponto de partida, a mesma reta")),
         [("parametro", "Parâmetro (t, λ)", "O ponto de partida é onde o contador vale 0."),
          ("vetor-diretor", "Vetor diretor", "O ponto diz por onde passa; o diretor diz para onde vai.")],
         ["ga-s4-l4q1a", "ga-s5-l6q1"], ["Avaliação 1, Q8", "Avaliação 2, Q3"])

A2, B2 = (-1, 1, 4), (2, 3, 1)
AB2 = sub(B2, A2)
t2 = F(1 - A2[0], AB2[0])
P2 = add(A2, esc(t2, AB2))
checa("parametro: t = 2/3, P = (1, 7/3, 2)", t2 == F(2, 3) and P2 == (1, F(7, 3), 2))
completo("parametro",
         ["Cada valor de t dá um ponto: t = 0 é o ponto de partida.",
          "Para achar o t de um ponto, use uma coordenada e confira nas outras.",
          "Se as coordenadas pedirem t diferentes, o ponto não está na reta."],
         ("Lista 4, Q2",
          "P = (1, m, n) está na reta por A = (−1, 1, 4) e B = (2, 3, 1). Partindo de A com a seta [[AB]] = (3, 2, −3): x = −1 + 3t = 1 dá t = 2/3. Então m = 1 + 2 · 2/3 = 7/3 e n = 4 − 3 · 2/3 = 2.",
          ("t = 2/3", "o contador que leva até P")),
         [("ponto-partida", "Ponto de partida", "O ponto de partida é o t = 0."),
          ("multiplo", "Múltiplo", "O t multiplica a seta: t[[v]] é múltiplo de [[v]].")],
         ["ga-s4-l4q2", "ga-s5-l6q7"], ["Avaliação 1, Q2"])

checa("multiplo: (-2,2,-2) = -2(1,-1,1)", esc(-2, (1, -1, 1)) == (-2, 2, -2))
completo("multiplo",
         ["Divida coordenada por coordenada: se o fator é o mesmo em todas, as setas são múltiplas.",
          "Outro teste: o produto vetorial dá [[0]].",
          "Coordenada 0 só combina com 0 na mesma posição."],
         ("Lista 6, Q5",
          "(−2, 2, −2) ÷ (1, −1, 1) dá −2, −2 e −2: mesmo fator. Já (1, −2, −3) ÷ (1, 1, 1) dá 1, −2 e −3: fatores diferentes, setas em direções diferentes.",
          ("λ = −2", "mesmo fator nas três coordenadas")),
         [("paralelas-distintas", "Paralelas distintas", "Setas múltiplas é o primeiro teste de retas paralelas."),
          ("colineares", "Colineares", "Pontos alinhados dão setas múltiplas entre si.")],
         ["ga-s5-l6q5a", "ga-s5-l6q6a", "ga-s5-l6q1"], ["Avaliação 1, Q5"])

Q1c, Q2c, Q3c = (0, 0, 0), (1, 1, 1), (2, 2, 2)
checa("colineares: produto vetorial nulo", cross(sub(Q2c, Q1c), sub(Q3c, Q1c)) == (0, 0, 0))
completo("colineares",
         ["Faça as setas de um ponto até os outros dois.",
          "Se as setas são múltiplas (produto vetorial [[0]]), os pontos estão alinhados.",
          "Três pontos alinhados não definem um plano: cabem em infinitos."],
         ("Avaliação 2, Q7",
          "(0, 0, 0), (1, 1, 1) e (2, 2, 2): as setas (1, 1, 1) e (2, 2, 2) são múltiplas, e o produto vetorial dá (0, 0, 0). Os planos x − y = 0 e y − z = 0 passam pelos três.",
          ("(0, 0, 0)", "produto vetorial nulo: pontos alinhados")),
         [("coplanares", "Coplanares", "Coplanar é caber num plano; colinear é caber numa reta."),
          ("multiplo", "Múltiplo", "O teste de colinear é o de setas múltiplas.")],
         ["ga-s5-l8q9i", "ga-s4-l4q2"], ["Avaliação 2, Q7"])

r6p, r6v, s6p, s6v = (-1, 2, 3), (1, 1, 1), (2, 4, 1), (7, 6, 2)
checa("coplanares: misto 0", dot(sub(s6p, r6p), cross(r6v, s6v)) == 0)
completo("coplanares",
         ["Para três setas: o produto misto dá 0.",
          "Para duas retas: [[AB]] · ([[u]] × [[v]]) = 0, com A de uma e B da outra.",
          "Retas coplanares são paralelas, coincidentes ou concorrentes; nunca reversas."],
         ("Lista 4, Q6",
          "r: (−1, 2, 3) + t(1, 1, 1) e s: (2, 4, 1) + λ(7, 6, 2). [[AB]] = (3, 2, −2) e [[u]] × [[v]] = (−4, 5, −1). O produto misto dá −12 + 10 + 2 = 0: as duas cabem num plano.",
          ("0", "produto misto: retas no mesmo plano")),
         [("reversas", "Reversas", "Retas que não são coplanares."),
          ("colineares", "Colineares", "Colinear é caber numa reta.")],
         ["ga-s4-l4q6", "ga-s5-l5q4", "ga-s5-l6q5b"], ["Avaliação 3, Q4 (frases 2 e 5)"])

Pi, ni_p, di_p = (1, 2, 3), (-1, -1, -1), 7
k_i = F(dot(ni_p, Pi) + di_p, dot(ni_p, ni_p))
pe_i = sub(Pi, esc(k_i, ni_p))
checa("pe: (4/3, 7/3, 10/3)", pe_i == (F(4, 3), F(7, 3), F(10, 3)) and dot(ni_p, pe_i) + di_p == 0)
f_pe = fig([folha_em(ni_p, pe_i, 1.4, 1.1, 1), ponto(Pi, "P"), ponto(pe_i, "pé"), trac(Pi, pe_i, 3)], angulo_folha(ni_p, 75), sem_eixos=True)
completo("pe-perpendicular",
         ["Saia do ponto P na direção do prego: X = P + k[[n]].",
          "Troque esse X na equação do plano e ache o k.",
          "O ponto achado é o pé; a distância de P até ele é a distância ao plano."],
         ("Lista 8, Q1i",
          "P = (1, 2, 3) e π: −x − y − z + 7 = 0. P dá −1 − 2 − 3 + 7 = 1, e ‖[[n]]‖² = 3. O pé é P − (1/3)(−1, −1, −1) = (4/3, 7/3, 10/3), que dá −4/3 − 7/3 − 10/3 + 7 = 0.",
          ("(4/3, 7/3, 10/3)", "pé da perpendicular no plano")),
         [("dist-ponto-plano", "Distância de ponto a plano", "A distância é o tamanho do tracejado até o pé."),
          ("vetor-normal", "Vetor normal", "O caminho mais curto até o plano segue o prego.")],
         ["ga-s5-l8q1i", "ga-s5-l8q9c", "ga-s5-l7q5"], [], f_pe)

# ---------- EQUACOES ----------
completo("eq-vetorial",
         ["Escolha um ponto A da reta e uma seta [[v]] na direção dela.",
          "Escreva X = A + t[[v]], com t real.",
          "Cada t dá um ponto: t = 0 é o A, t = 1 é A + [[v]]."],
         ("Lista 6, Q6a",
          "r: X = (1, 2, 3) + λ(1, 1, 1). Com λ = 0 sai (1, 2, 3); com λ = 1 sai (2, 3, 4); com λ = −1 sai (0, 1, 2).",
          ("(2, 3, 4)", "o ponto com λ = 1")),
         [("eq-parametricas", "Equações paramétricas", "É a mesma equação, separada por coordenada."),
          ("eq-param-plano", "Equações paramétricas do plano", "O plano precisa de duas setas e dois contadores.")],
         ["ga-s4-l4q1a", "ga-s4-l4q1b", "ga-s4-l4q1c"], ["Avaliação 1, Q8"])

checa("parametricas: t = -4", add((-1, 2, 3), esc(-4, (1, 1, 1))) == (-5, -2, -1))
completo("eq-parametricas",
         ["Separe X = A + t[[v]] em três linhas: x, y e z.",
          "Em cada linha: coordenada do ponto + t vezes a coordenada da seta.",
          "Para um ponto da reta, o mesmo t vale nas três linhas."],
         ("Lista 4, Q6",
          "r: x = −1 + t, y = 2 + t, z = 3 + t. Com t = −4: x = −5, y = −2 e z = −1.",
          ("(−5, −2, −1)", "o ponto com t = −4")),
         [("eq-vetorial", "Equação vetorial da reta", "As paramétricas são a vetorial escrita linha a linha."),
          ("eq-simetricas", "Equações simétricas", "As simétricas isolam o t de cada linha.")],
         ["ga-s4-l4q6", "ga-s4-l4q3", "ga-s5-l5q3"], ["Avaliação 1, Q4"])

completo("eq-simetricas",
         ["Isole o t em cada paramétrica: t = (x − x0)/a, t = (y − y0)/b, t = (z − z0)/c.",
          "Iguale as três frações.",
          "Se uma coordenada da seta é 0, aquela coordenada fica parada e não há simétrica com ela."],
         ("Lista 4, Q5",
          "x = 1 − 2t, y = t, z = −1 + 7t. Isolando: t = (1 − x)/2, t = y e t = (z + 1)/7. Então (1 − x)/2 = y = (z + 1)/7.",
          ("(1 − x)/2 = y = (z + 1)/7", "as três frações iguais")),
         [("eq-parametricas", "Equações paramétricas", "A simétrica sai das paramétricas."),
          ("vetor-diretor", "Vetor diretor", "Para ler o diretor, deixe x, y e z com sinal + antes.")],
         ["ga-s4-l4q1b", "ga-s4-l4q1c", "ga-s4-l4q5"], ["Avaliação 1, Q3 e Q7"])

completo("eq-geral-plano",
         ["Ache o prego [[n]] = (a, b, c).",
          "Escreva ax + by + cz + d = 0 e troque um ponto do plano para achar o d.",
          "Teste outro ponto: tem de dar 0."],
         ("Lista 5, Q1a",
          "Prego (1, 1, 1) e ponto (−1, 2, 3): x + y + z + d = 0 com −1 + 2 + 3 + d = 0, então d = −4.",
          ("x + y + z − 4 = 0", "equação geral do plano")),
         [("eq-param-plano", "Equações paramétricas do plano", "A mesma folha descrita por um ponto e duas setas."),
          ("vetor-normal", "Vetor normal", "Os números de x, y e z são o prego.")],
         ["ga-s5-l5q1a", "ga-s5-l5q2", "ga-s5-l6q3"], ["Avaliação 2, Q2, Q4 e Q8"])

u1p, w1p = (4, 2, 1), (-3, -1, 2)
checa("param plano: n = (5, -11, 2)", cross(u1p, w1p) == (5, -11, 2))
completo("eq-param-plano",
         ["Escolha um ponto A e duas setas deitadas, [[u]] e [[v]], que não sejam múltiplas.",
          "Escreva X = A + t[[u]] + s[[v]], com dois contadores.",
          "Para passar à equação geral, o prego é [[u]] × [[v]]."],
         ("Avaliação 2, Q1",
          "x = −1 + 4t − 3s, y = 2 + 2t − s, z = −3 + t + 2s: ponto (−1, 2, −3) e setas (4, 2, 1) e (−3, −1, 2). O prego é (4, 2, 1) × (−3, −1, 2) = (5, −11, 2).",
          ("(5, −11, 2)", "prego = produto vetorial das duas setas")),
         [("eq-geral-plano", "Equação geral do plano", "A geral usa o prego; a paramétrica usa duas setas deitadas."),
          ("eq-vetorial", "Equação vetorial da reta", "A reta tem uma seta e um contador.")],
         ["ga-s5-l5q7", "ga-s5-l5q8", "ga-s5-l5q9"], ["Avaliação 2, Q1 e Q3"])

p1e, p2e = (-1, 2, -3, 5), (2, -4, -4, 7)
comb = tuple(-3 * a + 2 * b for a, b in zip(p1e, p2e))
checa("feixe: -3 pi1 + 2 pi2", comb == (7, -14, 1, -1))
completo("feixe",
         ["Pegue dois planos que se cortam numa reta: π1 e π2.",
          "Todo plano por essa reta é uma mistura α·π1 + β·π2, termo solto incluído.",
          "Para achar a mistura, compare os coeficientes que você conhece."],
         ("Avaliação 5, Q9",
          "π1: −x + 2y − 3z + 5 = 0, π2: 2x − 4y − 4z + 7 = 0 e π3: mx − 14y + z + n = 0. Comparando y e z, sai α = −3 e β = 2. A mistura dá 7x − 14y + z − 1 = 0.",
          ("m = 7 e n = −1", "π3 = −3π1 + 2π2")),
         [("reta-comum", "Uma reta em comum", "É a posição dos três planos de um feixe."),
          ("calha", "Retas paralelas dois a dois", "Se o termo solto não acompanhar a mistura, sai a barraca.")],
         ["ga-s5-l8q11", "ga-s5-l8q10j"], ["Avaliação 5, Q9"])

# ---------- ANGULOS ----------
ua, va = (1, 1, 1), (1, -2, -3)
ca_ = dot(ua, va) / (norma(ua) * norma(va))
checa("angulos: 128,1 e 51,9", round(math.degrees(math.acos(ca_)), 1) == 128.1 and round(math.degrees(math.acos(abs(ca_))), 1) == 51.9)
completo("ang-vetores",
         ["cos θ = ([[u]] · [[v]]) / (‖[[u]]‖ ‖[[v]]‖), sem módulo.",
          "Produto escalar negativo dá ângulo maior que 90°.",
          "O resultado fica entre 0° e 180°."],
         ("Lista 7, Q1a",
          "Setas (1, 1, 1) e (1, −2, −3): produto escalar −4, tamanhos √3 e √14. cos θ = −4/√42, e θ ≈ 128,1°.",
          ("128,1°", "ângulo entre as setas, sem módulo")),
         [("ang-retas", "Ângulo entre retas", "Com módulo, as mesmas setas dão 51,9° entre as retas."),
          ("cossenos-diretores", "Cossenos diretores", "São ângulos de uma seta com os eixos.")],
         ["ga-s5-l7q1a"], ["Avaliação 4, Q3"])

completo("ang-retas",
         ["cos θ = |[[u]] · [[v]]| / (‖[[u]]‖ ‖[[v]]‖), com módulo.",
          "O módulo escolhe o ângulo agudo: fica entre 0° e 90°.",
          "Vale também para retas reversas: só as setas entram na conta."],
         ("Lista 7, Q1a",
          "Setas (1, 1, 1) e (1, −2, −3): |−4| / √42 ≈ 0,617, e θ ≈ 51,9°. As retas são reversas, e mesmo assim o ângulo existe.",
          ("51,9°", "ângulo entre as retas, igual ao gabarito")),
         [("ang-vetores", "Ângulo entre vetores", "Sem módulo, daria 128,1°."),
          ("ang-reta-plano", "Ângulo entre reta e plano", "Reta com plano usa seno.")],
         ["ga-s5-l7q1a", "ga-s5-l7q1e", "ga-s5-l7q7"], ["Avaliação 4, Q3 e Q7"])

vr_, nr_ = (-1, -2, 3), (2, -1, 3)
sen_r = abs(dot(vr_, nr_)) / (norma(vr_) * norma(nr_))
checa("reta-plano: 9/14 e 40 graus", dot(vr_, nr_) == 9 and round(math.degrees(math.asin(sen_r))) == 40)
completo("ang-reta-plano",
         ["sen θ = |[[v]] · [[n]]| / (‖[[v]]‖ ‖[[n]]‖), com seno.",
          "O seno entra porque o prego fica em pé: o ângulo com o plano é o que falta para 90°.",
          "[[v]] · [[n]] = 0 dá 0°: a reta é paralela ao plano ou está dentro dele."],
         ("Avaliação 4, Q1",
          "Reta com seta (−1, −2, 3) e plano 2x − y + 3z − 5 = 0: produto escalar 9, tamanhos √14 e √14. sen θ = 9/14, e θ ≈ 40°.",
          ("40°", "ângulo entre a reta e o plano")),
         [("ang-retas", "Ângulo entre retas", "Entre retas, o cosseno; com o plano, o seno."),
          ("contida", "Contida", "Ângulo 0° com ponto no plano: a reta está dentro (Lista 7, Q8).")],
         ["ga-s5-l7q1b", "ga-s5-l7q4", "ga-s5-l7q8"], ["Avaliação 4, Q1"])

n1a, n2a = (1, 1, -1), (3, -1, 1)
cos_p = abs(dot(n1a, n2a)) / (norma(n1a) * norma(n2a))
checa("planos: 80 graus", round(math.degrees(math.acos(cos_p))) == 80)
completo("ang-planos",
         ["cos θ = |[[n1]] · [[n2]]| / (‖[[n1]]‖ ‖[[n2]]‖): o ângulo entre os pregos, com módulo.",
          "Pregos múltiplos dão cos = 1 e ângulo 0°: planos paralelos.",
          "Pregos com produto escalar 0 dão 90°: planos perpendiculares."],
         ("Lista 7, Q1d",
          "π1: x + y − z + 3 = 0 e π2: 3x − y + z = 0. Pregos (1, 1, −1) e (3, −1, 1): produto escalar 1, tamanhos √3 e √11. cos θ = 1/√33, e θ ≈ 80°.",
          ("80°", "ângulo entre os planos, igual ao gabarito")),
         [("transversais", "Transversais", "Planos que se cortam têm ângulo entre 0° e 90°, sem incluir o 0°."),
          ("paralelos-distintos", "Paralelos distintos", "Ângulo 0°: cos = 1, e não 0 (avaliação 4, Q6).")],
         ["ga-s5-l7q1d", "ga-s5-l7q1c", "ga-s5-l7q2"], ["Avaliação 4, Q2, Q5 e Q6"])

c2g = 1 - F(1, 2) - F(1, 4)
checa("cossenos: cos^2 gama = 1/4", c2g == F(1, 4))
completo("cossenos-diretores",
         ["Para uma seta [[v]], cos α = vx/‖[[v]]‖, cos β = vy/‖[[v]]‖ e cos γ = vz/‖[[v]]‖.",
          "Os quadrados somam 1: cos²α + cos²β + cos²γ = 1.",
          "Para retas, o ângulo com o eixo usa módulo, então o sinal fica livre."],
         ("Lista 7, Q3",
          "45° com x e 60° com y: 1/2 + 1/4 + cos²γ = 1, então cos²γ = 1/4. As setas (√2/2, ±1/2, ±1/2) dão 4 retas diferentes.",
          ("4 retas", "uma para cada combinação de sinais")),
         [("ang-retas", "Ângulo entre retas", "O eixo é uma reta: vale o cosseno com módulo."),
          ("ang-vetores", "Ângulo entre vetores", "Com sinal fixo, seriam só 2 retas.")],
         ["ga-s5-l7q3", "ga-s5-l7q6"], ["Avaliação 4, Q4"])

# ---------- DISTANCIAS ----------
d_pp = abs(dot(ni_p, Pi) + di_p) / norma(ni_p)
checa("dist ponto-plano: raiz3/3", abs(d_pp - math.sqrt(3) / 3) < 1e-12)
completo("dist-ponto-plano",
         ["Troque as coordenadas do ponto na equação do plano.",
          "Tire o módulo do resultado.",
          "Divida pelo tamanho do prego: ‖[[n]]‖ = √(a² + b² + c²)."],
         ("Lista 8, Q1i",
          "P = (1, 2, 3) e π: −x − y − z + 7 = 0. |−1 − 2 − 3 + 7| = 1, e ‖[[n]]‖ = √3. A distância é 1/√3 = √3/3.",
          ("√3/3 ≈ 0,58", "distância de P até o plano")),
         [("pe-perpendicular", "Pé da perpendicular", "A distância é medida até o pé."),
          ("dist-planos", "Distância entre planos paralelos", "Entre planos paralelos, use um ponto de um deles.")],
         ["ga-s5-l8q1i", "ga-s5-l8q5", "ga-s5-l8q6"], ["Avaliação 5, Q6 e Q7"], f_pe)

Ph, Ah, vh = (1, 2, 3), (3, 1, -2), (2, 4, 6)
APh = sub(Ph, Ah)
wh = cross(APh, vh)
checa("dist ponto-reta: AP x v e 195/14", wh == (-14, 22, -10) and F(dot(wh, wh), dot(vh, vh)) == F(195, 14))
completo("dist-ponto-reta",
         ["Pegue um ponto A da reta e faça a seta [[AP]].",
          "O paralelogramo de [[AP]] e [[v]] tem área ‖[[AP]] × [[v]]‖.",
          "Divida pela base ‖[[v]]‖: sobra a altura, que é a distância."],
         ("Lista 8, Q1h",
          "P = (1, 2, 3) e s: (x − 3)/2 = (y − 1)/4 = (z + 2)/6. A = (3, 1, −2), [[v]] = (2, 4, 6) e [[AP]] = (−2, 1, 5). [[AP]] × [[v]] = (−14, 22, −10). Distância² = 780/56 = 195/14.",
          ("√(195/14) ≈ 3,73", "distância de P até a reta")),
         [("dist-retas-paralelas", "Distância entre retas paralelas", "Entre paralelas, é a mesma conta com um ponto de uma reta."),
          ("dist-ponto-plano", "Distância de ponto a plano", "Até um plano a conta é outra: troca na equação e divide pelo prego.")],
         ["ga-s5-l8q1h", "ga-s5-l8q4"], [])

Pq, Qq, vq = (1, 1, 1), (0, 1, -1), (1, -1, 1)
wq = cross(sub(Pq, Qq), vq)
checa("dist paralelas: raiz 2", F(dot(wq, wq), dot(vq, vq)) == 2)
completo("dist-retas-paralelas",
         ["Confirme que as setas são múltiplas e que as retas não coincidem.",
          "Pegue um ponto de uma reta.",
          "Calcule a distância desse ponto até a outra reta."],
         ("Lista 8, Q3b",
          "r: (1, 1, 1) + t(1, −1, 1) e s: x = −2k, y = 1 + 2k, z = −1 − 2k. Do ponto (1, 1, 1) até s: a seta até (0, 1, −1) é (1, 0, 2), e (1, 0, 2) × (1, −1, 1) = (2, 1, −1). Distância² = 6/3 = 2.",
          ("√2 ≈ 1,41", "distância entre as paralelas, igual ao gabarito")),
         [("dist-ponto-reta", "Distância de ponto a reta", "É a conta usada aqui."),
          ("dist-reversas", "Distância entre reversas", "Entre reversas, a conta usa o produto misto.")],
         ["ga-s5-l8q3b", "ga-s5-l8q1g", "ga-s5-l8q2"], [])

checa("dist reversas: raiz26/13", abs(2 / norma(cross(u, v)) - math.sqrt(26) / 13) < 1e-12)
completo("dist-reversas",
         ["Ponto A de uma reta, ponto B da outra e as duas setas [[u]] e [[v]].",
          "Volume da caixa: |[[AB]] · ([[u]] × [[v]])|. Área da base: ‖[[u]] × [[v]]‖.",
          "Volume dividido pela base dá a altura: a distância."],
         ("Lista 8, Q1a",
          "r: (1, 2, 3) + λ(1, 1, 1) e s: (1, 1, 1) + t(1, −2, −3). Produto misto 2, e ‖(−1, 4, −3)‖ = √26. A distância é 2/√26 = √26/13.",
          ("√26/13 ≈ 0,39", "altura do viaduto, igual ao gabarito")),
         [("reversas", "Reversas", "Só reversas têm essa distância positiva com setas não múltiplas."),
          ("dist-retas-paralelas", "Distância entre retas paralelas", "Com setas múltiplas, a caixa achata: use ponto a reta.")],
         ["ga-s5-l8q1a", "ga-s5-l8q3a"], ["Avaliação 5, Q4"], f_rev)

completo("dist-planos",
         ["Confirme que os pregos são múltiplos.",
          "Reescreva os dois planos com o mesmo prego.",
          "Distância = |d1 − d2| / ‖[[n]]‖."],
         ("Lista 8, Q1c",
          "π1: x + y + z + 1 = 0 e π2: −x − y − z + 7 = 0, que vira x + y + z − 7 = 0. |1 − (−7)| / √3 = 8/√3 = 8√3/3.",
          ("8√3/3 ≈ 4,62", "distância entre os planos, igual ao gabarito")),
         [("paralelos-distintos", "Paralelos distintos", "Só planos paralelos distintos têm distância maior que 0."),
          ("transversais", "Transversais", "Planos que se cortam têm distância 0 (Lista 8, Q1d).")],
         ["ga-s5-l8q1c", "ga-s5-l8q1d", "ga-s5-l8q5"], ["Avaliação 5, Q2 e Q5"], f_pdi)

A4, r4p, r4v = (0, 1, 2), (1, 1, 1), (1, -1, 1)
sols = [add(r4p, esc(t, r4v)) for t in (2, -2)]
checa("lugar: pontos a raiz14", all(dot(sub(s, A4), sub(s, A4)) == 14 for s in sols) and sols == [(3, -1, 3), (-1, 3, -1)])
completo("lugar-geometrico",
         ["Escreva a condição como conta: por exemplo, ‖X − A‖ = √14.",
          "Troque X pelos pontos do objeto que você tem (uma reta, um plano).",
          "As soluções são os pontos que cumprem a condição."],
         ("Lista 8, Q4",
          "Pontos de r: (1, 1, 1) + t(1, −1, 1) a √14 de A = (0, 1, 2). A distância² dá 3t² + 2 = 14, então t = 2 ou t = −2.",
          ("(3, −1, 3) e (−1, 3, −1)", "os dois pontos, iguais ao gabarito")),
         [("plano-mediador", "Plano mediador", "Um lugar geométrico famoso: mesma distância de A e de B."),
          ("equidistante", "Equidistante", "Equidistante é uma condição de lugar geométrico.")],
         ["ga-s5-l8q4", "ga-s5-l8q8"], ["Avaliação 5, Q10"])

A8, B8 = (-1, 1, 4), (2, 3, 1)
lado = tuple(2 * (b - a) for a, b in zip(A8, B8))
dir_ = dot(B8, B8) - dot(A8, A8)
checa("mediador: 6x + 4y - 6z = -4", lado == (6, 4, -6) and dir_ == -4)
M8 = esc(F(1, 2), add(A8, B8))
checa("mediador: M no plano", 3 * M8[0] + 2 * M8[1] - 3 * M8[2] + 2 == 0)
completo("plano-mediador",
         ["Iguale as distâncias ao quadrado: ‖X − A‖² = ‖X − B‖².",
          "Os quadrados de x, y e z se cancelam e sobra uma equação de 1º grau: um plano.",
          "O prego é [[AB]], e o plano passa pelo ponto médio de A e B."],
         ("Lista 8, Q8",
          "A = (−1, 1, 4) e B = (2, 3, 1): 2(3, 2, −3) · X = 14 − 18, que dá 3x + 2y − 3z + 2 = 0. O ponto médio (1/2, 2, 5/2) dá 3/2 + 4 − 15/2 + 2 = 0.",
          ("3x + 2y − 3z + 2 = 0", "plano mediador, igual ao gabarito")),
         [("lugar-geometrico", "Lugar geométrico", "O plano mediador é um lugar geométrico."),
          ("perpendiculares-planos", "Perpendiculares", "O prego do mediador é a seta [[AB]].")],
         ["ga-s5-l8q8"], ["Avaliação 5, Q10"])

r7p, r7v, A7, B7 = (1, 1, 1), (1, -1, 1), (1, 2, 3), (-1, 1, -2)
t7 = F(-2, 3)
X7 = add(r7p, esc(t7, r7v))
checa("equidistante: (1/3, 5/3, 1/3)", X7 == (F(1, 3), F(5, 3), F(1, 3)) and dot(sub(X7, A7), sub(X7, A7)) == dot(sub(X7, B7), sub(X7, B7)))
completo("equidistante",
         ["Iguale as duas distâncias ao quadrado (assim não precisa de raiz).",
          "Se o ponto está numa reta, use X = A + t[[v]] e resolva o t.",
          "Confira: as duas distâncias têm de dar iguais."],
         ("Lista 8, Q7",
          "Ponto de r: (1, 1, 1) + t(1, −1, 1) equidistante de A = (1, 2, 3) e B = (−1, 1, −2). As distâncias² dão 3t² − 2t + 5 e 3t² + 10t + 13; igualando, t = −2/3.",
          ("(1/3, 5/3, 1/3)", "o ponto equidistante, igual ao gabarito")),
         [("plano-mediador", "Plano mediador", "Todos os pontos equidistantes de A e B formam o plano mediador."),
          ("lugar-geometrico", "Lugar geométrico", "Equidistante é uma condição; o lugar é o conjunto que ela gera.")],
         ["ga-s5-l8q7"], ["Avaliação 5, Q8"])

checa("todos os termos completos", all(not t.get("esboco") for t in T) and len(T) == 14 + len(FRASES))

# ---------------- "Onde cai": avaliacoes viram links quando a questao ja esta no site ----------------
def ids_existentes():
    s = set()
    for nome in os.listdir(os.path.join(AQUI, "dados")):
        if nome.endswith(".json") and nome != "ga_vocabulario.json":
            with open(os.path.join(AQUI, "dados", nome), encoding="utf-8") as fh:
                s.update(q["id"] for q in json.load(fh).get("questoes", []))
    return s


import re  # noqa: E402

EXISTEM = ids_existentes()
for t in T:
    sobra = []
    for txt in t.get("avaliacoes", []):
        m = re.match(r"Avaliação (\d), (.*)$", txt)
        if not m:
            sobra.append(txt)
            continue
        av = int(m.group(1))
        sem = 4 if av == 1 else 5
        nums = [int(x) for x in re.findall(r"Q(\d+)", m.group(2))]
        qids = [f"ga-s{sem}-av2-t1-q{av}-{n:02d}" for n in nums]
        if nums and all(q in EXISTEM for q in qids):
            for q in qids:
                if q not in t["questoes"]:
                    t["questoes"].append(q)
        else:
            sobra.append(txt)
    if "avaliacoes" in t:
        t["avaliacoes"] = sobra

# ---------------- conferencias de estrutura ----------------
ids = [t["id"] for t in T]
checa("ids unicos", len(ids) == len(set(ids)))
grupos_ok = {g["id"] for g in GRUPOS}
for t in T:
    checa("grupo de " + t["id"], t["grupo"] in grupos_ok)
    for n in t.get("naoConfunda", []):
        checa("naoConfunda de " + t["id"] + " -> " + str(n["id"]), n["id"] in ids)
todas_q = set()
for nome in os.listdir(os.path.join(AQUI, "dados")):
    if nome.endswith(".json") and nome != "ga_vocabulario.json":
        with open(os.path.join(AQUI, "dados", nome), encoding="utf-8") as fh:
            for q in json.load(fh).get("questoes", []):
                todas_q.add(q["id"])
for t in T:
    for q in t.get("questoes", []):
        checa("questao inexistente em " + t["id"] + ": " + q, q in todas_q)
def textos(t):
    out = [t["termo"], t["frase"]] + t.get("conta", [])
    if "exemplo" in t:
        e = t["exemplo"]
        out += [e["fonte"], e["texto"], e["destaque"]["valor"], e["destaque"]["rotulo"]]
    out += [n["texto"] for n in t.get("naoConfunda", [])] + t.get("avaliacoes", [])
    if "nota" in t:
        out.append(t["nota"])
    return out


for t in T:
    for s in textos(t):
        checa("seta combinante em " + t["id"], "⃗" not in s)
        checa("hifen como menos em " + t["id"] + ": " + s[:40], not any(x in s for x in (" -", "(-", "−-")) and not s.startswith("-"))

if erros:
    print("FALHAS:", erros)
    sys.exit(1)

saida = {"disciplina": "ga", "vocabulario": {"semanas": [4, 5], "grupos": GRUPOS, "termos": T}}
with open(ARQ, "w", encoding="utf-8") as fh:
    json.dump(saida, fh, ensure_ascii=False, indent=2)
completos = [t for t in T if not t.get("esboco")]
print("vocabulario:", len(T), "termos |", len(completos), "completos |", len(T) - len(completos), "so titulo | contas OK")
