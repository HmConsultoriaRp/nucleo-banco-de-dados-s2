// Confere no interpretador do site as afirmacoes dos textos "confira" do lote lp_s5.
// Uso: node lp_s5_afirmacoes.js
const path = require('path');
const fs = require('fs');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const dados = path.join(__dirname, '..', 'dados');
const qs = {};
for (const f of ['lp_s5_p1.json', 'lp_s5_p2.json']) {
  for (const q of JSON.parse(fs.readFileSync(path.join(dados, f), 'utf8')).questoes) qs[q.id] = q;
}
let falhas = 0;
function roda(cod, ent) { return VA.executar(cod, ent || []); }
function saida(cod, ent) { const r = roda(cod, ent); return r.erro ? 'ERRO: ' + r.erro.msg : VA.normalizarSaida(r.saida); }
function espera(rotulo, obtido, esperado) {
  const ok = obtido === VA.normalizarSaida(esperado);
  if (!ok) falhas++;
  console.log((ok ? 'ok    ' : 'FALHA ') + rotulo + ' -> ' + JSON.stringify(obtido) + (ok ? '' : ' (esperado ' + JSON.stringify(esperado) + ')'));
}
function esperaErro(rotulo, cod, ent) {
  const r = roda(cod, ent);
  if (!r.erro) falhas++;
  console.log((r.erro ? 'ok    ' : 'FALHA ') + rotulo + ' -> ' + (r.erro ? 'erro: ' + r.erro.msg : 'rodou sem erro'));
}
const casca = (decl, corpo) => 'algoritmo "t"\nvar\n' + decl + '\ninicio\n' + corpo + '\nfimalgoritmo';

// p02: troca com 2 e 7
espera('p02 a=2 b=7', saida(qs['lp-s5-p02'].codigo.replace('a <- 8', 'a <- 2').replace('b <- 5', 'b <- 7')), '7 2');

// p03: so saldo2 declara sem erro
for (const nome of ['2trimestre', 'valor total', 'custo-medio', 'taxa%']) esperaErro('p03 ' + nome, casca(nome + ': inteiro', 'escreval(1)'));
espera('p03 saldo2', saida(casca('saldo2: inteiro', 'saldo2 <- 3\nescreval(saldo2)')), '3');

// p05: as cinco alternativas com 2000 e 300
const decl5 = 'valor, taxa: inteiro';
const alt5 = {
  certa: 'se valor > 1000 entao\ntaxa <- 20\nsenao\ntaxa <- 5\nfimse',
  trocados: 'se valor > 1000 entao\ntaxa <- 5\nsenao\ntaxa <- 20\nfimse',
  semSenao: 'se valor > 1000 entao\ntaxa <- 20\nfimse\ntaxa <- 5',
  enquanto: 'enquanto valor > 1000 faca\ntaxa <- 20\nfimenquanto\ntaxa <- 5',
  leia: 'leia(valor > 1000)\ntaxa <- 20\ntaxa <- 5'
};
const p5 = (k, v) => saida(casca(decl5, 'valor <- ' + v + '\n' + alt5[k] + '\nescreval(taxa)'));
espera('p05 certa 2000', p5('certa', 2000), '20');
espera('p05 certa 300', p5('certa', 300), '5');
espera('p05 trocados 2000', p5('trocados', 2000), '5');
espera('p05 trocados 300', p5('trocados', 300), '20');
espera('p05 sem senao 2000', p5('semSenao', 2000), '5');
espera('p05 sem senao 300', p5('semSenao', 300), '5');
esperaErro('p05 enquanto com 2000 nao termina', casca(decl5, 'valor <- 2000\n' + alt5.enquanto + '\nescreval(taxa)'));
esperaErro('p05 leia(valor > 1000)', casca(decl5, alt5.leia + '\nescreval(taxa)'), ['2000']);

// p06: versao com parenteses explicitos
espera('p06 parenteses', saida(casca('x: inteiro', 'x <- 50 - (4 * (2 ^ 3)) + (23 mod 6)\nescreval(x)')), '23');

// p07: versao corrigida e versao com parenteses do VisuAlg
const c7 = qs['lp-s5-p07'].codigo;
espera('p07 corrigida', saida(c7.replace('n1 + n2 / 2', '(n1 + n2) / 2'), ['4', '5']), 'Recuperação 4.5');
espera('p07 n1 + (n2 / 2)', saida(c7.replace('n1 + n2 / 2', 'n1 + (n2 / 2)'), ['4', '5']), 'Aprovado 6.5');

// p08: limites
const c8 = qs['lp-s5-p08'].codigo;
for (const [m, e] of [['3', 'T1'], ['4', 'T2'], ['6', 'T2'], ['13', 'Mês inválido'], ['0', 'T1']]) espera('p08 mes ' + m, saida(c8, [m]), e);

// p09: parenteses da leitura certa e da errada
const c9 = qs['lp-s5-p09'].codigo;
espera('p09 parenteses certos', saida(c9.replace('nao (x > 5) ou (y > 5) e (x mod 2 = 1)', 'nao (x > 5) ou ((y > 5) e (x mod 2 = 1))')), 'VERDADEIRO FALSO');
espera('p09 parenteses errados', saida(c9.replace('nao (x > 5) ou (y > 5) e (x mod 2 = 1)', '(nao (x > 5) ou (y > 5)) e (x mod 2 = 1)')), 'FALSO FALSO');
espera('p09 De Morgan completa', saida(c9.replace('nao ((x > 5) ou (y > 5))', '(nao (x > 5)) e (nao (y > 5))')), 'VERDADEIRO FALSO');

// p10: entrada 100
espera('p10 entrada 100', saida(qs['lp-s5-p10'].codigo, ['100']), '1 1');

// p11: outros caminhos
const c11 = qs['lp-s5-p11'].codigo;
espera('p11 17 e 3000', saida(c11, ['17', '3000']), 'EF');
espera('p11 18 e 3001', saida(c11, ['18', '3001']), 'ABDF');

// p12: cinco condicoes no interpretador, cinco casos
const conds = {
  A: '(valor > 200) ou (vip e dist <= 50)',
  B: '(valor >= 200 ou vip) e dist <= 50',
  C: 'valor >= 200 e vip ou dist <= 50',
  D: '(valor >= 200) ou (vip e dist <= 50)',
  E: '(valor >= 200) ou (vip e dist >= 50)'
};
const tab = qs['lp-s5-p12'].tabela.linhas;
for (const linha of tab) {
  const [caso, v, vip, dist] = linha;
  for (const [i, k] of ['A', 'B', 'C', 'D', 'E'].entries()) {
    const cod = casca('valor: real\nvip: logico\ndist: inteiro',
      'valor <- ' + v + '\nvip <- ' + (vip === 'V' ? 'verdadeiro' : 'falso') + '\ndist <- ' + dist +
      '\nse ' + conds[k] + ' entao\nescreval("V")\nsenao\nescreval("F")\nfimse');
    espera('p12 caso ' + caso + ' alt ' + k, saida(cod), linha[5 + i]);
  }
}
console.log(falhas ? falhas + ' falha(s)' : 'todas as afirmações conferem no interpretador do site');
process.exit(falhas ? 1 : 0);
