// Revisao lp_s6: roda no interpretador do site versoes "erradas" dos codigos
// (a mudanca que cada distrator descreve) e confere que dao o valor da alternativa.
// Uso: node rev_lp_s6_distratores.js
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
function roda(id, troca, entradas, esperado) {
  const q = qs[id];
  let cod = q.codigo;
  for (const [de, para] of troca) {
    if (!cod.includes(de)) { falhas++; console.log('FALHA ' + id + ': trecho nao achado ' + JSON.stringify(de)); return; }
    cod = cod.replace(de, para);
  }
  const r = VA.executar(cod, entradas === null ? (q.entradas || []) : entradas);
  const got = r.erro ? 'ERRO ' + r.erro.msg : VA.normalizarSaida(r.saida);
  const okk = got === VA.normalizarSaida(esperado);
  if (!okk) falhas++;
  console.log((okk ? 'ok    ' : 'FALHA ') + id + ' -> ' + JSON.stringify(got) + ' (alternativa ' + JSON.stringify(esperado) + ')');
  if (!q.alternativas.some(a => !a.certa && VA.normalizarSaida(a.t) === VA.normalizarSaida(esperado))) {
    falhas++; console.log('FALHA ' + id + ': alternativa errada ' + esperado + ' nao existe');
  }
}
roda('lp-s6-p01', [['se i mod 2 = 0 entao', 'se verdadeiro entao']], null, '21');
roda('lp-s6-p01', [['se i mod 2 = 0 entao', 'se i mod 2 = 1 entao']], null, '9');
roda('lp-s6-p01', [['s <- s + i', 's <- s + 1']], null, '3');
roda('lp-s6-p01', [['s <- s + i', 's <- i']], null, '6');
roda('lp-s6-p02', [['passo 4', 'passo 1']], null, '13');
roda('lp-s6-p03', [['para i de 10 ate 2 passo -2', 'para i de 2 ate 10 passo 2']], null, '2 4 6 8 10');
roda('lp-s6-p03', [['para i de 10 ate 2 passo -2', 'para i de 10 ate 4 passo -2']], null, '10 8 6 4');
roda('lp-s6-p03', [['para i de 10 ate 2 passo -2', 'para i de 8 ate 2 passo -2']], null, '8 6 4 2');
roda('lp-s6-p04', [['enquanto x < 10 faca', 'enquanto nao (x < 10) faca']], null, 'c = 4, x = 8');
roda('lp-s6-p05', [['repita\n', 'enquanto nao (n > 40) faca\n'], ['ate n > 40', 'fimenquanto']], null, '0 50');
roda('lp-s6-p05', [['ate n > 40', 'ate n > 60']], null, '2 70');
roda('lp-s6-p06', [['se v > 100 entao', 'se v >= 100 entao']], null, '3 470');
roda('lp-s6-p06', [['se v > 100 entao', 'se verdadeiro entao']], null, '5 590');
roda('lp-s6-p06', [['s <- s + v', 's <- v']], null, '2 250');
roda('lp-s6-p06', [['se v > 100 entao', 'se v <= 100 entao']], null, '3 220');
roda('lp-s6-p07', [['         interrompa\n', '']], null, '35 21');
roda('lp-s6-p07', [['      c <- c + 1\n      se i mod 7 = 0 entao\n         achou <- i\n         interrompa\n      fimse', '      se i mod 7 = 0 entao\n         achou <- i\n         interrompa\n      fimse\n      c <- c + 1']], null, '21 1');
roda('lp-s6-p08', [['para i de 2 ate 4 faca', 'para i de 1 ate 5 faca']], null, '15 45');
roda('lp-s6-p08', [['s <- s + v[i]', 's <- s + i']], null, '15 9');
roda('lp-s6-p08', [['para i de 2 ate 4 faca', 'para i de 2 ate 3 faca']], null, '15 15');
roda('lp-s6-p11', [['para i de 1 ate 4 faca', 'para i de 1 ate 5 faca']], null, '8 13');
roda('lp-s6-p11', [['      t <- a + b', '      a <- 1\n      b <- 1\n      t <- a + b']], null, '1 2');
roda('lp-s6-p11', [['para i de 1 ate 4 faca', 'para i de 1 ate 3 faca']], null, '3 5');
roda('lp-s6-p11', [['      a <- b\n      b <- t', '      b <- t\n      a <- b']], null, '16 16');
roda('lp-s6-p12', [['   repita\n', '   enquanto x <> 0 faca\n'], ['   ate x = 0', '   fimenquanto']], null, '0 0');
roda('lp-s6-p12', [['ate x = 0', 'ate nao (x = 0)']], null, '7 1');
// p09: correcao C (partir do primeiro lido) em varios casos, inclusive todos acima de 100 e negativos
const corrC = qs['lp-s6-p09'].codigo
  .replace('   maior <- 0\n   menor <- 0\n   para i de 1 ate 4 faca\n      leia(x)', '   leia(x)\n   maior <- x\n   menor <- x\n   para i de 2 ate 4 faca\n      leia(x)');
for (const ent of [['15', '8', '23', '11'], ['150', '200', '300', '120'], ['-5', '-9', '-2', '-7']]) {
  const r = VA.executar(corrC, ent);
  const n = ent.map(Number);
  const esp = Math.max(...n) + ' ' + Math.min(...n);
  const got = r.erro ? 'ERRO ' + r.erro.msg : VA.normalizarSaida(r.saida);
  const okk = got === VA.normalizarSaida(esp);
  if (!okk) falhas++;
  console.log((okk ? 'ok    ' : 'FALHA ') + 'p09 correcao C com ' + ent.join(',') + ' -> ' + got);
}
const corrE = qs['lp-s6-p09'].codigo.replace('menor <- 0', 'menor <- 100');
const rE = VA.executar(corrE, ['150', '200', '300', '120']);
console.log('p09 correcao E com 150,200,300,120 -> ' + VA.normalizarSaida(rE.saida) + ' (menor fica 100: falha esperada)');
if (VA.normalizarSaida(rE.saida) !== '300 100') falhas++;
console.log(falhas ? falhas + ' falha(s)' : 'OK');
