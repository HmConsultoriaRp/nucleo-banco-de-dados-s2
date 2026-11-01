# Roteiro do conteúdo — site "Núcleo" (Semestre 2, Ciclo 1: Geometria Analítica + Lógica de Programação)

## Quem vai estudar
Hélio, aluno de Tecnologia em Banco de Dados (EAD, UFTM/CEDD). Adulto, consultor financeiro e tributário:
vive em Excel, Power BI, SQL, extratos, DRE e conciliação. Estuda à noite, faz avaliação semanal no Moodle
e prova presencial. Quer entender, não decorar. Já aprovou o formato "questão de múltipla escolha +
explicação + dica + resolução". Agora quer **a mesma questão explicada de vários jeitos**, porque cada
pessoa entende por um caminho diferente.

## Seu trabalho
Escrever questões de múltipla escolha (5 alternativas) e, para cada uma, **8 jeitos de explicar**.
Gravar em arquivos JSON (UTF-8) com a ferramenta Write. Rodar o validador. Nada de HTML.

**Grave em partes de no máximo 6 questões**: `<prefixo>_p1.json`, `<prefixo>_p2.json`, ... (cada parte
é um arquivo completo com a estrutura abaixo). A teoria das semanas vai só na `_p1`. Isso evita estourar
o tamanho de uma resposta.

## Os 8 jeitos (campo `jeitos`) — cada um é um CAMINHO DIFERENTE, não a mesma explicação com outras palavras
1. `visual` — Enxergar. Imagem mental, desenho descrito, movimento: setas, eixos, a tabela-verdade como
   grade de interruptores, a memória como gavetas. Se a questão tem `figura`, o texto conversa com ela
   ("na figura, as três setas azuis...").
2. `receita` — Passo a passo. Lista de 3 a 7 passos curtos, cada um com a conta feita com os números da
   questão. O último passo chega na resposta. É a resolução completa.
3. `cotidiano` — Analogia do dia a dia (trajeto, trena, cozinha, fila, troco, interruptor). Precisa ser
   honesta: se a analogia distorce a matemática, troque de analogia.
4. `trabalho` — Ponte com o mundo do Hélio: Excel (SOMARPRODUTO, SE, SOMASE, PROCV), SQL (WHERE, AND/OR,
   SUM, CASE, JOIN), Power BI, finanças (lançamento, saldo, conciliação, DRE, rateio, reajuste), banco de
   dados (linha, coluna, chave, tipo de dado). Só quando a ligação for verdadeira. Exemplos que valem:
   produto escalar = SOMARPRODUTO(quantidades; preços); implicação p → q = regra de auditoria "se a NF é
   de importação, então tem DI" (só é violada quando a NF é de importação e não tem DI); acumulador num
   laço = saldo corrente do extrato; distância entre pontos = quão diferentes são dois clientes em três
   indicadores. Não cite clientes, empresas ou dados reais.
5. `conversa` — Diálogo curto (4 a 8 falas) entre "Você" (o aluno) e "Monitor". O aluno traz a dúvida real
   ou uma tentativa errada; o monitor corrige com uma pergunta ou um contraexemplo. Natural, sem elogio vazio.
6. `erro` — Onde a turma tropeça: a armadilha principal da questão e como perceber que caiu nela. É a
   visão geral (o `erro` de cada alternativa é o específico).
7. `confira` — Como tirar a prova sozinho por um caminho independente: substituir de volta, testar um caso,
   conferir o sinal, calcular de outro jeito, produto escalar = 0 para ortogonalidade, teste de mesa.
8. `atalho` — Estratégia de prova com pouco tempo: o que olhar primeiro para eliminar alternativas
   (coordenada que não muda, sinal, paridade, ordem de grandeza). Se não houver atalho honesto, diga qual é
   o caminho mais curto e seguro.

Tamanho: `visual`, `cotidiano`, `trabalho`, `erro`, `confira`, `atalho` com 35 a 110 palavras cada.
`receita` com 3 a 7 passos. `conversa` com 4 a 8 falas.

## Alternativas
- Exatamente 5. Exatamente 1 com `"certa": true`.
- Cada errada nasce de um erro plausível e específico (sinal trocado, B − A × A − B, esquecer um termo,
  somar em vez de subtrair, confundir produto escalar com vetorial, confundir `div` com `/`, uma volta a
  mais no laço, De Morgan pela metade...). O campo `erro` explica em 1 ou 2 frases qual conta leva àquele
  valor e por que está errada. **Confira que a conta descrita no `erro` dá mesmo aquele valor.**
