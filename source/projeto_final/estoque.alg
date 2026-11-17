algoritmo "ControleDeEstoque"
// Projeto final - Logica de Programacao (exemplo)
// Papelaria: cadastra os produtos, mostra o valor do estoque
// e avisa quais precisam ser repostos.
tipo Produto = registro
   nome: caractere
   qtd: inteiro
   minimo: inteiro
   preco: real
fimregistro
var
   p: vetor[1..5] de Produto
   n, i, repor: inteiro
   total: real

// valor parado no estoque de um produto
funcao valorItem(k: inteiro): real
inicio
   retorne p[k].qtd * p[k].preco
fimfuncao

// VERDADEIRO quando a quantidade ficou abaixo do minimo
funcao precisaRepor(k: inteiro): logico
inicio
   retorne p[k].qtd < p[k].minimo
fimfuncao

procedimento lerProduto(k: inteiro)
inicio
   escreval("Produto", k)
   escreva("  Nome: ")
   leia(p[k].nome)
   escreva("  Quantidade em estoque: ")
   leia(p[k].qtd)
   escreva("  Estoque minimo: ")
   leia(p[k].minimo)
   escreva("  Preco unitario (R$): ")
   leia(p[k].preco)
fimprocedimento

inicio
   repita
      escreva("Quantos produtos (1 a 5)? ")
      leia(n)
      se (n < 1) ou (n > 5) entao
         escreval("Valor invalido. Digite de 1 a 5.")
      fimse
   ate (n >= 1) e (n <= 5)
   para i de 1 ate n faca
      lerProduto(i)
   fimpara
   escreval("")
   escreval("===== RELATORIO DO ESTOQUE =====")
   total <- 0
   repor <- 0
   para i de 1 ate n faca
      escreva(i:2, " ", p[i].nome, " - qtd ", p[i].qtd:3, " - valor R$ ", valorItem(i):8:2)
      se precisaRepor(i) entao
         escreval(" - REPOR (faltam", p[i].minimo - p[i].qtd, ")")
         repor <- repor + 1
      senao
         escreval(" - ok")
      fimse
      total <- total + valorItem(i)
   fimpara
   escreval("Valor total do estoque: R$ ", total:8:2)
   escreval("Produtos para repor:", repor)
fimalgoritmo
