# Revisor adversarial do lote lp_s34 (Logica, semanas 3 e 4).
# Le o texto das alternativas direto do JSON, faz o parse das formulas e refaz tudo do zero.
# Nao confia no campo "resposta" nem no "certa": calcula e compara.
import itertools, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
Q = {}
SEM = {}
for f in sorted(os.listdir(DADOS)):
    if f.startswith("lp_s34_p") and f.endswith(".json"):
        d = json.load(open(os.path.join(DADOS, f), encoding="utf-8"))
        for s in d.get("semanas", []):
            SEM[s["semana"]] = s
        for q in d["questoes"]:
            Q[q["id"]] = q

falhas = []
def checa(nome, cond):
    print(("ok    " if cond else "FALHA ") + nome)
    if not cond:
        falhas.append(nome)

V, F = True, False
def tv(x): return "V" if x else "F"

# ---------- parser de formulas proposicionais ----------
# modo "padrao": ¬ > ∧ > ∨,⊕ > → (direita) > ↔
# modo "mesmo_nivel": ∧ e ∨ (e ⊕) no mesmo nivel, da esquerda para a direita
# modo "xou_baixo": ⊕ abaixo de ∨ e acima de →
def tokens(s):
    out = []
    for c in s:
        if c.isspace():
            continue
        if c in "pqrs":
            out.append(("at", c))
        elif c in "¬∧∨⊕→↔()":
            out.append((c, c))
        else:
            raise ValueError("simbolo " + repr(c) + " em " + s)
    return out

def parse(s, modo="padrao"):
    t = tokens(s)
    pos = [0]
    def pk():
        return t[pos[0]][0] if pos[0] < len(t) else None
    def come(x):
        assert pk() == x, (s, x, pos[0])
        pos[0] += 1
    def atom():
        k = pk()
        if k == "¬":
            pos[0] += 1
            a = atom()
            return ("¬", a)
        if k == "(":
            pos[0] += 1
            a = bi()
            come(")")
            return a
        if k == "at":
            v = t[pos[0]][1]
            pos[0] += 1
            return ("at", v)
        raise ValueError("esperava atomo em " + s)
    def bin_esq(sub, ops):
        a = sub()
        while pk() in ops:
            op = pk(); pos[0] += 1
            a = (op, a, sub())
        return a
    if modo == "padrao":
        def conj(): return bin_esq(atom, ("∧",))
        def disj(): return bin_esq(conj, ("∨", "⊕"))
    elif modo == "mesmo_nivel":
        def disj(): return bin_esq(atom, ("∧", "∨", "⊕"))
    elif modo == "xou_baixo":
        def conj(): return bin_esq(atom, ("∧",))
        def dis0(): return bin_esq(conj, ("∨",))
        def disj(): return bin_esq(dis0, ("⊕",))
    def imp():
        a = disj()
        if pk() == "→":
            pos[0] += 1
            return ("→", a, imp())
        return a
    def bi():
        return bin_esq(imp, ("↔",))
    r = bi()
    assert pos[0] == len(t), "sobrou algo em " + s
    return r

def ev(n, v):
    k = n[0]
    if k == "at": return v[n[1]]
    if k == "¬": return not ev(n[1], v)
    a, b = ev(n[1], v), ev(n[2], v)
    if k == "∧": return a and b
    if k == "∨": return a or b
    if k == "⊕": return a != b
    if k == "→": return (not a) or b
    if k == "↔": return a == b
    raise ValueError(k)

def letras(*fs):
    return sorted(set(c for f in fs for c in f if c in "pqrs"))

def linhas(ls):
    for comb in itertools.product([V, F], repeat=len(ls)):
        yield dict(zip(ls, comb))

def coluna(f, ls, modo="padrao"):
    n = parse(f, modo)
    return [ev(n, v) for v in linhas(ls)]

def robusto(f, ls):
    # o valor nao pode depender de convencao entre ∧/∨ nem da posicao do ⊕
    c = coluna(f, ls)
    return c == coluna(f, ls, "mesmo_nivel") == coluna(f, ls, "xou_baixo")

def colstr(c): return " ".join(tv(x) for x in c)

