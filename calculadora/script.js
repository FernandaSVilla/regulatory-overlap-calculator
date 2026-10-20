"use strict";
var DOI = ""; // escribir aquí el DOI de Zenodo, p. ej. "10.5281/zenodo.1234567"

var BASE = { r: 7.16, f: 2.72, pdlgd: 2, n: 3, cop: 150, a: 60, q: 10, trev: 0.5, tx: 0.1, P: 40, Cmod: 29277, N: 2500, d: 6 / 19 };
var IDS = ["r", "f", "pdlgd", "n", "cop", "a", "q", "trev", "tx", "P", "Cmod", "N", "d"];
var PROFILES = [["Gran grupo", 250000], ["Entidad mediana", 25000], ["Cooperativa", 2500]];
var LEVELS = [["Sin integración", 0], ["Integración actual", 6 / 19], ["Expediente único", 9 / 19]];

function $(id) { return document.getElementById(id); }
function fmt(x, dec) {
  if (!isFinite(x)) return "–";
  var neg = x < 0, s = Math.abs(x).toFixed(dec).split(".");
  var ent = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ".");
  return (neg ? "−" : "") + ent + (s[1] ? "," + s[1] : "");
}

function sfrac(r, n) {
  var i = r / 12, N = Math.round(n * 12);
  if (N < 1) return NaN;
  var pay = i === 0 ? 1 / N : i / (1 - Math.pow(1 + i, -N));
  var bal = 1, tot = 0;
  for (var k = 0; k < N; k++) { tot += bal; bal = bal * (1 + i) - pay; }
  return tot / N;
}

function read() {
  var p = {};
  IDS.forEach(function (k) { p[k] = parseFloat($(k).value); });
  return {
    r: p.r / 100, f: p.f / 100, pdlgd: p.pdlgd / 100, n: p.n, cop: p.cop,
    a: p.a / 100, q: p.q / 100, trev: p.trev, tx: p.tx, P: p.P, Cmod: p.Cmod, N: p.N, d: p.d
  };
}

function creg(p) { return (1 - p.a) / p.a * (p.q * p.trev + p.tx) * p.P; }
function cmod(p) { return p.Cmod * (1 - p.d) / p.N; }
function denom(p) { return (p.r - p.f - p.pdlgd) * sfrac(p.r, p.n) * p.n; }
function Lstar(p) { return (p.cop + creg(p) + cmod(p)) / denom(p); }
function dL(p) { return (creg(p) + cmod(p)) / denom(p); }
function withv(p, k, v) { var o = {}; for (var j in p) o[j] = p[j]; o[k] = v; return o; }

function setText(id, t) { var e = $(id); if (e) e.textContent = t; }

function update() {
  var p = read();
  var den = denom(p), s = sfrac(p.r, p.n);
  var cr = creg(p), cm = cmod(p);
  var bad = !(den > 0);
  $("warn").style.display = bad ? "block" : "none";
  setText("o_m", fmt(den * 100, 1) + " céntimos");
  setText("o_creg", fmt(cr, 2) + " €");
  setText("o_cmod", fmt(cm, 2) + " €");
  setText("o_ctot", fmt(cr + cm, 2) + " €");
  setText("o_L0", bad ? "–" : fmt(p.cop / den, 0) + " €");
  setText("o_L", bad ? "–" : fmt(Lstar(p), 0) + " €");
  setText("o_dL", bad ? "–" : fmt(dL(p), 0) + " €");
  setText("o_rel", bad ? "–" : fmt(100 * dL(p) / (p.cop / den), 1) + " %");
  setText("o_Nstar", cr > 0 ? fmt(p.Cmod * (1 - p.d) / cr, 0) + " préstamos al año por modelo" : "–");
  drawSens(p, bad);
  drawVolume(p, bad);
}

