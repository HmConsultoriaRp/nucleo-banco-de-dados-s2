# Revisao de forma do lote ga_s45: tamanhos, bytes de controle, dica em uma frase, temas.
# Uso: python -I rev_ga_s45_forma.py
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")

probs = []
n_ok = 0


def pal(s):
    return len(re.findall(r"\S+", s))


def faixa(onde, s, lo, hi):
    global n_ok
    n = pal(s)
    if lo <= n <= hi:
        n_ok += 1
    else:
        probs.append(f"{onde}: {n} palavras (alvo {lo} a {hi})")


for nome in sorted(os.listdir(DADOS)):
    if not (nome.startswith("ga_s45_p") and nome.endswith(".json")):
        continue
    caminho = os.path.join(DADOS, nome)
    with open(caminho, "rb") as f:
        bruto = f.read()
    ctrl = [b for b in bruto if b < 32 and b not in (9, 10, 13)]
    if ctrl:
        probs.append(f"{nome}: bytes de controle {sorted(set(ctrl))}")
    if "\\b".encode() in bruto or b"\\f" in bruto:
        probs.append(f"{nome}: escape \\b ou \\f no JSON")
    d = json.loads(bruto.decode("utf-8"))
    for s in d["semanas"]:
        for i, b in enumerate(s["blocos"]):
            faixa(f"{nome} sem{s['semana']} bloco{i}", b["texto"], 40, 120)
        for k, t in s["jeitos"].items():
            faixa(f"{nome} sem{s['semana']} jeito {k}", t, 50, 120)
    for q in d["questoes"]:
        for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
            faixa(f"{q['id']} {k}", q["jeitos"][k], 35, 110)
        frases = [x for x in re.split(r"(?<=[.?;])\s+", q["dica"].strip()) if x]
        if len([x for x in re.split(r"(?<=[.?])\s+", q["dica"].strip()) if x]) > 1:
            probs.append(f"{q['id']}: dica com mais de uma frase")
        if not (2 <= len(q["tema"].split()) <= 5):
            probs.append(f"{q['id']}: tema com {len(q['tema'].split())} palavras")
        for a in q["alternativas"]:
            if "erro" in a and pal(a["erro"]) > 60:
                probs.append(f"{q['id']}: erro de alternativa longo ({pal(a['erro'])})")

print(f"{n_ok} tamanhos dentro da faixa")
for p in probs:
    print("PROBLEMA", p)
print("sem problemas" if not probs else f"{len(probs)} problema(s)")
