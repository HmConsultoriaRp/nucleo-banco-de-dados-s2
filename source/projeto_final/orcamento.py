# Projeto final - Logica de Programacao (exemplo)
# Le a renda e os gastos do mes por categoria, mostra quanto cada gasto
# pesa na renda, avisa o que passou do limite e calcula a sobra.
# Mesmo algoritmo do Portugol.

# posicoes 1 a 4, como o vetor[1..4] do Portugol (a posicao 0 fica sem uso)
cat = ["", "Moradia", "Alimentacao", "Transporte", "Lazer"]
limite = [0, 35, 25, 15, 10]
gasto = [0.0] * 5


# quanto o valor representa da base, em %
def percentual(valor, base):
    return valor / base * 100


# desenha um # para cada 5% e pula a linha
def barra(pct):
    for j in range(1, int(pct / 5) + 1):
        print("#", end="")
    print()


while True:   # repita ... ate
    renda = float(input("Renda do mes (R$): "))
    if renda <= 0:
        print("A renda precisa ser maior que zero.")
    if renda > 0:
        break

totalGasto = 0
for i in range(1, 5):
    gasto[i] = float(input(f"Gasto com {cat[i]} (R$): "))
    totalGasto = totalGasto + gasto[i]

print()
print("===== ORCAMENTO DO MES =====")
acima = 0
for i in range(1, 5):
    p = percentual(gasto[i], renda)
    print(f"{cat[i]}: R$ {gasto[i]:8.2f} = {p:5.1f}% ", end="")
    barra(p)
    if p > limite[i]:
        print(f"   ATENCAO: passou do limite de {limite[i]}%")
        acima = acima + 1
print(f"Total gasto: R$ {totalGasto:8.2f}")
saldo = renda - totalGasto
if saldo >= 0:
    print(f"Sobra do mes: R$ {saldo:8.2f}")
else:
    print(f"Faltou dinheiro: R$ {abs(saldo):8.2f}")
print(f"Categorias acima do limite: {acima}")
