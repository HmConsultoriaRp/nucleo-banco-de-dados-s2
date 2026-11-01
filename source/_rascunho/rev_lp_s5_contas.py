# Revisao adversarial do lote lp_s5 (Logica, semana 5, previa).
# Uso: python -I rev_lp_s5_contas.py
# Resolve cada questao do zero (sem olhar o campo "resposta"), refaz a conta de cada "erro"
# e confere que a alternativa marcada como certa bate com a conta. Conta exata com Fraction.
import json, os, sys, re, itertools
from fractions import Fraction as F

AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

falhas = []
def ok(cond, msg):
    if not cond:
        falhas.append(msg)

qs, semanas = {}, []
for nome in sorted(os.listdir(DADOS)):
    if nome.startswith("lp_s5_p") and nome.endswith(".json"):
        bruto = open(os.path.join(DADOS, nome), "rb").read()
        ctrl = [b for b in bruto if b < 32 and b not in (9, 10, 13)]
        ok(not ctrl, f"{nome}: bytes de controle {ctrl[:5]}")
        d = json.loads(bruto.decode("utf-8"))
        semanas += d.get("semanas", [])
        for q in d["questoes"]:
            ok(q["id"] not in qs, f"id repetido {q['id']}")
            qs[q["id"]] = q

def alt(qid, letra):
    return qs[qid]["alternativas"]["ABCDE".index(letra)]
def certa_letra(qid):
    return "ABCDE"[[a.get("certa") is True for a in qs[qid]["alternativas"]].index(True)]
def texto(qid, letra):
    return alt(qid, letra)["t"]

# div e mod do VisuAlg (corta as casas, resto com o sinal do dividendo, como Pascal)
def vdiv(a, b):
    q = F(a) / F(b)
    return int(q) if q >= 0 else -int(-q)
def vmod(a, b):
    return a - b * vdiv(a, b)
def vreal(x):
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.10f}".rstrip("0")
    return s
def vlog(b):
    return "VERDADEIRO" if b else "FALSO"
def norm(s):
    return re.sub(r"\s+", " ", s).strip()

# ---------------- p01 (sem codigo) ----------------
ok(certa_letra("lp-s5-p01") == "C" and "Definição" in texto("lp-s5-p01", "C"), "p01 certa deveria ser Definição")

# ---------------- p02 ----------------
def p02(a=8, b=5):
    a = a + b
    b = a - b
    a = a - b
    return f"{a} {b}"
r = p02()
ok(r == "5 8", f"p02 conta {r}")
ok(norm(qs["lp-s5-p02"]["saida"]) == r == texto("lp-s5-p02", certa_letra("lp-s5-p02")), "p02 saida/certa")
# erros
a, b = 8, 5; a = a + b; b = a - b
ok(f"{a} {b}" == texto("lp-s5-p02", "B"), "p02 B 13 8")
ok("8 5" == texto("lp-s5-p02", "C"), "p02 C iniciais")
a, b = 8, 5; a = a + b; b2 = a - b; a = a - 5; b = b2
ok(f"{a} {b}" == texto("lp-s5-p02", "D"), f"p02 D {a} {b}")
a, b = 8, 5; a0 = a; a = a + b; b = a0 - b; a = a - b
ok(f"{a} {b}" == texto("lp-s5-p02", "E"), f"p02 E {a} {b}")
ok(p02(2, 7) == "7 2", "p02 confira 2 e 7")
a, b = 2, 7; a = a + b
ok(a == 9 and a - b == 2, "p02 confira contas intermediarias")

# ---------------- p03 ----------------
ident = re.compile(r"^[A-Za-z][A-Za-z0-9]*$")  # regra conservadora, sem sublinhado
validos = [L for L in "ABCDE" if ident.match(texto("lp-s5-p03", L).strip("`"))]
ok(validos == [certa_letra("lp-s5-p03")] == ["D"], f"p03 validos {validos}")

# ---------------- p04 ----------------
n = 47
q4, r4 = vdiv(n, 5), vmod(n, 5)
ok(f"{q4} {r4}" == "9 2" == norm(qs["lp-s5-p04"]["saida"]) == texto("lp-s5-p04", certa_letra("lp-s5-p04")), "p04")
ok(texto("lp-s5-p04", "A") == f"{r4} {q4}", "p04 A trocado")
ok(texto("lp-s5-p04", "C") == f"{vreal(F(47, 5))} {r4}", "p04 C 9.4")
ok(F(47, 5) - 9 == F(2, 5) and texto("lp-s5-p04", "D") == "9 4", "p04 D 0,4 = 2/5")
ok(texto("lp-s5-p04", "E") == f"{q4 * 5} {r4}", "p04 E 45")
ok(5 * 9 + 4 == 49 and 5 * 2 + 9 == 19 and 47 - 45 == 2, "p04 contas do texto")

