/* app.js: the page's behaviour. All arithmetic is in hecon-model.js, which is proved equal to the Python model.
   © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later */
(function () {
  "use strict";
  var M = window.HeconModel, $ = function (id) { return document.getElementById(id); };
  var NS = "http://www.w3.org/2000/svg", css = getComputedStyle(document.documentElement);
  function col(v) { return css.getPropertyValue(v).trim() || "#555"; }
  var COLORS = {comparator: "--muted", harvest: "--water", cultivate: "--leaf"};
  var NAMES = {comparator: "Conventional teaching", harvest: "AI, harvesting only", cultivate: "AI, cultivating"};
  var PRESETS = {default: {}, rich: {cohort_size: 250, faculty_rate: 80, tech_fixed: 30000, governance_fixed: 25000, validity: 0.7},
    lean: {cohort_size: 100, faculty_rate: 15, student_rate: 1, tech_fixed: 8000, tech_per_learner: 10, governance_fixed: 4000, implementation: 15000, maintenance: 3000, cultivation_cost: 4000, validity: 0.5},
    novalid: {validity: 0, capture: 0}};
  var KEYS = ["validity", "ai_practice_mult", "ai_feedback_mult", "cohort_size", "years", "faculty_rate", "automation_share", "tech_fixed", "governance_fixed", "cultivation_cost", "infra_own"];
  var GKEYS = ["players", "c", "s", "r", "f", "B", "k_star"];
  var ROLES = ["visitor", "practitioner", "learner", "teacher", "researcher", "engineer", "institution", "patient"];
  var params = {}, arm = "cultivate";
  function el(name, attrs, text) { var e = document.createElementNS(NS, name); for (var k in attrs) e.setAttribute(k, attrs[k]); if (text != null) e.textContent = text; return e; }
  function fmt(x) { if (x == null) return "none"; var a = Math.abs(x); return a >= 1000 ? Math.round(x).toLocaleString("en-GB") : (a >= 10 ? x.toFixed(0) : x.toFixed(2)); }
  function chart(svg, series, xs) {
    while (svg.firstChild) svg.removeChild(svg.firstChild);
    var W = 600, H = 260, L = 64, R = 16, T = 14, Bm = 44, vals = [];
    series.forEach(function (s) { s.values.forEach(function (v) { if (v != null && isFinite(v)) vals.push(v); }); });
    var lo = Math.min(0, Math.min.apply(null, vals)), hi = Math.max.apply(null, vals); if (hi <= lo) hi = lo + 1;
    var x = function (i) { return L + (W - L - R) * (xs.length > 1 ? i / (xs.length - 1) : 0.5); }, y = function (v) { return T + (H - T - Bm) * (1 - (v - lo) / (hi - lo)); };
    for (var g = 0; g <= 4; g++) { var v = lo + (hi - lo) * g / 4, yy = y(v);
      svg.appendChild(el("line", {x1: L, x2: W - R, y1: yy, y2: yy, stroke: col("--rule")})); svg.appendChild(el("text", {x: L - 8, y: yy + 4, "text-anchor": "end", "font-size": 12, fill: col("--muted")}, fmt(v))); }
    xs.forEach(function (t, i) { if (xs.length <= 12 || i % 2 === 0) svg.appendChild(el("text", {x: x(i), y: H - Bm + 18, "text-anchor": "middle", "font-size": 12, fill: col("--muted")}, "year " + t)); });
    series.forEach(function (s, j) {
      var pts = []; s.values.forEach(function (v, i) { if (v != null && isFinite(v)) pts.push(x(i).toFixed(1) + "," + y(v).toFixed(1)); });
      svg.appendChild(el("polyline", {points: pts.join(" "), fill: "none", stroke: col(s.color), "stroke-width": 2.5}));
      svg.appendChild(el("rect", {x: L + j * 175, y: H - 16, width: 12, height: 4, fill: col(s.color)})); svg.appendChild(el("text", {x: L + 16 + j * 175, y: H - 11, "font-size": 12, fill: col("--ink")}, s.name)); });
    svg.setAttribute("aria-label", series.map(function (s) { return s.name + ": last value " + fmt(s.values[s.values.length - 1]); }).join("; "));
  }
  function field(r) {
    var svg = $("field"); while (svg.firstChild) svg.removeChild(svg.firstChild);
    var a = r.arms[arm], n = r.params.cohort_size, Y = r.years.length, rowH = 310 / Y, maxD = Math.max.apply(null, r.arms.cultivate.D.concat(r.arms.harvest.D)) || 1;
    var maxI = Math.max.apply(null, r.arms.cultivate.I) || 1;
    for (var t = 0; t < Y; t++) {
      var base = 12 + rowH * (t + 1) - 3, soil = arm === "comparator" ? 1.5 : 1.5 + 5 * a.D[t] / maxD;
      svg.appendChild(el("rect", {x: 54, y: base, width: 570, height: soil, fill: col("--soil"), opacity: 0.85}));
      if (arm !== "comparator") svg.appendChild(el("line", {x1: 54, x2: 624, y1: base + soil + 1.5, y2: base + soil + 1.5, stroke: col("--water"), "stroke-width": 1.5, opacity: 0.15 + 0.85 * a.I[t] / maxI}));
      svg.appendChild(el("text", {x: 46, y: base - 2, "text-anchor": "end", "font-size": 11, fill: col("--muted")}, "year " + r.years[t]));
      var tall = Math.round(30 * a.competent[t] / n);
      for (var p = 0; p < 30; p++) { var px = 66 + p * 19, h = p < tall ? rowH * 0.78 : rowH * 0.3;
        svg.appendChild(el("line", {x1: px, x2: px, y1: base, y2: base - h, stroke: col(p < tall ? "--leaf" : "--sprout"), "stroke-width": 3, "stroke-linecap": "round"}));
        if (p < tall) svg.appendChild(el("circle", {cx: px, cy: base - h, r: 2.6, fill: col("--leaf")})); }
    }
    svg.setAttribute("aria-label", NAMES[arm] + ": " + a.cum_competent[Y - 1] + " learners reach the threshold over " + Y + " years");
  }
  function run() {
    var r = M.simulate(params), Y = r.years.length, c = r.arms.cultivate, h = r.arms.harvest, k = r.arms.comparator;
    field(r);
    chart($("c-competent"), ["comparator", "harvest", "cultivate"].map(function (a) { return {name: NAMES[a], color: COLORS[a], values: r.arms[a].competent}; }), r.years);
    chart($("c-cpc"), ["comparator", "harvest", "cultivate"].map(function (a) { return {name: NAMES[a], color: COLORS[a], values: r.arms[a].cost_per_competent}; }), r.years);
    chart($("c-cap"), [{name: "Infrastructure, cultivating", color: "--soil", values: c.D}, {name: "Infrastructure, harvesting", color: "--muted", values: h.D}, {name: "Institutional processes", color: "--water", values: c.I}], r.years);
    var t = $("icer"); Array.prototype.slice.call(t.querySelectorAll("tr")).forEach(function (x) { x.remove(); });
    var head = t.insertRow(); ["Arm", "Competent learners", "Cumulative cost", "Per additional competent learner"].forEach(function (x) { var th = document.createElement("th"); th.textContent = x; head.appendChild(th); });
    ["comparator", "harvest", "cultivate"].forEach(function (a) { var row = t.insertRow(), s = r.arms[a], ic = a === "comparator" ? null : r.icer[a][Y - 1];
      [NAMES[a], s.cum_competent[Y - 1], fmt(s.cum_cost[Y - 1]), ic ? (ic.label === "ratio" ? fmt(ic.value) : ic.label) : "reference"].forEach(function (x) { row.insertCell().textContent = x; }); });
    var ic = r.icer.cultivate[Y - 1], gain = c.cum_competent[Y - 1] - k.cum_competent[Y - 1];
    $("takeaway").textContent = "Over " + Y + " years, cultivating gives " + (gain >= 0 ? gain + " more" : (-gain) + " fewer") + " competent learners than conventional teaching, " +
      (ic.label === "ratio" ? "at " + fmt(ic.value) + " per additional competent learner." : (ic.label === "dominant" ? "and costs less." : "and is " + ic.label + ".")) +
      " It leaves shared infrastructure at " + fmt(c.D[Y - 1]) + " against " + fmt(h.D[Y - 1]) + " for harvesting alone.";
  }
  function game() {
    var g = {}; GKEYS.forEach(function (k) { g[k] = Number($("g_" + k).value); });
    if (g.k_star > g.players) { g.k_star = g.players; $("g_k_star").value = g.players; }
    syncOut("g_");
    var eq = M.equilibria(g), opt = M.optimum(g);
    $("gtext").textContent = "Stable outcomes: " + eq.map(function (k) { return k === 0 ? "nobody contributes" : k + " of " + g.players + " contribute"; }).join(", or ") +
      ". What would serve everyone best: " + opt + " contributing. " + (eq.indexOf(opt) >= 0 ? "That outcome is stable." : "No stable outcome reaches it without recognition, funding or shared maintenance.");
    var starts = [0.1, 0.3, 0.5, 0.7, 0.9], xs = []; for (var i = 0; i <= 120; i += 10) xs.push(i);
    chart($("c-rep"), starts.map(function (x0, j) { var tr = M.replicator(x0, g, 120, 0.05); return {name: "start " + x0, color: ["--signal", "--soil", "--muted", "--water", "--leaf"][j], values: xs.map(function (i) { return tr[i]; })}; }), xs.map(function (i) { return i; }));
    Array.prototype.slice.call($("c-rep").querySelectorAll("text")).forEach(function (tx) { if (/^year /.test(tx.textContent)) tx.textContent = tx.textContent.replace("year ", "round "); });
  }
  function syncOut(prefix) { Array.prototype.slice.call(document.querySelectorAll("output")).forEach(function (o) { var id = o.getAttribute("for"); if (id.indexOf(prefix) === 0 && $(id)) o.textContent = $(id).value; }); }
  function applyPreset(name) {
    var p = {}, k; for (k in M.DEFAULTS) p[k] = M.DEFAULTS[k]; var pr = PRESETS[name] || {}; for (k in pr) p[k] = pr[k]; params = p;
    KEYS.forEach(function (key) { $(key).value = p[key]; }); $("capture").checked = p.capture > 0; syncOut(""); run();
  }
  function setRole(role) {
    Array.prototype.slice.call(document.querySelectorAll("section[data-roles]")).forEach(function (s) { var r = s.getAttribute("data-roles"); s.hidden = !(r === "all" || role === "visitor" || r.split(" ").indexOf(role) >= 0); });
    Array.prototype.slice.call(document.querySelectorAll(".roles button")).forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.role === role)); });
    try { var u = new URL(location.href); u.searchParams.set("role", role); history.replaceState(null, "", u); } catch (e) { /* a page opened from disk cannot rewrite its address; the role still applies */ }
  }
  var NOTEBOOKS = [["01_capital_formation_scenarios.ipynb", "Capital formation scenarios", "The three forms of capital over time, and why AI is an input and not the outcome.", ""],
    ["02_cost_effectiveness_icer.ipynb", "Cost-effectiveness", "ICER per additional competent learner, uncertainty, acceptability curve, tornado and budget impact.", ""],
    ["03_cultivation_game.ipynb", "The cultivation game", "Equilibria, the social optimum and what recognition and funding change.", ""],
    ["04_health_it_ai_lab.ipynb", "Health IT and health-tech AI lab", "De-identification, re-identification risk, dialysis adequacy, reasoning records, a keyless AI tutor and FHIR.", "Hosted here; home: zistgah/marham."],
    ["05_formula_document_workbench.ipynb", "Formula and document conversion workbench", "LaTeX, Unicode, MathML and Word equations, and batch conversion of this paper's files.", "Hosted here; proposed home: zistgah/matba."],
    ["06_mint_with_misty.ipynb", "Mint your own work with Misty DOI", "Metadata, citation formats, a dry run, a MASI journal track, and minting under your own account.", "Hosted here; home: project-ilm/misty-doi."]];
  function notebooks() { var box = $("nblist");
    NOTEBOOKS.forEach(function (n) { var a = document.createElement("article"); a.innerHTML = "<h3></h3><p></p><p class='note'></p><p><a><img alt='Open in Colab' src='https://colab.research.google.com/assets/colab-badge.svg'></a> <a class='gh'>View on GitHub</a></p>";
      a.querySelector("h3").textContent = n[1]; a.querySelectorAll("p")[0].textContent = n[2]; a.querySelectorAll("p")[1].textContent = n[3];
      a.querySelector("a").href = "https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/" + n[0]; a.querySelector(".gh").href = "https://github.com/zistgah/hecon/blob/main/notebooks/" + n[0]; box.appendChild(a); }); }
  function refs() { if (!window.fetch) return;
    var seen = {}; fetch("data/refcheck-report.json").then(function (r) { return r.ok ? r.json() : {results: []}; }).catch(function () { return {results: []}; }).then(function (rep) {
      (rep.results || []).forEach(function (x) { seen[x.id] = x; }); return fetch("data/references.json"); }).then(function (r) { return r.json(); }).then(function (d) { var t = $("refs"), head = t.insertRow();
      d.references.forEach(function (x) { var c = seen[x.id]; if (x.state === "open" && c && (c.state === "verified" || c.state === "reachable")) { x.state = c.state; x.checked = "checked by refcheck on " + c.checked_on + " against " + c.source + (c.finding ? "; " + c.finding : ""); } });
      ["", "Reference", "State", "What was checked, or how it will be"].forEach(function (x) { var th = document.createElement("th"); th.textContent = x; head.appendChild(th); });
      d.references.forEach(function (x) { var row = t.insertRow(); row.insertCell().textContent = x.n || "";
        var c = row.insertCell(); c.textContent = x.title + (x.year ? " (" + x.year + ")" : ""); if (x.doi) { c.appendChild(document.createTextNode(" ")); var a = document.createElement("a"); a.href = "https://doi.org/" + x.doi; a.textContent = x.doi; c.appendChild(a); }
        var s = row.insertCell(); s.textContent = x.state; s.className = "state-" + x.state; row.insertCell().textContent = x.state === "open" ? x.note : x.checked; }); }).catch(function () { $("refs").insertRow().insertCell().textContent = "The reference list could not be loaded here; it is docs/data/references.json in the repository."; }); }
  function doi() { if (!window.fetch) return;
    fetch("https://raw.githubusercontent.com/zistgah/hecon/main/CITATION.cff").then(function (r) { return r.ok ? r.text() : ""; }).then(function (t) { var m = /^doi:\s*(\S+)/m.exec(t || "");
      var p = $("doi"); if (m) { p.textContent = "DOI: "; var a = document.createElement("a"); a.href = "https://doi.org/" + m[1]; a.textContent = m[1]; p.appendChild(a); } else p.textContent = "DOI: not yet minted. The repository records it here once it is."; })
      .catch(function () { $("doi").textContent = "DOI: the repository record could not be reached from this page."; }); }
  function init() {
    ["comparator", "harvest", "cultivate"].forEach(function (a) { var b = document.createElement("button"); b.type = "button"; b.setAttribute("role", "tab"); b.textContent = NAMES[a];
      b.setAttribute("aria-pressed", String(a === arm)); b.onclick = function () { arm = a; Array.prototype.slice.call($("tabs").children).forEach(function (x) { x.setAttribute("aria-pressed", String(x === b)); }); run(); }; $("tabs").appendChild(b); });
    var rb = document.querySelector(".roles"); ROLES.forEach(function (r) { var b = document.createElement("button"); b.type = "button"; b.dataset.role = r; b.textContent = r; b.onclick = function () { setRole(r); }; rb.appendChild(b); });
    KEYS.forEach(function (k) { $(k).addEventListener("input", function () { params[k] = Number($(k).value); syncOut(""); run(); }); });
    $("capture").addEventListener("change", function () { params.capture = $("capture").checked ? 1 : 0; run(); });
    $("preset").addEventListener("change", function () { applyPreset($("preset").value); });
    GKEYS.forEach(function (k) { $("g_" + k).value = M.GAME[k]; $("g_" + k).addEventListener("input", game); });
    notebooks(); applyPreset("default"); game(); refs(); doi();
    var role = new URL(location.href).searchParams.get("role"); setRole(ROLES.indexOf(role) >= 0 ? role : "visitor");
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
