/* Projeto final - Logica de Programacao (exemplo)
   Caixa de uma lanchonete: registra o pedido, da 10% de desconto
   a partir de R$ 50,00 e calcula o troco. Mesmo algoritmo do Portugol. */
#include <stdio.h>

/* posicoes 1 a 5, como o vetor[1..5] do Portugol (a posicao 0 fica sem uso) */
const char *item[6] = {"", "X-Burguer", "Misto quente", "Suco natural", "Refrigerante", "Pastel"};
double preco[6] = {0, 18.50, 9.00, 7.50, 6.00, 8.00};
int qtd[6];   /* comeca com zero, como no Portugol */

void mostraCardapio(void) {
    int k;
    printf("===== CARDAPIO =====\n");
    for (k = 1; k <= 5; k++) {
        printf("%1d - %s R$ %6.2f\n", k, item[k], preco[k]);
    }
    printf("0 - Fechar o pedido\n");
}

/* soma de quantidade x preco de todos os itens */
double subtotal(void) {
    int k;
    double s = 0;
    for (k = 1; k <= 5; k++) {
        s = s + qtd[k] * preco[k];
    }
    return s;
}

double desconto(double valor) {
    if (valor >= 50) {
        return valor * 0.10;
    } else {
        return 0;
    }
}

int main(void) {
    int cod, q, i;
    double bruto, desc, total, pago, troco, valorLinha;

    mostraCardapio();
    do {
        printf("Codigo do item (0 fecha): ");
        scanf("%d", &cod);
        if (cod >= 1 && cod <= 5) {
            printf("Quantidade: ");
            scanf("%d", &q);
            qtd[cod] = qtd[cod] + q;
            printf("  + %d x %s\n", q, item[cod]);
        } else {
            if (cod != 0) {
                printf("  Codigo invalido.\n");
            }
        }
    } while (!(cod == 0));

    bruto = subtotal();
    desc = desconto(bruto);
    total = bruto - desc;
    printf("\n");
    printf("===== CUPOM =====\n");
    for (i = 1; i <= 5; i++) {
        if (qtd[i] > 0) {
            valorLinha = qtd[i] * preco[i];
            printf("%2d x %s = R$ %7.2f\n", qtd[i], item[i], valorLinha);
        }
    }
    printf("Subtotal: R$ %7.2f\n", bruto);
    printf("Desconto: R$ %7.2f\n", desc);
    printf("Total:    R$ %7.2f\n", total);
    do {
        printf("Valor pago (R$): ");
        scanf("%lf", &pago);
        if (pago < total) {
            printf("  Valor menor que o total.\n");
        }
    } while (!(pago >= total));
    troco = pago - total;
    printf("Troco: R$ %7.2f\n", troco);
    return 0;
}