# ---------------- p05 (sem codigo) ----------------
def fluxo(v): return 20 if v > 1000 else 5
def altA(v): return 5 if v > 1000 else 20
def altB(v):
    t = None
    if v > 1000: t = 20
    t = 5
    return t
def altC(v, limite=10000):
    t = None
    passos = 0
    while v > 1000:
        t = 20
        passos += 1
        if passos > limite: return "nao termina"
    t = 5
    return t
ok([fluxo(2000), fluxo(300)] == [20, 5], "p05 fluxo")
ok([altA(2000), altA(300)] == [5, 20], "p05 A")
ok([altB(2000), altB(300)] == [5, 5], "p05 B")
ok(altC(2000) == "nao termina" and altC(300) == 5, "p05 C")
ok(certa_letra("lp-s5-p05") == "E" and texto("lp-s5-p05", "E").replace("\n", " ") ==
   "`se valor > 1000 entao` `taxa <- 20` `senao` `taxa <- 5` `fimse`", "p05 E")

# ---------------- p06 ----------------
x = 50 - 4 * 2 ** 3 + vmod(23, 6)
ok(x == 23 and norm(qs["lp-s5-p06"]["saida"]) == "23" == texto("lp-s5-p06", certa_letra("lp-s5-p06")), f"p06 {x}")
ok(str(50 - (4 * 2 ** 3 + vmod(23, 6))) == texto("lp-s5-p06", "A"), "p06 A 13")
ok(str(vmod(50 - 32 + 23, 6)) == texto("lp-s5-p06", "B") and 50 - 32 + 23 == 41, "p06 B 5")
ok(str(50 - 32 + vdiv(23, 6)) == texto("lp-s5-p06", "C"), "p06 C 21")
ok(str(50 - 4 * (2 * 3) + 5) == texto("lp-s5-p06", "E") and 4 * 6 == 24, "p06 E 31")
ok(50 - 4 == 46 and 46 * 2 == 92 and 2 + 3 * 4 == 14 and 50 - 32 == 18, "p06 contas do texto")

# ---------------- p07 (entradas 4 e 5, real) ----------------
def p07(e):
    n1, n2 = F(e[0]), F(e[1])        # leia(n1, n2): primeiro valor em n1
    media = n1 + n2 / 2
    return ("Aprovado " if media >= 6 else "Recuperação ") + vreal(media)
r = p07(qs["lp-s5-p07"]["entradas"])
ok(qs["lp-s5-p07"]["entradas"] == ["4", "5"], "p07 entradas")
ok(r == "Aprovado 6.5" == norm(qs["lp-s5-p07"]["saida"]) == texto("lp-s5-p07", certa_letra("lp-s5-p07")), f"p07 {r}")
m = (F(4) + F(5)) / 2
ok("Recuperação " + vreal(m) == texto("lp-s5-p07", "A"), "p07 A")
m = F(4) + vdiv(5, 2)
ok(m >= 6 and "Aprovado " + vreal(m) == texto("lp-s5-p07", "C"), "p07 C")
ok(texto("lp-s5-p07", "D") == "Recuperação 6.5", "p07 D")
ok(texto("lp-s5-p07", "E") == "Aprovado media", "p07 E")

# ---------------- p08 (entrada 6) ----------------
def p08(mes):
    t = vdiv(mes - 1, 3)
    return {0: "T1", 1: "T2", 2: "T3", 3: "T4"}.get(t, "Mês inválido")
ok(qs["lp-s5-p08"]["entradas"] == ["6"], "p08 entradas")
ok(p08(6) == "T2" == norm(qs["lp-s5-p08"]["saida"]) == texto("lp-s5-p08", certa_letra("lp-s5-p08")), "p08")
t_arred = round(F(5, 3))
ok(t_arred == 2 and {0: "T1", 1: "T2", 2: "T3", 3: "T4"}[t_arred] == texto("lp-s5-p08", "B"), "p08 B arredondou")
ok(texto("lp-s5-p08", "C") == "T1", "p08 C")
ok(6 not in (0, 1, 2, 3) and texto("lp-s5-p08", "D") == "Mês inválido", "p08 D")
ok([p08(3), p08(4), p08(13), p08(0)] == ["T1", "T2", "Mês inválido", "T1"], "p08 confira 3, 4, 13, 0")
ok(vdiv(-1, 3) == 0 and vdiv(12, 3) == 4, "p08 contas do confira")