- As 5 com textos diferentes entre si e do mesmo formato (a certa não pode ser a "mais caprichada").
- Varie a posição da certa (A a E) ao longo dos seus arquivos; nenhuma letra com mais de 30% das certas.

## Outros campos da questão
- `id`: "<disciplina>-s<semana>-<sufixo>". Lista: "ga-s1-l1q3", "ga-s2-l2q1k", "ga-s3-l3q5c".
  Construída: "ga-s3-c01". Prévia: "lp-s5-p07", "ga-s4-p03". Único.
- `semana`: 1 a 6. `nivel`: 1 = aplicação direta; 2 = dois passos ou interpretação; 3 = montar, combinar
  ou provar. `minutos`: 1 a 8. `tema`: 2 a 5 palavras.
- `origem` (o selo que mostra de onde veio): questão da lista = "Lista 1 · Q3", "Lista 2 · Q1k",
  "Lista 3 · Q5c" (exatamente assim). Construída a partir do assunto de uma lista = "Construída · conferida".
  Prévia = "Prévia · ementa".
- `enunciado`: questão da lista mantém o enunciado original (pode acrescentar "Qual é ...?" no fim).
- `dica`: uma frase que empurra sem entregar a resposta.
- `resposta`: a resposta final, curta.

## Formato do texto (sem HTML, sem LaTeX)
- Vetor com seta: `[[u]]`, `[[AB]]`, `[[v₁]]`. Norma: `‖[[u]]‖`.
- Negrito: `**texto**`. Código em linha entre crases: `` `x <- 10` ``.
- Sinal de menos tipográfico "−" (U+2212) nos números de matemática. Dentro de código VisuAlg, "-" comum.
- Frações "13/15", "−7/2". Raiz: "√19", "√17/4" (a raiz pega só o número colado), "√(a² + b²)".
  Expoentes e índices Unicode: ², ³, ₁, ₂, ₃, ⁿ. Graus "90°". Decimal com vírgula: "36,87°".
  Símbolos: ·, ×, ≠, ≤, ≥, ⊥, ∥, ¬, ∧, ∨, →, ↔, ∀, ∃, ≡.
- Quebra de linha: "\n".
- Português do Brasil **com acento** desde a primeira linha (questão, explicação, você, não, é).
  Numa disciplina anterior o texto saiu sem acento e a correção levou 3.100 trocas.

## Voz (o Hélio pediu "mais humano, menos cara de IA")
- Frases curtas. Verbos concretos. Os números da própria questão.
- Explique o termo técnico na primeira vez que aparecer.
- PROIBIDO: "Vamos lá", "Ótima pergunta", "Excelente", "mergulhar", "desvendar", "jornada",
  "fascinante", "crucial", "É importante notar", "Em resumo", "Basicamente", "simplesmente",
  ponto de exclamação, emoji, travessão em toda frase.
- Não repita a mesma frase entre os jeitos. Se dois jeitos ficaram parecidos, refaça um deles.
- Não invente fonte, autor, página, slide ou fala do professor.

## Figura (só Geometria) — campo `figura`, opcional
```json
"figura": {
  "modo": "3d",
  "onde": "explicacao",
  "itens": [
    {"tipo": "vetor", "de": [0, 0, 0], "ate": [1, 1, -1], "rot": "u", "cor": 1},
    {"tipo": "ponto", "em": [1, 1, 3], "rot": "A"},
    {"tipo": "segmento", "de": [0, 0, 0], "ate": [1, 0, 0], "tracejado": true},
    {"tipo": "poligono", "pts": [[0, 0, 0], [1, 0, 0], [1, 1, 0]], "cor": 3}
  ],
  "legenda": "Uma frase dizendo o que olhar."
}
```
- `modo`: "3d" (eixo z para cima; o aluno gira com o mouse ou o dedo) ou "2d".
- `onde`: "explicacao" (padrão, aparece junto dos jeitos de explicar) ou "enunciado" (só quando a
  figura faz parte do enunciado original, como os hexágonos e o paralelepípedo, e sem desenhar a resposta).
