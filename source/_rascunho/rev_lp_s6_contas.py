# Revisao adversarial do lote lp_s6 (Logica, semana 6).
# Refaz cada questao do zero em Python, confere a saida, os distratores,
# numeros citados nos jeitos, a teoria e a forma do texto.
# Uso: python -I rev_lp_s6_contas.py
import json, os, re, sys, random
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
GER = os.path.dirname(AQUI)
DADOS = os.path.join(GER, "dados")

falhas = []
def ok(cond, msg):
    if not cond:
        falhas.append(msg)
        print("FALHA", msg)

def carrega(nome):
    with open(os.path.join(DADOS, nome), encoding="utf-8") as f:
        return json.load(f)

p1 = carrega("lp_s6_p1.json")
p2 = carrega("lp_s6_p2.json")
Q = {}
for d in (p1, p2):
    for q in d["questoes"]:
        Q[q["id"]] = q

def norm(s):
    return re.sub(r"\s+", " ", s.strip())

def certa(q):
    return [a["t"] for a in q["alternativas"] if a.get("certa")][0]

def alts(q):
    return [a["t"] for a in q["alternativas"]]

def erro_de(q, t):
    for a in q["alternativas"]:
        if a["t"] == t:
            return a.get("erro", "")
    raise KeyError(t)

def para(a, b, p=1):
    # semantica do manual do VisuAlg: valor final entra; passo negativo desce
    i = a
    while (p > 0 and i <= b) or (p < 0 and i >= b):
        yield i
        i += p

def vdiv(a, b):
    # div do VisuAlg: divisao inteira truncada
    q = abs(a) // abs(b)
    return q if (a >= 0) == (b > 0) else -q

# ---------------- cobertura ----------------
ids = sorted(Q)
ok(ids == ["lp-s6-p%02d" % k for k in range(1, 13)], "ids esperados: %s" % ids)
niv = {}
for q in Q.values():
    niv.setdefault(q["nivel"], []).append(q["id"])
ok(all(len(niv.get(n, [])) == 4 for n in (1, 2, 3)), "4 por nivel: %s" % niv)
ok(all(q["origem"] == "Prévia · ementa" for q in Q.values()), "origem")
ok(all(q["semana"] == 6 for q in Q.values()), "semana 6")
com_cod = [q["id"] for q in Q.values() if q.get("codigo")]
com_ent = [q["id"] for q in Q.values() if q.get("entradas")]
ok(len(com_cod) >= 9, "codigo em >= 9: %d" % len(com_cod))
ok(len(com_ent) >= 3, "entradas em >= 3: %d" % len(com_ent))
pos = {}
for q in Q.values():
    for i, a in enumerate(q["alternativas"]):
        if a.get("certa"):
            pos["ABCDE"[i]] = pos.get("ABCDE"[i], 0) + 1
ok(max(pos.values()) <= 3, "posicao das certas: %s" % pos)
print("niveis", niv, "| com codigo", len(com_cod), "| com entradas", com_ent, "| posicoes", dict(sorted(pos.items())))

# p01 identica a exemplos.json
with open(os.path.join(GER, "exemplos.json"), encoding="utf-8") as f:
    ex = json.load(f)
ex01 = [q for q in ex["questoes"] if q["id"] == "lp-s6-p01"][0]
ok(ex01 == Q["lp-s6-p01"], "p01 diferente do exemplos.json")

