# Conferencia das contas do lote lp_s34 (Logica, semanas 3 e 4).
# Cada bloco refaz por forca bruta o que a questao afirma.
import itertools, sys
sys.stdout.reconfigure(encoding="utf-8")

V, F = True, False
def imp(a, b): return (not a) or b
def bi(a, b): return a == b
def xou(a, b): return a != b
def tv(x): return "V" if x else "F"

def linhas(n):
    # ordem padrao: primeira coluna V V V V F F F F ...
    return list(itertools.product([V, F], repeat=n))

def coluna(f, n):
    return [f(*l) for l in linhas(n)]

def equiv(f, g, n):
    return coluna(f, n) == coluna(g, n)

def classe(f, n):
    c = coluna(f, n)
    if all(c): return "tautologia"
    if not any(c): return "contradicao"
    return "contingencia (%d V, %d F)" % (sum(c), len(c) - sum(c))

ok = True
def checa(nome, cond):
    global ok
    print(("ok   " if cond else "FALHA ") + nome)
    if not cond: ok = False

print("=== SEMANA 3 ===")
# s3-p02: (p ∧ q) → (¬p ∨ r ∨ s)
formula = "(p ∧ q) → (¬p ∨ r ∨ s)"
ocorr = [c for c in formula if c in "pqrs"]
dist = sorted(set(ocorr))
print("p02 ocorrencias", len(ocorr), "distintas", len(dist))
checa("p02 2^4 = 16", 2 ** len(dist) == 16)
checa("p02 2^5 = 32 (contando p duas vezes)", 2 ** len(ocorr) == 32)
checa("p02 2x4 = 8, 2x5 = 10", 2 * 4 == 8 and 2 * 5 == 10)

# s3-p03: p = V, q = F
p, q = V, F
vals = {"p ∧ q": p and q, "p → q": imp(p, q), "p ↔ q": bi(p, q), "¬p ∨ q": (not p) or q, "p ⊕ q": xou(p, q)}
print("p03", {k: tv(v) for k, v in vals.items()})
checa("p03 so p ⊕ q e V", [k for k, v in vals.items() if v] == ["p ⊕ q"])

# s3-p04: ¬q ∧ p e as erradas nao sao equivalentes
certa = lambda p, q: (not q) and p
for nome, g in [("¬q ∨ p", lambda p, q: (not q) or p), ("¬(q ∧ p)", lambda p, q: not (q and p)),
                ("q ∧ ¬p", lambda p, q: q and not p), ("p → ¬q", lambda p, q: imp(p, not q))]:
    checa("p04 %s difere de ¬q ∧ p" % nome, not equiv(certa, g, 2))

# s3-p05: p = F, q = V, r = F
p, q, r = F, V, F
leituras = {
    "((¬p) ∨ q) → r": imp((not p) or q, r),
    "¬((p ∨ q) → r)": not imp(p or q, r),
    "(¬p) ∨ (q → r)": (not p) or imp(q, r),
    "¬(p ∨ q) → r": imp(not (p or q), r),
}
print("p05", {k: tv(v) for k, v in leituras.items()})
checa("p05 certa F", leituras["((¬p) ∨ q) → r"] is F)
checa("p05 B V, C V, E V", leituras["¬((p ∨ q) → r)"] and leituras["(¬p) ∨ (q → r)"] and leituras["¬(p ∨ q) → r"])

# s3-p06: coluna F V V F
alvo = [F, V, V, F]
cand = {"p ∨ q": lambda p, q: p or q, "p ↔ q": bi, "p ⊕ q": xou,
        "¬(p ∧ q)": lambda p, q: not (p and q), "p → q": imp}
for k, f in cand.items():
    c = coluna(f, 2)
    dif = [i + 1 for i in range(4) if c[i] != alvo[i]]
    print("p06", k, [tv(x) for x in c], "difere nas linhas", dif)
checa("p06 so ⊕ bate", [k for k, f in cand.items() if coluna(f, 2) == alvo] == ["p ⊕ q"])

# s3-p07: q → p; ¬q → ¬p equivale a p → q
checa("p07 ¬q → ¬p ≡ p → q", equiv(lambda p, q: imp(not q, not p), imp, 2))
checa("p07 q → p difere de p → q", not equiv(lambda p, q: imp(q, p), imp, 2))

