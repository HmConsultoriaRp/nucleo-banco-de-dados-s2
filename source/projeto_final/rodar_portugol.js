// Roda um .alg (UTF-8) no interpretador do site e imprime JSON com a saída normal e a da tela
// (a tela mostra também o que foi digitado, como no laboratório).
// Uso: node rodar_portugol.js <arquivo.alg> <entradas.json>
const fs = require('fs');
const path = require('path');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const cod = fs.readFileSync(process.argv[2], 'utf8');
const ent = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
const r = VA.executar(cod, ent, { maxPassos: 50000 });
const g = VA.executar(cod, ent, { guiada: true, maxPassos: 50000 });
process.stdout.write(JSON.stringify({ saida: r.saida, erro: r.erro, tela: g.saida, erroTela: g.erro, passos: r.passos.length }));
