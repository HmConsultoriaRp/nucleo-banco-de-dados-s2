// Revisao lp_s6 rodada 2: confere no interpretador do site as frases sobre o teste de mesa.
// Uso: node rev_lp_s6_r2_mesa.js
const fs = require('fs');
const path = require('path');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const ger = path.join(__dirname, '..');
const qs = {};
for (const f of ['lp_s6_p1.json', 'lp_s6_p2.json']) {
  const d = JSON.parse(fs.readFileSync(path.join(ger, 'dados', f), 'utf8'));
  for (const q of d.questoes) qs[q.id] = q;
}
function run(id) { const q = qs[id]; return VA.executar(q.codigo, q.entradas || []); }
function colunas(r, nome) { return r.passos.map(p => p.vars[nome]); }
function distintos(arr) { const o = []; for (const x of arr) if (o[o.length - 1] !== x) o.push(x); return o; }

// p02: o que aparece na coluna do i
let r = run('lp-s6-p02');
console.log('p02 coluna i (sem repeticao seguida):', distintos(colunas(r, 'i')).join(' '));
console.log('p02 coluna c:', distintos(colunas(r, 'c')).join(' '));
console.log('p02 notas do para:', r.passos.filter(p => p.linha === 6).map(p => p.nota).join(' | '));
// p03
r = run('lp-s6-p03');
console.log('p03 coluna i:', distintos(colunas(r, 'i')).join(' '), '| saida', JSON.stringify(r.saida));
// p04 linha 7
r = run('lp-s6-p04');
console.log('p04 passos na linha 7:', r.passos.filter(p => p.linha === 7).map(p => p.nota));
// p05 linha do ate
r = run('lp-s6-p05');
console.log('p05 passos:', r.passos.map(p => p.linha + ':' + p.nota).join(' | '));
// p07
r = run('lp-s6-p07');
console.log('p07 ultimos passos:', r.passos.slice(-5).map(p => p.linha + ':' + p.nota + ' c=' + p.vars.c + ' i=' + p.vars.i).join(' | '));
// p08 vetor
r = run('lp-s6-p08');
console.log('p08 coluna v:', distintos(colunas(r, 'v')).join(' ; '));
// p09 menor
r = run('lp-s6-p09');
console.log('p09 coluna menor:', distintos(colunas(r, 'menor')).join(' '), '| maior', distintos(colunas(r, 'maior')).join(' '));
// p11
r = run('lp-s6-p11');
console.log('p11 saida', JSON.stringify(r.saida));
// p12
r = run('lp-s6-p12');
console.log('p12 ultimos passos:', r.passos.slice(-6).map(p => p.linha + ':' + p.nota + ' x=' + p.vars.x + ' c=' + p.vars.c).join(' | '));

// p10: cada trecho como algoritmo completo
const trechos = [
  'x <- 1\nenquanto x < 10 faca\nx <- x + 2\nfimenquanto',
  'x <- 20\nenquanto x > 0 faca\nx <- x div 2\nfimenquanto',
  'x <- 1\nenquanto x <> 10 faca\nx <- x + 2\nfimenquanto',
  'x <- 10\nrepita\nx <- x - 3\nate x < 0',
  'x <- 1\nenquanto x <= 100 faca\nx <- x * 2\nfimenquanto',
];
trechos.forEach((t, k) => {
  const cod = 'algoritmo "t"\nvar\nx: inteiro\ninicio\n' + t + '\nescreval(x)\nfimalgoritmo';
  const rr = VA.executar(cod, []);
  console.log('p10 trecho ' + (k + 1) + ':', rr.erro ? 'ERRO ' + rr.erro.msg : 'termina, x =' + rr.saida.trim());
});

// laboratorio: Senha com repita com 1234 primeiro
const labs = JSON.parse(fs.readFileSync(path.join(ger, 'exemplos_visualg.json'), 'utf8')).questoes;
const senha = labs.find(e => e.titulo === 'Senha com repita');
console.log('lab existe:', !!senha, 'semana', senha && senha.semana);
let rl = VA.executar(senha.codigo, ['1234', '4321', '0000']);
console.log('lab saida:', JSON.stringify(rl.saida), '| passo inicial mostra saida:', JSON.stringify(rl.passos[0].saida), '| passos', rl.passos.length);
rl = VA.executar(senha.codigo, ['1234']);
console.log('lab so 1234:', JSON.stringify(rl.saida), rl.erro);

// formulas da teoria: comandos em uma linha rodam no interpretador?
const f1 = 'algoritmo "f"\nvar\nv: vetor[1..5] de inteiro\ni, s, x, maior, menor: inteiro\ninicio\npara i de 1 ate 5 faca leia(v[i]) fimpara\npara i de 1 ate 5 faca s <- s + v[i] fimpara\nx <- 7\nmaior <- 3\nse x > maior entao maior <- x fimse\nescreval(s, " ", maior)\nfimalgoritmo';
const rf = VA.executar(f1, ['1', '2', '3', '4', '5']);
console.log('formulas em uma linha:', rf.erro ? 'ERRO ' + rf.erro.msg : JSON.stringify(rf.saida));
