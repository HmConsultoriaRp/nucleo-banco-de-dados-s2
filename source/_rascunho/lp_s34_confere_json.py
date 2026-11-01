# Confere o que foi gravado nos JSON do lote lp_s34:
# 1. cada coluna de tabela cujo cabecalho e formula e recalculada linha a linha;
# 2. a alternativa marcada como certa e a esperada pelas contas (lp_s34_contas.py);
# 3. as saidas dos dois codigos VisuAlg, simuladas a mao em Python;
# 4. tamanho dos textos (jeitos, blocos da teoria).
import json, os, re, sys, itertools
sys.stdout.reconfigure(encoding="utf-8")

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("lp_s34_") and f.endswith(".json"))
docs = {}
for f in arqs:
    with open(os.path.join(DADOS, f), encoding="utf-8") as h:
        docs[f] = json.load(h)
qs = {q["id"]: q for d in docs.values() for q in d["questoes"]}
print("arquivos:", arqs, "questoes:", len(qs))

falhas = []
def checa(nome, cond):
    print(("ok   " if cond else "FALHA ") + nome)
    if not cond: falhas.append(nome)

# ---------- parser de formulas: ¬ > ∧ > ∨/⊕ > → (direita) > ↔ ----------
def tokens(s):
    out = []
    for c in s:
        if c.isspace(): continue
        if c in "pqrs¬∧∨⊕→↔()": out.append(c)
        else: raise ValueError("simbolo " + c)
    return out

def parse(s):
    t = tokens(s); i = [0]
    def pk(): return t[i[0]] if i[0] < len(t) else None
    def nx(): i[0] += 1; return t[i[0] - 1]
    def bi():
        a = imp()
        while pk() == "↔": nx(); b = imp(); a = ("↔", a, b)
        return a
    def imp():
        a = ou()
        if pk() == "→": nx(); return ("→", a, imp())
        return a
    def ou():
        a = e()
        while pk() in ("∨", "⊕"): op = nx(); a = (op, a, e())
        return a
    def e():
        a = nao()
        while pk() == "∧": nx(); a = ("∧", a, nao())
        return a
    def nao():
        if pk() == "¬": nx(); return ("¬", nao())
        return at()
    def at():
        c = nx()
        if c == "(":
            x = bi()
            assert nx() == ")"
            return x
        assert c in "pqrs", c
        return c
    arv = bi()
    assert i[0] == len(t), "sobrou " + s
    return arv

def ev(a, v):
    if isinstance(a, str): return v[a]
    op = a[0]
    if op == "¬": return not ev(a[1], v)
    x, y = ev(a[1], v), ev(a[2], v)
    return {"∧": x and y, "∨": x or y, "⊕": x != y, "→": (not x) or y, "↔": x == y}[op]

def eh_formula(s):
    try:
        parse(s); return True
    except Exception:
        return False

# ---------- 1. tabelas ----------
for qid, q in qs.items():
    t = q.get("tabela")
    if not t: continue
    cab, linhas = t["cab"], t["linhas"]
    letras = [c for c in cab if c in ("p", "q", "r", "s")]
    if letras:
        n_ok = 0; n_col = 0
        for j, c in enumerate(cab):
            nome = c.replace("conclusão ", "")
            if nome in letras or not eh_formula(nome) or nome == "fórmula": continue
            if q["tabela"]["onde"] == "enunciado" and c == "fórmula": continue
            n_col += 1
            arv = parse(nome)
            for l in linhas:
                v = {x: l[cab.index(x)] == "V" for x in letras}
                if (ev(arv, v) and l[j] == "V") or ((not ev(arv, v)) and l[j] == "F"): n_ok += 1
                else: print("   divergencia", qid, c, l)
        checa("%s tabela: %d colunas de formula, %d celulas conferidas" % (qid, n_col, n_ok), n_ok == n_col * len(linhas))
        # linhas na ordem padrao e sem repeticao (quando a tabela tem todas as combinacoes)
        combos = [tuple(l[cab.index(x)] for x in letras) for l in linhas]
        if len(linhas) == 2 ** len(letras):
            padrao = [tuple("V" if b else "F" for b in c) for c in itertools.product([True, False], repeat=len(letras))]
            checa("%s tabela na ordem padrao V...F" % qid, combos == padrao)

