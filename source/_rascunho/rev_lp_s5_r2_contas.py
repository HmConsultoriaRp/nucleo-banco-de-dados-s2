# Revisao adversarial, segunda rodada, do lote lp_s5 (Logica, semana 5, previa).
# Uso: python -I rev_lp_s5_r2_contas.py
# Resolve cada questao do zero, com programas Python equivalentes escritos a mao,
# sem usar o campo "resposta" nem o campo "saida" como ponto de partida.
# Depois compara: alternativa marcada como certa, campo saida, contas de cada "erro"
# e numeros citados nos jeitos. Conta exata com Fraction.
import json, os, sys, re, itertools
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

falhas, notas = [], []
def ok(cond, msg):
    if not cond:
        falhas.append(msg)

qs, semanas = {}, []
for nome in sorted(os.listdir(DADOS)):
    if re.fullmatch(r"lp_s5_p\d+\.json", nome):
        bruto = open(os.path.join(DADOS, nome), "rb").read()
        ctrl = [b for b in bruto if b < 32 and b not in (10, 13)]
        ok(not ctrl, f"{nome}: bytes de controle {ctrl[:5]}")
        d = json.loads(bruto.decode("utf-8"))
        ok(d["disciplina"] == "lp", f"{nome}: disciplina")
        semanas += d.get("semanas", [])
        for q in d["questoes"]:
            ok(q["id"] not in qs, f"id repetido {q['id']}")
            qs[q["id"]] = q

L = "ABCDE"
def alts(qid): return qs[qid]["alternativas"]
def t(qid, letra): return alts(qid)[L.index(letra)]["t"]
def certa(qid):
    c = [i for i, a in enumerate(alts(qid)) if a.get("certa") is True]
    ok(len(c) == 1, f"{qid}: {len(c)} certas")
    return L[c[0]]
def norm(s): return re.sub(r"\s+", " ", s).strip()
def todos_textos(q):
    j = q["jeitos"]
    out = [q["enunciado"], q["dica"], q["resposta"]]
    out += [a["t"] for a in q["alternativas"]] + [a.get("erro", "") for a in q["alternativas"]]
    for k, v in j.items():
        if isinstance(v, str): out.append(v)
        elif k == "receita": out += v
        else: out += [c["fala"] for c in v]
    return out

# VisuAlg: div corta as casas (para zero), mod com sinal do dividendo
def vdiv(a, b):
    q = F(a) / F(b)
    return int(q)  # int() de Fraction trunca para zero
def vmod(a, b): return a - b * vdiv(a, b)
def vnum(x):
    x = F(x)
    if x.denominator == 1: return str(x.numerator)
    return format(float(x), ".10f").rstrip("0")
def vlog(b): return "VERDADEIRO" if b else "FALSO"

# --------------------------- p01 ---------------------------
# Conceitual: o unico passo sem criterio e "bom pagador" -> fere a definicao.
ok(certa("lp-s5-p01") == "C" and t("lp-s5-p01", "C").startswith("Definição"), "p01 certa")
ok(sorted(t("lp-s5-p01", x).split(" (")[0] for x in L) ==
   sorted(["Finitude", "Entrada", "Definição", "Saída", "Efetividade"]), "p01 cinco propriedades")

# --------------------------- p02 ---------------------------
def p02(a, b):
    a = a + b; b = a - b; a = a - b
    return f"{a} {b}"
r = p02(8, 5)
ok("a <- 8" in qs["lp-s5-p02"]["codigo"] and "b <- 5" in qs["lp-s5-p02"]["codigo"], "p02 codigo")
ok(r == "5 8" == norm(qs["lp-s5-p02"]["saida"]) == t("lp-s5-p02", certa("lp-s5-p02")), f"p02 {r}")
a, b = 8, 5; a = a + b; b = a - b                      # parou antes da ultima
ok(f"{a} {b}" == t("lp-s5-p02", "B") == "13 8", "p02 B")
ok(t("lp-s5-p02", "C") == "8 5", "p02 C")
a, b = 8, 5; a = a + b; b_novo = a - b; a = a - 5       # ultima linha com b antigo
ok(f"{a} {b_novo}" == t("lp-s5-p02", "D") == "8 8", "p02 D")
a, b = 8, 5; b = 8 - b; a = 13 - b                      # linha do b com a antigo
ok(f"{a} {b}" == t("lp-s5-p02", "E") == "10 3", "p02 E")
ok(p02(2, 7) == "7 2" and 2 + 7 == 9 and 9 - 7 == 2 and 9 - 2 == 7, "p02 confira")

