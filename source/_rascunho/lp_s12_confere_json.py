# Confere os JSON do lote lp_s12 contra contas refeitas aqui (independente do validar.py).
# Uso: python -I lp_s12_confere_json.py
import json, os, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "dados")
ARQS = [f"lp_s12_p{i}.json" for i in range(1, 5)]
falhas = []

def ok(rot, cond, extra=""):
    if not cond:
        falhas.append(rot)
    print(("ok      " if cond else "FALHA   ") + rot + (f"  {extra}" if extra else ""))

def b8(n):
    return format(n & 0xFF, "08b")

def s8(bits):
    v = int(bits, 2)
    return v - 256 if v >= 128 else v

def palavras(s):
    return len(re.findall(r"\S+", s))

# 1. bytes de controle e leitura
dados = {}
for a in ARQS:
    p = os.path.join(BASE, a)
    raw = open(p, "rb").read()
    ctrl = [b for b in raw if b < 32 and b not in (9, 10, 13)]
    ok(f"{a}: sem bytes de controle", not ctrl, str(ctrl[:5]))
    ok(f"{a}: sem BOM", not raw.startswith(b"\xef\xbb\xbf"))
    dados[a] = json.loads(raw.decode("utf-8"))

qs = [q for a in ARQS for q in dados[a]["questoes"]]
ok("24 questões", len(qs) == 24, str(len(qs)))
ok("máximo 6 por arquivo", all(len(dados[a]["questoes"]) <= 6 for a in ARQS))
ok("disciplina lp", all(dados[a]["disciplina"] == "lp" for a in ARQS))
ok("teoria só na p1", [len(dados[a]["semanas"]) for a in ARQS] == [2, 0, 0, 0])

ids_esperados = [f"lp-s1-p{i:02d}" for i in range(1, 13)] + [f"lp-s2-p{i:02d}" for i in range(1, 13)]
ok("ids na ordem esperada", [q["id"] for q in qs] == ids_esperados)

# 2. níveis: 4 de cada por semana
for s in (1, 2):
    c = Counter(q["nivel"] for q in qs if q["semana"] == s)
    ok(f"semana {s}: 4 por nível", c == Counter({1: 4, 2: 4, 3: 4}), str(dict(c)))
ok("origem Prévia · ementa", all(q["origem"] == "Prévia · ementa" for q in qs))

# 3. resposta marcada = conta refeita
certa = {q["id"]: [a["t"] for a in q["alternativas"] if a.get("certa")][0] for q in qs}
esperado = {
    "lp-s1-p01": "O VisuAlg 3.0",
    "lp-s1-p02": "A ULA (unidade lógica e aritmética)",
    "lp-s1-p03": "Na memória RAM",
    "lp-s1-p04": str(2 ** 7),
    "lp-s1-p05": "Em outubro, 37 boletos venceram sem pagamento, 12 a mais que em setembro.",
    "lp-s1-p06": "3, 2, 1, 4",
    "lp-s1-p07": "1500 pelo barramento de endereço; o conteúdo, pelo de dados",
    "lp-s1-p08": f"{3 * 1024 * 8:,}".replace(",", "."),
    "lp-s1-p09": "I banco de dados; II inteligência artificial; III teoria da computação; IV computação gráfica",
    "lp-s1-p10": f"{4 * 1024 // 4:,}".replace(",", "."),
    "lp-s1-p11": str(len("Conciliação".encode("utf-8"))),
    "lp-s1-p12": str(7 + 5 + 5),
    "lp-s2-p01": format(25, "b"),
    "lp-s2-p02": str(int("110100", 2)),
    "lp-s2-p03": format(0b10110110, "X"),
    "lp-s2-p04": f"{2 ** 8} valores; o maior é {2 ** 8 - 1}",
    "lp-s2-p05": format(0b1011 + 0b0111, "b"),
    "lp-s2-p06": b8(-20),
    "lp-s2-p07": f"({0xFF}, {0x80}, {0x00})",
    "lp-s2-p08": format(int("57", 8), "X"),
    "lp-s2-p09": f"{b8(0b00001111 + 0b11110110)}, que vale {s8(b8(0b00001111 + 0b11110110))}",
    "lp-s2-p10": str(next(n for n in range(1, 64) if 2 ** n >= 1000)),
    "lp-s2-p11": "#" + format(200, "02X") * 3,
    "lp-s2-p12": str(s8(b8(100 + 50))).replace("-", "−"),
}
for k, v in esperado.items():
    ok(f"{k}: certa = {v}", certa[k] == v, f"no JSON: {certa[k]}")

