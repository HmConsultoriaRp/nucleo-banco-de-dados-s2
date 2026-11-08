# Monta as "Ideias da semana" de Geometria (Semanas 4 e 5) e grava em dados/ga_s45_p1.json.
# Texto: base_semana2.md (pasta Geometria analitica\Semana 2\Explicacao de base).
# As coordenadas das figuras saem de conta; cada numero do texto e conferido aqui antes de gravar.
# Uso: python -I montar_ideias.py   (para em erro se alguma conta nao bater)
import json
import math
import os
import sys
from fractions import Fraction as F

AQUI = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(AQUI, "dados", "ga_s45_p1.json")
erros = []


def checa(nome, cond):
    if not cond:
        erros.append(nome)


# ---------------- vetores ----------------
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


# ---------------- itens da figura ----------------
def folha(centro, e1, e2, a, b, cor=1):
    cs = [add(add(centro, esc(sa * a, e1)), esc(sb * b, e2)) for sa, sb in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
    return {"tipo": "poligono", "pts": [r3(c) for c in cs], "cor": cor}


def poli(pts, cor=3, aberto=False):
    it = {"tipo": "poligono", "pts": [r3(p) for p in pts], "cor": cor}
    if aberto:
        it["aberto"] = True
    return it


def ponto(p, rot, cor=4):
    return {"tipo": "ponto", "em": r3(p), "rot": rot, "cor": cor}


def vetor(de, ate, rot, cor):
    return {"tipo": "vetor", "de": r3(de), "ate": r3(ate), "rot": rot, "cor": cor}


def reta(p, v, t0, t1, cor, largura=3):
    return {"tipo": "segmento", "de": r3(add(p, esc(t0, v))), "ate": r3(add(p, esc(t1, v))), "cor": cor, "largura": largura}


def seg(de, ate, cor=None, largura=None, tracejado=False):
    it = {"tipo": "segmento", "de": r3(de), "ate": r3(ate)}
    if cor:
        it["cor"] = cor
    if largura:
        it["largura"] = largura
    if tracejado:
        it["tracejado"] = True
    return it


def trac(de, ate, cor=None, largura=None):
    return seg(de, ate, cor, largura if largura else (2.4 if cor else 2), True)


def fig(itens, angulo=None, sem_eixos=False, moldura=None):
    f = {"modo": "3d", "itens": itens}
    if angulo:
        f["angulo"] = angulo
    if sem_eixos:
        f["semEixos"] = True
    if moldura:
        f["moldura"] = [r3(p) for p in moldura]
    return f


# ---------------- angulos de vista ----------------
# A direcao de visao do figura.js e d = (-sen yaw cos pitch, -cos yaw cos pitch, sen pitch).
def angulo_para(d):
    d = unit(d)
    if d[2] < 0:
        d = tuple(-x for x in d)
    pitch = min(math.asin(d[2]), 1.35)
    cp = math.cos(pitch)
    yaw = math.atan2(-d[0] / cp, -d[1] / cp)
    return {"yaw": round(yaw, 3), "pitch": round(pitch, 3)}


def angulo_folha(n, graus=60, apoio=(0, 0, 1)):
    """Olha a folha de normal n inclinado `graus` em relacao ao prego: a folha aparece de frente e o prego aparece."""
    nh = unit(n)
    e = cross(n, apoio)
    if norma(e) < 1e-9:
        e = cross(n, (1, 0, 0))
    eh = unit(e)
    t = math.radians(graus)
    return angulo_para(tuple(math.cos(t) * a + math.sin(t) * b for a, b in zip(nh, eh)))


ANG_PADRAO = {"yaw": -0.62, "pitch": 0.42}
ANG_FOLHA = {"yaw": 0.6, "pitch": 0.45}      # folha de normal (1, 1, 1) de frente
ANG_DIST = {"yaw": 0.0, "pitch": 0.4}        # folha mais de lado: o tracejado de 90 graus aparece


def ideia(id_, titulo, frase, fonte, questoes, passos):
    return {"id": id_, "titulo": titulo, "frase": frase, "fonte": fonte, "questoes": questoes, "passos": passos}


def passo(titulo, texto, f, destaque=None):
    p = {"titulo": titulo, "texto": texto, "fig": f}
    if destaque:
        p["destaque"] = {"valor": destaque[0], "rotulo": destaque[1]}
    return p


# =====================================================================
# SEMANA 4 (Lista 4: retas)
# =====================================================================
S4 = []

# --- 4.1 Ponto e vetor (Lista 4, Q2) ---
A, B = (-1, 1, 4), (2, 3, 1)
AB = sub(B, A)
checa("4.1 B - A", AB == (3, 2, -3))
f1 = [ponto(A, "A"), ponto(B, "B")]
S4.append(ideia(
    "ponto-vetor", "Ponto e vetor", "Ponto diz onde estou; vetor diz como ando.", "Lista 4, Q2",
    ["ga-s4-l4q2", "ga-s4-l4q3", "ga-s4-l4q4"],
    [
        passo("Dois endereços", "Ponto é endereço: onde estou. A = (−1, 1, 4) e B = (2, 3, 1) são dois lugares do espaço (Lista 4, Q2).",
              fig(f1, ANG_PADRAO)),
        passo("A seta de A até B", "Vetor é deslocamento: como ando. A seta de A até B é B − A = (2, 3, 1) − (−1, 1, 4) = (3, 2, −3): ande 3 em x, 2 em y e −3 em z.",
              fig(f1 + [vetor(A, B, "B − A", 1)], ANG_PADRAO), ("B − A = (3, 2, −3)", "a seta que leva de A até B")),
        passo("Direção e sentido", "Direção é a linha em que a seta está; sentido é o lado para onde ela aponta. (3, 2, −3) e (−3, −2, 3) têm a mesma direção e sentidos opostos. Ponto e vetor se escrevem igual, com três números: por isso confundem.",
              fig(f1 + [vetor(A, B, "B − A", 1), vetor(A, sub(A, AB), "A − B", 2)], ANG_PADRAO)),
    ]))

# --- 4.2 Reta: um ponto e um passo (Lista 4, Q1a) ---
A, v = (-1, 2, 3), (1, 1, 1)
pts_t = {t: add(A, esc(t, v)) for t in (-1, 0, 1, 2)}
checa("4.2 t=1", pts_t[1] == (0, 3, 4))
checa("4.2 t=-1", pts_t[-1] == (-2, 1, 2))
checa("4.2 t=2", pts_t[2] == (1, 4, 5))
mold42 = [add(A, esc(-1.8, v)), add(A, esc(2.8, v))]
S4.append(ideia(
    "reta-passo", "Reta: um ponto e um passo", "Saia do ponto e ande na direção da seta, para frente ou para trás, sem fim.", "Lista 4, Q1a",
    ["ga-s4-l4q1a", "ga-s4-l4q1b", "ga-s4-l4q1c"],
    [
        passo("O ponto e a seta", "Reta = um ponto + uma seta que dá a direção, o vetor diretor. Lista 4, Q1a: A = (−1, 2, 3) e [[v]] = (1, 1, 1).",
              fig([ponto(A, "A"), vetor(A, add(A, v), "v", 2)], ANG_PADRAO, moldura=mold42)),
        passo("O contador t", "X = (−1, 2, 3) + t(1, 1, 1). O t conta os passos, e cada passo é a seta inteira: t = 0 está em A; t = 1 chega em (0, 3, 4); t = −1 é um passo para trás, (−2, 1, 2); t = 1/2 é meio passo.",
              fig([ponto(pts_t[0], "A"), ponto(pts_t[1], "t = 1"), ponto(pts_t[-1], "t = −1"), ponto(pts_t[2], "t = 2"), vetor(A, add(A, v), "", 2)], ANG_PADRAO, moldura=mold42)),
        passo("A reta inteira", "Com t passando por todos os números, inclusive frações e negativos, os pontos formam a reta inteira.",
              fig([reta(A, v, -1.8, 2.8, 1), ponto(A, "A"), vetor(A, add(A, v), "v", 2)], ANG_PADRAO, moldura=mold42),
              ("X = (−1, 2, 3) + t(1, 1, 1)", "forma vetorial da reta, igual ao gabarito")),
    ]))

# --- 4.3 Parametrica (Lista 4, Q1a) ---
p2t = add(A, esc(2, v))
checa("4.3 t=2", p2t == (1, 4, 5))
base43 = [reta(A, v, -1.8, 2.8, 1), ponto(A, "A")]
S4.append(ideia(
    "parametrica", "Paramétrica: a reta como planilha", "Mude o t e as três fórmulas recalculam, como a célula de entrada de uma planilha.", "Lista 4, Q1a",
    ["ga-s4-l4q1a", "ga-s4-l4q2", "ga-s4-l4q3"],
    [
        passo("Três fórmulas", "É a mesma reta, aberta coordenada por coordenada: x = −1 + t, y = 2 + t, z = 3 + t.",
              fig(base43, ANG_PADRAO, moldura=mold42)),
        passo("Dê um valor para t", "Parâmetro é o número livre, como a célula de entrada de uma planilha. Com t = 2: x = −1 + 2 = 1, y = 2 + 2 = 4, z = 3 + 2 = 5. São dois passos a partir de A.",
              fig(base43 + [vetor(A, add(A, v), "", 2), vetor(add(A, v), p2t, "", 2), ponto(p2t, "t = 2")], ANG_PADRAO, moldura=mold42),
              ("t = 2 → (1, 4, 5)", "o ponto está na reta")),
        passo("No seu trabalho", "Pense em três contas com movimento fixo por mês: saldo inicial + t meses × movimento. Cada conta é uma linha da paramétrica; o saldo inicial é o ponto A e o movimento é a seta.",
              fig(base43 + [ponto(p2t, "t = 2")], ANG_PADRAO, moldura=mold42)),
    ]))

# --- 4.4 Simetrica (Lista 4, Q1c, Q5, Q1b) ---
Ac, vc = (2, 1, 3), (2, 1, -2)
Pq5, vq5 = (1, 0, -1), (-2, 1, 7)
checa("4.4 Q5 ponto", ((1 - Pq5[0]), Pq5[1], (Pq5[2] + 1)) == (0, 0, 0))
q = add(Pq5, vq5)
checa("4.4 Q5 direcao", F(1 - q[0], 2) == q[1] == F(q[2] + 1, 7))
Ab, vb = (0, 1, 2), (2, 3, 0)
dentro, fora = (1, 4, 5), (1, 4, 6)
checa("4.4 dentro", (dentro[0] + 1, dentro[1] - 2, dentro[2] - 3) == (2, 2, 2))
checa("4.4 fora", (fora[0] + 1, fora[1] - 2, fora[2] - 3) == (2, 2, 3))
S4.append(ideia(
    "simetrica", "Simétrica: três partes iguais", "Isole o t em cada linha e iguale: as três partes valem o mesmo t.", "Lista 4, Q1c e Q5",
    ["ga-s4-l4q1c", "ga-s4-l4q5", "ga-s4-l4q1b"],
    [
        passo("Isole o t", "Lista 4, Q1c: x = 2 + 2t, y = 1 + t, z = 3 − 2t. Isolando: t = (x − 2)/2, t = y − 1, t = (3 − z)/2. Como as três valem t, iguale.",
              fig([reta(Ac, vc, -1.5, 1.5, 1), ponto(Ac, "(2, 1, 3)"), vetor(Ac, add(Ac, vc), "v", 2)], ANG_PADRAO),
              ("(x − 2)/2 = y − 1 = (3 − z)/2", "equação simétrica, igual ao gabarito")),
        passo("Como ler", "Ponto: o valor que zera cada parte de cima. Direção: o número de baixo; se a variável vier com menos, ele troca de sinal. Lista 4, Q5: (1 − x)/2 = y = (z + 1)/7.",
              fig([reta(Pq5, vq5, -0.6, 0.9, 1), ponto(Pq5, "P"), vetor(Pq5, add(Pq5, vq5), "v", 2)], ANG_PADRAO),
              ("P = (1, 0, −1) e v = (−2, 1, 7)", "igual ao gabarito")),
        passo("Quando não existe", "Se a direção tem um zero, não dá para dividir por zero. Lista 4, Q1b: [[v]] = (2, 3, 0). O z fica parado em 2: a reta corre deitada, paralela ao chão. O gabarito diz \"não tem\".",
              fig([reta(Ab, vb, -1.2, 1.2, 1), ponto(Ab, "(0, 1, 2)"), vetor(Ab, add(Ab, vb), "v", 2)], ANG_PADRAO)),
        passo("Para que serve", "É uma conciliação: um ponto está na reta se as três partes derem o mesmo t. Com x + 1 = y − 2 = z − 3: (1, 4, 5) dá 2, 2 e 2 (está); (1, 4, 6) dá 2, 2 e 3 (não está).",
              fig([reta((-1, 2, 3), (1, 1, 1), -1.5, 2.8, 1), ponto(dentro, "dentro", 1), ponto(fora, "fora", 2)], ANG_PADRAO),
              ("2 = 2 = 2", "as três partes batem: o ponto está na reta")),
    ]))

# --- 4.5 Encontro de duas retas (Lista 4, Q6) ---
r_p, r_v = (-1, 2, 3), (1, 1, 1)
s_p, s_v = (2, 4, 1), (7, 6, 2)
lam = F(2) - 3
t = 2 + 7 * lam + 1
enc = add(r_p, esc(t, r_v))
checa("4.5 lambda", lam == -1)
checa("4.5 t", t == -4)
checa("4.5 prova z", r_p[2] + t == s_p[2] + 2 * lam)
checa("4.5 encontro", enc == (-5, -2, -1) and add(s_p, esc(lam, s_v)) == enc)
retas45 = [reta(r_p, r_v, -7, -1, 1), reta(s_p, s_v, F(-17, 10), F(-3, 10), 2)]
S4.append(ideia(
    "encontro-retas", "Onde duas retas se cruzam", "Uma letra de contador para cada reta; a terceira equação é a prova.", "Lista 4, Q6",
    ["ga-s4-l4q6", "ga-s4-l4q7"],
    [
        passo("Duas retas, dois contadores", "r: x = −1 + t, y = 2 + t, z = 3 + t e s: X = (2, 4, 1) + λ(7, 6, 2). Use letras diferentes, t e λ: com a mesma letra, você exigiria o mesmo número de passos nas duas.",
              fig(retas45, ANG_PADRAO)),
        passo("Iguale e resolva", "x: −1 + t = 2 + 7λ. y: 2 + t = 4 + 6λ. Tire a primeira da segunda: 3 = 2 − λ, então λ = −1. Volte na primeira: −1 + t = 2 − 7, então t = −4.",
              fig(retas45, ANG_PADRAO), ("t = −4 e λ = −1", "duas equações acham os dois contadores")),
        passo("A prova", "A terceira confere, como numa conciliação. z: 3 + (−4) = −1 e 1 + 2(−1) = −1. Bateu: as retas se cruzam. Se não batesse, seriam reversas ou paralelas.",
              fig(retas45 + [ponto(enc, "(−5, −2, −1)")], ANG_PADRAO), ("(−5, −2, −1)", "ponto de encontro, igual ao gabarito")),
    ]))

# =====================================================================
# SEMANA 5 (Listas 5 a 8: planos, posicao, angulos, distancias)
# =====================================================================
S5 = []
O = (0, 0, 0)

# --- 5.1 Angulo entre duas setas (Lista 7, Q1a) ---
u, v = (1, 1, 1), (1, -2, -3)
checa("5.1 u.v", dot(u, v) == -4)
checa("5.1 normas", (dot(u, u), dot(v, v)) == (3, 14))
cosang = abs(dot(u, v)) / (norma(u) * norma(v))
checa("5.1 cos", abs(cosang - 0.617) < 0.0005)
checa("5.1 graus", round(math.degrees(math.acos(cosang)), 1) == 51.9)
fu = [vetor(O, u, "u", 1), vetor(O, v, "v", 2)]
S5.append(ideia(
    "angulo", "Ângulo entre duas setas", "A abertura entre duas setas que saem do mesmo lugar; o cosseno mede de −1 a 1.", "Lista 7, Q1a",
    ["ga-s5-l7q1a", "ga-s5-l7q1e", "ga-s5-l7q7"],
    [
        passo("Do mesmo ponto", "Ângulo é a abertura entre duas setas que saem do mesmo lugar, como os ponteiros do relógio. O tamanho das setas não muda o ângulo. Aqui [[u]] = (1, 1, 1) e [[v]] = (1, −2, −3), direções da Lista 7, Q1a.",
              fig(fu, ANG_PADRAO)),
        passo("Produto escalar", "É um SOMARPRODUTO: multiplique par a par e some. (1, 1, 1) · (1, −2, −3) = 1 − 2 − 3 = −4.",
              fig(fu, ANG_PADRAO), ("u · v = −4", "o sinal diz se a abertura passa de 90°")),
        passo("Comprimentos", "Norma é o comprimento da seta: a raiz da soma dos quadrados. ‖[[u]]‖ = √3 e ‖[[v]]‖ = √14.",
              fig(fu, ANG_PADRAO), ("√3 e √14", "os comprimentos das duas setas")),
        passo("O ângulo", "cos θ = |−4| / (√3 · √14) ≈ 0,617. Entre retas vale a menor abertura, de 0° a 90°: por isso o módulo. No Excel: =GRAUS(ACOS(0,617)).",
              fig(fu, ANG_PADRAO), ("≈ 51,9°", "ângulo entre as retas, igual ao gabarito")),
    ]))

# --- 5.2 Plano: folha e prego (Lista 5, Q1a) ---
A = (-1, 2, 3)
n = (1, 1, 1)
X = (1, 1, 2)
e1, e2 = (1, -1, 0), (1, 1, -2)
checa("5.2 X no plano", dot(n, X) == 4)
checa("5.2 A no plano", dot(n, A) == 4)
checa("5.2 X-A deitada", dot(n, sub(X, A)) == 0)
C1 = add(add(A, esc(F(3, 4), e1)), esc(F(1, 4), e2))
fol1 = folha(C1, e1, e2, 1.3, 0.6)
mold1 = [add(A, n), add(C1, esc(1.3, e1)), add(C1, esc(-1.3, e1)), add(C1, esc(0.6, e2)), add(C1, esc(-0.6, e2))]
it_A, it_n, it_X, it_XA = ponto(A, "A"), vetor(A, add(A, n), "n", 2), ponto(X, "X"), vetor(A, X, "X − A", 1)
S5.append(ideia(
    "plano-prego", "Plano: uma folha e um prego", "Um ponto e um vetor normal em pé bastam para escrever o plano.", "Lista 5, Q1a",
    ["ga-s5-l5q1a", "ga-s5-l5q1b", "ga-s5-l5q1c", "ga-s5-l5q2"],
    [
        passo("A folha", "Plano é uma folha lisa, sem espessura e sem fim, como um tampo de mesa que não acaba. Esta passa pelo ponto A = (−1, 2, 3).",
              fig([fol1, it_A], ANG_FOLHA, moldura=mold1)),
        passo("O prego", "O vetor normal [[n]] = (1, 1, 1) é um prego espetado em pé na folha. Aqui \"normal\" não quer dizer comum: quer dizer perpendicular.",
              fig([fol1, it_A, it_n], ANG_FOLHA, moldura=mold1)),
        passo("Uma seta deitada", "Pegue qualquer ponto X da folha, por exemplo (1, 1, 2). A seta de A até X fica deitada na folha e faz 90° com o prego. Arraste a figura para conferir de lado.",
              fig([fol1, it_A, it_n, it_X, it_XA], ANG_FOLHA, moldura=mold1)),
        passo("A conta", "90° quer dizer produto escalar 0: [[n]] · (X − A) = 0. Com X = (x, y, z): 1(x + 1) + 1(y − 2) + 1(z − 3) = 0.\nTeste: (1, 1, 2) dá 1 + 1 + 2 − 4 = 0. Está na folha.",
              fig([fol1, it_A, it_n, it_X, it_XA], ANG_FOLHA, moldura=mold1), ("x + y + z − 4 = 0", "equação geral do plano, igual ao gabarito")),
    ]))

# --- 5.3 Duas retas, os quatro casos (Lista 4 Q6 e Lista 6) ---
f_conc = fig(retas45 + [ponto(enc, "(−5, −2, −1)")], ANG_PADRAO)
pr, vr = (1, 1, 1), (1, -1, 1)
ps, vs = (0, 1, -1), (-2, 2, -2)
checa("5.3 paralelas: multiplos", cross(vr, vs) == (0, 0, 0))
checa("5.3 paralelas: (1,1,1) fora de s", cross(sub(pr, ps), vs) != (0, 0, 0))
f_par = fig([reta(pr, vr, -2, 2, 1), reta(ps, vs, -1, 1, 2), ponto(pr, "r"), ponto(ps, "s")], ANG_PADRAO)
p1, u = (1, 2, 3), (1, 1, 1)
p2, v = (1, 1, 1), (1, -2, -3)
w0 = sub(p1, p2)
a_, b_, c_ = dot(u, u), dot(u, v), dot(v, v)
d_, e_ = dot(u, w0), dot(v, w0)
den = a_ * c_ - b_ * b_
sc = F(b_ * e_ - c_ * d_, den)
tc = F(a_ * e_ - b_ * d_, den)
q1, q2 = add(p1, esc(sc, u)), add(p2, esc(tc, v))
checa("5.3 perpendicular comum a u", dot(sub(q1, q2), u) == 0)
checa("5.3 perpendicular comum a v", dot(sub(q1, q2), v) == 0)
checa("5.3 folga = sqrt(26)/13", abs(norma(sub(q1, q2)) - math.sqrt(26) / 13) < 1e-12)
# olhar pela bissetriz das direcoes, inclinado 35 graus para o lado da folga: retas em X e folga visivel.
# Olhar exatamente de lado da folga (ou pela bissetriz pura) faz as duas parecerem paralelas.
_b = unit(add(unit(u), unit(v)))
_w = unit(cross(u, v))
_t = math.radians(35)
ANG_REV = angulo_para(tuple(math.cos(_t) * x + math.sin(_t) * y for x, y in zip(_b, _w)))
retas_rev = [reta(p1, u, float(sc) - 0.6, float(sc) + 0.6, 1), reta(p2, v, float(tc) - 0.28, float(tc) + 0.28, 2), trac(q1, q2, 3)]
f_rev = fig(retas_rev, ANG_REV, sem_eixos=True)
pc, vc = (1, 1, 1), (1, -2, 3)
vs2 = (-2, 4, -6)
checa("5.3 coincidentes: multiplos", cross(vc, vs2) == (0, 0, 0))
f_coi = fig([reta(pc, vc, -1.2, 1.2, 2), reta(pc, vc, -1.2, 1.2, 1), vetor(pc, add(pc, vc), "r", 1), vetor(pc, add(pc, esc(F(1, 2), vs2)), "s", 2), ponto(pc, "(1, 1, 1)")], ANG_PADRAO)
S5.append(ideia(
    "duas-retas", "Duas retas: os quatro casos", "Compare as setas primeiro. O ponto só desempata.", "Lista 4, Q6 e Lista 6",
    ["ga-s5-l6q5a", "ga-s5-l6q6a", "ga-s5-l6q6e", "ga-s5-l6q1"],
    [
        passo("Concorrentes: se cruzam", "Direções diferentes e um ponto em comum. Na Lista 4, Q6, a reta azul e a coral se encontram em (−5, −2, −1).",
              f_conc, ("1 ponto em comum", "direções diferentes")),
        passo("Paralelas: dois trilhos", "Mesma direção: (−2, 2, −2) é −2 vezes (1, −1, 1), um trem indo e outro voltando. Mas o ponto (1, 1, 1) da azul não está na coral (Lista 6, Q5).",
              f_par, ("0 ponto em comum", "mesma direção")),
        passo("Reversas: o viaduto", "Direções diferentes e nenhum ponto em comum. Só existe em 3D: arraste a figura e veja uma passar por cima da outra. O tracejado é a folga entre elas (Lista 6, Q6a).",
              f_rev, ("0 ponto em comum", "direções diferentes")),
        passo("Coincidentes: a mesma reta", "As setas são múltiplas, (−2, 4, −6) = −2 · (1, −2, 3), e o ponto (1, 1, 1) está nas duas. É a mesma linha escrita de dois jeitos: a coral fica escondida embaixo da azul (Lista 6, Q6e).",
              f_coi, ("todos os pontos em comum", "mesma direção")),
    ]))

# --- 5.4 O que o professor compara (Lista 7, Q8, Q1b, Q1d) ---
P8, v8, n8 = (-2, -1, 1), (6, 0, -3), (2, -3, 4)
checa("5.4 Q8 v.n", dot(v8, n8) == 0)
checa("5.4 Q8 ponto no plano", dot(n8, P8) - 3 == 0)
g8 = unit(cross(n8, v8))
fol8 = folha(P8, unit(v8), g8, 2.4, 1.6)
fa = fig([fol8, reta(P8, v8, -0.35, 0.35, 4), vetor(P8, add(P8, unit(n8)), "n", 2), vetor(P8, add(P8, esc(0.25, v8)), "v", 1)], angulo_folha(n8, 62), sem_eixos=True)
Pb, vb5, nb = (1, 2, 3), (1, 1, 1), (1, 1, 1)
lb = F(-(dot(nb, Pb) + 1), dot(nb, vb5))
Hb = add(Pb, esc(lb, vb5))
checa("5.4 Q1b pe no plano", dot(nb, Hb) + 1 == 0)
checa("5.4 Q1b multiplos", cross(vb5, nb) == (0, 0, 0))
folb = folha(Hb, unit((1, -1, 0)), unit((1, 1, -2)), 2.0, 2.0)
fb = fig([folb, reta(Hb, vb5, -1.6, 1.6, 4), ponto(Hb, "")], angulo_folha(nb, 70), sem_eixos=True)
n1d, n2d = (1, 1, -1), (3, -1, 1)
cosd = abs(dot(n1d, n2d)) / (norma(n1d) * norma(n2d))
checa("5.4 Q1d cos = 1/raiz(33)", abs(cosd - 1 / math.sqrt(33)) < 1e-12)
checa("5.4 Q1d angulo ~ 80", round(math.degrees(math.acos(cosd))) == 80)
Pd = (F(-3, 4), F(-9, 4), 0)
checa("5.4 Q1d ponto nos dois", dot(n1d, Pd) + 3 == 0 and dot(n2d, Pd) == 0)
dd_ = cross(n1d, n2d)
checa("5.4 Q1d reta comum", dd_ == (0, -4, -4))
ud = unit(dd_)
fd = fig([folha(Pd, ud, unit(cross(n1d, dd_)), 1.6, 1.3, 1), folha(Pd, ud, unit(cross(n2d, dd_)), 1.6, 1.3, 2),
          vetor(Pd, add(Pd, unit(n1d)), "n₁", 1), vetor(Pd, add(Pd, unit(n2d)), "n₂", 2)], angulo_para((1, 0.15, 0.35)), sem_eixos=True)
S5.append(ideia(
    "compara", "O que o professor compara", "Reta usa a direção; plano usa o prego. Compare as setas e depois teste um ponto.", "Lista 7, Q8, Q1b e Q1d",
    ["ga-s5-l7q8", "ga-s5-l7q1b", "ga-s5-l7q1d", "ga-s5-l6q6b"],
    [
        passo("Reta deitada na folha", "Reta paralela ao plano faz 90° com o prego: [[v]] · [[n]] = 0. Lista 7, Q8: (6, 0, −3) · (2, −3, 4) = 12 − 12 = 0. Desempate: o ponto (−2, −1, 1) dá 2(−2) − 3(−1) + 4(1) − 3 = 0. A reta está contida no plano.",
              fa, ("v · n = 0", "paralela ou contida; o ponto desempata")),
        passo("Reta em pé", "Reta perpendicular ao plano fica na direção do prego: [[v]] e [[n]] são múltiplos. Lista 7, Q1b: (1, 1, 1) e (1, 1, 1). Parece trocado, mas não é erro: o prego já é perpendicular à folha.",
              fb, ("90°", "ângulo entre a reta e o plano, igual ao gabarito")),
        passo("Plano com plano", "Entre dois planos, compare os dois pregos: cos θ = |n₁ · n₂| / (‖n₁‖ ‖n₂‖). Lista 7, Q1d: |3 − 1 − 1| / (√3 · √11) = 1/√33.",
              fd, ("≈ 80°", "ângulo entre os planos, igual ao gabarito")),
    ]))

# --- 5.5 Reta de dois planos (Lista 5, Q3) ---
n1, n2 = (1, 1, 1), (1, -1, 1)
d53 = cross(n1, n2)
checa("5.5 direcao", d53 == (2, 0, -2))
P0 = (0, F(-1, 2), F(3, 2))
checa("5.5 ponto nos dois", dot(n1, P0) == 1 and dot(n2, P0) == 2)
ud53 = unit(d53)
f55a = folha(P0, ud53, unit(cross(n1, d53)), 1.7, 1.2, 1)
f55b = folha(P0, ud53, unit(cross(n2, d53)), 1.7, 1.2, 2)
# as duas folhas de frente o bastante (d . n1 ~ 0,83 e d . n2 ~ 0,57) e a reta comum visivel
ang55 = angulo_para((1.0, 0.25, 0.3))
S5.append(ideia(
    "reta-dois-planos", "A reta que nasce de dois planos", "A direção é o produto vetorial dos dois pregos.", "Lista 5, Q3",
    ["ga-s5-l5q3", "ga-s5-l7q6"],
    [
        passo("Duas folhas que se cortam", "x + y + z = 1 e x − y + z = 2 são duas folhas que se encontram numa linha, como as metades de um livro aberto na lombada.",
              fig([f55a, f55b], ang55, sem_eixos=True)),
        passo("A direção", "A reta está deitada nas duas folhas: faz 90° com os dois pregos ao mesmo tempo. A seta que faz 90° com outras duas é o produto vetorial: (1, 1, 1) × (1, −1, 1) = (2, 0, −2).",
              fig([f55a, f55b, reta(P0, ud53, -1.9, 1.9, 4), vetor(P0, add(P0, unit(n1)), "n₁", 1), vetor(P0, add(P0, unit(n2)), "n₂", 2)], ang55, sem_eixos=True),
              ("(2, 0, −2)", "direção da reta")),
        passo("Um ponto", "Escolha um valor fácil para uma letra. Com x = 0: y + z = 1 e −y + z = 2. Somando, 2z = 3: z = 3/2 e y = −1/2. Ponto (0, −1/2, 3/2).",
              fig([f55a, f55b, reta(P0, ud53, -1.9, 1.9, 4), ponto(P0, "(0, −1/2, 3/2)")], ang55, sem_eixos=True),
              ("x = 2t, y = −1/2, z = 3/2 − 2t", "igual ao gabarito")),
    ]))

# --- 5.6 Angulo com os eixos (Lista 7, Q3 e Q6) ---
c2g = 1 - F(1, 2) - F(1, 4)
checa("5.6 cos2 gama", c2g == F(1, 4))
vq3 = (math.sqrt(2) / 2, 0.5, 0.5)
checa("5.6 45 com x", abs(math.degrees(math.acos(vq3[0] / norma(vq3))) - 45) < 1e-9)
checa("5.6 60 com y", abs(math.degrees(math.acos(vq3[1] / norma(vq3))) - 60) < 1e-9)
dq6 = cross((1, -1, 3), (3, -2, 1))
checa("5.6 Q6 direcao", dq6 == (5, 8, 1))
checa("5.6 Q6 83,9", round(math.degrees(math.acos(1 / norma(dq6))), 1) == 83.9)
s2 = math.sqrt(2) / 2
quatro = [(s2, 0.5, 0.5), (s2, 0.5, -0.5), (s2, -0.5, 0.5), (s2, -0.5, -0.5)]
mold56 = [(1.1, 0, 0), (0, 1.1, 0), (0, 0, 1.1), (0, -0.6, -0.6)]
S5.append(ideia(
    "angulo-eixos", "Ângulo com os eixos", "Eixo também é reta: os três cossenos ao quadrado fecham 1.", "Lista 7, Q3 e Q6",
    ["ga-s5-l7q3", "ga-s5-l7q6"],
    [
        passo("Eixo é reta", "O eixo x tem direção (1, 0, 0); o y, (0, 1, 0); o z, o \"eixo das cotas\", (0, 0, 1). Com [[v]] = (a, b, c): cos α = |a| / ‖v‖ com o x, e o mesmo com b e c para y e z.",
              fig([vetor(O, quatro[0], "v", 2)], ANG_PADRAO, moldura=mold56)),
        passo("Os cossenos fecham 1", "cos²α + cos²β + cos²γ = 1, como participações que somam 100% (Lista 3, Q5). Lista 7, Q3 pede 45° com x e 60° com y: 1/2 + 1/4 = 3/4. Falta 1/4.",
              fig([vetor(O, quatro[0], "v", 2)], ANG_PADRAO, moldura=mold56), ("cos γ = ±1/2", "o que falta para fechar 1")),
        passo("Quatro retas", "Reta não tem ida nem volta: os sinais do y e do z podem trocar. São 4 direções, (√2/2, ±1/2, ±1/2), e 4 retas por (1, 2, 3), como no gabarito.",
              fig([vetor(O, quatro[0], "", 2), vetor(O, quatro[1], "", 1), vetor(O, quatro[2], "", 2), vetor(O, quatro[3], "", 1)], ANG_PADRAO, moldura=mold56),
              ("4 retas", "trocar os três sinais juntos não cria reta nova")),
        passo("Com o eixo z", "Lista 7, Q6: a reta é encontro de dois planos, então a direção é (1, −1, 3) × (3, −2, 1) = (5, 8, 1). Com o eixo z: cos γ = 1/√90.",
              fig([vetor(O, dq6, "(5, 8, 1)", 2)], ANG_PADRAO), ("≈ 83,9°", "ângulo com o eixo das cotas, igual ao gabarito")),
    ]))

# --- 5.7 Parte deitada e parte em pe (Lista 6, Q10) ---
n10 = cross((-2, 1, -2), (1, 1, 0))
checa("5.7 normal", n10 == (2, -2, -3))
O10 = (0, 0, -2)
checa("5.7 O10 no plano", dot(n10, O10) - 6 == 0)
v10 = (1, -1, -2)
k10 = F(dot(v10, n10), dot(n10, n10))
checa("5.7 v.n e n.n", (dot(v10, n10), dot(n10, n10)) == (10, 17))
v2_ = esc(k10, n10)
v1_ = sub(v10, v2_)
checa("5.7 em pe", v2_ == (F(20, 17), F(-20, 17), F(-30, 17)))
checa("5.7 deitada", v1_ == (F(-3, 17), F(3, 17), F(-4, 17)))
checa("5.7 prova", dot(v1_, n10) == 0)
g10 = unit(cross(n10, (0, 0, 1)))
fol10 = folha(add(O10, esc(0.5, v1_)), g10, unit(cross(n10, g10)), 1.6, 1.3)
ang57 = angulo_folha(n10, 72)
mold57 = [add(O10, v10), add(O10, v2_)]
it_v = vetor(O10, add(O10, v10), "v", 4)
it_v2 = vetor(O10, add(O10, v2_), "em pé", 2)
it_v1 = vetor(O10, add(O10, v1_), "deitada", 1)
S5.append(ideia(
    "deitada-em-pe", "Parte deitada e parte em pé", "A sombra no chão e a altura: a seta é a soma das duas partes.", "Lista 6, Q10",
    ["ga-s5-l6q10a", "ga-s5-l6q10b"],
    [
        passo("A seta e a folha", "Plano 2x − 2y − 3z − 6 = 0 (Lista 6, Q10a), com prego [[n]] = (2, −2, −3), e a seta [[v]] = (1, −1, −2). Pense no sol a pino: a sombra da seta no chão é a parte deitada.",
              fig([fol10, it_v], ang57, sem_eixos=True, moldura=mold57)),
        passo("A parte em pé", "Parte em pé = (v · n / n · n) · n. Aqui v · n = 2 + 2 + 6 = 10 e n · n = 4 + 4 + 9 = 17. Então (10/17) · (2, −2, −3) = (20/17, −20/17, −30/17).",
              fig([fol10, it_v, it_v2], ang57, sem_eixos=True, moldura=mold57), ("10/17 do prego", "v · n = 10 e n · n = 17")),
        passo("A parte deitada", "Parte deitada = v − parte em pé = (−3/17, 3/17, −4/17). É como ratear um lançamento: o que não vai para o prego fica na folha.",
              fig([fol10, it_v, it_v2, it_v1, trac(add(O10, v1_), add(O10, v10))], ang57, sem_eixos=True, moldura=mold57),
              ("(−3/17, 3/17, −4/17)", "parte deitada, igual ao gabarito")),
        passo("A prova", "v₁ · n = −6/17 − 6/17 + 12/17 = 0: a parte deitada faz 90° com o prego. E as duas partes somadas voltam a [[v]].",
              fig([fol10, it_v, it_v2, it_v1, trac(add(O10, v1_), add(O10, v10))], ang57, sem_eixos=True, moldura=mold57), ("v₁ · n = 0", "a parte deitada está mesmo na folha")),
    ]))

# --- 5.8 Distancia de ponto a plano (Lista 8, Q1i) ---
P = (1, 2, 3)
nn = (-1, -1, -1)
dd = 7
resto = dot(nn, P) + dd
checa("5.8 resto = 1", resto == 1)
H = sub(P, esc(F(resto, dot(nn, nn)), nn))
checa("5.8 pe no plano", dot(nn, H) + dd == 0)
checa("5.8 distancia", abs(norma(sub(P, H)) - math.sqrt(3) / 3) < 1e-12)
Q = add(add(H, esc(F(4, 5), e1)), esc(F(3, 10), e2))
checa("5.8 Q no plano", dot(nn, Q) + dd == 0)
fol3 = folha(H, e1, e2, 0.9, 0.4)
mold3 = [P, add(H, esc(0.9, e1)), add(H, esc(-0.9, e1)), add(H, esc(0.4, e2)), add(H, esc(-0.4, e2))]
it_P, it_H, it_torto, it_reto = ponto(P, "P"), ponto(H, ""), trac(P, Q), trac(P, H, 2)
S5.append(ideia(
    "dist-ponto-plano", "Distância de ponto a plano", "O caminho mais curto chega fazendo 90°, na direção do prego.", "Lista 8, Q1i",
    ["ga-s5-l8q1i", "ga-s5-l8q5", "ga-s5-l8q6", "ga-s5-l8q1c"],
    [
        passo("O ponto e a folha", "P = (1, 2, 3) e o plano −x − y − z + 7 = 0. A pergunta: qual a menor distância de P até a folha?",
              fig([fol3, it_P], ANG_DIST, sem_eixos=True, moldura=mold3)),
        passo("O caminho mais curto", "Da cadeira até a parede, o menor caminho vai reto, de frente. Ele chega à folha fazendo 90°, na direção do prego (tracejado coral). Qualquer caminho torto, como o cinza, é mais longo.",
              fig([fol3, it_P, it_torto, it_reto, it_H], ANG_DIST, sem_eixos=True, moldura=mold3)),
        passo("O resto", "Ponha P na equação: −1 − 2 − 3 + 7 = 1. Se P estivesse na folha, daria 0. O que sobra é o resto.",
              fig([fol3, it_P, it_reto, it_H], ANG_DIST, sem_eixos=True, moldura=mold3), ("resto = 1", "P posto na equação do plano")),
        passo("Divida pelo prego", "O prego é [[n]] = (−1, −1, −1), de tamanho √3. Distância = |resto| / ‖[[n]]‖ = 1/√3 = √3/3.",
              fig([fol3, it_P, it_reto, it_H], ANG_DIST, sem_eixos=True, moldura=mold3), ("≈ 0,58", "distância de P até o plano, igual ao gabarito (√3/3)")),
    ]))

# --- 5.9 Distancia de ponto a reta (Lista 8, Q1h) ---
Ah, vh, Ph = (3, 1, -2), (2, 4, 6), (1, 2, 3)
APh = sub(Ph, Ah)
crh = cross(APh, vh)
checa("5.9 AP", APh == (-2, 1, 5))
checa("5.9 AP x v", crh == (-14, 22, -10))
checa("5.9 quadrados", (dot(crh, crh), dot(vh, vh)) == (780, 56))
kh = F(dot(APh, vh), dot(vh, vh))
Hh = add(Ah, esc(kh, vh))
checa("5.9 pe perpendicular", dot(sub(Ph, Hh), vh) == 0)
dist_h = norma(crh) / norma(vh)
checa("5.9 distancia", abs(dist_h - math.sqrt(195 / 14)) < 1e-12 and abs(norma(sub(Ph, Hh)) - dist_h) < 1e-12)
checa("5.9 ~3,73", round(dist_h, 2) == 3.73)
paral = poli([Ah, add(Ah, vh), add(add(Ah, vh), APh), Ph], 3)
ang59 = angulo_folha(crh, 30)
base59 = [reta(Ah, vh, -0.6, 1.6, 1), ponto(Ah, "A"), ponto(Ph, "P")]
S5.append(ideia(
    "dist-ponto-reta", "Distância de ponto a reta", "Área do paralelogramo dividida pela base dá a altura.", "Lista 8, Q1h",
    ["ga-s5-l8q1h", "ga-s5-l8q4"],
    [
        passo("O ponto e a reta", "P = (1, 2, 3) e s: (x − 3)/2 = (y − 1)/4 = (z + 2)/6. Lendo a simétrica: A = (3, 1, −2) e [[v]] = (2, 4, 6).",
              fig(base59, ang59, sem_eixos=True)),
        passo("O paralelogramo", "Monte um paralelogramo com [[v]] e [[AP]] = P − A = (−2, 1, 5). A área é ‖AP × v‖ = ‖(−14, 22, −10)‖ = √780.",
              fig(base59 + [paral, vetor(Ah, add(Ah, vh), "v", 2), vetor(Ah, Ph, "AP", 4)], ang59, sem_eixos=True), ("área = √780", "‖AP × v‖")),
        passo("Base × altura", "Área = base × altura. A base é ‖v‖ = √56. A altura, tracejada, é a distância de P até a reta: √780 / √56 = √(195/14).",
              fig(base59 + [paral, vetor(Ah, add(Ah, vh), "v", 2), vetor(Ah, Ph, "AP", 4), trac(Ph, Hh, 2), ponto(Hh, "")], ang59, sem_eixos=True),
              ("≈ 3,73", "distância de P até a reta, igual ao gabarito")),
    ]))

# --- 5.10 Distancia entre reversas (Lista 8, Q1a) ---
AB10 = sub(p2, p1)
uxv = cross(u, v)
checa("5.10 AB", AB10 == (0, -1, -2))
checa("5.10 u x v", uxv == (-1, 4, -3))
checa("5.10 misto", dot(AB10, uxv) == 2)
checa("5.10 distancia", abs(abs(dot(AB10, uxv)) / norma(uxv) - math.sqrt(26) / 13) < 1e-12)
checa("5.10 ~0,39", round(math.sqrt(26) / 13, 2) == 0.39)
A10, B10 = p1, p2
base_cx = poli([A10, add(A10, u), add(add(A10, u), v), add(A10, v)], 3)
topo_cx = poli([B10, add(B10, u), add(add(B10, u), v), add(B10, v)], 3, aberto=True)
arestas = [seg(add(A10, c), add(B10, c)) for c in ((0, 0, 0), u, add(u, v), v)]
caixa = [base_cx, topo_cx] + arestas + [vetor(A10, add(A10, u), "u", 1), vetor(A10, add(A10, v), "v", 2), vetor(A10, B10, "AB", 4)]
ang510 = angulo_folha(uxv, 75)
S5.append(ideia(
    "dist-reversas", "Distância entre retas reversas", "Volume da caixa dividido pela área da base dá a folga do viaduto.", "Lista 8, Q1a",
    ["ga-s5-l8q1a", "ga-s5-l6q6a"],
    [
        passo("O viaduto", "r: X = (1, 2, 3) + λ(1, 1, 1) e s: X = (1, 1, 1) + t(1, −2, −3) são reversas (Lista 6, Q6a). O tracejado é a menor folga entre elas.",
              f_rev),
        passo("A caixa", "Monte uma caixa com [[u]], [[v]] e [[AB]] = (0, −1, −2), com A numa reta e B na outra. O volume é o módulo do produto misto: AB · (u × v) = 0 − 4 + 6 = 2. A caixa sai fina porque a folga é pequena.",
              fig(caixa, ang510, sem_eixos=True), ("volume = 2", "módulo do produto misto (Lista 3)")),
        passo("Volume ÷ área da base", "A base é o paralelogramo de [[u]] e [[v]], de área ‖u × v‖ = ‖(−1, 4, −3)‖ = √26. A altura da caixa é a folga: 2/√26 = √26/13.",
              fig(caixa, ang510, sem_eixos=True), ("≈ 0,39", "distância entre as retas, igual ao gabarito (√26/13)")),
    ]))

# --- 5.11 Lugar geometrico (Lista 8, Q8) ---
A8, B8 = (-1, 1, 4), (2, 3, 1)
n8l = sub(B8, A8)
M8 = tuple(F(a + b, 2) for a, b in zip(A8, B8))
d8 = -dot(n8l, M8)
checa("5.11 normal", n8l == (3, 2, -3))
checa("5.11 meio", M8 == (F(1, 2), 2, F(5, 2)))
checa("5.11 d", d8 == 2)
ea8 = (2, -3, 0)
checa("5.11 ea deitada", dot(ea8, n8l) == 0)
eb8 = cross(n8l, ea8)
X8 = add(M8, esc(F(1, 2), ea8))
checa("5.11 X8", X8 == (F(3, 2), F(1, 2), F(5, 2)))
checa("5.11 X8 no plano", dot(n8l, X8) + d8 == 0)
checa("5.11 equidistante", dot(sub(X8, A8), sub(X8, A8)) == dot(sub(X8, B8), sub(X8, B8)) == F(35, 4))
checa("5.11 ~2,96", round(math.sqrt(35) / 2, 2) == 2.96)
fol11 = folha(M8, unit(ea8), unit(eb8), 2.4, 2.0)
ang511 = angulo_folha(n8l, 70)
pA, pB, pM = ponto(A8, "A"), ponto(B8, "B"), ponto(M8, "M")
mold511 = [add(M8, esc(2.4, unit(ea8))), add(M8, esc(-2.4, unit(ea8)))]
S5.append(ideia(
    "lugar-geometrico", "Lugar geométrico", "Todos os pontos que passam no filtro: equidistantes de A e B formam uma parede.", "Lista 8, Q8",
    ["ga-s5-l8q8", "ga-s5-l8q7"],
    [
        passo("A regra", "Lugar geométrico é o conjunto de todos os pontos que obedecem a uma regra, como um filtro de planilha. Lista 8, Q8: mesma distância de A = (−1, 1, 4) e de B = (2, 3, 1).",
              fig([pA, pB, trac(A8, B8)], ang511, sem_eixos=True, moldura=mold511)),
        passo("O meio", "O ponto do meio, M = (1/2, 2, 5/2), passa no filtro. Numa folha, em 2D, os pontos que passam formariam uma reta: a mediatriz.",
              fig([pA, pB, trac(A8, B8), pM], ang511, sem_eixos=True, moldura=mold511)),
        passo("A parede", "No espaço, os pontos que passam formam um plano: uma parede que corta AB no meio, a 90°. O prego é a própria seta AB = (3, 2, −3). Passando por M: 3/2 + 4 − 15/2 + d = 0, então d = 2.",
              fig([fol11, pA, pB, vetor(A8, B8, "AB", 2), pM], ang511, sem_eixos=True), ("3x + 2y − 3z + 2 = 0", "é um plano, como diz o gabarito")),
        passo("A prova", "O ponto (3/2, 1/2, 5/2) está na parede: 9/2 + 1 − 15/2 + 2 = 0. E fica a √35/2 de A e também de B.",
              fig([fol11, pA, pB, pM, ponto(X8, "X", 1), trac(X8, A8, 1), trac(X8, B8, 1)], ang511, sem_eixos=True),
              ("√35/2 ≈ 2,96", "distância de X até A e até B")),
    ]))


# --- 5.12 Tres planos (Lista 8, Q10 e Q11) ---
def resolve3(ns, cs):
    """Cramer em fracoes: ns = 3 normais, cs = 3 constantes (n . p = c)."""
    det = dot(ns[0], cross(ns[1], ns[2]))
    sol = []
    for i in range(3):
        m = [list(r) for r in ns]
        for k in range(3):
            m[k][i] = cs[k]
        sol.append(F(dot(m[0], cross(m[1], m[2])), det))
    return tuple(sol)


def folha_em(nv, centro, a, b, cor):
    ea = cross(nv, (0, 0, 1))
    if norma(ea) < 1e-9:
        ea = cross(nv, (1, 0, 0))
    ea = unit(ea)
    eb = unit(cross(nv, ea))
    return folha(centro, ea, eb, a, b, cor)


nc = (1, 1, -4)
const_c = [F(-2), F(4, 3), F(-1)]
checa("5.12 c normais multiplas", cross(nc, (-3, -3, 12)) == (0, 0, 0))
checa("5.12 c d diferentes", len(set(const_c)) == 3)
ea_c = unit((1, -1, 0))
eb_c = unit(cross(nc, ea_c))
fc = fig([folha(esc(c / dot(nc, nc), nc), ea_c, eb_c, 1.6, 1.0, cor) for c, cor in zip(const_c, (1, 2, 3))], angulo_folha(nc, 80), sem_eixos=True)
na = [(-1, 3, -4), (-4, -1, 8), (1, -1, 4)]
ca = [-2, -4, -1]
checa("5.12 a misto = 48", dot(na[0], cross(na[1], na[2])) == 48)
Pa = resolve3(na, ca)
checa("5.12 a ponto nos tres", all(dot(nk, Pa) == ck for nk, ck in zip(na, ca)))
fa3 = fig([folha_em(nk, Pa, 1.2, 1.2, cor) for nk, cor in zip(na, (1, 2, 3))] + [ponto(Pa, "")], ANG_PADRAO, sem_eixos=True)
ni = [(2, 2, -4), (-1, -1, 1), (-2, -2, -8)]
ci = [-4, 6, -4]
checa("5.12 i misto = 0", dot(ni[0], cross(ni[1], ni[2])) == 0)
eixo_i = (1, -1, 0)
checa("5.12 i direcao comum", all(dot(nk, eixo_i) == 0 for nk in ni))


def ponto_par(i, j):
    return resolve3([ni[i], ni[j], eixo_i], [ci[i], ci[j], 0])


P12, P13, P23 = ponto_par(0, 1), ponto_par(0, 2), ponto_par(1, 2)
checa("5.12 i P12", P12 == (-5, -5, -4))
checa("5.12 i P13", P13 == (F(-1, 3), F(-1, 3), F(2, 3)))
checa("5.12 i P23", P23 == (F(-11, 5), F(-11, 5), F(8, 5)))
checa("5.12 i sem ponto comum", dot(ni[2], P12) != ci[2])
ue = unit(eixo_i)


def faixa(pa, pb, cor):
    m = esc(F(1, 2), add(pa, pb))
    meia = esc(0.65, sub(pb, pa))
    return folha(m, ue, unit(meia), 3.0, norma(meia), cor)


tenda = [faixa(P12, P13, 1), faixa(P12, P23, 2), faixa(P13, P23, 3)] + [reta(pp, ue, -3.0, 3.0, 4, 2) for pp in (P12, P13, P23)]
# olhar quase pela direcao comum (1, -1, 0), uns 30 graus de lado: aparece o triangulo da barraca
ang_tenda = angulo_para((0.6, -0.6, 0.53))
fi = fig(tenda, ang_tenda, sem_eixos=True)


def misto_m(m):
    return dot((2, 3, -5), cross((4, -2, 1), (m, -8, 11)))


checa("5.12 Q11 m=0", misto_m(0) == 0 and misto_m(1) == -7)
checa("5.12 Q11 combinacao", add(esc(-2, (2, 3, -5)), (4, -2, 1)) == (0, -8, 11))
checa("5.12 Q11 n", -2 * 7 + (-5) == -19)
S5.append(ideia(
    "tres-planos", "Três planos", "Primeiro veja quais pregos são múltiplos; depois, o produto misto.", "Lista 8, Q10 e Q11",
    ["ga-s5-l8q10a", "ga-s5-l8q10c", "ga-s5-l8q10i", "ga-s5-l8q11"],
    [
        passo("Pregos múltiplos: paralelos", "Q10c: os três pregos são múltiplos de (1, 1, −4). Com o mesmo prego, os números soltos ficam 2, −4/3 e 1, todos diferentes: três folhas paralelas, como andares de um prédio.",
              fc, ("3 paralelos distintos", "igual ao gabarito")),
        passo("Produto misto ≠ 0: um ponto", "Q10a: nenhum par de pregos é múltiplo. O produto misto dos três pregos dá 48, diferente de 0: os três se encontram num ponto só, como o canto de uma sala.",
              fa3, ("1 ponto em comum", "produto misto = 48")),
        passo("Produto misto = 0: a barraca", "Q10i: os três pregos estão deitados numa mesma folha, e o produto misto dá 0. Teste um ponto da reta de dois deles no terceiro: não serve. Os planos se cortam dois a dois em três retas paralelas, como as faces de uma barraca.",
              fi, ("3 retas paralelas", "igual ao gabarito")),
        passo("Lista 8, Q11", "Q11 pede a barraca. Produto misto = −7m, então m = 0. Com m = 0, o prego 3 = −2 × prego 1 + prego 2. Se o número solto seguisse a mesma conta, n = −2·7 + (−5) = −19, os três passariam por uma reta só.",
              fi, ("m = 0 e n ≠ −19", "igual ao gabarito")),
    ]))

# ---------------- gravar ----------------
for lista in (S4, S5):
    for it in lista:
        for p in it["passos"]:
            for k in ("titulo", "texto"):
                if "⃗" in p[k]:
                    erros.append("seta combinante em " + it["id"])
if erros:
    print("FALHAS:", erros)
    sys.exit(1)

with open(ARQ, encoding="utf-8") as fh:
    dados = json.load(fh)
por_semana = {s["semana"]: s for s in dados["semanas"]}
por_semana[4]["ideias"] = S4
por_semana[5]["ideias"] = S5
with open(ARQ, "w", encoding="utf-8") as fh:
    json.dump(dados, fh, ensure_ascii=False, indent=2)
npassos = sum(len(i["passos"]) for i in S4 + S5)
print("ideias: semana 4 =", len(S4), "| semana 5 =", len(S5), "| passos =", npassos, "| contas OK")