# --------------------------- p03 ---------------------------
ident = re.compile(r"[A-Za-z][A-Za-z0-9]*")
val = [x for x in L if ident.fullmatch(t("lp-s5-p03", x).strip("`"))]
ok(val == [certa("lp-s5-p03")] == ["D"], f"p03 {val}")

# --------------------------- p04 ---------------------------
q4, r4 = vdiv(47, 5), vmod(47, 5)
ok(f"{q4} {r4}" == "9 2" == norm(qs["lp-s5-p04"]["saida"]) == t("lp-s5-p04", certa("lp-s5-p04")), "p04")
ok(t("lp-s5-p04", "A") == f"{r4} {q4}", "p04 A")
ok(t("lp-s5-p04", "C") == f"{vnum(F(47, 5))} {r4}", "p04 C")
ok(t("lp-s5-p04", "D") == "9 4" and F(47, 5) - 9 == F(2, 5) == F(4, 10), "p04 D")
ok(t("lp-s5-p04", "E") == f"{5 * q4} {r4}", "p04 E")
ok(5 * 9 + 4 == 49 and 5 * 2 + 9 == 19 and F(4, 10) * 5 == 2, "p04 confira/erro")
ok(vdiv(47, 7) == 6 and vmod(47, 7) == 5, "p04 trabalho 47 dias")
ok([5 * k for k in range(1, 10)][-1] == 45 and 47 - 45 == 2, "p04 visual saltos")

# --------------------------- p05 ---------------------------
def fluxo(v): return 20 if v > 1000 else 5
def a5A(v): return 5 if v > 1000 else 20
def a5B(v):
    taxa = 20 if v > 1000 else None
    taxa = 5
    return taxa
def a5C(v, limite=100000):
    voltas = 0
    while v > 1000:
        voltas += 1
        if voltas > limite: return "nao termina"
    return 5
ok((fluxo(2000), fluxo(300)) == (20, 5), "p05 fluxo")
ok((a5A(2000), a5A(300)) == (5, 20), "p05 A")
ok((a5B(2000), a5B(300)) == (5, 5), "p05 B")
ok(a5C(2000) == "nao termina" and a5C(300) == 5, "p05 C")
ok(certa("lp-s5-p05") == "E", "p05 certa")
ok("taxa <- 20`\n`senao`\n`taxa <- 5" in t("lp-s5-p05", "E"), "p05 E texto")

# --------------------------- p06 ---------------------------
x = 50 - 4 * 2 ** 3 + vmod(23, 6)
ok(x == 23 and norm(qs["lp-s5-p06"]["saida"]) == "23" == t("lp-s5-p06", certa("lp-s5-p06")), f"p06 {x}")
ok(str(50 - (32 + 5)) == t("lp-s5-p06", "A") == "13", "p06 A")
ok(str(vmod(50 - 32 + 23, 6)) == t("lp-s5-p06", "B") == "5" and 50 - 32 + 23 == 41, "p06 B")
ok(str(50 - 32 + vdiv(23, 6)) == t("lp-s5-p06", "C") == "21", "p06 C")
ok(str(50 - 4 * (2 * 3) + 5) == t("lp-s5-p06", "E") == "31", "p06 E")
ok(50 - 4 == 46 and 46 * 2 == 92 and 2 + 3 * 4 == 14 and 6 * 3 == 18 and 23 - 18 == 5, "p06 textos")

# --------------------------- p07 ---------------------------
def p07(ent):
    n1, n2 = F(ent[0]), F(ent[1])     # leia(n1, n2): primeiro valor em n1
    media = n1 + n2 / 2
    return ("Aprovado " if media >= 6 else "Recuperação ") + vnum(media)
e7 = qs["lp-s5-p07"]["entradas"]
ok(e7 == ["4", "5"] and "leia(n1, n2)" in qs["lp-s5-p07"]["codigo"], "p07 entradas")
r = p07(e7)
ok(r == "Aprovado 6.5" == norm(qs["lp-s5-p07"]["saida"]) == t("lp-s5-p07", certa("lp-s5-p07")), f"p07 {r}")
m = (F(4) + 5) / 2
ok(("Recuperação " if m < 6 else "Aprovado ") + vnum(m) == t("lp-s5-p07", "A"), "p07 A")
m = 4 + vdiv(5, 2)
ok(("Aprovado " if m >= 6 else "Recuperação ") + vnum(m) == t("lp-s5-p07", "C"), "p07 C")
ok(t("lp-s5-p07", "D") == "Recuperação 6.5" and t("lp-s5-p07", "E") == "Aprovado media", "p07 D E")