def certa_idx(q):
    return [a.get("certa") for a in q["alternativas"]].index(True)

def alts(q): return [a["t"] for a in q["alternativas"]]

# ---------- tabela do JSON: recalcula toda coluna que seja formula ----------
def confere_tabela(qid, tab, extra=None):
    cab = tab["cab"]
    ls = [c for c in cab if c in ("p", "q", "r", "s")]
    for i, l in enumerate(tab["linhas"]):
        # ordem padrao V...F
        esperado = list(itertools.product(["V", "F"], repeat=len(ls)))
        v = {}
        for j, c in enumerate(cab):
            if c in ls:
                v[c] = (l[j] == "V")
        if ls and len(tab["linhas"]) == 2 ** len(ls):
            checa(f"{qid} tabela linha {i+1} na ordem padrão", tuple(l[cab.index(x)] for x in ls) == esperado[i])
        for j, c in enumerate(cab):
            if c in ls: continue
            try:
                n = parse(c)
            except Exception:
                continue
            checa(f"{qid} tabela linha {i+1} coluna '{c}' = {l[j]}", tv(ev(n, v)) == l[j])

print("=================== SEMANA 3 ===================")

# s3-p01: so a classificacao. A conta citada: 15 = 4*3 + 3
q = Q["lp-s3-p01"]
checa("s3-p01 15 = 4×3 + 3 e 15 % 4 = 3 (frase falsa)", 15 == 4 * 3 + 3 and 15 % 4 == 3)
checa("s3-p01 x + 3 = 10: V com x = 7, F com x = 1", 7 + 3 == 10 and 1 + 3 != 10)
checa("s3-p01 certa é a frase do 15", "15" in alts(q)[certa_idx(q)])

# s3-p02
q = Q["lp-s3-p02"]
fm = "(p ∧ q) → (¬p ∨ r ∨ s)"
checa("s3-p02 enunciado traz a fórmula", fm in q["enunciado"])
oc = [c for c in fm if c in "pqrs"]
n = len(set(oc))
checa(f"s3-p02 ocorrências {len(oc)} distintas {n}", len(oc) == 5 and n == 4)
checa("s3-p02 certa = 2^4 = 16", alts(q)[certa_idx(q)] == str(2 ** n))
dist = {"4": n, "8": 2 * 4, "32": 2 ** 5, "10": 2 * 5}
for a in q["alternativas"]:
    if not a["certa"]:
        checa(f"s3-p02 distrator {a['t']} reproduzido pela conta do erro", str(dist[a["t"]]) == a["t"] and a["t"] != "16")
checa("s3-p02 confira: p com 8 V e 8 F", [x["p"] for x in linhas("pqrs")].count(True) == 8)
checa("s3-p02 tabela explicacao", [l[2] for l in q["tabela"]["linhas"]] == [str(2 ** k) for k in range(1, 5)])

# s3-p03: p = V, q = F
q = Q["lp-s3-p03"]
v = {"p": V, "q": F}
vals = [ev(parse(t), v) for t in alts(q)]
print("   s3-p03 valores:", dict(zip(alts(q), map(tv, vals))))
checa("s3-p03 exatamente uma verdadeira e é a marcada", vals.count(True) == 1 and vals.index(True) == certa_idx(q))
for l in q["tabela"]["linhas"]:
    checa(f"s3-p03 tabela {l[0]} = {l[2]}", tv(ev(parse(l[0]), v)) == l[2])
# confira: p = V, q = V
v2 = {"p": V, "q": V}
checa("s3-p03 confira p=q=V: ⊕ F; ∧, →, ↔ V", (not ev(parse("p ⊕ q"), v2)) and all(ev(parse(x), v2) for x in ["p ∧ q", "p → q", "p ↔ q"]))
checa("s3-p03 ¬p ∨ q ≡ p → q", coluna("¬p ∨ q", "pq") == coluna("p → q", "pq"))