# s3-p08: codigo (conferido tambem pelo interpretador do site)
p, q, r = V, F, F
s3p08 = [p or (q and r), (p or q) and r, (not q) and r]
print("p08", [tv(x) for x in s3p08])
checa("p08 V F F", s3p08 == [V, F, F])
checa("p08 A: linha 2 sem parentese = V", (p or (q and r)) is V)
checa("p08 B: linha 1 da esquerda p/ direita = F", ((p or q) and r) is F)
checa("p08 C: nao estendido na linha 3 = V", (not (q and r)) is V)
troca = [p and (q or r), (p and q) or r, (not q) or r]
print("p08 E (e trocado por ou):", [tv(x) for x in troca])
checa("p08 E = F F V", troca == [F, F, V])

# s3-p09: (p ∨ q) → ¬r
f9 = lambda p, q, r: imp(p or q, not r)
c9 = coluna(f9, 3)
checa("p09 3 linhas F", c9.count(F) == 3)
checa("p09 5 linhas V", c9.count(V) == 5)
checa("p09 r = V em 4 linhas", sum(1 for l in linhas(3) if l[2]) == 4)
checa("p09 lendo ∨ como ∧: 1 F", coluna(lambda p, q, r: imp(p and q, not r), 3).count(F) == 1)
checa("p09 lendo ∨ como ⊕: 2 F", coluna(lambda p, q, r: imp(xou(p, q), not r), 3).count(F) == 2)
print("p09 tabela:")
for l in linhas(3):
    p, q, r = l
    print("   ", tv(p), tv(q), tv(r), "| p∨q", tv(p or q), "| ¬r", tv(not r), "|", tv(f9(p, q, r)))

# s3-p10: p → q F e q ∨ r V
sol = [l for l in linhas(3) if imp(l[0], l[1]) is F and (l[1] or l[2])]
print("p10 solucoes", [tuple(tv(x) for x in l) for l in sol])
checa("p10 unica (V, F, V)", sol == [(V, F, V)])

# s3-p11: (p ∧ q) → (r ∨ s)
alvo11 = lambda p, q, r, s: imp(p and q, r or s)
# p ∧ q → r ∨ s pela precedencia
certa11 = lambda p, q, r, s: imp((p and q), (r or s))
checa("p11 certa equivalente", equiv(alvo11, certa11, 4))
for nome, g in [("p ∧ (q → r ∨ s)", lambda p, q, r, s: p and imp(q, r or s)),
                ("(p ∨ q) → (r ∧ s)", lambda p, q, r, s: imp(p or q, r and s)),
                ("p ∧ q ↔ r ∨ s", lambda p, q, r, s: bi(p and q, r or s)),
                ("p ∧ q → r ∧ s", lambda p, q, r, s: imp(p and q, r and s))]:
    checa("p11 %s NAO equivalente" % nome, not equiv(alvo11, g, 4))
# contraexemplos citados nos erros
checa("p11 p=F: certa V, p ∧ (q → r ∨ s) F", alvo11(F, V, V, V) and not (F and imp(V, V)))
checa("p11 p=V,q=F,r=s=F: certa V, (p∨q)→(r∧s) F", alvo11(V, F, F, F) and not imp(V or F, F and F))
checa("p11 p=q=F, r=V: certa V, ↔ F", alvo11(F, F, V, F) and not bi(F and F, V or F))
checa("p11 p=q=r=V, s=F: certa V, r ∧ s F", alvo11(V, V, V, F) and not imp(V and V, V and F))

# s3-p12: coluna F V F V F V F F
f12 = {"(p ∨ q) → ¬r": lambda p, q, r: imp(p or q, not r),
       "(p ∨ q) ↔ ¬r": lambda p, q, r: bi(p or q, not r),
       "(p ∨ q) ∧ ¬r": lambda p, q, r: (p or q) and not r,
       "(p ⊕ q) ∧ ¬r": lambda p, q, r: xou(p, q) and not r,
       "p ∨ (q ∧ ¬r)": lambda p, q, r: p or (q and not r)}
alvo12 = coluna(f12["(p ∨ q) ∧ ¬r"], 3)
print("p12 coluna alvo", [tv(x) for x in alvo12])
rot = ["".join(tv(x) for x in l) for l in linhas(3)]
for k, f in f12.items():
    c = coluna(f, 3)
    print("p12", k, [tv(x) for x in c], "difere em", [rot[i] for i in range(8) if c[i] != alvo12[i]])
