# Projeto final - Logica de Programacao (exemplo)
# Papelaria: cadastra os produtos, mostra o valor do estoque
# e avisa quais precisam ser repostos. Mesmo algoritmo do Portugol.

p = [None] * 6   # usa as posicoes 1 a 5, como o vetor[1..5] do Portugol


# valor parado no estoque de um produto
def valorItem(k):
    return p[k]["qtd"] * p[k]["preco"]


# True quando a quantidade ficou abaixo do minimo
def precisaRepor(k):
    return p[k]["qtd"] < p[k]["minimo"]


def lerProduto(k):
    print(f"Produto {k}")
    nome = input("  Nome: ")
    qtd = int(input("  Quantidade em estoque: "))
    minimo = int(input("  Estoque minimo: "))
    preco = float(input("  Preco unitario (R$): "))
    p[k] = {"nome": nome, "qtd": qtd, "minimo": minimo, "preco": preco}


while True:   # repita ... ate
    n = int(input("Quantos produtos (1 a 5)? "))
    if n < 1 or n > 5:
        print("Valor invalido. Digite de 1 a 5.")
    if 1 <= n <= 5:
        break

for i in range(1, n + 1):
    lerProduto(i)

print()
print("===== RELATORIO DO ESTOQUE =====")
total = 0
repor = 0
for i in range(1, n + 1):
    print(f"{i:2d} {p[i]['nome']} - qtd {p[i]['qtd']:3d} - valor R$ {valorItem(i):8.2f}", end="")
    if precisaRepor(i):
        print(f" - REPOR (faltam {p[i]['minimo'] - p[i]['qtd']})")
        repor = repor + 1
    else:
        print(" - ok")
    total = total + valorItem(i)
print(f"Valor total do estoque: R$ {total:8.2f}")
print(f"Produtos para repor: {repor}")