# s3-p04: p aprovado, q enviado. frase: ¬q ∧ p
q = Q["lp-s3-p04"]
alvo = coluna("¬q ∧ p", "pq")
cols = [coluna(t, "pq") for t in alts(q)]
checa("s3-p04 só a marcada tem a coluna de ¬q ∧ p", [c == alvo for c in cols] == [i == certa_idx(q) for i in range(5)])
checa("s3-p04 confira p=V,q=F: ¬q ∧ p = V", ev(parse("¬q ∧ p"), {"p": V, "q": F}))
v = {"p": F, "q": F}
checa("s3-p04 confira p=F,q=F: ¬q∧p F; ¬(q∧p) V; ¬q∨p V", (not ev(parse("¬q ∧ p"), v)) and ev(parse("¬(q ∧ p)"), v) and ev(parse("¬q ∨ p"), v))

# s3-p05: p F, q V, r F; leituras com valor
q = Q["lp-s3-p05"]
v = {"p": F, "q": V, "r": F}
leitura_certa = parse("¬p ∨ q → r")
checa("s3-p05 parse padrão de ¬p ∨ q → r = ((¬p) ∨ q) → r", leitura_certa == parse("((¬p) ∨ q) → r"))
valor = ev(leitura_certa, v)
checa("s3-p05 valor F", valor is False)
for i, t in enumerate(alts(q)):
    form, val = t.split(", valor ")
    calc = ev(parse(form), v)
    if i == 3:
        # distrator D de proposito: leitura certa, valor errado
        checa(f"s3-p05 alt D '{form}' traz valor {val} errado de propósito (calc {tv(calc)})", tv(calc) != val)
    else:
        checa(f"s3-p05 alt {'ABCDE'[i]} '{form}' vale {val} (calc {tv(calc)})", tv(calc) == val)
    eh_certa = parse(form) == leitura_certa and val == tv(valor)
    checa(f"s3-p05 alt {'ABCDE'[i]} certa={eh_certa} bate com o JSON", eh_certa == (i == certa_idx(q)))

# s3-p06: coluna F V V F
q = Q["lp-s3-p06"]
col = [l[2] == "V" for l in q["tabela"]["linhas"]]
checa("s3-p06 linhas do enunciado na ordem padrão", [tuple(l[:2]) for l in q["tabela"]["linhas"]] == list(itertools.product("VF", repeat=2)))
cols = [coluna(t, "pq") for t in alts(q)]
checa("s3-p06 só a marcada bate", [c == col for c in cols] == [i == certa_idx(q) for i in range(5)])
checa("s3-p06 ¬(p∧q) bate só nas 3 primeiras", [a == b for a, b in zip(coluna("¬(p ∧ q)", "pq"), col)] == [V, V, V, F])
checa("s3-p06 p⊕q ≡ ¬(p↔q)", coluna("p ⊕ q", "pq") == coluna("¬(p ↔ q)", "pq"))
checa("s3-p06 p→q: V na 1ª e F na 2ª", coluna("p → q", "pq")[:2] == [V, F])

# s3-p07: q → p (q fechado, p conciliado); caso proibido de cada alternativa
q = Q["lp-s3-p07"]
form_alts = ["p → q", "q → p", "q ↔ p", "q ∧ p", "¬q → ¬p"]
for i, fa in enumerate(form_alts):
    proib = [(v["p"], v["q"]) for v in linhas("pq") if not ev(parse(fa), v)]
    print(f"   s3-p07 {'ABCDE'[i]} {fa}: casos proibidos (p,q) {proib}")
checa("s3-p07 marcada é a B (somente se)", certa_idx(q) == 1)
checa("s3-p07 ¬q → ¬p ≡ p → q (proíbe o mesmo caso)", coluna("¬q → ¬p", "pq") == coluna("p → q", "pq"))
checa("s3-p07 q → p não equivale a p → q", coluna("q → p", "pq") != coluna("p → q", "pq"))
checa("s3-p07 ↔ proíbe 2, ∧ proíbe 3", coluna("q ↔ p", "pq").count(F) == 2 and coluna("q ∧ p", "pq").count(F) == 3)
checa("s3-p07 conversa: nenhuma alternativa começa com 'Se o mês foi fechado'", not any(t.startswith("Se o mês foi fechado") for t in alts(q)))

# s3-p08: codigo (simulado em s34_visualg abaixo)

