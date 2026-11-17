# Projeto final - Logica de Programacao (exemplo)
# Le as notas da turma, calcula a media de cada aluno, diz a situacao
# e mostra o resumo da turma. Mesmo algoritmo do Portugol.

nomes = [""] * 11   # posicoes 1 a 10, como o vetor[1..10] do Portugol
n1 = [0.0] * 11
n2 = [0.0] * 11


def media(k):
    return (n1[k] + n2[k]) / 2


def situacao(x):
    if x >= 6:
        return "Aprovado"
    else:
        if x >= 4:
            return "Recuperacao"
        else:
            return "Reprovado"


def notaValida(x):
    return x >= 0 and x <= 10


aprovados = recuperacao = reprovados = 0
somaMedias = 0

n = int(input("Quantos alunos (1 a 10)? "))
while n < 1 or n > 10:
    n = int(input("Valor invalido. Quantos alunos (1 a 10)? "))

for i in range(1, n + 1):
    nomes[i] = input(f"Nome do aluno {i}: ")
    while True:   # repita ... ate
        n1[i] = float(input("  Nota 1: "))
        if not notaValida(n1[i]):
            print("  Nota invalida: use de 0 a 10.")
        if notaValida(n1[i]):
            break
    while True:
        n2[i] = float(input("  Nota 2: "))
        if not notaValida(n2[i]):
            print("  Nota invalida: use de 0 a 10.")
        if notaValida(n2[i]):
            break

print()
print("===== BOLETIM =====")
melhor = 1
for i in range(1, n + 1):
    m = media(i)
    sit = situacao(m)
    print(f"{nomes[i]}: media {m:5.2f} - {sit}")
    if sit == "Aprovado":
        aprovados = aprovados + 1
    else:
        if sit == "Recuperacao":
            recuperacao = recuperacao + 1
        else:
            reprovados = reprovados + 1
    somaMedias = somaMedias + m
    if m > media(melhor):
        melhor = i
mediaTurma = somaMedias / n
print(f"Media da turma: {mediaTurma:4.2f}")
print(f"Maior media: {nomes[melhor]} ({media(melhor):4.2f})")
print(f"Aprovados: {aprovados} | Recuperacao: {recuperacao} | Reprovados: {reprovados}")
