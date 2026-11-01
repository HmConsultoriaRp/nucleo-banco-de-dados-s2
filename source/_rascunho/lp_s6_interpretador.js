// Confere no interpretador do site o que os textos do lote lp_s6 afirmam sobre o teste de mesa.
// Uso: node lp_s6_interpretador.js
const fs = require('fs');
const path = require('path');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const ger = path.join(__dirname, '..');
const qs = {};
for (const f of ['lp_s6_p1.json', 'lp_s6_p2.json']) {
  const d = JSON.parse(fs.readFileSync(path.join(ger, 'dados', f), 'utf8'));
  for (const q of d.questoes) qs[q.id] = q;
}
let falhas = 0;
function ok(c, m) { if (!c) { falhas++; console.log('FALHA ' + m); } }

// p04: a linha 7 (enquanto) aparece uma vez, com condicao FALSA
let r = VA.executar(qs['lp-s6-p04'].codigo, []);
let l7 = r.passos.filter(p => p.linha === 7);
console.log('p04 linha 7:', l7.map(p => p.nota));
ok(l7.length === 1 && /FALSA/.test(l7[0].nota), 'p04 linha 7');

// p05: a linha do ate aparece uma vez
r = VA.executar(qs['lp-s6-p05'].codigo, qs['lp-s6-p05'].entradas);
const linhaAte = qs['lp-s6-p05'].codigo.split('\n').findIndex(l => l.trim().startsWith('ate ')) + 1;
let la = r.passos.filter(p => p.linha === linhaAte);
console.log('p05 linha do ate (' + linhaAte + '):', la.map(p => p.nota));
ok(la.length === 1, 'p05 ate uma vez');

// p07: ultimo valor de c antes do escreval
r = VA.executar(qs['lp-s6-p07'].codigo, []);
const antes = r.passos[r.passos.length - 3];
console.log('p07 c antes do escreval:', antes.vars.c, '| i:', antes.vars.i);
ok(antes.vars.c === '2', 'p07 c = 2');

// p09: coluna menor nunca muda
r = VA.executar(qs['lp-s6-p09'].codigo, qs['lp-s6-p09'].entradas);
const menores = new Set(r.passos.map(p => p.vars.menor));
console.log('p09 valores de menor:', [...menores]);
ok(menores.size === 1, 'p09 menor nao muda');

// p10: os cinco trechos montados como programa
function trecho(antes, laco, corpo) {
  let cod = 'algoritmo "t"\nvar\n   x: inteiro\ninicio\n   ' + antes + '\n';
  if (laco.startsWith('repita')) cod += '   repita\n      ' + corpo + '\n   ' + laco.replace('repita ... ', '') + '\n';
  else cod += '   ' + laco + '\n      ' + corpo + '\n   fimenquanto\n';
  cod += '   escreval(x)\nfimalgoritmo';
  return cod;
}
for (const l of qs['lp-s6-p10'].tabela.linhas) {
  const cod = trecho(...l.slice(1).map(s => s.replace(/`/g, '')));
  const rr = VA.executar(cod, []);
  console.log('p10 trecho ' + l[0] + ':', rr.erro ? 'ERRO ' + rr.erro.msg : 'termina com x =' + rr.saida.trim());
  ok(l[0] === '3' ? !!rr.erro && /5000 passos/.test(rr.erro.msg) : !rr.erro, 'p10 trecho ' + l[0]);
}

// p12: c vira 4 na volta do 0, antes da linha do ate
r = VA.executar(qs['lp-s6-p12'].codigo, qs['lp-s6-p12'].entradas);
const i4 = r.passos.findIndex(p => p.vars.c === '4');
console.log('p12 passo em que c = 4:', r.passos[i4].linha, '| x =', r.passos[i4].vars.x, '| proximo:', r.passos[i4 + 1].linha, r.passos[i4 + 1].nota);

// lab: exemplo "Senha com repita" com 1234 primeiro
const exs = JSON.parse(fs.readFileSync(path.join(ger, 'exemplos_visualg.json'), 'utf8')).questoes;
const senha = exs.find(e => e.titulo === 'Senha com repita');
r = VA.executar(senha.codigo, ['1234', '0000', '4321']);
console.log('lab senha com 1234 primeiro:', JSON.stringify(r.saida));
ok(/tentativa\s+1\b/.test(r.saida), 'lab senha');

console.log(falhas ? falhas + ' falha(s)' : 'OK');