# s3-p09: (p ∨ q) → ¬r
q = Q["lp-s3-p09"]
c = coluna("(p ∨ q) → ¬r", "pqr")
nf = c.count(F)
checa(f"s3-p09 linhas falsas = {nf}", alts(q)[certa_idx(q)] == str(nf) and nf == 3)
checa("s3-p09 distrator 5 = verdadeiras", c.count(V) == 5)
checa("s3-p09 distrator 4 = linhas com r V", sum(1 for v in linhas("pqr") if v["r"]) == 4)
checa("s3-p09 distrator 1 = lendo ∧", coluna("(p ∧ q) → ¬r", "pqr").count(F) == 1)
checa("s3-p09 distrator 2 = lendo ⊕", coluna("(p ⊕ q) → ¬r", "pqr").count(F) == 2)
confere_tabela("s3-p09", q["tabela"])
falsas = [i + 1 for i, x in enumerate(c) if not x]
checa(f"s3-p09 visual: linhas com r V são 1,3,5,7 e falsas são 1,3,5 ({falsas})", falsas == [1, 3, 5] and [i + 1 for i, v in enumerate(linhas("pqr")) if v["r"]] == [1, 3, 5, 7])
checa("s3-p09 confira: 2 + 4 − 1 = 5", 2 + 4 - 1 == 5 == c.count(V))

# s3-p10: p→q F e q∨r V
q = Q["lp-s3-p10"]
sol = [v for v in linhas("pqr") if not ev(parse("p → q"), v) and ev(parse("q ∨ r"), v)]
print("   s3-p10 soluções:", sol)
checa("s3-p10 solução única p=V q=F r=V", sol == [{"p": V, "q": F, "r": V}])
checa("s3-p10 marcada", alts(q)[certa_idx(q)] == "p = V, q = F, r = V")
for i, t in enumerate(alts(q)):
    if "indeterminado" in t: continue
    vv = dict((k.strip(), x.strip() == "V") for k, x in (par.split("=") for par in t.split(",")))
    checa(f"s3-p10 alt {'ABCDE'[i]} atende? {vv in sol} (só a marcada)", (vv in sol) == (i == certa_idx(q)))
confere_tabela("s3-p10", q["tabela"])

# s3-p11: (p ∧ q) → (r ∨ s)
q = Q["lp-s3-p11"]
alvo = coluna("(p ∧ q) → (r ∨ s)", "pqrs")
for i, t in enumerate(alts(q)):
    cc = coluna(t, "pqrs")
    checa(f"s3-p11 alt {'ABCDE'[i]} '{t}' equivale? {cc == alvo}; não depende de ∧ x ∨", (cc == alvo) == (i == certa_idx(q)) and robusto(t, "pqrs"))
v = {"p": F, "q": V, "r": F, "s": F}
checa("s3-p11 confira: p=F,q=V,r=F,s=F: certa V, p ∧ (q → r ∨ s) F", ev(parse("p ∧ q → r ∨ s"), v) and not ev(parse("p ∧ (q → r ∨ s)"), v))
v = {"p": F, "q": V, "r": V, "s": F}
checa("s3-p11 erro C: enviado sem pagamento, ↔ acusa (F) e a frase não (V)", (not ev(parse("p ∧ q ↔ r ∨ s"), v)) and ev(parse("p ∧ q → r ∨ s"), v))

# s3-p12
q = Q["lp-s3-p12"]
col = [l[3] == "V" for l in q["tabela"]["linhas"]]
checa("s3-p12 linhas do enunciado na ordem padrão", [tuple(l[:3]) for l in q["tabela"]["linhas"]] == list(itertools.product("VF", repeat=3)))
ordem = [tuple(l[:3]) for l in q["tabela"]["linhas"]]
for i, t in enumerate(alts(q)):
    cc = coluna(t, "pqr")
    erra = ["".join(ordem[k]) for k in range(8) if cc[k] != col[k]]
    print(f"   s3-p12 {'ABCDE'[i]} {t}: erra {erra}")
    checa(f"s3-p12 alt {'ABCDE'[i]} certa só se bate nas 8; robusto", (not erra) == (i == certa_idx(q)) and robusto(t, "pqr"))