checa("p12 so a certa bate", [k for k, f in f12.items() if coluna(f, 3) == alvo12] == ["(p ∨ q) ∧ ¬r"])

print()
print("=== SEMANA 4 ===")
# s4-p01
f1 = {"(p ∧ q) → p": lambda p, q: imp(p and q, p),
      "p → (p ∧ q)": lambda p, q: imp(p, p and q),
      "(p ∨ q) → p": lambda p, q: imp(p or q, p),
      "p ∧ ¬p": lambda p, q: p and not p,
      "p ↔ q": bi}
for k, f in f1.items():
    print("p01", k, classe(f, 2), [tv(x) for x in coluna(f, 2)])
checa("p01 so (p ∧ q) → p e tautologia", [k for k, f in f1.items() if all(coluna(f, 2))] == ["(p ∧ q) → p"])

# s4-p02: ¬(p ∧ q)
neg = lambda p, q: not (p and q)
f2 = {"¬p ∧ ¬q": lambda p, q: (not p) and (not q), "¬p ∨ ¬q": lambda p, q: (not p) or (not q),
      "¬p ∨ q": lambda p, q: (not p) or q, "p ∧ ¬q": lambda p, q: p and not q, "¬p ∧ q": lambda p, q: (not p) and q}
checa("p02 so ¬p ∨ ¬q equivale", [k for k, f in f2.items() if equiv(neg, f, 2)] == ["¬p ∨ ¬q"])

# s4-p03: p → q
f3 = {"q → p (reciproca)": lambda p, q: imp(q, p), "¬p → ¬q (inversa)": lambda p, q: imp(not p, not q),
      "¬q → ¬p (contrapositiva)": lambda p, q: imp(not q, not p), "p ∧ ¬q": lambda p, q: p and not q,
      "p ∧ q": lambda p, q: p and q}
checa("p03 so a contrapositiva equivale", [k for k, f in f3.items() if equiv(imp, f, 2)] == ["¬q → ¬p (contrapositiva)"])
checa("p03 reciproca ≡ inversa", equiv(f3["q → p (reciproca)"], f3["¬p → ¬q (inversa)"], 2))

# quantificadores: forca bruta em dominios de 1 a 3 elementos, todas as escolhas de predicados
def mundos(npred, tam):
    for vals in itertools.product([V, F], repeat=npred * tam):
        yield [vals[i * npred:(i + 1) * npred] for i in range(tam)]

def equiv_q(f, g, npred):
    for tam in (1, 2, 3):
        for m in mundos(npred, tam):
            if f(m) != g(m): return False
    return True

# s4-p04: "Todo titulo vencido foi cobrado": ∀x (Ve(x) → C(x)); elemento = (Ve, C)
orig4 = lambda m: all(imp(ve, c) for ve, c in m)
neg4 = lambda m: not orig4(m)
f4 = {"Nenhum vencido foi cobrado": lambda m: all(not (ve and c) for ve, c in m),
      "Algum vencido nao foi cobrado": lambda m: any(ve and not c for ve, c in m),
      "Algum vencido foi cobrado": lambda m: any(ve and c for ve, c in m),
      "Todo nao vencido foi cobrado": lambda m: all(imp(not ve, c) for ve, c in m),
      "Algum nao vencido foi cobrado": lambda m: any((not ve) and c for ve, c in m)}
checa("p04 so 'algum vencido nao foi cobrado' e a negacao", [k for k, f in f4.items() if equiv_q(neg4, f, 2)] == ["Algum vencido nao foi cobrado"])
# contraexemplo do erro "nenhum": dois titulos vencidos, um cobrado e outro nao
m = [(V, V), (V, F)]
checa("p04 cenario: original F, 'nenhum' F tambem", orig4(m) is F and f4["Nenhum vencido foi cobrado"](m) is F)

# s4-p05: ¬(p → q)
n5 = lambda p, q: not imp(p, q)
f5 = {"p ∧ ¬q": lambda p, q: p and not q, "p → ¬q": lambda p, q: imp(p, not q),
      "¬p → ¬q": lambda p, q: imp(not p, not q), "¬p ∧ q": lambda p, q: (not p) and q,
      "¬p ∨ q": lambda p, q: (not p) or q}
checa("p05 so p ∧ ¬q e a negacao", [k for k, f in f5.items() if equiv(n5, f, 2)] == ["p ∧ ¬q"])
checa("p05 ¬p ∨ q e a propria original", equiv(imp, f5["¬p ∨ q"], 2))

