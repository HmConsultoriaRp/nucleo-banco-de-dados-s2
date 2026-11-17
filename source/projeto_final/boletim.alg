algoritmo "BoletimDaTurma"
// Projeto final - Logica de Programacao (exemplo)
// Le as notas da turma, calcula a media de cada aluno, diz a situacao
// e mostra o resumo da turma.
var
   nomes: vetor[1..10] de caractere
   n1, n2: vetor[1..10] de real
   n, i, melhor, aprovados, recuperacao, reprovados: inteiro
   m, somaMedias, mediaTurma: real
   sit: caractere

funcao media(k: inteiro): real
inicio
   retorne (n1[k] + n2[k]) / 2
fimfuncao

funcao situacao(x: real): caractere
inicio
   se x >= 6 entao
      retorne "Aprovado"
   senao
      se x >= 4 entao
         retorne "Recuperacao"
      senao
         retorne "Reprovado"
      fimse
   fimse
fimfuncao

funcao notaValida(x: real): logico
inicio
   retorne (x >= 0) e (x <= 10)
fimfuncao

inicio
   escreva("Quantos alunos (1 a 10)? ")
   leia(n)
   enquanto (n < 1) ou (n > 10) faca
      escreva("Valor invalido. Quantos alunos (1 a 10)? ")
      leia(n)
   fimenquanto
   para i de 1 ate n faca
      escreva("Nome do aluno", i, ": ")
      leia(nomes[i])
      repita
         escreva("  Nota 1: ")
         leia(n1[i])
         se nao notaValida(n1[i]) entao
            escreval("  Nota invalida: use de 0 a 10.")
         fimse
      ate notaValida(n1[i])
      repita
         escreva("  Nota 2: ")
         leia(n2[i])
         se nao notaValida(n2[i]) entao
            escreval("  Nota invalida: use de 0 a 10.")
         fimse
      ate notaValida(n2[i])
   fimpara
   escreval("")
   escreval("===== BOLETIM =====")
   melhor <- 1
   para i de 1 ate n faca
      m <- media(i)
      sit <- situacao(m)
      escreval(nomes[i], ": media ", m:5:2, " - ", sit)
      se sit = "Aprovado" entao
         aprovados <- aprovados + 1
      senao
         se sit = "Recuperacao" entao
            recuperacao <- recuperacao + 1
         senao
            reprovados <- reprovados + 1
         fimse
      fimse
      somaMedias <- somaMedias + m
      se m > media(melhor) entao
         melhor <- i
      fimse
   fimpara
   mediaTurma <- somaMedias / n
   escreval("Media da turma: ", mediaTurma:4:2)
   escreval("Maior media: ", nomes[melhor], " (", media(melhor):4:2, ")")
   escreval("Aprovados:", aprovados, " | Recuperacao:", recuperacao, " | Reprovados:", reprovados)
fimalgoritmo
