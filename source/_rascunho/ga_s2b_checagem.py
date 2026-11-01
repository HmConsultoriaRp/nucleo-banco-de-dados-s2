# Checagem extra dos arquivos do lote ga_s2b: gabarito, bytes de controle, tamanho dos jeitos,
# coordenadas das figuras e hifen usado como sinal de menos.
import json, os, re, sys, math

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("ga_s2b_p") and f.endswith(".json"))

GABARITO = {
    "ga-s2-l2q2": "[[u]] e [[v]]",
    "ga-s2-l2q3": "(−1, 2, −3)",
    "ga-s2-l2q4": "Vetores dois a dois ortogonais",
    "ga-s2-l2q5a": "m = 0 ou m = 1/2",
    "ga-s2-l2q5b": "√2/2 se m = 0, e √17/4 se m = 1/2",
    "ga-s2-l2q6": "C = (0, 0, 1) ou C = (0, 0, 2)",
    "ga-s2-l2q7": "(2, 4, 0)",
    "ga-s2-l2q8": "Â = 90°, B̂ ≈ 36,87° e Ĉ ≈ 53,13°",
    "ga-s2-l2q9a": "[[v₁]] = (−1/14, 1/7, 3/14) e [[v₂]] = (29/14, −1/7, 11/14)",
    "ga-s2-l2q9b": "[[v₁]] = (4/3, 4/3, 4/3) e [[v₂]] = (−7/3, 2/3, 5/3)",
    "ga-s2-l2q9c": "[[v₁]] = (−3, −6, 0) e [[v₂]] = (0, 0, 0)",
    "ga-s2-l2q10": "(−15/11, −6/11, 6/11)",
    "ga-s2-l2q11": "8√26",
    "ga-s2-l2q12a": "−3",
    "ga-s2-l2q12b": "3√3",
    "ga-s2-l2q12c": "√7",
    "ga-s2-l2q12d": "3√3",
}
NIVEL = {"ga-s2-l2q2": 1, "ga-s2-l2q3": 2, "ga-s2-l2q4": 3, "ga-s2-l2q5a": 2, "ga-s2-l2q5b": 3,
         "ga-s2-l2q6": 3, "ga-s2-l2q7": 3, "ga-s2-l2q8": 2, "ga-s2-l2q9a": 2, "ga-s2-l2q9b": 2,
         "ga-s2-l2q9c": 2, "ga-s2-l2q10": 2, "ga-s2-l2q11": 3, "ga-s2-l2q12a": 1, "ga-s2-l2q12b": 2,
         "ga-s2-l2q12c": 2, "ga-s2-l2q12d": 3}

problemas = []
vistos = []
for a in arqs:
    p = os.path.join(DADOS, a)
    bruto = open(p, "rb").read()
    ctrl = [b for b in bruto if b < 0x20 and b not in (0x0A, 0x0D, 0x09)]
    if ctrl:
        problemas.append(f"{a}: {len(ctrl)} byte(s) de controle")
    if bruto.startswith(b"\xef\xbb\xbf"):
        problemas.append(f"{a}: tem BOM")
    d = json.loads(bruto.decode("utf-8"))
    for q in d["questoes"]:
        qid = q["id"]
        vistos.append(qid)
        certa = [x["t"] for x in q["alternativas"] if x.get("certa")][0]
        letra = "ABCDE"[[x.get("certa") for x in q["alternativas"]].index(True)]
        esp = GABARITO.get(qid)
        ok = esp is not None and certa.startswith(esp)
        if not ok:
            problemas.append(f"{qid}: certa '{certa}' difere do gabarito '{esp}'")
        if NIVEL.get(qid) != q["nivel"]:
            problemas.append(f"{qid}: nivel {q['nivel']} difere do pedido {NIVEL.get(qid)}")
        tam = {k: len(re.findall(r"\S+", q["jeitos"][k])) for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]}
        fora = {k: n for k, n in tam.items() if n < 35 or n > 110}
        print(f"{a} {qid} certa={letra} nivel={q['nivel']} min={q['minutos']} palavras={tam}" + (f" FORA:{fora}" if fora else ""))
        # hifen como menos em qualquer texto (fora de crase)
        def textos(o):
            if isinstance(o, str):
                yield o
            elif isinstance(o, list):
                for x in o:
                    yield from textos(x)
            elif isinstance(o, dict):
                for k, x in o.items():
                    if k not in ("de", "ate", "em", "pts"):
                        yield from textos(x)
        for s in textos(q):
            t = re.sub(r"`[^`]*`", " ", s)
            if re.search(r"(?<![A-Za-z])-\d", t):
                problemas.append(f"{qid}: hífen antes de dígito em '{t[:60]}'")

faltam = set(GABARITO) - set(vistos)
if faltam:
    problemas.append(f"ids faltando: {sorted(faltam)}")
print("total de questões:", len(vistos))

# coordenadas das figuras conferidas contra o enunciado
fig_esperado = {
    "ga-s2-l2q2": [[1, 4, 3], [-1, 1, -1], [-2, -0.5, 5], [-1, 2, -3]],
    "ga-s2-l2q7": [[2, 4, 0], [1, 2, 0], [1, -1, 2], [8, -4, -6]],
    "ga-s2-l2q9a": [[-1, 2, 3], [2, 0, 1]],
    "ga-s2-l2q9b": [[1, 1, 1], [-1, 2, 3]],
    "ga-s2-l2q9c": [[1, 2, 0], [-3, -6, 0]],
}
for a in arqs:
    d = json.load(open(os.path.join(DADOS, a), encoding="utf-8"))
    for q in d["questoes"]:
        f = q.get("figura")
        if not f:
            continue
        pontos = []
        for it in f["itens"]:
            for k in ("de", "ate", "em"):
                if k in it:
                    pontos.append(it[k])
            if "pts" in it:
                pontos.extend(it["pts"])
        if q["id"] in fig_esperado:
            for e in fig_esperado[q["id"]]:
                if e not in pontos:
                    problemas.append(f"{q['id']}: figura sem o ponto/ponta {e}")
        print(q["id"], "figura", f["modo"], "itens", len(f["itens"]))

# pontos especificos
t120 = math.radians(120)
print("v com 120 graus:", round(3 * math.cos(t120), 3), round(3 * math.sin(t120), 3))
print("v - u:", round(3 * math.cos(t120) - 2, 3))
print("v1 9a decimal:", round(-1 / 14, 3), round(1 / 7, 3), round(3 / 14, 3), " v1 9b:", round(4 / 3, 3))
print("ponta da proj Q10:", round(-1 - 15 / 11, 3), round(-1 - 6 / 11, 3), round(-2 + 6 / 11, 3))

for pr in problemas:
    print("PROBLEMA", pr)
print("SEM PROBLEMAS" if not problemas else f"{len(problemas)} problema(s)")
