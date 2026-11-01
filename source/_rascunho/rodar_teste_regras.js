// Roda o teste_regras_visualg.alg no interpretador do site e mostra a saída exata (espaços visíveis como ·).
const fs = require('fs');
const path = require('path');
const VA = require(path.join(__dirname, '..', 'site', 'visualg.js'));
const cod = fs.readFileSync(path.join(__dirname, '..', 'teste_regras_visualg.alg'), 'utf8');
const r = VA.executar(cod, []);
if (r.erro) console.log('ERRO linha', r.erro.linha, r.erro.msg);
console.log(r.saida.replace(/ /g, '·'));
