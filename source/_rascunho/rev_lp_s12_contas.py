# Revisor adversarial do lote lp_s12 (Logica, semanas 1 e 2, previa).
# Resolve cada enunciado do zero, sem olhar o campo "resposta", e compara
# com a alternativa marcada como certa no JSON. Depois refaz a conta
# descrita no "erro" de cada alternativa errada e confere o valor.
import json, os, sys
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
arqs = sorted(f for f in os.listdir(DADOS) if f.startswith("lp_s12_p") and f.endswith(".json"))
Q = {}
SEM = {}
for f in arqs:
    with open(os.path.join(DADOS, f), encoding="utf-8") as h:
        d = json.load(h)
    for s in d.get("semanas", []):
        SEM[s["semana"]] = s
    for q in d["questoes"]:
        Q[q["id"]] = q
print("arquivos:", arqs, "questoes:", len(Q))

falhas = []
def ok(rot, cond, extra=""):
    if not cond:
        falhas.append(rot)
    print(("ok      " if cond else "FALHA   ") + rot + ((" | " + str(extra)) if extra else ""))

def certa(qid):
    return [a["t"] for a in Q[qid]["alternativas"] if a.get("certa")][0]

def erradas(qid):
    return [a["t"] for a in Q[qid]["alternativas"] if not a.get("certa")]

def b8(n):
    return format(n & 0xFF, "08b")

def sinal8(bits):
    v = int(bits, 2)
    return v - 256 if v >= 128 else v

def num(t):
    # "24.576" -> 24576 ; "−106" -> -106
    return int(t.replace(".", "").replace("−", "-"))

# ================= SEMANA 1 =================
ok("s1p01 certa = VisuAlg", "VisuAlg" in certa("lp-s1-p01"), certa("lp-s1-p01"))
ok("s1p02 certa = ULA", certa("lp-s1-p02").startswith("A ULA"), certa("lp-s1-p02"))
ok("s1p03 certa = RAM", "RAM" in certa("lp-s1-p03"), certa("lp-s1-p03"))

# p04: quantos simbolos com 7 bits
r = 2 ** 7
ok("s1p04 certa 2^7", num(certa("lp-s1-p04")) == r, r)
dis = {"127": 2 ** 7 - 1, "256": 2 ** 8, "14": 2 * 7, "49": 7 ** 2}
ok("s1p04 distratores", sorted(erradas("lp-s1-p04")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()))

# p05: dado x informacao. A unica alternativa com contexto (o que, quando, comparacao)
ok("s1p05 certa = boletos", "boletos" in certa("lp-s1-p05"))
ok("s1p05 37 em binario", format(37, "b") == "100101" and 37 < 256)
ok("s1p05 setembro = 25", 37 - 12 == 25)

# p06: ordem do ciclo por dependencias. 3 busca, 2 decodifica, 1 soma, 4 guarda
dep = {3: [], 2: [3], 1: [2], 4: [1]}
def valida(ordem):
    vistos = set()
    for e in ordem:
        if any(p not in vistos for p in dep[e]):
            return False
        vistos.add(e)
    return True
import itertools
validas = [o for o in itertools.permutations([1, 2, 3, 4]) if valida(o)]
ok("s1p06 unica ordem valida", validas == [(3, 2, 1, 4)], validas)
ok("s1p06 certa", certa("lp-s1-p06") == "3, 2, 1, 4")
for t in erradas("lp-s1-p06"):
    ok("s1p06 errada invalida " + t, not valida(tuple(int(x) for x in t.split(", "))))
alts6 = [a["t"] for a in Q["lp-s1-p06"]["alternativas"]]
com3 = [t for t in alts6 if t.startswith("3")]
ok("s1p06 atalho: tres comecam com 3", len(com3) == 3)
ok("s1p06 atalho: duas terminam com 4", len([t for t in com3 if t.endswith("4")]) == 2)

ok("s1p07 certa = endereco/dados", certa("lp-s1-p07").startswith("1500 pelo barramento de endereço; o conteúdo, pelo de dados"))

