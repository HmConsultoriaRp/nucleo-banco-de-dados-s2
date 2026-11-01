# Revisor: simula os dois codigos VisuAlg do lote lp_s34 (s3-p08 e s4-p08).
# 1) mini avaliador lendo as linhas do proprio JSON (nao > e > ou, parenteses primeiro);
# 2) programa Python equivalente escrito a mao;
# 3) reproduz a saida que cada distrator alega.
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
Q = {}
for f in sorted(os.listdir(DADOS)):
    if f.startswith("lp_s34_p") and f.endswith(".json"):
        for q in json.load(open(os.path.join(DADOS, f), encoding="utf-8"))["questoes"]:
            Q[q["id"]] = q

falhas = []
def checa(nome, cond):
    print(("ok    " if cond else "FALHA ") + nome)
    if not cond: falhas.append(nome)

def tok(s):
    return re.findall(r"\(|\)|[a-z_]+", s.lower())

def avalia(expr, amb, troca_e_ou=False):
    t = tok(expr); i = [0]
    # troca_e_ou: mesma estrutura, mas o `e` passa a agir como ou e vice-versa
    E, OU = "e", "ou"
    def pk(): return t[i[0]] if i[0] < len(t) else None
    def prim():
        k = pk()
        if k == "nao":
            i[0] += 1; return not prim()
        if k == "(":
            i[0] += 1; v = disj(); assert pk() == ")"; i[0] += 1; return v
        i[0] += 1
        if k == "verdadeiro": return True
        if k == "falso": return False
        return amb[k]
    def conj():
        v = prim()
        while pk() == E:
            i[0] += 1; w = prim()
            v = (v and w) if not troca_e_ou else (v or w)
        return v
    def disj():
        v = conj()
        while pk() in (OU, "xou"):
            op = pk(); i[0] += 1; w = conj()
            if op == "xou": v = v != w
            elif not troca_e_ou: v = v or w
            else: v = v and w
        return v
    r = disj(); assert i[0] == len(t), expr
    return r

def roda(codigo, troca_e_ou=False, amb_extra=None):
    amb, out = {}, []
    for l in codigo.split("\n"):
        l = l.strip()
        m = re.fullmatch(r"([a-z_]+)\s*<-\s*(verdadeiro|falso)", l)
        if m:
            amb[m.group(1)] = m.group(2) == "verdadeiro"; continue
        m = re.fullmatch(r"escreval\((.*)\)", l)
        if m:
            if amb_extra: amb.update(amb_extra)
            out.append("VERDADEIRO" if avalia(m.group(1), amb, troca_e_ou) else "FALSO")
    return out

def fmt(b): return "VERDADEIRO" if b else "FALSO"

# ---------- s3-p08 ----------
q = Q["lp-s3-p08"]
print(q["codigo"])
saida = roda(q["codigo"])
checa(f"s3-p08 mini avaliador = saida do JSON ({saida})", "\n".join(saida) == q["saida"])
p, qq, r = True, False, False
py = [fmt(p or (qq and r)), fmt((p or qq) and r), fmt((not qq) and r)]
checa(f"s3-p08 Python equivalente ({py})", "\n".join(py) == q["saida"])
certa = [a for a in q["alternativas"] if a["certa"]][0]["t"]
checa("s3-p08 alternativa certa = saída", certa.split(", ") == saida)
# distratores
A = [fmt(p or (qq and r)), fmt(p or (qq and r)), fmt((not qq) and r)]
B = [fmt((p or qq) and r), fmt((p or qq) and r), fmt((not qq) and r)]
C = [fmt(p or (qq and r)), fmt((p or qq) and r), fmt(not (qq and r))]
Etr = roda(q["codigo"], troca_e_ou=True)
for letra, calc in zip("ABCE", [A, B, C, Etr]):
    t = q["alternativas"]["ABCDE".index(letra)]["t"]
    checa(f"s3-p08 distrator {letra} '{t}' reproduzido ({calc})", t.split(", ") == calc and calc != saida)
# confira: r = VERDADEIRO
r2 = roda(q["codigo"], amb_extra={"r": True})
checa(f"s3-p08 confira com r V: linhas 2 e 3 VERDADEIRO ({r2})", r2[1] == "VERDADEIRO" and r2[2] == "VERDADEIRO")
# leitura errada com r V tambem da V (o teste so serve se o aluno ve a MUDANCA)
checa("s3-p08 confira: leitura errada nao(q e r) com r V também dá V", (not (False and True)) is True)

# ---------- s4-p08 ----------
q = Q["lp-s4-p08"]
print(q["codigo"])
saida = roda(q["codigo"])
checa(f"s4-p08 mini avaliador = saida do JSON ({saida})", "\n".join(saida) == q["saida"])
pg, em = True, False
py = [fmt(not (pg and em)), fmt((not pg) and (not em)), fmt((not pg) or (not em))]
checa(f"s4-p08 Python equivalente ({py})", "\n".join(py) == q["saida"])
certa = [a for a in q["alternativas"] if a["certa"]][0]["t"]
checa("s4-p08 alternativa certa = saída", certa.split(", ") == saida)
A = [fmt(not (pg and em))] * 2 + [fmt((not pg) or (not em))]
B = [fmt((not pg) and em), fmt((not pg) and (not em)), fmt((not pg) or (not em))]
D = [fmt(not (pg and em)), fmt((not pg) and (not em)), fmt(not (pg or (not em)))]
Etr = roda(q["codigo"], troca_e_ou=True)
for letra, calc in zip("ABDE", [A, B, D, Etr]):
    t = q["alternativas"]["ABCDE".index(letra)]["t"]
    checa(f"s4-p08 distrator {letra} '{t}' reproduzido ({calc})", t.split(", ") == calc and calc != saida)
# confira: os 4 casos
for a_, b_, esp in [(True, True, ["FALSO"] * 3), (False, False, ["VERDADEIRO"] * 3), (False, True, ["VERDADEIRO", "FALSO", "VERDADEIRO"])]:
    calc = roda(q["codigo"], amb_extra={"pago": a_, "emitida": b_})
    checa(f"s4-p08 confira pago={a_} emitida={b_}: {calc}", calc == esp and calc[0] == calc[2])

print()
print("FALHAS:", len(falhas))
for f_ in falhas: print("  -", f_)
