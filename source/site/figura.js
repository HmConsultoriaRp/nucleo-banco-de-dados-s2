/* Desenho das figuras de Geometria em canvas: 2d (plano com grade) ou 3d (eixo z para cima, gira arrastando).
   Figura.montar(canvas, fig) -> { redesenhar(), vista(nome), trocar(novaFig) } */
(function (root) {
  'use strict';
  function cssVar(nome, padrao) {
    var v = getComputedStyle(document.body).getPropertyValue(nome);
    return (v && v.trim()) || padrao;
  }
  function cores() {
    return {
      1: cssVar('--blue', '#356b73'),
      2: cssVar('--coral', '#d4643f'),
      3: cssVar('--ocre', '#b5871f'),
      4: cssVar('--ink', '#20251f'),
      linha: cssVar('--line', '#d9d2c5'),
      eixo: cssVar('--muted', '#6a6f67'),
    };
  }
  function p3(c) { return [c[0], c[1], c.length > 2 ? c[2] : 0]; }
  function fmtN(x) { return String(Math.round(x * 100) / 100).replace('.', ','); }
  function fonte(peso, px) { return peso + ' ' + px + 'px ' + cssVar('--font-body', 'system-ui'); }

  function montar(canvas, figInicial) {
    var fig, modo, centro, raio, caixa;
    var yaw = -0.62, pitch = 0.42;
    var ctx = canvas.getContext('2d');

    function prepara(f) {
      fig = f || { itens: [] };
      modo = fig.modo === '2d' ? '2d' : '3d';
      var pts = fig.semEixos ? [] : [[0, 0, 0]];
      (fig.itens || []).forEach(function (it) {
        if (it.de) pts.push(p3(it.de));
        if (it.ate) pts.push(p3(it.ate));
        if (it.em) pts.push(p3(it.em));
        if (it.pts) it.pts.forEach(function (q) { pts.push(p3(q)); });
      });
      (fig.moldura || []).forEach(function (q) { pts.push(p3(q)); });
      var mn = [Infinity, Infinity, Infinity], mx = [-Infinity, -Infinity, -Infinity];
      pts.forEach(function (q) { for (var i = 0; i < 3; i++) { mn[i] = Math.min(mn[i], q[i]); mx[i] = Math.max(mx[i], q[i]); } });
      for (var i = 0; i < 3; i++) { if (mx[i] - mn[i] < 1) { mx[i] += 0.5; mn[i] -= 0.5; } }
      caixa = { mn: mn.slice(), mx: mx.slice() };
      centro = [(mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2, modo === '2d' ? 0 : (mn[2] + mx[2]) / 2];
      raio = 0;
      pts.forEach(function (q) {
        var dx = q[0] - centro[0], dy = q[1] - centro[1], dz = modo === '2d' ? 0 : q[2] - centro[2];
        raio = Math.max(raio, Math.sqrt(dx * dx + dy * dy + dz * dz));
      });
      if (raio < 1) raio = 1;
      canvas.style.cursor = modo === '3d' ? 'grab' : 'default';
      canvas.style.touchAction = modo === '3d' ? 'none' : 'auto';
    }

    function proj(q, W, H, esc) {
      var x = q[0] - centro[0], y = q[1] - centro[1], z = q[2] - centro[2];
      if (modo === '2d') return [W / 2 + x * esc, H / 2 - y * esc];
      var X = x * Math.cos(yaw) - y * Math.sin(yaw);
      var Y = x * Math.sin(yaw) + y * Math.cos(yaw);
      var Z2 = z * Math.cos(pitch) + Y * Math.sin(pitch);
      return [W / 2 + X * esc, H / 2 - Z2 * esc];
    }
    function seta(a, b, cor, largura) {
      ctx.strokeStyle = cor; ctx.fillStyle = cor; ctx.lineWidth = largura; ctx.lineCap = 'round';
      var ang = Math.atan2(b[1] - a[1], b[0] - a[0]), len = Math.hypot(b[0] - a[0], b[1] - a[1]);
      var h = Math.min(13, len * 0.45);
      var fimX = b[0] - Math.cos(ang) * h * 0.6, fimY = b[1] - Math.sin(ang) * h * 0.6;
      ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(fimX, fimY); ctx.stroke();
      if (len < 2) return;
      ctx.beginPath();
      ctx.moveTo(b[0], b[1]);
      ctx.lineTo(b[0] - h * Math.cos(ang - 0.42), b[1] - h * Math.sin(ang - 0.42));
      ctx.lineTo(b[0] - h * Math.cos(ang + 0.42), b[1] - h * Math.sin(ang + 0.42));
      ctx.closePath(); ctx.fill();
    }
    function rotulo(txt, x, y, cor, vetor) {
      if (!txt) return;
      ctx.font = '600 13px ' + cssVar('--font-body', 'system-ui');
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      var w = ctx.measureText(txt).width;
      ctx.save();
      ctx.fillStyle = cssVar('--white', '#fffdf8'); ctx.globalAlpha = 0.85;
      ctx.fillRect(x - w / 2 - 3, y - (vetor ? 15 : 9), w + 6, vetor ? 24 : 18);
      ctx.restore();
      ctx.fillStyle = cor;
      ctx.fillText(txt, x, y);
      if (vetor) {
        ctx.strokeStyle = cor; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(x - w / 2, y - 10); ctx.lineTo(x + w / 2, y - 10); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x + w / 2, y - 10); ctx.lineTo(x + w / 2 - 4, y - 13); ctx.moveTo(x + w / 2, y - 10); ctx.lineTo(x + w / 2 - 4, y - 7); ctx.stroke();
      }
    }

    function desenhar() {
      if (!canvas.isConnected) return;
      var dpr = window.devicePixelRatio || 1;
      var W = canvas.clientWidth || 480, H = canvas.clientHeight || 340;
      if (canvas.width !== Math.round(W * dpr) || canvas.height !== Math.round(H * dpr)) {
        canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);
      var C = cores();
      var esc = Math.min(W, H) / 2 / (raio * 1.18);

      if (modo === '2d') {
        var passo = 1, alcance = Math.max(W, H) / esc;
        if (alcance > 60) passo = 10; else if (alcance > 30) passo = 5; else if (alcance > 16) passo = 2;
        ctx.strokeStyle = C.linha; ctx.lineWidth = 1; ctx.globalAlpha = 0.7;
        var x0 = Math.floor((centro[0] - W / 2 / esc) / passo) * passo, x1 = centro[0] + W / 2 / esc;
        for (var gx = x0; gx <= x1; gx += passo) { var a = proj([gx, 0, 0], W, H, esc); ctx.beginPath(); ctx.moveTo(a[0], 0); ctx.lineTo(a[0], H); ctx.stroke(); }
        var y0 = Math.floor((centro[1] - H / 2 / esc) / passo) * passo, y1 = centro[1] + H / 2 / esc;
        for (var gy = y0; gy <= y1; gy += passo) { var b = proj([0, gy, 0], W, H, esc); ctx.beginPath(); ctx.moveTo(0, b[1]); ctx.lineTo(W, b[1]); ctx.stroke(); }
        ctx.globalAlpha = 1;
        var o = proj([0, 0, 0], W, H, esc);
        ctx.strokeStyle = C.eixo; ctx.lineWidth = 1.2;
        ctx.beginPath(); ctx.moveTo(0, o[1]); ctx.lineTo(W, o[1]); ctx.moveTo(o[0], 0); ctx.lineTo(o[0], H); ctx.stroke();
      } else if (!fig.semEixos) {
        // chao quadriculado (plano xy, z = 0) e eixos firmes com marcas numeradas
        var vao = Math.max(caixa.mx[0] - caixa.mn[0], caixa.mx[1] - caixa.mn[1], caixa.mx[2] - caixa.mn[2]);
        var pas = vao <= 8 ? 1 : vao <= 16 ? 2 : vao <= 40 ? 5 : 10;
        var lim = function (i, lado) {
          var v = lado < 0 ? Math.min(0, caixa.mn[i]) : Math.max(0, caixa.mx[i]);
          return lado < 0 ? Math.floor(v / pas) * pas : Math.ceil(v / pas) * pas;
        };
        var gx0 = lim(0, -1), gx1 = lim(0, 1), gy0 = lim(1, -1), gy1 = lim(1, 1), gz0 = lim(2, -1), gz1 = lim(2, 1);
        ctx.strokeStyle = C.linha; ctx.lineWidth = 1; ctx.globalAlpha = 0.8;
        for (var u = gx0; u <= gx1 + 1e-9; u += pas) {
          var g1 = proj([u, gy0, 0], W, H, esc), g2 = proj([u, gy1, 0], W, H, esc);
          ctx.beginPath(); ctx.moveTo(g1[0], g1[1]); ctx.lineTo(g2[0], g2[1]); ctx.stroke();
        }
        for (var v = gy0; v <= gy1 + 1e-9; v += pas) {
          var g3 = proj([gx0, v, 0], W, H, esc), g4 = proj([gx1, v, 0], W, H, esc);
          ctx.beginPath(); ctx.moveTo(g3[0], g3[1]); ctx.lineTo(g4[0], g4[1]); ctx.stroke();
        }
        ctx.globalAlpha = 1;
        [[0, gx0, gx1 + pas * 0.7, 'x'], [1, gy0, gy1 + pas * 0.7, 'y'], [2, gz0, gz1 + pas * 0.7, 'z']].forEach(function (e) {
          var ini = [0, 0, 0], fim = [0, 0, 0];
          ini[e[0]] = e[1]; fim[e[0]] = e[2];
          var a = proj(ini, W, H, esc), b = proj(fim, W, H, esc);
          seta(a, b, C.eixo, 1.5);
          var dx = b[0] - a[0], dy = b[1] - a[1], l = Math.hypot(dx, dy) || 1;
          ctx.font = fonte(700, 13); ctx.fillStyle = C.eixo; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
          if (l > 4) ctx.fillText(e[3], b[0] + dx / l * 12, b[1] + dy / l * 12);
          ctx.font = fonte(500, 10);
          for (var t = Math.ceil(e[1] / pas) * pas; t <= e[2] - pas * 0.6; t += pas) {
            if (Math.abs(t) < 1e-9) continue;
            var p = [0, 0, 0]; p[e[0]] = t;
            var m = proj(p, W, H, esc);
            ctx.beginPath(); ctx.arc(m[0], m[1], 1.8, 0, Math.PI * 2); ctx.fill();
            ctx.fillText(fmtN(t), m[0] + (e[0] === 2 ? -12 : 0), m[1] + (e[0] === 2 ? 0 : 10));
          }
        });
        var o3 = proj([0, 0, 0], W, H, esc);
        ctx.fillText('0', o3[0] - 9, o3[1] + 9);
      }
      alvos = [];

      var ordem = { poligono: 0, segmento: 1, vetor: 2, ponto: 3 };
      (fig.itens || []).slice().sort(function (a, b) { return (ordem[a.tipo] || 0) - (ordem[b.tipo] || 0); }).forEach(function (it) {
        var cor = C[it.cor || (it.tipo === 'ponto' ? 4 : 1)] || C[1];
        if (it.tipo === 'poligono') {
          var ps = it.pts.map(function (q) { return proj(p3(q), W, H, esc); });
          ctx.beginPath(); ctx.moveTo(ps[0][0], ps[0][1]);
          for (var k = 1; k < ps.length; k++) ctx.lineTo(ps[k][0], ps[k][1]);
          if (!it.aberto) { ctx.closePath(); ctx.globalAlpha = 0.10; ctx.fillStyle = cor; ctx.fill(); ctx.globalAlpha = 1; }
          ctx.strokeStyle = cor; ctx.lineWidth = 1.6; ctx.stroke();
        } else if (it.tipo === 'segmento') {
          var a2 = proj(p3(it.de), W, H, esc), b2 = proj(p3(it.ate), W, H, esc);
          ctx.strokeStyle = it.cor ? cor : C.eixo; ctx.lineWidth = it.largura || 1.4;
          if (it.tracejado) ctx.setLineDash([5, 5]);
          ctx.beginPath(); ctx.moveTo(a2[0], a2[1]); ctx.lineTo(b2[0], b2[1]); ctx.stroke();
          ctx.setLineDash([]);
        } else if (it.tipo === 'vetor') {
          var a3 = proj(p3(it.de), W, H, esc), b3 = proj(p3(it.ate), W, H, esc);
          seta(a3, b3, cor, 3);
          if (it.rot) {
            var dx = b3[0] - a3[0], dy = b3[1] - a3[1], len = Math.hypot(dx, dy) || 1;
            rotulo(it.rot, (a3[0] + b3[0]) / 2 - dy / len * 16, (a3[1] + b3[1]) / 2 + dx / len * 16, cor, true);
          }
        } else if (it.tipo === 'ponto') {
          var q = proj(p3(it.em), W, H, esc);
          ctx.fillStyle = cor; ctx.beginPath(); ctx.arc(q[0], q[1], 4.5, 0, Math.PI * 2); ctx.fill();
          if (it.rot) rotulo(it.rot, q[0] + 13, q[1] - 12, cor, false);
          alvos.push({ it: it, x: q[0], y: q[1] });
        }
      });

      // coordenadas do ponto apontado (mouse) ou tocado (celular)
      var alvo = dica && alvos.filter(function (p) { return p.it === dica; })[0];
      if (alvo) {
        var c = p3(dica.em);
        var txt = (dica.rot ? dica.rot + ' ' : '') + '(' + fmtN(c[0]) + '; ' + fmtN(c[1]) + (modo === '2d' ? '' : '; ' + fmtN(c[2])) + ')';
        ctx.font = fonte(600, 12);
        var bw = ctx.measureText(txt).width + 16, bh = 24;
        var bx = Math.min(Math.max(alvo.x - bw / 2, 4), W - bw - 4), by = alvo.y - 38;
        if (by < 4) by = alvo.y + 14;
        ctx.strokeStyle = C[4]; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(alvo.x, alvo.y, 8, 0, Math.PI * 2); ctx.stroke();
        ctx.fillStyle = C[4]; ctx.globalAlpha = 0.92; ctx.fillRect(bx, by, bw, bh); ctx.globalAlpha = 1;
        ctx.fillStyle = cssVar('--white', '#fffdf8'); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(txt, bx + bw / 2, by + bh / 2);
      }
    }

    var arrasto = null, toque = null, dica = null, alvos = [];
    function pontoEm(x, y, alcance) {
      var melhor = null, dmin = alcance;
      alvos.forEach(function (p) { var d = Math.hypot(p.x - x, p.y - y); if (d <= dmin) { dmin = d; melhor = p.it; } });
      return melhor;
    }
    canvas.addEventListener('pointerdown', function (e) {
      toque = { x: e.clientX, y: e.clientY };
      if (modo !== '3d') return;
      arrasto = { x: e.clientX, y: e.clientY, yaw: yaw, pitch: pitch };
      try { canvas.setPointerCapture(e.pointerId); } catch (err) { /* sem captura */ }
      canvas.style.cursor = 'grabbing';
    });
    canvas.addEventListener('pointermove', function (e) {
      if (arrasto) {
        yaw = arrasto.yaw + (e.clientX - arrasto.x) * 0.011;
        pitch = Math.max(-1.45, Math.min(1.45, arrasto.pitch + (e.clientY - arrasto.y) * 0.011));
        desenhar();
        return;
      }
      if (e.pointerType !== 'mouse') return;
      var h = pontoEm(e.offsetX, e.offsetY, 12);
      canvas.style.cursor = h ? 'pointer' : (modo === '3d' ? 'grab' : 'default');
      if (h !== dica) { dica = h; desenhar(); }
    });
    function solta() { arrasto = null; if (modo === '3d') canvas.style.cursor = 'grab'; }
    canvas.addEventListener('pointerup', function (e) {
      if (toque && Math.hypot(e.clientX - toque.x, e.clientY - toque.y) < 6) {
        var h = pontoEm(e.offsetX, e.offsetY, e.pointerType === 'mouse' ? 12 : 22);
        dica = e.pointerType === 'mouse' ? h : (h && h !== dica ? h : null);
        desenhar();
      }
      toque = null;
      solta();
    });
    canvas.addEventListener('pointercancel', function () { toque = null; solta(); });
    canvas.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse' && dica && !arrasto) { dica = null; desenhar(); } });

    // angulo inicial proprio da figura (opcional): { yaw, pitch }
    var yaw0 = -0.62, pitch0 = 0.42;
    function anguloDe(f) {
      var a = f && f.angulo;
      if (a && (a.yaw !== yaw0 || a.pitch !== pitch0)) { yaw0 = a.yaw; pitch0 = a.pitch; yaw = yaw0; pitch = pitch0; }
    }
    anguloDe(figInicial);
    prepara(figInicial);
    desenhar();
    return {
      redesenhar: desenhar,
      trocar: function (f) { dica = null; anguloDe(f); prepara(f); desenhar(); },
      vista: function (nome) {
        if (nome === 'frente') { yaw = 0; pitch = 0; }
        else if (nome === 'cima') { yaw = 0; pitch = 1.45; }
        else { yaw = yaw0; pitch = pitch0; }
        desenhar();
      },
      get modo() { return modo; },
      canvas: canvas,
    };
  }
  root.Figura = { montar: montar };
})(this);
