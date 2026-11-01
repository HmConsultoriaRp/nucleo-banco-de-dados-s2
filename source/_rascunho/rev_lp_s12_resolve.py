# Revisor adversarial (segunda passada) do lote lp_s12: Logica, semanas 1 e 2, previa.
# Resolve cada enunciado do zero, sem ler o campo "resposta", e compara com a
# alternativa marcada como certa. Refaz a conta de cada "erro" das erradas.
# Confere numeros citados nos jeitos, na teoria e no laboratorio.
import json, os, sys, itertools, re
from fractions import Fraction
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
AQUI = os.path.dirname(os.path.abspath(__file__))
DADOS = os.path.join(os.path.dirname(AQUI), "dados")
ARQS = sorted(f for f in os.listdir(DADOS) if f.startswith("lp_s12_p") and f.endswith(".json"))
Q, SEM = {}, {}
for f in ARQS:
    with open(os.path.join(DADOS, f), encoding="utf-8") as h:
        d = json.load(h)
    for s in d.get("semanas", []):
        SEM[s["semana"]] = s
    for q in d["questoes"]:
        Q[q["id"]] = q

FALHAS = []
def ck(rot, cond, info=""):
    if not cond:
        FALHAS.append(rot)
    print(("ok     " if cond else "FALHA  ") + rot + (("  | " + str(info)) if info != "" else ""))

def alts(qid):
    return [(a["t"], bool(a.get("certa"))) for a in Q[qid]["alternativas"]]
def certa(qid):
    c = [t for t, v in alts(qid) if v]
    assert len(c) == 1
    return c[0]
def erradas(qid):
    return sorted(t for t, v in alts(qid) if not v)
def n(t):
    return int(t.replace(".", "").replace("−", "-"))
def b8(x):
    return format(x & 0xFF, "08b")
def s8(bits):
    v = int(bits, 2)
    return v - 256 if bits[0] == "1" else v
def j(qid, k):
    return Q[qid]["jeitos"][k]
def texto_todo(qid):
    q = Q[qid]
    partes = [q["enunciado"], q["dica"], q["resposta"]]
    for a in q["alternativas"]:
        partes.append(a["t"]); partes.append(a.get("erro", ""))
    for k, v in q["jeitos"].items():
        if isinstance(v, str): partes.append(v)
        elif k == "receita": partes += v
        else: partes += [x["fala"] for x in v]
    return "\n".join(partes)

def distratores(qid, mapa, certo):
    # mapa: texto da alternativa errada -> valor que a conta do "erro" produz
    ck(qid + " conjunto das erradas", erradas(qid) == sorted(mapa), erradas(qid))
    for k, v in mapa.items():
        ck(qid + " erro de '" + k + "' reproduz o valor", v[0], v[1])
        ck(qid + " '" + k + "' difere da certa", v[2] != certo, (v[2], certo))

# ============================ SEMANA 1 ============================
# p04: 7 bits
r = 2 ** 7
ck("s1p04 certa", n(certa("lp-s1-p04")) == r, r)
distratores("lp-s1-p04", {
    "127": (2 ** 7 - 1 == 127, "2^7-1", 127),
    "256": (2 ** 8 == 256, "2^8", 256),
    "14": (2 * 7 == 14, "2*7", 14),
    "49": (7 ** 2 == 49, "7^2", 49)}, r)
ck("s1p04 tabela 1..7 bits", Q["lp-s1-p04"]["tabela"]["linhas"] == [[str(i), str(2 ** i)] for i in range(1, 8)])
ck("s1p04 A = 65", ord("A") == 65 and chr(65) == "A")

# p05: 37 - 12 = 25 citado no visual
ck("s1p05 setembro 25", 37 - 12 == 25 and "25" in j("lp-s1-p05", "visual"))
ck("s1p05 37 = 100101", format(37, "b") == "100101")

# p06: ordem por dependencias
dep = {3: set(), 2: {3}, 1: {2}, 4: {1}}
def valida(o):
    vis = set()
    for e in o:
        if not dep[e] <= vis: return False
        vis.add(e)
    return True
