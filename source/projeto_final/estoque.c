/* Projeto final - Logica de Programacao (exemplo)
   Papelaria: cadastra os produtos, mostra o valor do estoque
   e avisa quais precisam ser repostos. Mesmo algoritmo do Portugol. */
#include <stdio.h>

typedef struct {
    char nome[50];
    int qtd;
    int minimo;
    double preco;
} Produto;

Produto p[6];   /* usa as posicoes 1 a 5, como o vetor[1..5] do Portugol */

/* valor parado no estoque de um produto */
double valorItem(int k) {
    return p[k].qtd * p[k].preco;
}

/* 1 (verdadeiro) quando a quantidade ficou abaixo do minimo */
int precisaRepor(int k) {
    return p[k].qtd < p[k].minimo;
}

void lerProduto(int k) {
    printf("Produto %d\n", k);
    printf("  Nome: ");
    scanf(" %49[^\n]", p[k].nome);
    printf("  Quantidade em estoque: ");
    scanf("%d", &p[k].qtd);
    printf("  Estoque minimo: ");
    scanf("%d", &p[k].minimo);
    printf("  Preco unitario (R$): ");
    scanf("%lf", &p[k].preco);
}

int main(void) {
    int n, i, repor;
    double total;

    do {
        printf("Quantos produtos (1 a 5)? ");
        scanf("%d", &n);
        if (n < 1 || n > 5) {
            printf("Valor invalido. Digite de 1 a 5.\n");
        }
    } while (!(n >= 1 && n <= 5));

    for (i = 1; i <= n; i++) {
        lerProduto(i);
    }

    printf("\n");
    printf("===== RELATORIO DO ESTOQUE =====\n");
    total = 0;
    repor = 0;
    for (i = 1; i <= n; i++) {
        printf("%2d %s - qtd %3d - valor R$ %8.2f", i, p[i].nome, p[i].qtd, valorItem(i));
        if (precisaRepor(i)) {
            printf(" - REPOR (faltam %d)\n", p[i].minimo - p[i].qtd);
            repor = repor + 1;
        } else {
            printf(" - ok\n");
        }
        total = total + valorItem(i);
    }
    printf("Valor total do estoque: R$ %8.2f\n", total);
    printf("Produtos para repor: %d\n", repor);
    return 0;
}
