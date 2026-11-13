/* Tira-dúvidas do Núcleo.
   O aluno escreve a dúvida ou cola um print; o site manda para o "porteiro" (Apps Script do Google).
   Uma atividade na nuvem responde de tempos em tempos; o site lista as respostas.
   Sem endereço do porteiro (PORTEIRO vazio), roda em MODO PROTÓTIPO: nada sai do navegador. */
(function () {
  'use strict';
  // endereço do App da Web do Apps Script ("Porteiro v1", implantado em 09/11/2026). Não é segredo:
  // sem a CHAVE, ele só recebe dúvida, informa status e lista respostas liberadas.
  var PORTEIRO = 'https://script.google.com/macros/s/AKfycbyjUWCd3Zj4cpITJxpE8DoygjSrt87cKzhVRWWOPEKkNkFWVJcyOs0sIjzs1KprkdCf/exec';
  var MAX_TEXTO = 2000;
  var MAX_LADO = 1600;                     // maior lado do print depois de reduzido, em pixels
  var CHAVE_MINHAS = 'nucleo-duvidas-minhas';
  var D = window.NUCLEO;

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function txt(s) { return esc(s).replace(/\n/g, '<br>'); }
  function semAcento(s) { return String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  var NOME = { ga: 'Geometria', lp: 'Lógica' };

  // ---------- estado ----------
  var imagem = null;                       // { base64, tipo, largura, altura, kb }
  var ref = null;                          // { questaoId, rotulo }
  var filtro = 'todas';
  var respondidas = [];

  function minhas() { try { return JSON.parse(localStorage.getItem(CHAVE_MINHAS) || '[]'); } catch (e) { return []; } }
  function guardaMinha(item) { try { var m = minhas(); m.unshift(item); localStorage.setItem(CHAVE_MINHAS, JSON.stringify(m.slice(0, 30))); } catch (e) { /* sem armazenamento */ } }

  // ---------- exemplos do protótipo (só aparecem sem porteiro) ----------
  var EXEMPLOS = [
    { id: 'EX1', data: '08/11/2026', disciplina: 'ga', semana: 5, ref: 'Lista 6 · Q5a',
      pergunta: 'Na Lista 6, Q5, por que as retas são paralelas se as direções têm os sinais trocados?',
      resposta: 'Porque paralela é ter a mesma direção, e o sentido pode ser oposto. A direção de s é (−2, 2, −2), que é −2 vezes (1, −1, 1), a direção de r. Multiplicar por um número negativo só vira a seta para o outro lado: um trem indo e outro voltando no mesmo par de trilhos. Depois disso, teste um ponto: (1, 1, 1) é de r e não está em s, então são paralelas distintas.' },
    { id: 'EX2', data: '08/11/2026', disciplina: 'ga', semana: 5, ref: '',
      pergunta: 'Qual a diferença entre a distância de um ponto a um plano e de um ponto a uma reta?',
      resposta: 'Nas duas, o caminho mais curto chega fazendo 90°. Muda a conta. Até o plano: ponha o ponto na equação e divida o resto pelo tamanho do prego (vetor normal). Até a reta: monte o paralelogramo com a direção da reta e a seta até o ponto; a área dividida pela base dá a altura, que é a distância. Veja as ideias "Distância de ponto a plano" e "Distância de ponto a reta" na Semana 5.' },
    { id: 'EX3', data: '08/11/2026', disciplina: 'lp', semana: 1, ref: '',
      pergunta: 'No VisuAlg, por que o número aparece com um espaço antes quando uso escreval?',
      resposta: 'É o jeito do VisuAlg: ele escreve número com um espaço na frente (conferido no VisuAlg 3.0.7). Não é erro do seu programa.' }
  ];

  // ---------- print: colar, arrastar, anexar ----------
  function carregaImagem(arquivo) {
    if (!arquivo || !/^image\//.test(arquivo.type)) { msg('Esse arquivo não é imagem. Cole ou anexe um print (PNG ou JPG).', 'erro'); return; }
    if (arquivo.size > 15 * 1024 * 1024) { msg('Imagem grande demais (mais de 15 MB). Recorte só a questão e tente de novo.', 'erro'); return; }
    var url = URL.createObjectURL(arquivo);
    var img = new Image();
    img.onload = function () {
      var esc_ = Math.min(1, MAX_LADO / Math.max(img.width, img.height));
      var w = Math.round(img.width * esc_), h = Math.round(img.height * esc_);
      var cv = document.createElement('canvas'); cv.width = w; cv.height = h;
      var cx = cv.getContext('2d'); cx.fillStyle = '#fff'; cx.fillRect(0, 0, w, h); cx.drawImage(img, 0, 0, w, h);
      var dataUrl = cv.toDataURL('image/jpeg', 0.82);
      URL.revokeObjectURL(url);
      var b64 = dataUrl.split(',')[1];
      imagem = { base64: b64, tipo: 'image/jpeg', largura: w, altura: h, kb: Math.round(b64.length * 3 / 4 / 1024) };
      $('#duv-img').src = dataUrl;
      $('#duv-img-info').textContent = w + ' × ' + h + ' px · ' + imagem.kb + ' KB';
      $('#duv-print').hidden = false;
      msg('', '');
    };
    img.onerror = function () { URL.revokeObjectURL(url); msg('Não consegui ler essa imagem.', 'erro'); };
    img.src = url;
  }
  function tiraImagem() { imagem = null; $('#duv-print').hidden = true; $('#duv-img').removeAttribute('src'); }

  // ---------- referência a uma questão ou ideia ----------
  function mostraRef() {
    var el = $('#duv-ref');
    if (!ref) { el.hidden = true; el.innerHTML = ''; return; }
    el.hidden = false;
    el.innerHTML = '<span>Sobre: <b>' + esc(ref.rotulo) + '</b></span><button type="button" aria-label="Tirar a referência">×</button>';
    $('button', el).addEventListener('click', function () { ref = null; mostraRef(); });
  }
  function abrir(o) {
    var dlg = document.querySelector('dialog[open]'); if (dlg) dlg.close();
    if (o.disc) $('#duv-disc').value = o.disc;
    if (o.sem) $('#duv-sem').value = String(o.sem);
    ref = o.rotulo ? { questaoId: o.questaoId || '', rotulo: o.rotulo } : null;
    mostraRef();
    $('#duvidas').scrollIntoView({ behavior: 'smooth', block: 'start' });
    setTimeout(function () { $('#duv-texto').focus({ preventScroll: true }); }, 350);
  }
  function achaQuestao(id) {
    var achada = null;
    ['ga', 'lp'].forEach(function (d) { D.disc[d].questoes.forEach(function (q) { if (q.id === id) achada = { q: q, disc: d }; }); });
    return achada;
  }

  // ---------- envio ----------
  function msg(t, tipo) { var m = $('#duv-msg'); m.textContent = t; m.className = 'duv-msg ' + (tipo || ''); }
  function envia(e) {
    e.preventDefault();
    var texto = $('#duv-texto').value.trim();
    if (!texto && !imagem) { msg('Escreva a dúvida ou cole um print da questão.', 'erro'); return; }
    var pacote = {
      acao: 'enviar', disciplina: $('#duv-disc').value, semana: $('#duv-sem').value,
      questaoId: ref ? ref.questaoId : '', referencia: ref ? ref.rotulo : '',
      texto: texto.slice(0, MAX_TEXTO), imagem: imagem ? imagem.base64 : '', tipoImagem: imagem ? imagem.tipo : ''
    };
    var botao = $('#duv-enviar'); botao.disabled = true;
    var fim = function (id, prototipo) {
      guardaMinha({ id: id, data: new Date().toLocaleDateString('pt-BR'), disciplina: pacote.disciplina, semana: pacote.semana, texto: texto || '(print)', prototipo: !!prototipo });
      $('#duv-texto').value = ''; contaTexto(); tiraImagem(); ref = null; mostraRef();
      msg(prototipo ? 'Protótipo: nada foi enviado. No site de verdade, a dúvida vai para a planilha e ganha o código #' + id + '.'
        : 'Recebida! Código #' + id + '. A resposta aparece nesta página em até 1 dia.', 'ok');
      botao.disabled = false;
      desenhaMinhas();
    };
    if (!PORTEIRO) { setTimeout(function () { fim('P' + Date.now().toString(36).slice(-5).toUpperCase(), true); }, 400); return; }
    fetch(PORTEIRO, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(pacote) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (j && j.ok) fim(j.id, false);
        else { msg((j && j.erro) || 'Não foi possível enviar agora. Tente de novo em alguns minutos.', 'erro'); botao.disabled = false; }
      })
      .catch(function () { msg('Sem conexão com o tira-dúvidas agora. Tente de novo em alguns minutos.', 'erro'); botao.disabled = false; });
  }
  function contaTexto() { var n = $('#duv-texto').value.length; $('#duv-conta').textContent = n + '/' + MAX_TEXTO; }

  // ---------- lista ----------
  function carregaRespondidas() {
    if (!PORTEIRO) { respondidas = EXEMPLOS.map(function (x) { x.exemplo = true; return x; }); desenhaLista(); desenhaMinhas(); return; }
    $('#duv-itens').innerHTML = '<p class="duv-vazio">Carregando as respostas…</p>';
    fetch(PORTEIRO + '?acao=respondidas')
      .then(function (r) { return r.json(); })
      .then(function (j) { respondidas = (j && j.itens) || []; listaCarregada = true; desenhaLista(); desenhaMinhas(); consultaMinhas(); })
      .catch(function () { $('#duv-itens').innerHTML = '<p class="duv-vazio">Não consegui carregar as respostas agora.</p>'; });
  }
  function desenhaLista() {
    var busca = semAcento($('#duv-busca').value);
    var itens = respondidas.filter(function (x) {
      if (filtro !== 'todas' && x.disciplina !== filtro) return false;
      if (!busca) return true;
      return semAcento(x.pergunta + ' ' + x.resposta + ' ' + (x.ref || '')).indexOf(busca) >= 0;
    });
    $('#duv-total').textContent = respondidas.length ? itens.length + ' de ' + respondidas.length : '';
    if (!itens.length) { $('#duv-itens').innerHTML = '<p class="duv-vazio">' + (respondidas.length ? 'Nenhuma dúvida com esse filtro.' : 'Ainda não há dúvidas respondidas. Seja o primeiro a perguntar.') + '</p>'; return; }
    $('#duv-itens').innerHTML = itens.map(function (x) {
      return '<details class="duv-item"><summary><span class="duv-tag ' + x.disciplina + '">' + (NOME[x.disciplina] || '') + (x.semana ? ' · Semana ' + esc(x.semana) : '') + (x.ref ? ' · ' + esc(x.ref) : '') + '</span>' +
        '<span class="duv-perg">' + esc(x.pergunta) + '</span></summary>' +
        '<div class="duv-resp">' + txt(x.resposta) + '</div>' +
        '<p class="duv-meta">#' + esc(x.id) + ' · respondida em ' + esc(x.data) + (x.exemplo ? ' · <span class="stamp">exemplo do protótipo</span>' : '') + '</p></details>';
    }).join('');
  }
  // ---------- suas dúvidas: aguardando, não respondida (com o motivo) ou respondida ----------
  var listaCarregada = false;
  var situacoes = {};                      // id -> { status, motivo }, perguntado ao porteiro
  var avisoRespondidas = null;             // as suas que já saíram na lista: aparecem uma vez e saem da memória
  function tiraMinha(id) { try { localStorage.setItem(CHAVE_MINHAS, JSON.stringify(minhas().filter(function (m) { return m.id !== id; }))); } catch (e) { /* sem armazenamento */ } }
  function consultaMinhas() {
    if (!PORTEIRO) return;
    minhas().filter(function (m) { return !m.prototipo; }).slice(0, 5).forEach(function (m) {
      fetch(PORTEIRO + '?acao=status&id=' + encodeURIComponent(m.id))
        .then(function (r) { return r.json(); })
        .then(function (j) { if (j && j.ok) { situacoes[m.id] = j; desenhaMinhas(); } })
        .catch(function () { /* sem resposta do porteiro: fica como aguardando */ });
    });
  }
  function resumo(m) { var t = String(m.texto || ''); return esc(t.slice(0, 90)) + (t.length > 90 ? '…' : ''); }
  function desenhaMinhas() {
    var feitas = {}; respondidas.forEach(function (x) { feitas[x.id] = true; });
    if (avisoRespondidas === null && listaCarregada) {
      avisoRespondidas = minhas().filter(function (m) { return feitas[m.id]; });
      avisoRespondidas.forEach(function (m) { tiraMinha(m.id); });
    }
    var blocos = (avisoRespondidas || []).map(function (m) {
      return '<div class="duv-pend duv-ok"><span class="duv-relogio" aria-hidden="true">✓</span><div><b>#' + esc(m.id) + ' · Respondida</b>' +
        '<small>Veja em "Dúvidas respondidas", logo abaixo. Este aviso some sozinho.</small></div></div>';
    });
    minhas().slice(0, 5).forEach(function (m) {
      var s = situacoes[m.id] || {};
      if (s.motivo) {
        blocos.push('<div class="duv-pend duv-motivo"><span class="duv-relogio" aria-hidden="true">!</span><div><b>#' + esc(m.id) + ' · Não respondida</b>' +
          '<small>' + esc(s.motivo) + '</small>' +
          '<span class="duv-pend-acoes"><button type="button" class="ghost" data-minha="de-novo" data-id="' + esc(m.id) + '">Perguntar de novo</button>' +
          '<button type="button" class="ghost" data-minha="dispensar" data-id="' + esc(m.id) + '">Dispensar</button></span></div></div>');
      } else if (!feitas[m.id]) {
        blocos.push('<div class="duv-pend"><span class="duv-relogio" aria-hidden="true">◷</span><div>#' + esc(m.id) + ' · ' + resumo(m) +
          '<small>Aguardando. A resposta aparece aqui em até 1 dia.</small></div>' + (m.prototipo ? '<span class="stamp">protótipo</span>' : '') + '</div>');
      }
    });
    $('#duv-minhas').innerHTML = blocos.length ? '<p class="duv-minhas-tit">Suas dúvidas</p>' + blocos.join('') : '';
  }
  function acaoMinha(e) {
    var b = e.target.closest && e.target.closest('[data-minha]');
    if (!b) return;
    var m = minhas().filter(function (x) { return x.id === b.dataset.id; })[0];
    tiraMinha(b.dataset.id);
    desenhaMinhas();
    if (b.dataset.minha === 'de-novo') {
      abrir({ disc: m && m.disciplina, sem: m && m.semana });
      if (m && m.texto && m.texto !== '(print)') { $('#duv-texto').value = m.texto; contaTexto(); }
    }
  }

  // ---------- liga ----------
  function liga() {
    if (!$('#duvidas')) return;
    var sem = $('#duv-sem');
    sem.innerHTML = '<option value="">Não sei</option>' + [1, 2, 3, 4, 5, 6].map(function (n) { return '<option value="' + n + '">Semana ' + n + '</option>'; }).join('');
    if (!PORTEIRO) $('#duv-modo').hidden = false;
    $('#duv-form').addEventListener('submit', envia);
    $('#duv-texto').addEventListener('input', contaTexto);
    $('#duv-texto').addEventListener('paste', function (e) {
      var itens = (e.clipboardData && e.clipboardData.items) || [];
      for (var i = 0; i < itens.length; i++) {
        if (itens[i].kind === 'file' && /^image\//.test(itens[i].type)) { e.preventDefault(); carregaImagem(itens[i].getAsFile()); return; }
      }
    });
    var caixa = $('#duv-caixa');
    ['dragenter', 'dragover'].forEach(function (ev) { caixa.addEventListener(ev, function (e) { e.preventDefault(); caixa.classList.add('arrastando'); }); });
    ['dragleave', 'drop'].forEach(function (ev) { caixa.addEventListener(ev, function () { caixa.classList.remove('arrastando'); }); });
    caixa.addEventListener('drop', function (e) { e.preventDefault(); var f = e.dataTransfer && e.dataTransfer.files[0]; if (f) carregaImagem(f); });
    $('#duv-arquivo').addEventListener('change', function () { if (this.files[0]) carregaImagem(this.files[0]); this.value = ''; });
    $('#duv-tira').addEventListener('click', tiraImagem);
    $('#duv-busca').addEventListener('input', desenhaLista);
    $('#duv-minhas').addEventListener('click', acaoMinha);
    $$('#duv-filtros button').forEach(function (b) {
      b.addEventListener('click', function () { filtro = b.dataset.f; $$('#duv-filtros button').forEach(function (x) { x.classList.toggle('active', x === b); }); desenhaLista(); });
    });
    document.addEventListener('click', function (e) {
      var b = e.target.closest && e.target.closest('[data-duvida-q],[data-duvida-ideia]');
      if (!b) return;
      if (b.dataset.duvidaQ) {
        var a = achaQuestao(b.dataset.duvidaQ);
        if (a) abrir({ disc: a.disc, sem: a.q.semana, questaoId: a.q.id, rotulo: a.q.origem });
      } else {
        abrir({ disc: b.dataset.duvidaDisc, sem: b.dataset.duvidaSem, questaoId: '', rotulo: 'Ideia: ' + b.dataset.duvidaIdeia });
      }
    });
    contaTexto();
    carregaRespondidas();
  }
  window.NucleoDuvidas = { abrir: abrir, carregaImagem: carregaImagem, estado: function () { return { imagem: imagem, ref: ref }; } };
  liga();
})();
