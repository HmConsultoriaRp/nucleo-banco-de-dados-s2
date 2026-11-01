# Revisor - lote ga_s2b: cobertura, certa x gabarito, niveis, tamanho, bytes, figuras.
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pasta = os.path.join(base, "dados")
arqs = sorted(os.path.join(pasta, f) for f in os.listdir(pasta) if f.startswith("ga_s2b_p") and f.endswith(".json"))
print("arquivos:", [os.path.basename(a) for a in arqs])

esperado = {
    "ga-s2-l2q2": (1, "[[u]] e [[v]]"),
    "ga-s2-l2q3": (2, "(−1, 2, −3)"),
    "ga-s2-l2q4": (3, None),
    "ga-s2-l2q5a": (2, "m = 0 ou m = 1/2"),
    "ga-s2-l2q5b": (3, "√2/2 se m = 0, e √17/4 se m = 1/2"),
    "ga-s2-l2q6": (3, "C = (0, 0, 1) ou C = (0, 0, 2)"),
    "ga-s2-l2q7": (3, "(2, 4, 0)"),
    "ga-s2-l2q8": (2, "Â = 90°, B̂ ≈ 36,87° e Ĉ ≈ 53,13°"),
    "ga-s2-l2q9a": (2, "[[v₁]] = (−1/14, 1/7, 3/14) e [[v₂]] = (29/14, −1/7, 11/14)"),
    "ga-s2-l2q9b": (2, "[[v₁]] = (4/3, 4/3, 4/3) e [[v₂]] = (−7/3, 2/3, 5/3)"),
    "ga-s2-l2q9c": (2, "[[v₁]] = (−3, −6, 0) e [[v₂]] = (0, 0, 0)"),
    "ga-s2-l2q10": (2, "(−15/11, −6/11, 6/11)"),
    "ga-s2-l2q11": (3, "8√26"),
    "ga-s2-l2q12a": (1, "−3"),
    "ga-s2-l2q12b": (2, "3√3"),
    "ga-s2-l2q12c": (2, "√7"),
    "ga-s2-l2q12d": (3, "3√3"),
}
problemas = []
vistos = []
pos = Counter()
for a in arqs:
    raw = open(a, "rb").read()
    ctrl = [b for b in raw if b < 32 and b not in (10, 13, 9)]
    if ctrl:
        problemas.append(f"{a}: bytes de controle {ctrl[:5]}")
    txt = raw.decode("utf-8")
    for ch in "—–!":
        if ch in txt:
            problemas.append(f"{os.path.basename(a)}: caractere '{ch}' presente")
    d = json.loads(txt)
    if d.get("semanas"):
        problemas.append(f"{a}: semanas nao vazio")
    for q in d["questoes"]:
        qid = q["id"]
        vistos.append(qid)
        alts = q["alternativas"]
        certa = [i for i, x in enumerate(alts) if x.get("certa")]
        pos["ABCDE"[certa[0]]] += 1
        if qid not in esperado:
            problemas.append(f"{qid}: fora do pedido")
            continue
        niv, txt_certa = esperado[qid]
        if q["nivel"] != niv:
            problemas.append(f"{qid}: nivel {q['nivel']} != {niv}")
        if txt_certa is not None and alts[certa[0]]["t"] != txt_certa:
            problemas.append(f"{qid}: certa '{alts[certa[0]]['t']}' != '{txt_certa}'")
        # tamanhos
        for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
            n = len(re.findall(r"\S+", q["jeitos"][k]))
            if not 35 <= n <= 110:
                problemas.append(f"{qid}.{k}: {n} palavras")
        if not 3 <= len(q["jeitos"]["receita"]) <= 7:
            problemas.append(f"{qid}: receita {len(q['jeitos']['receita'])} passos")
        if not 4 <= len(q["jeitos"]["conversa"]) <= 8:
            problemas.append(f"{qid}: conversa {len(q['jeitos']['conversa'])} falas")
        # alternativas distintas
        ts = [x["t"] for x in alts]
        if len(set(ts)) != 5:
            problemas.append(f"{qid}: alternativas repetidas")
        # figura: onde
        f = q.get("figura")
        if f and f.get("onde") != "explicacao":
            problemas.append(f"{qid}: figura no enunciado - checar se desenha a resposta")
        # hifen como menos fora de crase
        def semcod(s):
            return re.sub(r"`[^`]*`", " ", s)
        textos = [q["enunciado"], q["dica"], q["resposta"]] + [x.get("erro", "") for x in alts] + [x["t"] for x in alts]
        textos += [q["jeitos"][k] for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]]
        textos += q["jeitos"]["receita"] + [c["fala"] for c in q["jeitos"]["conversa"]]
        for t in textos:
            if re.search(r"(^|[\s(,\[=;])-\d", semcod(t)):
                problemas.append(f"{qid}: hifen como menos em '{t[:50]}'")

faltam = set(esperado) - set(vistos)
if faltam:
    problemas.append(f"faltam ids: {sorted(faltam)}")
rep = [k for k, c in Counter(vistos).items() if c > 1]
if rep:
    problemas.append(f"ids repetidos: {rep}")
print("posicoes:", dict(sorted(pos.items())), "total", sum(pos.values()))
print("problemas:", len(problemas))
for p in problemas:
    print("  ", p)
