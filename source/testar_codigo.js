// Roda no interpretador do site todo código VisuAlg das questões e compara com o campo "saida".
// Uso: node testar_codigo.js <pasta dados> [exemplos.json]
const fs = require('fs');
const path = require('path');
const VA = require('./site/visualg.js');

let falhas = 0, total = 0;
function testa(id, codigo, entradas, esperado) {
  total++;
  const r = VA.executar(codigo, entradas || []);
  if (r.erro) {
    falhas++;
    console.log(`FALHA ${id}: erro na linha ${r.erro.linha}: ${r.erro.msg}`);
    return;
  }
  const a = VA.normalizarSaida(r.saida), b = VA.normalizarSaida(esperado);
  if (a !== b) {
    falhas++;
    console.log(`FALHA ${id}: saída diferente\n  programa: ${JSON.stringify(r.saida)}\n  esperado: ${JSON.stringify(esperado)}`);
  }
}

// casos de controle do próprio interpretador
const casos = [
  ['ctrl-para', 'algoritmo "a"\nvar\ni, s: inteiro\ninicio\npara i de 1 ate 5 faca\ns <- s + i\nfimpara\nescreval(s, " ", i)\nfimalgoritmo', [], '15 6'],
  ['ctrl-passo-neg', 'algoritmo "a"\nvar\ni: inteiro\ninicio\npara i de 10 ate 1 passo -3 faca\nescreva(i, " ")\nfimpara\nfimalgoritmo', [], '10 7 4 1'],
  ['ctrl-divmod', 'algoritmo "a"\nvar\nn: inteiro\ninicio\nn <- 347\nescreval(n div 100, n mod 100 div 10, n mod 10, 7 \\ 2, -7 mod 3)\nfimalgoritmo', [], '3 4 7 3 -1'],
  ['ctrl-real', 'algoritmo "a"\nvar\nm: real\ninicio\nm <- (7 + 8) / 2\nescreval(m)\nm <- 10 / 2\nescreval(m)\nfimalgoritmo', [], '7.5\n5'],
  ['ctrl-leia', 'algoritmo "a"\nvar\na, b: inteiro\nnome: caractere\ninicio\nleia(nome)\nleia(a, b)\nse a > b entao\nescreval(nome, " maior: ", a)\nsenao\nescreval(nome, " maior: ", b)\nfimse\nfimalgoritmo', ['Ana', '3', '9'], 'Ana maior: 9'],
  ['ctrl-repita', 'algoritmo "a"\nvar\nx: inteiro\ninicio\nx <- 10\nrepita\nx <- x - 3\nate x < 0\nescreval(x)\nfimalgoritmo', [], '-2'],
  ['ctrl-enquanto0', 'algoritmo "a"\nvar\nx: inteiro\ninicio\nx <- 5\nenquanto x < 3 faca\nx <- x + 1\nfimenquanto\nescreval(x)\nfimalgoritmo', [], '5'],
  ['ctrl-escolha', 'algoritmo "a"\nvar\nd: inteiro\ninicio\nd <- 6\nescolha d\ncaso 1, 7\nescreval("fim de semana")\ncaso 2 ate 6\nescreval("dia útil")\noutrocaso\nescreval("?")\nfimescolha\nfimalgoritmo', [], 'dia útil'],
  ['ctrl-logico', 'algoritmo "a"\nvar\np, q: logico\ninicio\np <- verdadeiro\nq <- falso\nescreval(p e q, " ", p ou q, " ", nao p, " ", p xou q, " ", nao (p e q) = (nao p ou nao q))\nfimalgoritmo', [], 'FALSO VERDADEIRO FALSO VERDADEIRO VERDADEIRO'],
  ['ctrl-vetor', 'algoritmo "a"\nvar\nv: vetor[1..4] de inteiro\ni, s: inteiro\ninicio\npara i de 1 ate 4 faca\nv[i] <- i * i\nfimpara\npara i de 1 ate 4 faca\ns <- s + v[i]\nfimpara\nescreval(s)\nfimalgoritmo', [], '30'],
  ['ctrl-interrompa', 'algoritmo "a"\nvar\ni: inteiro\ninicio\npara i de 1 ate 10 faca\nse i = 4 entao\ninterrompa\nfimse\nescreva(i)\nfimpara\nfimalgoritmo', [], '1 2 3'],
  ['ctrl-precedencia', 'algoritmo "a"\nvar\nx: inteiro\ninicio\nx <- 2 + 3 * 4 ^ 2 - 10 div 3\nescreval(x, " ", -2 ^ 2)\nfimalgoritmo', [], '47 -4'],
  ['ctrl-formato', 'algoritmo "a"\nvar\nm: real\ni: inteiro\ninicio\nm <- 43 / 6\ni <- 7\nescreval("M:", m:5:2, " I:", i:3)\nfimalgoritmo', [], 'M: 7.17 I: 7'],
  ['ctrl-ponto-e-virgula', 'algoritmo "a"\nvar x: inteiro;\ninicio\nx <- 5;\nescreval(x);\nfimalgoritmo', [], '5'],
  ['ctrl-texto-maiuscula', 'algoritmo "a"\nvar\nc: caractere\ninicio\nc <- "abc"\nse c = "ABC" entao\nescreval("igual")\nfimse\nescolha "b"\ncaso "B"\nescreval("caso B")\nfimescolha\nfimalgoritmo', [], 'igual\ncaso B'],
  ['ctrl-acentos', 'algoritmo "a"\nvar\nx: inteiro\ninicio\nx <- 3\nse x > 2 então\nescreval("sim")\nsenão\nescreval("não")\nfimse\nfimalgoritmo', [], 'sim'],
  // funcao e procedimento (17/11/2026): forma dos Exemplos do VisuAlg (fatorial2.alg, troca.alg, buscbinr.alg, decpoutras.alg)
  ['ctrl-funcao-recursao', 'algoritmo "a"\nfuncao fat(n: inteiro): inteiro\ninicio\nse n <= 1 entao\nretorne 1\nfimse\nretorne n * fat(n - 1)\nfimfuncao\ninicio\nescreval(fat(5))\nfimalgoritmo', [], '120'],
  ['ctrl-procedimento-ref', 'algoritmo "a"\nvar\nv: vetor[1..3] de inteiro\na, b: inteiro\nprocedimento troca(var x, y: inteiro)\nvar t: inteiro\ninicio\nt <- x\nx <- y\ny <- t\nfimprocedimento\ninicio\na <- 1\nb <- 2\ntroca(a, b)\nv[1] <- 10\nv[3] <- 30\ntroca(v[1], v[3])\nescreval(a, b, v[1], v[3])\nfimalgoritmo', [], '2 1 30 10'],
  ['ctrl-funcao-local', 'algoritmo "a"\nvar\nx: inteiro\nprocedimento p(n: inteiro)\nvar x: inteiro\ninicio\nx <- n * 2\nn <- 0\nescreva(x)\nfimprocedimento\ninicio\nx <- 7\np(x)\nescreval(x)\nfimalgoritmo', [], '14 7'],
  ['ctrl-funcao-sem-parenteses', 'algoritmo "a"\nfuncao dez: inteiro\ninicio\nretorne 10\nfimfuncao\ninicio\nescreval(dez + 1)\nfimalgoritmo', [], '11'],
  ['ctrl-funcao-texto-logico', 'algoritmo "a"\nfuncao par(n: inteiro): logico\ninicio\nretorne n mod 2 = 0\nfimfuncao\nfuncao rotulo(n: inteiro): caractere\ninicio\nse par(n) entao\nretorne "par"\nsenao\nretorne "impar"\nfimse\nfimfuncao\ninicio\nescreval(rotulo(4), " ", rotulo(7))\nfimalgoritmo', [], 'par impar'],
];
for (const c of casos) testa(c[0], c[1], c[2], c[3]);

