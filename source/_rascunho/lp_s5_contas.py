# Confere as contas do lote lp_s5 (Logica, semana 5, previa).
# Uso: python -I lp_s5_contas.py
# Cada programa VisuAlg foi reescrito aqui em Python; cada alternativa errada tem a conta que o
# campo "erro" descreve, e o script confere que essa conta da mesmo o texto da alternativa.
import json, os, sys, math, itertools

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

falhas = []
def ok(cond, msg):
    if not cond:
        falhas.append(msg)

qs = {}
for nome in ("lp_s5_p1.json", "lp_s5_p2.json"):
    p = os.path.join(DADOS, nome)
    bruto = open(p, "rb").read()
    ctrl = [b for b in bruto if b < 32 and b not in (9, 10, 13)]
    ok(not ctrl, f"{nome}: bytes de controle {ctrl[:5]}")
    d = json.loads(bruto.decode("utf-8"))
    for q in d["questoes"]:
        qs[q["id"]] = q

def alts(qid):
    return {a["t"]: a for a in qs[qid]["alternativas"]}

def certa(qid):
    return [a["t"] for a in qs[qid]["alternativas"] if a.get("certa")][0]

def vtxt(b):
    return "VERDADEIRO" if b else "FALSO"

def trunc_div(a, b):
    return int(a / b)  # div do VisuAlg corta as casas

def real_fmt(x):
    return str(int(x)) if float(x).is_integer() else repr(round(x, 10)).rstrip("0").rstrip(".")

# ---------- p01: sem conta (propriedades) ----------
ok(certa("lp-s5-p01") == "Definição (sem ambiguidade)", "p01 certa")

# ---------- p02: atribuicao em sequencia ----------
a, b = 8, 5
a = a + b; b = a - b; a = a - b
s = f"{a} {b}"
ok(qs["lp-s5-p02"]["saida"] == s == certa("lp-s5-p02"), f"p02 saida {s}")
A = alts("lp-s5-p02")
# 13 8: parou antes da ultima linha
a, b = 8, 5; a = a + b; b = a - b
ok(f"{a} {b}" == "13 8" and "13 8" in A, "p02 13 8")
ok("8 5" in A, "p02 8 5 (valores iniciais)")
# 8 8: ultima linha com b antigo (5)
a, b = 8, 5; a = a + b; b_novo = a - b; a = a - 5; b = b_novo
ok(f"{a} {b}" == "8 8", f"p02 8 8 -> {a} {b}")
# 10 3: linha do b com a antigo (8)
a, b = 8, 5; a_ant = a; a = a + b; b = a_ant - b; a = a - b
ok(f"{a} {b}" == "10 3", f"p02 10 3 -> {a} {b}")
# confira: a=2, b=7 vira 7 2
a, b = 2, 7; a = a + b; b = a - b; a = a - b
ok((a, b) == (7, 2), "p02 confira 2,7")
# atalho: b final 8 elimina '8 5' e '10 3'; a final 5 elimina '13 8' e '8 8'
restam = [t for t in A if t.split()[1] == "8" and t.split()[0] == "5"]
ok(restam == ["5 8"], f"p02 atalho {restam}")

# ---------- p03: identificadores ----------
import re
regra = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
validos = [t.strip("`") for t in alts("lp-s5-p03") if regra.match(t.strip("`"))]
ok(validos == ["saldo2"], f"p03 validos {validos}")

# ---------- p04: div e mod ----------
n = 47
q, r = trunc_div(n, 5), n % 5
ok(f"{q} {r}" == qs["lp-s5-p04"]["saida"] == certa("lp-s5-p04"), "p04 saida")
A = alts("lp-s5-p04")
ok(f"{r} {q}" == "2 9" and "2 9" in A, "p04 2 9")
ok(f"{n / 5} {r}" == "9.4 2" and "9.4 2" in A, "p04 9.4 2")
ok(round((n / 5 - q) * 10) == 4 and "9 4" in A, "p04 9 4")
ok(5 * q + 4 == 49 and 47 - 45 == 2 and round(2 / 5, 1) == 0.4, "p04 conversa/erro")
ok(f"{q * 5} {r}" == "45 2" and "45 2" in A, "p04 45 2")
ok(5 * 2 + 9 == 19, "p04 confira 19")