/* ---------- Figura 1: sensibilidad ---------- */
function drawSens(p, bad) {
  var svg = $("fig1"); svg.innerHTML = "";
  if (bad) return;
  var L0 = Lstar(p);
  var items = [
    ["Tipo de interés, r", "r", false], ["Coste de financiación, f", "f", false], ["Plazo, n", "n", false],
    ["Pérdida esperada", "pdlgd", false], ["Coste por modelo, C_mod", "Cmod", true], ["Coste por hora, P", "P", true],
    ["Revisión, q", "q", true], ["Tiempo de revisión, t_rev", "trev", true], ["Explicación, t_x", "tx", true]
  ].map(function (it) {
    var lo = Lstar(withv(p, it[1], p[it[1]] * 0.8)) - L0;
    var hi = Lstar(withv(p, it[1], p[it[1]] * 1.2)) - L0;
    return { lab: it[0], lo: lo, hi: hi, reg: it[2] };
  }).filter(function (o) { return isFinite(o.lo) && isFinite(o.hi); });
  items.sort(function (a, b) { return (Math.abs(b.hi) + Math.abs(b.lo)) - (Math.abs(a.hi) + Math.abs(a.lo)); });
  var W = 460, left = 150, right = 20, top = 14, rowh = 28;
  var H = top + items.length * rowh + 46;
  svg.setAttribute("viewBox", "0 0 " + W + " " + H);
  var m = 0; items.forEach(function (o) { m = Math.max(m, Math.abs(o.lo), Math.abs(o.hi)); });
  m = m * 1.08 || 1;
  var x0 = left + (W - left - right) / 2, sc = (W - left - right) / 2 / m;
  var out = [];
  items.forEach(function (o, i) {
    var y = top + i * rowh;
    out.push('<text x="' + (left - 6) + '" y="' + (y + 14) + '" text-anchor="end">' + o.lab + '</text>');
    var fill = o.reg ? "#555" : "#bbb";
    [o.lo, o.hi].forEach(function (v) {
      var x = v < 0 ? x0 + v * sc : x0, w = Math.abs(v) * sc;
      out.push('<rect x="' + x.toFixed(1) + '" y="' + (y + 4) + '" width="' + Math.max(w, 0.5).toFixed(1) + '" height="14" fill="' + fill + '" stroke="#000" stroke-width="0.6"/>');
    });
  });
  var ya = top + items.length * rowh + 4;
  out.push('<line x1="' + x0 + '" y1="' + (top - 4) + '" x2="' + x0 + '" y2="' + ya + '" stroke="#000" stroke-width="0.8"/>');
  out.push('<line x1="' + left + '" y1="' + ya + '" x2="' + (W - right) + '" y2="' + ya + '" stroke="#000" stroke-width="0.8"/>');
  var step = niceStep(m);
  for (var t = -Math.floor(m / step) * step; t <= m; t += step) {
    var x = x0 + t * sc;
    out.push('<line x1="' + x.toFixed(1) + '" y1="' + ya + '" x2="' + x.toFixed(1) + '" y2="' + (ya + 4) + '" stroke="#000" stroke-width="0.8"/>');
    out.push('<text x="' + x.toFixed(1) + '" y="' + (ya + 16) + '" text-anchor="middle">' + fmt(t, 0) + '</text>');
  }
  out.push('<text x="' + ((left + W - right) / 2) + '" y="' + (ya + 30) + '" text-anchor="middle">Cambio de L* (€) respecto de ' + fmt(L0, 0) + ' €</text>');
  svg.innerHTML = out.join("");
}

function niceStep(m) {
  var raw = m / 3, p10 = Math.pow(10, Math.floor(Math.log10(raw))), r = raw / p10;
  return (r < 1.5 ? 1 : r < 3.5 ? 2 : r < 7.5 ? 5 : 10) * p10;
}