# 4. valores das alternativas erradas citados nos 'erro' (amostra das contas)
extra = [
    ("37 = 100101", format(37, "b") == "100101"),
    ("setembro = 37 − 12 = 25", 37 - 12 == 25),
    ("10010100 com sinal = −108", s8("10010100") == -108),
    ("11101100 sem sinal = 236", int("11101100", 2) == 236),
    ("10010100 + 00010100 = 10101000", b8(0b10010100 + 0b00010100) == "10101000"),
    ("11101100 + 00010100 = 100000000", format(0b11101100 + 0b00010100, "b") == "100000000"),
    ("−128 + 64 + 32 + 8 + 4 = −20", -128 + 64 + 32 + 8 + 4 == -20),
    ("128 + 32 + 16 + 4 + 2 = 182", 128 + 32 + 16 + 4 + 2 == 182),
    ("6B = 107", 0x6B == 107),
    ("B3 = 179", 0xB3 == 179),
    ("57 hex = 87", 0x57 == 87),
    ("755 octal = 111 101 101", format(0o755, "b") == "111101101"),
    ("BIGINT: 4096 / 8 = 512", 4096 // 8 == 512),
    ("−128 + 64 + 32 + 16 + 4 + 2 = −10", -128 + 64 + 32 + 16 + 4 + 2 == -10),
    ("inverter 11110110 = 00001001", b8(~0b11110110) == "00001001"),
    ("15 + 246 − 256 = 5", 15 + 246 - 256 == 5),
    ("relógio: 5 + 9 − 12 = 2 = 5 − 3", 5 + 9 - 12 == 2 == 5 - 3),
    ("placar: 60 − 100 = −40", 60 - 100 == -40),
    ("relógio 8 bits: 100 + 27 = 127, mais 23 → −106", 100 + 27 == 127 and -128 + 22 == -106 and 27 + 23 == 50),
    ("−128 + 16 + 4 + 2 = −106", -128 + 16 + 4 + 2 == -106),
    ("8C = 140", 0x8C == 140),
    ("C5 = 197", 0xC5 == 197),
    ("200 = 128 + 64 + 8", 128 + 64 + 8 == 200),
    ("11001000 restos invertidos = 13 hex", format(int("00010011", 2), "X") == "13"),
    ("1011 + 0111: 1100 = 12, 0010 = 2, 1111 = 15, 10000 = 16",
     [int(x, 2) for x in ("1100", "0010", "1111", "10000")] == [12, 2, 15, 16]),
    ("1024 − 1000 = 24 códigos livres", 1024 - 1000 == 24),
    ("1000 − 512 = 488 faltam", 1000 - 512 == 488),
    ("excel DECABIN(-20) = 1111101100", format(1024 - 20, "010b") == "1111101100"),
    ("teoria 13 = 1101", format(13, "b") == "1101"),
    ("teoria 21 = 16 + 4 + 1", 16 + 4 + 1 == 21),
]
for rot, cond in extra:
    ok(rot, cond)

# 5. posições das certas
pos = Counter("ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in qs)
ok("nenhuma letra acima de 30%", max(pos.values()) / len(qs) <= 0.30, str(dict(sorted(pos.items()))))

# 6. tamanhos (alvo do BRIEF)
for a in ARQS:
    for s in dados[a]["semanas"]:
        for i, b in enumerate(s["blocos"]):
            n = palavras(b["texto"])
            ok(f"semana {s['semana']} bloco {i + 1}: {n} palavras (40 a 120)", 40 <= n <= 120)
        for k, t in s["jeitos"].items():
            n = palavras(t)
            ok(f"semana {s['semana']} jeito {k}: {n} palavras (50 a 120)", 50 <= n <= 120)
fora = []
for q in qs:
    for k in ("visual", "cotidiano", "trabalho", "erro", "confira", "atalho"):
        n = palavras(q["jeitos"][k])
        if not 35 <= n <= 110:
            fora.append(f"{q['id']}.{k}={n}")
    if not 3 <= len(q["jeitos"]["receita"]) <= 7:
        fora.append(f"{q['id']}.receita={len(q['jeitos']['receita'])}")
    if not 4 <= len(q["jeitos"]["conversa"]) <= 8:
        fora.append(f"{q['id']}.conversa={len(q['jeitos']['conversa'])}")
ok("jeitos das questões dentro do alvo", not fora, ", ".join(fora))

# 7. texto: hífen antes de algarismo fora de crase (sinal de menos errado)
def textos(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from textos(x)
    elif isinstance(o, dict):
        for x in o.values():
            yield from textos(x)
ruins = []
for a in ARQS:
    for t in textos(dados[a]):
        sem_codigo = re.sub(r"`[^`]*`", " ", t)
        if re.search(r"(^|[\s(,\[=])-\d", sem_codigo):
            ruins.append(t[:50])
ok("sem hífen como sinal de menos", not ruins, str(ruins[:3]))

print()
print("FALHAS:", falhas if falhas else "nenhuma")
