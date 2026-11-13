# Núcleo · Semestre 2

Fonte do site de apoio para Geometria Analítica e Lógica de Programação.

## Gerar o HTML único

```powershell
node gerar.mjs "Nucleo - Semestre 2.html"
```

O arquivo final incorpora CSS, JavaScript e todo o banco de questões. Pode ser aberto com duplo clique ou publicado diretamente no GitHub Pages.

## Acrescentar uma atividade semanal

1. Transcrever o enunciado original do print sem alterar o pedido.
2. Resolver e conferir a resposta.
3. Incluir a questão no JSON da disciplina e semana em `dados/`, seguindo o padrão do `BRIEF.md`.
4. Executar os validadores e os testes do interpretador VisuAlg quando houver código.
5. Gerar novamente o HTML e testar a questão no navegador.

O site exibe automaticamente a nova questão em **Atividades da universidade** e em **Questões**. O progresso fica no navegador, em `localStorage`, sob a chave `nucleo-s2-v1`.

Questões recebidas em avaliações usam origem própria, por exemplo `Avaliação semanal 1 · T1 · Q01`. Formatos de múltipla seleção e classificação podem ser convertidos em alternativas compostas para manter a correção, o simulado e o progresso compatíveis com o banco principal.

## Compatibilidade com a versão anterior

No primeiro acesso, quando ainda não existe o novo estado, o site lê `nucleo-state`, preserva tema, registros de atividades, marcadores e histórico de simulados em um resumo legado. A chave anterior não é apagada. Respostas antigas não são convertidas em acertos porque os bancos de questões são diferentes.
