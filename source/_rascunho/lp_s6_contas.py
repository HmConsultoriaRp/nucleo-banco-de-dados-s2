# Confere por Python as contas do lote lp_s6 (Logica, semana 6).
# Cada algoritmo e reescrito em Python, a saida e comparada com o campo "saida"
# e cada valor citado no "erro" das alternativas e recalculado.
# Uso: python -I lp_s6_contas.py
import json, os, re, sys

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

d1 = carrega("lp_s6_p1.json")
d2 = carrega("lp_s6_p2.json")
qs = {q["id"]: q for q in d1["questoes"] + d2["questoes"]}
with open(os.path.join(GER, "exemplos.json"), encoding="utf-8") as f:
    ex = json.load(f)

def norm(s):
    # mesma ideia do normalizarSaida do site: espaco em volta de numero, espacos colapsados
    linhas = []
    for l in s.replace("\r", "").split("\n"):
        l = re.sub(r"(-?\d+(?:\.\d+)?)", r" \1 ", l)
        linhas.append(re.sub(r"\s+", " ", l).strip())
    return "\n".join(linhas).strip("\n")

def certa(q):
    return [a["t"] for a in q["alternativas"] if a.get("certa")][0]

def confere_saida(qid, obtida):
    q = qs[qid]
    ok(norm(obtida) == norm(q["saida"]), f"{qid}: saida Python {obtida!r} x JSON {q['saida']!r}")
    print(f"{qid}: saida Python = {obtida!r}")

# ---------- p01 (copia do exemplos.json) ----------
ex_p01 = [q for q in ex["questoes"] if q["id"] == "lp-s6-p01"][0]
ok(ex_p01 == qs["lp-s6-p01"], "lp-s6-p01: nao e copia exata do exemplos.json")
s = sum(i for i in range(1, 7) if i % 2 == 0)
confere_saida("lp-s6-p01", str(s))

# ---------- p02 ----------
def voltas_para(a, b, p):
    vals, i = [], a
    while (i <= b if p > 0 else i >= b):
        vals.append(i); i += p
    return vals