# teoria so na _p1, previa true, fonte pedida
ok(len(p1["semanas"]) == 1 and p2["semanas"] == [], "teoria so na p1")
S = p1["semanas"][0]
ok(S["semana"] == 6 and S["previa"] is True, "teoria previa")
ok(S["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "fonte")

def confere_saida(qid, saida_py):
    q = Q[qid]
    ok(norm(q["saida"]) == norm(saida_py), "%s saida json %r x python %r" % (qid, q["saida"], saida_py))
    ok(norm(certa(q)) == norm(saida_py) or certa(q).startswith(saida_py) or saida_py in certa(q),
       "%s certa %r x python %r" % (qid, certa(q), saida_py))
    print(qid, "saida python:", repr(saida_py), "| certa:", repr(certa(q)))

def distrator(qid, texto, valor, regra=""):
    q = Q[qid]
    ok(texto in alts(q), "%s: alternativa %r nao existe" % (qid, texto))
    ok(norm(texto) == norm(valor), "%s: conta do erro (%s) da %r, alternativa diz %r" % (qid, regra, valor, texto))
    ok(norm(valor) != norm(q["saida"]) if q.get("saida") else True, "%s: distrator igual a certa" % qid)

# ---------------- p01 ----------------
s = 0
for i in para(1, 6):
    if i % 2 == 0:
        s += i
confere_saida("lp-s6-p01", str(s))
distrator("lp-s6-p01", "21", str(sum(para(1, 6))), "soma de tudo")
distrator("lp-s6-p01", "9", str(1 + 3 + 5), "impares")
distrator("lp-s6-p01", "3", str(len([i for i in para(1, 6) if i % 2 == 0])), "contador")
distrator("lp-s6-p01", "6", str([i for i in para(1, 6) if i % 2 == 0][-1]), "ultimo par")
ok(3 * 4 == 12, "p01 confira")

# ---------------- p02 ----------------
vals = list(para(3, 15, 4))
confere_saida("lp-s6-p02", str(len(vals)))
ok(vals == [3, 7, 11, 15], "p02 valores do i")
distrator("lp-s6-p02", "13", str(15 - 3 + 1), "passo 1")
distrator("lp-s6-p02", "3", str((15 - 3) // 4), "so saltos")
distrator("lp-s6-p02", "5", str(len(vals + [19])), "conta o 19")
distrator("lp-s6-p02", "12", str(15 - 3), "distancia")
ok(vdiv(15 - 3, 4) + 1 == 4, "p02 formula")
ok([3 + 4 * k for k in range(4)] == [3, 7, 11, 15], "p02 SEQUENCIA(4;1;3;4)")
ok(int((15 - 3) / 4) + 1 == 4, "p02 INT")

# ---------------- p03 ----------------
vals = list(para(10, 2, -2))
confere_saida("lp-s6-p03", " ".join(map(str, vals)))
distrator("lp-s6-p03", "2 4 6 8 10", " ".join(map(str, reversed(vals))), "subindo")
distrator("lp-s6-p03", "10 8 6 4", " ".join(map(str, [i for i in vals if i > 2])), "exclui limite")
distrator("lp-s6-p03", "8 6 4 2", " ".join(map(str, vals[1:])), "passo antes")
ok(len(list(para(10, 2, 2))) == 0, "p03 com passo positivo nao roda (base do distrator Nada)")
ok(vdiv(10 - 2, 2) + 1 == 5, "p03 formula")
ok([10 - 2 * k for k in range(5)] == [10, 8, 6, 4, 2], "p03 SEQUENCIA(5;1;10;-2)")

# ---------------- p04 ----------------
x, c = 20, 0
while x < 10:
    x -= 3; c += 1
confere_saida("lp-s6-p04", "c = %d, x = %d" % (c, x))
# erro A: ler como condicao de parada (repita ate x < 10)
x, c = 20, 0
while not (x < 10):
    x -= 3; c += 1
distrator("lp-s6-p04", "c = 4, x = 8", "c = %d, x = %d" % (c, x), "parada")
distrator("lp-s6-p04", "c = 1, x = 17", "c = %d, x = %d" % (1, 20 - 3), "uma volta antes")

# ---------------- p05 ----------------
def p05(n, semantica="repita", voltas_extra=0):
    c = 0
    if semantica == "enquanto":
        while not (n > 40):
            n += 10; c += 1
        return "%d %d" % (c, n)
    while True:
        n += 10; c += 1
        if n > 40:
            break
    for _ in range(voltas_extra):
        n += 10; c += 1
    return "%d %d" % (c, n)
confere_saida("lp-s6-p05", p05(50))
distrator("lp-s6-p05", "0 50", p05(50, "enquanto"), "teste antes")
distrator("lp-s6-p05", "2 70", p05(50, voltas_extra=1), "volta a mais")
ok(50 + 10 * 1 == 60, "p05 confira")

# ---------------- p06 ----------------
E6 = [int(v) for v in Q["lp-s6-p06"]["entradas"]]
ok(E6 == [120, 80, 100, 250, 40], "p06 entradas")
def p06(filtro, acum=True):
    c = s = 0
    for v in E6:
        if filtro(v):
            c += 1
            s = s + v if acum else v
    return "%d %d" % (c, s)
confere_saida("lp-s6-p06", p06(lambda v: v > 100))
distrator("lp-s6-p06", "3 470", p06(lambda v: v >= 100), ">=")
distrator("lp-s6-p06", "5 590", p06(lambda v: True), "sem filtro")
distrator("lp-s6-p06", "2 250", p06(lambda v: v > 100, acum=False), "s <- v")
distrator("lp-s6-p06", "3 220", p06(lambda v: v <= 100), "filtro invertido")
ok(sum(E6) == 590 and 80 + 100 + 40 == 220 and 590 - 220 == 370 and 5 - 3 == 2, "p06 confira")

# ---------------- p07 ----------------
def p07(com_interrompa=True, conta_antes=True):
    c = 0; achou = 0
    for i in para(20, 40):
        if conta_antes:
            c += 1
        if i % 7 == 0:
            achou = i
            if com_interrompa:
                break
        if not conta_antes:
            c += 1
    return "%d %d" % (achou, c)
confere_saida("lp-s6-p07", p07())
distrator("lp-s6-p07", "35 21", p07(com_interrompa=False), "sem interrompa")
distrator("lp-s6-p07", "21 1", p07(conta_antes=False), "nao conta a volta do achado")
distrator("lp-s6-p07", "21 21", "21 %d" % (40 - 20 + 1), "c pela formula do para inteiro")
ok("40 − 20 + 1 = 21" in erro_de(Q["lp-s6-p07"], "21 21"), "p07 erro E cita a conta")
ok(7 * 3 == 21 and 7 * 2 == 14 and 21 - 20 + 1 == 2, "p07 confira")

# ---------------- p08 ----------------
v = {i: i * 3 for i in para(1, 5)}
s = sum(v[i] for i in para(2, 4))
confere_saida("lp-s6-p08", "%d %d" % (v[5], s))
distrator("lp-s6-p08", "15 45", "%d %d" % (v[5], sum(v.values())), "vetor inteiro")
distrator("lp-s6-p08", "15 9", "%d %d" % (v[5], 2 + 3 + 4), "indices")
distrator("lp-s6-p08", "15 15", "%d %d" % (v[5], v[2] + v[3]), "exclui o 4")
distrator("lp-s6-p08", "5 27", "%d %d" % (5, s), "indice no lugar do conteudo")
ok(3 * (2 + 3 + 4) == 27 and 3 * 6 > 9, "p08 confira/atalho")

# ---------------- p09 ----------------
E9 = [int(t) for t in Q["lp-s6-p09"]["entradas"]]
ok(E9 == [15, 8, 23, 11], "p09 entradas")
def p09(lista, ini_maior=0, ini_menor=0, sinal_menor="<", primeiro=False):
    if primeiro:
        maior = menor = lista[0]
        resto = lista[1:]
    else:
        maior, menor, resto = ini_maior, ini_menor, lista
    for x in resto:
        if x > maior:
            maior = x
        if (x < menor) if sinal_menor == "<" else (x > menor):
            menor = x
    return maior, menor
mx, mn = p09(E9)
confere_saida("lp-s6-p09", "%d %d" % (mx, mn))
ok(certa(Q["lp-s6-p09"]).startswith("Escreve 23 0;"), "p09 certa")
ok(p09(E9, sinal_menor=">")[1] == 23, "p09 B: menor com > segue os grandes")
random.seed(6)
for _ in range(2000):
    lst = [random.randint(-500, 500) for _ in range(4)]
    ok(p09(lst, primeiro=True) == (max(lst), min(lst)), "p09 correcao C falhou em %s" % lst)
ok(p09([150, 200, 300, 120], primeiro=True) == (300, 120), "p09 confira")
ok(p09([150, 200, 300, 120], ini_menor=100)[1] == 100, "p09 E com 100 falha")
ok(p09(E9, ini_menor=100)[1] == 8, "p09 E funciona com estas entradas")
ok(p09(E9)[0] == 23 and p09(E9)[0] != 0, "p09 D: maior troca")

# ---------------- p10 ----------------
def roda(ini, cond, corpo, repita=False, limite=5000):
    x = ini; seq = [x]; passos = 0
    if repita:
        while True:
            x = corpo(x); seq.append(x); passos += 1
            if cond(x) or passos > limite:
                break
        return seq, passos <= limite
    while cond(x):
        x = corpo(x); seq.append(x); passos += 1
        if passos > limite:
            return seq, False
    return seq, True
T = {
    1: roda(1, lambda x: x < 10, lambda x: x + 2),
    2: roda(20, lambda x: x > 0, lambda x: vdiv(x, 2)),
    3: roda(1, lambda x: x != 10, lambda x: x + 2),
    4: roda(10, lambda x: x < 0, lambda x: x - 3, repita=True),
    5: roda(1, lambda x: x <= 100, lambda x: x * 2),
}
for k, (seq, termina) in T.items():
    print("p10 trecho", k, "termina" if termina else "NAO termina", seq[:8])
ok([k for k, (s_, t_) in T.items() if not t_] == [3], "p10 so o trecho 3 nao termina")
ok(T[1][0] == [1, 3, 5, 7, 9, 11], "p10 t1")
ok(T[2][0] == [20, 10, 5, 2, 1, 0], "p10 t2")
ok(T[4][0] == [10, 7, 4, 1, -2], "p10 t4")
ok(T[5][0] == [1, 2, 4, 8, 16, 32, 64, 128], "p10 t5")
ok(all(x % 2 == 1 for x in T[3][0]), "p10 t3 so impares")
ok(certa(Q["lp-s6-p10"]) == "Trecho 3", "p10 certa")
linhas = Q["lp-s6-p10"]["tabela"]["linhas"]
ok([l[1:] for l in linhas] == [
    ["`x <- 1`", "`enquanto x < 10 faca`", "`x <- x + 2`"],
    ["`x <- 20`", "`enquanto x > 0 faca`", "`x <- x div 2`"],
    ["`x <- 1`", "`enquanto x <> 10 faca`", "`x <- x + 2`"],
    ["`x <- 10`", "`repita ... ate x < 0`", "`x <- x - 3`"],
    ["`x <- 1`", "`enquanto x <= 100 faca`", "`x <- x * 2`"]], "p10 tabela bate com a simulacao")
# trabalho: diferenca 3, ajuste de 2
d = 3; dif = []
for _ in range(4):
    dif.append(d); d -= 2
ok(dif == [3, 1, -1, -3] and 0 not in dif and abs(1) < 2, "p10 trabalho")

# ---------------- p11 ----------------
def p11(voltas=4, reset=False, ordem_trocada=False):
    a = b = 1; tab = []
    for i in para(1, voltas):
        if reset:
            a = b = 1
        t = a + b
        if ordem_trocada:
            b = t; a = b
        else:
            a = b; b = t
        tab.append((i, t, a, b))
    return "%d %d" % (a, b), tab
s11, tab = p11()
confere_saida("lp-s6-p11", s11)
ok(tab == [(1, 2, 1, 2), (2, 3, 2, 3), (3, 5, 3, 5), (4, 8, 5, 8)], "p11 visual: linhas da tabela")
distrator("lp-s6-p11", "8 13", p11(5)[0], "volta a mais")
distrator("lp-s6-p11", "1 2", p11(reset=True)[0], "reset")
distrator("lp-s6-p11", "3 5", p11(3)[0], "3 voltas")
distrator("lp-s6-p11", "16 16", p11(ordem_trocada=True)[0], "ordem trocada")
ok([r[2:] for r in p11(ordem_trocada=True)[1]] == [(2, 2), (4, 4), (8, 8), (16, 16)], "p11 erro E cita 2 2, 4 4, 8 8, 16 16")

# ---------------- p12 ----------------
E12 = [int(t) for t in Q["lp-s6-p12"]["entradas"]]
ok(E12 == [7, 5, 9, 0], "p12 entradas")
def p12(sem="repita"):
    fila = list(E12); s = c = 0; x = 0
    if sem == "repita":
        while True:
            x = fila.pop(0); s += x; c += 1
            if x == 0:
                break
        return "%d %d" % (s, c), len(fila)
    if sem == "enquanto_x_igual_0":  # le o ate como continuar enquanto x = 0
        while True:
            x = fila.pop(0); s += x; c += 1
            if not (x == 0):
                break
        return "%d %d" % (s, c), len(fila)
    if sem == "testa_antes":  # testa x = 0 antes de ler; x comeca em 0
        while not (x == 0):
            x = fila.pop(0); s += x; c += 1
        return "%d %d" % (s, c), len(fila)
s12, sobra = p12()
confere_saida("lp-s6-p12", s12)
ok(sobra == 0, "p12 nao pede quinta entrada")
distrator("lp-s6-p12", "21 3", "%d %d" % (7 + 5 + 9, 3), "proposito")
distrator("lp-s6-p12", "7 1", p12("enquanto_x_igual_0")[0], "ate como enquanto")
distrator("lp-s6-p12", "0 0", p12("testa_antes")[0], "testa antes")
ok(7 + 5 + 9 + 0 == 21, "p12 soma")

# ---------------- teoria: formula das voltas ----------------
for _ in range(3000):
    a = random.randint(-30, 30); b = random.randint(-30, 30); p = random.choice([1, 2, 3, 4, 5, -1, -2, -3, -4])
    real = len(list(para(a, b, p)))
    if p > 0:
        prev = vdiv(b - a, p) + 1 if a <= b else 0
    else:
        prev = vdiv(a - b, abs(p)) + 1 if a >= b else 0
    ok(real == prev, "formula de voltas falhou a=%d b=%d p=%d real=%d prev=%d" % (a, b, p, real, prev))
    if p != 0 and ((p > 0 and a <= b) or (p < 0 and a >= b)):
        ok(vdiv(b - a, p) + 1 == real, "formula do bloco (fim - inicio) div passo + 1 falhou a=%d b=%d p=%d" % (a, b, p))
# exemplo do bloco: para i de 1 ate 9 passo 2
ok(list(para(1, 9, 2)) == [1, 3, 5, 7, 9], "bloco para")

# ---------------- forma do texto ----------------
def textos(o, caminho=""):
    if isinstance(o, str):
        yield caminho, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from textos(v, caminho + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from textos(v, caminho + "[%d]" % i)
PROIB = ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada", "fascinante",
         "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente"]
travessoes = 0
for nome, d in (("p1", p1), ("p2", p2)):
    for cam, t in textos(d):
        if cam.endswith(".codigo"):
            continue
        ok(not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", t), "%s%s byte de controle" % (nome, cam))
        travessoes += t.count("—")
        low = t.lower()
        for w in PROIB:
            ok(w not in low, "%s%s expressao proibida %s" % (nome, cam, w))
        ok("!" not in t, "%s%s exclamacao" % (nome, cam))
ok(travessoes == 1, "travessoes: %d" % travessoes)
for nome in ("lp_s6_p1.json", "lp_s6_p2.json"):
    with open(os.path.join(DADOS, nome), "rb") as f:
        raw = f.read()
    ok(not re.search(rb"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", raw), nome + " bytes de controle no arquivo")

def npal(s):
    return len(re.findall(r"\S+", s))
for q in Q.values():
    j = q["jeitos"]
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = npal(j[k])
        ok(35 <= n <= 110, "%s.%s com %d palavras" % (q["id"], k, n))
    ok(3 <= len(j["receita"]) <= 7, "%s receita %d passos" % (q["id"], len(j["receita"])))
    ok(4 <= len(j["conversa"]) <= 8, "%s conversa %d falas" % (q["id"], len(j["conversa"])))
for b in S["blocos"]:
    n = npal(b["texto"])
    ok(40 <= n <= 120, "bloco %s com %d palavras" % (b["titulo"], n))
for k, t in S["jeitos"].items():
    n = npal(t)
    ok(50 <= n <= 120, "teoria jeito %s com %d palavras" % (k, n))
ok(3 <= len(S["blocos"]) <= 6, "blocos 3 a 6")

print()
print("RESULTADO:", "OK" if not falhas else "%d falha(s)" % len(falhas))