# validade de argumento: nao existe linha com premissas V e conclusao F
def valido(premissas, conclusao, n):
    contra = [l for l in linhas(n) if all(pr(*l) for pr in premissas) and not conclusao(*l)]
    return len(contra) == 0, contra

# s4-p06: p = "chove", q = "a rua molha", r = "o transito para"
args6 = {
    "afirmar o consequente": ([imp, lambda p, q: q], lambda p, q: p, 2),
    "negar o antecedente": ([imp, lambda p, q: not p], lambda p, q: not q, 2),
    "modus tollens": ([imp, lambda p, q: not q], lambda p, q: not p, 2),
    "disjuntivo mal aplicado": ([lambda p, q: p or q, lambda p, q: p], lambda p, q: not q, 2),
    "hipotetico invertido": ([lambda p, q, r: imp(p, q), lambda p, q, r: imp(q, r)], lambda p, q, r: imp(r, p), 3),
}
for k, (prem, conc, n) in args6.items():
    vld, contra = valido(prem, conc, n)
    print("p06", k, "valido" if vld else "invalido, contraexemplo " + str([tuple(tv(x) for x in c) for c in contra]))
checa("p06 so modus tollens valido", [k for k, a in args6.items() if valido(*a)[0]] == ["modus tollens"])
checa("p06 silogismo hipotetico direito e valido", valido([lambda p, q, r: imp(p, q), lambda p, q, r: imp(q, r)], lambda p, q, r: imp(p, r), 3)[0])
checa("p06 modus ponens valido", valido([imp, lambda p, q: p], lambda p, q: q, 2)[0])
checa("p06 disjuntivo certo valido", valido([lambda p, q: p or q, lambda p, q: not p], lambda p, q: q, 2)[0])

# s4-p07: "Nenhum lancamento sem documento foi aprovado"; elemento = (D, A)
orig7 = lambda m: not any((not d) and a for d, a in m)
f7 = {"∃x (¬D ∧ ¬A)": lambda m: any((not d) and (not a) for d, a in m),
      "∀x (¬D ∧ ¬A)": lambda m: all((not d) and (not a) for d, a in m),
      "∀x (D → A)": lambda m: all(imp(d, a) for d, a in m),
      "∀x (¬D → ¬A)": lambda m: all(imp(not d, not a) for d, a in m),
      "¬∃x (¬D ∧ ¬A)": lambda m: not any((not d) and (not a) for d, a in m)}
checa("p07 so ∀x (¬D → ¬A) traduz", [k for k, f in f7.items() if equiv_q(orig7, f, 2)] == ["∀x (¬D → ¬A)"])
checa("p07 ¬∃x(¬D ∧ ¬A) ≡ ∀x(¬D → A)", equiv_q(f7["¬∃x (¬D ∧ ¬A)"], lambda m: all(imp(not d, a) for d, a in m), 2))
# cenarios citados nos erros
m1 = [(V, V), (F, F)]   # um com documento aprovado, um sem documento nao aprovado
checa("p07 cenario m1: regra V, ∀x(¬D ∧ ¬A) F", orig7(m1) and not f7["∀x (¬D ∧ ¬A)"](m1))
m2 = [(F, F), (F, V)]   # dois sem documento, um aprovado
checa("p07 cenario m2: regra F, ∃x(¬D ∧ ¬A) V", (not orig7(m2)) and f7["∃x (¬D ∧ ¬A)"](m2))
m3 = [(V, F)]           # com documento e nao aprovado
checa("p07 cenario m3: regra V, ∀x(D → A) F", orig7(m3) and not f7["∀x (D → A)"](m3))
m4 = [(F, F)]           # sem documento e nao aprovado
checa("p07 cenario m4: regra V, ¬∃x(¬D ∧ ¬A) F", orig7(m4) and not f7["¬∃x (¬D ∧ ¬A)"](m4))

# s4-p08: codigo De Morgan com pago = V, emitida = F
pg, em = V, F
s4p08 = [not (pg and em), (not pg) and (not em), (not pg) or (not em)]
print("p08", [tv(x) for x in s4p08])
checa("p08 V F V", s4p08 == [V, F, V])
checa("p08 B: (nao pago) e emitida = F", ((not pg) and em) is F)
checa("p08 D: nao (pago ou nao emitida) = F", (not (pg or (not em))) is F)
tr = [not (pg or em), (not pg) or (not em), (not pg) and (not em)]
print("p08 E (e trocado por ou):", [tv(x) for x in tr])
checa("p08 E = F V F", tr == [F, V, F])
checa("p08 linhas 1 e 3 sempre iguais", equiv(lambda a, b: not (a and b), lambda a, b: (not a) or (not b), 2))