// erros que o VisuAlg também acusa
const deveErrar = [
  ['erro-real-em-inteiro', 'algoritmo "a"\nvar\nm: inteiro\ninicio\nm <- 7 / 2\nfimalgoritmo'],
  ['erro-infinito', 'algoritmo "a"\nvar\nx: inteiro\ninicio\nenquanto x >= 0 faca\nx <- x + 1\nfimenquanto\nfimalgoritmo'],
  ['erro-nao-declarada', 'algoritmo "a"\ninicio\ny <- 1\nfimalgoritmo'],
  // regras do site para sub-rotinas (não conferidas no VisuAlg real)
  ['erro-retorne-fora', 'algoritmo "a"\ninicio\nretorne 1\nfimalgoritmo'],
  ['erro-funcao-sem-retorne', 'algoritmo "a"\nfuncao f(n: inteiro): inteiro\ninicio\nn <- 1\nfimfuncao\ninicio\nescreval(f(2))\nfimalgoritmo'],
  ['erro-qtd-argumentos', 'algoritmo "a"\nfuncao f(n: inteiro): inteiro\ninicio\nretorne n\nfimfuncao\ninicio\nescreval(f(1, 2))\nfimalgoritmo'],
  ['erro-procedimento-inexistente', 'algoritmo "a"\nprocedimento p\ninicio\nescreval("p")\nfimprocedimento\ninicio\nq\nfimalgoritmo'],
];
for (const [id, cod] of deveErrar) {
  total++;
  const r = VA.executar(cod, []);
  if (!r.erro) { falhas++; console.log(`FALHA ${id}: deveria dar erro`); }
}

const pasta = process.argv[2];
const extras = process.argv.slice(3);
const arquivos = [];
if (pasta && fs.existsSync(pasta)) for (const f of fs.readdirSync(pasta)) if (f.endsWith('.json')) arquivos.push(path.join(pasta, f));
for (const f of extras) arquivos.push(f);
let nq = 0;
for (const f of arquivos) {
  const d = JSON.parse(fs.readFileSync(f, 'utf8'));
  for (const q of d.questoes || []) {
    if (!q.codigo) continue;
    nq++;
    // entradasTeste: exemplos que no laboratório começam sem respostas (o programa pergunta)
    testa(q.id, q.codigo, q.entradasTeste || q.entradas, q.saida);
  }
}
// projeto final de Lógica: o Portugol de cada exemplo tem de dar a saída conferida (saidas.json)
const PF = path.join(__dirname, 'projeto_final');
let npf = 0;
if (fs.existsSync(path.join(PF, 'saidas.json'))) {
  const s = JSON.parse(fs.readFileSync(path.join(PF, 'saidas.json'), 'utf8')).exemplos;
  for (const id of Object.keys(s)) {
    npf++;
    testa('projeto-' + id, fs.readFileSync(path.join(PF, id + '.alg'), 'utf8'), s[id].entradas, s[id].saida);
  }
}
console.log(`${total} testes (${nq} questões com código, ${npf} exemplos do projeto final); ${falhas} falha(s)`);
process.exit(falhas ? 1 : 0);
