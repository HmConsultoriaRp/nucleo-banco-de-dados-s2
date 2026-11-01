# Revisor: forma, voz e cobertura do lote lp_s34.
import json, os, re, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("lp_s34_p") and f.endswith(".json"))
probs = []
def p(msg):
    probs.append(msg); print("PROBLEMA", msg)
def obs(msg):
    print("obs     ", msg)

def np_(s): return len(re.findall(r"\S+", s))
def frases(s): return [f for f in re.split(r"(?<=[.?])\s+", s.strip()) if f]

qs, sems = [], []
for f in arqs:
    raw = open(os.path.join(DADOS, f), "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"): p(f + ": BOM")
    for i, by in enumerate(raw):
        if by < 32 and by not in (10, 13): p(f"{f}: byte de controle {by} na posição {i}")
    d = json.loads(raw.decode("utf-8"))
    if d["disciplina"] != "lp": p(f + ": disciplina")
    sems += d.get("semanas", [])
    if f != "lp_s34_p1.json" and d.get("semanas"): p(f + ": teoria fora da _p1")
    if len(d["questoes"]) > 6: p(f + ": mais de 6 questões")
    qs += d["questoes"]

ids = [q["id"] for q in qs]
esp = [f"lp-s3-p{i:02d}" for i in range(1, 13)] + [f"lp-s4-p{i:02d}" for i in range(1, 13)]
if sorted(ids) != sorted(esp): p(f"ids: {sorted(set(ids) ^ set(esp))}")
niv = Counter((q["semana"], q["nivel"]) for q in qs)
print("níveis:", dict(sorted(niv.items())))
for s in (3, 4):
    for n in (1, 2, 3):
        if niv[(s, n)] != 4: p(f"semana {s} nível {n}: {niv[(s, n)]}")
pos = Counter("ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in qs)
print("posições:", dict(sorted(pos.items())))
for q in qs:
    if q["origem"] != "Prévia · ementa": p(q["id"] + ": origem")
    if q["semana"] != int(q["id"][4]): p(q["id"] + ": semana")
    if not 2 <= np_(q["tema"]) <= 5: p(q["id"] + f": tema com {np_(q['tema'])} palavras")
print("com código:", [q["id"] for q in qs if q.get("codigo")])
print("com tabela:", len([q for q in qs if q.get("tabela")]), [(q["id"], q["tabela"]["onde"]) for q in qs if q.get("tabela")])

FONTE = "Prévia pela ementa do PPC — trocar quando o material da semana chegar"
for s in sems:
    if s["fonte"] != FONTE or s["previa"] is not True: p(f"semana {s['semana']}: fonte/previa")
    for i, b in enumerate(s["blocos"]):
        n = np_(b["texto"])
        if not 40 <= n <= 120: p(f"semana {s['semana']} bloco {i}: {n} palavras")
    for k, v in s["jeitos"].items():
        n = np_(v)
        if not 50 <= n <= 120: p(f"semana {s['semana']} jeito {k}: {n} palavras")
    print(f"semana {s['semana']}: blocos", [np_(b['texto']) for b in s['blocos']], "jeitos", {k: np_(v) for k, v in s['jeitos'].items()})
print("semanas presentes:", [s["semana"] for s in sems])

PROIB = ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada", "fascinante",
         "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente", "parabéns", "muito bem"]
def textos(q):
    yield "enunciado", q["enunciado"]
    yield "dica", q["dica"]
    yield "resposta", q["resposta"]
    for a in q["alternativas"]:
        yield "alt", a["t"]
        if a.get("erro"): yield "erro_alt", a["erro"]
    for k, v in q["jeitos"].items():
        if isinstance(v, str): yield k, v
        elif k == "receita":
            for x in v: yield k, x
        else:
            for x in v: yield k, x["fala"]
    if q.get("tabela"):
        for c in q["tabela"]["cab"]: yield "tabela", c

def todos_textos_sem(s):
    yield "titulo", s["titulo"]; yield "chamada", s["chamada"]; yield "lab", s["lab"]
    for b in s["blocos"]: yield "bloco", b["texto"]
    for f in s["formulas"]: yield "formula", f["nome"] + " " + f["expr"] + " " + f["quando"]
    for k, v in s["jeitos"].items(): yield "jeito_" + k, v

frases_lote = defaultdict(list)
for s in sems:
    for onde, t in todos_textos_sem(s):
        if "!" in t: p(f"semana {s['semana']} {onde}: exclamação")
        for w in PROIB:
            if w in t.lower(): p(f"semana {s['semana']} {onde}: proibida {w}")
        for fr in frases(t):
            if len(fr) > 40: frases_lote[fr.lower()].append(f"sem{s['semana']}.{onde}")

for q in qs:
    j = q["jeitos"]
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n = np_(j[k])
        if not 35 <= n <= 110: p(f"{q['id']} {k}: {n} palavras")
    if not 3 <= len(j["receita"]) <= 7: p(f"{q['id']} receita {len(j['receita'])} passos")
    if not 4 <= len(j["conversa"]) <= 8: p(f"{q['id']} conversa {len(j['conversa'])} falas")
    nd = len(frases(q["dica"]))
    if nd > 1: p(f"{q['id']} dica com {nd} frases: {q['dica']}")
    for k in j:
        if k != "visual":
            txt = j[k] if isinstance(j[k], str) else " ".join(x if isinstance(x, str) else x["fala"] for x in j[k])
            if "ao lado" in txt and "tabela" in txt: p(f"{q['id']} {k}: cita 'tabela ao lado', mas a tabela da explicação só aparece no jeito Visual")
    if q.get("tabela") and q["tabela"]["onde"] == "explicacao" and "tabela" not in j["visual"].lower():
        obs(f"{q['id']}: tabela na explicação, mas o visual não fala dela")
    vistos = Counter()
    for onde, t in textos(q):
        low = t.lower()
        for w in PROIB:
            if w in low: p(f"{q['id']} {onde}: proibida {w}")
        if "!" in t: p(f"{q['id']} {onde}: exclamação")
        if re.search(r"(^|[\s(,\[=])-\d", re.sub(r"`[^`]*`", " ", t)): p(f"{q['id']} {onde}: hífen como menos")
        if "—" in t: obs(f"{q['id']} {onde}: travessão")
        for fr in frases(t):
            if len(fr) > 40:
                vistos[fr.lower()] += 1
                frases_lote[fr.lower()].append(f"{q['id']}.{onde}")
    for fr, c in vistos.items():
        if c > 1: p(f"{q['id']}: frase repetida dentro da questão: {fr[:70]}")
    L = [len(a["t"]) for a in q["alternativas"]]
    c = [a.get("certa") for a in q["alternativas"]].index(True)
    if L[c] == max(L) and L[c] > 1.3 * sorted(L)[-2]: obs(f"{q['id']}: certa bem mais longa {L}")

for fr, onde in frases_lote.items():
    if len(onde) > 1 and len(set(o.split(".")[0] for o in onde)) > 1:
        obs(f"frase repetida entre questões/teoria {onde}: {fr[:80]}")

print()
print("PROBLEMAS:", len(probs))