erra = lambda t: ["".join(ordem[k]) for k in range(8) if coluna(t, "pqr")[k] != col[k]]
checa("s3-p12 erro A: seta erra só as duas últimas", erra("(p ∨ q) → ¬r") == ["FFV", "FFF"])
checa("s3-p12 erro B: ↔ erra só F F V", erra("(p ∨ q) ↔ ¬r") == ["FFV"])
checa("s3-p12 erro D: ⊕ erra só V V F", erra("(p ⊕ q) ∧ ¬r") == ["VVF"])
checa("s3-p12 erro E: erra V V V e V F V", erra("p ∨ (q ∧ ¬r)") == ["VVV", "VFV"])

print("=================== SEMANA 4 ===================")
def classe(f):
    ls = letras(f)
    c = coluna(f, ls)
    return "T" if all(c) else "C" if not any(c) else "K"

q = Q["lp-s4-p01"]
cl = [classe(t) for t in alts(q)]
print("   s4-p01 classes:", dict(zip(alts(q), cl)))
checa("s4-p01 só a marcada é tautologia", [x == "T" for x in cl] == [i == certa_idx(q) for i in range(5)])
checa("s4-p01 p ∧ ¬p contradição; demais contingência", cl == ["K", "T", "K", "C", "K"])
checa("s4-p01 p → (p ∧ q): 3 V e 1 F", coluna("p → (p ∧ q)", "pq").count(V) == 3)
checa("s4-p01 p → (p ∧ q) falha em V F; (p ∨ q) → p falha em F V",
      [k for k, v in enumerate(linhas("pq")) if not ev(parse("p → (p ∧ q)"), v)] == [1] and [k for k, v in enumerate(linhas("pq")) if not ev(parse("(p ∨ q) → p"), v)] == [2])
confere_tabela("s4-p01", q["tabela"])

q = Q["lp-s4-p02"]
neg = coluna("¬(p ∧ q)", "pq")
form_alts = ["¬p ∧ ¬q", "¬p ∨ ¬q", "¬p ∨ q", "p ∧ ¬q", "¬p ∧ q"]
for i, fa in enumerate(form_alts):
    checa(f"s4-p02 alt {'ABCDE'[i]} ({fa}) é a negação? {coluna(fa, 'pq') == neg}", (coluna(fa, "pq") == neg) == (i == certa_idx(q)))
checa("s4-p02 erro C: pago sem nota (p V q F): ¬p ∨ q = F", not ev(parse("¬p ∨ q"), {"p": V, "q": F}))
confere_tabela("s4-p02", q["tabela"])

q = Q["lp-s4-p03"]
pq = coluna("p → q", "pq")
form_alts = ["q → p", "¬p → ¬q", "¬q → ¬p", "p ∧ ¬q", "p ∧ q"]
for i, fa in enumerate(form_alts):
    checa(f"s4-p03 alt {'ABCDE'[i]} ({fa}) equivale a p → q? {coluna(fa, 'pq') == pq}", (coluna(fa, "pq") == pq) == (i == certa_idx(q)))
checa("s4-p03 recíproca ≡ inversa", coluna("q → p", "pq") == coluna("¬p → ¬q", "pq"))
confere_tabela("s4-p03", q["tabela"])

q = Q["lp-s4-p05"]
neg = coluna("¬(p → q)", "pq")
form_alts = ["p ∧ ¬q", "p → ¬q", "¬p → ¬q", "¬p ∧ q", "¬p ∨ q"]
for i, fa in enumerate(form_alts):
    checa(f"s4-p05 alt {'ABCDE'[i]} ({fa}) é a negação? {coluna(fa, 'pq') == neg}", (coluna(fa, "pq") == neg) == (i == certa_idx(q)))