- Cores: 1 azul-petróleo (dado), 2 coral (segundo dado), 3 ocre (auxiliar), 4 tinta escura (resultado).
- Polígono com `"aberto": true` vira linha sem fechar e sem preenchimento (curvas: parábola, ramo de hipérbole).
- Coordenadas em número decimal JSON (1.732 para √3). No modo 2d use [x, y].
- Ponha figura sempre que ver ajudar (soma de vetores, pontos, paralelogramo, projeção, área, volume,
  retas, planos, cônicas desenhadas por pontos). As coordenadas têm de bater com o enunciado.

## Código (só Lógica) — campos `codigo`, `entradas`, `saida`
VisuAlg 3.0 (o programa que a disciplina usa). O site roda o código num interpretador próprio e mostra
o teste de mesa linha a linha, então use SÓ este subconjunto:
- `algoritmo "nome"` / `var` / `inicio` / `fimalgoritmo`; comentário `//`.
- Tipos `inteiro`, `real`, `caractere`, `logico`. Vetor: `v: vetor[1..5] de inteiro`.
- Atribuição `<-`. Aritméticos `+ - * /` (a barra `/` sempre dá real), `\` e `div` (divisão inteira),
  `mod` e `%` (resto), `^` (potência). Relacionais `= <> < > <= >=`. Lógicos `e ou nao xou`.
  Literais `verdadeiro` e `falso`; texto entre aspas duplas; `+` junta textos.
- Funções: `raizq abs int quad compr maiusc minusc`.
- `leia(a, b)` lê de `entradas` (lista de textos, na ordem). `escreva(...)` e `escreval(...)` com
  vários argumentos separados por vírgula.
- `se cond entao ... senao ... fimse`; `escolha x` / `caso 1, 2` / `caso 3` / `outrocaso` / `fimescolha`;
  `para i de 1 ate 10 passo 2 faca ... fimpara`; `enquanto cond faca ... fimenquanto`;
  `repita ... ate cond`; `interrompa`.
- Fora do subconjunto: procedimento, função, arquivo, aleatório, cronômetro, formatação `x:5:2`.
- `saida`: o texto exato que o programa escreve, linhas separadas por "\n". O site compara ignorando
  espaços repetidos e espaços nas pontas. Real sai com ponto ("2.5"); real de valor inteiro sai sem casas
  ("5"); lógico sai "VERDADEIRO" ou "FALSO".
- Não faça questão cuja resposta dependa de detalhe de formatação (espaço antes de número, casas decimais).
- No JSON, a aspa dentro do código vira `\"` e a barra invertida vira `\\`.

## Tabela (só Lógica) — campo `tabela`, opcional
`"tabela": {"onde": "enunciado", "cab": ["p", "q", "p → q"], "linhas": [["V","V","V"], ["V","F","F"], ["F","V","V"], ["F","F","V"]]}`
(`onde`: "enunciado" ou "explicacao", mesma regra da figura.)

## Estrutura do arquivo
```json
{
  "disciplina": "ga",
  "semanas": [],
  "questoes": []
}
```
Teoria da semana (só na `_p1` do lote dono da semana):
```json
{
  "semana": 1,
  "titulo": "Vetores: somar, esticar e medir",
  "chamada": "Uma frase que diz para que serve o assunto.",
  "fonte": "Lista 1 — Prof. Danilo Adrian Marques",
  "previa": false,
  "blocos": [{"titulo": "...", "texto": "..."}],
  "formulas": [{"nome": "Norma", "expr": "‖[[u]]‖ = √(x² + y² + z²)", "quando": "tamanho de um vetor"}],
  "jeitos": {"visual": "...", "cotidiano": "...", "receita": "...", "trabalho": "...", "erro": "..."},
  "lab": "Uma frase sugerindo o que testar no laboratório interativo da semana."
}
```
- `blocos`: 3 a 6, com 40 a 120 palavras cada. `formulas`: todas as que a semana usa.
- `jeitos` da semana: o conceito central explicado de 5 jeitos, 50 a 120 palavras cada.
- Prévia: `"fonte": "Prévia pela ementa do PPC — trocar quando o material da semana chegar"`, `"previa": true`.

Questão: veja os dois exemplos completos em `exemplos.json` (mesma pasta). Esse é o nível de qualidade.

## Antes de terminar
1. Rode `python -I "<pasta _gerador>\validar.py" "<arquivo>"` em cada parte e corrija até sair "OK".
2. Refaça cada conta por Python, num arquivo `.py` na pasta `_gerador\_rascunho\` (nunca `python -c`,
   nunca heredoc). Para Lógica, simule cada código e confira `saida`.
3. Responda só o resumo pedido.