# tabelas especiais
t = qs["lp-s3-p03"]["tabela"]
for l in t["linhas"]:
    val = ev(parse(l[0]), {"p": True, "q": False})
    checa("s3-p03 linha %s = %s" % (l[0], l[2]), ("V" if val else "F") == l[2])
t = qs["lp-s3-p02"]["tabela"]
checa("s3-p02 tabela de 2^n", all(int(l[2]) == 2 ** int(l[0]) for l in t["linhas"]))
t = qs["lp-s3-p10"]["tabela"]
for l in t["linhas"]:
    v = {"p": l[0] == "V", "q": l[1] == "V", "r": l[2] == "V"}
    a, b = ev(parse("p → q"), v), ev(parse("q ∨ r"), v)
    serve = (a is False) and (b is True)
    checa("s3-p10 linha %s %s %s: atende = %s" % (l[0], l[1], l[2], l[5]), (l[5] == "sim") == serve)

# tabela do enunciado de s3-p12: a certa tem de reproduzir a coluna, as outras nao
t = qs["lp-s3-p12"]["tabela"]
for a in qs["lp-s3-p12"]["alternativas"]:
    arv = parse(a["t"])
    bate = all((ev(arv, {"p": l[0] == "V", "q": l[1] == "V", "r": l[2] == "V"}) == (l[3] == "V")) for l in t["linhas"])
    checa("s3-p12 alternativa %s bate=%s certa=%s" % (a["t"], bate, a["certa"]), bate == a["certa"])
t = qs["lp-s3-p06"]["tabela"]
for a in qs["lp-s3-p06"]["alternativas"]:
    arv = parse(a["t"])
    bate = all((ev(arv, {"p": l[0] == "V", "q": l[1] == "V"}) == (l[2] == "V")) for l in t["linhas"])
    checa("s3-p06 alternativa %s bate=%s certa=%s" % (a["t"], bate, a["certa"]), bate == a["certa"])

# ---------- 2. alternativa certa ----------
esperado = {
    "lp-s3-p01": "O número 15 é divisível por 4.",
    "lp-s3-p02": "16", "lp-s3-p03": "p ⊕ q", "lp-s3-p04": "¬q ∧ p",
    "lp-s3-p05": "((¬p) ∨ q) → r, valor F", "lp-s3-p06": "p ⊕ q",
    "lp-s3-p07": "O mês foi fechado somente se o lançamento foi conciliado.",
    "lp-s3-p08": "VERDADEIRO, FALSO, FALSO", "lp-s3-p09": "3",
    "lp-s3-p10": "p = V, q = F, r = V", "lp-s3-p11": "p ∧ q → r ∨ s", "lp-s3-p12": "(p ∨ q) ∧ ¬r",
    "lp-s4-p01": "(p ∧ q) → p", "lp-s4-p02": "O boleto não foi pago ou a nota não foi emitida.",
    "lp-s4-p03": "Se a NF não tem DI, então ela não é de importação.",
    "lp-s4-p04": "Algum título vencido não foi cobrado.",
    "lp-s4-p05": "O valor passa de 10 mil reais e o pagamento não tem duas aprovações.",
    "lp-s4-p06": "Se o pedido foi pago, ele foi liberado. Ele não foi liberado. Logo, não foi pago.",
    "lp-s4-p07": "∀x (¬D(x) → ¬A(x))", "lp-s4-p08": "VERDADEIRO, FALSO, VERDADEIRO",
    "lp-s4-p09": "p = F, q = V, r = F", "lp-s4-p10": "O lote chegou e o custo foi lançado.",
    "lp-s4-p11": "p → q", "lp-s4-p12": "∀x (P(x) → ¬N(x))",
}
for qid, txt in esperado.items():
    certa = [a["t"] for a in qs[qid]["alternativas"] if a.get("certa")]
    checa("%s certa = %s" % (qid, txt), certa == [txt])

# s3-p11 e s4-p11: a certa e equivalente ao alvo; as erradas nao
def equiv(f, g, letras):
    a, b = parse(f), parse(g)
    for c in itertools.product([True, False], repeat=len(letras)):
        v = dict(zip(letras, c))
        if ev(a, v) != ev(b, v): return False
    return True
