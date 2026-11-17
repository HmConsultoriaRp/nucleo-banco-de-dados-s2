/* Projeto final - Logica de Programacao (exemplo)
   Le as notas da turma, calcula a media de cada aluno, diz a situacao
   e mostra o resumo da turma. Mesmo algoritmo do Portugol. */
#include <stdio.h>
#include <string.h>

char nomes[11][50];        /* posicoes 1 a 10, como o vetor[1..10] do Portugol */
double n1[11], n2[11];

double media(int k) {
    return (n1[k] + n2[k]) / 2;
}

const char *situacao(double x) {
    if (x >= 6) {
        return "Aprovado";
    } else {
        if (x >= 4) {
            return "Recuperacao";
        } else {
            return "Reprovado";
        }
    }
}

int notaValida(double x) {
    return x >= 0 && x <= 10;
}

int main(void) {
    int n, i, melhor, aprovados = 0, recuperacao = 0, reprovados = 0;
    double m, somaMedias = 0, mediaTurma;
    const char *sit;

    printf("Quantos alunos (1 a 10)? ");
    scanf("%d", &n);
    while (n < 1 || n > 10) {
        printf("Valor invalido. Quantos alunos (1 a 10)? ");
        scanf("%d", &n);
    }
    for (i = 1; i <= n; i++) {
        printf("Nome do aluno %d: ", i);
        scanf(" %49[^\n]", nomes[i]);
        do {
            printf("  Nota 1: ");
            scanf("%lf", &n1[i]);
            if (!notaValida(n1[i])) {
                printf("  Nota invalida: use de 0 a 10.\n");
            }
        } while (!notaValida(n1[i]));
        do {
            printf("  Nota 2: ");
            scanf("%lf", &n2[i]);
            if (!notaValida(n2[i])) {
                printf("  Nota invalida: use de 0 a 10.\n");
            }
        } while (!notaValida(n2[i]));
    }

    printf("\n");
    printf("===== BOLETIM =====\n");
    melhor = 1;
    for (i = 1; i <= n; i++) {
        m = media(i);
        sit = situacao(m);
        printf("%s: media %5.2f - %s\n", nomes[i], m, sit);
        if (strcmp(sit, "Aprovado") == 0) {
            aprovados = aprovados + 1;
        } else {
            if (strcmp(sit, "Recuperacao") == 0) {
                recuperacao = recuperacao + 1;
            } else {
                reprovados = reprovados + 1;
            }
        }
        somaMedias = somaMedias + m;
        if (m > media(melhor)) {
            melhor = i;
        }
    }
    mediaTurma = somaMedias / n;
    printf("Media da turma: %4.2f\n", mediaTurma);
    printf("Maior media: %s (%4.2f)\n", nomes[melhor], media(melhor));
    printf("Aprovados: %d | Recuperacao: %d | Reprovados: %d\n", aprovados, recuperacao, reprovados);
    return 0;
}