# --------------------------- p08 ---------------------------
def p08(mes):
    tt = vdiv(mes - 1, 3)
    return {0: "T1", 1: "T2", 2: "T3", 3: "T4"}.get(tt, "Mês inválido")
ok(qs["lp-s5-p08"]["entradas"] == ["6"], "p08 entradas")
ok(p08(6) == "T2" == norm(qs["lp-s5-p08"]["saida"]) == t("lp-s5-p08", certa("lp-s5-p08")), "p08")
ok(round(F(5, 3)) == 2 and t("lp-s5-p08", "B") == "T3", "p08 B")
ok(t("lp-s5-p08", "C") == "T1" and t("lp-s5-p08", "D") == "Mês inválido", "p08 C D")
ok([p08(m) for m in (1, 2, 3, 4, 5, 6, 7, 9, 10, 12, 13, 0)] ==
   ["T1", "T1", "T1", "T2", "T2", "T2", "T3", "T3", "T4", "T4", "Mês inválido", "T1"], "p08 confira")
ok(vdiv(-1, 3) == 0 and vdiv(12, 3) == 4 and vdiv(2, 3) == 0 and vdiv(3, 3) == 1, "p08 contas")
ok(format(5 / 3, ".2f") == "1.67", "p08 1,67")

# --------------------------- p09 ---------------------------
x, y = 4, 9
A, B, C = x > 5, y > 5, vmod(x, 2) == 1
p = (not A) or (B and C)          # nao > e > ou
q = not (A or B)
r = f"{vlog(p)} {vlog(q)}"
ok(r == "VERDADEIRO FALSO" == norm(qs["lp-s5-p09"]["saida"]) == t("lp-s5-p09", certa("lp-s5-p09")), f"p09 {r}")
p_ou_antes = ((not A) or B) and C
q_meia = (not A) or (not B)
ok(f"{vlog(p_ou_antes)} {vlog(q)}" == t("lp-s5-p09", "A"), "p09 A")
ok(f"{vlog(p)} {vlog(q_meia)}" == t("lp-s5-p09", "B"), "p09 B")
ok(f"{vlog(p_ou_antes)} {vlog(q_meia)}" == t("lp-s5-p09", "D"), "p09 D")
ok(q == ((not A) and (not B)), "p09 De Morgan")
# dependencia da precedencia: se e e ou tivessem a mesma prioridade (esquerda para direita), p seria FALSO
ok(vlog(p_ou_antes) == "FALSO", "p09 sensibilidade")
notas.append("p09: a resposta depende de 'e' antes de 'ou' (com prioridade igual, p seria FALSO)")

# --------------------------- p10 ---------------------------
def p10(n):
    c = vdiv(n, 100); d = vdiv(vmod(n, 100), 10); u = vmod(n, 10)
    return u * 100 + d * 10 + c, c + d + u, c, d, u
e10 = qs["lp-s5-p10"]["entradas"]
inv, s, c, d, u = p10(int(e10[0]))
ok(e10 == ["583"], "p10 entradas")
ok(f"{inv} {s}" == "385 16" == norm(qs["lp-s5-p10"]["saida"]) == t("lp-s5-p10", certa("lp-s5-p10")), "p10")
ok(f"{c * 100 + d * 10 + u} {s}" == t("lp-s5-p10", "A"), "p10 A")
d83 = vmod(583, 100)
ok(f"{u * 100 + d83 * 10 + c} {c + d83 + u}" == t("lp-s5-p10", "B") == "1135 91", "p10 B")
ok(f"{inv} {str(c) + str(d) + str(u)}" == t("lp-s5-p10", "D"), "p10 D")
c6 = round(F(583, 100))
ok(f"{u * 100 + d * 10 + c6} {c6 + d + u}" == t("lp-s5-p10", "E") == "386 17", "p10 E")
ok(p10(100)[:2] == (1, 1) and p10(385)[0] == 583 and 3 + 8 + 5 == 16, "p10 confira")
ok(300 + 830 + 5 == 1135 and 5 + 83 + 3 == 91, "p10 erro B")

# --------------------------- p11 ---------------------------
def p11(idade, renda, fora_ge=True, dentro_gt=True, d_dentro=False, f_no_senao=False):
    s = ""
    if (idade >= 18) if fora_ge else (idade > 18):
        s += "A"
        if (renda > 3000) if dentro_gt else (renda >= 3000):
            s += "B"
            if d_dentro: s += "D"
        else:
            s += "C"
        if not d_dentro: s += "D"
    else:
        s += "E"
        if f_no_senao: s += "F"
    if not f_no_senao: s += "F"
    return s