for qid, alvo, letras in [("lp-s3-p11", "(p ∧ q) → (r ∨ s)", "pqrs"), ("lp-s4-p11", "¬(p ∧ ¬q)", "pq"),
                          ("lp-s4-p01", "p ∨ ¬p", "pq")]:
    for a in qs[qid]["alternativas"]:
        eq = equiv(alvo, a["t"], letras)
        checa("%s %s equivalente a %s: %s" % (qid, a["t"], alvo, eq), eq == bool(a.get("certa")))

# s3-p05: as 5 leituras e valores com p = F, q = V, r = F
v = {"p": False, "q": True, "r": False}
for a in qs["lp-s3-p05"]["alternativas"]:
    form, val = a["t"].rsplit(", valor ", 1)
    real = "V" if ev(parse(form), v) else "F"
    leitura_certa = form == "((¬p) ∨ q) → r"
    if leitura_certa and not a.get("certa"):
        # alternativa D: leitura certa com a conta final errada, de proposito
        checa("s3-p05 '%s' (D) afirma %s e o valor real e %s: erro de conta proposital" % (form, val, real), val != real)
    else:
        checa("s3-p05 '%s' vale %s" % (form, val), real == val)
checa("s3-p05 leitura sem parenteses = leitura certa", equiv("¬p ∨ q → r", "((¬p) ∨ q) → r", "pqr"))

# s3-p09: numero de linhas falsas
nf = sum(1 for c in itertools.product([True, False], repeat=3) if not ev(parse("(p ∨ q) → ¬r"), dict(zip("pqr", c))))
checa("s3-p09 linhas falsas = %d" % nf, nf == 3)

# ---------- 3. codigos VisuAlg simulados a mao ----------
p, q, r = True, False, False
s3 = [p or (q and r), (p or q) and r, (not q) and r]
pago, emitida = True, False
s4 = [not (pago and emitida), (not pago) and (not emitida), (not pago) or (not emitida)]
def txt(lst): return "\n".join("VERDADEIRO" if x else "FALSO" for x in lst)
checa("s3-p08 saida simulada = campo saida", txt(s3) == qs["lp-s3-p08"]["saida"])
checa("s4-p08 saida simulada = campo saida", txt(s4) == qs["lp-s4-p08"]["saida"])
checa("s3-p08 alternativa certa = saida", qs["lp-s3-p08"]["saida"].replace("\n", ", ") == esperado["lp-s3-p08"])
checa("s4-p08 alternativa certa = saida", qs["lp-s4-p08"]["saida"].replace("\n", ", ") == esperado["lp-s4-p08"])

# ---------- 4. tamanhos ----------
def np(s): return len(re.findall(r"\S+", s))
fora = []
for qid, q in qs.items():
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n = np(q["jeitos"][k])
        if not 35 <= n <= 110: fora.append((qid, k, n))
    if not 3 <= len(q["jeitos"]["receita"]) <= 7: fora.append((qid, "receita", len(q["jeitos"]["receita"])))
    if not 4 <= len(q["jeitos"]["conversa"]) <= 8: fora.append((qid, "conversa", len(q["jeitos"]["conversa"])))
for d in docs.values():
    for s in d["semanas"]:
        for b in s["blocos"]:
            n = np(b["texto"])
            if not 40 <= n <= 120: fora.append(("semana %d" % s["semana"], b["titulo"], n))
        for k, t in s["jeitos"].items():
            n = np(t)
            if not 50 <= n <= 120: fora.append(("semana %d" % s["semana"], "jeitos." + k, n))
print("textos fora da faixa:", fora)
checa("todos os textos na faixa", not fora)

# niveis e posicoes
from collections import Counter
for sem in (3, 4):
    c = Counter(q["nivel"] for q in qs.values() if q["semana"] == sem)
    checa("semana %d: 4 questoes por nivel %s" % (sem, dict(c)), c == Counter({1: 4, 2: 4, 3: 4}))
pos = Counter("ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in qs.values())
print("posicoes das certas:", dict(sorted(pos.items())))
checa("nenhuma letra acima de 30%", max(pos.values()) / len(qs) <= 0.30)

print()
print("TUDO OK" if not falhas else "FALHAS: %d" % len(falhas))
