# Projeto final - Logica de Programacao (exemplo)
# Caixa de uma lanchonete: registra o pedido, da 10% de desconto
# a partir de R$ 50,00 e calcula o troco. Mesmo algoritmo do Portugol.

# posicoes 1 a 5, como o vetor[1..5] do Portugol (a posicao 0 fica sem uso)
item = ["", "X-Burguer", "Misto quente", "Suco natural", "Refrigerante", "Pastel"]
preco = [0, 18.50, 9.00, 7.50, 6.00, 8.00]
qtd = [0] * 6   # comeca com zero, como no Portugol


def mostraCardapio():
    print("===== CARDAPIO =====")
    for k in range(1, 6):
        print(f"{k:1d} - {item[k]} R$ {preco[k]:6.2f}")
    print("0 - Fechar o pedido")


# soma de quantidade x preco de todos os itens
def subtotal():
    s = 0
    for k in range(1, 6):
        s = s + qtd[k] * preco[k]
    return s


def desconto(valor):
    if valor >= 50:
        return valor * 0.10
    else:
        return 0


mostraCardapio()
while True:   # repita ... ate
    cod = int(input("Codigo do item (0 fecha): "))
    if cod >= 1 and cod <= 5:
        q = int(input("Quantidade: "))
        qtd[cod] = qtd[cod] + q
        print(f"  + {q} x {item[cod]}")
    else:
        if cod != 0:
            print("  Codigo invalido.")
    if cod == 0:
        break

bruto = subtotal()
desc = desconto(bruto)
total = bruto - desc
print()
print("===== CUPOM =====")
for i in range(1, 6):
    if qtd[i] > 0:
        valorLinha = qtd[i] * preco[i]
        print(f"{qtd[i]:2d} x {item[i]} = R$ {valorLinha:7.2f}")
print(f"Subtotal: R$ {bruto:7.2f}")
print(f"Desconto: R$ {desc:7.2f}")
print(f"Total:    R$ {total:7.2f}")
while True:
    pago = float(input("Valor pago (R$): "))
    if pago < total:
        print("  Valor menor que o total.")
    if pago >= total:
        break
troco = pago - total
print(f"Troco: R$ {troco:7.2f}")
