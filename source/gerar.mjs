// Monta o site Núcleo em um único HTML usando apenas Node.js.
// Uso: node gerar.mjs "<caminho do html de saída>"
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.join(AQUI, 'site');
const DADOS = path.join(AQUI, 'dados');
const INICIO = '2026-10-26';
// Tira-dúvidas na página publicada. false = a página sai SEM ele: sem o item do menu, a seção,
// o atalho fixo, os botões "Tenho uma dúvida" e o duvidas.js. Ligar (true) só depois do teste
// com dúvida real e com a rotina de respostas ligada, e com ok do dono do site.
const TIRA_DUVIDAS_NO_AR = true;   // ligado em 13/11/2026, com ok do dono do site

const ler = (p) => fs.readFileSync(p, 'utf8');
const natural = new Intl.Collator('pt-BR', { numeric: true, sensitivity: 'base' });

function ordemOrigem(q) {
  const origem = q.origem || '';
  if (origem.startsWith('Avaliação')) return 0;
  if (origem.startsWith('Lista')) return 1;
  if (origem.startsWith('Constru')) return 2;
  return 3;
}

function agoraBrasil() {
  const partes = new Intl.DateTimeFormat('pt-BR', {
    timeZone: 'America/Sao_Paulo', day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit', hour12: false
  }).formatToParts(new Date());
  const p = Object.fromEntries(partes.map((x) => [x.type, x.value]));
  return `${p.day}/${p.month}/${p.year} ${p.hour}:${p.minute}`;
}

function main(saida) {
  const disc = { ga: { semanas: {}, questoes: [], vocabulario: null }, lp: { semanas: {}, questoes: [], vocabulario: null } };
  const ids = new Set();
  const arquivos = fs.readdirSync(DADOS).filter((n) => n.endsWith('.json')).sort((a, b) => natural.compare(a, b));

  for (const nome of arquivos) {
    const d = JSON.parse(ler(path.join(DADOS, nome)));
    const alvo = disc[d.disciplina];
    if (!alvo) throw new Error(`disciplina desconhecida em ${nome}: ${d.disciplina}`);
    for (const s of d.semanas || []) {
      if (alvo.semanas[s.semana]) throw new Error(`semana ${s.semana} de ${d.disciplina} definida duas vezes (${nome})`);
      alvo.semanas[s.semana] = s;
    }
    if (d.vocabulario) {
      if (alvo.vocabulario) throw new Error(`vocabulario de ${d.disciplina} definido duas vezes (${nome})`);
      alvo.vocabulario = d.vocabulario;
    }
    for (const q of d.questoes || []) {
      if (ids.has(q.id)) throw new Error(`id repetido: ${q.id} (${nome})`);
      ids.add(q.id);
      alvo.questoes.push(q);
    }
  }

  for (const valor of Object.values(disc)) {
    valor.questoes.sort((a, b) => a.semana - b.semana || ordemOrigem(a) - ordemOrigem(b) || natural.compare(a.origem || '', b.origem || '') || natural.compare(a.id, b.id));
    valor.semanas = Object.values(valor.semanas).sort((a, b) => a.semana - b.semana);
  }

  const exs = JSON.parse(ler(path.join(AQUI, 'exemplos_visualg.json'))).questoes;
  const exemplosVisualg = exs.map(({ titulo, semana, codigo, entradas, grupo }) => ({ titulo, semana, codigo, entradas, grupo: grupo || '' }));
  const dados = { geradoEm: agoraBrasil(), inicio: INICIO, disc, exemplosVisualg };
  const jsDados = `window.NUCLEO = ${JSON.stringify(dados).replaceAll('</', '<\\/')};`;

  let html = ler(path.join(SITE, 'template.html'));
  const blocosDuvidas = html.match(/<!--duvidas-->[\s\S]*?<!--\/duvidas-->/g) || [];
  if (blocosDuvidas.length !== 3) throw new Error(`template: esperava 3 blocos <!--duvidas-->, achei ${blocosDuvidas.length}`);
  if (TIRA_DUVIDAS_NO_AR) html = html.replaceAll('<!--duvidas-->', '').replaceAll('<!--/duvidas-->', '');
  else html = html.replace(/[ \t]*<!--duvidas-->[\s\S]*?<!--\/duvidas-->[ \t]*\r?\n?/g, '');
  if (!TIRA_DUVIDAS_NO_AR && /duvidas|duv-/.test(html)) throw new Error('template: sobrou pedaço do tira-duvidas');
  const css = ler(path.join(SITE, 'styles.css')) + (TIRA_DUVIDAS_NO_AR ? '' : '\n.duv-gatilho{display:none!important}\n');
  const js = ['visualg.js', 'figura.js', 'app.js'].concat(TIRA_DUVIDAS_NO_AR ? ['duvidas.js'] : []).map((f) => ler(path.join(SITE, f))).join('\n');
  for (const [marca, conteudo] of [['/*__CSS__*/', css], ['/*__DADOS__*/', jsDados], ['/*__JS__*/', js.replaceAll('</script', '<\\/script')]]) {
    if (html.split(marca).length !== 2) throw new Error(`marcador ausente ou repetido: ${marca}`);
    // Função de substituição evita que sequências como `$$` do JavaScript
    // sejam interpretadas como padrões especiais de String.replace.
    html = html.replace(marca, () => conteudo);
  }
  fs.writeFileSync(saida, html, 'utf8');

  console.log(`gerado: ${saida} (${Math.floor(Buffer.byteLength(html) / 1024)} KB)`);
  for (const [nome, valor] of Object.entries(disc)) {
    const porSemana = {};
    for (const q of valor.questoes) {
      porSemana[q.semana] ||= [0, 0, 0];
      porSemana[q.semana][q.nivel - 1]++;
    }
    console.log(`${nome}: ${valor.questoes.length} questões`, porSemana);
  }
}

const saida = process.argv[2];
if (!saida) throw new Error('uso: node gerar.mjs <html de saída>');
main(path.resolve(saida));
