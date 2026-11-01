/* Interpretador de um subconjunto do VisuAlg 3.0, com teste de mesa.
   Uso: VisuAlg.executar(codigo, entradas) -> { saida, passos, erro, ordem, decl }
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
      if (c === ' ' || c === '\t' || c === '\r') { i++; continue; }
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
      if ('+-*/\\^%()[],:=<>'.indexOf(c) >= 0) { toks.push({ t: 'op', v: c, linha: linha }); i++; continue; }
      throw new ErroVA('símbolo inesperado: ' + c, linha);
    }
    toks.push({ t: 'eof', v: '', linha: linha });
    return toks;
  }

  // ---------- analisador sintático ----------
  function parse(toks) {
    var p = 0;
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
        if (bt.t !== 'kw' || ['inteiro', 'real', 'caractere', 'caracter', 'literal', 'logico'].indexOf(bt.v) < 0) throw new ErroVA('tipo do vetor desconhecido', bt.linha);
        return { base: normTipo(bt.v), dims: dims };
      }
      throw new ErroVA('tipo desconhecido: ' + mostra(t), t.linha);
    }

    expectKw('algoritmo');
    var nome = '';
    if (peek().t === 'str') nome = next().v;
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
    return { nome: nome, decl: decl, ordem: ordem, corpo: corpo, linhaInicio: ini.linha, linhaFim: fim.linha };

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
      return { nome: t.v, idx: idx, linha: t.linha };
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
        if (!isOp('<-')) throw new ErroVA('esperava "<-" depois de "' + t.raw + '"', linha);
        next();
        return { k: 'atrib', nome: t.v, idx: idx, e: expr(), linha: linha };
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
            if (!isOp(')')) { args.push(expr()); while (isOp(',')) { next(); args.push(expr()); } }
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
        if (isOp('[')) {
          next();
          var idx = [expr()];
          while (isOp(',')) { next(); idx.push(expr()); }
          expectOp(']');
          return { k: 'var', nome: t.v, idx: idx, linha: t.linha };
        }
        return { k: 'var', nome: t.v, idx: null, linha: t.linha };
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

  function executar(codigo, entradas, opts) {
    opts = opts || {};
    var MAX = opts.maxPassos || 5000;
    var res = { saida: '', passos: [], erro: null, ordem: [], decl: {}, nomes: [] };
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
    prog.ordem.forEach(function (n) {
      var d = prog.decl[n];
      if (d.tipo.dims) {
        var tam = 1;
        d.tipo.dims.forEach(function (dm) { tam *= (dm[1] - dm[0] + 1); });
        var dados = [];
        for (var i = 0; i < tam; i++) dados.push(inicial(d.tipo.base));
        mem[n] = { vetor: true, dims: d.tipo.dims, dados: dados };
      } else mem[n] = inicial(d.tipo.base);
    });
    var fila = (entradas || []).map(String);
    var saida = '';
    var INTERROMPA = { interrompa: true };

    function txtVar(v) {
      if (v && v.vetor) return '[' + v.dados.map(fmt).join(', ') + ']';
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
    function ler(nome, idx, linha) {
      var d = decl(nome, linha), cel = mem[nome];
      if (idx) return cel.dados[posicao(nome, idx, linha)];
      if (cel.vetor) throw new ErroVA('use ' + d.raw + '[índice] para ler uma posição do vetor', linha);
      return cel;
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
    function atribuir(nome, idx, val, linha) {
      var d = decl(nome, linha), cel = mem[nome];
      var v = converte(val, d.tipo.base, linha, d.raw);
      if (idx) cel.dados[posicao(nome, idx, linha)] = v;
      else {
        if (cel.vetor) throw new ErroVA('não dá para atribuir a um vetor inteiro de uma vez (' + d.raw + ')', linha);
        mem[nome] = v;
      }
    }
    function nomeAlvo(nome, idx) {
      var raw = prog.decl[nome] ? prog.decl[nome].raw : nome;
      if (!idx) return raw;
      return raw + '[' + idx.map(function (e) { return fmt(ev(e)); }).join(',') + ']';
    }
    function entrada(txt, base, linha) {
      var t = txt.trim();
      if (base === 'inteiro') {
        if (!/^[+-]?\d+$/.test(t)) throw new ErroVA('a entrada "' + txt + '" não é um número inteiro', linha);
        return { tipo: 'i', v: parseInt(t, 10) };
      }
      if (base === 'real') {
        var tt = t.replace(',', '.');
        if (!/^[+-]?(\d+\.?\d*|\.\d+)$/.test(tt)) throw new ErroVA('a entrada "' + txt + '" não é um número', linha);
        return { tipo: 'r', v: parseFloat(tt) };
      }
      if (base === 'logico') {
        var l = semAcento(t.toLowerCase());
        if (l === 'verdadeiro' || l === 'v') return { tipo: 'b', v: true };
        if (l === 'falso' || l === 'f') return { tipo: 'b', v: false };
        throw new ErroVA('a entrada "' + txt + '" não é lógica (use VERDADEIRO ou FALSO)', linha);
      }
      return { tipo: 's', v: txt };
    }
    function num(a, linha, op) {
      if (a.tipo !== 'i' && a.tipo !== 'r') throw new ErroVA('a operação "' + op + '" precisa de números, recebeu ' + NOME_TIPO[a.tipo], linha);
    }
    function logi(a, linha, op) {
      if (a.tipo !== 'b') throw new ErroVA('"' + op + '" precisa de valor lógico, recebeu ' + NOME_TIPO[a.tipo], linha);
    }
    function compara(a, b, linha) {
      if ((a.tipo === 'i' || a.tipo === 'r') && (b.tipo === 'i' || b.tipo === 'r')) return a.v < b.v ? -1 : a.v > b.v ? 1 : 0;
      if (a.tipo === 's' && b.tipo === 's') return a.v < b.v ? -1 : a.v > b.v ? 1 : 0;
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
        case 'var': return ler(e.nome, e.idx, e.linha);
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
          atribuir(s.nome, s.idx, val, s.linha);
          passo(s.linha, nomeAlvo(s.nome, s.idx) + ' recebe ' + (val.tipo === 's' ? '"' + val.v + '"' : fmt(val)));
          return;
        }
        case 'leia': {
          s.alvos.forEach(function (a) {
            if (!fila.length) throw new ErroVA('o programa pediu uma entrada (leia) e a lista de entradas acabou', s.linha);
            var txt = fila.shift();
            var d = decl(a.nome, s.linha);
            atribuir(a.nome, a.idx, entrada(txt, d.tipo.base, s.linha), s.linha);
            passo(s.linha, 'leu ' + txt + ' para ' + nomeAlvo(a.nome, a.idx));
          });
          return;
        }
        case 'escreva': {
          // o VisuAlg escreve número com um espaço antes (ver Exemplos\decomp.alg: escreval(p[j], ex[j]))
          var txt = '';
          s.args.forEach(function (a) { var v = ev(a); txt += (v.tipo === 'i' || v.tipo === 'r') ? ' ' + fmt(v) : fmt(v); });
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

  function normalizarSaida(s) {
    return String(s || '').replace(/\r/g, '').split('\n').map(function (l) {
      return l.replace(/(-?\d+(?:\.\d+)?)/g, ' $1 ').replace(/\s+/g, ' ').trim();
    }).join('\n').replace(/\n+$/, '').replace(/^\n+/, '');
  }

  var api = { executar: executar, normalizarSaida: normalizarSaida };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.VisuAlg = api;
})(this);
