# Revisao adversarial (rodada 2) do lote lp_s6: Logica, semana 6.
# Resolve cada questao do zero em Python, sem ler o campo "resposta",
# refaz a conta de cada distrator e confere numeros citados nos jeitos.
# Uso: python -I rev_lp_s6_r2_contas.py
import json, os, re, sys
from fractions import Fraction
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
GER = os.path.dirname(AQUI)
DADOS = os.path.join(GER, "dados")

falhas = []
def ok(cond, msg):
    if not cond:
        falhas.append(msg)
        print("FALHA", msg)
    return cond

def carrega(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

p1 = carrega(os.path.join(DADOS, "lp_s6_p1.json"))
p2 = carrega(os.path.join(DADOS, "lp_s6_p2.json"))
ex = carrega(os.path.join(GER, "exemplos.json"))
Q = {}
ordem = []
for d in (p1, p2):
    ok(d["disciplina"] == "lp", "disciplina")
    for q in d["questoes"]:
        Q[q["id"]] = q
        ordem.append(q["id"])

def norm(s):
    # mesma ideia do normalizarSaida do site: separa numeros e junta espacos
    linhas = []
    for l in str(s).replace("\r", "").split("\n"):
        l = re.sub(r"(-?\d+(?:\.\d+)?)", r" \1 ", l)
        linhas.append(re.sub(r"\s+", " ", l).strip())
    return "\n".join(linhas).strip("\n")

def certa(q):
    c = [a["t"] for a in q["alternativas"] if a.get("certa") is True]
    ok(len(c) == 1, q["id"] + " certa unica")
    return c[0]

def erradas(q):
    return {a["t"]: a.get("erro", "") for a in q["alternativas"] if a.get("certa") is not True}

def vdiv(a, b):
    # div do VisuAlg: trunca para zero
    r = abs(a) // abs(b)
    return r if (a >= 0) == (b > 0) else -r

def para(a, b, p=1):
    i = a
    while (p > 0 and i <= b) or (p < 0 and i >= b):
        yield i
        i += p

def num(x):
    # escreva de numero: inteiro sai sem casas
    if isinstance(x, Fraction):
        if x.denominator == 1:
            return str(x.numerator)
        return str(float(x))
    return str(x)

# ---------------- p01: copia exata do exemplos.json ----------------
ex01 = [q for q in ex["questoes"] if q["id"] == "lp-s6-p01"][0]
ok(Q["lp-s6-p01"] == ex01, "p01 diferente do exemplos.json")

def q01(filtro=lambda i: i % 2 == 0, soma=lambda s, i: s + i):
    s = 0
    for i in para(1, 6):
        if filtro(i):
            s = soma(s, i)
    return num(s)
q = Q["lp-s6-p01"]
ok(norm(q01()) == norm(q["saida"]) == norm(certa(q)), "p01 saida")
E = erradas(q)
ok(q01(filtro=lambda i: True) == "21" and "21" in E, "p01 21")
ok(q01(filtro=lambda i: i % 2 == 1) == "9" and "9" in E, "p01 9")
ok(q01(soma=lambda s, i: s + 1) == "3" and "3" in E, "p01 3")
ok(q01(soma=lambda s, i: i) == "6" and "6" in E, "p01 6")

# ---------------- p02 ----------------
def q02(a=3, b=15, p=4):
    c = 0
    for i in para(a, b, p):
        c += 1
    return str(c)
q = Q["lp-s6-p02"]
ok(q02() == norm(q["saida"]) == certa(q), "p02 saida")
E = erradas(q)
ok(q02(p=1) == "13" == str(15 - 3 + 1) and "13" in E, "p02 13")
ok(str(vdiv(15 - 3, 4)) == "3" and "3" in E, "p02 3")
ok(str(len(list(para(3, 15, 4))) + 1) == "5" and 3 + 4 * 4 == 19 and "5" in E, "p02 5 (inclui 19)")
ok(str(15 - 3) == "12" and "12" in E, "p02 12")
ok(list(para(3, 15, 4)) == [3, 7, 11, 15], "p02 valores do i")
ok(vdiv(15 - 3, 4) + 1 == 4, "p02 formula")

# ---------------- p03 ----------------
def q03(a=10, b=2, p=-2):
    return " ".join(str(i) for i in para(a, b, p))
q = Q["lp-s6-p03"]
ok(norm(q03()) == norm(q["saida"]) == norm(certa(q)), "p03 saida")
E = erradas(q)
ok(q03(2, 10, 2) in E, "p03 subindo")
ok(q03(10, 2, 2) == "", "p03 passo positivo nao roda (alternativa Nada)")
ok(q03(10, 4, -2) in E, "p03 para no 4")
ok(q03(8, 2, -2) in E, "p03 comeca no 8")
ok(vdiv(10 - 2, 2) + 1 == 5 and 2 - 2 == 0, "p03 formula e proximo valor 0")

# ---------------- p04 ----------------
def q04(cont=lambda x: x < 10, primeira_sem_teste=False):
    x, c = 20, 0
    if primeira_sem_teste:
        x -= 3; c += 1
    while cont(x):
        x -= 3; c += 1
    return "c = %d, x = %d" % (c, x)
q = Q["lp-s6-p04"]
ok(norm(q04()) == norm(q["saida"]) == norm(certa(q)), "p04 saida")
E = erradas(q)
ok(q04(cont=lambda x: not (x < 10)) in E, "p04 condicao de parada -> c = 4, x = 8")
ok(q04(primeira_sem_teste=True) in E, "p04 roda uma vez -> c = 1, x = 17")
ok("c = 0, x = 10" in E, "p04 c=0 x=10 existe")

# ---------------- p05 ----------------
def q05(n=50, limite=40, voltas_extra=0):
    c = 0
    while True:
        n += 10; c += 1
        if n > limite:
            break
    for _ in range(voltas_extra):
        n += 10; c += 1
    return "%d %d" % (c, n)
q = Q["lp-s6-p05"]
ok(q["entradas"] == ["50"], "p05 entradas")
ok(norm(q05()) == norm(q["saida"]) == norm(certa(q)), "p05 saida")
E = erradas(q)
ok("0 50" in E, "p05 0 50 (testar antes: 50 > 40 ja verdadeiro)")
ok(q05(voltas_extra=1) == "2 70" and "2 70" in E, "p05 2 70")

# ---------------- p06 ----------------
ent06 = [120, 80, 100, 250, 40]
def q06(filtro=lambda v: v > 100, guarda=False):
    c = s = 0
    for v in ent06:
        if filtro(v):
            c += 1
            s = v if guarda else s + v
    return "%d %d" % (c, s)
q = Q["lp-s6-p06"]
ok([int(x) for x in q["entradas"]] == ent06, "p06 entradas")
ok(norm(q06()) == norm(q["saida"]) == norm(certa(q)), "p06 saida")
E = erradas(q)
ok(q06(filtro=lambda v: v >= 100) == "3 470" and "3 470" in E, "p06 3 470")
ok(q06(filtro=lambda v: True) == "5 590" and "5 590" in E, "p06 5 590")
ok(q06(guarda=True) == "2 250" and "2 250" in E, "p06 2 250")
ok(q06(filtro=lambda v: v <= 100) == "3 220" and "3 220" in E, "p06 3 220")
ok(sum(ent06) - (80 + 100 + 40) == 370, "p06 confira 590 - 220")

# ---------------- p07 ----------------
def q07(com_interrompa=True, conta_depois=False):
    c = 0; achou = 0
    for i in para(20, 40):
        if not conta_depois:
            c += 1
        if i % 7 == 0:
            achou = i
            if com_interrompa:
                if conta_depois:
                    pass
                break
        if conta_depois:
            c += 1
    return "%d %d" % (achou, c)
q = Q["lp-s6-p07"]
ok(norm(q07()) == norm(q["saida"]) == norm(certa(q)), "p07 saida")
E = erradas(q)
ok(q07(com_interrompa=False) == "35 21" and "35 21" in E, "p07 35 21")
ok(q07(conta_depois=True) == "21 1" and "21 1" in E, "p07 21 1")
ok(40 - 20 + 1 == 21 and "21 21" in E, "p07 21 21")
ok([i for i in range(20, 41) if i % 7 == 0] == [21, 28, 35], "p07 multiplos")
ok(20 % 7 == 6, "p07 20 mod 7")

# ---------------- p08 ----------------
def q08(ini=2, fim=4, soma_indice=False, mostra_indice=False):
    v = {i: i * 3 for i in para(1, 5)}
    s = 0
    for i in para(ini, fim):
        s += i if soma_indice else v[i]
    return "%d %d" % (5 if mostra_indice else v[5], s)
q = Q["lp-s6-p08"]
ok(norm(q08()) == norm(q["saida"]) == norm(certa(q)), "p08 saida")
E = erradas(q)
ok(q08(1, 5) == "15 45" and "15 45" in E, "p08 15 45")
ok(q08(soma_indice=True) == "15 9" and "15 9" in E, "p08 15 9")
ok(q08(2, 3) == "15 15" and "15 15" in E, "p08 15 15")
ok(q08(mostra_indice=True) == "5 27" and "5 27" in E, "p08 5 27")
ok(3 * (2 + 3 + 4) == 27 and 3 * 6 > 9, "p08 confira e atalho")

# ---------------- p09 ----------------
def q09(ent, ini_maior=0, ini_menor=0, sinal_menor="<", primeiro=False):
    ent = list(ent)
    if primeiro:
        maior = menor = ent[0]
        resto = ent[1:]
    else:
        maior, menor = ini_maior, ini_menor
        resto = ent
    for x in resto:
        if x > maior:
            maior = x
        if (x < menor) if sinal_menor == "<" else (x > menor):
            menor = x
    return "%d %d" % (maior, menor)
q = Q["lp-s6-p09"]
ent09 = [int(x) for x in q["entradas"]]
ok(ent09 == [15, 8, 23, 11], "p09 entradas")
ok(norm(q09(ent09)) == norm(q["saida"]) == "23 0", "p09 saida")
ok(certa(q).startswith("Escreve 23 0; começar maior e menor com o primeiro"), "p09 certa")
ok(q09(ent09, primeiro=True) == "23 8", "p09 correcao funciona aqui")
ok(q09(ent09, sinal_menor=">") == "23 23", "p09 trocar sinal: menor segue os grandes")
ok(q09(ent09, ini_menor=100) == "23 8", "p09 menor 100 funciona aqui")
ok(q09([150, 200, 300, 120], ini_menor=100) == "300 100", "p09 menor 100 falha acima de 100")
ok(q09([150, 200, 300, 120], primeiro=True) == "300 120", "p09 confira 300 120")
ok(q09([-5, -2, -9], primeiro=True) == "-2 -9", "p09 correcao com negativos")
ok(q09([-5, -2, -9]) == "0 -9", "p09 maior com 0 falha com negativos (por isso a correcao vale para os dois)")

# ---------------- p10: cinco trechos ----------------
def roda_trecho(x, cond, corpo, repita=False, limite=10000):
    vals = [x]
    if repita:
        for _ in range(limite):
            x = corpo(x); vals.append(x)
            if cond(x):
                return True, vals
        return False, vals[:12]
    for _ in range(limite):
        if not cond(x):
            return True, vals
        x = corpo(x); vals.append(x)
    return False, vals[:12]
t1 = roda_trecho(1, lambda x: x < 10, lambda x: x + 2)
t2 = roda_trecho(20, lambda x: x > 0, lambda x: vdiv(x, 2))
t3 = roda_trecho(1, lambda x: x != 10, lambda x: x + 2)
t4 = roda_trecho(10, lambda x: x < 0, lambda x: x - 3, repita=True)
t5 = roda_trecho(1, lambda x: x <= 100, lambda x: x * 2)
ok(t1 == (True, [1, 3, 5, 7, 9, 11]), "p10 t1 %s" % (t1,))
ok(t2 == (True, [20, 10, 5, 2, 1, 0]), "p10 t2 %s" % (t2,))
ok(t3[0] is False and all(v % 2 == 1 for v in t3[1]), "p10 t3")
ok(t4 == (True, [10, 7, 4, 1, -2]), "p10 t4 %s" % (t4,))
ok(t5 == (True, [1, 2, 4, 8, 16, 32, 64, 128]), "p10 t5 %s" % (t5,))
q = Q["lp-s6-p10"]
ok(certa(q) == "Trecho 3", "p10 certa")
tab = q["tabela"]["linhas"]
ok(tab[0][1:] == ["`x <- 1`", "`enquanto x < 10 faca`", "`x <- x + 2`"], "p10 tabela 1")
ok(tab[1][1:] == ["`x <- 20`", "`enquanto x > 0 faca`", "`x <- x div 2`"], "p10 tabela 2")
ok(tab[2][1:] == ["`x <- 1`", "`enquanto x <> 10 faca`", "`x <- x + 2`"], "p10 tabela 3")
ok(tab[3][1:] == ["`x <- 10`", "`repita ... ate x < 0`", "`x <- x - 3`"], "p10 tabela 4")
ok(tab[4][1:] == ["`x <- 1`", "`enquanto x <= 100 faca`", "`x <- x * 2`"], "p10 tabela 5")
# trabalho: diferenca 3, ajuste de 2
d = [3]
for _ in range(3):
    d.append(d[-1] - 2)
ok(d == [3, 1, -1, -3], "p10 trabalho 3 1 -1 -3")

# ---------------- p11 ----------------
def q11(voltas=4, reset=False, ordem_trocada=False):
    a, b = 1, 1
    linhas = []
    for i in para(1, voltas):
        if reset:
            a, b = 1, 1
        t = a + b
        if ordem_trocada:
            b = t; a = b
        else:
            a = b; b = t
        linhas.append((i, t, a, b))
    return "%d %d" % (a, b), linhas
q = Q["lp-s6-p11"]
s11, lin11 = q11()
ok(norm(s11) == norm(q["saida"]) == norm(certa(q)), "p11 saida")
ok(lin11 == [(1, 2, 1, 2), (2, 3, 2, 3), (3, 5, 3, 5), (4, 8, 5, 8)], "p11 linhas do visual")
E = erradas(q)
ok(q11(5)[0] == "8 13" and "8 13" in E, "p11 8 13")
ok(q11(reset=True)[0] == "1 2" and "1 2" in E, "p11 1 2")
ok(q11(3)[0] == "3 5" and "3 5" in E, "p11 3 5")
s, l = q11(ordem_trocada=True)
ok(s == "16 16" and "16 16" in E and [x[2:] for x in l] == [(2, 2), (4, 4), (8, 8), (16, 16)], "p11 16 16")

# ---------------- p12 ----------------
def q12(ent, modo="certo"):
    ent = list(ent)
    x = s = c = 0
    if modo == "testa_antes":
        if x == 0:
            return "%d %d" % (s, c)
    while True:
        if not ent:
            return "PEDE MAIS"
        x = ent.pop(0); s += x; c += 1
        if modo == "enquanto_igual":
            if not (x == 0):
                break
        elif x == 0:
            break
    if modo == "volta_a_mais":
        return "PEDE MAIS" if not ent else "?"
    return "%d %d" % (s, c)
q = Q["lp-s6-p12"]
ent12 = [int(x) for x in q["entradas"]]
ok(ent12 == [7, 5, 9, 0], "p12 entradas")
ok(norm(q12(ent12)) == norm(q["saida"]) == norm(certa(q)), "p12 saida")
E = erradas(q)
ok(q12(ent12, "enquanto_igual") == "7 1" and "7 1" in E, "p12 7 1")
ok(q12(ent12, "testa_antes") == "0 0" and "0 0" in E, "p12 0 0")
ok(q12(ent12, "volta_a_mais") == "PEDE MAIS", "p12 quinta entrada seria pedida")
ok("21 3" in E and 7 + 5 + 9 == 21, "p12 21 3")

# ---------------- nenhuma errada igual a certa ----------------
for qid in ordem:
    q = Q[qid]
    c = norm(certa(q))
    for t in erradas(q):
        ok(norm(t) != c, qid + " errada igual a certa: " + t)

# ---------------- formulas da teoria ----------------
import itertools
for a, b, p in itertools.product(range(-6, 7), range(-6, 7), [1, 2, 3, 4, -1, -2, -3]):
    real = len(list(para(a, b, p)))
    if p > 0 and a <= b:
        ok(vdiv(b - a, p) + 1 == real, "formula voltas %d %d %d" % (a, b, p))
    if p > 0 and a > b:
        ok(real == 0, "zero voltas %d %d %d" % (a, b, p))
    if p < 0 and a >= b:
        ok(vdiv(a - b, abs(p)) + 1 == real, "formula voltas negativas %d %d %d" % (a, b, p))
        # o bloco do para diz (fim - inicio) div passo + 1 tambem
        ok(vdiv(b - a, p) + 1 == real, "formula do bloco com passo negativo %d %d %d" % (a, b, p))
    if p < 0 and a < b:
        ok(real == 0, "zero voltas negativas %d %d %d" % (a, b, p))

# ---------------- cobertura ----------------
ok(ordem == ["lp-s6-p%02d" % k for k in range(1, 13)], "ids %s" % ordem)
niveis = Counter(Q[i]["nivel"] for i in ordem)
ok(niveis == Counter({1: 4, 2: 4, 3: 4}), "niveis %s" % niveis)
ok(all(Q[i]["origem"] == "Prévia · ementa" and Q[i]["semana"] == 6 for i in ordem), "origem/semana")
com_cod = [i for i in ordem if Q[i].get("codigo")]
com_ent = [i for i in ordem if Q[i].get("entradas")]
ok(len(com_cod) >= 9, "codigo em %d" % len(com_cod))
ok(len(com_ent) >= 3, "entradas em %d" % len(com_ent))
pos = Counter("ABCDE"[[a.get("certa") is True for a in Q[i]["alternativas"]].index(True)] for i in ordem)
print("posicoes", dict(sorted(pos.items())), "codigo", len(com_cod), "entradas", len(com_ent), "niveis", dict(niveis))
ok(max(pos.values()) / 12 <= 0.30, "posicao concentrada")
# leia x entradas
for i in com_cod:
    q = Q[i]
    nleia = len(re.findall(r"\bleia\(", q["codigo"]))
    print(i, "leia no codigo:", nleia, "entradas:", len(q.get("entradas", [])))

sem = p1["semanas"]
ok(len(sem) == 1 and sem[0]["semana"] == 6 and sem[0]["previa"] is True and
   sem[0]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "teoria")
ok(p2["semanas"] == [], "p2 sem teoria")

# ---------------- forma ----------------
def palavras(s):
    return len(re.findall(r"\S+", s))
def textos(obj, caminho=""):
    if isinstance(obj, str):
        yield caminho, obj
    elif isinstance(obj, list):
        for k, v in enumerate(obj):
            yield from textos(v, "%s[%d]" % (caminho, k))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from textos(v, caminho + "." + k)
travessoes = 0
for nome, d in (("p1", p1), ("p2", p2)):
    for cam, s in textos(d, nome):
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", s):
            ok(False, "byte de controle em " + cam)
        travessoes += s.count("—")
        if "!" in re.sub(r"`[^`]*`", "", s) and ".codigo" not in cam:
            ok(False, "exclamacao em " + cam)
ok(travessoes == 1, "travessoes %d" % travessoes)
for i in ordem:
    j = Q[i]["jeitos"]
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = palavras(j[k])
        if not 35 <= n <= 110:
            print("AVISO palavras", i, k, n)
    ok(3 <= len(j["receita"]) <= 7, i + " receita passos")
    ok(4 <= len(j["conversa"]) <= 8, i + " conversa falas")
for b in sem[0]["blocos"]:
    n = palavras(b["texto"])
    if not 40 <= n <= 120:
        print("AVISO bloco", b["titulo"], n)
for k, v in sem[0]["jeitos"].items():
    n = palavras(v)
    if not 50 <= n <= 120:
        print("AVISO jeito da semana", k, n)

print()
print("RESULTADO:", "OK" if not falhas else "%d falha(s)" % len(falhas))
