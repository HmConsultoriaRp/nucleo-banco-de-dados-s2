# Confere os arquivos ga_s2a_p*.json contra contas refeitas em Python.
# Uso: python -I ga_s2a_confere_json.py <pasta dados>
import json, math, os, re, sys
from fractions import Fraction as F

sys.stdout.reconfigure(encoding="utf-8")
pasta = sys.argv[1]
arqs = sorted(n for n in os.listdir(pasta) if n.startswith("ga_s2a_p") and n.endswith(".json"))

u = (F(1), F(4), F(3)); v = (F(-1), F(1), F(-1)); w = (F(-2), F(-1, 2), F(5)); z = (F(-1), F(2), F(-3))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross(a, b): return (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0])
def comp(a, b): return tuple(x * y for x, y in zip(a, b))
def soma(a, b): return tuple(x + y for x, y in zip(a, b))
def neg(a): return tuple(-x for x in a)
def meio_sem_menos(a, b): return (a[1]*b[2] - a[2]*b[1], a[0]*b[2] - a[2]*b[0], a[0]*b[1] - a[1]*b[0])
w_mais = (F(-2), F(1, 2), F(5))

# valor esperado de cada alternativa, na ordem A..E (texto antes do ';' quando houver)
esperado = {
    "ga-s2-l2q1a": [comp(u, v), dot(u, v), dot(u, v), F(-1) + F(4) + F(3), cross(u, v)],
    "ga-s2-l2q1b": [u[0]*w[0] + u[1]*F(1, 2) + u[2]*w[2], comp(u, w), u[0]*w[0] + u[1]*F(-2) + u[2]*w[2], dot(u, w), sum(abs(x*y) for x, y in zip(u, w))],
    "ga-s2-l2q1c": [dot(u, z), F(-1) + F(8) + F(9), comp(u, z), sum(abs(x*y) for x, y in zip(u, z)), sum(soma(u, z))],
    "ga-s2-l2q1d": [v[0]*w[0] + v[1]*F(1, 2) + v[2]*w[2], comp(v, w), F(-2) + F(-1, 2) + F(-5), F(-3 - 1, 2), dot(v, w)],
    "ga-s2-l2q1e": [F(-1) + F(2) + F(-3), comp(v, z), dot(v, z), sum(soma(v, z)), F(1) + F(2) + F(-3)],
    "ga-s2-l2q1f": [w[0]*z[0] + F(1, 2)*z[1] + w[2]*z[2], dot(w, z), comp(w, z), F(-2) + F(-1) + F(-15), sum(soma(w, z))],
    "ga-s2-l2q1g": ["raiz26", comp(u, u), sum(u) ** 2, dot(u, u), sum(u)],
    "ga-s2-l2q1h": [dot(v, v), F(-1) + F(1) + F(-1), "raiz3", sum(v) ** 2, comp(v, v)],
    "ga-s2-l2q1i": [F(4) + F(-1, 4) + F(25), F(4) + F(1, 2) + F(25), dot(w, w), "raiz117/2", comp(w, w)],
    "ga-s2-l2q1j": [F(-1) + F(4) + F(-9), "raiz14", comp(z, z), sum(z) ** 2, dot(z, z)],
    "ga-s2-l2q1k": [meio_sem_menos(u, v), cross(u, v), cross(v, u), comp(u, v), dot(u, v)],
    "ga-s2-l2q1l": [meio_sem_menos(u, w), comp(u, w), cross(w, u), cross(u, w), cross(u, w_mais)],
    "ga-s2-l2q1m": [cross(v, w), meio_sem_menos(v, w), comp(v, w), (F(11, 2), F(7), F(3, 2)), cross(w, v)],
    "ga-s2-l2q1n": [cross(v, w), meio_sem_menos(w, v), cross(w, v), dot(w, v), comp(w, v)],
}
gabarito = {
    "ga-s2-l2q1a": dot(u, v), "ga-s2-l2q1b": dot(u, w), "ga-s2-l2q1c": dot(u, z), "ga-s2-l2q1d": dot(v, w),
    "ga-s2-l2q1e": dot(v, z), "ga-s2-l2q1f": dot(w, z), "ga-s2-l2q1g": dot(u, u), "ga-s2-l2q1h": dot(v, v),
    "ga-s2-l2q1i": dot(w, w), "ga-s2-l2q1j": dot(z, z), "ga-s2-l2q1k": cross(u, v), "ga-s2-l2q1l": cross(u, w),
    "ga-s2-l2q1m": cross(v, w), "ga-s2-l2q1n": cross(w, v),
}
gab_lista = {  # gabarito da propria lista (pagina 2 do PDF)
    "ga-s2-l2q1a": F(0), "ga-s2-l2q1b": F(11), "ga-s2-l2q1c": F(-2), "ga-s2-l2q1d": F(-7, 2), "ga-s2-l2q1e": F(6),
    "ga-s2-l2q1f": F(-14), "ga-s2-l2q1g": F(26), "ga-s2-l2q1h": F(3), "ga-s2-l2q1i": F(117, 4), "ga-s2-l2q1j": F(14),
    "ga-s2-l2q1k": (F(-7), F(-2), F(5)), "ga-s2-l2q1l": (F(43, 2), F(-11), F(15, 2)),
    "ga-s2-l2q1m": (F(9, 2), F(7), F(5, 2)), "ga-s2-l2q1n": (F(-9, 2), F(-7), F(-5, 2)),
}

