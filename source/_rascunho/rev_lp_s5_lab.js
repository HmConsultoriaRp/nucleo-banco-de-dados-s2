// Revisao do lote lp_s5: confere no interpretador do site o que os textos "confira" mandam testar no laboratorio.
// Uso: node rev_lp_s5_lab.js
const fs = require('fs');
const path = require('path');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const DADOS = path.join(__dirname, '..', 'dados');
const qs = {};
for (const f of fs.readdirSync(DADOS)) if (/^lp_s5_p\d+\.json$/.test(f)) for (const q of JSON.parse(fs.readFileSync(path.join(DADOS, f), 'utf8')).questoes) qs[q.id] = q;

let falhas = 0, n = 0;
function roda(cod, ent) { return VA.executar(cod, ent || []); }
function saida(cod, ent) { const r = roda(cod, ent); return r.erro ? 'ERRO: ' + r.erro.msg : VA.normalizarSaida(r.saida); }
function igual(id, obtido, esperado) { n++; esperado = VA.normalizarSaida(esperado); if (obtido !== esperado) { falhas++; console.log('FALHA', id, JSON.stringify(obtido), '!=', JSON.stringify(esperado)); } }
function erra(id, cod, ent) { n++; const r = roda(cod, ent); if (!r.erro) { falhas++; console.log('FALHA', id, 'deveria dar erro e deu', JSON.stringify(r.saida)); } }

// cada questao com codigo: saida do campo
for (const id of Object.keys(qs).sort()) {
  const q = qs[id];
  if (q.codigo) igual(id + ' saida', saida(q.codigo, q.entradas), VA.normalizarSaida(q.saida));
}

// p03: os quatro nomes invalidos param o programa; saldo2 passa
const p03 = n => 'algoritmo "t"\nvar\n   ' + n + ': inteiro\ninicio\nfimalgoritmo';
for (const nome of ['2trimestre', 'valor total', 'custo-medio', 'taxa%']) erra('p03 ' + nome, p03(nome));
igual('p03 saldo2', saida(p03('saldo2')), '');

// p05: as alternativas como programas, valores 2000 e 300
const p05 = (corpo) => 'algoritmo "t"\nvar\n   valor, taxa: inteiro\ninicio\n   leia(valor)\n' + corpo + '\n   escreval(taxa)\nfimalgoritmo';
const altE = 'se valor > 1000 entao\ntaxa <- 20\nsenao\ntaxa <- 5\nfimse';
const altA = 'se valor > 1000 entao\ntaxa <- 5\nsenao\ntaxa <- 20\nfimse';
const altB = 'se valor > 1000 entao\ntaxa <- 20\nfimse\ntaxa <- 5';
const altC = 'enquanto valor > 1000 faca\ntaxa <- 20\nfimenquanto\ntaxa <- 5';
const altD = 'leia(valor > 1000)\ntaxa <- 20\ntaxa <- 5';
for (const [nome, corpo, s2000, s300] of [['E', altE, '20', '5'], ['A', altA, '5', '20'], ['B', altB, '5', '5']]) {
  igual('p05 ' + nome + ' 2000', saida(p05(corpo), ['2000']), s2000);
  igual('p05 ' + nome + ' 300', saida(p05(corpo), ['300']), s300);
}
erra('p05 C nao termina', p05(altC), ['2000']);
erra('p05 D leia', p05(altD), ['2000', '1']);

// p06: com parenteses explicitos a saida nao muda
const p06 = qs['lp-s5-p06'].codigo;
igual('p06 parenteses', saida(p06.replace('50 - 4 * 2 ^ 3 + 23 mod 6', '50 - (4 * (2 ^ 3)) + (23 mod 6)')), '23');

// p07: com a linha corrigida sai Recuperacao 4.5; com parenteses implicitos nao muda
const p07 = qs['lp-s5-p07'].codigo;
igual('p07 corrigido', saida(p07.replace('n1 + n2 / 2', '(n1 + n2) / 2'), ['4', '5']), 'Recuperação 4.5');
igual('p07 implicitos', saida(p07.replace('n1 + n2 / 2', 'n1 + (n2 / 2)'), ['4', '5']), 'Aprovado 6.5');

// p08: limites
const p08 = qs['lp-s5-p08'].codigo;
igual('p08 3', saida(p08, ['3']), 'T1');
igual('p08 4', saida(p08, ['4']), 'T2');
igual('p08 13', saida(p08, ['13']), 'Mês inválido');
igual('p08 0', saida(p08, ['0']), 'T1');
igual('p08 12', saida(p08, ['12']), 'T4');

// p09: parenteses da leitura certa e da errada
const p09 = qs['lp-s5-p09'].codigo;
const linhaP = 'nao (x > 5) ou (y > 5) e (x mod 2 = 1)';
igual('p09 certa explicita', saida(p09.replace(linhaP, 'nao (x > 5) ou ((y > 5) e (x mod 2 = 1))')), 'VERDADEIRO FALSO');
igual('p09 leitura errada', saida(p09.replace(linhaP, '(nao (x > 5) ou (y > 5)) e (x mod 2 = 1)')), 'FALSO FALSO');
igual('p09 nao no resto todo', saida(p09.replace(linhaP, 'nao ((x > 5) ou (y > 5) e (x mod 2 = 1))')), 'VERDADEIRO FALSO');
igual('p09 De Morgan completa', saida(p09.replace('nao ((x > 5) ou (y > 5))', '(nao (x > 5)) e (nao (y > 5))')), 'VERDADEIRO FALSO');

// p10: confira com 100 e prova inversa
const p10 = qs['lp-s5-p10'].codigo;
igual('p10 100', saida(p10, ['100']), '1 1');
igual('p10 385', saida(p10, ['385']), '583 16');

// p11: outros caminhos
const p11 = qs['lp-s5-p11'].codigo;
igual('p11 17 3000', saida(p11, ['17', '3000']), 'EF');
igual('p11 18 3001', saida(p11, ['18', '3001']), 'ABDF');

// p12: as cinco condicoes num programa, nos cinco casos da tabela
const conds = {
  A: '(valor > 200) ou (vip e dist <= 50)',
  B: '(valor >= 200 ou vip) e dist <= 50',
  C: 'valor >= 200 e vip ou dist <= 50',
  D: '(valor >= 200) ou (vip e dist <= 50)',
  E: '(valor >= 200) ou (vip e dist >= 50)',
};
const tab = qs['lp-s5-p12'].tabela.linhas;
for (const L of 'ABCDE') {
  const cod = 'algoritmo "t"\nvar\n   valor: real\n   vip: logico\n   dist: inteiro\ninicio\n   leia(valor, vip, dist)\n   escreval(' + conds[L] + ')\nfimalgoritmo';
  tab.forEach((l, i) => {
    const s = saida(cod, [l[1], l[2] === 'V' ? 'verdadeiro' : 'falso', l[3]]);
    igual('p12 ' + L + ' caso ' + (i + 1), s, l[5 + 'ABCDE'.indexOf(L)] === 'V' ? 'VERDADEIRO' : 'FALSO');
  });
}
console.log(n + ' testes; ' + falhas + ' falha(s)');
process.exit(falhas ? 1 : 0);