v = voltas_para(3, 15, 4)
confere_saida("lp-s6-p02", str(len(v)))
ok(v == [3, 7, 11, 15], "p02 valores do i")
ok(15 - 3 + 1 == 13 and (15 - 3) // 4 == 3 and 15 - 3 == 12, "p02 erros 13/3/12")
ok(len(v) + 1 == 5 and v[-1] + 4 == 19, "p02 erro 5 (conta o 19)")
ok((15 - 3) // 4 + 1 == 4, "p02 formula das voltas")

# ---------- p03 ----------
v = voltas_para(10, 2, -2)
confere_saida("lp-s6-p03", " ".join(map(str, v)))
ok((10 - 2) // 2 + 1 == 5 == len(v), "p03 formula passo negativo")
ok(v[-1] - 2 == 0, "p03 proximo valor seria 0")

# ---------- p04 ----------
x, c = 20, 0
while x < 10:
    x -= 3; c += 1
confere_saida("lp-s6-p04", f"c = {c}, x = {x}")
# erro A: leu como "ate x < 10"
x, c = 20, 0
while not (x < 10):
    x -= 3; c += 1
ok((c, x) == (4, 8), f"p04 erro A deu {(c, x)}")
# erro B: uma volta antes de testar
ok((20 - 3, 1) == (17, 1), "p04 erro B")

# ---------- p05 ----------
def p05(n, extra=0):
    c = 0
    while True:
        n += 10; c += 1
        if n > 40:
            break
    for _ in range(extra):
        n += 10; c += 1
    return c, n
c, n = p05(int(qs["lp-s6-p05"]["entradas"][0]))
confere_saida("lp-s6-p05", f"{c} {n}")
ok(p05(50, extra=1) == (2, 70), "p05 erro 2 70")

# ---------- p06 ----------
ent = list(map(int, qs["lp-s6-p06"]["entradas"]))
c = sum(1 for v in ent if v > 100); s = sum(v for v in ent if v > 100)
confere_saida("lp-s6-p06", f"{c} {s}")
ok((sum(1 for v in ent if v >= 100), sum(v for v in ent if v >= 100)) == (3, 470), "p06 erro 3 470")
ok((len(ent), sum(ent)) == (5, 590), "p06 erro 5 590")
ok([v for v in ent if v > 100][-1] == 250, "p06 erro 2 250")
ok((sum(1 for v in ent if v <= 100), sum(v for v in ent if v <= 100)) == (3, 220), "p06 erro 3 220")
ok(590 - 220 == 370 and 5 - 3 == 2, "p06 confira")

# ---------- p07 ----------
c, achou = 0, 0
for i in range(20, 41):
    c += 1
    if i % 7 == 0:
        achou = i
        break
confere_saida("lp-s6-p07", f"{achou} {c}")
c2, ach2 = 0, 0
for i in range(20, 41):
    c2 += 1
    if i % 7 == 0:
        ach2 = i
ok((ach2, c2) == (35, 21), f"p07 erro sem interrompa deu {(ach2, c2)}")
ok([m for m in range(20, 41) if m % 7 == 0] == [21, 28, 35], "p07 multiplos")

# ---------- p08 ----------
vet = {i: i * 3 for i in range(1, 6)}
s = sum(vet[i] for i in range(2, 5))
confere_saida("lp-s6-p08", f"{vet[5]} {s}")
ok(sum(vet.values()) == 45, "p08 erro 45")
ok(2 + 3 + 4 == 9, "p08 erro 9")
ok(vet[2] + vet[3] == 15, "p08 erro 15")
ok(3 * (2 + 3 + 4) == 27, "p08 confira")

# ---------- p09 ----------
def p09(ent, maior0, menor0):
    maior, menor = maior0, menor0
    for x in ent:
        if x > maior: maior = x
        if x < menor: menor = x
    return maior, menor
ent = list(map(int, qs["lp-s6-p09"]["entradas"]))
mx, mn = p09(ent, 0, 0)
confere_saida("lp-s6-p09", f"{mx} {mn}")
ok((max(ent), min(ent)) == (23, 8), "p09 alvo 23 8")
ok(p09(ent[1:], ent[0], ent[0]) == (23, 8), "p09 correcao com o primeiro lido")
ok(p09([150, 200, 300, 120][1:], 150, 150) == (300, 120), "p09 confira correcao")
ok(p09([150, 200, 300, 120], 0, 100)[1] == 100, "p09 confira menor com 100")

# ---------- p10 (sem codigo: simula os cinco trechos com limite de passos) ----------
def roda(x, cond, corpo, repita=False, limite=10000):
    passos = 0
    if repita:
        while True:
            x = corpo(x); passos += 1
            if cond(x): return x, passos
            if passos > limite: return None, passos
    while cond(x):
        x = corpo(x); passos += 1
        if passos > limite: return None, passos
    return x, passos
t1 = roda(1, lambda x: x < 10, lambda x: x + 2)
t2 = roda(20, lambda x: x > 0, lambda x: x // 2)
t3 = roda(1, lambda x: x != 10, lambda x: x + 2)
t4 = roda(10, lambda x: x < 0, lambda x: x - 3, repita=True)
t5 = roda(1, lambda x: x <= 100, lambda x: x * 2)
print("p10 trechos (valor final, voltas):", t1, t2, t3, t4, t5)
ok(t1[0] == 11 and t2[0] == 0 and t3[0] is None and t4[0] == -2 and t5[0] == 128, "p10 trechos")
ok(certa(qs["lp-s6-p10"]) == "Trecho 3", "p10 certa deveria ser Trecho 3")
# a analogia do trabalho: diferenca impar andando de 2 em 2 centavos
d, vistos = 3, []
for _ in range(3):
    vistos.append(d); d -= 2
ok(vistos == [3, 1, -1], "p10 trabalho 3, 1, -1")

# ---------- p11 ----------
def p11(voltas, ordem_trocada=False, reinicia=False):
    a, b = 1, 1
    for _ in range(voltas):
        if reinicia: a, b = 1, 1
        t = a + b
        if ordem_trocada:
            b = t; a = b
        else:
            a = b; b = t
    return a, b
a, b = p11(4)
confere_saida("lp-s6-p11", f"{a} {b}")
ok(p11(5) == (8, 13), "p11 erro 8 13")
ok(p11(3) == (3, 5), "p11 erro 3 5")
ok(p11(4, reinicia=True) == (1, 2), "p11 erro 1 2")
ok(p11(4, ordem_trocada=True) == (16, 16), "p11 erro 16 16")

# ---------- p12 ----------
def p12(ent, como="repita"):
    fila = list(ent); s = c = x = 0
    if como == "testa_antes":          # erro: testa x = 0 antes de ler
        if x == 0: return s, c
    while True:
        x = fila.pop(0); s += x; c += 1
        if como == "ate_como_enquanto":   # erro: continua enquanto x = 0
            if x != 0: return s, c
        elif x == 0:
            return s, c
ent = list(map(int, qs["lp-s6-p12"]["entradas"]))
s, c = p12(ent)
confere_saida("lp-s6-p12", f"{s} {c}")
ok(p12(ent, "testa_antes") == (0, 0), "p12 erro 0 0")
ok(p12(ent, "ate_como_enquanto") == (7, 1), "p12 erro 7 1")
ok((sum(ent), len([v for v in ent if v != 0])) == (21, 3), "p12 erro 21 3")

# ---------- lab da semana: senha com 1234 primeiro ----------
fila = ["1234", "0000", "4321"]; vezes = 0
while True:
    tent = fila.pop(0); vezes += 1
    if tent == "1234": break
ok(vezes == 1, "lab senha deveria entrar na tentativa 1")

# ---------- forma: niveis, posicoes, tamanhos ----------
niveis = {}
for q in qs.values():
    niveis[q["nivel"]] = niveis.get(q["nivel"], 0) + 1
print("niveis:", dict(sorted(niveis.items())))
ok(niveis == {1: 4, 2: 4, 3: 4}, "deveria ter 4 questoes por nivel")
com_cod = [q["id"] for q in qs.values() if q.get("codigo")]
com_ent = [q["id"] for q in qs.values() if q.get("entradas")]
print("com codigo:", len(com_cod), "| com entradas:", com_ent)
ok(len(com_cod) >= 9 and len(com_ent) >= 3, "minimo de codigo/entradas")
pos = {}
for q in qs.values():
    L = "ABCDE"[[i for i, a in enumerate(q["alternativas"]) if a.get("certa")][0]]
    pos[L] = pos.get(L, 0) + 1
print("posicoes:", dict(sorted(pos.items())))
ok(max(pos.values()) / len(qs) <= 0.30, "letra acima de 30%")

def npal(s): return len(re.findall(r"\S+", s))
for qid, q in sorted(qs.items()):
    if qid == "lp-s6-p01":
        continue
    j = q["jeitos"]
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n = npal(j[k])
        ok(35 <= n <= 110, f"{qid}.{k}: {n} palavras")
    ok(3 <= len(j["receita"]) <= 7, f"{qid}.receita: {len(j['receita'])} passos")
    ok(4 <= len(j["conversa"]) <= 8, f"{qid}.conversa: {len(j['conversa'])} falas")
sem = d1["semanas"][0]
for b in sem["blocos"]:
    n = npal(b["texto"]); ok(40 <= n <= 120, f"bloco '{b['titulo']}': {n} palavras")
for k, t in sem["jeitos"].items():
    n = npal(t); ok(50 <= n <= 120, f"jeito da semana {k}: {n} palavras")

# ---------- bytes de controle e travessao ----------
for nome in ("lp_s6_p1.json", "lp_s6_p2.json"):
    with open(os.path.join(DADOS, nome), "rb") as f:
        raw = f.read()
    ctrl = [b for b in raw if b < 32 and b not in (9, 10, 13)]
    ok(not ctrl, f"{nome}: bytes de controle {ctrl[:5]}")
    txt = raw.decode("utf-8")
    print(nome, "travessoes:", txt.count("—"), "| hifen-menos em codigo e ok")

print("RESULTADO:", "OK" if not falhas else f"{len(falhas)} falha(s)")