# ---------------- p09 ----------------
x, y = 4, 9
c1, c2, c3 = x > 5, y > 5, vmod(x, 2) == 1
p = (not c1) or (c2 and c3)
q = not (c1 or c2)
r = f"{vlog(p)} {vlog(q)}"
ok(r == "VERDADEIRO FALSO" == norm(qs["lp-s5-p09"]["saida"]) == texto("lp-s5-p09", certa_letra("lp-s5-p09")), f"p09 {r}")
# robustez: se o nao valesse para o resto inteiro da expressao, p continuaria VERDADEIRO
ok((not (c1 or (c2 and c3))) == p and (not ((c1 or c2) and c3)) == p, "p09 robustez do nao")
p_ou_antes = ((not c1) or c2) and c3
q_metade = (not c1) or (not c2)
ok(f"{vlog(p_ou_antes)} {vlog(q)}" == texto("lp-s5-p09", "A"), "p09 A")
ok(f"{vlog(p)} {vlog(q_metade)}" == texto("lp-s5-p09", "B"), "p09 B")
ok(f"{vlog(p_ou_antes)} {vlog(q_metade)}" == texto("lp-s5-p09", "D"), "p09 D")
ok(q == ((not c1) and (not c2)), "p09 De Morgan")
ok(1 + 1 * 0 == 1, "p09 conversa 1 + 1 x 0")

# ---------------- p10 (entrada 583) ----------------
def p10(n):
    c = vdiv(n, 100); d = vdiv(vmod(n, 100), 10); u = vmod(n, 10)
    return u * 100 + d * 10 + c, c + d + u, (c, d, u)
inv, soma, (c, d, u) = p10(int(qs["lp-s5-p10"]["entradas"][0]))
ok(qs["lp-s5-p10"]["entradas"] == ["583"], "p10 entradas")
ok(f"{inv} {soma}" == "385 16" == norm(qs["lp-s5-p10"]["saida"]) == texto("lp-s5-p10", certa_letra("lp-s5-p10")), "p10")
ok(f"{c * 100 + d * 10 + u} {soma}" == texto("lp-s5-p10", "A"), "p10 A")
d83 = vmod(583, 100)
ok(f"{u * 100 + d83 * 10 + c} {c + d83 + u}" == texto("lp-s5-p10", "B"), "p10 B")
ok(f"{inv} {c}{d}{u}" == texto("lp-s5-p10", "D"), "p10 D")
c6 = round(F(583, 100))
ok(f"{u * 100 + d * 10 + c6} {c6 + d + u}" == texto("lp-s5-p10", "E"), "p10 E")
ok(p10(100)[:2] == (1, 1), "p10 confira 100")
ok(p10(385)[0] == 583, "p10 prova inversa")

# ---------------- p11 (entradas 18 e 3000) ----------------
def p11(idade, renda, op_fora=">=", op_dentro=">", d_no_b=False, f_no_senao=False):
    s = ""
    fora = idade >= 18 if op_fora == ">=" else idade > 18
    if fora:
        s += "A"
        dentro = renda > 3000 if op_dentro == ">" else renda >= 3000
        if dentro:
            s += "B" + ("D" if d_no_b else "")
        else:
            s += "C"
        if not d_no_b:
            s += "D"
    else:
        s += "E" + ("F" if f_no_senao else "")
    if not f_no_senao:
        s += "F"
    return s
ok(qs["lp-s5-p11"]["entradas"] == ["18", "3000"], "p11 entradas")
ok(p11(18, 3000) == "ACDF" == norm(qs["lp-s5-p11"]["saida"]) == texto("lp-s5-p11", certa_letra("lp-s5-p11")), "p11")
ok(p11(18, 3000, op_dentro=">=") == texto("lp-s5-p11", "A"), "p11 A")
ok(p11(18, 3000, op_fora=">") == texto("lp-s5-p11", "C"), "p11 C")
ok(p11(18, 3000, d_no_b=True) == texto("lp-s5-p11", "D"), "p11 D")
ok(p11(18, 3000, f_no_senao=True) == texto("lp-s5-p11", "E"), "p11 E")
ok(p11(17, 3000) == "EF" and p11(18, 3001) == "ABDF", "p11 confira")