/* ---------- Figura 2: ΔL* frente al volumen ---------- */
function drawVolume(p, bad) {
  var svg = $("fig2"); svg.innerHTML = "";
  if (bad) return;
  var W = 460, H = 290, l = 54, r = 16, t = 14, b = 46;
  var xmin = Math.log10(500), xmax = Math.log10(500000);
  var dashes = ["", "6,4", "2,3"];
  var curves = LEVELS.map(function (lv) {
    var pts = [];
    for (var k = 0; k <= 80; k++) {
      var lx = xmin + (xmax - xmin) * k / 80, N = Math.pow(10, lx);
      pts.push([lx, dL(withv(withv(p, "N", N), "d", lv[1]))]);
    }
    return pts;
  });
  var ymax = 0; curves.forEach(function (c) { c.forEach(function (q) { ymax = Math.max(ymax, q[1]); }); });
  var ystep = niceStep(ymax); ymax = Math.ceil(ymax / ystep) * ystep;
  function X(lx) { return l + (lx - xmin) / (xmax - xmin) * (W - l - r); }
  function Y(v) { return H - b - v / ymax * (H - t - b); }
  var out = [];
  out.push('<line x1="' + l + '" y1="' + (H - b) + '" x2="' + (W - r) + '" y2="' + (H - b) + '" stroke="#000" stroke-width="0.8"/>');
  out.push('<line x1="' + l + '" y1="' + t + '" x2="' + l + '" y2="' + (H - b) + '" stroke="#000" stroke-width="0.8"/>');
  for (var v = 0; v <= ymax + 1e-9; v += ystep) {
    out.push('<line x1="' + (l - 4) + '" y1="' + Y(v).toFixed(1) + '" x2="' + l + '" y2="' + Y(v).toFixed(1) + '" stroke="#000" stroke-width="0.8"/>');
    out.push('<text x="' + (l - 7) + '" y="' + (Y(v) + 4).toFixed(1) + '" text-anchor="end">' + fmt(v, 0) + '</text>');
  }
  [1000, 10000, 100000].forEach(function (N) {
    var x = X(Math.log10(N));
    out.push('<line x1="' + x.toFixed(1) + '" y1="' + (H - b) + '" x2="' + x.toFixed(1) + '" y2="' + (H - b + 4) + '" stroke="#000" stroke-width="0.8"/>');
    out.push('<text x="' + x.toFixed(1) + '" y="' + (H - b + 16) + '" text-anchor="middle">' + fmt(N, 0) + '</text>');
  });
  out.push('<text x="' + ((l + W - r) / 2) + '" y="' + (H - 8) + '" text-anchor="middle">Préstamos aprobados por modelo al año, N</text>');
  out.push('<text transform="translate(13,' + ((t + H - b) / 2) + ') rotate(-90)" text-anchor="middle">ΔL* (€)</text>');
  curves.forEach(function (c, i) {
    var d = c.map(function (q, k) { return (k ? "L" : "M") + X(q[0]).toFixed(1) + "," + Y(q[1]).toFixed(1); }).join("");
    out.push('<path d="' + d + '" fill="none" stroke="#000" stroke-width="1.2"' + (dashes[i] ? ' stroke-dasharray="' + dashes[i] + '"' : "") + '/>');
  });
  if (p.N >= 500 && p.N <= 500000) {
    var xn = X(Math.log10(p.N));
    out.push('<line x1="' + xn.toFixed(1) + '" y1="' + t + '" x2="' + xn.toFixed(1) + '" y2="' + (H - b) + '" stroke="#888" stroke-width="0.8"/>');
  }
  var lx0 = W - r - 150, ly0 = t + 6;
  LEVELS.forEach(function (lv, i) {
    var y = ly0 + i * 15;
    out.push('<line x1="' + lx0 + '" y1="' + y + '" x2="' + (lx0 + 26) + '" y2="' + y + '" stroke="#000" stroke-width="1.2"' + (dashes[i] ? ' stroke-dasharray="' + dashes[i] + '"' : "") + '/>');
    out.push('<text x="' + (lx0 + 32) + '" y="' + (y + 4) + '">' + lv[0] + '</text>');
  });
  svg.innerHTML = out.join("");
}

/* ---------- Controles ---------- */
function syncSelects() {
  var q = parseFloat($("q").value) / 100;
  $("design").value = Math.abs(q - 0.10) < 1e-9 ? "0.10" : Math.abs(q - 1) < 1e-9 ? "1" : "custom";
  var N = parseFloat($("N").value), pv = "custom";
  PROFILES.forEach(function (pr) { if (pr[1] === N) pv = String(N); });
  $("profile").value = pv;
  var d = parseFloat($("d").value), dv = "custom";
  LEVELS.forEach(function (lv, i) { if (Math.abs(lv[1] - d) < 1e-3) dv = $("integ").options[i].value; });
  $("integ").value = dv;
}

function reset() {
  IDS.forEach(function (k) {
    var v = BASE[k];
    $(k).value = k === "d" ? v.toFixed(4) : v;
  });
  syncSelects(); update();
}

$("design").addEventListener("change", function () {
  if (this.value !== "custom") $("q").value = parseFloat(this.value) * 100;
  update();
});
$("profile").addEventListener("change", function () {
  if (this.value !== "custom") $("N").value = this.value;
  update();
});
$("integ").addEventListener("change", function () {
  if (this.value !== "custom") $("d").value = parseFloat(this.value).toFixed(4);
  update();
});
IDS.forEach(function (k) { $(k).addEventListener("input", function () { syncSelects(); update(); }); });
$("reset").addEventListener("click", reset);
if (DOI) { $("doi").innerHTML = 'DOI: <a href="https://doi.org/' + DOI + '">' + DOI + '</a>'; }
reset();