def num(s):
    s = s.strip().replace("−", "-")
    m = re.fullmatch(r"√(\d+)(?:/(\d+))?", s)
    if m:
        return "raiz" + m.group(1) + ("/" + m.group(2) if m.group(2) else "")
    return F(s)

def parse(t):
    t = t.split(";")[0].strip()
    if t.startswith("("):
        return tuple(num(p) for p in t.strip("()").split(","))
    return num(t)

problemas = []
def falha(msg):
    problemas.append(msg)
    print("ERRO ", msg)

total = 0
pos = {}
for arq in arqs:
    caminho = os.path.join(pasta, arq)
    bruto = open(caminho, "rb").read()
    ctrl = [b for b in bruto if b < 0x20 and b not in (0x0A, 0x0D)]
    print(f"{arq}: {len(bruto)} bytes; bytes de controle fora de \\n/\\r: {len(ctrl)}")
    if ctrl:
        falha(f"{arq}: bytes de controle {set(ctrl)}")
    d = json.loads(bruto.decode("utf-8"))
    for s in d.get("semanas", []):
        for i, b in enumerate(s["blocos"]):
            n = len(b["texto"].split())
            print(f"     teoria bloco {i + 1}: {n} palavras")
            if not 40 <= n <= 120: falha(f"teoria bloco {i + 1} com {n} palavras")
        for k, t in s["jeitos"].items():
            n = len(t.split())
            print(f"     teoria jeito {k}: {n} palavras")
            if not 50 <= n <= 120: falha(f"teoria jeito {k} com {n} palavras")
    for q in d["questoes"]:
        total += 1
        qid = q["id"]
        alts = q["alternativas"]
        for i, a in enumerate(alts):
            if re.search(r"(^|[\s(,\[=])-\d", a["t"]):
                falha(f"{qid} alt {'ABCDE'[i]} com hífen no lugar de −")
            val = parse(a["t"])
            if val != esperado[qid][i]:
                falha(f"{qid} alt {'ABCDE'[i]}: texto {a['t']} != conta {esperado[qid][i]}")
            if a.get("certa"):
                pos[qid] = "ABCDE"[i]
                if val != gabarito[qid] or val != gab_lista[qid]:
                    falha(f"{qid}: certa {a['t']} não bate com o gabarito")
        # jeitos: tamanho
        for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
            n = len(q["jeitos"][k].split())
            if not 35 <= n <= 110:
                falha(f"{qid}.{k}: {n} palavras (alvo 35 a 110)")
        if not 3 <= len(q["jeitos"]["receita"]) <= 7: falha(f"{qid}: receita fora de 3 a 7")
        if not 4 <= len(q["jeitos"]["conversa"]) <= 8: falha(f"{qid}: conversa fora de 4 a 8")
        # figura: cada ponta de vetor tem de ser um vetor conhecido
        conhecidos = {
            "u": u, "v": v, "w": w, "z": z, "u × v": cross(u, v), "u × w": cross(u, w),
            "v × w": cross(v, w), "w × v": cross(w, v),
        }
        if "figura" in q:
            for it in q["figura"]["itens"]:
                if it["tipo"] == "vetor":
                    alvo = conhecidos[it["rot"]]
                    if tuple(F(x).limit_denominator(100) for x in it["ate"]) != alvo or it["de"] != [0, 0, 0]:
                        falha(f"{qid}: vetor {it['rot']} da figura {it['ate']} != {alvo}")
                if it["tipo"] == "poligono":
                    p = [tuple(F(x).limit_denominator(100) for x in pt) for pt in it["pts"]]
                    a, b = p[1], p[3]
                    if p[0] != (0, 0, 0) or p[2] != soma(a, b):
                        falha(f"{qid}: paralelogramo inconsistente {it['pts']}")
                    # os lados tem de ser os dois vetores da questao
                    print(f"     {qid}: paralelogramo de {a} e {b}")