# ---------------- p12 (sem codigo) ----------------
def regra(v, vip, dist): return v >= 200 or (vip and dist <= 50)
alts12 = {
    "A": lambda v, vip, dist: (v > 200) or (vip and dist <= 50),
    "B": lambda v, vip, dist: (v >= 200 or vip) and dist <= 50,
    "C": lambda v, vip, dist: ((v >= 200) and vip) or (dist <= 50),
    "D": lambda v, vip, dist: (v >= 200) or (vip and dist <= 50),
    "E": lambda v, vip, dist: (v >= 200) or (vip and dist >= 50),
}
grade = list(itertools.product([F(0), F(100), F("199.99"), F(200), F("200.01"), F(300)], [False, True], [0, 30, 49, 50, 51, 80]))
equiv = [L for L in "ABCDE" if all(alts12[L](*g) == regra(*g) for g in grade)]
ok(equiv == ["D"] == [certa_letra("lp-s5-p12")], f"p12 equivalentes {equiv}")
VF = lambda b: "V" if b else "F"
casos = [(300, False, 80), (200, False, 80), (100, True, 50), (100, True, 80), (100, False, 30)]
linhas = [[str(i), str(v), VF(vip), str(dd), VF(regra(v, vip, dd))] + [VF(alts12[L](v, vip, dd)) for L in "ABCDE"]
          for i, (v, vip, dd) in enumerate(casos, 1)]
ok(qs["lp-s5-p12"]["tabela"]["linhas"] == linhas, f"p12 tabela\n{linhas}")
ok(alts12["B"](300, False, 80) is False, "p12 B 300 a 80 km")
ok(alts12["C"](100, False, 30) is True and alts12["C"](300, False, 80) is False, "p12 C")
ok(alts12["E"](100, True, 20) is False and alts12["E"](100, True, 80) is True, "p12 E")
ok(alts12["A"](200, False, 80) is False, "p12 A")

# ---------------- conjunto ----------------
ids = sorted(qs)
ok(ids == [f"lp-s5-p{i:02d}" for i in range(1, 13)], f"ids {ids}")
ok(all(q["semana"] == 5 and q["origem"] == "Prévia · ementa" for q in qs.values()), "semana/origem")
niv = [qs[i]["nivel"] for i in ids]
ok([niv.count(k) for k in (1, 2, 3)] == [4, 4, 4], f"niveis {niv}")
cod = [i for i in ids if qs[i].get("codigo")]
ent = [i for i in ids if qs[i].get("entradas")]
ok(len(cod) >= 7 and len(ent) >= 3, f"codigo {cod} entradas {ent}")
pos = "".join(certa_letra(i) for i in ids)
ok(max(pos.count(L) for L in "ABCDE") <= 3, f"posicoes {pos}")
for i in ids:
    nt = len(qs[i]["tema"].split())
    ok(2 <= nt <= 5, f"{i}: tema com {nt} palavras")
    for k, v in qs[i]["jeitos"].items():
        if isinstance(v, str) and "professor" in v.lower():
            falhas.append(f"{i}.{k}: cita professor")
    if "professor" in qs[i]["enunciado"].lower():
        falhas.append(f"{i}: enunciado cita professor")
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        nw = len(qs[i]["jeitos"][k].split())
        ok(35 <= nw <= 110, f"{i}.{k}: {nw} palavras (alvo 35 a 110)")
    ok(3 <= len(qs[i]["jeitos"]["receita"]) <= 7, f"{i}: receita com {len(qs[i]['jeitos']['receita'])} passos")
    ok(4 <= len(qs[i]["jeitos"]["conversa"]) <= 8, f"{i}: conversa com {len(qs[i]['jeitos']['conversa'])} falas")
# teoria
ok(len(semanas) == 1 and semanas[0]["semana"] == 5 and semanas[0]["previa"] is True and
   semanas[0]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar", "teoria")
for b in semanas[0]["blocos"]:
    nb = len(b["texto"].split())
    ok(40 <= nb <= 120, f"bloco '{b['titulo']}' com {nb} palavras")
for k, v in semanas[0]["jeitos"].items():
    nj = len(v.split())
    ok(50 <= nj <= 120, f"jeito da semana {k} com {nj} palavras")
ok(vdiv(583, 100) == 5 and vdiv(vmod(583, 100), 10) == 8 and vmod(583, 10) == 3, "teoria digitos")
ok(vdiv(47, 5) == 9 and vmod(47, 5) == 2 and F(5, 2) == F("2.5"), "teoria div/mod")
ok(vmod(-7, 3) == -1 and (-7) % 3 == 2, "mod negativo: VisuAlg -1, Excel/Python 2")

sys.stdout.reconfigure(encoding="utf-8")
print("posições:", pos, {L: pos.count(L) for L in "ABCDE"})
print("com código:", len(cod), "com entradas:", len(ent))
if falhas:
    print("FALHAS:")
    for f in falhas:
        print(" -", f)
    sys.exit(1)
print("revisão: todas as contas conferem")
