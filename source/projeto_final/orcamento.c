/* Projeto final - Logica de Programacao (exemplo)
   Le a renda e os gastos do mes por categoria, mostra quanto cada gasto
   pesa na renda, avisa o que passou do limite e calcula a sobra.
   Mesmo algoritmo do Portugol. */
#include <stdio.h>
#include <math.h>

/* posicoes 1 a 4, como o vetor[1..4] do Portugol (a posicao 0 fica sem uso) */
const char *cat[5] = {"", "Moradia", "Alimentacao", "Transporte", "Lazer"};
int limite[5] = {0, 35, 25, 15, 10};
double gasto[5];

/* quanto o valor representa da base, em % */
double percentual(double valor, double base) {
    return valor / base * 100;
}

/* desenha um # para cada 5% e pula a linha */
void barra(double pct) {
    int j;
    for (j = 1; j <= (int)(pct / 5); j++) {
        printf("#");
    }
    printf("\n");
}

int main(void) {
    double renda, totalGasto, saldo, p;
    int i, acima;

    do {
        printf("Renda do mes (R$): ");
        scanf("%lf", &renda);
        if (renda <= 0) {
            printf("A renda precisa ser maior que zero.\n");
        }
    } while (!(renda > 0));

    totalGasto = 0;
    for (i = 1; i <= 4; i++) {
        printf("Gasto com %s (R$): ", cat[i]);
        scanf("%lf", &gasto[i]);
        totalGasto = totalGasto + gasto[i];
    }

    printf("\n");
    printf("===== ORCAMENTO DO MES =====\n");
    acima = 0;
    for (i = 1; i <= 4; i++) {
        p = percentual(gasto[i], renda);
        printf("%s: R$ %8.2f = %5.1f%% ", cat[i], gasto[i], p);
        barra(p);
        if (p > limite[i]) {
            printf("   ATENCAO: passou do limite de %d%%\n", limite[i]);
            acima = acima + 1;
        }
    }
    printf("Total gasto: R$ %8.2f\n", totalGasto);
    saldo = renda - totalGasto;
    if (saldo >= 0) {
        printf("Sobra do mes: R$ %8.2f\n", saldo);
    } else {
        printf("Faltou dinheiro: R$ %8.2f\n", fabs(saldo));
    }
    printf("Categorias acima do limite: %d\n", acima);
    return 0;
}