e11 = qs["lp-s5-p11"]["entradas"]
ok(e11 == ["18", "3000"] and "leia(idade, renda)" in qs["lp-s5-p11"]["codigo"], "p11 entradas")
ok(p11(18, 3000) == "ACDF" == norm(qs["lp-s5-p11"]["saida"]) == t("lp-s5-p11", certa("lp-s5-p11")), "p11")
ok(p11(18, 3000, dentro_gt=False) == t("lp-s5-p11", "A"), "p11 A")
ok(p11(18, 3000, fora_ge=False) == t("lp-s5-p11", "C"), "p11 C")
ok(p11(18, 3000, d_dentro=True) == t("lp-s5-p11", "D"), "p11 D")
ok(p11(18, 3000, f_no_senao=True) == t("lp-s5-p11", "E"), "p11 E")
ok(p11(17, 3000) == "EF" and p11(18, 3001) == "ABDF", "p11 confira")

# --------------------------- p12 ---------------------------
def regra(v, vip, dist): return v >= 200 or (vip and dist <= 50)
c12 = {
    "A": lambda v, vip, dist: (v > 200) or (vip and dist <= 50),
    "B": lambda v, vip, dist: (v >= 200 or vip) and dist <= 50,
    "C": lambda v, vip, dist: (v >= 200 and vip) or dist <= 50,   # e antes de ou
    "D": lambda v, vip, dist: (v >= 200) or (vip and dist <= 50),
    "E": lambda v, vip, dist: (v >= 200) or (vip and dist >= 50),
}
grade = list(itertools.product([F(0), F(100), F("199.99"), F(200), F("200.01"), F(300)],
                               [False, True], [0, 20, 30, 49, 50, 51, 80]))
eq = [x for x in L if all(c12[x](*g) == regra(*g) for g in grade)]
ok(eq == ["D"] == [certa("lp-s5-p12")], f"p12 {eq}")
VF = lambda b: "V" if b else "F"
casos = [(300, False, 80), (200, False, 80), (100, True, 50), (100, True, 80), (100, False, 30)]
linhas = [[str(i), str(v), VF(vip), str(dd), VF(regra(v, vip, dd))] + [VF(c12[x](v, vip, dd)) for x in L]
          for i, (v, vip, dd) in enumerate(casos, 1)]
ok(qs["lp-s5-p12"]["tabela"]["linhas"] == linhas, "p12 tabela")
ok(qs["lp-s5-p12"]["tabela"]["cab"][5:] == list(L), "p12 cabecalho")
erra = {x: [i + 1 for i, (v, vip, dd) in enumerate(casos) if c12[x](v, vip, dd) != regra(v, vip, dd)] for x in L}
ok(erra == {"A": [2], "B": [1, 2], "C": [1, 2, 5], "D": [], "E": [4]}, f"p12 confira {erra}")
ok(c12["B"](300, False, 80) is False and c12["C"](100, False, 30) is True and c12["C"](300, False, 80) is False, "p12 B C")
ok(c12["E"](100, True, 20) is False and c12["E"](100, True, 80) is True, "p12 E")
ok(all(c12["B"](v, vip, dd) == regra(v, vip, dd) for (v, vip, dd) in grade if dd <= 50), "p12 trabalho B perto")

# --------------------------- conjunto ---------------------------
ids = sorted(qs)
ok(ids == [f"lp-s5-p{i:02d}" for i in range(1, 13)], f"ids {ids}")
ok(all(qs[i]["semana"] == 5 and qs[i]["origem"] == "Prévia · ementa" for i in ids), "semana/origem")
niv = [qs[i]["nivel"] for i in ids]
ok([niv.count(k) for k in (1, 2, 3)] == [4, 4, 4], f"niveis {niv}")
cod = [i for i in ids if qs[i].get("codigo")]
ent = [i for i in ids if qs[i].get("entradas")]
ok(len(cod) >= 7 and len(ent) >= 3, f"codigo {cod} entradas {ent}")
pos = "".join(certa(i) for i in ids)
ok(max(pos.count(x) for x in L) <= 3, f"posicoes {pos}")

