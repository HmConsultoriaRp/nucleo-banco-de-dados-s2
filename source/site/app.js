/* Núcleo · semestre 2 — lógica da página. Dados em window.NUCLEO (gerados por gerar.py). */
(function () {
  'use strict';
  var D = window.NUCLEO;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // ---------- armazenamento (falha em silêncio: a página funciona sem ele) ----------
  var CHAVE = 'nucleo-s2-v1';
  var st = { resp: {}, lentes: {}, tema: 'claro', ultimo: null, sim: {} };
  try {
    var lido = JSON.parse(localStorage.getItem(CHAVE) || 'null');
    if (lido) {
      for (var k in lido) st[k] = lido[k];
    } else {
      var antigo = JSON.parse(localStorage.getItem('nucleo-state') || 'null');
      if (antigo) {
        st.tema = antigo.theme === 'dark' ? 'escuro' : 'claro';
        st.legado = {
          migradoEm: new Date().toLocaleDateString('pt-BR'),
          atividades: Array.isArray(antigo.done) ? antigo.done.filter(function (x) { return String(x).indexOf('quiz-') !== 0; }) : [],
          marcadores: Array.isArray(antigo.bookmarks) ? antigo.bookmarks : [],
          simulados: Array.isArray(antigo.simHistory) ? antigo.simHistory : [],
          chavePreservada: true
        };
        localStorage.setItem(CHAVE, JSON.stringify(st));
      }
    }
  } catch (e) { /* sem armazenamento */ }
  function salva() { try { localStorage.setItem(CHAVE, JSON.stringify(st)); } catch (e) { /* sem armazenamento */ } }

  // ---------- texto ----------
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function md(s) {
    var codigos = [];
    var t = esc(s).replace(/`([^`]+)`/g, function (m, c) { codigos.push(c); return '\u0000' + (codigos.length - 1) + '\u0000'; });
    t = t.replace(/\[\[([^\]]+)\]\]/g, '<span class="vec">$1</span>')
      .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/\n/g, '<br>');
    return t.replace(/\u0000(\d+)\u0000/g, function (m, i) { return '<code>' + codigos[+i] + '</code>'; });
  }
  function semMarca(s) { return String(s || '').replace(/\[\[([^\]]+)\]\]/g, '$1').replace(/\*\*/g, '').replace(/`/g, ''); }
  function n2(n) { return (n < 10 ? '0' : '') + n; }
  function fmtNota(x) { return (Math.round(x * 10) / 10).toFixed(1).replace('.', ','); }

  // ---------- dados derivados ----------
  var NOME = { ga: 'Geometria', lp: 'Lógica' };
  var NOME_LONGO = { ga: 'Geometria Analítica', lp: 'Lógica de Programação' };
  var porId = {};
  ['ga', 'lp'].forEach(function (d) {
    D.disc[d].questoes.forEach(function (q) { q.disc = d; porId[q.id] = q; });
  });
  function questoesDa(d, s) { return D.disc[d].questoes.filter(function (q) { return q.semana === s; }); }
  function semanaInfo(d, s) {
    var x = D.disc[d].semanas.filter(function (w) { return w.semana === s; })[0];
    return x || { semana: s, titulo: 'Semana ' + s, chamada: 'O material desta semana ainda não chegou.', fonte: '', previa: true, blocos: [], formulas: [], jeitos: {}, lab: '' };
  }
  function semanaAtual() {
    var ini = new Date(D.inicio + 'T00:00:00');
    var dias = Math.floor((Date.now() - ini.getTime()) / 86400000);
    return Math.max(1, Math.min(6, Math.floor(dias / 7) + 1));
  }
  function rotuloCurto(q) {
    var m = /· Q(\d+[a-z]?)$/.exec(q.origem);
    if (m) return 'Q' + m[1];
    var s = q.id.split('-').pop();
    return s.toUpperCase();
  }
  function tipoOrigem(q) { return /^Avaliação/.test(q.origem) ? 'avaliacao' : (/^Lista/.test(q.origem) ? 'lista' : (/Construída/.test(q.origem) ? 'constr' : 'previa')); }

  // ---------- estado da tela ----------
  var ui = { disc: 'ga', sem: 1, view: 'questao', qid: null, filtro: 'todas', revelado: {}, dica: {}, lente: {} };
  var figuras = [];

  // ---------- progresso ----------
  function progresso() {
    var tot = 0, certas = 0, feitas = 0;
    ['ga', 'lp'].forEach(function (d) {
      D.disc[d].questoes.forEach(function (q) { tot++; var r = st.resp[q.id]; if (r) { feitas++; if (r.ok) certas++; } });
    });
    var pct = tot ? Math.round(certas / tot * 100) : 0;
    $('#progress-number').textContent = pct + '%';
    $('#progress-detail').textContent = certas + ' de ' + tot + ' certas';
    $('#progress-ring').style.strokeDashoffset = 100.5 - (100.5 * pct / 100);
    $('#chip-um').textContent = tot + ' questões · 8 jeitos cada';
  }
  function statsSemana(d, s) {
    var qs = questoesDa(d, s), f = 0, ok = 0;
    qs.forEach(function (q) { var r = st.resp[q.id]; if (r) { f++; if (r.ok) ok++; } });
    return { total: qs.length, feitas: f, certas: ok };
  }

  // ---------- hoje ----------
  function lentePreferida() {
    var melhor = null, n = 0;
    for (var k in st.lentes) if (st.lentes[k] > n) { n = st.lentes[k]; melhor = k; }
    return melhor;
  }
  var LENTES = [
    { k: 'visual', nome: 'Enxergar', ic: '◎' },
    { k: 'receita', nome: 'Passo a passo', ic: '1·2' },
    { k: 'cotidiano', nome: 'No dia a dia', ic: '≈' },
    { k: 'trabalho', nome: 'No seu trabalho', ic: 'Σ' },
    { k: 'conversa', nome: 'Conversa', ic: '“ ”' },
    { k: 'erro', nome: 'Onde se erra', ic: '!' },
  ];
  function nomeLente(k) { var l = LENTES.filter(function (x) { return x.k === k; })[0]; return l ? l.nome : k; }

  function renderHoje() {
    var s = semanaAtual();
    $('#hero-ciclo').textContent = 'Ciclo 01 · semana ' + s + ' de 6';
    var html = '';
    ['ga', 'lp'].forEach(function (d) {
      var st2 = statsSemana(d, s), info = semanaInfo(d, s);
      var falta = st2.total - st2.feitas;
      var erradas = questoesDa(d, s).filter(function (q) { return st.resp[q.id] && !st.resp[q.id].ok; }).length;
      var txt = !st2.total ? 'material ainda não chegou' : falta > 0 ? 'faltam ' + falta + ' de ' + st2.total : (erradas ? 'semana feita; refaça as ' + erradas + ' que errou' : 'semana completa');
      html += '<li><b>' + NOME[d] + '</b> <span>S' + s + ' · ' + esc(info.titulo) + (info.previa ? ' (prévia)' : '') + ': ' + txt + '.</span> <button data-ir="' + d + '|' + s + '">abrir</button></li>';
    });
    var pref = lentePreferida();
    if (pref) html += '<li><b>Seu jeito</b> <span>“' + nomeLente(pref) + '” é o que mais funcionou até agora; as explicações abrem por ele.</span></li>';
    $('#para-hoje').innerHTML = html;
    $$('#para-hoje [data-ir]').forEach(function (b) {
      b.addEventListener('click', function () {
        var p = b.dataset.ir.split('|');
        abrirSemana(p[0], +p[1], 'questao', primeiraPendente(p[0], +p[1]));
      });
    });
  }
  function primeiraPendente(d, s) {
    var qs = questoesDa(d, s);
    for (var i = 0; i < qs.length; i++) if (!st.resp[qs[i].id]) return qs[i].id;
    return qs.length ? qs[0].id : null;
  }

  function renderTrilha() {
    var s = semanaAtual(), html = '';
    for (var w = 1; w <= 6; w++) {
      var a = statsSemana('ga', w), b = statsSemana('lp', w);
      var done = a.total + b.total > 0 && a.feitas + b.feitas === a.total + b.total;
      html += '<button class="' + (w === s ? 'now' : '') + (done ? ' done' : '') + '" data-sem="' + w + '" aria-label="Semana ' + w + '"><i>' + w + '</i>' + (w === s ? '<small>agora</small>' : '') + '</button>';
    }
    $('#week-line').innerHTML = html;
    $$('#week-line button').forEach(function (b) { b.addEventListener('click', function () { abrirSemana(ui.disc, +b.dataset.sem, 'conceito'); }); });
    var g = '';
    for (var x = 1; x <= 6; x++) {
      var A = semanaInfo('ga', x), B = semanaInfo('lp', x);
      g += '<article><b>' + n2(x) + '</b><span>Geometria</span><strong>' + esc(A.titulo) + '</strong>' + (A.previa ? '<em>PRÉVIA</em>' : '') + '<span>Lógica</span><strong>' + esc(B.titulo) + '</strong>' + (B.previa ? '<em>PRÉVIA</em>' : '') + '</article>';
    }
    $('#planner-grid').innerHTML = g;
  }

  // ---------- sala de estudo ----------
  function abrirSemana(d, s, view, qid) {
    ui.disc = d; ui.sem = s; ui.view = view || ui.view;
    if (qid) ui.qid = qid;
    else if (!ui.qid || !porId[ui.qid] || porId[ui.qid].disc !== d || porId[ui.qid].semana !== s) ui.qid = primeiraPendente(d, s);
    renderEstudo();
    var alvo = $('#estudo');
    if (alvo.getBoundingClientRect().top > 120 || alvo.getBoundingClientRect().bottom < 200) alvo.scrollIntoView();
  }
  function renderEstudo() {
    document.body.dataset.subject = ui.disc;
    $$('[data-subject]').forEach(function (b) { if (b.tagName === 'BUTTON') b.classList.toggle('active', b.dataset.subject === ui.disc); });
    var tabs = '';
    for (var w = 1; w <= 6; w++) {
      var info = semanaInfo(ui.disc, w), stt = statsSemana(ui.disc, w);
      tabs += '<button role="tab" class="' + (w === ui.sem ? 'active' : '') + (info.previa ? ' previa' : '') + '" data-week="' + w + '"><span>Semana</span>' + n2(w) +
        '<small>' + esc(info.titulo) + '</small><em>' + (info.previa ? 'prévia · ' : '') + stt.feitas + '/' + stt.total + '</em>' +
        '<span class="week-bar"><i style="width:' + (stt.total ? Math.round(stt.feitas / stt.total * 100) : 0) + '%"></i></span></button>';
    }
    $('#week-tabs').innerHTML = tabs;
    $$('#week-tabs button').forEach(function (b) { b.addEventListener('click', function () { ui.qid = null; abrirSemana(ui.disc, +b.dataset.week); }); });
    $$('.view-link').forEach(function (b) { b.classList.toggle('active', b.dataset.view === ui.view); });
    $('#qcount').textContent = questoesDa(ui.disc, ui.sem).length;
    var info2 = semanaInfo(ui.disc, ui.sem);
    $('#index-note').innerHTML = info2.previa
      ? '<strong>Prévia</strong><p>Montado pela ementa do PPC. Quando o material do professor chegar, esta semana muda.</p>'
      : '<strong>Fonte</strong><p>' + esc(info2.fonte) + '. Gabarito refeito conta por conta antes de entrar aqui.</p>';
    renderLista();
    $$('.view').forEach(function (v) {
      var on = v.id === 'view-' + ui.view;
      v.classList.toggle('on', on);
      if (!on) v.innerHTML = '';
    });
    figuras = [];
    if (ui.view === 'conceito') renderConceito();
    else if (ui.view === 'lab') renderLab();
    else if (ui.view === 'atividades') renderAtividades();
    else renderQuestao();
  }
  function renderLista() {
    var qs = questoesDa(ui.disc, ui.sem).filter(function (q) {
      var r = st.resp[q.id];
      if (ui.filtro === 'pendentes') return !r;
      if (ui.filtro === 'erradas') return r && !r.ok;
      return true;
    });
    var html = '', grupo = '';
    qs.forEach(function (q) {
      var tipo = tipoOrigem(q);
      var g = tipo === 'avaliacao' ? q.origem.split(' · Q')[0] : (tipo === 'lista' ? q.origem.split(' · ')[0] : (tipo === 'constr' ? 'Construídas' : 'Prévia pela ementa'));
      if (g !== grupo) { html += '<h5>' + esc(g) + '</h5>'; grupo = g; }
      var r = st.resp[q.id];
      html += '<button class="qitem' + (q.id === ui.qid && ui.view === 'questao' ? ' active' : '') + '" data-q="' + q.id + '" title="' + esc(q.tema) + '">' +
        '<span class="st ' + (r ? (r.ok ? 'ok' : 'bad') : '') + '">' + (r ? (r.ok ? '✓' : '✗') : '') + '</span>' +
        '<span class="tt"><b>' + esc(rotuloCurto(q)) + '</b><span class="tema"> · ' + esc(q.tema) + '</span></span><small class="min">' + '●'.repeat(q.nivel) + '</small></button>';
    });
    if (!qs.length) html = '<p style="font-size:12px;color:var(--muted);padding:8px">' + (ui.filtro === 'erradas' ? 'Nenhuma questão errada nesta semana.' : ui.filtro === 'pendentes' ? 'Você já respondeu todas desta semana.' : 'Sem questões ainda.') + '</p>';
    $('#qlist').innerHTML = html;
    $$('#qlist .qitem').forEach(function (b) {
      b.addEventListener('click', function () { ui.qid = b.dataset.q; ui.view = 'questao'; renderEstudo(); });
    });
    $$('.qfilter button').forEach(function (b) { b.classList.toggle('active', b.dataset.filtro === ui.filtro); });
  }

  // ---------- atividades da faculdade ----------
  function renderAtividades() {
    var el = $('#view-atividades');
    var info = semanaInfo(ui.disc, ui.sem);
    var qs = questoesDa(ui.disc, ui.sem);
    var avaliacoes = qs.filter(function (q) { return tipoOrigem(q) === 'avaliacao'; });
    var oficiais = qs.filter(function (q) { return tipoOrigem(q) === 'lista'; });
    var construidas = qs.filter(function (q) { return tipoOrigem(q) === 'constr'; });
    var previas = qs.filter(function (q) { return tipoOrigem(q) === 'previa'; });
    var legado = st.legado;
    var h = '<div class="activity-hub"><header class="activity-head"><div><p class="lesson-kicker">' + esc(NOME_LONGO[ui.disc]) + ' · semana ' + n2(ui.sem) + '</p>' +
      '<h2>Atividades da faculdade</h2><p>O print chega, nós resolvemos juntos e a atividade entra aqui com resposta, armadilhas e diferentes caminhos de explicação.</p></div>' +
      '<span class="activity-count">' + qs.length + '<small>questões</small></span></header>';
    h += '<div class="activity-flow"><article><b>01</b><strong>Enunciado original</strong><span>Transcrito do print sem mudar o que foi pedido.</span></article>' +
      '<article><b>02</b><strong>Ideia central</strong><span>O que a questão realmente quer avaliar.</span></article>' +
      '<article><b>03</b><strong>Resolução comentada</strong><span>Conta, raciocínio e conferência passo a passo.</span></article>' +
      '<article><b>04</b><strong>Outros jeitos</strong><span>Visual, cotidiano, receita, conversa e erros comuns.</span></article></div>';
    if (legado) {
      h += '<div class="migration-note"><strong>Progresso anterior preservado</strong><p>' + legado.atividades.length + ' registros de atividade, ' + legado.marcadores.length + ' marcadores e ' + legado.simulados.length + ' simulados foram guardados. As novas questões começam limpas porque o banco mudou; o armazenamento antigo não foi apagado.</p></div>';
    }
    h += '<div class="activity-source"><div><span>Fonte desta semana</span><strong>' + esc(info.previa ? 'Prévia baseada na ementa' : (info.fonte || 'Material da disciplina')) + '</strong></div>' +
      '<ul><li><b>' + avaliacoes.length + '</b> da avaliação</li><li><b>' + oficiais.length + '</b> da lista recebida</li><li><b>' + construidas.length + '</b> de reforço</li><li><b>' + previas.length + '</b> de prévia</li></ul></div>';
    if (!qs.length) {
      h += '<div class="activity-empty"><b>Pronto para o próximo print.</b><p>Quando a atividade chegar, ela será incorporada ao banco desta disciplina e semana.</p></div>';
    } else {
      h += '<div class="activity-list"><div class="activity-list-head"><h3>Caderno da semana</h3><p>Abra qualquer item para responder e ver todos os caminhos de explicação.</p></div>';
      qs.forEach(function (q, i) {
        var r = st.resp[q.id];
        var tipo = tipoOrigem(q);
        h += '<button class="activity-item" data-activity-q="' + esc(q.id) + '"><span class="activity-number">' + n2(i + 1) + '</span><span><small>' + esc(tipo === 'avaliacao' ? q.origem : tipo === 'lista' ? q.origem : tipo === 'constr' ? 'Questão de reforço' : 'Prévia pela ementa') + '</small><strong>' + esc(q.tema) + '</strong><em>' + (r ? (r.ok ? 'respondida corretamente' : 'refazer') : 'ainda não feita') + '</em></span><i>' + (r ? (r.ok ? '✓' : '↺') : '→') + '</i></button>';
      });
      h += '</div>';
    }
    h += '<div class="activity-next"><div><strong>Vai enviar uma nova atividade?</strong><p>Mande o print na conversa. Ela entra na disciplina e na semana corretas depois que conferirmos juntos.</p></div><button class="primary-button" data-first-activity>Começar pelas questões <span>→</span></button></div></div>';
    el.innerHTML = h;
    $$('[data-activity-q]', el).forEach(function (b) {
      b.addEventListener('click', function () { ui.qid = b.dataset.activityQ; ui.view = 'questao'; renderEstudo(); });
    });
    var primeiro = $('[data-first-activity]', el);
    if (primeiro) primeiro.addEventListener('click', function () { ui.qid = primeiraPendente(ui.disc, ui.sem); ui.view = 'questao'; renderEstudo(); });
  }

  // ---------- figura, tabela, código ----------
  var figReg = [];
  function htmlFigura(fig) {
    figReg.push(fig);
    var i = figReg.length - 1;
    return '<figure class="fig"><canvas data-fig="' + i + '" aria-label="Figura"></canvas><figcaption>' + (fig.legenda ? md(fig.legenda) : '') +
      (fig.modo !== '2d' ? ' <span>Arraste para girar.</span><span class="vistas"><button data-vista="padrao">3D</button><button data-vista="frente">frente</button><button data-vista="cima">de cima</button></span>' : '') + '</figcaption></figure>';
  }
  function montaFiguras(raiz) {
    $$('canvas[data-fig]', raiz).forEach(function (c) {
      var f = Figura.montar(c, figReg[+c.dataset.fig]);
      figuras.push(f);
      var cap = c.parentNode.querySelector('.vistas');
      if (cap) $$('button', cap).forEach(function (b) { b.addEventListener('click', function () { f.vista(b.dataset.vista); }); });
    });
  }
  function htmlTabela(t) {
    var h = '<div class="tw"><table class="tv"><thead><tr>' + t.cab.map(function (c) { return '<th>' + md(c) + '</th>'; }).join('') + '</tr></thead><tbody>';
    t.linhas.forEach(function (l) {
      h += '<tr>' + l.map(function (c) { var s = String(c); return '<td class="' + (s === 'V' ? 'v' : s === 'F' ? 'f' : '') + '">' + md(s) + '</td>'; }).join('') + '</tr>';
    });
    return h + '</tbody></table></div>';
  }
  var KWVA = /^(algoritmo|var|inicio|início|fimalgoritmo|inteiro|real|caractere|caracter|logico|lógico|vetor|de|leia|escreva|escreval|se|entao|então|senao|senão|fimse|escolha|caso|outrocaso|fimescolha|para|ate|até|passo|faca|faça|fimpara|enquanto|fimenquanto|repita|fimrepita|interrompa|e|ou|nao|não|xou|div|mod|verdadeiro|falso)$/i;
  function realce(linha) {
    var out = '', i = 0;
    var com = linha.indexOf('//');
    var cod = com >= 0 ? linha.slice(0, com) : linha, cm = com >= 0 ? linha.slice(com) : '';
    var re = /("[^"]*")|(\d+(?:\.\d+)?)|([A-Za-zÀ-ÿ_][A-Za-zÀ-ÿ0-9_]*)|([^"\dA-Za-zÀ-ÿ_]+)/g, m;
    while ((m = re.exec(cod))) {
      if (m[1]) out += '<span class="st">' + esc(m[1]) + '</span>';
      else if (m[2]) out += '<span class="nu">' + esc(m[2]) + '</span>';
      else if (m[3]) out += KWVA.test(m[3]) ? '<span class="kw">' + esc(m[3]) + '</span>' : esc(m[3]);
      else out += esc(m[4]);
    }
    if (cm) out += '<span class="cm">' + esc(cm) + '</span>';
    return out;
  }
  function htmlCodigo(codigo, atual) {
    return '<pre class="code">' + codigo.split('\n').map(function (l, i) {
      return '<span class="ln' + (atual === i + 1 ? ' cur' : '') + '" data-l="' + (i + 1) + '"><i>' + (i + 1) + '</i>' + realce(l) + '</span>';
    }).join('') + '</pre>';
  }

  // ---------- teste de mesa ----------
  function mesa(host, codigo, entradas, titulo) {
    var res = VisuAlg.executar(codigo, entradas || []);
    var passos = res.passos, i = 0, play = null, cheia = false;
    function render() {
      var p = passos[i] || { linha: 0, nota: '', vars: {}, saida: '' };
      var ant = passos[i - 1];
      var fim = i === passos.length - 1;
      var linhasVars = res.nomes.map(function (n) {
        var mud = ant && ant.vars[n] !== p.vars[n];
        return '<tr class="' + (mud ? 'mud' : '') + '"><td>' + esc(n) + '</td><td>' + esc(p.vars[n]) + '</td></tr>';
      }).join('');
      var erro = res.erro && (fim || !passos.length) ? '<span class="err">Erro' + (res.erro.linha ? ' na linha ' + res.erro.linha : '') + ': ' + esc(res.erro.msg) + '</span>' : '';
      var tabela = '';
      if (cheia) {
        tabela = '<div class="mesa-full"><table><thead><tr><th>#</th><th>linha</th><th>o que aconteceu</th>' + res.nomes.map(function (n) { return '<th>' + esc(n) + '</th>'; }).join('') + '</tr></thead><tbody>' +
          passos.map(function (q, k) {
            return '<tr class="' + (k === i ? 'cur' : '') + '" data-k="' + k + '"><td>' + (k + 1) + '</td><td>' + q.linha + '</td><td>' + esc(q.nota) + '</td>' + res.nomes.map(function (n) { return '<td>' + esc(q.vars[n]) + '</td>'; }).join('') + '</tr>';
          }).join('') + '</tbody></table></div>';
      }
      host.innerHTML = '<div class="mesa"><div class="mesa-top"><strong>' + esc(titulo || 'Teste de mesa') + '</strong>' +
        (entradas && entradas.length ? '<span style="font-size:11.5px;color:var(--muted)">entradas: ' + esc(entradas.join(', ')) + '</span>' : '') +
        '<div class="ctl"><button data-a="ini" title="início">⏮</button><button data-a="ant" title="passo anterior">◀</button><span>passo ' + (passos.length ? i + 1 : 0) + ' de ' + passos.length + '</span><button data-a="prox" title="próximo passo">▶</button><button data-a="fim" title="fim">⏭</button><button data-a="play" title="tocar sozinho">' + (play ? '❚❚' : '▶▶') + '</button><button data-a="tab" title="tabela completa">' + (cheia ? 'menos' : 'tabela') + '</button></div></div>' +
        '<div class="mesa-body">' + htmlCodigo(codigo, p.linha) + '<div class="mesa-state"><div class="nota">' + (passos.length ? 'Linha ' + p.linha + ': ' + esc(p.nota) : 'O programa não chegou a rodar.') + '</div>' +
        '<table class="mesa-vars">' + linhasVars + '</table><div class="console">' + esc(p.saida || '') + erro + (p.saida || erro ? '' : '<span style="opacity:.5">tela vazia</span>') + '</div></div></div>' + tabela + '</div>';
      $$('.ctl button', host).forEach(function (b) {
        b.addEventListener('click', function () {
          var a = b.dataset.a;
          if (a === 'ini') i = 0;
          else if (a === 'ant') i = Math.max(0, i - 1);
          else if (a === 'prox') i = Math.min(passos.length - 1, i + 1);
          else if (a === 'fim') i = passos.length - 1;
          else if (a === 'tab') cheia = !cheia;
          else if (a === 'play') {
            if (play) { clearInterval(play); play = null; }
            else {
              if (i >= passos.length - 1) i = 0;
              play = setInterval(function () {
                if (!host.isConnected || i >= passos.length - 1) { clearInterval(play); play = null; if (host.isConnected) render(); return; }
                i++; render();
              }, 650);
            }
          }
          render();
        });
      });
      $$('.mesa-full tr[data-k]', host).forEach(function (tr) { tr.addEventListener('click', function () { i = +tr.dataset.k; render(); }); });
    }
    render();
    return res;
  }

  // ---------- lentes ----------
  function corpoLente(k, jeitos, extra) {
    var v = jeitos[k];
    if (k === 'receita' && Array.isArray(v)) return '<ol>' + v.map(function (p) { return '<li>' + md(p) + '</li>'; }).join('') + '</ol>';
    if (k === 'conversa' && Array.isArray(v)) {
      return '<div class="conversa">' + v.map(function (f) {
        var voce = f.quem === 'Você';
        return '<div class="fala ' + (voce ? 'voce' : 'monitor') + '"><b>' + (voce ? 'Você' : 'Monitor') + '</b>' + md(f.fala) + '</div>';
      }).join('') + '</div>';
    }
    var h = '<p>' + md(v || '') + '</p>';
    if (k === 'visual' && extra) h += extra;
    return h;
  }
  function lentes(host, jeitos, opts) {
    opts = opts || {};
    var disp = LENTES.filter(function (l) { return jeitos[l.k] && (!Array.isArray(jeitos[l.k]) || jeitos[l.k].length); });
    var pref = lentePreferida();
    var chave = opts.chave || 'x';
    var atual = ui.lente[chave] || (pref && jeitos[pref] ? pref : disp[0].k);
    function render() {
      ui.lente[chave] = atual;
      figReg = figReg || [];
      var l = disp.filter(function (x) { return x.k === atual; })[0] || disp[0];
      var extra = atual === 'visual' ? (opts.extraVisual ? opts.extraVisual() : '') : '';
      host.innerHTML = '<div class="lens-tabs" role="tablist">' + disp.map(function (x) {
        return '<button role="tab" class="' + (x.k === atual ? 'active' : '') + (x.k === pref ? ' pref' : '') + '" data-l="' + x.k + '"><i>' + x.ic + '</i>' + x.nome + '</button>';
      }).join('') + '</div>' +
        '<div class="lens-panel"><div class="lens-icon">' + l.ic + '</div><div class="lens-body"><span class="lens-label">' + l.nome + '</span>' + corpoLente(atual, jeitos, extra) + '</div></div>' +
        (opts.questao ? '<div class="lens-foot"><button class="ghost" data-acao="funcionou">Esse jeito funcionou</button><button class="ghost" data-acao="outro">Ainda não entendi → outro jeito</button><small id="lens-msg"></small></div>' : '');
      $$('.lens-tabs button', host).forEach(function (b) { b.addEventListener('click', function () { atual = b.dataset.l; render(); }); });
      var fb = $('[data-acao="funcionou"]', host), ob = $('[data-acao="outro"]', host);
      if (fb) fb.addEventListener('click', function () {
        st.lentes[atual] = (st.lentes[atual] || 0) + 1; salva();
        fb.classList.add('on'); fb.textContent = 'Anotado: ' + l.nome;
        $('#lens-msg', host).textContent = 'As próximas explicações abrem pelo jeito que mais funcionou para você.';
        renderHoje();
      });
      if (ob) ob.addEventListener('click', function () {
        var idx = disp.map(function (x) { return x.k; }).indexOf(atual);
        atual = disp[(idx + 1) % disp.length].k; render();
      });
      montaFiguras(host);
      if (opts.depois) opts.depois(host);
    }
    render();
  }

  // ---------- conceito ----------
  function renderConceito() {
    figReg = [];
    var w = semanaInfo(ui.disc, ui.sem);
    var h = '<header class="lesson-header"><div><p class="lesson-kicker">' + NOME[ui.disc] + ' · Semana ' + n2(ui.sem) + '</p><h2>' + esc(w.titulo) + '</h2><p class="chamada">' + md(w.chamada) + '</p>' +
      (w.previa ? '<p class="fonte"><span class="stamp">prévia</span> ' + esc(w.fonte) + '</p>' : (w.fonte ? '<p class="fonte">Fonte: ' + esc(w.fonte) + '</p>' : '')) + '</div></header>';
    if (w.ideias && w.ideias.length) {
      h += '<section class="ideias"><div class="ideias-head"><h3>Ideias da semana</h3><p>Cada cartão abre um painel com a figura que gira e a conta em passos, com um exemplo da lista do professor.</p></div><div class="ideias-grid">' +
        w.ideias.map(function (it, i) {
          var meta = it.esboco ? '<span class="stamp">em preparo</span>' : '<span class="ideia-meta">' + it.passos.length + ' passos · figura que gira · ' + esc(it.fonte) + '</span>';
          return '<button class="ideia-card' + (it.esboco ? ' esboco' : '') + '" data-ideia="' + i + '"' + (it.esboco ? ' disabled' : '') + '><span class="ideia-num">' + n2(i + 1) + '</span><b>' + esc(it.titulo) + '</b><span class="ideia-frase">' + md(it.frase) + '</span>' + meta + '</button>';
        }).join('') + '</div></section>';
    } else if (w.blocos && w.blocos.length) {
      h += '<div class="blocos">' + w.blocos.map(function (b, i) { return '<div class="bloco"><h4><span>' + n2(i + 1) + '</span>' + esc(b.titulo) + '</h4><p>' + md(b.texto) + '</p></div>'; }).join('') + '</div>';
    }
    if (w.formulas && w.formulas.length) {
      h += '<div class="formulas"><h3>O que usar e quando</h3><table class="ftable">' + w.formulas.map(function (f) { return '<tr><td>' + md(f.nome) + '</td><td>' + md(f.expr) + '</td><td>' + md(f.quando) + '</td></tr>'; }).join('') + '</table></div>';
    }
    var nj = w.jeitos ? LENTES.filter(function (l) { return w.jeitos[l.k]; }).length : 0;
    var extenso = ['', 'Um jeito', 'Dois jeitos', 'Três jeitos', 'Quatro jeitos', 'Cinco jeitos', 'Seis jeitos'][nj] || nj + ' jeitos';
    if (nj) h += '<div class="jeitos-semana"><h3>' + extenso + ' de entender a ideia da semana</h3><div id="lentes-semana"></div></div>';
    h += '<div class="lab-chamada"><p><b>Laboratório.</b> ' + md(w.lab || 'Mexa nos valores e veja o resultado mudar na hora.') + '</p><button class="primary-button" data-view-go="lab">Abrir laboratório <span>→</span></button></div>';
    var qs = questoesDa(ui.disc, ui.sem);
    if (qs.length) h += '<div class="lab-chamada" style="border-left-color:var(--yellow)"><p><b>' + qs.length + ' questões</b> nesta semana, cada uma com oito jeitos de explicar.</p><button class="primary-button" data-view-go="questao">Ir para as questões <span>→</span></button></div>';
    var el = $('#view-conceito');
    el.innerHTML = h;
    if (nj) lentes($('#lentes-semana'), w.jeitos, { chave: 'sem-' + ui.disc + ui.sem });
    $$('[data-view-go]', el).forEach(function (b) { b.addEventListener('click', function () { ui.view = b.dataset.viewGo; renderEstudo(); }); });
    $$('[data-ideia]', el).forEach(function (b) { b.addEventListener('click', function () { abrirIdeia(w, +b.dataset.ideia); }); });
  }

  // ---------- ideia: painel com figura e passos ----------
  function abrirIdeia(w, idx) {
    var it = w.ideias[idx];
    if (!it || it.esboco) return;
    var dlg = $('#ideia-dialog'), corpo = $('#ideia-corpo');
    var passo = 0, fig = null;
    var total = w.ideias.length;
    corpo.innerHTML =
      '<p class="lesson-kicker">' + NOME[ui.disc] + ' · Semana ' + n2(ui.sem) + ' · Ideia ' + (idx + 1) + ' de ' + total + '</p>' +
      '<h2 id="ideia-titulo">' + esc(it.titulo) + '</h2><p class="ideia-frase-grande">' + md(it.frase) + '</p>' +
      '<div class="ideia-fig"><canvas id="ideia-cv" aria-label="Figura da ideia; arraste para girar"></canvas>' +
      '<span class="vistas"><button data-vista="padrao">3D</button><button data-vista="frente">frente</button><button data-vista="cima">de cima</button></span>' +
      '<span class="ideia-dica">arraste para girar</span></div>' +
      '<div class="ideia-passo" aria-live="polite"><div id="ideia-passo-corpo"></div>' +
      '<div class="ideia-nav"><button class="ghost" id="ideia-ant">← Anterior</button><span id="ideia-pos"></span><button class="primary-button" id="ideia-prox">Próximo <span>→</span></button></div></div>' +
      '<div class="ideia-lista"><p>Na lista do professor</p><div>' + (it.questoes || []).filter(function (id) { return porId[id]; }).map(function (id) {
        return '<button class="chip" data-ir-questao="' + id + '">' + esc(porId[id].origem) + '</button>';
      }).join('') + '</div></div>';
    function mostra() {
      var p = it.passos[passo];
      $('#ideia-passo-corpo').innerHTML = '<h4><span>' + (passo + 1) + '</span>' + esc(p.titulo) + '</h4><p>' + md(p.texto) + '</p>' +
        (p.destaque ? '<div class="ideia-destaque"><strong>' + esc(p.destaque.valor) + '</strong><small>' + esc(p.destaque.rotulo) + '</small></div>' : '');
      $('#ideia-pos').textContent = 'Passo ' + (passo + 1) + ' de ' + it.passos.length;
      $('#ideia-ant').disabled = passo === 0;
      var ultimo = passo === it.passos.length - 1;
      $('#ideia-prox').innerHTML = ultimo ? 'Concluir <span>✓</span>' : 'Próximo <span>→</span>';
      if (fig) fig.trocar(p.fig); else fig = Figura.montar($('#ideia-cv'), p.fig);
    }
    $('#ideia-ant').addEventListener('click', function () { if (passo > 0) { passo--; mostra(); } });
    $('#ideia-prox').addEventListener('click', function () {
      if (passo < it.passos.length - 1) { passo++; mostra(); } else dlg.close();
    });
    $$('[data-vista]', corpo).forEach(function (b) { b.addEventListener('click', function () { if (fig) fig.vista(b.dataset.vista); }); });
    $$('[data-ir-questao]', corpo).forEach(function (b) {
      b.addEventListener('click', function () { var q = porId[b.dataset.irQuestao]; dlg.close(); abrirSemana(q.disc, q.semana, 'questao', q.id); });
    });
    dlg.showModal();
    mostra();
    var redesenha = function () { if (fig) fig.redesenhar(); };
    window.addEventListener('resize', redesenha);
    dlg.addEventListener('close', function () { window.removeEventListener('resize', redesenha); }, { once: true });
  }

  // ---------- questão ----------
  function renderQuestao() {
    figReg = [];
    var el = $('#view-questao');
    var qs = questoesDa(ui.disc, ui.sem);
    if (!qs.length) { el.innerHTML = '<div class="vazio">Ainda não há questões nesta semana.</div>'; return; }
    var q = porId[ui.qid];
    if (!q || q.disc !== ui.disc || q.semana !== ui.sem) { q = qs[0]; ui.qid = q.id; }
    st.ultimo = { disc: ui.disc, sem: ui.sem, id: q.id }; salva();
    var pos = qs.indexOf(q);
    var r = st.resp[q.id];
    var aberto = !!r || ui.revelado[q.id];
    var to = tipoOrigem(q);
    var h = '<div class="qview"><div class="q-head"><span class="q-origem ' + (to === 'previa' ? 'previa' : to === 'constr' ? 'constr' : to === 'avaliacao' ? 'avaliacao' : '') + '">' + esc(q.origem) + '</span>' +
      '<span class="q-tema">' + esc(q.tema) + '</span><span class="q-nivel" title="nível ' + q.nivel + ' de 3">' + [1, 2, 3].map(function (n) { return '<i class="' + (n <= q.nivel ? 'f' : '') + '"></i>'; }).join('') + ' ' + ['', 'básico', 'médio', 'avançado'][q.nivel] + ' · ' + q.minutos + ' min</span>' +
      '<span class="q-nav"><button data-nav="-1" aria-label="Questão anterior">←</button><span>' + (pos + 1) + ' de ' + qs.length + '</span><button data-nav="1" aria-label="Próxima questão">→</button></span></div>';
    h += '<p class="q-enunciado">' + md(q.enunciado) + '</p>';
    if (q.codigo) {
      h += htmlCodigo(q.codigo);
      if (q.entradas && q.entradas.length) h += '<p class="entradas-chip">Valores digitados quando o programa pede (leia), na ordem: ' + q.entradas.map(function (x) { return '<code>' + esc(x) + '</code>'; }).join(' ') + '</p>';
    }
    if (q.figura && q.figura.onde === 'enunciado') h += htmlFigura(q.figura);
    if (q.tabela && q.tabela.onde === 'enunciado') h += htmlTabela(q.tabela);
    h += '<div class="alts' + (r ? ' done' : '') + '" role="group" aria-label="Alternativas">' + q.alternativas.map(function (a, i) {
      var cls = '';
      if (r) { if (a.certa) cls = 'ok'; else if (r.e === i) cls = 'bad'; }
      return '<button class="alt ' + cls + '" data-alt="' + i + '"' + (r ? ' disabled' : '') + '><span class="l">' + 'ABCDE'[i] + '</span><span>' + md(a.t) + '</span><span class="m"></span></button>';
    }).join('') + '</div>';
    h += '<div class="q-actions">' + (!r ? '<button class="ghost" data-acao="dica">Uma dica</button>' : '') +
      (!aberto ? '<button class="ghost" data-acao="revelar">Ver explicação sem responder</button>' : '') +
      (r ? '<button class="ghost" data-acao="refazer">Refazer esta questão</button>' : '') +
      (r || aberto ? '<button class="ghost" data-nav="1">Próxima questão →</button>' : '') + '</div>';
    if (ui.dica[q.id] && !r) h += '<div class="dica"><strong>Dica</strong>' + md(q.dica) + '</div>';
    if (r) {
      var certa = q.alternativas.filter(function (a) { return a.certa; })[0];
      if (r.ok) h += '<div class="feedback"><strong>Isso: ' + 'ABCDE'[r.e] + '.</strong>' + md(q.resposta) + '</div>';
      else h += '<div class="feedback bad"><strong>Não é ' + 'ABCDE'[r.e] + '. A certa é ' + 'ABCDE'[q.alternativas.indexOf(certa)] + '.</strong>' + md(q.alternativas[r.e].erro || '') + '</div>';
    }
    if (aberto) {
      h += '<section class="jeitos"><div class="jeitos-head"><h3>Jeitos de entender</h3><p>Cada aba é um caminho diferente para a mesma resposta. Se um não encaixar, tente outro.</p></div>';
      if (q.codigo) h += '<div id="mesa-q"></div>';
      h += '<div id="lentes-q"></div>';
      if (q.ouro) h += '<aside class="ouro"><span>Dicas que valem ouro</span>' + md(q.ouro) + '</aside>';
      h += '<div class="strips"><div class="strip prova"><strong>Tire a prova</strong>' + md(q.jeitos.confira) + '</div><div class="strip atalho"><strong>Atalho de prova</strong>' + md(q.jeitos.atalho) + '</div></div>';
      h += '<details class="outras"' + (r && !r.ok ? ' open' : '') + '><summary>Por que as outras alternativas estão erradas</summary><ul>' + q.alternativas.map(function (a, i) {
        return a.certa ? '' : '<li><b>' + 'ABCDE'[i] + ') ' + md(a.t) + '</b> · ' + md(a.erro) + '</li>';
      }).join('') + '</ul></details></section>';
    }
    h += '</div>';
    el.innerHTML = h;
    montaFiguras(el);
    if (aberto) {
      if (q.codigo) mesa($('#mesa-q'), q.codigo, q.entradas, 'O programa rodando, linha a linha');
      var extra = function () {
        var x = '';
        if (q.figura && q.figura.onde !== 'enunciado') x += htmlFigura(q.figura);
        if (q.tabela && q.tabela.onde !== 'enunciado') x += htmlTabela(q.tabela);
        return x;
      };
      lentes($('#lentes-q'), q.jeitos, { questao: true, chave: q.id, extraVisual: extra });
    }
    $$('[data-alt]', el).forEach(function (b) { b.addEventListener('click', function () { responder(q, +b.dataset.alt); }); });
    $$('[data-nav]', el).forEach(function (b) { b.addEventListener('click', function () { navegar(+b.dataset.nav); }); });
    var bd = $('[data-acao="dica"]', el); if (bd) bd.addEventListener('click', function () { ui.dica[q.id] = true; renderQuestao(); });
    var br = $('[data-acao="revelar"]', el); if (br) br.addEventListener('click', function () { ui.revelado[q.id] = true; renderQuestao(); });
    var bf = $('[data-acao="refazer"]', el); if (bf) bf.addEventListener('click', function () { delete st.resp[q.id]; delete ui.revelado[q.id]; salva(); atualizaTudo(); });
  }
  function responder(q, i) {
    if (st.resp[q.id]) return;
    st.resp[q.id] = { e: i, ok: !!q.alternativas[i].certa };
    salva();
    atualizaTudo();
  }
  function navegar(dir) {
    var qs = questoesDa(ui.disc, ui.sem), i = qs.map(function (x) { return x.id; }).indexOf(ui.qid);
    var j = i + dir;
    if (j < 0 || j >= qs.length) {
      var s2 = ui.sem + dir;
      if (s2 >= 1 && s2 <= 6 && questoesDa(ui.disc, s2).length) {
        var q2 = questoesDa(ui.disc, s2);
        abrirSemana(ui.disc, s2, 'questao', dir > 0 ? q2[0].id : q2[q2.length - 1].id);
      }
      return;
    }
    ui.qid = qs[j].id;
    renderEstudo();
    var v = $('#view-questao'); if (v.getBoundingClientRect().top < 0) v.scrollIntoView();
  }
  function atualizaTudo() { progresso(); renderHoje(); renderTrilha(); renderEstudo(); }

  // ---------- laboratórios ----------
  var labGA = { u: [3, 1, 2], v: [1, 3, -1], w: [1, 1, 3], k: 2, op: null };
  var labCon = { tipo: 'elipse', a: 5, b: 3, p: 2 };
  var labBits = { n: 45 };
  var labTV = { e1: '¬(p ∧ q)', e2: '¬p ∨ ¬q' };
  var labVA = null;
  var EX_VA = window.NUCLEO.exemplosVisualg || [];

  function renderLab() {
    figReg = [];
    var el = $('#view-lab');
    var w = semanaInfo(ui.disc, ui.sem);
    var tipo;
    if (ui.disc === 'ga') tipo = ui.sem === 6 ? 'conicas' : 'vetores';
    else tipo = ui.sem <= 2 ? 'bits' : ui.sem <= 4 ? 'verdade' : 'visualg';
    var head = '<div class="lab-head"><div><p class="lesson-kicker">' + NOME[ui.disc] + ' · Semana ' + n2(ui.sem) + ' · Laboratório</p><h3>' +
      { vetores: 'Vetores que respondem', conicas: 'Cônicas sob controle', bits: 'Interruptores de bits', verdade: 'Fábrica de tabela-verdade', visualg: 'VisuAlg no navegador' }[tipo] +
      '</h3></div><p>' + md(w.lab || '') + '</p></div>';
    el.innerHTML = '<div class="lab">' + head + '<div id="lab-corpo"></div></div>';
    ({ vetores: labVetores, conicas: labConicas, bits: labBitsR, verdade: labVerdade, visualg: labVisualg })[tipo]($('#lab-corpo'));
  }

  // --- vetores ---
  function vsoma(a, b) { return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]; }
  function vsub(a, b) { return [a[0] - b[0], a[1] - b[1], a[2] - b[2]]; }
  function vmul(k, a) { return [k * a[0], k * a[1], k * a[2]]; }
  function vdot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function vcross(a, b) { return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]; }
  function vnorm(a) { return Math.sqrt(vdot(a, a)); }
  function fn(x) {
    if (Math.abs(x) < 1e-9) x = 0;
    var r = Math.round(x * 1000) / 1000;
    var s = String(r);
    return s.replace('-', '−').replace('.', ',');
  }
  function fv(a) {
    var inteiros = a.every(function (x) { return Math.abs(x - Math.round(x)) < 1e-9; });
    return '(' + a.map(fn).join(inteiros ? ', ' : '; ') + ')';
  }
  function raizTxt(q) {
    if (Math.abs(q - Math.round(q)) > 1e-9) return fn(Math.sqrt(q));
    q = Math.round(q);
    var r = Math.sqrt(q);
    if (Number.isInteger(r)) return String(r);
    var fora = 1, dentro = q;
    for (var f = 2; f * f <= dentro; f++) while (dentro % (f * f) === 0) { dentro /= f * f; fora *= f; }
    return (fora > 1 ? fora : '') + '√' + dentro + ' ≈ ' + fn(r);
  }
  var OPS = [
    ['soma', 'u + v'], ['dif', 'u − v'], ['escalar', 'k·u'], ['norma', '‖u‖'], ['pe', 'u · v e ângulo'],
    ['pv', 'u × v e área'], ['proj', 'projeção de v em u'], ['misto', 'u · (v × w)'], ['reta', 'reta e distância'], ['plano', 'plano e distância'],
  ];
  function labVetores(host) {
    if (!labGA.op || labGA.semOp !== ui.sem) {
      labGA.op = { 1: 'soma', 2: 'pv', 3: 'misto', 4: 'reta', 5: 'plano' }[ui.sem] || 'soma';
      labGA.semOp = ui.sem;
    }
    var fig = null;
    function nomes() {
      if (labGA.op === 'reta') return ['P', 'v', 'Q'];
      if (labGA.op === 'plano') return ['P', 'n', 'Q'];
      return ['u', 'v', 'w'];
    }
    function render() {
      var nm = nomes();
      var usaW = ['misto', 'reta', 'plano'].indexOf(labGA.op) >= 0;
      var usaV = ['escalar', 'norma'].indexOf(labGA.op) < 0;
      function linha(id, rot, arr, on) {
        return '<div class="vin" style="' + (on ? '' : 'opacity:.35') + '"><label>' + rot + '</label>' + arr.map(function (x, i) { return '<input type="number" step="any" data-vec="' + id + '" data-i="' + i + '" value="' + x + '" aria-label="' + rot + ' coordenada ' + 'xyz'[i] + '">'; }).join('') + '</div>';
      }
      var ctl = '<div class="lab-ctl"><h5>Vetores e pontos (x, y, z)</h5>' + linha('u', nm[0], labGA.u, true) + linha('v', nm[1], labGA.v, usaV) + linha('w', nm[2], labGA.w, usaW) +
        (labGA.op === 'escalar' ? '<div class="vin"><label>k</label><input type="number" step="any" id="lab-k" value="' + labGA.k + '"></div>' : '') +
        '<h5 style="margin-top:14px">Operação</h5><div class="ops">' + OPS.map(function (o) { return '<button data-op="' + o[0] + '" class="' + (o[0] === labGA.op ? 'active' : '') + '">' + o[1] + '</button>'; }).join('') + '</div>' +
        '<div class="lab-res" id="lab-res"></div><div class="insight" id="lab-ins"></div></div>';
      host.innerHTML = '<div class="lab-grid">' + ctl + '<div class="lab-canvas"><canvas id="lab-cv" aria-label="Desenho do laboratório"></canvas><span class="vistas"><button data-vista="padrao">3D</button><button data-vista="frente">frente</button><button data-vista="cima">de cima</button></span></div></div>';
      $$('[data-vec]', host).forEach(function (inp) {
        inp.addEventListener('input', function () {
          var val = parseFloat(inp.value.replace(',', '.'));
          if (!isNaN(val)) { labGA[inp.dataset.vec][+inp.dataset.i] = val; calcula(); }
        });
      });
      var kk = $('#lab-k', host); if (kk) kk.addEventListener('input', function () { var val = parseFloat(kk.value.replace(',', '.')); if (!isNaN(val)) { labGA.k = val; calcula(); } });
      $$('[data-op]', host).forEach(function (b) { b.addEventListener('click', function () { labGA.op = b.dataset.op; render(); }); });
      fig = Figura.montar($('#lab-cv', host), { modo: '3d', itens: [] });
      figuras.push(fig);
      $$('.vistas button', host).forEach(function (b) { b.addEventListener('click', function () { fig.vista(b.dataset.vista); }); });
      calcula();
    }
    function calcula() {
      var u = labGA.u, v = labGA.v, w = labGA.w, O = [0, 0, 0], it = [], res = [], ins = '';
      var vet = function (de, ate, rot, cor) { it.push({ tipo: 'vetor', de: de, ate: ate, rot: rot, cor: cor }); };
      switch (labGA.op) {
        case 'soma': {
          var s = vsoma(u, v);
          it.push({ tipo: 'poligono', pts: [O, u, s, v], cor: 3 });
          vet(O, u, 'u', 1); vet(O, v, 'v', 2); vet(u, s, '', 2); vet(O, s, 'u+v', 4);
          res = [['u + v', fv(s), true], ['‖u + v‖', raizTxt(vdot(s, s))]];
          ins = 'Somar é andar u e depois andar v. O resultado é a diagonal do paralelogramo (a área clara). Coordenada com coordenada: x com x, y com y, z com z.';
          break;
        }
        case 'dif': {
          var d = vsub(u, v);
          vet(O, u, 'u', 1); vet(O, v, 'v', 2); vet(v, u, 'u−v', 4); it.push({ tipo: 'segmento', de: O, ate: d, tracejado: true, cor: 4 });
          res = [['u − v', fv(d), true], ['‖u − v‖ (distância entre as pontas)', raizTxt(vdot(d, d))]];
          ins = 'u − v é a seta que sai da ponta de v e chega na ponta de u. Por isso o vetor AB é B − A: destino menos origem.';
          break;
        }
        case 'escalar': {
          var ku = vmul(labGA.k, u);
          vet(O, ku, labGA.k + '·u', 4); vet(O, u, 'u', 1);
          res = [['k·u', fv(ku), true], ['‖k·u‖', fn(Math.abs(labGA.k) * vnorm(u))], ['‖u‖', fn(vnorm(u))]];
          ins = labGA.k < 0 ? 'k negativo inverte o sentido: a seta aponta para o lado oposto.' : labGA.k === 0 ? 'k = 0 dá o vetor nulo.' : 'k positivo mantém o sentido e multiplica o tamanho por ' + fn(labGA.k) + '.';
          break;
        }
        case 'norma': {
          vet(O, u, 'u', 1);
          it.push({ tipo: 'segmento', de: O, ate: [u[0], 0, 0], tracejado: true, cor: 3 });
          it.push({ tipo: 'segmento', de: [u[0], 0, 0], ate: [u[0], u[1], 0], tracejado: true, cor: 3 });
          it.push({ tipo: 'segmento', de: [u[0], u[1], 0], ate: u, tracejado: true, cor: 3 });
          res = [['‖u‖', raizTxt(vdot(u, u)), true], ['x² + y² + z²', fn(vdot(u, u))]];
          ins = 'Pitágoras duas vezes: primeiro no chão (x e y), depois subindo z. As linhas tracejadas são esse caminho.';
          break;
        }
        case 'pe': {
          var pe = vdot(u, v), nu = vnorm(u), nv = vnorm(v);
          vet(O, u, 'u', 1); vet(O, v, 'v', 2);
          var ang = nu && nv ? Math.acos(Math.max(-1, Math.min(1, pe / (nu * nv)))) * 180 / Math.PI : NaN;
          res = [['u · v', fn(pe), true], ['cos θ', nu && nv ? fn(pe / (nu * nv)) : '—'], ['θ', isNaN(ang) ? '—' : fn(ang) + '°']];
          ins = Math.abs(pe) < 1e-9 ? 'u · v = 0: os vetores são perpendiculares.' : pe > 0 ? 'u · v positivo: ângulo agudo (menor que 90°).' : 'u · v negativo: ângulo obtuso (maior que 90°).';
          ins += ' É o SOMARPRODUTO das coordenadas: ' + fn(u[0]) + '·' + fn(v[0]) + ' + ' + fn(u[1]) + '·' + fn(v[1]) + ' + ' + fn(u[2]) + '·' + fn(v[2]) + '.';
          break;
        }
        case 'pv': {
          var c = vcross(u, v), s2 = vsoma(u, v);
          it.push({ tipo: 'poligono', pts: [O, u, s2, v], cor: 3 });
          vet(O, u, 'u', 1); vet(O, v, 'v', 2); vet(O, c, 'u×v', 4);
          res = [['u × v', fv(c), true], ['área do paralelogramo', raizTxt(vdot(c, c))], ['área do triângulo', fn(vnorm(c) / 2)], ['confira: u · (u × v)', fn(vdot(u, c))]];
          ins = 'u × v sai perpendicular aos dois (gire a figura para ver). O tamanho dele é a área do paralelogramo claro. Troque a ordem e ele aponta para o outro lado.';
          break;
        }
        case 'proj': {
          var nu2 = vdot(u, u);
          if (nu2 < 1e-12) { res = [['projeção', 'u não pode ser nulo', true]]; ins = 'Projetar sobre o vetor nulo não tem direção.'; vet(O, v, 'v', 2); break; }
          var v1 = vmul(vdot(v, u) / nu2, u), v2 = vsub(v, v1);
          vet(O, u, 'u', 1); vet(O, v, 'v', 2); vet(O, v1, 'v₁', 4); it.push({ tipo: 'segmento', de: v1, ate: v, tracejado: true, cor: 3 });
          res = [['v₁ = proj de v em u', fv(v1), true], ['v₂ = v − v₁', fv(v2)], ['confira: v₂ · u', fn(vdot(v2, u))]];
          ins = 'A sombra de v sobre a reta de u é v₁. O que sobra, v₂, fica perpendicular a u (a linha tracejada). Fórmula: (v·u / u·u)·u.';
          break;
        }
        case 'misto': {
          var m = vdot(u, vcross(v, w));
          var uv = vsoma(u, v), uw = vsoma(u, w), vw = vsoma(v, w), uvw = vsoma(uv, w);
          [[O, u], [O, v], [O, w], [u, uv], [u, uw], [v, uv], [v, vw], [w, uw], [w, vw], [uv, uvw], [uw, uvw], [vw, uvw]].forEach(function (e, i) {
            if (i > 2) it.push({ tipo: 'segmento', de: e[0], ate: e[1], cor: 3 });
          });
          vet(O, u, 'u', 1); vet(O, v, 'v', 2); vet(O, w, 'w', 4);
          res = [['u · (v × w)', fn(m), true], ['volume do paralelepípedo', fn(Math.abs(m))], ['volume do tetraedro', fn(Math.abs(m) / 6)]];
          ins = Math.abs(m) < 1e-9 ? 'Produto misto zero: os três vetores estão no mesmo plano (coplanares). A caixa achatou.' : 'O módulo do produto misto é o volume da caixa. O sinal só diz a orientação (regra da mão direita).';
          break;
        }
        case 'reta': {
          var P = u, dv = v, Q = w;
          var nd = vdot(dv, dv);
          if (nd < 1e-12) { res = [['reta', 'o vetor diretor não pode ser nulo', true]]; break; }
          it.push({ tipo: 'segmento', de: vsoma(P, vmul(-2, dv)), ate: vsoma(P, vmul(2, dv)), cor: 1 });
          it.push({ tipo: 'ponto', em: P, rot: 'P' }); vet(P, vsoma(P, dv), 'v', 2); it.push({ tipo: 'ponto', em: Q, rot: 'Q', cor: 2 });
          var H = vsoma(P, vmul(vdot(vsub(Q, P), dv) / nd, dv));
          it.push({ tipo: 'segmento', de: Q, ate: H, tracejado: true, cor: 4 }); it.push({ tipo: 'ponto', em: H, rot: 'H', cor: 3 });
          var dist = vnorm(vcross(vsub(Q, P), dv)) / Math.sqrt(nd);
          res = [['reta', '(x, y, z) = ' + fv(P) + ' + t·' + fv(dv), false], ['distância de Q à reta', fn(dist), true], ['pé da perpendicular H', fv(H)]];
          ins = 'Distância ponto-reta = ‖PQ × v‖ / ‖v‖: a área do paralelogramo dividida pela base. H é o ponto da reta mais perto de Q.';
          break;
        }
        case 'plano': {
          var P0 = u, n = v, Q2 = w, nn = vnorm(n);
          if (nn < 1e-12) { res = [['plano', 'o vetor normal não pode ser nulo', true]]; break; }
          var a1 = Math.abs(n[0]) < 0.9 * nn ? [1, 0, 0] : [0, 1, 0];
          var e1 = vcross(n, a1); e1 = vmul(1 / vnorm(e1), e1);
          var e2 = vcross(n, e1); e2 = vmul(1 / vnorm(e2), e2);
          var L = 3;
          it.push({ tipo: 'poligono', pts: [vsoma(P0, vsoma(vmul(L, e1), vmul(L, e2))), vsoma(P0, vsoma(vmul(-L, e1), vmul(L, e2))), vsoma(P0, vsoma(vmul(-L, e1), vmul(-L, e2))), vsoma(P0, vsoma(vmul(L, e1), vmul(-L, e2)))], cor: 1 });
          it.push({ tipo: 'ponto', em: P0, rot: 'P' }); vet(P0, vsoma(P0, n), 'n', 2); it.push({ tipo: 'ponto', em: Q2, rot: 'Q', cor: 2 });
          var dd = -vdot(n, P0), sd = (vdot(n, Q2) + dd) / nn;
          var F = vsub(Q2, vmul(sd / nn, n));
          it.push({ tipo: 'segmento', de: Q2, ate: F, tracejado: true, cor: 4 });
          res = [['plano', fn(n[0]) + 'x + ' + fn(n[1]) + 'y + ' + fn(n[2]) + 'z + ' + fn(dd) + ' = 0', false], ['distância de Q ao plano', fn(Math.abs(sd)), true], ['pé da perpendicular', fv(F)]];
          ins = 'O vetor normal dá os coeficientes a, b, c. O d sai de substituir P. Distância = |a·x₀ + b·y₀ + c·z₀ + d| / ‖n‖.';
          break;
        }
      }
      $('#lab-res', host).innerHTML = res.map(function (r) { return '<div><span>' + esc(r[0]) + '</span><strong class="' + (r[2] ? 'big' : '') + '">' + esc(r[1]) + '</strong></div>'; }).join('');
      $('#lab-ins', host).textContent = ins;
      fig.trocar({ modo: '3d', itens: it });
    }
    render();
  }

  // --- cônicas ---
  function labConicas(host) {
    var fig;
    function render() {
      var t = labCon.tipo;
      host.innerHTML = '<div class="lab-grid"><div class="lab-ctl"><h5>Curva</h5><div class="ops">' +
        [['elipse', 'elipse'], ['hiperbole', 'hipérbole'], ['parabola', 'parábola'], ['circ', 'circunferência']].map(function (o) { return '<button data-t="' + o[0] + '" class="' + (o[0] === t ? 'active' : '') + '">' + o[1] + '</button>'; }).join('') + '</div>' +
        (t === 'parabola' ? '<label class="vin" style="grid-template-columns:60px 1fr"><b>p</b><input type="range" min="0.5" max="4" step="0.5" id="c-p" value="' + labCon.p + '"></label>'
          : '<label class="vin" style="grid-template-columns:60px 1fr"><b>a</b><input type="range" min="1" max="7" step="0.5" id="c-a" value="' + labCon.a + '"></label>' +
          (t === 'circ' ? '' : '<label class="vin" style="grid-template-columns:60px 1fr"><b>b</b><input type="range" min="1" max="7" step="0.5" id="c-b" value="' + labCon.b + '"></label>')) +
        '<div class="lab-res" id="c-res"></div><div class="insight" id="c-ins"></div></div><div class="lab-canvas"><canvas id="c-cv"></canvas></div></div>';
      $$('[data-t]', host).forEach(function (b) { b.addEventListener('click', function () { labCon.tipo = b.dataset.t; render(); }); });
      ['a', 'b', 'p'].forEach(function (k) { var i = $('#c-' + k, host); if (i) i.addEventListener('input', function () { labCon[k] = +i.value; calc(); }); });
      fig = Figura.montar($('#c-cv', host), { modo: '2d', itens: [] }); figuras.push(fig);
      calc();
    }
    function calc() {
      var t = labCon.tipo, a = labCon.a, b = labCon.b, p = labCon.p, it = [], res = [], ins = '', pts = [], k;
      if (t === 'elipse' || t === 'circ') {
        if (t === 'circ') b = a;
        for (k = 0; k <= 72; k++) { var th = k / 72 * 2 * Math.PI; pts.push([a * Math.cos(th), b * Math.sin(th)]); }
        it.push({ tipo: 'poligono', pts: pts, cor: 1, aberto: true });
        var maior = Math.max(a, b), menor = Math.min(a, b), c = Math.sqrt(maior * maior - menor * menor);
        var focos = a >= b ? [[c, 0], [-c, 0]] : [[0, c], [0, -c]];
        focos.forEach(function (f, i) { it.push({ tipo: 'ponto', em: f, rot: i ? 'F₂' : 'F₁', cor: 2 }); });
        res = [['equação', 'x²/' + fn(a * a) + ' + y²/' + fn(b * b) + ' = 1', true], ['c (centro ao foco)', fn(c)], ['excentricidade e = c/a', fn(c / maior)]];
        ins = t === 'circ' ? 'Com a = b, os dois focos caem no centro e a excentricidade é 0: a elipse vira circunferência.' : 'Na elipse, o maior denominador manda: ele diz qual eixo é o maior. a² = b² + c² (com a o semieixo maior). Quanto mais perto de 1 a excentricidade, mais achatada.';
      } else if (t === 'hiperbole') {
        [1, -1].forEach(function (lado) {
          var ramo = [];
          for (k = -30; k <= 30; k++) { var s = k / 10; ramo.push([lado * a * Math.cosh(s), b * Math.sinh(s)]); }
          it.push({ tipo: 'poligono', pts: ramo, cor: 1, aberto: true });
        });
        var ch = Math.sqrt(a * a + b * b), L = a * Math.cosh(3);
        it.push({ tipo: 'segmento', de: [-L, -L * b / a], ate: [L, L * b / a], tracejado: true });
        it.push({ tipo: 'segmento', de: [-L, L * b / a], ate: [L, -L * b / a], tracejado: true });
        it.push({ tipo: 'ponto', em: [ch, 0], rot: 'F₁', cor: 2 }); it.push({ tipo: 'ponto', em: [-ch, 0], rot: 'F₂', cor: 2 });
        res = [['equação', 'x²/' + fn(a * a) + ' − y²/' + fn(b * b) + ' = 1', true], ['c', fn(ch)], ['assíntotas', 'y = ±' + fn(b / a) + 'x'], ['excentricidade', fn(ch / a)]];
        ins = 'Na hipérbole o sinal de menos muda tudo: c² = a² + b², então c é maior que a e a excentricidade passa de 1. As retas tracejadas são as assíntotas.';
      } else {
        for (k = -40; k <= 40; k++) { var y = k / 40 * 4 * Math.sqrt(p) * 2; pts.push([y * y / (4 * p), y]); }
        it.push({ tipo: 'poligono', pts: pts, cor: 1, aberto: true });
        it.push({ tipo: 'ponto', em: [p, 0], rot: 'F', cor: 2 });
        var yy = 4 * Math.sqrt(p) * 2;
        it.push({ tipo: 'segmento', de: [-p, -yy], ate: [-p, yy], tracejado: true, cor: 3 });
        res = [['equação', 'y² = ' + fn(4 * p) + 'x', true], ['foco', '(' + fn(p) + ', 0)'], ['diretriz', 'x = ' + fn(-p)]];
        ins = 'Cada ponto da parábola está à mesma distância do foco e da diretriz (a reta tracejada). O número na frente do x é 4p.';
      }
      $('#c-res', host).innerHTML = res.map(function (r) { return '<div><span>' + esc(r[0]) + '</span><strong class="' + (r[2] ? 'big' : '') + '">' + esc(r[1]) + '</strong></div>'; }).join('');
      $('#c-ins', host).textContent = ins;
      fig.trocar({ modo: '2d', itens: it });
    }
    render();
  }

  // --- bits ---
  function labBitsR(host) {
    function render() {
      var n = labBits.n & 255, bits = '';
      for (var i = 7; i >= 0; i--) {
        var on = (n >> i) & 1;
        bits += '<button class="bit ' + (on ? 'on' : '') + '" data-b="' + i + '" aria-pressed="' + (on ? 'true' : 'false') + '"><b>' + on + '</b><small>' + (1 << i) + '</small></button>';
      }
      var bin = ('00000000' + n.toString(2)).slice(-8);
      var soma = [];
      for (var j = 7; j >= 0; j--) if ((n >> j) & 1) soma.push(1 << j);
      var comSinal = n >= 128 ? n - 256 : n;
      host.innerHTML = '<div class="lab-grid" style="grid-template-columns:1fr"><div class="lab-pane"><h5 style="font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">Um byte: clique nos interruptores</h5><div class="bits">' + bits + '</div>' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px"><label style="font-size:13px">Decimal <input type="number" min="0" max="255" id="b-n" value="' + n + '" style="width:90px;border:1px solid var(--line);padding:6px 8px;background:var(--white)"></label><button class="ghost" id="b-mais">+1</button><button class="ghost" id="b-menos">−1</button><button class="ghost" id="b-inv">inverter todos</button></div>' +
        '<div class="lab-res" style="grid-template-columns:repeat(auto-fit,minmax(170px,1fr));display:grid">' +
        '<div><span>decimal</span><strong class="big">' + n + '</strong></div><div><span>binário</span><strong>' + bin.slice(0, 4) + ' ' + bin.slice(4) + '</strong></div>' +
        '<div><span>hexadecimal</span><strong>' + n.toString(16).toUpperCase() + '</strong></div><div><span>octal</span><strong>' + n.toString(8) + '</strong></div>' +
        '<div><span>com sinal (complemento de 2)</span><strong>' + String(comSinal).replace('-', '−') + '</strong></div><div><span>soma das posições ligadas</span><strong>' + (soma.length ? soma.join(' + ') : '0') + '</strong></div></div>' +
        '<div class="insight">Cada interruptor vale o dobro do vizinho da direita. Hexadecimal agrupa 4 bits: ' + bin.slice(0, 4) + ' = ' + parseInt(bin.slice(0, 4), 2).toString(16).toUpperCase() + ' e ' + bin.slice(4) + ' = ' + parseInt(bin.slice(4), 2).toString(16).toUpperCase() + '. Com o bit de 128 ligado, quem lê como número com sinal enxerga um negativo.</div></div></div>';
      $$('[data-b]', host).forEach(function (b) { b.addEventListener('click', function () { labBits.n = n ^ (1 << +b.dataset.b); render(); }); });
      var inp = $('#b-n', host);
      inp.addEventListener('change', function () { var v = parseInt(inp.value, 10); if (!isNaN(v)) { labBits.n = Math.max(0, Math.min(255, v)); render(); } });
      $('#b-mais', host).addEventListener('click', function () { labBits.n = (n + 1) & 255; render(); });
      $('#b-menos', host).addEventListener('click', function () { labBits.n = (n + 255) & 255; render(); });
      $('#b-inv', host).addEventListener('click', function () { labBits.n = (~n) & 255; render(); });
    }
    render();
  }

  // --- tabela-verdade ---
  function parseLogica(src) {
    var toks = [], i = 0;
    var s = src.replace(/<->|<=>/g, '↔').replace(/->|=>/g, '→');
    while (i < s.length) {
      var c = s[i];
      if (/\s/.test(c)) { i++; continue; }
      if (/[p-u]/i.test(c)) { toks.push({ t: 'at', v: c.toLowerCase() }); i++; continue; }
      if ('¬~!'.indexOf(c) >= 0) { toks.push({ t: 'nao' }); i++; continue; }
      if ('∧&^'.indexOf(c) >= 0) { toks.push({ t: 'e' }); i++; continue; }
      if ('∨|'.indexOf(c) >= 0) { toks.push({ t: 'ou' }); i++; continue; }
      if (c === '⊕') { toks.push({ t: 'xou' }); i++; continue; }
      if (c === '→') { toks.push({ t: 'imp' }); i++; continue; }
      if (c === '↔') { toks.push({ t: 'bi' }); i++; continue; }
      if (c === '(' || c === ')') { toks.push({ t: c }); i++; continue; }
      throw new Error('não entendi o símbolo "' + c + '"');
    }
    var p = 0;
    function pk() { return toks[p] || { t: 'fim' }; }
    function bi() { var a = imp(); while (pk().t === 'bi') { p++; a = { op: '↔', a: a, b: imp() }; } return a; }
    function imp() { var a = ou(); if (pk().t === 'imp') { p++; return { op: '→', a: a, b: imp() }; } return a; }
    function ou() { var a = e(); while (pk().t === 'ou' || pk().t === 'xou') { var op = toks[p++].t === 'ou' ? '∨' : '⊕'; a = { op: op, a: a, b: e() }; } return a; }
    function e() { var a = nao(); while (pk().t === 'e') { p++; a = { op: '∧', a: a, b: nao() }; } return a; }
    function nao() { if (pk().t === 'nao') { p++; return { op: '¬', a: nao() }; } return at(); }
    function at() {
      var t = toks[p++];
      if (!t) throw new Error('a expressão terminou no meio');
      if (t.t === 'at') return { at: t.v };
      if (t.t === '(') { var x = bi(); if (!toks[p] || toks[p].t !== ')') throw new Error('faltou fechar parêntese'); p++; return x; }
      throw new Error('esperava uma letra (p, q, r...) ou "("');
    }
    var arv = bi();
    if (p < toks.length) throw new Error('sobrou algo depois do fim da expressão');
    return arv;
  }
  function txtArv(n, topo) {
    if (n.at) return n.at;
    if (n.op === '¬') return '¬' + txtArv(n.a);
    var s = txtArv(n.a) + ' ' + n.op + ' ' + txtArv(n.b);
    return topo ? s : '(' + s + ')';
  }
  function atomos(n, set) { if (n.at) set[n.at] = 1; else { atomos(n.a, set); if (n.b) atomos(n.b, set); } return set; }
  function avalia(n, v) {
    if (n.at) return v[n.at];
    var a = avalia(n.a, v);
    if (n.op === '¬') return !a;
    var b = avalia(n.b, v);
    return n.op === '∧' ? a && b : n.op === '∨' ? a || b : n.op === '⊕' ? a !== b : n.op === '→' ? (!a || b) : a === b;
  }
  function subformulas(n, lista) { if (!n.at) { subformulas(n.a, lista); if (n.b) subformulas(n.b, lista); lista.push(n); } return lista; }
  function labVerdade(host) {
    host.innerHTML = '<div class="lab-grid" style="grid-template-columns:1fr"><div class="lab-pane">' +
      '<h5 style="font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:0 0 6px">Expressão (letras p, q, r, s)</h5>' +
      '<div class="tv-input"><input id="tv1" value="' + esc(labTV.e1) + '" aria-label="Expressão 1" autocomplete="off" spellcheck="false"></div>' +
      '<div class="symbtn">' + ['¬', '∧', '∨', '→', '↔', '⊕', '(', ')', 'p', 'q', 'r'].map(function (s) { return '<button data-s="' + s + '">' + s + '</button>'; }).join('') + '</div>' +
      '<h5 style="font-size:9px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin:10px 0 6px">Comparar com (opcional: testa se são equivalentes)</h5>' +
      '<div class="tv-input"><input id="tv2" value="' + esc(labTV.e2) + '" aria-label="Expressão 2" autocomplete="off" spellcheck="false"></div>' +
      '<div id="tv-out"></div></div></div>';
    var foco = $('#tv1', host);
    ['#tv1', '#tv2'].forEach(function (s) { $(s, host).addEventListener('focus', function () { foco = $(s, host); }); $(s, host).addEventListener('input', calc); });
    $$('[data-s]', host).forEach(function (b) {
      b.addEventListener('click', function () {
        var i = foco.selectionStart || foco.value.length;
        foco.value = foco.value.slice(0, i) + b.dataset.s + foco.value.slice(foco.selectionEnd || i);
        foco.focus(); foco.selectionStart = foco.selectionEnd = i + 1; calc();
      });
    });
    function calc() {
      labTV.e1 = $('#tv1', host).value; labTV.e2 = $('#tv2', host).value;
      var out = $('#tv-out', host);
      try {
        var a1 = parseLogica(labTV.e1), a2 = labTV.e2.trim() ? parseLogica(labTV.e2) : null;
        var at = atomos(a1, {}); if (a2) atomos(a2, at);
        var letras = Object.keys(at).sort();
        if (letras.length > 4) throw new Error('use no máximo 4 letras');
        var cols = subformulas(a1, []);
        var vistos = {}; cols = cols.filter(function (c) { var t = txtArv(c, true); if (vistos[t]) return false; vistos[t] = 1; return true; });
        var linhas = 1 << letras.length, col1 = [], col2 = [];
        var h = '<div class="tw"><table class="tv"><thead><tr>' + letras.map(function (l) { return '<th>' + l + '</th>'; }).join('') + cols.map(function (c) { return '<th>' + esc(txtArv(c, true)) + '</th>'; }).join('') + (a2 ? '<th>' + esc(txtArv(a2, true)) + '</th>' : '') + '</tr></thead><tbody>';
        for (var r = 0; r < linhas; r++) {
          var v = {};
          letras.forEach(function (l, i) { v[l] = !((r >> (letras.length - 1 - i)) & 1); });
          h += '<tr>' + letras.map(function (l) { return '<td class="' + (v[l] ? 'v' : 'f') + '">' + (v[l] ? 'V' : 'F') + '</td>'; }).join('');
          cols.forEach(function (c) { var x = avalia(c, v); h += '<td class="' + (x ? 'v' : 'f') + '">' + (x ? 'V' : 'F') + '</td>'; });
          col1.push(avalia(a1, v));
          if (a2) { var y = avalia(a2, v); col2.push(y); h += '<td class="' + (y ? 'v' : 'f') + '">' + (y ? 'V' : 'F') + '</td>'; }
          h += '</tr>';
        }
        h += '</tbody></table></div>';
        var nv = col1.filter(Boolean).length;
        var cls = nv === linhas ? 'tautologia (V em todas as linhas)' : nv === 0 ? 'contradição (F em todas as linhas)' : 'contingência (' + nv + ' V e ' + (linhas - nv) + ' F)';
        var eq = '';
        if (a2) {
          var dif = -1;
          for (var k = 0; k < linhas; k++) if (col1[k] !== col2[k]) { dif = k; break; }
          eq = dif < 0 ? ' As duas colunas finais são iguais em todas as ' + linhas + ' linhas: as expressões são <b>equivalentes</b>.' : ' As expressões <b>não são equivalentes</b>: diferem na linha ' + (dif + 1) + '.';
        }
        out.innerHTML = h + '<div class="insight">' + linhas + ' linhas (2 elevado ao número de letras). A primeira expressão é ' + cls + '.' + eq + '</div>';
      } catch (err) {
        out.innerHTML = '<div class="insight">' + esc(err.message) + '. Use ¬ ∧ ∨ → ↔ ⊕ e parênteses (também aceito ~ & | -> <->).</div>';
      }
    }
    calc();
  }

  // --- VisuAlg ---
  function labVisualg(host) {
    var exs = EX_VA.filter(function (e) { return e.semana <= ui.sem; });
    if (!labVA) labVA = { cod: exs.length ? exs[exs.length - 1].codigo : '', ent: exs.length ? (exs[exs.length - 1].entradas || []).join('\n') : '' };
    host.innerHTML = '<div class="lab-grid" style="grid-template-columns:minmax(0,1fr)"><div class="lab-pane" style="padding:0;border-bottom:1px solid var(--line)">' +
      '<div style="display:flex;gap:6px;padding:10px;border-bottom:1px solid var(--line);flex-wrap:wrap;align-items:center"><select id="va-ex" style="flex:1;min-width:160px;border:1px solid var(--line);padding:7px;background:var(--white)"><option value="">Exemplos prontos…</option>' +
      exs.map(function (e, i) { return '<option value="' + i + '">' + esc(e.titulo) + '</option>'; }).join('') + '</select><button class="primary-button" id="va-run" style="padding:9px 14px">Rodar ▶</button></div>' +
      '<textarea class="editor" id="va-cod" spellcheck="false" aria-label="Código VisuAlg" style="min-height:240px">' + esc(labVA.cod) + '</textarea>' +
      '<div style="padding:10px"><label style="font-size:11.5px;color:var(--muted)">Entradas (uma por linha, na ordem dos leia)</label><textarea id="va-ent" style="width:100%;min-height:60px;border:1px solid var(--line);padding:6px;font-family:var(--font-mono);background:var(--white)">' + esc(labVA.ent) + '</textarea></div></div>' +
      '<div class="lab-pane" id="va-mesa"><p style="color:var(--muted);font-size:13px">Escreva ou escolha um programa e clique em Rodar. O teste de mesa mostra cada linha executada e o valor das variáveis naquele momento.</p></div></div>';
    $('#va-ex', host).addEventListener('change', function () {
      var e = exs[+this.value]; if (!e) return;
      $('#va-cod', host).value = e.codigo; $('#va-ent', host).value = (e.entradas || []).join('\n'); roda();
    });
    $('#va-run', host).addEventListener('click', roda);
    function roda() {
      labVA.cod = $('#va-cod', host).value; labVA.ent = $('#va-ent', host).value;
      var ent = labVA.ent.split('\n').map(function (s) { return s.trim(); }).filter(function (s) { return s.length; });
      mesa($('#va-mesa', host), labVA.cod, ent, 'Teste de mesa');
    }
  }

  // ---------- simulado ----------
  var sim = { tipo: 'misto', lista: [], i: 0, resp: [] };
  function sorteia(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
  function montaSim(tipo, soMaterial) {
    var lista = [];
    var anteriores = st.simUltimas && st.simUltimas[tipo] ? st.simUltimas[tipo] : [];
    var discs = tipo === 'misto' ? ['ga', 'lp'] : [tipo];
    discs.forEach(function (d) {
      for (var w = 1; w <= 6; w++) {
        if (soMaterial && semanaInfo(d, w).previa) continue;
        var qs = questoesDa(d, w);
        if (!qs.length) continue;
        var niveis = tipo === 'misto' ? [((w - 1) % 3) + 1] : [1, 2, 3];
        niveis.forEach(function (n) {
          var cand = qs.filter(function (q) { return q.nivel === n && lista.indexOf(q) < 0 && anteriores.indexOf(q.id) < 0; });
          if (!cand.length) cand = qs.filter(function (q) { return lista.indexOf(q) < 0 && anteriores.indexOf(q.id) < 0; });
          if (!cand.length) cand = qs.filter(function (q) { return q.nivel === n && lista.indexOf(q) < 0; });
          if (!cand.length) cand = qs.filter(function (q) { return lista.indexOf(q) < 0; });
          if (cand.length) lista.push(sorteia(cand));
        });
      }
    });
    return lista;
  }
  function renderSimCard() {
    var html = '';
    [['ga', 'Geometria'], ['lp', 'Lógica'], ['misto', 'Misto']].forEach(function (x) {
      var r = st.sim[x[0]];
      html += '<div class="sim-row"><span><b>' + x[1] + '</b></span>' + (r ? '<strong>' + fmtNota(r.nota) + '</strong><small>' + r.acertos + ' de ' + r.total + '<br>' + esc(r.data) + '</small>' : '<small>ainda não feito</small>') + '</div>';
    });
    $('#sim-rows').innerHTML = html;
  }
  function simQuestao() {
    figReg = [];
    var q = sim.lista[sim.i];
    $('#quiz-label').textContent = 'Questão ' + (sim.i + 1) + ' de ' + sim.lista.length;
    $('#quiz-bar').style.width = ((sim.i + 1) / sim.lista.length * 100) + '%';
    $('#quiz-topic').textContent = NOME[q.disc] + ' · Semana ' + q.semana + ' · ' + q.tema;
    var h = '<p class="q-enunciado">' + md(q.enunciado) + '</p>';
    if (q.codigo) { h += htmlCodigo(q.codigo); if (q.entradas && q.entradas.length) h += '<p class="entradas-chip">Entradas: ' + q.entradas.map(function (x) { return '<code>' + esc(x) + '</code>'; }).join(' ') + '</p>'; }
    if (q.figura && q.figura.onde === 'enunciado') h += htmlFigura(q.figura);
    if (q.tabela && q.tabela.onde === 'enunciado') h += htmlTabela(q.tabela);
    h += '<div class="alts">' + q.alternativas.map(function (a, i) { return '<button class="alt" data-s="' + i + '"><span class="l">' + 'ABCDE'[i] + '</span><span>' + md(a.t) + '</span><span class="m"></span></button>'; }).join('') + '</div>';
    var area = $('#quiz-q');
    area.innerHTML = h;
    montaFiguras(area);
    $('#next-question').disabled = true;
    $('#next-question').innerHTML = sim.i === sim.lista.length - 1 ? 'Ver resultado <span>→</span>' : 'Próxima <span>→</span>';
    $$('[data-s]', area).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('[data-s]', area).forEach(function (x) { x.style.borderColor = ''; x.style.background = ''; });
        b.style.borderColor = 'var(--ink)'; b.style.background = 'var(--white)';
        sim.resp[sim.i] = +b.dataset.s; $('#next-question').disabled = false;
      });
    });
  }
  function simResultado() {
    var ac = 0;
    sim.lista.forEach(function (q, i) { if (q.alternativas[sim.resp[i]] && q.alternativas[sim.resp[i]].certa) ac++; });
    var nota = ac / sim.lista.length * 10;
    $('#quiz-area').hidden = true; $('#quiz-result').hidden = false;
    $('#quiz-score').textContent = ac; $('#quiz-total').textContent = sim.lista.length; $('#quiz-nota').textContent = fmtNota(nota);
    $('#result-mark').textContent = fmtNota(nota);
    $('#quiz-message').textContent = nota >= 8 ? 'Base firme. Leia o comentário das que errou e siga em frente.' : nota >= 5 ? 'Boa parte já está no lugar. As erradas abaixo dizem exatamente onde revisar.' : 'Este resultado é um mapa, não um rótulo. Volte às questões erradas e troque de jeito de explicação.';
    $('#quiz-review').innerHTML = sim.lista.map(function (q, i) {
      var e = sim.resp[i], ok = q.alternativas[e] && q.alternativas[e].certa;
      var ci = q.alternativas.map(function (a) { return !!a.certa; }).indexOf(true);
      return '<div class="review-item"><span class="mk ' + (ok ? 'ok' : 'bad') + '">' + (ok ? '✓' : '✗') + '</span><div><b>' + esc(NOME[q.disc]) + ' · ' + esc(q.origem) + ' · ' + esc(q.tema) + '</b>' +
        '<p>' + (ok ? 'Você marcou ' + 'ABCDE'[e] + '. ' + md(q.resposta) : 'Você marcou ' + 'ABCDE'[e] + '; a certa é ' + 'ABCDE'[ci] + '. ' + md(q.alternativas[e].erro || '')) + '</p></div><button class="ghost" data-rever="' + q.id + '">rever</button></div>';
    }).join('');
    $$('[data-rever]').forEach(function (b) {
      b.addEventListener('click', function () {
        var q = porId[b.dataset.rever];
        $('#sim-dialog').close();
        abrirSemana(q.disc, q.semana, 'questao', q.id);
      });
    });
    var d = new Date();
    st.sim[sim.tipo] = { acertos: ac, total: sim.lista.length, nota: nota, data: n2(d.getDate()) + '/' + n2(d.getMonth() + 1) + '/' + d.getFullYear() };
    st.simUltimas = st.simUltimas || {};
    st.simUltimas[sim.tipo] = sim.lista.map(function (q) { return q.id; });
    salva(); renderSimCard();
  }
  function comecaSim() {
    var so = $('#sim-so-material').checked;
    sim.lista = montaSim(sim.tipo, so); sim.i = 0; sim.resp = [];
    var aviso = $('#sim-msg');
    if (!sim.lista.length) {
      aviso.hidden = false;
      aviso.textContent = 'Lógica ainda não tem material do professor: todas as semanas são prévia. Desmarque "Só semanas com material" para incluir as prévias.';
      $('#sim-setup').hidden = false; $('#quiz-area').hidden = true; $('#quiz-result').hidden = true;
      return;
    }
    aviso.hidden = true;
    $('#sim-setup').hidden = true; $('#quiz-area').hidden = false; $('#quiz-result').hidden = true;
    simQuestao();
  }

  // ---------- ligações ----------
  function liga() {
    $$('.subject-switch [data-subject]').forEach(function (b) {
      b.addEventListener('click', function () { ui.qid = null; abrirSemana(b.dataset.subject, ui.sem); });
    });
    $$('.view-link').forEach(function (b) { b.addEventListener('click', function () { ui.view = b.dataset.view; renderEstudo(); }); });
    $$('.qfilter button').forEach(function (b) { b.addEventListener('click', function () { ui.filtro = b.dataset.filtro; renderLista(); }); });
    $('#continuar').addEventListener('click', function () {
      if (st.ultimo && porId[st.ultimo.id]) abrirSemana(st.ultimo.disc, st.ultimo.sem, 'questao', st.ultimo.id);
      else { var s = semanaAtual(); abrirSemana('ga', s, 'questao', primeiraPendente('ga', s)); }
    });
    $$('[data-open-planner]').forEach(function (b) { b.addEventListener('click', function () { $('#planner-dialog').showModal(); }); });
    $$('[data-close-dialog]').forEach(function (b) { b.addEventListener('click', function () { b.closest('dialog').close(); }); });
    $$('dialog').forEach(function (d) { d.addEventListener('click', function (e) { if (e.target === d) d.close(); }); });
    $$('.topnav a').forEach(function (a) { a.addEventListener('click', function () { $$('.topnav a').forEach(function (x) { x.classList.remove('active'); }); a.classList.add('active'); }); });
    $('#theme-toggle').addEventListener('click', function () {
      st.tema = st.tema === 'escuro' ? 'claro' : 'escuro'; salva();
      document.body.classList.toggle('dark', st.tema === 'escuro');
      figuras.forEach(function (f) { f.redesenhar(); });
    });
    document.body.classList.toggle('dark', st.tema === 'escuro');
    $('#start-sim').addEventListener('click', function () {
      $('#sim-dialog').showModal(); $('#sim-setup').hidden = false; $('#quiz-area').hidden = true; $('#quiz-result').hidden = true;
    });
    $$('#sim-opts button').forEach(function (b) {
      b.addEventListener('click', function () { sim.tipo = b.dataset.sim; $$('#sim-opts button').forEach(function (x) { x.classList.toggle('active', x === b); }); });
    });
    $('#begin-quiz').addEventListener('click', comecaSim);
    $('#sim-again').addEventListener('click', comecaSim);
    $('#next-question').addEventListener('click', function () { if (sim.i < sim.lista.length - 1) { sim.i++; simQuestao(); } else simResultado(); });
    var tempo = null;
    window.addEventListener('resize', function () { clearTimeout(tempo); tempo = setTimeout(function () { figuras.forEach(function (f) { f.redesenhar(); }); }, 120); });
    document.addEventListener('keydown', function (e) {
      if (e.target.closest && e.target.closest('input,textarea,select,dialog')) return;
      if (document.querySelector('dialog[open]')) return;
      if (e.ctrlKey || e.metaKey || e.altKey || ui.view !== 'questao') return;
      var r = $('#view-questao').getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var k = e.key.toLowerCase(), idx = 'abcde'.indexOf(k);
      if (idx < 0 && /^[1-5]$/.test(k)) idx = +k - 1;
      if (idx >= 0 && porId[ui.qid] && !st.resp[ui.qid]) { responder(porId[ui.qid], idx); e.preventDefault(); }
      else if (e.key === 'ArrowRight') { navegar(1); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { navegar(-1); e.preventDefault(); }
    });
  }

  liga();
  progresso();
  renderHoje();
  renderTrilha();
  renderSimCard();
  ui.sem = semanaAtual();
  if (!questoesDa('ga', ui.sem).length) ui.sem = 1;
  ui.qid = primeiraPendente('ga', ui.sem);
  ui.view = 'conceito';
  renderEstudo();
  $('#rodape-info').textContent = 'Tecnologia em Banco de Dados · UFTM/CEDD · conteúdo gerado em ' + D.geradoEm;
})();