ords = [o for o in itertools.permutations([1, 2, 3, 4]) if valida(o)]
ck("s1p06 ordem unica", ords == [(3, 2, 1, 4)], ords)
ck("s1p06 certa", tuple(int(x) for x in certa("lp-s1-p06").split(", ")) == ords[0])
for t in erradas("lp-s1-p06"):
    ck("s1p06 errada viola dependencia " + t, not valida(tuple(int(x) for x in t.split(", "))))
todas = [t for t, _ in alts("lp-s1-p06")]
c3 = [t for t in todas if t.startswith("3")]
ck("s1p06 atalho: 3 comecam com 3, 2 terminam com 4", len(c3) == 3 and len([t for t in c3 if t.endswith("4")]) == 2)

# p07
ck("s1p07 certa", certa("lp-s1-p07").startswith("1500 pelo barramento de endereço; o conteúdo, pelo de dados"))
todas = [t for t, _ in alts("lp-s1-p07")]
ck("s1p07 atalho: duas com 1500 no de endereco", len([t for t in todas if t.startswith("1500 pelo barramento de endereço") or t.endswith("os dois pelo barramento de endereço")]) == 2)

# p08: 3 KB em bits
r = 3 * 1024 * 8
ck("s1p08 certa", n(certa("lp-s1-p08")) == r, r)
distratores("lp-s1-p08", {
    "3.072": (3 * 1024 == 3072, "bytes", 3072),
    "24.000": (3 * 1000 * 8 == 24000, "1000", 24000),
    "384": (Fraction(3072, 8) == 384, "3072/8", 384),
    "24": (3 * 8 == 24, "3*8", 24)}, r)
ck("s1p08 confira volta", Fraction(r, 8) == 3072 and Fraction(3072, 1024) == 3)
ck("s1p08 trabalho 8 s (mesmo prefixo)", Fraction(10 * 8, 10) == 8)
ck("s1p08 trabalho >= 8 s (MB = 2^20, Mbps = 10^6)", Fraction(10 * 2 ** 20 * 8, 10 * 10 ** 6) >= 8)

# p09
ck("s1p09 certa", certa("lp-s1-p09") == "I banco de dados; II inteligência artificial; III teoria da computação; IV computação gráfica")
todas = [t for t, _ in alts("lp-s1-p09")]
sobra = [t for t in todas if "IV redes" not in t and "III segurança" not in t]
ck("s1p09 atalho sobram tres", len(sobra) == 3, sobra)
sobra2 = [t for t in sobra if t.startswith("I banco de dados; II inteligência artificial")]
ck("s1p09 atalho fecha em uma", len(sobra2) == 1 and sobra2[0] == certa("lp-s1-p09"))

