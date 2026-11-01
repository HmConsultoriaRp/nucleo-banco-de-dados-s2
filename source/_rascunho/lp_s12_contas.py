# Confere as contas do lote lp_s12 (Logica de Programacao, semanas 1 e 2, previa).
# Cada linha: rotulo, valor calculado, valor esperado no JSON.
import sys

sys.stdout.reconfigure(encoding="utf-8")
falhas = []

def ok(rot, calc, esperado):
    st = "ok" if calc == esperado else "DIVERGE"
    if calc != esperado:
        falhas.append(rot)
    print(f"{st:8} {rot}: calculado={calc!r} esperado={esperado!r}")

def b8(n):
    return format(n & 0xFF, "08b")

def com_sinal8(bits):
    v = int(bits, 2)
    return v - 256 if v >= 128 else v

# ---------------- Semana 1 ----------------
# p04 ASCII 7 bits
ok("s1p04 2^7", 2 ** 7, 128)
ok("s1p04 2^7-1", 2 ** 7 - 1, 127)
ok("s1p04 2^8", 2 ** 8, 256)
ok("s1p04 2*7", 2 * 7, 14)
ok("s1p04 7^2", 7 ** 2, 49)
ok("ASCII A", ord("A"), 65)
ok("ASCII a", ord("a"), 97)
ok("ASCII 0", ord("0"), 48)

