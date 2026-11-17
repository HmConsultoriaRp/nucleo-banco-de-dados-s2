algoritmo "CaixaLanchonete"
// Projeto final - Logica de Programacao (exemplo)
// Caixa de uma lanchonete: registra o pedido, da 10% de desconto
// a partir de R$ 50,00 e calcula o troco.
var
   item: vetor[1..5] de caractere
   preco: vetor[1..5] de real
   qtd: vetor[1..5] de inteiro
   cod, q, i: inteiro
   bruto, desc, total, pago, troco, valorLinha: real

procedimento mostraCardapio
var k: inteiro
inicio
   escreval("===== CARDAPIO =====")
   para k de 1 ate 5 faca
      escreval(k:1, " - ", item[k], " R$ ", preco[k]:6:2)
   fimpara
   escreval("0 - Fechar o pedido")
fimprocedimento

// soma de quantidade x preco de todos os itens (funcao sem parametro:
// no Portugol do VisuAlg ela e chamada sem parenteses)
funcao subtotal: real
var k: inteiro
   s: real
inicio
   s <- 0
   para k de 1 ate 5 faca
      s <- s + qtd[k] * preco[k]
   fimpara
   retorne s
fimfuncao

funcao desconto(valor: real): real
inicio
   se valor >= 50 entao
      retorne valor * 0.10
   senao
      retorne 0
   fimse
fimfuncao

inicio
   item[1] <- "X-Burguer"
   preco[1] <- 18.50
   item[2] <- "Misto quente"
   preco[2] <- 9.00
   item[3] <- "Suco natural"
   preco[3] <- 7.50
   item[4] <- "Refrigerante"
   preco[4] <- 6.00
   item[5] <- "Pastel"
   preco[5] <- 8.00
   mostraCardapio
   repita
      escreva("Codigo do item (0 fecha): ")
      leia(cod)
      se (cod >= 1) e (cod <= 5) entao
         escreva("Quantidade: ")
         leia(q)
         qtd[cod] <- qtd[cod] + q
         escreval("  +", q, " x ", item[cod])
      senao
         se cod <> 0 entao
            escreval("  Codigo invalido.")
         fimse
      fimse
   ate cod = 0
   bruto <- subtotal
   desc <- desconto(bruto)
   total <- bruto - desc
   escreval("")
   escreval("===== CUPOM =====")
   para i de 1 ate 5 faca
      se qtd[i] > 0 entao
         valorLinha <- qtd[i] * preco[i]
         escreval(qtd[i]:2, " x ", item[i], " = R$ ", valorLinha:7:2)
      fimse
   fimpara
   escreval("Subtotal: R$ ", bruto:7:2)
   escreval("Desconto: R$ ", desc:7:2)
   escreval("Total:    R$ ", total:7:2)
   repita
      escreva("Valor pago (R$): ")
      leia(pago)
      se pago < total entao
         escreval("  Valor menor que o total.")
      fimse
   ate pago >= total
   troco <- pago - total
   escreval("Troco: R$ ", troco:7:2)
fimalgoritmo