checa("s4-p05 erro C: p=q=V, regra e inversa V juntas", ev(parse("p → q"), {"p": V, "q": V}) and ev(parse("¬p → ¬q"), {"p": V, "q": V}))
checa("s4-p05 ¬p ∨ q ≡ regra", coluna("¬p ∨ q", "pq") == coluna("p → q", "pq"))
confere_tabela("s4-p05", q["tabela"])
# confira: 15 mil c/ 2 (V,V), 15 mil c/ 1 (V,F), 5 mil (F,?)
for (pp, qq) in [(V, V), (V, F), (F, V), (F, F)]:
    vv = {"p": pp, "q": qq}
    checa(f"s4-p05 confira p={tv(pp)} q={tv(qq)}: regra e negação opostas", ev(parse("p → q"), vv) != ev(parse("p ∧ ¬q"), vv))

# argumentos
def valido(premissas, conclusao):
    ls = letras(*premissas, conclusao)
    contra = [v for v in linhas(ls) if all(ev(parse(p), v) for p in premissas) and not ev(parse(conclusao), v)]
    return contra

q = Q["lp-s4-p06"]
args = [(["p → q", "q"], "p"), (["p → q", "¬p"], "¬q"), (["p ∨ q", "p"], "¬q"), (["p → q", "q → r"], "r → p"), (["p → q", "¬q"], "¬p")]
for i, (pr, co) in enumerate(args):
    cx = valido(pr, co)
    print(f"   s4-p06 {'ABCDE'[i]} {pr} ⊢ {co}: contraexemplos {cx}")
    checa(f"s4-p06 alt {'ABCDE'[i]} válido={not cx} bate com marcada", (not cx) == (i == certa_idx(q)))
checa("s4-p06 contraexemplo citado A,B: p=F q=V", {"p": F, "q": V} in valido(*args[0]) and {"p": F, "q": V} in valido(*args[1]))
checa("s4-p06 contraexemplo citado C: p=V q=V", {"p": V, "q": V} in valido(*args[2]))
checa("s4-p06 contraexemplo citado D: p=F q=V r=V", {"p": F, "q": V, "r": V} in valido(*args[3]))
checa("s4-p06 hipotético dá p → r", not valido(["p → q", "q → r"], "p → r"))
for l in Q["lp-s4-p06"]["tabela"]["linhas"]:
    partes = [x.strip() for x in l[1].replace("logo", "").split(";")]
    cx = valido(partes[:-1], partes[-1])
    checa(f"s4-p06 tabela '{l[0]}' {l[2]}", (l[2] == "válido") == (not cx))

q = Q["lp-s4-p09"]
cx = valido(["p ∨ q", "p → r"], "r")
print("   s4-p09 contraexemplos:", cx)
checa("s4-p09 contraexemplo único p=F q=V r=F", cx == [{"p": F, "q": V, "r": F}])
for i, t in enumerate(alts(q)):
    if t.startswith("Em nenhuma"):
        checa("s4-p09 E 'válido' é falso", bool(cx)); continue
    vv = dict((k.strip(), x.strip() == "V") for k, x in (par.split("=") for par in t.split(",")))
    checa(f"s4-p09 alt {'ABCDE'[i]} é contraexemplo? {vv in cx}", (vv in cx) == (i == certa_idx(q)))
confere_tabela("s4-p09", q["tabela"])
tab = q["tabela"]["linhas"]
checa("s4-p09 coluna 'conclusão r' = r", all(l[5] == l[2] for l in tab))
prem_f = [i + 1 for i, l in enumerate(tab) if l[3] == "F" or l[4] == "F"]
checa(f"s4-p09 visual: premissa F nas linhas 2,4,7,8 ({prem_f})", prem_f == [2, 4, 7, 8])

# s4-p10: L→D, D→C, L∨X, ¬X  (s = cancelado, usar letras p=L q=D r=C s=X)
prem = ["p → q", "q → r", "p ∨ s", "¬s"]
mundos = [v for v in linhas("pqrs") if all(ev(parse(x), v) for x in prem)]
print("   s4-p10 mundos que respeitam as premissas:", mundos)
checa("s4-p10 em todo mundo: lote chegou e custo lançado", all(v["p"] and v["r"] for v in mundos) and len(mundos) >= 1)
checa("s4-p10 também a DI registrada (B e D erradas)", all(v["q"] for v in mundos))
checa("s4-p10 com ou exclusivo também vale", all(v["p"] and v["r"] for v in linhas("pqrs") if ev(parse("p → q"), v) and ev(parse("q → r"), v) and ev(parse("p ⊕ s"), v) and not v["s"]))
checa("s4-p10 erro C: lendo L ↔ X, sairia lote F", all(not v["p"] for v in linhas("pqrs") if ev(parse("p ↔ s"), v) and not v["s"]))