# p08: 3 KB (1024) em bits
r = 3 * 1024 * 8
ok("s1p08 certa", num(certa("lp-s1-p08")) == r, r)
dis = {"3.072": 3 * 1024, "24.000": 3 * 1000 * 8, "384": Fraction(3 * 1024, 8), "24": 3 * 8}
ok("s1p08 distratores", sorted(erradas("lp-s1-p08")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()))
# trabalho: 10 MB numa conexao de 10 Mbps leva pelo menos 8 s (nas duas convencoes)
ok("s1p08 trabalho 8 s (MB=10^6)", Fraction(10 * 10 ** 6 * 8, 10 * 10 ** 6) == 8)
ok("s1p08 trabalho >= 8 s (MB=2^20)", Fraction(10 * 2 ** 20 * 8, 10 * 10 ** 6) >= 8)

# p09: areas
ok("s1p09 certa", certa("lp-s1-p09") == "I banco de dados; II inteligência artificial; III teoria da computação; IV computação gráfica")
alts9 = [a["t"] for a in Q["lp-s1-p09"]["alternativas"]]
s1 = [t for t in alts9 if "IV redes" not in t]
s2 = [t for t in s1 if "III segurança" not in t and "III engenharia" not in t]
ok("s1p09 atalho: sobram tres", len(s2) == 3, s2)

