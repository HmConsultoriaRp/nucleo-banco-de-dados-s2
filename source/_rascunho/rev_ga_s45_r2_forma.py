# Segunda revisao de forma do lote ga_s45: frases por "erro" de alternativa, dica em uma frase,
# frases longas, palavras proibidas, hifen como menos e vetor sem marcador.
# Uso: python -I rev_ga_s45_r2_forma.py
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")


def frases(s):
    s = re.sub(r"`[^`]*`", "X", s)
    partes = re.split(r"(?<=[.?])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ(\[0-9−])", s.strip())
    return [p for p in partes if p.strip()]


probs = []
longas = []
for nome in sorted(os.listdir(DADOS)):
    if not (nome.startswith("ga_s45_p") and nome.endswith(".json")):
        continue
    d = json.load(open(os.path.join(DADOS, nome), encoding="utf-8"))
    textos = []
    for s in d["semanas"]:
        for b in s["blocos"]:
            textos.append((f"sem{s['semana']} bloco {b['titulo']}", b["texto"]))
        for k, t in s["jeitos"].items():
            textos.append((f"sem{s['semana']} jeito {k}", t))
        textos.append((f"sem{s['semana']} lab", s["lab"]))
        textos.append((f"sem{s['semana']} chamada", s["chamada"]))
    for q in d["questoes"]:
        qid = q["id"]
        for i, a in enumerate(q["alternativas"]):
            if "erro" in a:
                n = len(frases(a["erro"]))
                if n > 2:
                    probs.append(f"{qid} alt {'ABCDE'[i]}: erro com {n} frases")
                textos.append((f"{qid} alt {'ABCDE'[i]}", a["erro"]))
        if len(frases(q["dica"])) > 1:
            probs.append(f"{qid}: dica com {len(frases(q['dica']))} frases")
        textos.append((f"{qid} enunciado", q["enunciado"]))
        textos.append((f"{qid} dica", q["dica"]))
        for k, t in q["jeitos"].items():
            if isinstance(t, str):
                textos.append((f"{qid} {k}", t))
            elif k == "receita":
                for j, p in enumerate(t):
                    textos.append((f"{qid} receita {j}", p))
            else:
                for j, c in enumerate(t):
                    textos.append((f"{qid} conversa {j}", c["fala"]))
        if "figura" in q:
            textos.append((f"{qid} legenda", q["figura"].get("legenda", "")))
    for onde, t in textos:
        for f in frases(t):
            n = len(re.findall(r"\S+", f))
            if n > 32:
                longas.append(f"{onde}: {n} palavras: {f[:90]}")
        if re.search(r"(^|[\s(,\[=])-\d", re.sub(r"`[^`]*`", "", t)):
            probs.append(f"{onde}: hifen como menos")
        sem_cod = re.sub(r"`[^`]*`", " ", t)
        if "!" in sem_cod:
            probs.append(f"{onde}: exclamacao")
        if re.search(r"\b(AB|AC|AP|PQ|QP|RS|PA)\b", re.sub(r"\[\[[^\]]*\]\]", "", sem_cod)):
            probs.append(f"{onde}: vetor sem [[ ]]? {re.findall(r'.{0,20}(?:AB|AC|AP|PQ|QP|RS|PA).{0,20}', re.sub(r'\[\[[^\]]*\]\]', '', sem_cod))}")

for p in probs:
    print("PROBLEMA", p)
for l in longas:
    print("LONGA", l)
print(f"{len(probs)} problema(s), {len(longas)} frase(s) longa(s)")