# s4-p09: p ∨ q, p → r, logo r
prem9 = [lambda p, q, r: p or q, lambda p, q, r: imp(p, r)]
conc9 = lambda p, q, r: r
vld, contra = valido(prem9, conc9, 3)
print("p09 contraexemplos", [tuple(tv(x) for x in c) for c in contra])
checa("p09 unico contraexemplo (F, V, F)", contra == [(F, V, F)])
for l in [(V, V, F), (F, F, F), (F, V, V)]:
    p, q, r = l
    print("   p09 linha", tuple(tv(x) for x in l), "p∨q", tv(p or q), "p→r", tv(imp(p, r)), "r", tv(r))
print("p09 tabela:")
for l in linhas(3):
    p, q, r = l
    print("   ", tv(p), tv(q), tv(r), "| p∨q", tv(p or q), "| p→r", tv(imp(p, r)), "| r", tv(r))

# s4-p10: L → D, D → C, L ∨ X, ¬X
mod10 = [l for l in linhas(4) if imp(l[0], l[1]) and imp(l[1], l[2]) and (l[0] or l[3]) and not l[3]]
print("p10 modelos (L, D, C, X)", [tuple(tv(x) for x in l) for l in mod10])
checa("p10 unico modelo L=V, D=V, C=V, X=F", mod10 == [(V, V, V, F)])
# com ou exclusivo na premissa 3, o resultado e o mesmo
mod10x = [l for l in linhas(4) if imp(l[0], l[1]) and imp(l[1], l[2]) and xou(l[0], l[3]) and not l[3]]
checa("p10 com ⊕ tambem L = V e C = V", mod10x == [(V, V, V, F)])

# s4-p11: ¬(p ∧ ¬q)
n11 = lambda p, q: not (p and not q)
f11 = {"p → q": imp, "¬p ∧ q": lambda p, q: (not p) and q, "¬p ∨ ¬q": lambda p, q: (not p) or (not q),
       "q → p": lambda p, q: imp(q, p), "p ∧ q": lambda p, q: p and q}
checa("p11 so p → q equivale", [k for k, f in f11.items() if equiv(n11, f, 2)] == ["p → q"])
print("p11 colunas")
for k, f in [("¬(p ∧ ¬q)", n11)] + list(f11.items()):
    print("   ", k, [tv(x) for x in coluna(f, 2)])

# s4-p12: ¬∃x (P ∧ N); elemento = (P, N)
n12 = lambda m: not any(pp and nn for pp, nn in m)
f12b = {"∃x (¬P ∨ ¬N)": lambda m: any((not pp) or (not nn) for pp, nn in m),
        "∀x (¬P ∧ ¬N)": lambda m: all((not pp) and (not nn) for pp, nn in m),
        "∀x (P → ¬N)": lambda m: all(imp(pp, not nn) for pp, nn in m),
        "∀x (¬P → ¬N)": lambda m: all(imp(not pp, not nn) for pp, nn in m),
        "∃x (P ∧ ¬N)": lambda m: any(pp and not nn for pp, nn in m)}
checa("p12 so ∀x (P → ¬N) e a negacao", [k for k, f in f12b.items() if equiv_q(n12, f, 2)] == ["∀x (P → ¬N)"])
# cenarios citados nos erros
mA = [(V, V), (F, F)]
checa("p12 cenario A: negacao F, ∃x(¬P ∨ ¬N) V", (not n12(mA)) and f12b["∃x (¬P ∨ ¬N)"](mA))
mB = [(V, F)]
checa("p12 cenario B: negacao V, ∀x(¬P ∧ ¬N) F", n12(mB) and not f12b["∀x (¬P ∧ ¬N)"](mB))
mD = [(F, V)]
checa("p12 cenario D: negacao V, ∀x(¬P → ¬N) F", n12(mD) and not f12b["∀x (¬P → ¬N)"](mD))
mE = [(V, V), (V, F)]
checa("p12 cenario E: negacao F, ∃x(P ∧ ¬N) V", (not n12(mE)) and f12b["∃x (P ∧ ¬N)"](mE))

print()
print("TUDO OK" if ok else "HA FALHAS")
