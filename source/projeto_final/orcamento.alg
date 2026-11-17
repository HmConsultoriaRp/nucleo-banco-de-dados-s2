algoritmo "OrcamentoDomestico"
// Projeto final - Logica de Programacao (exemplo)
// Le a renda e os gastos do mes por categoria, mostra quanto cada gasto
// pesa na renda, avisa o que passou do limite e calcula a sobra.
var
   cat: vetor[1..4] de caractere
   limite: vetor[1..4] de inteiro
   gasto: vetor[1..4] de real
   renda, totalGasto, saldo, p: real
   i, acima: inteiro

// quanto o valor representa da base, em %
funcao percentual(valor, base: real): real
inicio
   retorne valor / base * 100
fimfuncao

// desenha um # para cada 5% e pula a linha
procedimento barra(pct: real)
var j: inteiro
inicio
   para j de 1 ate int(pct / 5) faca
      escreva("#")
   fimpara
   escreval("")
fimprocedimento

inicio
   cat[1] <- "Moradia"
   limite[1] <- 35
   cat[2] <- "Alimentacao"
   limite[2] <- 25
   cat[3] <- "Transporte"
   limite[3] <- 15
   cat[4] <- "Lazer"
   limite[4] <- 10
   repita
      escreva("Renda do mes (R$): ")
      leia(renda)
      se renda <= 0 entao
         escreval("A renda precisa ser maior que zero.")
      fimse
   ate renda > 0
   totalGasto <- 0
   para i de 1 ate 4 faca
      escreva("Gasto com ", cat[i], " (R$): ")
      leia(gasto[i])
      totalGasto <- totalGasto + gasto[i]
   fimpara
   escreval("")
   escreval("===== ORCAMENTO DO MES =====")
   acima <- 0
   para i de 1 ate 4 faca
      p <- percentual(gasto[i], renda)
      escreva(cat[i], ": R$ ", gasto[i]:8:2, " = ", p:5:1, "% ")
      barra(p)
      se p > limite[i] entao
         escreval("   ATENCAO: passou do limite de", limite[i], "%")
         acima <- acima + 1
      fimse
   fimpara
   escreval("Total gasto: R$ ", totalGasto:8:2)
   saldo <- renda - totalGasto
   se saldo >= 0 entao
      escreval("Sobra do mes: R$ ", saldo:8:2)
   senao
      escreval("Faltou dinheiro: R$ ", abs(saldo):8:2)
   fimse
   escreval("Categorias acima do limite:", acima)
fimalgoritmo