# p10: 4 KB / palavra de 32 bits
r = 4 * 1024 // (32 // 8)
ok("s1p10 certa", num(certa("lp-s1-p10")) == r, r)
dis = {"128": 4 * 1024 // 32, "4.096": 4 * 1024, "1.000": 4 * 1000 // 4, "32.768": 4 * 1024 * 8}
ok("s1p10 distratores", sorted(erradas("lp-s1-p10")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()))
ok("s1p10 confira bits", 4 * 1024 * 8 // 32 == r)
ok("s1p10 BIGINT 512", 4096 // 8 == 512)
pot2 = lambda n: n > 0 and n & (n - 1) == 0
ok("s1p10 atalho: so 1.000 nao e potencia de 2", [t for t in [a["t"] for a in Q["lp-s1-p10"]["alternativas"]] if not pot2(num(t))] == ["1.000"])

# p11: Conciliacao em UTF-8
w = "Conciliação"
r = len(w.encode("utf-8"))
ok("s1p11 certa", num(certa("lp-s1-p11")) == r, r)
fora = [c for c in w if ord(c) > 127]
dis = {"11": len(w), "22": 2 * len(w), "12": len(w) + 1, "104": r * 8}
ok("s1p11 distratores", sorted(erradas("lp-s1-p11")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()))
ok("s1p11 9 + 2", len(w) - len(fora) == 9 and len(fora) == 2)
ok("s1p11 mojibake", w.encode("utf-8").decode("cp1252") == "ConciliaÃ§Ã£o")

# p12: maquina de acumulador
mem = {10: 7, 11: 5, 12: 0}
acc = mem[10]; acc += mem[11]; acc += mem[11]; mem[12] = acc
ok("s1p12 certa", num(certa("lp-s1-p12")) == mem[12], mem[12])
dis = {"12": 7 + 5, "32": 10 + 11 + 11, "0": 0, "5": 5}
ok("s1p12 distratores", sorted(erradas("lp-s1-p12")) == sorted(dis) and all(num(k) == v != mem[12] for k, v in dis.items()))

# ================= SEMANA 2 =================
# p01: 25 para binario por divisoes sucessivas
n, restos = 25, []
while n:
    restos.append(n % 2); n //= 2
r = "".join(map(str, restos[::-1]))
ok("s2p01 certa", certa("lp-s2-p01") == r, r)
ok("s2p01 tabela", [l[2] for l in Q["lp-s2-p01"]["tabela"]["linhas"]] == [str(x) for x in restos])
dis = {"10011": "".join(map(str, restos)), "1100": format(12, "b"), "10101": format(2, "b") + format(5, "b"), "11010": format(26, "b")}
ok("s2p01 distratores", sorted(erradas("lp-s2-p01")) == sorted(dis) and all(k == v != r for k, v in dis.items()))
ok("s2p01 valores citados", int("10011", 2) == 19 and int("10101", 2) == 21 and int("11010", 2) == 26)
# atalho
alts = [a["t"] for a in Q["lp-s2-p01"]["alternativas"]]
impar = [t for t in alts if t.endswith("1")]
ok("s2p01 atalho impar elimina 1100 e 11010", sorted(set(alts) - set(impar)) == ["1100", "11010"])
ok("s2p01 atalho segundo bit 1", [t for t in impar if len(t) == 5 and t[1] == "1"] == ["11001"])

# p02: 110100 para decimal
b = "110100"
r = sum(2 ** i for i, c in enumerate(b[::-1]) if c == "1")
ok("s2p02 certa", num(certa("lp-s2-p02")) == r, r)
dis = {"11": int(b[::-1], 2), "3": b.count("1"),
       "26": sum(2 ** (i - 1) for i, c in enumerate(b[::-1]) if c == "1" and i >= 1),
       "104": sum(2 ** (i + 1) for i, c in enumerate(b[::-1]) if c == "1")}
ok("s2p02 distratores", sorted(erradas("lp-s2-p02")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()), dis)
ok("s2p02 atalho par e faixa 32..63", [t for t in [a["t"] for a in Q["lp-s2-p02"]["alternativas"]] if num(t) % 2 == 0 and 32 <= num(t) <= 63] == ["52"])

# p03: 10110110 para hexadecimal
b = "10110110"
r = format(int(b, 2), "X")
ok("s2p03 certa", certa("lp-s2-p03") == r, r)
g = [b[:4], b[4:]]
dis = {"6B": format(int(g[1], 2), "X") + format(int(g[0], 2), "X"),
       "266": "".join(str(int(x, 2)) for x in ["10", "110", "110"]),
       "116": str(int(g[0], 2)) + str(int(g[1], 2)),
       "182": str(int(b, 2))}
ok("s2p03 distratores", sorted(erradas("lp-s2-p03")) == sorted(dis) and all(k == v != r for k, v in dis.items()), dis)
ok("s2p03 266 = octal", format(int(b, 2), "o") == "266")
ok("s2p03 6B = 107", 0x6B == 107)

# p04: 8 bits sem sinal
ok("s2p04 certa", certa("lp-s2-p04") == f"{2**8} valores; o maior é {2**8-1}")
dis = {"256 valores; o maior é 256": None, "255 valores; o maior é 255": None,
       f"{8**2} valores; o maior é {8**2-1}": None, f"{2*8} valores; o maior é {2*8-1}": None}
ok("s2p04 distratores", sorted(erradas("lp-s2-p04")) == sorted(dis))

# p05: 1011 + 0111
x, y = 0b1011, 0b0111
r = format(x + y, "b")
ok("s2p05 certa", certa("lp-s2-p05") == r, r)
def soma_errada(a, b, col_err):
    a, b = a[::-1], b[::-1]; c = 0; out = []
    for i in range(len(a)):
        t = int(a[i]) + int(b[i]) + c
        bit = t % 2
        if i == col_err:
            bit = 0
        out.append(str(bit)); c = t // 2
    if c: out.append("1")
    return "".join(out[::-1])
dis = {"1100": format(x ^ y, "04b"), "0010": format((x + y) & 0xF, "04b"),
       "1111": format(x | y, "04b"), "10000": soma_errada("1011", "0111", 1)}
ok("s2p05 distratores", sorted(erradas("lp-s2-p05")) == sorted(dis) and all(k == v != r for k, v in dis.items()), dis)
ok("s2p05 valores citados", int("1100", 2) == 12 and int("0010", 2) == 2 and int("1111", 2) == 15 and int("10000", 2) == 16)
# tabela de colunas
a, bb = "1011"[::-1], "0111"[::-1]; c = 0; linhas = []
for i in range(4):
    t = int(a[i]) + int(bb[i]) + c
    linhas.append((t, t % 2, t // 2)); c = t // 2
tab = Q["lp-s2-p05"]["tabela"]["linhas"]
ok("s2p05 tabela", [(int(l[2]), int(l[3]), int(l[4])) for l in tab[:4]] == linhas and tab[4][3] == "1", linhas)

# p06: -20 em complemento de 2
r = b8(-20)
ok("s2p06 certa", certa("lp-s2-p06") == r, r)
dis = {"10010100": "1" + format(20, "07b"), "11101011": b8(~20), "00010100": b8(20),
       "11101000": None}
# atalho errado: copia os zeros da direita e inverte a partir do primeiro 1 (inclusive)
s20 = b8(20); k = len(s20) - 1 - s20[::-1].index("1")
dis["11101000"] = "".join("1" if ch == "0" else "0" for ch in s20[:k + 1]) + s20[k + 1:]
ok("s2p06 distratores", sorted(erradas("lp-s2-p06")) == sorted(dis) and all(k2 == v != r for k2, v in dis.items()), dis)
ok("s2p06 10010100 vale -108", sinal8("10010100") == -108)
ok("s2p06 11101000 vale -24", sinal8("11101000") == -24)
ok("s2p06 Excel DECABIN(-20) 10 bits", format((-20) & 0x3FF, "010b") == "1111101100")
ok("s2p06 conversa 10010100 + 00010100", b8(0b10010100 + 0b00010100) == "10101000")
ok("s2p06 236 sem sinal", int(r, 2) == 236 and 1000 - 20 == 980)
ok("s2p06 pesos", -128 + 64 + 32 + 8 + 4 == -20)
# atalho correto: copia 100, inverte 00010
ok("s2p06 atalho certo", "".join("1" if ch == "0" else "0" for ch in "00010") + "100" == r)

# p07: #FF8000
cod = "FF8000"
r = tuple(int(cod[i:i + 2], 16) for i in (0, 2, 4))
ok("s2p07 certa", certa("lp-s2-p07") == "(%d, %d, %d)" % r, r)
dis = {"(255, 80, 0)": (255, int("80"), 0), "(0, 128, 255)": r[::-1],
       "(256, 128, 0)": (16 * 16, 128, 0), "(15, 8, 0)": tuple(int(cod[i], 16) for i in (0, 2, 4))}
ok("s2p07 distratores", sorted(erradas("lp-s2-p07")) == sorted(dis) and all(k == "(%d, %d, %d)" % v for k, v in dis.items()))

# p08: 57 octal para hexadecimal
v = int("57", 8)
r = format(v, "X")
ok("s2p08 certa", certa("lp-s2-p08") == r, r)
bits = "".join(format(int(ch), "03b") for ch in "57")
dis = {"B3": format(int(bits[:4], 2), "X") + format(int(bits[4:], 2), "X"),
       "39": format(57, "X"), "47": str(v), "57": format(int("".join(format(int(ch), "04b") for ch in "57"), 2), "X")}
ok("s2p08 distratores", sorted(erradas("lp-s2-p08")) == sorted(dis) and all(k == v2 != r for k, v2 in dis.items()), dis)
ok("s2p08 binario 101111", bits == "101111")
ok("s2p08 0o100 = 64 = 0x40", int("100", 8) == 64 and format(64, "X") == "40")
ok("s2p08 B3 = 179 ; 57h = 87", 0xB3 == 179 and 0x57 == 87)
ok("s2p08 permissao 755", "".join(format(int(ch), "03b") for ch in "755") == "111101101")
# atalho: valores < 0x40 -> primeiro algarismo 0..3
sobra = [t for t in [a["t"] for a in Q["lp-s2-p08"]["alternativas"]] if int(t, 16) < 0x40]
ok("s2p08 atalho sobram 39 e 2F", sorted(sobra) == ["2F", "39"], sobra)

# p09: 00001111 + 11110110 em 8 bits
t = 0b00001111 + 0b11110110
r = "%s, que vale %d" % (b8(t), sinal8(b8(t)))
ok("s2p09 certa", certa("lp-s2-p09") == r, r)
dis = {"100000101, que vale 261": (format(t, "b"), t),
       "11111001, que vale −7": (b8(0b00001111 ^ 0b11110110), sinal8(b8(0b00001111 ^ 0b11110110))),
       "00011001, que vale 25": (b8(15 + 10), 25),
       "10000101, que vale −123": ("1" + format(t, "b")[2:], sinal8("1" + format(t, "b")[2:]))}
ok("s2p09 distratores", sorted(erradas("lp-s2-p09")) == sorted(dis) and all(k.replace("−", "-") == "%s, que vale %d" % vv for k, vv in dis.items()), dis)
ok("s2p09 11110110 = -10", sinal8("11110110") == -10 and int("11110110", 2) == 246)
ok("s2p09 inverter+1", format((~0b11110110) & 0xFF, "08b") == "00001001" and ((~0b11110110) & 0xFF) + 1 == 10)
ok("s2p09 relogio", (5 + 9) % 12 == 2 and (15 + 246) % 256 == 5)

# p10: menor n com 2^n >= 1000
n = 0
while 2 ** n < 1000:
    n += 1
ok("s2p10 certa", num(certa("lp-s2-p10")) == n, n)
k = 0
while k * k < 1000:
    k += 1
dis = {"9": 9, "12": 3 * 4, "32": k, "1.000": 1000}
ok("s2p10 distratores", sorted(erradas("lp-s2-p10")) == sorted(dis) and all(num(a) == b2 != n for a, b2 in dis.items()))
ok("s2p10 faltam 488 / sobram 24", 1000 - 512 == 488 and 1024 - 1000 == 24)
ok("s2p10 faixa 513..1024 da 10", all((m - 1).bit_length() == 10 for m in range(513, 1025)) and (512 - 1).bit_length() == 9)

# p11: cinza 200
q16, r16 = divmod(200, 16)
par = format(q16, "X") + format(r16, "X")
r = "#" + par * 3
ok("s2p11 certa", certa("lp-s2-p11") == r, r)
dec = Fraction(200, 16)
dis = {"#8C8C8C": "#" + par[::-1] * 3, "#C5C5C5": "#" + ("C" + str(int((dec - int(dec)) * 10))) * 3,
       "#131313": "#" + format(int(format(200, "08b")[::-1], 2), "02X") * 3, "#C8": "#" + par}
ok("s2p11 distratores", sorted(erradas("lp-s2-p11")) == sorted(dis) and all(k == v != r for k, v in dis.items()), dis)
ok("s2p11 8C=140 C5=197", 0x8C == 140 and 0xC5 == 197)

# p12: 100 + 50 em 8 bits com sinal
t = b8(100 + 50)
r = sinal8(t)
ok("s2p12 certa", num(certa("lp-s2-p12")) == r, r)
dis = {"150": 150, "−22": -int(t[1:], 2), "127": 127, "106": -r}
ok("s2p12 distratores", sorted(erradas("lp-s2-p12")) == sorted(dis) and all(num(k) == v != r for k, v in dis.items()))
ok("s2p12 bits", t == "10010110" and b8(100) == "01100100" and b8(50) == "00110010")
ok("s2p12 relogio 27+23", 127 - 100 == 27 and -128 + (23 - 1) == -106 and 27 + 23 == 50)
ok("s2p12 placar 60 -> -40", 60 - 100 == -40)

# ================= TEORIA =================
ok("teo 1011=11", int("1011", 2) == 11)
ok("teo 13=1101", format(13, "b") == "1101")
ok("teo D7/327/215", format(0b11010111, "X") == "D7" and format(0b11010111, "o") == "327" and 0b11010111 == 215)
ok("teo 0110+0011", format(0b0110 + 0b0011, "04b") == "1001")
ok("teo -5", b8(-5) == "11111011" and b8(~5) == "11111010")
ok("teo 256^3", 256 ** 3 == 16777216)
ok("teo 21", 16 + 4 + 1 == 21)
ok("teo ASCII A=65", ord("A") == 65)
ok("teo euro 3 bytes", len("€".encode("utf-8")) == 3)
ok("teo emoji comum 4 bytes", len("\U0001F600".encode("utf-8")) == 4)
ok("teo emoji de 3 bytes existe (U+2705)", len("✅".encode("utf-8")) == 3)
ok("lab s1 sete da direita = 127", sum(2 ** i for i in range(7)) == 127)
ok("lab s2 5 inverte +1", (((~5) & 255) + 1) & 255 == 0b11111011 and (((~5) & 255) + 1) - 256 == -5)

print()
print("FALHAS:", falhas if falhas else "nenhuma")