q = Q["lp-s4-p11"]
alvo = coluna("¬(p ∧ ¬q)", "pq")
for i, t in enumerate(alts(q)):
    checa(f"s4-p11 alt {'ABCDE'[i]} {t} equivale? {coluna(t, 'pq') == alvo}", (coluna(t, "pq") == alvo) == (i == certa_idx(q)))
checa("s4-p11 ¬p ∧ q só V em p=F,q=V", coluna("¬p ∧ q", "pq") == [F, F, V, F])
confere_tabela("s4-p11", q["tabela"])

# ---------- quantificadores: forca bruta em mundos de 1 a 3 elementos ----------
def mundos_pred(n, k):
    # cada elemento recebe k bits (um por predicado)
    return itertools.product(itertools.product([V, F], repeat=k), repeat=n)

def todos_mundos(k, nmin=1, nmax=3):
    for n in range(nmin, nmax + 1):
        for m in mundos_pred(n, k):
            yield m

imp = lambda a, b: (not a) or b
# s4-p04: T vencido, C cobrado. Original ∀x(T→C). Negação: ∃x(T ∧ ¬C)
orig = lambda m: all(imp(t, c) for t, c in m)
alts04 = [
    ("Algum vencido não cobrado", lambda m: any(t and not c for t, c in m)),
    ("Nenhum vencido cobrado", lambda m: all(imp(t, not c) for t, c in m)),
    ("Algum vencido cobrado", lambda m: any(t and c for t, c in m)),
    ("Todo não vencido cobrado", lambda m: all(imp(not t, c) for t, c in m)),
    ("Algum não vencido cobrado", lambda m: any((not t) and c for t, c in m)),
]
q = Q["lp-s4-p04"]
for i, (nm, fn) in enumerate(alts04):
    e_neg = all(fn(m) != orig(m) for m in todos_mundos(2))
    checa(f"s4-p04 alt {'ABCDE'[i]} '{nm}' é negação? {e_neg}", e_neg == (i == certa_idx(q)))
m_ex = ((V, V), (V, F))
checa("s4-p04 erro B: 2 vencidos, 1 cobrado: original F e 'nenhum' F", (not orig(m_ex)) and not alts04[1][1](m_ex))
checa("s4-p04 erro C: 'algum vencido cobrado' pode ser V junto com a original", any(orig(m) and alts04[2][1](m) for m in todos_mundos(2)))

# s4-p07: D documento, A aprovado. Frase: nenhum sem documento foi aprovado = ∀x(¬D → ¬A)
frase = lambda m: not any((not d) and a for d, a in m)
alts07 = [
    lambda m: any((not d) and (not a) for d, a in m),
    lambda m: all((not d) and (not a) for d, a in m),
    lambda m: all(imp(d, a) for d, a in m),
    lambda m: all(imp(not d, not a) for d, a in m),
    lambda m: not any((not d) and (not a) for d, a in m),
]
q = Q["lp-s4-p07"]
for i, fn in enumerate(alts07):
    eq = all(fn(m) == frase(m) for m in todos_mundos(2))
    checa(f"s4-p07 alt {'ABCDE'[i]} equivale à frase? {eq}", eq == (i == certa_idx(q)))
checa("s4-p07 E ≡ ∀x(¬D → A)", all(alts07[4](m) == all(imp(not d, a) for d, a in m) for m in todos_mundos(2)))
m1 = ((V, V), (F, F))
checa("s4-p07 confira base 1: frase V, certa V, ∀(¬D∧¬A) F", frase(m1) and alts07[3](m1) and not alts07[1](m1))
m2 = ((V, V), (F, V))
checa("s4-p07 confira base 2: frase F e certa F", (not frase(m2)) and not alts07[3](m2))
checa("s4-p07 erro C: lançamento com documento sem aprovação quebra C e não a frase", (not alts07[2](((V, F),))) and frase(((V, F),)))