# subconjunto do BRIEF no codigo
PERM = set("""algoritmo var inicio fimalgoritmo inteiro real caractere logico vetor de
se entao senao fimse escolha caso outrocaso fimescolha para ate passo faca fimpara enquanto
fimenquanto repita interrompa e ou nao xou div mod verdadeiro falso leia escreva escreval
raizq abs int quad compr maiusc minusc""".split())
for i in cod:
    c = qs[i]["codigo"]
    sem_txt = re.sub(r'"[^"]*"', '""', c)
    sem_txt = re.sub(r"//.*", "", sem_txt)
    palavras = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", sem_txt))
    decl = set()
    for linha in sem_txt.split("\n"):
        mm = re.match(r"\s*([A-Za-z0-9_,\s]+):\s*(inteiro|real|caractere|logico)\s*$", linha)
        if mm: decl |= {v.strip() for v in mm.group(1).split(",")}
    fora = palavras - PERM - decl
    ok(not fora, f"{i}: palavras fora do subconjunto ou nao declaradas {sorted(fora)}")
    ok(not re.search(r":\s*\d", re.sub(r'"[^"]*"', "", c).split("inicio", 1)[1]), f"{i}: formatacao x:n")

# voz e forma
PROIB = ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada", "fascinante",
         "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente"]
for i in ids:
    q = qs[i]
    for s_ in todos_textos(q):
        fora_cod = re.sub(r"`[^`]*`", " ", s_)
        low = fora_cod.lower()
        for pr in PROIB:
            ok(pr not in low, f"{i}: proibida '{pr}'")
        ok("!" not in fora_cod, f"{i}: exclamação")
        ok("—" not in fora_cod, f"{i}: travessão em '{s_[:40]}'")
        ok("professor" not in low and "forbellone" not in low and "página" not in low, f"{i}: fonte citada")
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        nw = len(q["jeitos"][k].split())
        ok(35 <= nw <= 110, f"{i}.{k}: {nw} palavras")
    ok(3 <= len(q["jeitos"]["receita"]) <= 7, f"{i}: receita")
    ok(4 <= len(q["jeitos"]["conversa"]) <= 8, f"{i}: conversa")
    nt = len(q["tema"].split())
    ok(2 <= nt <= 5, f"{i}: tema {nt}")
    # frase repetida entre jeitos (qualquer tamanho acima de 25 caracteres)
    vist = {}
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        for fr in re.split(r"(?<=[.?:])\s+", q["jeitos"][k]):
            f2 = fr.strip().lower()
            if len(f2) > 25:
                if f2 in vist and vist[f2] != k:
                    falhas.append(f"{i}: frase repetida em {vist[f2]} e {k}: {f2[:50]}")
                vist.setdefault(f2, k)
    # tamanho das alternativas: a certa nao pode ser a mais longa com folga
    tam = [len(a["t"]) for a in q["alternativas"]]
    ic = L.index(certa(i))
    outras = [tam[k] for k in range(5) if k != ic]
    if tam[ic] > 1.5 * max(outras):
        falhas.append(f"{i}: certa bem mais longa que as outras {tam}")

# teoria
ok(len(semanas) == 1, "uma semana de teoria")
s5 = semanas[0]
ok(s5["semana"] == 5 and s5["previa"] is True and
   s5["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "teoria cabeçalho")
ok(3 <= len(s5["blocos"]) <= 6, "teoria blocos")
for bl in s5["blocos"]:
    nb = len(bl["texto"].split())
    ok(40 <= nb <= 120, f"bloco '{bl['titulo']}' {nb} palavras")
for k, v in s5["jeitos"].items():
    nj = len(v.split())
    ok(50 <= nj <= 120, f"jeito semana {k}: {nj}")
ok(vdiv(5, 2) == 2 and F(5, 2) == F("2.5") and vdiv(47, 5) == 9 and vmod(47, 5) == 2, "teoria div/mod")
ok((vdiv(583, 100), vdiv(vmod(583, 100), 10), vmod(583, 10)) == (5, 8, 3), "teoria digitos")
ok((F(4) + 5) / 2 == F(9, 2) and 4 + F(5, 2) == F(13, 2), "teoria lab media")
ok((vdiv(347, 100), vdiv(vmod(347, 100), 10), vmod(347, 10)) == (3, 4, 7), "lab digitos 347")

print("posições:", pos, {x: pos.count(x) for x in L})
print("com código:", len(cod), cod)
print("com entradas:", len(ent), ent)
for n_ in notas:
    print("NOTA", n_)
if falhas:
    print("FALHAS:")
    for f_ in falhas:
        print(" -", f_)
    sys.exit(1)
print("revisão r2: todas as contas conferem")
