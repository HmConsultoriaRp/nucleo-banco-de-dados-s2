/* Interpretador de um subconjunto do VisuAlg 3.0, com teste de mesa.
   Uso: VisuAlg.executar(codigo, entradas, opts) -> { saida, passos, erro, ordem, decl, lidas, espera, recusada }
   opts.guiada (laboratório): a resposta aparece na tela e o leia sem resposta vira res.espera.
   Cada passo: { linha, nota, vars: {nome: texto}, saida } */
(function (root) {
  'use strict';

  var KW = ['algoritmo', 'var', 'inicio', 'fimalgoritmo', 'inteiro', 'real', 'caractere', 'caracter',
    'literal', 'logico', 'vetor', 'de', 'leia', 'escreva', 'escreval', 'se', 'entao', 'senao', 'fimse',
    'escolha', 'caso', 'outrocaso', 'fimescolha', 'para', 'ate', 'passo', 'faca', 'fimpara', 'enquanto',
    'fimenquanto', 'repita', 'fimrepita', 'interrompa', 'e', 'ou', 'nao', 'xou', 'div', 'mod',
    'verdadeiro', 'falso', 'limpatela', 'pausa'];
  var KWSET = {};
  KW.forEach(function (k) { KWSET[k] = true; });
  var ACENTO = { 'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'é': 'e', 'ê': 'e', 'í': 'i', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ú': 'u', 'ç': 'c' };
  function semAcento(s) { return s.replace(/[áàâãéêíóôõúç]/g, function (c) { return ACENTO[c]; }); }

  function ErroVA(msg, linha) { this.message = msg; this.linha = linha || 0; }

  // ---------- analisador léxico ----------
  function lex(src) {
    var toks = [], i = 0, linha = 1, n = src.length;
    while (i < n) {
      var c = src[i];
      if (c === '\n') { linha++; i++; continue; }
      // ";" no fim da linha é aceito e ignorado (o manual do VisuAlg usa "var x: inteiro;")
      if (c === ' ' || c === '\t' || c === '\r' || c === ';') { i++; continue; }
      if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; continue; }
      if (c === '"') {
        var j = i + 1;
        while (j < n && src[j] !== '"' && src[j] !== '\n') j++;
        if (src[j] !== '"') throw new ErroVA('texto sem aspas de fechamento', linha);
        toks.push({ t: 'str', v: src.slice(i + 1, j), linha: linha });
        i = j + 1; continue;
      }
      if (/[0-9]/.test(c)) {
        var k = i;
        while (k < n && /[0-9]/.test(src[k])) k++;
        if (src[k] === '.' && /[0-9]/.test(src[k + 1] || '')) {
          k++;
          while (k < n && /[0-9]/.test(src[k])) k++;
          toks.push({ t: 'num', v: parseFloat(src.slice(i, k)), real: true, linha: linha });
        } else {
          toks.push({ t: 'num', v: parseInt(src.slice(i, k), 10), real: false, linha: linha });
        }
        i = k; continue;
      }
      if (/[A-Za-z_À-ÿ]/.test(c)) {
        var m = i;
        while (m < n && /[A-Za-z0-9_À-ÿ]/.test(src[m])) m++;
        var raw = src.slice(i, m), low = semAcento(raw.toLowerCase());
        toks.push(KWSET[low] ? { t: 'kw', v: low, linha: linha } : { t: 'id', v: low, raw: raw, linha: linha });
        i = m; continue;
      }
      if (c === '←') { toks.push({ t: 'op', v: '<-', linha: linha }); i++; continue; }
      var dois = src.substr(i, 2);
      if (dois === '<-' || dois === ':=' || dois === '<=' || dois === '>=' || dois === '<>' || dois === '..') {
        toks.push({ t: 'op', v: dois === ':=' ? '<-' : dois, linha: linha }); i += 2; continue;
      }
      // "." sozinho: campo de registro (p[i].nome); ".." já foi tratado acima
      if ('+-*/\\^%()[],:=<>.'.indexOf(c) >= 0) { toks.push({ t: 'op', v: c, linha: linha }); i++; continue; }
      throw new ErroVA('símbolo inesperado: ' + c, linha);
    }
    toks.push({ t: 'eof', v: '', linha: linha });
    return toks;
  }

  // ---------- analisador sintático ----------
  function parse(toks) {
    var p = 0;
    // tipos registro declarados em "tipo Nome = registro ... fimregistro" (antes do var).
    // "tipo", "registro" e "fimregistro" são reconhecidos só nessa posição, para não quebrar
    // programas que usam essas palavras como nome de variável.
    var tipos = {};
    function peek() { return toks[p]; }
    function next() { return toks[p++]; }
    function isKw(v) { return peek().t === 'kw' && peek().v === v; }
    function isOp(v) { return peek().t === 'op' && peek().v === v; }
    function mostra(t) { return t.t === 'eof' ? 'fim do código' : String(t.v); }
    function expectKw(v) {
      var t = next();
      if (!(t.t === 'kw' && t.v === v)) throw new ErroVA('esperava "' + v + '" e encontrei "' + mostra(t) + '"', t.linha);
      return t;
    }
    function expectOp(v) {
      var t = next();
      if (!(t.t === 'op' && t.v === v)) throw new ErroVA('esperava "' + v + '" e encontrei "' + mostra(t) + '"', t.linha);
      return t;
    }
    function normTipo(v) { return (v === 'caracter' || v === 'literal') ? 'caractere' : v; }
    function parseTipo() {
      var t = next();
      if (t.t === 'kw' && ['inteiro', 'real', 'caractere', 'caracter', 'literal', 'logico'].indexOf(t.v) >= 0) return { base: normTipo(t.v) };
      if (t.t === 'id' && tipos[t.v]) return { base: 'registro', reg: tipos[t.v] };
      if (t.t === 'kw' && t.v === 'vetor') {
        expectOp('[');
        var dims = [];
        for (;;) {
          var a = next(); expectOp('..'); var b = next();
          if (a.t !== 'num' || b.t !== 'num') throw new ErroVA('limites do vetor precisam ser números inteiros', a.linha);
          dims.push([a.v, b.v]);
          if (isOp(',')) { next(); continue; }
          break;
        }
        expectOp(']'); expectKw('de');
        var bt = next();
        if (bt.t === 'id' && tipos[bt.v]) return { base: 'registro', reg: tipos[bt.v], dims: dims };
        if (bt.t !== 'kw' || ['inteiro', 'real', 'caractere', 'caracter', 'literal', 'logico'].indexOf(bt.v) < 0) throw new ErroVA('tipo do vetor desconhecido', bt.linha);
        return { base: normTipo(bt.v), dims: dims };
      }
      throw new ErroVA('tipo desconhecido: ' + mostra(t), t.linha);
    }

    expectKw('algoritmo');
    var nome = '';
    if (peek().t === 'str') nome = next().v;
    // tipo Produto = registro / campos / fimregistro (aceita também "tipo" sozinho na linha)
    while (peek().t === 'id' && peek().v === 'tipo') {
      next();
      while (peek().t === 'id' && toks[p + 1] && toks[p + 1].t === 'op' && toks[p + 1].v === '=') {
        var tn = next(); next();
        var rg = next();
        if (!(rg.t === 'id' && rg.v === 'registro')) throw new ErroVA('depois de "' + tn.raw + ' =" vem "registro"', rg.linha);
        if (tipos[tn.v]) throw new ErroVA('tipo declarado duas vezes: ' + tn.raw, tn.linha);
        var campos = {}, ordemC = [];
        while (!(peek().t === 'id' && peek().v === 'fimregistro')) {
          if (peek().t === 'eof' || (peek().t === 'kw' && (peek().v === 'var' || peek().v === 'inicio'))) throw new ErroVA('faltou "fimregistro" no tipo ' + tn.raw, peek().linha);
          var cn = [next()];
          if (cn[0].t !== 'id') throw new ErroVA('nome de campo inválido: ' + mostra(cn[0]), cn[0].linha);
          while (isOp(',')) {
            next();
            var c2 = next();
            if (c2.t !== 'id') throw new ErroVA('nome de campo inválido: ' + mostra(c2), c2.linha);
            cn.push(c2);
          }
          expectOp(':');
          var ct = parseTipo();
          if (ct.base === 'registro' || ct.dims) throw new ErroVA('campo de registro precisa ser inteiro, real, caractere ou logico', cn[0].linha);
          cn.forEach(function (tk) {
            if (campos[tk.v]) throw new ErroVA('campo declarado duas vezes: ' + tk.raw, tk.linha);
            campos[tk.v] = { tipo: ct, raw: tk.raw };
            ordemC.push(tk.v);
          });
        }
        next();
        tipos[tn.v] = { nome: tn.raw, campos: campos, ordem: ordemC };
      }
    }
    var decl = {}, ordem = [];
    if (isKw('var')) {
      next();
      while (peek().t === 'id') {
        var nomes = [next()];
        while (isOp(',')) {
          next();
          var t2 = next();
          if (t2.t !== 'id') throw new ErroVA('nome de variável inválido: ' + mostra(t2), t2.linha);
          nomes.push(t2);
        }
        expectOp(':');
        var tipo = parseTipo();
        nomes.forEach(function (tk) {
          if (decl[tk.v]) throw new ErroVA('variável declarada duas vezes: ' + tk.raw, tk.linha);
          decl[tk.v] = { tipo: tipo, raw: tk.raw, linha: tk.linha };
          ordem.push(tk.v);
        });
      }
    }
    var ini = expectKw('inicio');
    var corpo = bloco(['fimalgoritmo']);
    var fim = expectKw('fimalgoritmo');
    return { nome: nome, decl: decl, ordem: ordem, corpo: corpo, linhaInicio: ini.linha, linhaFim: fim.linha, tipos: tipos };

    function bloco(fins) {
      var lista = [];
      while (!(peek().t === 'kw' && fins.indexOf(peek().v) >= 0)) {
        if (peek().t === 'eof') throw new ErroVA('faltou "' + fins[0] + '"', peek().linha);
        lista.push(comando());
      }
      return lista;
    }
    function lval() {
      var t = next();
      if (t.t !== 'id') throw new ErroVA('leia precisa de uma variável', t.linha);
      var idx = null;
      if (isOp('[')) { next(); idx = [expr()]; while (isOp(',')) { next(); idx.push(expr()); } expectOp(']'); }
      return { nome: t.v, idx: idx, campo: campoOpc(), linha: t.linha };
    }
    // ".campo" depois do nome (ou do índice) de um registro
    function campoOpc() {
      if (!isOp('.')) return null;
      next();
      var c = next();
      if (c.t !== 'id') throw new ErroVA('depois do ponto vem o nome do campo do registro', c.linha);
      return c.v;
    }
    // argumento do escreva com formatação opcional: x:5 (largura) ou x:5:2 (largura e casas decimais)
    function argEscreva() {
      var e = expr();
      if (!isOp(':')) return e;
      next();
      var w = next();
      if (w.t !== 'num' || w.real) throw new ErroVA('depois de ":" vem a largura, um número inteiro (ex.: x:5:2)', w.linha);
      var f = { k: 'formato', e: e, larg: w.v, dec: null };
      if (isOp(':')) {
        next();
        var d = next();
        if (d.t !== 'num' || d.real) throw new ErroVA('depois da largura vem o número de casas decimais, inteiro (ex.: x:5:2)', d.linha);
        f.dec = d.v;
      }
      return f;
    }
    function valorCaso() {
      var a = expr();
      if (isKw('ate')) { next(); return { faixa: [a, expr()] }; }
      return { v: a };
    }
    function comando() {
      var t = peek(), linha = t.linha;
      if (t.t === 'id') {
        next();
        var idx = null;
        if (isOp('[')) { next(); idx = [expr()]; while (isOp(',')) { next(); idx.push(expr()); } expectOp(']'); }
        var campo = campoOpc();
        if (!isOp('<-')) throw new ErroVA('esperava "<-" depois de "' + t.raw + '"', linha);
        next();
        return { k: 'atrib', nome: t.v, idx: idx, campo: campo, e: expr(), linha: linha };
      }
      if (t.t !== 'kw') throw new ErroVA('comando inesperado: ' + mostra(t), linha);
      switch (t.v) {
        case 'leia': {
          next(); expectOp('(');
          var alvos = [lval()];
          while (isOp(',')) { next(); alvos.push(lval()); }
          expectOp(')');
          return { k: 'leia', alvos: alvos, linha: linha };
        }
        case 'escreva': case 'escreval': {
          next();
          var args = [];
          if (isOp('(')) {
            next();
            if (!isOp(')')) { args.push(argEscreva()); while (isOp(',')) { next(); args.push(argEscreva()); } }
            expectOp(')');
          }
          return { k: 'escreva', nl: t.v === 'escreval', args: args, linha: linha };
        }
        case 'se': {
          next();
          var c = expr(); expectKw('entao');
          var entao = bloco(['senao', 'fimse']), senao = null, linhaSenao = null;
          if (isKw('senao')) { linhaSenao = next().linha; senao = bloco(['fimse']); }
          expectKw('fimse');
          return { k: 'se', c: c, entao: entao, senao: senao, linha: linha, linhaSenao: linhaSenao };
        }
        case 'escolha': {
          next();
          var e = expr();
          if (isKw('faca')) next();
          var casos = [], outro = null, outroLinha = null;
          while (isKw('caso')) {
            var cl = next().linha, vals = [valorCaso()];
            while (isOp(',')) { next(); vals.push(valorCaso()); }
            casos.push({ vals: vals, corpo: bloco(['caso', 'outrocaso', 'fimescolha']), linha: cl });
          }
          if (isKw('outrocaso')) { outroLinha = next().linha; outro = bloco(['fimescolha']); }
          expectKw('fimescolha');
          return { k: 'escolha', e: e, casos: casos, outro: outro, outroLinha: outroLinha, linha: linha };
        }
        case 'para': {
          next();
          var v = next();
          if (v.t !== 'id') throw new ErroVA('"para" precisa de uma variável', linha);
          expectKw('de'); var a = expr(); expectKw('ate'); var b = expr();
          var passo = null;
          if (isKw('passo')) { next(); passo = expr(); }
          expectKw('faca');
          var corpoP = bloco(['fimpara']);
          var fl = expectKw('fimpara').linha;
          return { k: 'para', v: v.v, ini: a, fim: b, passo: passo, corpo: corpoP, linha: linha, fimLinha: fl };
        }
        case 'enquanto': {
          next();
          var ce = expr(); expectKw('faca');
          var corpoE = bloco(['fimenquanto']);
          var fe = expectKw('fimenquanto').linha;
          return { k: 'enquanto', c: ce, corpo: corpoE, linha: linha, fimLinha: fe };
        }
        case 'repita': {
          next();
          var corpoR = bloco(['ate', 'fimrepita']);
          var tl = next(), cr = null;
          if (tl.v === 'ate') cr = expr();
          return { k: 'repita', c: cr, corpo: corpoR, linha: linha, ateLinha: tl.linha };
        }
        case 'interrompa': next(); return { k: 'interrompa', linha: linha };
        case 'limpatela': case 'pausa': next(); return { k: 'nada', linha: linha };
      }
      throw new ErroVA('comando inesperado: ' + mostra(t), linha);
    }
    // precedência: ou/xou < e < nao < relacionais < + - < * / \ div mod < unário < ^
    function expr() { return ou(); }
    function ou() {
      var a = e_();
      while (isKw('ou') || isKw('xou')) { var op = next().v; a = { k: 'bin', op: op, a: a, b: e_() }; }
      return a;
    }
    function e_() {
      var a = nao();
      while (isKw('e')) { next(); a = { k: 'bin', op: 'e', a: a, b: nao() }; }
      return a;
    }
    function nao() {
      if (isKw('nao')) { var l = next().linha; return { k: 'un', op: 'nao', a: nao(), linha: l }; }
      return rel();
    }
    function rel() {
      var a = soma();
      if (peek().t === 'op' && ['=', '<>', '<', '>', '<=', '>='].indexOf(peek().v) >= 0) {
        var t = next();
        a = { k: 'bin', op: t.v, a: a, b: soma(), linha: t.linha };
      }
      return a;
    }
    function soma() {
      var a = mult();
      while (isOp('+') || isOp('-')) { var t = next(); a = { k: 'bin', op: t.v, a: a, b: mult(), linha: t.linha }; }
      return a;
    }
    function mult() {
      var a = unario();
      while (isOp('*') || isOp('/') || isOp('\\') || isOp('%') || isKw('div') || isKw('mod')) {
        var t = next(), op = t.v;
        if (op === '%') op = 'mod';
        if (op === '\\') op = 'div';
        a = { k: 'bin', op: op, a: a, b: unario(), linha: t.linha };
      }
      return a;
    }
    function unario() {
      if (isOp('-')) { var l = next().linha; return { k: 'un', op: '-', a: unario(), linha: l }; }
      if (isOp('+')) { next(); return unario(); }
      return pot();
    }
    function pot() {
      var a = prim();
      if (isOp('^')) { var t = next(); return { k: 'bin', op: '^', a: a, b: unario(), linha: t.linha }; }
      return a;
    }
    function prim() {
      var t = next();
      if (t.t === 'num') return { k: 'num', v: t.v, real: t.real };
      if (t.t === 'str') return { k: 'str', v: t.v };
      if (t.t === 'kw' && (t.v === 'verdadeiro' || t.v === 'falso')) return { k: 'log', v: t.v === 'verdadeiro' };
      if (t.t === 'op' && t.v === '(') { var e = expr(); expectOp(')'); return e; }
      if (t.t === 'id') {
        if (isOp('(')) {
          next();
          var args = [];
          if (!isOp(')')) { args.push(expr()); while (isOp(',')) { next(); args.push(expr()); } }
          expectOp(')');
          return { k: 'fn', nome: t.v, raw: t.raw, args: args, linha: t.linha };
        }
        var idx = null;
        if (isOp('[')) {
          next();
          idx = [expr()];
          while (isOp(',')) { next(); idx.push(expr()); }
          expectOp(']');
        }
        return { k: 'var', nome: t.v, idx: idx, campo: campoOpc(), linha: t.linha };
      }
      throw new ErroVA('expressão inválida perto de "' + mostra(t) + '"', t.linha);
    }
  }

  // ---------- execução ----------
  function fmtReal(v) {
    if (Number.isInteger(v)) return String(v);
    var s = Number(v.toFixed(10)).toString();
    return s;
  }
  function fmt(val) {
    if (val.tipo === 'i') return String(val.v);
    if (val.tipo === 'r') return fmtReal(val.v);
    if (val.tipo === 'b') return val.v ? 'VERDADEIRO' : 'FALSO';
    return val.v;
  }
  var NOME_TIPO = { i: 'inteiro', r: 'real', s: 'caractere', b: 'lógico' };

  // escreva(x:larg:dec). Medido no VisuAlg 3.0.7 real (02/11/2026): arredonda (7,1666 -> 7.17) e
  // completa com espaços à esquerda até a largura, SEM o espaço extra dos números ("prova: 10.00").
  // Não medido (hipótese): texto também é alinhado à direita; inteiro com :dec ganha casas decimais;
  // o meio exato arredonda para longe do zero (-7,25 -> -7.3).
  function formatado(v, larg, dec) {
    var t;
    if (dec !== null && (v.tipo === 'i' || v.tipo === 'r')) {
      var p = Math.pow(10, dec), sinal = v.v < 0 ? -1 : 1;
      t = (sinal * Math.round(Math.abs(v.v) * p + 1e-9) / p).toFixed(dec);
    } else t = fmt(v);
    while (t.length < larg) t = ' ' + t;
    return t;
  }

  // Converte o texto digitado para o tipo da variável. Devolve { val } ou { msg }.
  function lerEntrada(txt, base) {
    txt = String(txt);
    var t = txt.trim();
    if (base === 'inteiro') {
      if (!/^[+-]?\d+$/.test(t)) return { msg: 'a entrada "' + txt + '" não é um número inteiro' };
      return { val: { tipo: 'i', v: parseInt(t, 10) } };
    }
    if (base === 'real') {
      var tt = t.replace(',', '.');
      if (!/^[+-]?(\d+\.?\d*|\.\d+)$/.test(tt)) return { msg: 'a entrada "' + txt + '" não é um número' };
      return { val: { tipo: 'r', v: parseFloat(tt) } };
    }
    if (base === 'logico') {
      var l = semAcento(t.toLowerCase());
      if (l === 'verdadeiro' || l === 'v') return { val: { tipo: 'b', v: true } };
      if (l === 'falso' || l === 'f') return { val: { tipo: 'b', v: false } };
      return { msg: 'a entrada "' + txt + '" não é lógica (use VERDADEIRO ou FALSO)' };
    }
    return { val: { tipo: 's', v: txt } };
  }
  function validarEntrada(txt, base) { var r = lerEntrada(txt, base); return r.msg || null; }

  function executar(codigo, entradas, opts) {
    opts = opts || {};
    var MAX = opts.maxPassos || 5000;
    var res = { saida: '', passos: [], erro: null, ordem: [], decl: {}, nomes: [], lidas: [], espera: null, recusada: null };
    // guiada: modo do laboratório. A resposta digitada aparece na tela depois da pergunta
    // e, quando falta entrada, o programa registra em que leia parou (res.espera).
    var guiada = !!opts.guiada;
    var prog;
    try { prog = parse(lex(codigo)); } catch (e) {
      res.erro = { linha: e.linha || 0, msg: e.message || String(e) };
      return res;
    }
    res.ordem = prog.ordem; res.decl = prog.decl;
    res.nomes = prog.ordem.map(function (n) { return prog.decl[n].raw; });
    var mem = {};
    function inicial(base) {
      if (base === 'inteiro') return { tipo: 'i', v: 0 };
      if (base === 'real') return { tipo: 'r', v: 0 };
      if (base === 'logico') return { tipo: 'b', v: false };
      return { tipo: 's', v: '' };
    }
    // valor inicial de uma variável (ou de uma posição de vetor): registro ganha um valor por campo
    function novo(tipo) {
      if (tipo.base !== 'registro') return inicial(tipo.base);
      var c = {};
      tipo.reg.ordem.forEach(function (k) { c[k] = inicial(tipo.reg.campos[k].tipo.base); });
      return { reg: tipo.reg, campos: c };
    }
    prog.ordem.forEach(function (n) {
      var d = prog.decl[n];
      if (d.tipo.dims) {
        var tam = 1;
        d.tipo.dims.forEach(function (dm) { tam *= (dm[1] - dm[0] + 1); });
        var dados = [];
        for (var i = 0; i < tam; i++) dados.push(novo(d.tipo));
        mem[n] = { vetor: true, dims: d.tipo.dims, dados: dados };
      } else mem[n] = novo(d.tipo);
    });
    var fila = (entradas || []).map(String);
    var saida = '';
    var INTERROMPA = { interrompa: true };

    function txtReg(v) {
      return '{' + v.reg.ordem.map(function (k) { return v.reg.campos[k].raw + ': ' + txtVar(v.campos[k]); }).join(', ') + '}';
    }
    function txtVar(v) {
      if (v && v.vetor) return '[' + v.dados.map(function (x) { return x.reg ? txtReg(x) : fmt(x); }).join(', ') + ']';
      if (v && v.reg) return txtReg(v);
      return v.tipo === 's' ? '"' + v.v + '"' : fmt(v);
    }
    function snap() {
      var o = {};
      prog.ordem.forEach(function (n) { o[prog.decl[n].raw] = txtVar(mem[n]); });
      return o;
    }
    function passo(linha, nota) {
      if (res.passos.length >= MAX) throw new ErroVA('passei de ' + MAX + ' passos: parece um laço que não termina', linha);
      res.passos.push({ linha: linha, nota: nota || '', vars: snap(), saida: saida });
    }
    function decl(nome, linha) {
      var d = prog.decl[nome];
      if (!d) throw new ErroVA('variável não declarada: ' + nome, linha);
      return d;
    }
    function posicao(nome, idx, linha) {
      var cel = mem[nome], d = decl(nome, linha);
      if (!cel.vetor) throw new ErroVA(d.raw + ' não é vetor', linha);
      if (idx.length !== cel.dims.length) throw new ErroVA('número de índices errado em ' + d.raw, linha);
      var off = 0, mult = 1;
      for (var i = cel.dims.length - 1; i >= 0; i--) {
        var iv = ev(idx[i]);
        if (iv.tipo !== 'i') throw new ErroVA('índice de vetor precisa ser inteiro', linha);
        var lo = cel.dims[i][0], hi = cel.dims[i][1];
        if (iv.v < lo || iv.v > hi) throw new ErroVA('índice ' + iv.v + ' fora do vetor ' + d.raw + '[' + lo + '..' + hi + ']', linha);
        off += (iv.v - lo) * mult;
        mult *= (hi - lo + 1);
      }
      return off;
    }
    // tipo base do alvo: o da variável ou, com .campo, o do campo do registro
    function baseDe(nome, campo, linha) {
      var d = decl(nome, linha);
      if (!campo) return d.tipo.base;
      if (d.tipo.base !== 'registro') throw new ErroVA(d.raw + ' não é registro: não tem o campo .' + campo, linha);
      var c = d.tipo.reg.campos[campo];
      if (!c) throw new ErroVA('o registro ' + d.tipo.reg.nome + ' não tem o campo ' + campo, linha);
      return c.tipo.base;
    }
    function ler(nome, idx, linha, campo) {
      var d = decl(nome, linha), cel = mem[nome];
      var alvo;
      if (idx) alvo = cel.dados[posicao(nome, idx, linha)];
      else {
        if (cel.vetor) throw new ErroVA('use ' + d.raw + '[índice] para ler uma posição do vetor', linha);
        alvo = cel;
      }
      if (campo) { baseDe(nome, campo, linha); return alvo.campos[campo]; }
      if (alvo.reg) throw new ErroVA('use ' + d.raw + (idx ? '[índice]' : '') + '.campo para usar um campo do registro', linha);
      return alvo;
    }
    function converte(val, base, linha, nome) {
      if (base === 'inteiro') {
        if (val.tipo === 'i') return val;
        if (val.tipo === 'r') throw new ErroVA('tipos incompatíveis: valor real em variável inteira (' + nome + ')', linha);
      } else if (base === 'real') {
        if (val.tipo === 'i' || val.tipo === 'r') return { tipo: 'r', v: val.v };
      } else if (base === 'caractere') {
        if (val.tipo === 's') return val;
      } else if (base === 'logico') {
        if (val.tipo === 'b') return val;
      }
      throw new ErroVA('tipos incompatíveis: ' + NOME_TIPO[val.tipo] + ' em variável ' + base + ' (' + nome + ')', linha);
    }
    function atribuir(nome, idx, val, linha, campo) {
      var d = decl(nome, linha), cel = mem[nome];
      if (campo) {
        var vc = converte(val, baseDe(nome, campo, linha), linha, d.raw + '.' + d.tipo.reg.campos[campo].raw);
        if (!idx && cel.vetor) throw new ErroVA('use ' + d.raw + '[índice].' + campo + ' para gravar num registro do vetor', linha);
        (idx ? cel.dados[posicao(nome, idx, linha)] : cel).campos[campo] = vc;
        return;
      }
      if (d.tipo.base === 'registro') throw new ErroVA('grave campo por campo: ' + d.raw + (idx ? '[índice]' : '') + '.campo <- valor', linha);
      var v = converte(val, d.tipo.base, linha, d.raw);
      if (idx) cel.dados[posicao(nome, idx, linha)] = v;
      else {
        if (cel.vetor) throw new ErroVA('não dá para atribuir a um vetor inteiro de uma vez (' + d.raw + ')', linha);
        mem[nome] = v;
      }
    }
    function nomeAlvo(nome, idx, campo) {
      var d = prog.decl[nome], raw = d ? d.raw : nome;
      if (idx) raw += '[' + idx.map(function (e) { return fmt(ev(e)); }).join(',') + ']';
      if (campo) raw += '.' + (d && d.tipo.reg && d.tipo.reg.campos[campo] ? d.tipo.reg.campos[campo].raw : campo);
      return raw;
    }
    function entrada(txt, base, linha) {
      var r = lerEntrada(txt, base);
      if (r.msg) throw new ErroVA(r.msg, linha);
      return r.val;
    }
    // A pergunta é o que o programa escreveu desde o leia anterior (a última linha com texto).
    var marcaLeia = 0;
    function perguntaAtual() {
      var partes = saida.slice(marcaLeia).split('\n');
      for (var k = partes.length - 1; k >= 0; k--) if (partes[k].trim()) return partes[k].trim();
      return '';
    }
    function num(a, linha, op) {
      if (a.tipo !== 'i' && a.tipo !== 'r') throw new ErroVA('a operação "' + op + '" precisa de números, recebeu ' + NOME_TIPO[a.tipo], linha);
    }
    function logi(a, linha, op) {
      if (a.tipo !== 'b') throw new ErroVA('"' + op + '" precisa de valor lógico, recebeu ' + NOME_TIPO[a.tipo], linha);
    }
    function compara(a, b, linha) {
      if ((a.tipo === 'i' || a.tipo === 'r') && (b.tipo === 'i' || b.tipo === 'r')) return a.v < b.v ? -1 : a.v > b.v ? 1 : 0;
      // Manual do VisuAlg: comparações entre textos não diferenciam maiúsculas de minúsculas ("ABC" = "abc")
      if (a.tipo === 's' && b.tipo === 's') {
        var x = a.v.toLowerCase(), y = b.v.toLowerCase();
        return x < y ? -1 : x > y ? 1 : 0;
      }
      if (a.tipo === 'b' && b.tipo === 'b') return a.v === b.v ? 0 : (a.v ? 1 : -1);
      throw new ErroVA('não dá para comparar ' + NOME_TIPO[a.tipo] + ' com ' + NOME_TIPO[b.tipo], linha);
    }
    function bin(e) {
      var a = ev(e.a), b = ev(e.b), op = e.op, L = e.linha;
      switch (op) {
        case '+':
          if (a.tipo === 's' && b.tipo === 's') return { tipo: 's', v: a.v + b.v };
          num(a, L, op); num(b, L, op);
          return { tipo: a.tipo === 'r' || b.tipo === 'r' ? 'r' : 'i', v: a.v + b.v };
        case '-': case '*':
          num(a, L, op); num(b, L, op);
          return { tipo: a.tipo === 'r' || b.tipo === 'r' ? 'r' : 'i', v: op === '-' ? a.v - b.v : a.v * b.v };
        case '/':
          num(a, L, op); num(b, L, op);
          if (b.v === 0) throw new ErroVA('divisão por zero', L);
          return { tipo: 'r', v: a.v / b.v };
        case 'div': case 'mod':
          num(a, L, op); num(b, L, op);
          if (!Number.isInteger(a.v) || !Number.isInteger(b.v)) throw new ErroVA('"' + op + '" só funciona com inteiros', L);
          if (b.v === 0) throw new ErroVA('divisão por zero', L);
          return { tipo: 'i', v: op === 'div' ? Math.trunc(a.v / b.v) : a.v % b.v };
        case '^': {
          num(a, L, op); num(b, L, op);
          var r = Math.pow(a.v, b.v);
          var inteiro = a.tipo === 'i' && b.tipo === 'i' && b.v >= 0 && Number.isInteger(r);
          return { tipo: inteiro ? 'i' : 'r', v: r };
        }
        case '=': return { tipo: 'b', v: compara(a, b, L) === 0 };
        case '<>': return { tipo: 'b', v: compara(a, b, L) !== 0 };
        case '<': return { tipo: 'b', v: compara(a, b, L) < 0 };
        case '>': return { tipo: 'b', v: compara(a, b, L) > 0 };
        case '<=': return { tipo: 'b', v: compara(a, b, L) <= 0 };
        case '>=': return { tipo: 'b', v: compara(a, b, L) >= 0 };
        case 'e': logi(a, L, 'e'); logi(b, L, 'e'); return { tipo: 'b', v: a.v && b.v };
        case 'ou': logi(a, L, 'ou'); logi(b, L, 'ou'); return { tipo: 'b', v: a.v || b.v };
        case 'xou': logi(a, L, 'xou'); logi(b, L, 'xou'); return { tipo: 'b', v: a.v !== b.v };
      }
      throw new ErroVA('operador desconhecido ' + op, L);
    }
    function fn(e) {
      var args = e.args.map(ev), L = e.linha, nome = e.nome;
      function n1() { if (args.length !== 1) throw new ErroVA(e.raw + ' precisa de 1 argumento', L); }
      switch (nome) {
        case 'raizq': n1(); num(args[0], L, nome); if (args[0].v < 0) throw new ErroVA('raiz de número negativo', L); return { tipo: 'r', v: Math.sqrt(args[0].v) };
        case 'abs': n1(); num(args[0], L, nome); return { tipo: args[0].tipo, v: Math.abs(args[0].v) };
        case 'int': n1(); num(args[0], L, nome); return { tipo: 'i', v: Math.trunc(args[0].v) };
        case 'quad': n1(); num(args[0], L, nome); return { tipo: args[0].tipo, v: args[0].v * args[0].v };
        case 'compr': n1(); if (args[0].tipo !== 's') throw new ErroVA('compr precisa de texto', L); return { tipo: 'i', v: args[0].v.length };
        case 'maiusc': n1(); if (args[0].tipo !== 's') throw new ErroVA('maiusc precisa de texto', L); return { tipo: 's', v: args[0].v.toUpperCase() };
        case 'minusc': n1(); if (args[0].tipo !== 's') throw new ErroVA('minusc precisa de texto', L); return { tipo: 's', v: args[0].v.toLowerCase() };
        case 'pot': case 'exp':
          if (args.length !== 2) throw new ErroVA(e.raw + ' precisa de 2 argumentos (base, expoente)', L);
          return bin({ op: '^', a: { k: 'lit', val: args[0] }, b: { k: 'lit', val: args[1] }, linha: L });
      }
      throw new ErroVA('função desconhecida: ' + e.raw, L);
    }
    function ev(e) {
      switch (e.k) {
        case 'lit': return e.val;
        case 'num': return { tipo: e.real ? 'r' : 'i', v: e.v };
        case 'str': return { tipo: 's', v: e.v };
        case 'log': return { tipo: 'b', v: e.v };
        case 'var': return ler(e.nome, e.idx, e.linha, e.campo);
        case 'un': {
          var a = ev(e.a);
          if (e.op === '-') { num(a, e.linha, '-'); return { tipo: a.tipo, v: -a.v }; }
          logi(a, e.linha, 'nao'); return { tipo: 'b', v: !a.v };
        }
        case 'bin': return bin(e);
        case 'fn': return fn(e);
      }
      throw new ErroVA('expressão inválida', 0);
    }
    function cond(e, linha) {
      var v = ev(e);
      if (v.tipo !== 'b') throw new ErroVA('a condição precisa dar VERDADEIRO ou FALSO', linha);
      return v.v;
    }
    function casa(x, v, linha) {
      if (x.faixa) return compara(v, ev(x.faixa[0]), linha) >= 0 && compara(v, ev(x.faixa[1]), linha) <= 0;
      return compara(v, ev(x.v), linha) === 0;
    }
    function laco(corpo) {
      try { exec(corpo); return false; } catch (err) { if (err === INTERROMPA) return true; throw err; }
    }
    function exec(lista) { for (var i = 0; i < lista.length; i++) um(lista[i]); }
    function um(s) {
      switch (s.k) {
        case 'atrib': {
          var val = ev(s.e);
          atribuir(s.nome, s.idx, val, s.linha, s.campo);
          passo(s.linha, nomeAlvo(s.nome, s.idx, s.campo) + ' recebe ' + (val.tipo === 's' ? '"' + val.v + '"' : fmt(val)));
          return;
        }
        case 'leia': {
          var pergunta = perguntaAtual();
          s.alvos.forEach(function (a) {
            if (!fila.length) {
              if (guiada) {
                var dd = prog.decl[a.nome];
                res.espera = { linha: s.linha, nome: dd ? nomeAlvo(a.nome, a.idx, a.campo) : a.nome, tipo: dd ? baseDe(a.nome, a.campo, s.linha) : '', pergunta: pergunta };
                passo(s.linha, 'esperando a ' + (res.lidas.length + 1) + 'ª entrada (' + res.espera.nome + ')');
              }
              throw new ErroVA('o programa pediu uma entrada (leia) e a lista de entradas acabou', s.linha);
            }
            var txt = fila.shift();
            var base = baseDe(a.nome, a.campo, s.linha);
            if (base === 'registro') throw new ErroVA('leia um campo por vez: ' + nomeAlvo(a.nome, a.idx) + '.campo', s.linha);
            var info = { linha: s.linha, nome: nomeAlvo(a.nome, a.idx, a.campo), tipo: base, pergunta: pergunta, valor: txt };
            var val;
            try { val = entrada(txt, base, s.linha); } catch (e) {
              info.msg = e.message; res.recusada = info; throw e;
            }
            atribuir(a.nome, a.idx, val, s.linha, a.campo);
            res.lidas.push(info);
            if (guiada) saida += txt + '\n';
            passo(s.linha, 'leu ' + txt + ' para ' + info.nome);
          });
          marcaLeia = saida.length;
          return;
        }
        case 'escreva': {
          // o VisuAlg escreve número com um espaço antes (ver Exemplos\decomp.alg: escreval(p[j], ex[j]))
          var txt = '';
          s.args.forEach(function (a) {
            if (a.k === 'formato') { txt += formatado(ev(a.e), a.larg, a.dec); return; }
            var v = ev(a); txt += (v.tipo === 'i' || v.tipo === 'r') ? ' ' + fmt(v) : fmt(v);
          });
          if (s.nl) txt += '\n';
          saida += txt;
          passo(s.linha, 'escreveu ' + JSON.stringify(txt));
          return;
        }
        case 'se': {
          var c = cond(s.c, s.linha);
          passo(s.linha, 'condição ' + (c ? 'VERDADEIRA: entra no então' : (s.senao ? 'FALSA: vai para o senão' : 'FALSA: pula o bloco')));
          if (c) exec(s.entao); else if (s.senao) exec(s.senao);
          return;
        }
        case 'escolha': {
          var v = ev(s.e), feito = false;
          passo(s.linha, 'compara ' + fmt(v) + ' com cada caso');
          for (var i = 0; i < s.casos.length; i++) {
            var cs = s.casos[i];
            if (cs.vals.some(function (x) { return casa(x, v, cs.linha); })) {
              passo(cs.linha, 'este caso combina');
              exec(cs.corpo); feito = true; break;
            }
          }
          if (!feito && s.outro) { passo(s.outroLinha, 'nenhum caso combinou: outrocaso'); exec(s.outro); }
          return;
        }
        case 'para': {
          var d = decl(s.v, s.linha);
          if (d.tipo.base !== 'inteiro' || d.tipo.dims) throw new ErroVA('a variável do "para" precisa ser inteira', s.linha);
          var ini = ev(s.ini), fim = ev(s.fim), pa = s.passo ? ev(s.passo) : { tipo: 'i', v: 1 };
          if (ini.tipo !== 'i' || fim.tipo !== 'i' || pa.tipo !== 'i') throw new ErroVA('limites e passo do "para" precisam ser inteiros', s.linha);
          if (pa.v === 0) throw new ErroVA('passo 0 deixaria o laço parado', s.linha);
          atribuir(s.v, null, ini, s.linha);
          for (;;) {
            var atual = mem[s.v].v;
            var segue = pa.v > 0 ? atual <= fim.v : atual >= fim.v;
            passo(s.linha, d.raw + ' = ' + atual + (segue ? ': entra no laço' : ': passou de ' + fim.v + ', sai do laço'));
            if (!segue) break;
            if (laco(s.corpo)) break;
            atribuir(s.v, null, { tipo: 'i', v: mem[s.v].v + pa.v }, s.linha);
          }
          return;
        }
        case 'enquanto': {
          for (;;) {
            var ce = cond(s.c, s.linha);
            passo(s.linha, 'condição ' + (ce ? 'VERDADEIRA: executa o corpo' : 'FALSA: sai do laço'));
            if (!ce) break;
            if (laco(s.corpo)) break;
          }
          return;
        }
        case 'repita': {
          for (;;) {
            if (laco(s.corpo)) break;
            if (s.c) {
              var cr = cond(s.c, s.ateLinha);
              passo(s.ateLinha, 'condição ' + (cr ? 'VERDADEIRA: sai do repita' : 'FALSA: repete'));
              if (cr) break;
            } else passo(s.ateLinha, 'volta ao repita');
          }
          return;
        }
        case 'interrompa':
          passo(s.linha, 'interrompa: sai do laço');
          throw INTERROMPA;
        case 'nada':
          return;
      }
    }

    try {
      passo(prog.linhaInicio, 'início: variáveis criadas com valor zero, texto vazio ou FALSO');
      exec(prog.corpo);
      passo(prog.linhaFim, 'fim do algoritmo');
    } catch (err) {
      if (err === INTERROMPA) {
        res.erro = { linha: 0, msg: '"interrompa" fora de um laço' };
      } else {
        res.erro = { linha: err.linha || 0, msg: err.message || String(err) };
      }
    }
    res.saida = saida;
    return res;
  }

  // ---------- explicador de erros (laboratório) ----------
  // VisuAlg.explicar(codigo, res) -> { tipo, titulo, oque, como, hoje, linha, correcao } ou null.
  // correcao: { codigo, diff: [{ s: '-'|'+', n, t }], rotulo, sugestao }. Texto com `código` entre crases.
  var CMDS = ['escreval', 'escreva', 'leia', 'se', 'entao', 'senao', 'fimse', 'para', 'faca', 'fimpara', 'enquanto',
    'fimenquanto', 'repita', 'fimrepita', 'escolha', 'caso', 'outrocaso', 'fimescolha', 'interrompa', 'inicio',
    'fimalgoritmo', 'algoritmo', 'limpatela', 'pausa'];
  var FUNCS = ['raizq', 'abs', 'int', 'quad', 'compr', 'maiusc', 'minusc', 'exp'];
  var FUNC_SIN = { raiz: 'raizq', sqrt: 'raizq', raizquadrada: 'raizq', pow: 'exp', potencia: 'exp', modulo: 'abs', absoluto: 'abs' };
  var TIPO_SIN = { inteira: 'inteiro', int: 'inteiro', integer: 'inteiro', numero: 'inteiro', inteiros: 'inteiro',
    texto: 'caractere', string: 'caractere', str: 'caractere', char: 'caractere', caracteres: 'caractere',
    float: 'real', double: 'real', decimal: 'real', reais: 'real', bool: 'logico', boolean: 'logico', logica: 'logico' };
  var ABRE = { se: 'fimse', para: 'fimpara', enquanto: 'fimenquanto', repita: 'ate', escolha: 'fimescolha' };
  var FECHA = { fimse: 'se', fimpara: 'para', fimenquanto: 'enquanto', ate: 'repita', fimrepita: 'repita', fimescolha: 'escolha' };
  var OPKW = { e: 1, ou: 1, nao: 1, xou: 1, div: 1, mod: 1, de: 1, ate: 1, passo: 1, faca: 1, entao: 1 };

  function distancia(a, b) {
    var m = a.length, n = b.length, d = [], i, j;
    for (i = 0; i <= m; i++) { d[i] = [i]; }
    for (j = 0; j <= n; j++) d[0][j] = j;
    for (i = 1; i <= m; i++) for (j = 1; j <= n; j++) {
      d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    }
    return d[m][n];
  }
  // palavra parecida: nada para palavras de 1 ou 2 letras (j e i não são "parecidas");
  // 3 a 5 letras aceitam 1 diferença, 6 ou mais aceitam 2. minimo: tamanho mínimo da palavra.
  function parecida(w, lista, minimo) {
    if (w.length < (minimo || 3)) return null;
    var melhor = null, md = 3, lim = w.length >= 6 ? 2 : 1;
    lista.forEach(function (x) {
      var dd = distancia(w, x);
      if (dd > 0 && dd < md && dd <= lim && x.length >= 3) { md = dd; melhor = x; }
    });
    return melhor;
  }
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  function explicar(codigo, res) {
    if (!res || !res.erro) return null;
    try { return explicar_(String(codigo), res); } catch (e) {
      return { tipo: 'geral', titulo: 'Linha ' + (res.erro.linha || '?') + ' · erro', hoje: res.erro.msg, linha: res.erro.linha,
        oque: 'O site parou com a mensagem: ' + res.erro.msg + '.', como: 'Confira esta linha e a de cima.', correcao: null };
    }
  }

  function explicar_(codigo, res) {
    var msg = res.erro.msg, L = res.erro.linha || 0, L0 = L;
    var lin = codigo.split('\n');
    function get(n) { return (lin[n - 1] || '').replace(/\r$/, ''); }
    function ind(s) { return (s.match(/^[ \t]*/) || [''])[0]; }
    function low(s) { return semAcento(String(s).toLowerCase()); }
    function pw(n) { var m = low(get(n)).trim().match(/^[a-z_][a-z0-9_]*/); return m ? m[0] : ''; }
    function semCom(s) { var k = s.indexOf('//'); return k >= 0 ? s.slice(0, k) : s; }
    var decl = res.decl || {};
    var nomesDecl = Object.keys(decl).map(function (k) { return decl[k].raw; });
    var ultimo = res.passos && res.passos.length ? res.passos[res.passos.length - 1].vars : {};
    function valores(n) {
      var vistos = {}, out = [];
      (get(n).match(/[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*/g) || []).forEach(function (w) {
        var k = low(w);
        if (vistos[k] || !decl[k]) return; vistos[k] = 1;
        var raw = decl[k].raw;
        if (ultimo[raw] !== undefined) out.push('`' + raw + ' = ' + ultimo[raw] + '`');
      });
      return out;
    }
    function ex(tipo, titulo, oque, como, nova, extra) {
      var r = { tipo: tipo, titulo: titulo, oque: oque, como: como, hoje: (L0 ? 'linha ' + L0 + ': ' : '') + msg, linha: L, correcao: null };
      if (nova) {
        var d = diff(lin, nova);
        if (d.length) r.correcao = { codigo: nova.join('\n'), diff: d, rotulo: (extra && extra.rotulo) || 'Aplicar correção', sugestao: !!(extra && extra.sugestao) };
      }
      return r;
    }
    function copia() { return lin.slice(); }
    function troca(n, t) { var c = copia(); c[n - 1] = t; return c; }
    function insere(depoisDe, t) { var c = copia(); c.splice(depoisDe, 0, t); return c; }
    function trocaPalavra(n, de, para) {
      var re = new RegExp('(^|[^A-Za-z0-9_À-ÿ])' + escRe(de) + '(?![A-Za-z0-9_À-ÿ])', 'i');
      var s = get(n);
      return re.test(s) ? troca(n, s.replace(re, function (m, a) { return a + para; })) : null;
    }
    function linhaVar() { for (var n = 1; n <= lin.length; n++) if (pw(n) === 'var') return n; return 0; }
    function linhaInicio() { for (var n = 1; n <= lin.length; n++) if (pw(n) === 'inicio') return n; return 0; }
    var REDECL = /^(\s*(?:var\s+)?)(.+?)(\s*:\s*)(inteiro|real|caractere|caracter|literal|logico)(\s*;?\s*)$/i;
    function achaDecl(nome) {
      var a = linhaVar(), b = linhaInicio() || lin.length + 1;
      if (!a) return null;
      for (var n = a; n < b; n++) {
        var m = semCom(get(n)).match(REDECL);
        if (!m) continue;
        var nomes = m[2].split(',').map(function (x) { return x.trim(); });
        var k = nomes.map(low).indexOf(low(nome));
        if (k >= 0) return { n: n, m: m, nomes: nomes, k: k };
      }
      return null;
    }
    function mudaTipo(nome, tipo) {
      var dd = achaDecl(nome);
      if (!dd) return null;
      var m = dd.m;
      if (dd.nomes.length === 1) return troca(dd.n, m[1] + m[2] + m[3] + tipo + m[5]);
      var resto = dd.nomes.filter(function (x, i) { return i !== dd.k; });
      var c = troca(dd.n, m[1] + resto.join(', ') + m[3] + m[4] + m[5]);
      var recuo = ind(get(dd.n)) || '   ';
      if (/^\s*var\s/i.test(get(dd.n))) recuo = '   ';
      c.splice(dd.n, 0, recuo + dd.nomes[dd.k] + ': ' + tipo);
      return c;
    }
    function acrescentaDecl(nome, tipo) {
      var a = linhaVar(), b = linhaInicio();
      if (a && b) {
        for (var n = a; n < b; n++) {
          var m = semCom(get(n)).match(REDECL);
          if (m && low(m[4]).replace(/caracter$|literal/, 'caractere') === tipo) return troca(n, m[1] + m[2] + ', ' + nome + m[3] + m[4] + m[5]);
        }
        return insere(b - 1, '   ' + nome + ': ' + tipo);
      }
      if (b) { var c = copia(); c.splice(b - 1, 0, 'var', '   ' + nome + ': ' + tipo); return c; }
      return null;
    }
    function tipoPeloUso(v) {
      var vr = escRe(v);
      for (var n = 1; n <= lin.length; n++) {
        var s = semCom(get(n));
        if (new RegExp('^\\s*para\\s+' + vr + '\\s+de\\b', 'i').test(s)) return { tipo: 'inteiro', porque: 'Ela conta as voltas do `para`' };
        var m = s.match(new RegExp('^\\s*' + vr + '\\s*(?:<-|:=|←)\\s*(.+)$', 'i'));
        if (!m) continue;
        var r = m[1].trim();
        if (/^"/.test(r)) return { tipo: 'caractere', porque: 'Ela recebe um texto' };
        if (/^(verdadeiro|falso)\b/i.test(r)) return { tipo: 'logico', porque: 'Ela recebe VERDADEIRO ou FALSO' };
        if (/^-?\d+\.\d+/.test(r) || /\//.test(r) || /raizq\s*\(/i.test(r)) return { tipo: 'real', porque: 'Ela recebe um número com casas decimais' };
        if (/^-?\d+\s*$/.test(r)) return { tipo: 'inteiro', porque: 'Ela recebe um número inteiro' };
      }
      return null;
    }
    // pilha de blocos pelo começo de cada linha
    function blocos() {
      var pilha = [];
      for (var n = 1; n <= lin.length; n++) {
        var w = pw(n);
        if (ABRE[w]) pilha.push({ kw: w, n: n, ind: ind(get(n)) });
        else if (FECHA[w]) {
          var topo = pilha[pilha.length - 1];
          if (topo && topo.kw === FECHA[w]) pilha.pop();
          else if (topo) return { aberto: topo, achou: { w: w, n: n } };
          else return { sobra: { w: w, n: n } };
        } else if (w === 'fimalgoritmo' && pilha.length) return { aberto: pilha[pilha.length - 1], achou: { w: w, n: n } };
      }
      return pilha.length ? { aberto: pilha[pilha.length - 1], achou: { w: 'fim do código', n: lin.length } } : null;
    }
    function fechaBloco(b) {
      if (b.kw === 'repita') return null;
      var ultimoN = b.n;
      for (var k = b.n + 1; k <= lin.length; k++) {
        var s = get(k);
        if (!s.trim()) continue;
        var w = pw(k);
        if (ind(s).length > b.ind.length) { ultimoN = k; continue; }
        if (b.kw === 'se' && w === 'senao') { ultimoN = k; continue; }
        if (b.kw === 'escolha' && (w === 'caso' || w === 'outrocaso')) { ultimoN = k; continue; }
        break;
      }
      if (ultimoN === b.n) return null;
      return { nova: insere(ultimoN, b.ind + ABRE[b.kw]), depois: ultimoN };
    }
    function blocoAberto(bl) {
      var a = bl.aberto, fim = ABRE[a.kw], onde = bl.achou.w === 'fim do código' ? 'no fim do código' : 'na linha ' + bl.achou.n + ', ao encontrar `' + bl.achou.w + '`';
      var fb = fechaBloco(a);
      L = a.n;
      return ex('bloco-aberto', 'Linha ' + a.n + ' · `' + a.kw + '` sem `' + fim + '`',
        'O `' + a.kw + '` aberto na linha ' + a.n + ' não foi fechado. O site só percebeu ' + onde + '.',
        fb ? 'Feche com `' + fim + '`. Pelo recuo do texto, o bloco termina na linha ' + fb.depois + ', então o `' + fim + '` entra logo depois dela.'
          : 'Feche com `' + fim + '` depois do último comando que deve ficar dentro do `' + a.kw + '`.' + (a.kw === 'repita' ? ' O `repita` fecha com `ate` e uma condição: `ate i > 10`.' : ''),
        fb ? fb.nova : null);
    }
    var m;

    // 1. variável não declarada
    if ((m = msg.match(/^variável não declarada: (\S+)/))) {
      var v = m[1], vRaw = (get(L).match(new RegExp('[A-Za-z0-9_À-ÿ]*', 'g')) || []).filter(function (w) { return low(w) === v; })[0] || v;
      var quis = parecida(v, Object.keys(decl), 4);
      if (quis) {
        return ex('nao-declarada', 'Linha ' + L + ' · nome escrito diferente',
          'O programa usa `' + vRaw + '`, que não existe no `var`. Existe uma variável parecida: `' + decl[quis].raw + '`.',
          'Você quis dizer `' + decl[quis].raw + '`? Troque o nome nesta linha.', trocaPalavra(L, vRaw, decl[quis].raw));
      }
      var tu = tipoPeloUso(vRaw);
      return ex('nao-declarada', 'Linha ' + L + ' · variável que não existe',
        'O programa usa a variável `' + vRaw + '`, mas ela não foi criada no `var`. Toda variável precisa ser declarada antes do `inicio`.',
        tu ? 'Acrescente `' + vRaw + '` no `var`. ' + tu.porque + ', então é `' + tu.tipo + '`.'
          : 'Acrescente `' + vRaw + '` no `var` com o tipo certo: `inteiro` (número sem vírgula), `real` (com casas decimais), `caractere` (texto) ou `logico` (VERDADEIRO ou FALSO).',
        tu ? acrescentaDecl(vRaw, tu.tipo) : null);
    }

    // 2. palavra seguida de algo que não é <-: comando digitado errado, = no lugar de <-, nome com espaço
    if ((m = msg.match(/^esperava "<-" depois de "(.+)"$/))) {
      var w = m[1], wl = low(w), s2 = get(L);
      if (wl === 'senaose' || wl === 'senaoSe') {
        return ex('senaose', 'Linha ' + L + ' · `senaose` não existe',
          'O VisuAlg não tem `senaose`. Para testar outra condição, use `senao` e, dentro dele, um novo `se`.',
          'Escreva `senao` numa linha e `se ... entao` na linha de baixo. Esse `se` de dentro precisa do próprio `fimse`, então no fim ficam dois `fimse`.', null);
      }
      var reIg = new RegExp('^(\\s*' + escRe(w) + '\\s*(?:\\[[^\\]]*\\])?\\s*)=(?!=)', 'i');
      if (reIg.test(s2)) {
        return ex('igual', 'Linha ' + L + ' · `=` no lugar de `<-`',
          'No VisuAlg, guardar um valor numa variável é com `<-` (sinal de menor e hífen). O `=` serve para comparar, por exemplo dentro de um `se`.',
          'Troque o `=` por `<-`.', troca(L, s2.replace(reIg, function (x, a) { return a.replace(/\s*$/, ' ') + '<-'; })));
      }
      var cmd = parecida(wl, CMDS);
      if (cmd) {
        return ex('comando-errado', 'Linha ' + L + ' · comando que não existe',
          '`' + w + '` não é um comando do VisuAlg. Como o site não reconheceu a palavra, achou que fosse uma variável recebendo valor e ficou esperando um `<-`.',
          'Você quis dizer `' + cmd + '`?', trocaPalavra(L, w, cmd));
      }
      if (/^\s*[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*\s*\(/.test(s2)) {
        return ex('comando-errado', 'Linha ' + L + ' · comando que não existe',
          '`' + w + '` não é um comando do VisuAlg. Como o site não reconheceu a palavra, achou que fosse uma variável recebendo valor.',
          'Confira a escrita. Os comandos de tela são `escreva`, `escreval` e `leia`.', null);
      }
      return ex('sem-recebe', 'Linha ' + L + ' · faltou `<-`',
        'Depois do nome de uma variável o VisuAlg espera `<-`, para guardar um valor nela.',
        'Se a linha era para guardar um valor, escreva `' + w + ' <- valor`. Se era um comando, confira a escrita da primeira palavra.', null);
    }

    // 3. tipos incompatíveis
    if ((m = msg.match(/^tipos incompatíveis: valor real em variável inteira \((.+)\)$/))) {
      return ex('real-em-inteiro', 'Linha ' + L + ' · número com vírgula em variável inteira',
        'A conta desta linha dá um número com casas decimais (a divisão `/` sempre dá). A variável `' + m[1] + '` foi declarada como `inteiro`, e inteiro não guarda casas decimais.',
        'Declare `' + m[1] + '` como `real`. Se quiser só a parte inteira da divisão, use `div` no lugar de `/`.', mudaTipo(m[1], 'real'));
    }
    if ((m = msg.match(/^tipos incompatíveis: caractere em variável (inteiro|real) \((.+)\)$/))) {
      var s3 = get(L), q = s3.match(/<-\s*"(\s*-?\d+(?:[.,]\d+)?\s*)"/);
      if (q) {
        return ex('texto-em-numero', 'Linha ' + L + ' · número entre aspas',
          'Entre aspas, `"' + q[1] + '"` é um texto, não um número. A variável `' + m[2] + '` é `' + m[1] + '` e só guarda número.',
          'Tire as aspas: `' + q[1].trim() + '`.', troca(L, s3.replace(q[0], '<- ' + q[1].trim().replace(',', '.'))));
      }
      return ex('texto-em-numero', 'Linha ' + L + ' · texto em variável de número',
        'A variável `' + m[2] + '` é `' + m[1] + '`, mas esta linha guarda um texto nela.',
        'Se ela deve guardar texto, declare como `caractere`.', mudaTipo(m[2], 'caractere'));
    }
    if ((m = msg.match(/^tipos incompatíveis: (inteiro|real) em variável caractere \((.+)\)$/))) {
      var s4 = get(L), q2 = s4.match(/<-\s*(-?\d+(?:\.\d+)?)\s*$/);
      return ex('numero-em-texto', 'Linha ' + L + ' · número em variável de texto',
        'A variável `' + m[2] + '` é `caractere` (texto), mas esta linha guarda um número nela.',
        q2 ? 'Se é para guardar como texto, ponha entre aspas: `"' + q2[1] + '"`. Se é para fazer conta, declare `' + m[2] + '` como `inteiro` ou `real`.'
          : 'Se é para fazer conta, declare `' + m[2] + '` como `inteiro` ou `real`.',
        q2 ? troca(L, s4.replace(q2[0], '<- "' + q2[1] + '"')) : null);
    }
    if ((m = msg.match(/^tipos incompatíveis: (.+) em variável (.+) \((.+)\)$/))) {
      return ex('tipos', 'Linha ' + L + ' · tipo diferente', 'Esta linha guarda um valor ' + m[1] + ' na variável `' + m[3] + '`, que é ' + m[2] + '.',
        'Confira o tipo da variável no `var` ou o valor guardado.', null);
    }

    // 4. blocos sem fechar e estrutura
    if (/^comando inesperado: /.test(msg) || /^faltou "/.test(msg) || /^esperava "(fimse|fimpara|fimenquanto|fimescolha|ate|fimalgoritmo)"/.test(msg)) {
      var bl = blocos();
      if (bl && bl.aberto) return blocoAberto(bl);
      if (bl && bl.sobra) {
        L = bl.sobra.n;
        return ex('fecha-sobrando', 'Linha ' + bl.sobra.n + ' · `' + bl.sobra.w + '` sem abertura',
          'Há um `' + bl.sobra.w + '` na linha ' + bl.sobra.n + ', mas não existe um `' + FECHA[bl.sobra.w] + '` aberto antes dele.',
          'Confira se o `' + FECHA[bl.sobra.w] + '` está escrito certo. Se esta linha sobrou, apague.', null);
      }
      if ((m = msg.match(/^comando inesperado: var$/))) {
        // tira o inicio de cima e devolve antes do primeiro comando depois das declarações
        var iv = linhaInicio(), nv = linhaVar(), cv = null;
        if (iv && nv > iv) {
          cv = copia(); var linhaIni = cv.splice(iv - 1, 1)[0];
          var p = nv - 1;
          while (p < cv.length && (!cv[p].trim() || /^\s*var\s*$/i.test(cv[p]) || REDECL.test(semCom(cv[p])))) p++;
          cv.splice(p, 0, linhaIni);
        }
        return ex('estrutura', 'Linha ' + L + ' · `var` depois do `inicio`',
          'O programa tem uma ordem fixa: `algoritmo`, depois `var` com as variáveis, depois `inicio` com os comandos e, por último, `fimalgoritmo`.',
          'Coloque o `var` e as declarações antes do `inicio`.', cv);
      }
      if (/^faltou "fimalgoritmo"/.test(msg)) {
        var ult = lin.length; while (ult > 1 && !get(ult).trim()) ult--;
        return ex('estrutura', 'Fim do código · falta `fimalgoritmo`', 'Todo programa termina com `fimalgoritmo`.', 'Acrescente `fimalgoritmo` na última linha.', insere(ult, 'fimalgoritmo'));
      }
    }

    // 5. falta entao / faca, <- na condição
    if ((m = msg.match(/^esperava "(entao|faca)" e encontrei "(.+)"$/))) {
      var alvo = m[1], achou = m[2], abre = alvo === 'entao' ? ['se'] : ['para', 'enquanto', 'escolha'], ln = 0;
      for (var k5 = L; k5 >= 1; k5--) if (abre.indexOf(pw(k5)) >= 0) { ln = k5; break; }
      if (alvo === 'entao' && achou === '<-' && ln) {
        return ex('recebe-na-condicao', 'Linha ' + ln + ' · `<-` na condição',
          'Na condição do `se` a gente compara, não guarda. Comparar é com `=`; o `<-` guarda valor numa variável.',
          'Troque o `<-` por `=`.', troca(ln, get(ln).replace('<-', '=')));
      }
      if (ln && ln < L) {
        var sl = get(ln), corpo = semCom(sl).replace(/\s+$/, '');
        L = ln;
        return ex('falta-' + alvo, 'Linha ' + ln + ' · falta `' + alvo + '`',
          alvo === 'entao' ? 'Depois da condição do `se` vem sempre `entao`: `se media >= 6 entao`.' : 'O `' + pw(ln) + '` termina com `faca`: `para i de 1 ate 10 faca` ou `enquanto i <= 10 faca`.',
          'Acrescente `' + alvo + '` no fim da linha ' + ln + '.', troca(ln, corpo + ' ' + alvo + sl.slice(corpo.length)));
      }
      return ex('falta-' + alvo, 'Linha ' + L + ' · falta `' + alvo + '`', 'O site esperava `' + alvo + '` e encontrou `' + achou + '`.',
        alvo === 'entao' ? 'O `se` tem a forma `se condição entao`, e os comandos vão nas linhas de baixo.' : 'O laço tem a forma `para i de 1 ate 10 faca` ou `enquanto condição faca`, e os comandos vão nas linhas de baixo.', null);
    }
    if ((m = msg.match(/^esperava "(de|ate)" e encontrei/))) {
      return ex('forma-para', 'Linha ' + L + ' · forma do `para`', 'O `para` tem uma forma fixa: `para i de 1 ate 10 faca`.',
        'Confira se estão as palavras `de`, `ate` e `faca`, nessa ordem.', null);
    }

    // 6. aspas e símbolos
    if (/^texto sem aspas de fechamento/.test(msg)) {
      var s6 = get(L), np = s6.replace(/\)\s*$/, '"$&');
      if (np === s6) np = s6.replace(/\s*$/, '"');
      return ex('aspas', 'Linha ' + L + ' · aspas sem fechar', 'Todo texto começa e termina com aspas: `"Olá"`. Nesta linha uma aspa abriu e não fechou.',
        'Feche as aspas no fim do texto.', troca(L, np));
    }
    if ((m = msg.match(/^símbolo inesperado: (.)$/))) {
      var c6 = m[1];
      if (c6 === "'") {
        return ex('aspas-simples', 'Linha ' + L + ' · aspas simples', "No VisuAlg, texto vai entre aspas duplas: `\"Olá\"`. A aspa simples `'` não funciona.",
          "Troque `'` por `\"`.", troca(L, get(L).replace(/'/g, '"')));
      }
      return ex('simbolo', 'Linha ' + L + ' · símbolo `' + c6 + '`', 'O símbolo `' + c6 + '` não faz parte da linguagem do VisuAlg.', 'Apague ou troque esse símbolo.', null);
    }

    // 7. parênteses, vírgulas e formatação
    if ((m = msg.match(/^esperava "\)" e encontrei "(.+)"$/))) {
      var achou7 = m[1], s7 = get(L);
      if (achou7 === ':') {
        var semFmt = s7.replace(/\s*:\s*\d+(\s*:\s*\d+)?(?=\s*[,)])/g, '');
        return ex('formatacao', 'Linha ' + L + ' · formatação fora do lugar',
          'A formatação `:5:2` (5 espaços, 2 casas decimais) só vale dentro do `escreva` e do `escreval`, por exemplo `escreval(media:5:2)`. Aqui ela apareceu em outro lugar.',
          'Tire a formatação desta linha. Para mostrar o número formatado, use-a no `escreval`.', semFmt !== s7 ? troca(L, semFmt) : null);
      }
      // parêntese aberto numa linha de cima: o site só acusa na linha seguinte
      var lp = 0;
      for (var k7 = L; k7 >= 1; k7--) {
        var sk = semCom(get(k7)).replace(/"[^"]*"/g, '');
        if ((sk.match(/\(/g) || []).length > (sk.match(/\)/g) || []).length) { lp = k7; break; }
      }
      if (lp && (lp < L || CMDS.indexOf(achou7) >= 0 || achou7 === 'fim do código')) {
        L = lp;
        return ex('parentese', 'Linha ' + lp + ' · parêntese sem fechar', 'Na linha ' + lp + ' um `(` abriu e não fechou.' + (lp < L0 ? ' O site só percebeu na linha ' + L0 + '.' : ''),
          'Feche o parêntese no fim da linha ' + lp + '.', troca(lp, get(lp).replace(/\s*$/, ')')));
      }
      // falta vírgula entre dois pedaços
      // textos mascarados para não procurar dentro das aspas (mesmas posições)
      var m7 = s7.replace(/"[^"]*"/g, function (x) { return '"' + new Array(x.length - 1).join('_') + '"'; });
      var re7 = /("[^"]*"|[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*|\d+(?:\.\d+)?|\))(\s+)(?=("|[A-Za-z_À-ÿ]|\d))/g, mm, nova7 = null;
      while ((mm = re7.exec(m7))) {
        var antes = low(mm[1]), depois = low(m7.slice(mm.index + mm[0].length).match(/^("|[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*|\d+)/)[0]);
        if (OPKW[antes] || OPKW[depois] || KWSET[antes] && antes !== 'verdadeiro' && antes !== 'falso') continue;
        nova7 = s7.slice(0, mm.index + mm[1].length) + ', ' + s7.slice(mm.index + mm[0].length);
        break;
      }
      if (nova7) {
        return ex('virgula', 'Linha ' + L + ' · falta vírgula', 'Dentro dos parênteses, cada pedaço é separado por vírgula: `escreval("Total: ", x)`.',
          'Acrescente a vírgula que falta.', troca(L, nova7));
      }
      return ex('parentese', 'Linha ' + L + ' · parênteses', 'O site esperava fechar um parêntese e encontrou `' + achou7 + '`.', 'Confira os parênteses e as vírgulas desta linha.', null);
    }
    if ((m = msg.match(/^esperava "\(" e encontrei/))) {
      var s8 = get(L), r8 = s8.match(/^(\s*)(leia|escreval|escreva)\s+(.+?)\s*$/i);
      return ex('sem-parenteses', 'Linha ' + L + ' · faltam parênteses', 'Os comandos `leia`, `escreva` e `escreval` usam parênteses: `leia(x)`.',
        'Coloque o que vem depois do comando entre parênteses.', r8 ? troca(L, r8[1] + r8[2] + '(' + r8[3] + ')') : null);
    }

    if (/^depois d[ae] (":"|largura)/.test(msg)) {
      return ex('formato-numero', 'Linha ' + L + ' · formatação `:5:2`',
        'A formatação tem a forma `valor:largura:casas`, com números inteiros: `media:5:2` escreve em 5 espaços com 2 casas decimais. Só a largura também vale: `idade:3`.',
        'Confira os números depois dos `:`. Eles não podem ter vírgula nem ponto.', null);
    }

    // 8. nomes e tipos na declaração
    if ((m = msg.match(/^tipo desconhecido: (.+)$/))) {
      var tp = TIPO_SIN[low(m[1])] || parecida(low(m[1]), ['inteiro', 'real', 'caractere', 'logico']);
      return ex('tipo', 'Linha ' + L + ' · tipo `' + m[1] + '` não existe', 'Os tipos do VisuAlg são `inteiro`, `real`, `caractere` e `logico`.',
        tp ? 'Você quis dizer `' + tp + '`?' : 'Escolha um desses tipos.', tp ? trocaPalavra(L, m[1], tp) : null);
    }
    if ((m = msg.match(/^função desconhecida: (.+)$/))) {
      var fs = FUNC_SIN[low(m[1])] || parecida(low(m[1]), FUNCS);
      return ex('funcao', 'Linha ' + L + ' · função `' + m[1] + '` não existe', 'O site conhece estas funções: ' + FUNCS.map(function (f) { return '`' + f + '`'; }).join(', ') + '.',
        fs ? 'Você quis dizer `' + fs + '`?' + (fs === 'exp' ? ' `exp(2, 3)` dá 2 elevado a 3.' : '') : 'Confira o nome da função.', fs ? trocaPalavra(L, m[1], fs) : null);
    }
    if ((m = msg.match(/^esperava ":" e encontrei "(.+)"$/))) {
      var s9 = get(L), li = linhaInicio();
      if (!li && /<-|:=/.test(s9)) {
        return ex('estrutura', 'Linha ' + L + ' · falta `inicio`', 'Antes dos comandos vem `inicio`. Sem ele, o site achou que esta linha ainda era declaração de variável.',
          'Acrescente `inicio` antes da linha ' + L + '.', insere(L - 1, 'inicio'));
      }
      var r9 = semCom(s9).match(/^(\s*(?:var\s+)?)([A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*)\s+([A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*)\s*:/);
      if (r9) {
        var junto = r9[2] + '_' + r9[3], reJ = new RegExp(escRe(r9[2]) + '\\s+' + escRe(r9[3]), 'gi');
        return ex('nome-espaco', 'Linha ' + L + ' · nome com espaço',
          'Nome de variável não pode ter espaço. Pelo manual, ele começa com letra e depois só tem letras, números ou `_`.',
          'Junte as palavras com `_`: `' + junto + '`, aqui e em todo lugar onde o nome aparece.', lin.map(function (x) { return x.replace(reJ, junto); }));
      }
      return ex('declaracao', 'Linha ' + L + ' · declaração', 'Cada declaração tem a forma `nome: tipo`, por exemplo `idade: inteiro`.', 'Confira esta linha.', null);
    }
    if ((m = msg.match(/^esperava "inicio" e encontrei "(.+)"$/))) {
      if (/^\d/.test(m[1]) || /^\s*\d/.test(get(L))) {
        return ex('nome-numero', 'Linha ' + L + ' · nome começando com número',
          'Nome de variável começa com letra. Depois pode ter números: `nota1` vale, `1nota` não.', 'Troque o nome para começar com letra, por exemplo `nota1`.', null);
      }
      if (/<-|:=|\(/.test(get(L))) {
        return ex('estrutura', 'Linha ' + L + ' · falta `inicio`', 'Antes dos comandos vem `inicio`.', 'Acrescente `inicio` antes da linha ' + L + '.', insere(L - 1, 'inicio'));
      }
    }
    if ((m = msg.match(/^variável declarada duas vezes: (.+)$/))) {
      return ex('duas-vezes', 'Linha ' + L + ' · variável declarada duas vezes', 'A variável `' + m[1] + '` aparece duas vezes no `var`. Cada nome só pode existir uma vez.',
        'Apague uma das declarações ou troque o nome de uma delas.', null);
    }
    if ((m = msg.match(/^nome de variável inválido: (.+)$/))) {
      return ex('nome', 'Linha ' + L + ' · nome inválido', 'Pelo manual, o nome começa com letra e depois só tem letras, números ou `_`, até 30 caracteres.', 'Troque `' + m[1] + '` por um nome nessa regra.', null);
    }

    // 9. laço que não termina
    var val = valores(L), vtxt = val.length ? ' Valores quando o site parou: ' + val.join(', ') + '.' : '';
    if (/^passei de \d+ passos/.test(msg)) return lacoInfinito();

    // 10. erros ao rodar: explica com os valores do momento
    if (/^divisão por zero/.test(msg)) return ex('divisao-zero', 'Linha ' + L + ' · divisão por zero', 'Esta linha divide por zero.' + vtxt, 'Confira se o divisor recebeu valor antes. Toda variável numérica começa em 0.', null);
    if ((m = msg.match(/^não dá para comparar (.+) com (.+)$/))) {
      return ex('comparar', 'Linha ' + L + ' · comparação de tipos diferentes', 'Só dá para comparar valores do mesmo tipo: texto com texto, número com número. Aqui a comparação é entre ' + m[1] + ' e ' + m[2] + '.' + vtxt,
        'Se o valor é texto, ponha entre aspas: `"5"`. Se a variável deveria ser número, declare como `inteiro` ou `real`.', null);
    }
    if ((m = msg.match(/^índice (.+) fora do vetor (.+)$/))) {
      return ex('vetor', 'Linha ' + L + ' · posição fora do vetor', 'O vetor `' + m[2] + '` não tem a posição ' + m[1] + '.' + vtxt, 'Confira o limite do `para` que percorre o vetor ou o tamanho na declaração.', null);
    }
    if ((m = msg.match(/^"(mod|div|\\)" só funciona com inteiros/))) {
      return ex('mod-div', 'Linha ' + L + ' · `' + m[1] + '` com número real', '`mod` e `div` são contas de números inteiros (resto e quociente).' + vtxt, 'Use variáveis `inteiro`, ou `int(x)` para tirar a parte decimal antes.', null);
    }
    if ((m = msg.match(/^a variável do "para" precisa ser inteira/))) {
      var vp = (get(L).match(/para\s+([A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*)/i) || [])[1];
      return ex('para-inteiro', 'Linha ' + L + ' · contador do `para`', 'O contador do `para` anda de 1 em 1, por isso precisa ser `inteiro`.', vp ? 'Declare `' + vp + '` como `inteiro`.' : 'Declare o contador como `inteiro`.', vp ? mudaTipo(vp, 'inteiro') : null);
    }
    if (/^a condição precisa dar VERDADEIRO ou FALSO/.test(msg)) {
      return ex('condicao', 'Linha ' + L + ' · condição sem comparação', 'A condição precisa dar VERDADEIRO ou FALSO, como `x > 3` ou `nome = "Ana"`.' + vtxt, 'Complete a condição com uma comparação.', null);
    }
    if ((m = msg.match(/^a operação "(.+)" precisa de números, recebeu (.+)$/))) {
      return ex('conta-texto', 'Linha ' + L + ' · conta com texto', 'A conta `' + m[1] + '` só funciona com números, e aqui entrou um valor ' + m[2] + '.' + vtxt, 'Confira o tipo das variáveis da conta. Texto entre aspas não vira número.', null);
    }
    return ex('geral', 'Linha ' + L + ' · erro', 'O site parou com a mensagem: ' + msg + '.' + vtxt, 'Confira esta linha e a de cima. Muitas vezes o erro é um parêntese, uma aspa ou uma palavra que faltou no fim da linha anterior.', null);

    function lacoInfinito() {
      var ab = 0, fe = 0;
      for (var k = L; k >= 1 && !ab; k--) {
        var w = pw(k);
        if (w !== 'enquanto' && w !== 'repita') continue;
        var prof = 0;
        for (var j = k + 1; j <= lin.length; j++) {
          var wj = pw(j);
          if (ABRE[wj]) prof++;
          else if (FECHA[wj]) { if (prof === 0) { if (FECHA[wj] === w && j >= L) { ab = k; fe = j; } break; } prof--; }
        }
      }
      var padrao = ex('laco', 'Linha ' + L + ' · laço que não termina', 'O site parou depois de 5.000 passos: a condição do laço nunca mudou para sair.' + vtxt, 'Confira se a variável da condição muda a cada volta e na direção certa.', null);
      if (!ab) return padrao;
      var kw = pw(ab), cond = kw === 'enquanto' ? (semCom(get(ab)).match(/enquanto\s+(.+?)\s+fa[cç]a\b/i) || [])[1] : (semCom(get(fe)).match(/^\s*ate\s+(.+?)\s*$/i) || [])[1];
      if (!cond) return padrao;
      var vs = [];
      (cond.match(/[A-Za-z_À-ÿ][A-Za-z0-9_À-ÿ]*/g) || []).forEach(function (x) { if (decl[low(x)] && vs.indexOf(decl[low(x)].raw) < 0) vs.push(decl[low(x)].raw); });
      if (!vs.length) return padrao;
      var corpo = lin.slice(ab, fe - 1).map(semCom);
      var mudam = vs.filter(function (x) {
        var r = new RegExp('^\\s*' + escRe(x) + '\\s*(\\[[^\\]]*\\])?\\s*(<-|:=|←)|leia\\s*\\([^)]*\\b' + escRe(x) + '\\b|para\\s+' + escRe(x) + '\\b', 'i');
        return corpo.some(function (s) { return r.test(s); });
      });
      var vals = vs.filter(function (x) { return ultimo[x] !== undefined; }).map(function (x) { return '`' + x + ' = ' + ultimo[x] + '`'; });
      L = ab;
      if (mudam.length) {
        return ex('laco', 'Linha ' + ab + ' · laço que não termina', 'O `' + kw + '` depende de `' + cond + '`, e essa condição nunca deixou o laço sair. O site parou depois de 5.000 passos.' + (vals.length ? ' Valores quando parou: ' + vals.join(', ') + '.' : ''),
          'Confira se a variável anda na direção certa a cada volta: somando quando precisa crescer, subtraindo quando precisa diminuir.', null);
      }
      var x0 = vs[0], cm = cond.match(new RegExp('^\\s*' + escRe(x0) + '\\s*(<=|>=|<>|<|>|=)', 'i')), passoTxt = null;
      if (cm) {
        var cresce = kw === 'enquanto' ? (cm[1] === '<' || cm[1] === '<=') : (cm[1] === '>' || cm[1] === '>=');
        var desce = kw === 'enquanto' ? (cm[1] === '>' || cm[1] === '>=') : (cm[1] === '<' || cm[1] === '<=');
        if (cresce) passoTxt = x0 + ' <- ' + x0 + ' + 1';
        else if (desce) passoTxt = x0 + ' <- ' + x0 + ' - 1';
      }
      var recuo = null;
      for (var b = ab + 1; b < fe; b++) if (get(b).trim()) { recuo = ind(get(b)); break; }
      if (recuo === null) recuo = ind(get(ab)) + '   ';
      return ex('laco', 'Linha ' + ab + ' · laço que não termina',
        'O `' + kw + '` depende de `' + cond + '`. Dentro do laço nada muda ' + vs.map(function (x) { return '`' + x + '`'; }).join(', ') + (vals.length ? ' (' + vals.join(', ') + ')' : '') + ', então a condição nunca muda. O site parou depois de 5.000 passos.',
        passoTxt ? 'Sugestão provável: mude `' + x0 + '` a cada volta, com `' + passoTxt + '` antes do `' + (kw === 'enquanto' ? 'fimenquanto' : 'ate') + '`. Confira se é isso que o exercício pede.'
          : 'Mude ' + vs.map(function (x) { return '`' + x + '`'; }).join(', ') + ' dentro do laço, de um jeito que a condição chegue ao fim.',
        passoTxt ? insere(fe - 1, recuo + passoTxt) : null, { rotulo: 'Aplicar sugestão', sugestao: true });
    }
  }

  // diferença entre dois códigos, linha a linha (só o trecho que mudou)
  function diff(a, b) {
    var i = 0, ja = a.length - 1, jb = b.length - 1, out = [];
    while (i <= ja && i <= jb && a[i] === b[i]) i++;
    while (ja >= i && jb >= i && a[ja] === b[jb]) { ja--; jb--; }
    if (ja - i === jb - i) {
      for (var k = i; k <= ja; k++) if (a[k] !== b[k]) { out.push({ s: '-', n: k + 1, t: a[k] }); out.push({ s: '+', n: k + 1, t: b[k] }); }
    } else {
      for (var x = i; x <= ja; x++) out.push({ s: '-', n: x + 1, t: a[x] });
      for (var y = i; y <= jb; y++) out.push({ s: '+', n: y + 1, t: b[y] });
    }
    return out;
  }

  function normalizarSaida(s) {
    return String(s || '').replace(/\r/g, '').split('\n').map(function (l) {
      return l.replace(/(-?\d+(?:\.\d+)?)/g, ' $1 ').replace(/\s+/g, ' ').trim();
    }).join('\n').replace(/\n+$/, '').replace(/^\n+/, '');
  }

  var api = { executar: executar, normalizarSaida: normalizarSaida, validarEntrada: validarEntrada, explicar: explicar };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VisuAlg = api;
})(this);