# p10: palavras
r = (4 * 1024) // (32 // 8)
ck("s1p10 certa", n(certa("lp-s1-p10")) == r, r)
distratores("lp-s1-p10", {
    "128": (4096 // 32 == 128, "4096/32", 128),
    "4.096": (4 * 1024 == 4096, "bytes", 4096),
    "1.000": (4000 // 4 == 1000, "4000/4", 1000),
    "32.768": (4096 * 8 == 32768, "bits", 32768)}, r)
ck("s1p10 confira bits", 32768 // 32 == r and r * 4 == 4096)
ck("s1p10 BIGINT 512", 4096 // 8 == 512)
pot = lambda x: x > 0 and x & (x - 1) == 0
ck("s1p10 atalho: so 1.000 nao e potencia de 2", [t for t, _ in alts("lp-s1-p10") if not pot(n(t))] == ["1.000"])

# p11: Conciliacao
w = "Conciliação"
r = len(w.encode("utf-8"))
fora = [c for c in w if ord(c) > 127]
ck("s1p11 certa", n(certa("lp-s1-p11")) == r, r)
distratores("lp-s1-p11", {
    "11": (len(w) == 11, "caracteres", 11),
    "22": (2 * len(w) == 22, "2 por letra", 22),
    "12": ((len(w) - 1) * 1 + 2 == 12, "so o ã", 12),
    "104": (r * 8 == 104, "bits", 104)}, r)
ck("s1p11 9 + 2", len(w) - len(fora) == 9 and fora == ["ç", "ã"])
ck("s1p11 mojibake cp1252", w.encode("utf-8").decode("cp1252") == "ConciliaÃ§Ã£o")
ck("s1p11 mojibake latin-1", w.encode("utf-8").decode("latin-1") == "ConciliaÃ§Ã£o")
# confira novo: numerar bytes da esquerda para a direita
pos, fim = 0, {}
for c in w:
    ini = pos + 1
    pos += len(c.encode("utf-8"))
    fim.setdefault(c, []).append((ini, pos))
ck("s1p11 confira: 'a' termina no 8", w.encode("utf-8")[:8] == b"Concilia")
ck("s1p11 confira: ç em 9-10, ã em 11-12, o em 13", fim["ç"] == [(9, 10)] and fim["ã"] == [(11, 12)] and fim["o"][-1] == (13, 13), fim)
ck("s1p11 bytes de ç e ã", "ç".encode("utf-8") == b"\xc3\xa7" and "ã".encode("utf-8") == b"\xc3\xa3")

# p12: acumulador
mem = {10: 7, 11: 5, 12: 0}
acc = mem[10]; acc += mem[11]; acc += mem[11]; mem[12] = acc
ck("s1p12 certa", n(certa("lp-s1-p12")) == mem[12], mem[12])
distratores("lp-s1-p12", {
    "12": (7 + 5 == 12, "uma soma so", 12),
    "32": (10 + 11 + 11 == 32, "enderecos", 32),
    "0": (True, "valor antigo", 0),
    "5": (True, "substituir", 5)}, mem[12])
ck("s1p12 confira de tras para frente", 17 - 5 - 5 == 7 == mem[10] and 12 - 5 - 5 == 2 != mem[10])
ck("s1p12 tabela enunciado", Q["lp-s1-p12"]["tabela"]["linhas"] == [["10", "7"], ["11", "5"], ["12", "0"]])

# ============================ SEMANA 2 ============================
# p01: 25
x, rest = 25, []
lin = []
while x:
    lin.append((x, x // 2, x % 2)); rest.append(x % 2); x //= 2
r = "".join(str(b) for b in reversed(rest))
ck("s2p01 certa", certa("lp-s2-p01") == r, r)
ck("s2p01 tabela", [[f"{a} ÷ 2", str(b), str(c)] for a, b, c in lin] == Q["lp-s2-p01"]["tabela"]["linhas"])
distratores("lp-s2-p01", {
    "10011": ("".join(map(str, rest)) == "10011" and int("10011", 2) == 19, "restos de cima para baixo = 19", "10011"),
    "1100": (format(12, "b") == "1100", "so o 12", "1100"),
    "10101": (format(2, "b") + format(5, "b") == "10101" and int("10101", 2) == 21, "algarismo a algarismo = 21", "10101"),
    "11010": (int("11010", 2) == 26 == 16 + 8 + 2, "26", "11010")}, r)
todas = [t for t, _ in alts("lp-s2-p01")]
imp = [t for t in todas if t.endswith("1")]
ck("s2p01 atalho", sorted(set(todas) - set(imp)) == ["1100", "11010"] and [t for t in imp if t[1] == "1"] == ["11001"])
ck("s2p01 confira", 1 + 8 + 16 == 25)

# p02: 110100
b = "110100"
r = sum(2 ** i for i, c in enumerate(reversed(b)) if c == "1")
ck("s2p02 certa", n(certa("lp-s2-p02")) == r, r)
distratores("lp-s2-p02", {
    "11": (int(b[::-1], 2) == 11, "espelhado", 11),
    "3": (b.count("1") == 3, "contou uns", 3),
    "26": (sum(2 ** (i - 1) for i, c in enumerate(reversed(b)) if c == "1") == 26, "uma posicao a menos", 26),
    "104": (sum(2 ** (i + 1) for i, c in enumerate(reversed(b)) if c == "1") == 104, "comecou em 2^1", 104)}, r)
ck("s2p02 confira 52 de volta", format(52, "b") == b)
ck("s2p02 atalho", [t for t, _ in alts("lp-s2-p02") if n(t) % 2 == 0 and 32 <= n(t) <= 63] == ["52"])

# p03: 10110110 -> hex
b = "10110110"
r = format(int(b, 2), "X")
ck("s2p03 certa", certa("lp-s2-p03") == r, r)
distratores("lp-s2-p03", {
    "6B": (format(int(b[4:], 2), "X") + format(int(b[:4], 2), "X") == "6B", "grupos trocados", "6B"),
    "266": (format(int(b, 2), "o") == "266", "octal", "266"),
    "116": (str(int(b[:4], 2)) + str(int(b[4:], 2)) == "116", "11 e 6 decimais", "116"),
    "182": (int(b, 2) == 182, "decimal", "182")}, r)
ck("s2p03 6B = 107 e B6 = 182", 0x6B == 107 and 0xB6 == 182 == 128 + 32 + 16 + 4 + 2)

# p04
ck("s2p04 certa", certa("lp-s2-p04") == f"{2 ** 8} valores; o maior é {2 ** 8 - 1}")
ck("s2p04 erradas", erradas("lp-s2-p04") == sorted(["256 valores; o maior é 256", "255 valores; o maior é 255",
                                                    f"{8 ** 2} valores; o maior é {8 ** 2 - 1}", f"{2 * 8} valores; o maior é {2 * 8 - 1}"]))
ck("s2p04 tabela", Q["lp-s2-p04"]["tabela"]["linhas"] == [[str(i), str(2 ** i), str(2 ** i - 1)] for i in range(1, 9)])
ck("s2p04 11111111 + 1", int("11111111", 2) + 1 == int("100000000", 2) == 256)

# p05: 1011 + 0111
a_, b_ = "1011", "0111"
r = format(int(a_, 2) + int(b_, 2), "b")
ck("s2p05 certa", certa("lp-s2-p05") == r, r)
def soma(a, b, zera_coluna=None):
    a, b = a[::-1], b[::-1]; c = 0; out = []; tab = []
    for i in range(len(a)):
        t = int(a[i]) + int(b[i]) + c
        bit = t % 2
        if i == zera_coluna: bit = 0
        tab.append((t, bit, t // 2)); out.append(str(bit)); c = t // 2
    if c: out.append("1")
    return "".join(reversed(out)), tab
xor = format(int(a_, 2) ^ int(b_, 2), "04b")
distratores("lp-s2-p05", {
    "1100": (xor == "1100" and int(xor, 2) == 12, "sem vai-um (xor) = 12", "1100"),
    "0010": (format((11 + 7) % 16, "04b") == "0010", "descarta 5o bit", "0010"),
    "1111": (format(0b1011 | 0b0111, "04b") == "1111", "ou logico", "1111"),
    "10000": (soma(a_, b_, 1)[0] == "10000", "escreveu 0 na 2a coluna", "10000")}, r)
_, tab = soma(a_, b_)
tt = Q["lp-s2-p05"]["tabela"]["linhas"]
ck("s2p05 tabela colunas", [(int(l[2]), int(l[3]), int(l[4])) for l in tt[:4]] == tab and tt[4][3] == "1", tab)
ck("s2p05 decimal", 11 + 7 == 18 == 16 + 2)

# p06: -20
r = b8(-20)
ck("s2p06 certa", certa("lp-s2-p06") == r, r)
s20 = b8(20)
k1 = s20.rfind("1")
inverte = lambda s: "".join("1" if c == "0" else "0" for c in s)
distratores("lp-s2-p06", {
    "10010100": ("1" + s20[1:] == "10010100" and s8("10010100") == -108, "sinal-magnitude, -108", "10010100"),
    "11101011": (inverte(s20) == "11101011", "complemento de 1", "11101011"),
    "00010100": (s20 == "00010100", "+20", "00010100"),
    "11101000": (inverte(s20[:k1 + 1]) + s20[k1 + 1:] == "11101000" and s8("11101000") == -24, "atalho errado, -24", "11101000")}, r)
ck("s2p06 atalho certo", inverte(s20[:k1]) + s20[k1:] == r)
ck("s2p06 Excel 10 bits", format((-20) & 0x3FF, "010b") == "1111101100" and "1111101100"[2:] == r)
ck("s2p06 conversa 10010100 + 00010100", b8(0b10010100 + 0b00010100) == "10101000")
ck("s2p06 soma com +20 da 2^8", int(r, 2) + 20 == 256)
ck("s2p06 sem sinal 236, odometro 980", int(r, 2) == 236 and 1000 - 20 == 980)
ck("s2p06 pesos", -128 + 64 + 32 + 8 + 4 == -20)
ck("s2p06 erro 10100 invertido", inverte("10100") == "01011")

# p07: #FF8000
cod = "FF8000"
rgb = tuple(int(cod[i:i + 2], 16) for i in (0, 2, 4))
ck("s2p07 certa", certa("lp-s2-p07") == "(%d, %d, %d)" % rgb, rgb)
distratores("lp-s2-p07", {
    "(255, 80, 0)": (True, "copiou 80", (255, 80, 0)),
    "(0, 128, 255)": (rgb[::-1] == (0, 128, 255), "ordem invertida", (0, 128, 255)),
    "(256, 128, 0)": (16 * 16 == 256, "FF = 16x16", (256, 128, 0)),
    "(15, 8, 0)": (tuple(int(cod[i], 16) for i in (0, 2, 4)) == (15, 8, 0), "so 1o algarismo", (15, 8, 0))}, rgb)
ck("s2p07 FF = 15*16+15", 15 * 16 + 15 == 255 and divmod(255, 16) == (15, 15) and divmod(128, 16) == (8, 0))

# p08: 57 octal -> hex
v = int("57", 8)
r = format(v, "X")
ck("s2p08 certa", certa("lp-s2-p08") == r, r)
bits = "".join(format(int(c), "03b") for c in "57")
distratores("lp-s2-p08", {
    "B3": (format(int(bits[:4], 2), "X") + format(int(bits[4:], 2), "X") == "B3", "agrupou pela esquerda", "B3"),
    "39": (format(57, "X") == "39", "57 decimal", "39"),
    "47": (str(v) == "47", "decimal", "47"),
    "57": (format(int("".join(format(int(c), "04b") for c in "57"), 2), "X") == "57", "4 bits por algarismo", "57")}, r)
ck("s2p08 binario e grupos", bits == "101111" and bits.zfill(8)[:4] == "0010" and bits[-4:] == "1111")
ck("s2p08 confira", 5 * 8 + 7 == 47 == 2 * 16 + 15 and 0xB3 == 179 and 0x57 == 87)
ck("s2p08 atalho", int("100", 8) == 64 and format(64, "X") == "40" and sorted(t for t, _ in alts("lp-s2-p08") if int(t, 16) < 0x40) == ["2F", "39"])
ck("s2p08 755", "".join(format(int(c), "03b") for c in "755") == "111101101")

# p09: 00001111 + 11110110
p1, p2 = "00001111", "11110110"
t = int(p1, 2) + int(p2, 2)
r = "%s, que vale %d" % (b8(t), s8(b8(t)))
ck("s2p09 certa", certa("lp-s2-p09") == r, r)
xr = b8(int(p1, 2) ^ int(p2, 2))
distratores("lp-s2-p09", {
    "100000101, que vale 261": (format(t, "b") == "100000101" and t == 261, "manteve 9o bit", 261),
    "11111001, que vale −7": (xr == "11111001" and s8(xr) == -7, "xor", -7),
    "00011001, que vale 25": (b8(15 + 10) == "00011001", "leu +10", 25),
    "10000101, que vale −123": (s8("1" + b8(t)[1:]) == -123, "vai-um no sinal", -123)}, 5)
ck("s2p09 -10", s8(p2) == -10 and inverte(p2) == "00001001" and int(inverte(p2), 2) + 1 == 10)
ck("s2p09 cadeia de vai-um a partir da 2a coluna", soma(p1, p2)[1][0][2] == 0 and all(c[2] == 1 for c in soma(p1, p2)[1][1:]))
ck("s2p09 relogio", (5 + 9) % 12 == 2 and (15 + 246) % 256 == 5)
ck("s2p09 pesos", -128 + 64 + 32 + 16 + 4 + 2 == -10)

# p10: 1000 produtos
m = 0
while 2 ** m < 1000: m += 1
ck("s2p10 certa", n(certa("lp-s2-p10")) == m, m)
kq = 1
while kq * kq < 1000: kq += 1
distratores("lp-s2-p10", {
    "9": (2 ** 9 == 512 < 1000 and 1000 - 512 == 488, "512", 9),
    "12": (3 * 4 == 12 and len(str(999)) == 3, "BCD", 12),
    "32": (kq == 32, "n^2", 32),
    "1.000": (True, "um bit por produto", 1000)}, m)
ck("s2p10 999 em binario", format(999, "b") == "1111100111" and 512 + 256 + 128 + 64 + 32 + 4 + 2 + 1 == 999 and 999 > 2 ** 9 - 1)
ck("s2p10 sobram 24", 1024 - 1000 == 24)
ck("s2p10 faixa 513..1024", all((q - 1).bit_length() == 10 for q in range(513, 1025)))
ck("s2p10 SMALLINT unsigned", 2 ** 16 - 1 == 65535)

# p11: cinza 200
qq, rr = divmod(200, 16)
par = format(qq, "X") + format(rr, "X")
r = "#" + par * 3
ck("s2p11 certa", certa("lp-s2-p11") == r, r)
rest200 = []
x = 200
while x: rest200.append(str(x % 2)); x //= 2
lido_errado = "".join(rest200)
distratores("lp-s2-p11", {
    "#8C8C8C": (par[::-1] == "8C" and 0x8C == 140, "trocou", "#8C8C8C"),
    "#C5C5C5": (Fraction(200, 16) == Fraction(25, 2) and 0xC5 == 197, "parte decimal", "#C5C5C5"),
    "#131313": (lido_errado == "00010011" and format(int(lido_errado, 2), "02X") == "13", "restos de cima", "#131313"),
    "#C8": (True, "um par so", "#C8")}, r)
ck("s2p11 binario", format(200, "08b") == "11001000" and 128 + 64 + 8 == 200 and 12 * 16 == 192)

# p12: 100 + 50
t = b8(100 + 50)
r = s8(t)
ck("s2p12 certa", n(certa("lp-s2-p12")) == r, r)
distratores("lp-s2-p12", {
    "150": (100 + 50 == 150, "matematica", 150),
    "−22": (-int(t[1:], 2) == -22, "sinal-magnitude", -22),
    "127": (True, "saturacao", 127),
    "106": (-r == 106, "modulo", 106)}, r)
ck("s2p12 bits", b8(100) == "01100100" and b8(50) == "00110010" and t == "10010110")
ck("s2p12 relogio", 127 - 100 == 27 and 27 + 23 == 50 and -128 + 22 == -106)
ck("s2p12 placar", 60 - 100 == -40)
ck("s2p12 confira inverso", b8(106) == "01101010" and 64 + 32 + 8 + 2 == 106 and inverte("01101010") == "10010101" and b8(int("10010101", 2) + 1) == t)
ck("s2p12 confira -22", b8(-22) == "11101010" and b8(-22) != t)

# ============================ TEORIA E LAB ============================
ck("teo 352", 3 * 100 + 5 * 10 + 2 == 352)
ck("teo 1011 = 11", int("1011", 2) == 11)
ck("teo 13 = 1101 (restos)", format(13, "b") == "1101" and [13 % 2, 6 % 2, 3 % 2, 1 % 2] == [1, 0, 1, 1])
ck("teo D7 / 327 / 215", format(0b11010111, "X") == "D7" and format(0b11010111, "o") == "327" and 0b11010111 == 215)
ck("teo 0110 + 0011", format(0b0110 + 0b0011, "04b") == "1001" and 6 + 3 == 9)
ck("teo -5", b8(-5) == "11111011" and inverte("00000101") == "11111010")
ck("teo 256^3", 256 ** 3 == 16777216)
ck("teo 21", format(21, "08b") == "00010101")
ck("teo euro 3 bytes, emoji 4", len("€".encode("utf-8")) == 3 and len("\U0001F600".encode("utf-8")) == 4)
ck("teo faixa 8 bits", (-(2 ** 7), 2 ** 7 - 1) == (-128, 127))
ck("teo palavras 32/64 bits", 32 // 8 == 4 and 64 // 8 == 8)
ck("lab s1: 7 da direita = 127", sum(2 ** i for i in range(7)) == 127)
v = 5
v = (~v) & 255; v = (v + 1) & 255
ck("lab s2: 5, inverter, +1", format(v, "08b") == "11111011" and v - 256 == -5)
ck("lab s2: 128 com sinal", 128 - 256 == -128)

# ============================ FORMA E COBERTURA ============================
ids = sorted(Q)
esp = sorted([f"lp-s1-p{i:02d}" for i in range(1, 13)] + [f"lp-s2-p{i:02d}" for i in range(1, 13)])
ck("ids = pedido", ids == esp, set(ids) ^ set(esp))
niv = Counter((q["semana"], q["nivel"]) for q in Q.values())
ck("4 por nivel por semana", all(niv[(s, k)] == 4 for s in (1, 2) for k in (1, 2, 3)), dict(niv))
posc = Counter("ABCDE"[[a.get("certa") for a in q["alternativas"]].index(True)] for q in Q.values())
ck("posicoes <= 30%", max(posc.values()) / len(Q) <= 0.30, dict(sorted(posc.items())))
ck("origem", all(q["origem"] == "Prévia · ementa" for q in Q.values()))
ck("teoria s1 e s2 na p1", sorted(SEM) == [1, 2] and all(SEM[s]["previa"] is True and SEM[s]["fonte"] == "Prévia pela ementa do PPC — trocar quando o material da semana chegar" for s in SEM))
np_ = lambda s: len(re.findall(r"\S+", s))
for qid, q in Q.items():
    for k in ["visual", "cotidiano", "trabalho", "erro", "confira", "atalho"]:
        w_ = np_(q["jeitos"][k])
        if not 35 <= w_ <= 110:
            ck(f"{qid} {k} com {w_} palavras", False)
    if not 3 <= len(q["jeitos"]["receita"]) <= 7: ck(qid + " receita", False)
    if not 4 <= len(q["jeitos"]["conversa"]) <= 8: ck(qid + " conversa", False)
    if q["jeitos"]["conversa"][0]["quem"] != "Você": ck(qid + " conversa comeca com Você", False)
    tx = re.sub(r"`[^`]*`", " ", texto_todo(qid))
    if re.search(r"(^|[\s(,\[=])-\d", tx): ck(qid + " hifen como menos", False)
    if "!" in tx: ck(qid + " exclamacao", False)
for s in SEM.values():
    for i, bl in enumerate(s["blocos"]):
        if not 40 <= np_(bl["texto"]) <= 120: ck(f"semana {s['semana']} bloco {i} {np_(bl['texto'])} palavras", False)
    for k, v in s["jeitos"].items():
        if not 50 <= np_(v) <= 120: ck(f"semana {s['semana']} jeito {k} {np_(v)} palavras", False)
for f in ARQS:
    raw = open(os.path.join(DADOS, f), "rb").read()
    ck(f + " sem BOM e sem byte de controle", not raw.startswith(b"\xef\xbb\xbf") and all(c >= 32 or c in (9, 10, 13) for c in raw))

print()
print("FALHAS:", FALHAS if FALHAS else "nenhuma")