# s4-p12: P prazo, N nota. Original ∃x(P ∧ N). Negação.
orig12 = lambda m: any(p and n for p, n in m)
alts12 = [
    lambda m: any((not p) or (not n) for p, n in m),
    lambda m: all((not p) and (not n) for p, n in m),
    lambda m: all(imp(not p, not n) for p, n in m),
    lambda m: all(imp(p, not n) for p, n in m),
    lambda m: any(p and (not n) for p, n in m),
]
q = Q["lp-s4-p12"]
for i, fn in enumerate(alts12):
    e_neg = all(fn(m) != orig12(m) for m in todos_mundos(2))
    checa(f"s4-p12 alt {'ABCDE'[i]} é negação? {e_neg}", e_neg == (i == certa_idx(q)))
checa("s4-p12 erro A: perfeito + atrasado: original e A V juntas", orig12(((V, V), (F, V))) and alts12[0](((V, V), (F, V))))
checa("s4-p12 confira 1: um só, prazo e nota ok: certa F", not alts12[3](((V, V),)))
checa("s4-p12 confira 2: um só, atrasado e nota ok: certa V e C F", alts12[3](((F, V),)) and not alts12[2](((F, V),)))

# ---------- teoria das semanas ----------
print("=================== TEORIA ===================")
eqs = [("¬(p ∧ q)", "¬p ∨ ¬q"), ("¬(p ∨ q)", "¬p ∧ ¬q"), ("p → q", "¬p ∨ q"), ("p → q", "¬q → ¬p"), ("¬(p → q)", "p ∧ ¬q")]
for a, b in eqs:
    checa(f"teoria {a} ≡ {b}", coluna(a, "pq") == coluna(b, "pq"))
checa("teoria ¬¬p ≡ p", coluna("¬¬p", "p") == coluna("p", "p"))
checa("teoria recíproca e inversa não equivalem a p → q", coluna("q → p", "pq") != coluna("p → q", "pq") and coluna("¬p → ¬q", "pq") != coluna("p → q", "pq"))
checa("teoria p ∨ ¬p tautologia; p ∧ ¬p contradição; p → q contingência", classe("p ∨ ¬p") == "T" and classe("p ∧ ¬p") == "C" and classe("p → q") == "K")
for pr, co, ok in [(["p → q", "p"], "q", True), (["p → q", "¬q"], "¬p", True), (["p → q", "q → r"], "p → r", True), (["p ∨ q", "¬p"], "q", True), (["p → q", "q"], "p", False), (["p → q", "¬p"], "¬q", False)]:
    checa(f"teoria {pr} ⊢ {co} válido={ok}", (not valido(pr, co)) == ok)
checa("teoria falácias: contraexemplo p=F q=V nas duas", {"p": F, "q": V} in valido(["p → q", "q"], "p") and {"p": F, "q": V} in valido(["p → q", "¬p"], "¬q"))
checa("teoria ¬∀x P ≡ ∃x ¬P", all((not all(m)) == any(not x for x in m) for n in range(1, 4) for m in itertools.product([V, F], repeat=n)))
checa("teoria ¬∃x P ≡ ∀x ¬P", all((not any(m)) == all(not x for x in m) for n in range(1, 4) for m in itertools.product([V, F], repeat=n)))
checa("teoria precedência do exemplo ¬p ∨ q → r", parse("¬p ∨ q → r") == parse("((¬p) ∨ q) → r"))
checa("teoria p ∧ (p ∨ q) tem 2 letras: 4 linhas", len(letras("p ∧ (p ∨ q)")) == 2)
checa("teoria nem p nem q = ¬p ∧ ¬q = ¬(p ∨ q)", coluna("¬p ∧ ¬q", "pq") == coluna("¬(p ∨ q)", "pq"))
checa("teoria ↔ = V com valores iguais; ⊕ = V com diferentes", coluna("p ↔ q", "pq") == [V, F, F, V] and coluna("p ⊕ q", "pq") == [F, V, V, F])

print()
print("FALHAS:", len(falhas))
for f_ in falhas:
    print("  -", f_)
