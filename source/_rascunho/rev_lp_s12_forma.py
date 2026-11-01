# Revisor: forma e cobertura do lote lp_s12.
import json, os, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("lp_s12_p") and f.endswith(".json"))
probs = []
def p(msg):
    probs.append(msg); print("PROBLEMA", msg)

def np(s):
    return len(re.findall(r"\S+", s))

def frases(s):
    return [f for f in re.split(r"(?<=[.?:;])\s+", s.strip()) if f]

qs, sems = [], []
for f in arqs:
    raw = open(os.path.join(DADOS, f), "rb").read()
    if raw.startswith(b"\xef\xbb\xbf"):
        p(f + ": BOM")
    for i, by in enumerate(raw):
        if by < 32 and by not in (10, 13, 9):
            p(f"{f}: byte de controle {by} na posição {i}")
    d = json.loads(raw.decode("utf-8"))
    sems += d.get("semanas", [])
    qs += d["questoes"]
    if f != "lp_s12_p1.json" and d.get("semanas"):
        p(f + ": teoria fora da _p1")

# cobertura
ids = [q["id"] for q in qs]
esperados = [f"lp-s1-p{i:02d}" for i in range(1, 13)] + [f"lp-s2-p{i:02d}" for i in range(1, 13)]
if sorted(ids) != sorted(esperados):
    p(f"ids diferentes do pedido: {sorted(set(ids) ^ set(esperados))}")
niv = Counter((q["semana"], q["nivel"]) for q in qs)
print("níveis:", dict(sorted(niv.items())))
for s in (1, 2):
    for n in (1, 2, 3):
        if niv[(s, n)] != 4:
            p(f"semana {s} nível {n}: {niv[(s, n)]} questões (pedido 4)")
pos = Counter("ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in qs)
print("posições:", dict(sorted(pos.items())))
for q in qs:
    if q["origem"] != "Prévia · ementa":
        p(q["id"] + ": origem " + q["origem"])
    if not q["id"].startswith(f"lp-s{q['semana']}-"):
        p(q["id"] + ": semana não bate com id")

# teoria
for s in sems:
    if s["fonte"] != "Prévia pela ementa do PPC — trocar quando o material da semana chegar" or s["previa"] is not True:
        p(f"semana {s['semana']}: fonte/previa")
    for i, b in enumerate(s["blocos"]):
        n = np(b["texto"])
        if not 40 <= n <= 120:
            p(f"semana {s['semana']} bloco {i}: {n} palavras")
    for k, v in s["jeitos"].items():
        n = np(v)
        if not 50 <= n <= 120:
            p(f"semana {s['semana']} jeito {k}: {n} palavras")
    print(f"semana {s['semana']}: blocos", [np(b['texto']) for b in s['blocos']], "jeitos", {k: np(v) for k, v in s['jeitos'].items()})

PROIB = ["vamos lá", "ótima pergunta", "excelente", "mergulh", "desvend", "jornada", "fascinante",
         "crucial", "é importante notar", "em resumo", "basicamente", "simplesmente"]
def textos(q):
    yield "enunciado", q["enunciado"]
    yield "dica", q["dica"]
    yield "resposta", q["resposta"]
    for a in q["alternativas"]:
        yield "alt", a["t"]
        if a.get("erro"):
            yield "erro", a["erro"]
    for k, v in q["jeitos"].items():
        if isinstance(v, str):
            yield k, v
        elif k == "receita":
            for x in v: yield k, x
        else:
            for x in v: yield k, x["fala"]

for q in qs:
    j = q["jeitos"]
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        n = np(j[k])
        if not 35 <= n <= 110:
            p(f"{q['id']} {k}: {n} palavras")
    if not 3 <= len(j["receita"]) <= 7:
        p(f"{q['id']} receita {len(j['receita'])} passos")
    if not 4 <= len(j["conversa"]) <= 8:
        p(f"{q['id']} conversa {len(j['conversa'])} falas")
    nd = len(frases(q["dica"]))
    if nd > 1:
        print(f"obs {q['id']} dica com {nd} frases: {q['dica']}")
    for onde, t in textos(q):
        low = t.lower()
        for w in PROIB:
            if w in low:
                p(f"{q['id']} {onde}: proibida {w}")
        if "!" in t:
            p(f"{q['id']} {onde}: exclamação")
        if re.search(r"(^|[\s(,\[=])-\d", re.sub(r"`[^`]*`", " ", t)):
            p(f"{q['id']} {onde}: hífen como menos")
        if t.count("—") > 0 and onde != "tabela":
            print(f"obs {q['id']} {onde}: travessão")
    # alternativas: tamanho parecido; a certa não pode ser a mais longa de longe
    L = [len(a["t"]) for a in q["alternativas"]]
    c = [a.get("certa") for a in q["alternativas"]].index(True)
    if L[c] == max(L) and L[c] > 1.3 * sorted(L)[-2]:
        print(f"obs {q['id']}: certa bem mais longa que as outras {L}")

print()
print("PROBLEMAS:", len(probs))