# ---------- p05: fluxograma -> se/senao ----------
def certo(v):
    return 20 if v > 1000 else 5
def ramos_trocados(v):
    return 5 if v > 1000 else 20
def sem_senao(v):
    t = 0
    if v > 1000:
        t = 20
    t = 5
    return t
ok((certo(2000), certo(300)) == (20, 5), "p05 certo")
ok((ramos_trocados(2000), ramos_trocados(300)) == (5, 20), "p05 trocados")
ok((sem_senao(2000), sem_senao(300)) == (5, 5), "p05 sem senao")
ok(certa("lp-s5-p05").startswith("`se valor > 1000 entao`\n`taxa <- 20`\n`senao`"), "p05 certa")

# ---------- p06: precedencia aritmetica ----------
x = 50 - 4 * 2 ** 3 + 23 % 6
ok(str(x) == qs["lp-s5-p06"]["saida"] == certa("lp-s5-p06") == "23", f"p06 {x}")
ok(50 - (32 + 5) == 13, "p06 13")
ok((50 - 32 + 23) % 6 == 5 and 50 - 32 + 23 == 41, "p06 5")
ok(23 // 6 == 3 and 50 - 32 + 3 == 21, "p06 21")
ok(50 - 4 * (2 * 3) + 5 == 31 and 4 * 6 == 24, "p06 31")
ok(set(alts("lp-s5-p06")) == {"13", "5", "21", "23", "31"}, "p06 alternativas")
ok(50 - 4 * 2 ** 3 + 23 % 6 == 50 - (4 * (2 ** 3)) + (23 % 6), "p06 confira")

# ---------- p07: media sem parenteses (entradas 4 e 5) ----------
n1, n2 = map(float, qs["lp-s5-p07"]["entradas"])
media = n1 + n2 / 2
saida = ("Aprovado " if media >= 6 else "Recuperação ") + real_fmt(media)
ok(saida == qs["lp-s5-p07"]["saida"] == certa("lp-s5-p07") == "Aprovado 6.5", f"p07 {saida}")
A = alts("lp-s5-p07")
m_certa = (n1 + n2) / 2
ok("Recuperação " + real_fmt(m_certa) == "Recuperação 4.5" and "Recuperação 4.5" in A, "p07 4.5")
m_int = n1 + trunc_div(int(n2), 2)
ok("Aprovado " + real_fmt(m_int) == "Aprovado 6" and "Aprovado 6" in A, "p07 6")
ok("Recuperação 6.5" in A and media >= 6, "p07 ramo trocado")
ok("Aprovado media" in A, "p07 literal")

# ---------- p08: escolha com conta (entrada 6) ----------
def trimestre(mes):
    t = trunc_div(mes - 1, 3)
    return {0: "T1", 1: "T2", 2: "T3", 3: "T4"}.get(t, "Mês inválido")
mes = int(qs["lp-s5-p08"]["entradas"][0])
ok(trimestre(mes) == qs["lp-s5-p08"]["saida"] == certa("lp-s5-p08") == "T2", "p08 saida")
A = alts("lp-s5-p08")
ok({0: "T1", 1: "T2", 2: "T3", 3: "T4"}[round((mes - 1) / 3)] == "T3" and "T3" in A, "p08 arredondou")
ok(round(5 / 3, 2) == 1.67, "p08 1,67")
ok("T1" in A and trunc_div(mes - 1, 3) == 1, "p08 rotulo")
ok(mes not in (0, 1, 2, 3) and "Mês inválido" in A, "p08 comparou o mes")
ok("T2 e Mês inválido" in A, "p08 outrocaso")
ok(trimestre(3) == "T1" and trimestre(4) == "T2" and trimestre(13) == "Mês inválido" and trimestre(0) == "T1", "p08 confira")
ok(trunc_div(2, 3) == 0 and trunc_div(3, 3) == 1 and trunc_div(12, 3) == 4 and trunc_div(-1, 3) == 0, "p08 confira contas")

# ---------- p09: e, ou, nao ----------
x, y = 4, 9
A1, B1, C1 = x > 5, y > 5, (x % 2 == 1)
p = (not A1) or (B1 and C1)
q = not (A1 or B1)
s = f"{vtxt(p)} {vtxt(q)}"
ok(s == qs["lp-s5-p09"]["saida"] == certa("lp-s5-p09") == "VERDADEIRO FALSO", f"p09 {s}")
A = alts("lp-s5-p09")
p_esq = ((not A1) or B1) and C1          # ou antes do e
q_meia = (not A1) or (not B1)             # De Morgan pela metade
ok(f"{vtxt(p_esq)} {vtxt(q)}" == "FALSO FALSO" and "FALSO FALSO" in A, "p09 FF")
ok(f"{vtxt(p)} {vtxt(q_meia)}" == "VERDADEIRO VERDADEIRO" and "VERDADEIRO VERDADEIRO" in A, "p09 VV")
ok(f"{vtxt(p_esq)} {vtxt(q_meia)}" == "FALSO VERDADEIRO" and "FALSO VERDADEIRO" in A, "p09 FV")
ok(x % 2 == 0 and (0 == 1) is False, "p09 mod antes do =")
ok(q == ((not A1) and (not B1)), "p09 De Morgan completa")

# ---------- p10: separar e inverter digitos (entrada 583) ----------
n = int(qs["lp-s5-p10"]["entradas"][0])
c, d, u = trunc_div(n, 100), trunc_div(n % 100, 10), n % 10
inv = u * 100 + d * 10 + c
s = f"{inv} {c + d + u}"
ok(s == qs["lp-s5-p10"]["saida"] == certa("lp-s5-p10") == "385 16", f"p10 {s}")
A = alts("lp-s5-p10")
ok(f"{c * 100 + d * 10 + u} {c + d + u}" == "583 16" and "583 16" in A, "p10 ordem original")
d83 = n % 100
ok(f"{u * 100 + d83 * 10 + c} {c + d83 + u}" == "1135 91" and "1135 91" in A, "p10 d = 83")
ok(f"{inv} {c}{d}{u}" == "385 583" and "385 583" in A, "p10 texto")
c6 = round(n / 100)
ok(c6 == 6 and f"{u * 100 + d * 10 + c6} {c6 + d + u}" == "386 17" and "386 17" in A, "p10 arredondou")
n = 100
c, d, u = trunc_div(n, 100), trunc_div(n % 100, 10), n % 10
ok((u * 100 + d * 10 + c, c + d + u) == (1, 1), "p10 confira 100")
# atalho: soma 16 deixa so duas
ok(sorted(t for t in A if t.split()[1] == "16") == ["385 16", "583 16"], "p10 atalho")

# ---------- p11: se aninhado (entradas 18 e 3000) ----------
def etapas(idade, renda, ge_dentro=False, gt_fora=False, d_no_b=False, f_no_senao=False):
    out = ""
    cond_fora = idade > 18 if gt_fora else idade >= 18
    if cond_fora:
        out += "A"
        cond_dentro = renda >= 3000 if ge_dentro else renda > 3000
        if cond_dentro:
            out += "B"
            if d_no_b:
                out += "D"
        else:
            out += "C"
        if not d_no_b:
            out += "D"
    else:
        out += "E"
        if f_no_senao:
            out += "F"
    if not f_no_senao:
        out += "F"
    return out
idade, renda = map(int, qs["lp-s5-p11"]["entradas"])
ok(etapas(idade, renda) == qs["lp-s5-p11"]["saida"] == certa("lp-s5-p11") == "ACDF", "p11 saida")
A = alts("lp-s5-p11")
ok(etapas(idade, renda, ge_dentro=True) == "ABDF" and "ABDF" in A, "p11 ABDF")
ok(etapas(idade, renda, gt_fora=True) == "EF" and "EF" in A, "p11 EF")
ok(etapas(idade, renda, d_no_b=True) == "ACF" and "ACF" in A, "p11 ACF")
ok(etapas(idade, renda, f_no_senao=True) == "ACD" and "ACD" in A, "p11 ACD")
ok(etapas(17, 3000) == "EF" and etapas(18, 3001) == "ABDF", "p11 confira")

# ---------- p12: condicao composta + tabela ----------
def regra(v, vip, dist):
    return v >= 200 or (vip and dist <= 50)
cond = {
    "A": lambda v, vip, dist: (v > 200) or (vip and dist <= 50),
    "B": lambda v, vip, dist: (v >= 200 or vip) and dist <= 50,
    "C": lambda v, vip, dist: (v >= 200 and vip) or dist <= 50,
    "D": lambda v, vip, dist: (v >= 200) or (vip and dist <= 50),
    "E": lambda v, vip, dist: (v >= 200) or (vip and dist >= 50),
}
ok(certa("lp-s5-p12") == qs["lp-s5-p12"]["alternativas"][3]["t"], "p12 certa na D")
# D equivale a regra em todo o reticulado; cada errada difere em algum ponto
grade = list(itertools.product([100, 199, 200, 201, 300], [False, True], [20, 30, 49, 50, 51, 80]))
ok(all(cond["D"](*g) == regra(*g) for g in grade), "p12 D == regra")
for k in "ABCE":
    ok(any(cond[k](*g) != regra(*g) for g in grade), f"p12 {k} deveria diferir")
casos = [(300, False, 80), (200, False, 80), (100, True, 50), (100, True, 80), (100, False, 30)]
VF = lambda b: "V" if b else "F"
esperado = []
for i, (v, vip, dist) in enumerate(casos, 1):
    esperado.append([str(i), str(v), VF(vip), str(dist), VF(regra(v, vip, dist))] + [VF(cond[k](v, vip, dist)) for k in "ABCDE"])
ok(qs["lp-s5-p12"]["tabela"]["linhas"] == esperado, f"p12 tabela difere:\n{esperado}")
erra = {k: [i for i, cs in enumerate(casos, 1) if cond[k](*cs) != regra(*cs)] for k in "ABCDE"}
ok(erra == {"A": [2], "B": [1, 2], "C": [1, 2, 5], "D": [], "E": [4]}, f"p12 confira {erra}")
# erros citados nas alternativas
ok(cond["B"](300, False, 80) is False and regra(300, False, 80), "p12 B 300/80")
ok(cond["C"](100, False, 30) is True and cond["C"](300, False, 80) is False, "p12 C 30 km e 300/80")
ok(cond["E"](100, True, 20) is False and cond["E"](100, True, 80) is True, "p12 E 20 e 80 km")
ok(cond["A"](200, False, 80) is False, "p12 A 200")

# ---------- conjunto ----------
todas = list(qs.values())
ok(len(todas) == 12, "12 questoes")
ok(sorted(qs) == [f"lp-s5-p{i:02d}" for i in range(1, 13)], "ids p01..p12")
niveis = [q["nivel"] for q in todas]
ok(all(niveis.count(n) == 4 for n in (1, 2, 3)), f"niveis {niveis}")
com_codigo = [q["id"] for q in todas if q.get("codigo")]
com_entrada = [q["id"] for q in todas if q.get("entradas")]
ok(len(com_codigo) >= 7, f"codigo {len(com_codigo)}")
ok(len(com_entrada) >= 3, f"entradas {len(com_entrada)}")
ok(all(q["origem"] == "Prévia · ementa" for q in todas), "origem")
pos = [ "ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in todas]
ok(max(pos.count(l) for l in "ABCDE") / 12 <= 0.30, f"posicoes {pos}")

sys.stdout.reconfigure(encoding="utf-8")
print("questões com código:", len(com_codigo), com_codigo)
print("questões com entradas:", len(com_entrada), com_entrada)
print("posições das certas:", "".join(pos), {l: pos.count(l) for l in "ABCDE"})
if falhas:
    print("FALHAS:")
    for f in falhas:
        print(" -", f)
    sys.exit(1)
print("todas as contas conferem")