print("certas:", pos)
# contas citadas nos textos dos jeitos e da teoria
def ang(a, b):
    return math.degrees(math.acos(float(dot(a, b)) / math.sqrt(float(dot(a, a) * dot(b, b)))))
ref = {
    "angulo u,w 66,49": round(ang(u, w), 2) == 66.49,
    "angulo u,z 96,02": round(ang(u, z), 2) == 96.02,
    "angulo v,w 111,94": round(ang(v, w), 2) == 111.94,
    "angulo v,z 22,21": round(ang(v, z), 2) == 22.21,
    "angulo w,z 133,78": round(ang(w, z), 2) == 133.78,
    "cos v,z 0,9258": round(float(dot(v, z)) / math.sqrt(float(dot(v, v) * dot(z, z))), 4) == 0.9258,
    "b: |u||w| passa de 27": math.sqrt(float(dot(u, u) * dot(w, w))) > 27,
    "b: u.(2w) = 22": dot(u, tuple(2 * x for x in w)) == 22,
    "c: -2/(5,10*3,74) ~ -0,105": round(-2 / (5.10 * 3.74), 3) == -0.105,
    "c: 16/(5,10*3,74) ~ 0,84": round(16 / (5.10 * 3.74), 2) == 0.84,
    "d: v.(2w) = -7": dot(v, tuple(2 * x for x in w)) == -7,
    "e: |v+z|^2 = 29 = 3+12+14": dot(soma(v, z), soma(v, z)) == 29 == 3 + 2 * 6 + 14,
    "e: com 0 daria 17": 3 + 0 + 14 == 17,
    "e: SUM(V)*SUM(Z) = 2": sum(v) * sum(z) == 2,
    "f: |w-z|^2 = 285/4": dot(soma(w, neg(z)), soma(w, neg(z))) == F(285, 4) == dot(w, w) - 2 * dot(w, z) + dot(z, z),
    "g: sqrt26 ~ 5,10": round(math.sqrt(26), 2) == 5.10,
    "g: 25 < 26": 25 < 26,
    "i: 2w.2w = 117": dot(tuple(2 * x for x in w), tuple(2 * x for x in w)) == 117,
    "i: 29,25 / 29,5 / 28,75": (float(F(117, 4)), float(F(59, 2)), float(F(115, 4))) == (29.25, 29.5, 28.75),
    "k: |uxv| = sqrt78 ~ 8,83": dot(cross(u, v), cross(u, v)) == 78 and round(math.sqrt(78), 2) == 8.83,
    "k: (-7,2,5).u = 16": dot((F(-7), F(2), F(5)), u) == 16,
    "k: (-1,4,-3).u = 6": dot((F(-1), F(4), F(-3)), u) == 6,
    "k: (7,2,-5).u = 0": dot((F(7), F(2), F(-5)), u) == 0,
    "teoria: sqrt78/2 ~ 4,42": round(math.sqrt(78) / 2, 2) == 4.42,
    "teoria: proj z sobre v = (-2,2,-2)": tuple(dot(z, v) / dot(v, v) * x for x in v) == (-2, 2, -2),
    "l: |uxw| ~ 25,29": round(math.sqrt(float(dot(cross(u, w), cross(u, w)))), 2) == 25.29,
    "l: u x 2w = (43,-22,15)": cross(u, tuple(2 * x for x in w)) == (43, -22, 15),
    "l: (37/2,-11,17/2).u = 0 e .w = 11": dot(cross(u, w_mais), u) == 0 and dot(cross(u, w_mais), w) == 11,
    "l: y ciclico 3*(-2) - 1*5 = -11": 3 * (-2) - 1 * 5 == -11,
    "m: |vxw| ~ 8,69": round(math.sqrt(float(dot(cross(v, w), cross(v, w)))), 2) == 8.69,
    "m: (11/2,7,3/2).v = 0 e .w = -7": dot((F(11, 2), F(7), F(3, 2)), v) == 0 and dot((F(11, 2), F(7), F(3, 2)), w) == -7,
    "n: m + n = 0": soma(cross(v, w), cross(w, v)) == (0, 0, 0),
}
for k, ok in ref.items():
    print(("OK   " if ok else "ERRO ") + k)
    if not ok:
        problemas.append(k)
print(f"{total} questões conferidas")
print("TUDO OK" if not problemas else f"{len(problemas)} problema(s)")