# p08 3 KB em bits (1 KB = 1024 bytes)
ok("s1p08 certa", 3 * 1024 * 8, 24576)
ok("s1p08 bytes", 3 * 1024, 3072)
ok("s1p08 SI", 3 * 1000 * 8, 24000)
ok("s1p08 dividiu", 3 * 1024 // 8, 384)
ok("s1p08 so x8", 3 * 8, 24)

# p10 4 KB, palavras de 32 bits
ok("s1p10 certa", 4 * 1024 // (32 // 8), 1024)
ok("s1p10 dividiu por 32", 4 * 1024 // 32, 128)
ok("s1p10 bytes", 4 * 1024, 4096)
ok("s1p10 SI", 4 * 1000 // 4, 1000)
ok("s1p10 bits da memoria", 4 * 1024 * 8, 32768)
ok("s1p10 confira 1024 x 32 bits", 1024 * 32, 32768)

# p11 UTF-8 de 'Conciliação'
w = "Conciliação"
ok("s1p11 palavra", w, "Conciliação")
ok("s1p11 caracteres", len(w), 11)
ok("s1p11 bytes UTF-8", len(w.encode("utf-8")), 13)
ok("s1p11 acentuadas", sum(1 for c in w if ord(c) > 127), 2)
ok("s1p11 2 por letra", 2 * len(w), 22)
ok("s1p11 so um acento", 9 + 1 + 2, 12)
ok("s1p11 em bits", 13 * 8, 104)
ok("s1p11 latin-1", len(w.encode("latin-1")), 11)
ok("s1p11 c-cedilha 2 bytes", len("ç".encode("utf-8")), 2)
ok("s1p11 a-til 2 bytes", len("ã".encode("utf-8")), 2)
ok("euro 3 bytes", len("€".encode("utf-8")), 3)
ok("emoji 4 bytes", len("\U0001F600".encode("utf-8")), 4)
ok("mojibake", w.encode("utf-8").decode("cp1252"), "ConciliaÃ§Ã£o")
ok("Unicode posicoes", 0x10FFFF + 1, 1114112)

# p12 maquina de acumulador
mem = {10: 7, 11: 5, 12: 0}
acc = mem[10]
acc += mem[11]
acc += mem[11]
mem[12] = acc
ok("s1p12 certa", mem[12], 17)
ok("s1p12 uma soma", 7 + 5, 12)
ok("s1p12 enderecos", 10 + 11 + 11, 32)
# substitui em vez de somar
acc2 = 7; acc2 = 5; acc2 = 5
ok("s1p12 substitui", acc2, 5)

# ---------------- Semana 2 ----------------
# p01 25 em binario
ok("s2p01 certa", format(25, "b"), "11001")
restos = []
n = 25
while n > 0:
    restos.append(n % 2)
    n //= 2
ok("s2p01 restos de cima p/ baixo", "".join(map(str, restos)), "10011")
ok("s2p01 invertido vale", int("10011", 2), 19)
ok("s2p01 sem o primeiro resto", format(12, "b"), "1100")
ok("s2p01 algarismo por algarismo", format(2, "b") + format(5, "b"), "10101")
ok("s2p01 10101 vale", int("10101", 2), 21)
ok("s2p01 11010 vale", int("11010", 2), 26)
ok("s2p01 confira", 16 + 8 + 1, 25)

# p02 110100 para decimal
ok("s2p02 certa", int("110100", 2), 52)
ok("s2p02 pesos invertidos", int("110100"[::-1], 2), 11)
ok("s2p02 contou uns", "110100".count("1"), 3)
ok("s2p02 um bit a menos", 16 + 8 + 2, 26)
ok("s2p02 expoente em 1", 64 + 32 + 8, 104)
ok("s2p02 confira", format(52, "b"), "110100")

# p03 10110110 para hexadecimal
ok("s2p03 certa", format(0b10110110, "X"), "B6")
ok("s2p03 octal", format(0b10110110, "o"), "266")
ok("s2p03 decimal", 0b10110110, 182)
ok("s2p03 grupo 1011", int("1011", 2), 11)
ok("s2p03 grupo 0110", int("0110", 2), 6)
ok("s2p03 confira B6", 11 * 16 + 6, 182)
ok("s2p03 6B vale", 0x6B, 107)

# p04 8 bits
ok("s2p04 valores", 2 ** 8, 256)
ok("s2p04 maior", 2 ** 8 - 1, 255)
ok("s2p04 8^2", 8 ** 2, 64)
ok("s2p04 2*8", 2 * 8, 16)

# p05 1011 + 0111
s = int("1011", 2) + int("0111", 2)
ok("s2p05 certa", format(s, "b"), "10010")
ok("s2p05 decimal", (11, 7, s), (11, 7, 18))
ok("s2p05 sem vai-um (xor)", format(0b1011 ^ 0b0111, "04b"), "1100")
ok("s2p05 descartou vai-um final", format(s & 0xF, "04b"), "0010")
ok("s2p05 or", format(0b1011 | 0b0111, "04b"), "1111")
# erro: na 2a coluna 1+1+1 escrito como 0
a, b = "1011"[::-1], "0111"[::-1]
c = 0; out = []
for i in range(4):
    t = int(a[i]) + int(b[i]) + c
    bit = t % 2
    if i == 1 and t == 3:
        bit = 0  # erro simulado
    out.append(str(bit)); c = t // 2
if c: out.append("1")
ok("s2p05 erro 1+1+1", "".join(out[::-1]), "10000")

# p06 -20 em 8 bits
ok("s2p06 certa", b8(-20), "11101100")
ok("s2p06 20", b8(20), "00010100")
ok("s2p06 inverte", b8(~20), "11101011")
ok("s2p06 sinal-magnitude", "1" + format(20, "07b"), "10010100")
ok("s2p06 atalho errado", b8(-24), "11101000")
ok("s2p06 11101000 vale", com_sinal8("11101000"), -24)
ok("s2p06 confira soma", b8(int("11101100", 2) + 20), "00000000")
ok("s2p06 Excel DECABIN(-20)", format((1 << 10) - 20, "010b"), "1111101100")

# p07 #FF8000
ok("s2p07 FF", 0xFF, 255)
ok("s2p07 80", 0x80, 128)
ok("s2p07 00", 0x00, 0)
ok("s2p07 F", 0xF, 15)
ok("s2p07 16*16", 16 * 16, 256)

# p08 57 octal para hexadecimal
ok("s2p08 decimal", int("57", 8), 47)
ok("s2p08 certa", format(int("57", 8), "X"), "2F")
ok("s2p08 binario", format(int("57", 8), "b"), "101111")
ok("s2p08 grupos da esquerda", format(int("1011", 2), "X") + format(int("11", 2), "X"), "B3")
ok("s2p08 57 decimal em hex", format(57, "X"), "39")
ok("s2p08 4 bits por octal", format(int("01010111", 2), "X"), "57")
ok("s2p08 0x57 vale", 0x57, 87)
ok("s2p08 confira", 2 * 16 + 15, 47)

# p09 00001111 + 11110110
t = int("00001111", 2) + int("11110110", 2)
ok("s2p09 soma 9 bits", format(t, "b"), "100000101")
ok("s2p09 certa", b8(t), "00000101")
ok("s2p09 valor", com_sinal8(b8(t)), 5)
ok("s2p09 11110110 com sinal", com_sinal8("11110110"), -10)
ok("s2p09 11110110 sem sinal", int("11110110", 2), 246)
ok("s2p09 9 bits vale", t, 261)
ok("s2p09 xor", b8(0b00001111 ^ 0b11110110), "11111001")
ok("s2p09 xor vale", com_sinal8("11111001"), -7)
ok("s2p09 15+10", b8(25), "00011001")
ok("s2p09 vai-um no sinal", com_sinal8("10000101"), -123)

# p10 bits para 1000 produtos
nmin = 0
while 2 ** nmin < 1000:
    nmin += 1
ok("s2p10 certa", nmin, 10)
ok("s2p10 2^9", 2 ** 9, 512)
ok("s2p10 2^10", 2 ** 10, 1024)
ok("s2p10 BCD 3 algarismos", 3 * 4, 12)
k = 0
while k * k < 1000:
    k += 1
ok("s2p10 n^2 >= 1000", k, 32)
ok("s2p10 31^2", 31 * 31, 961)
ok("TINYINT UNSIGNED", 2 ** 8 - 1, 255)
ok("SMALLINT UNSIGNED", 2 ** 16 - 1, 65535)

# p11 cinza 200
ok("s2p11 certa", format(200, "X"), "C8")
ok("s2p11 200/16", 200 / 16, 12.5)
ok("s2p11 resto", 200 - 12 * 16, 8)
ok("s2p11 binario", format(200, "08b"), "11001000")
ok("s2p11 restos invertidos", format(200, "08b")[::-1], "00010011")
ok("s2p11 restos invertidos em hex", format(int("00010011", 2), "02X"), "13")
ok("s2p11 8C vale", 0x8C, 140)
ok("s2p11 C5 vale", 0xC5, 197)
ok("s2p11 confira", 12 * 16 + 8, 200)

# p12 100 + 50 em 8 bits com sinal
t = 100 + 50
ok("s2p12 bits", b8(t), "10010110")
ok("s2p12 certa", com_sinal8(b8(t)), -106)
ok("s2p12 150-256", 150 - 256, -106)
ok("s2p12 sinal-magnitude", -int(b8(t)[1:], 2), -22)
ok("s2p12 100", b8(100), "01100100")
ok("s2p12 50", b8(50), "00110010")

# ---------------- Teoria ----------------
ok("teo 13", format(13, "b"), "1101")
ok("teo 1011", int("1011", 2), 11)
ok("teo 352", 3 * 100 + 5 * 10 + 2, 352)
ok("teo D7", format(0b11010111, "X"), "D7")
ok("teo 327 octal", format(0b11010111, "o"), "327")
ok("teo 215", 0b11010111, 215)
ok("teo 0110+0011", format(0b0110 + 0b0011, "04b"), "1001")
ok("teo -5", b8(-5), "11111011")
ok("teo inverte 5", b8(~5 & 0xFF), "11111010")
ok("teo cores", 256 ** 3, 16777216)
ok("teo 21 = 16+4+1", 16 + 4 + 1, 21)
ok("teo 7 bits ligados", 2 ** 7 - 1, 127)
ok("teo DECABIN(13)", format(13, "b"), "1101")
ok("teo DECAHEX(255)", format(255, "X"), "FF")
ok("teo 2^10", 2 ** 10, 1024)

print()
print("FALHAS:", falhas if falhas else "nenhuma")
