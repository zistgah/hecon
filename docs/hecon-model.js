/* hecon-model.js: the same scenario model as hecon/model.py and hecon/game.py, for the browser.
   tests/parity.js runs both and requires agreement. Every number is an assumption the user sets.
   © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later */
(function (root) {
  "use strict";
  var DEFAULTS = {years: 10, cohort_size: 150, terms: 4, k0_mean: 40.0, k0_sd: 10.0, eff_sd: 0.25, threshold: 60.0,
    delta_term: 0.05, eta: 9.0, w_practice: 0.4, w_feedback: 0.3, w_experience: 0.3, ai_practice_mult: 1.6,
    ai_feedback_mult: 1.5, validity: 0.6, capture: 1.0, inst_dep: 0.10, inst_invest: 0.5, infra_initial: 1.0,
    infra_dep: 0.12, infra_own: 0.6, infra_ext: 0.2, infra_cost_effect: 0.35, faculty_hours: 20.0, faculty_rate: 50.0,
    student_hours: 30.0, student_rate: 5.0, automation_share: 0.4, supervision_hours: 4.0, tech_fixed: 20000.0,
    tech_per_learner: 30.0, implementation: 50000.0, governance_fixed: 15000.0, cases: 40.0, validation_per_case: 200.0,
    maintenance: 10000.0, cultivation_cost: 12000.0, graduate_dep: 0.05, cap_a: 0.5, cap_b: 0.25, cap_c: 0.25};
  var ARMS = ["comparator", "harvest", "cultivate"];
  var A = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00];
  var B = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01];
  var C = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00];
  var D = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00];
  function invNorm(p) {
    var plow = 0.02425, q, r;
    if (p < plow) { q = Math.sqrt(-2.0 * Math.log(p)); return (((((C[0]*q+C[1])*q+C[2])*q+C[3])*q+C[4])*q+C[5]) / ((((D[0]*q+D[1])*q+D[2])*q+D[3])*q+1.0); }
    if (p <= 1.0 - plow) { q = p - 0.5; r = q * q; return (((((A[0]*r+A[1])*r+A[2])*r+A[3])*r+A[4])*r+A[5])*q / (((((B[0]*r+B[1])*r+B[2])*r+B[3])*r+B[4])*r+1.0); }
    q = Math.sqrt(-2.0 * Math.log(1.0 - p)); return -(((((C[0]*q+C[1])*q+C[2])*q+C[3])*q+C[4])*q+C[5]) / ((((D[0]*q+D[1])*q+D[2])*q+D[3])*q+1.0);
  }
  function icer(dc, de) {
    if (de > 0 && dc <= 0) return {label: "dominant", value: null};
    if (de <= 0 && dc >= 0) return {label: (de < 0 || dc > 0) ? "dominated" : "no difference", value: null};
    if (de > 0) return {label: "ratio", value: dc / de};
    return {label: "cheaper, less effective", value: dc / de};
  }
  function simulate(params) {
    var p = {}, k; for (k in DEFAULTS) p[k] = DEFAULTS[k]; for (k in (params || {})) p[k] = params[k];
    var T = Math.trunc(p.years), n = Math.trunc(p.cohort_size), terms = Math.trunc(p.terms), i, t, j;
    var z = [], k0 = [], eff = [];
    for (i = 0; i < n; i++) { z.push(invNorm((i + 0.5) / n)); k0.push(p.k0_mean + p.k0_sd * z[i]); eff.push(Math.max(0.05, 1.0 + p.eff_sd * z[i])); }
    var out = {params: p, years: [], arms: {}, icer: {}}; for (t = 1; t <= T; t++) out.years.push(t);
    ARMS.forEach(function (arm) {
      var I = 0.0, Dk = p.infra_initial, H = 0.0, cumC = 0.0, cumE = 0;
      var s = {competent: [], mean_k: [], cost: [], cum_cost: [], cum_competent: [], cost_per_competent: [], I: [], D: [], H: [], capacity: []};
      for (t = 0; t < T; t++) {
        var P, F, uI;
        if (arm === "comparator") { P = 1.0; F = 1.0; uI = 0.0; }
        else { uI = I / (I + 1.0); var v = p.validity * (0.5 + 0.5 * uI); P = 1.0 + (p.ai_practice_mult - 1.0) * v; F = 1.0 + (p.ai_feedback_mult - 1.0) * v; }
        var g = Math.pow(P, p.w_practice) * Math.pow(F, p.w_feedback) * Math.pow(1.0, p.w_experience);
        var competent = 0, totalK = 0.0;
        for (i = 0; i < n; i++) {
          var phi = p.eta * eff[i] * g, kk = k0[i];
          for (j = 0; j < terms; j++) { kk = (1.0 - p.delta_term) * kk + phi; if (kk > 100.0) kk = 100.0; }
          totalK += kk; if (kk >= p.threshold) competent += 1;
        }
        var students = n * p.student_hours * p.student_rate, cost;
        if (arm === "comparator") cost = n * p.faculty_hours * p.faculty_rate + students;
        else {
          var fac = n * (p.faculty_hours * (1.0 - p.automation_share * uI) + p.supervision_hours) * p.faculty_rate;
          var kap = 1.0 + p.infra_cost_effect * Dk;
          var tech = p.tech_fixed / kap + n * p.tech_per_learner;
          var impl = (t === 0) ? p.implementation / kap : 0.0;
          var gov = p.governance_fixed + p.cases * p.validation_per_case;
          var cult = (arm === "cultivate") ? p.cultivation_cost : 0.0;
          cost = fac + students + tech + impl + gov + p.maintenance + cult;
        }
        H = (1.0 - p.graduate_dep) * H + competent;
        var cap = Math.pow(H, p.cap_a) * Math.pow(1.0 + I, p.cap_b) * Math.pow(1.0 + Dk, p.cap_c);
        cumC += cost; cumE += competent;
        s.competent.push(competent); s.mean_k.push(totalK / n); s.cost.push(cost); s.cum_cost.push(cumC);
        s.cum_competent.push(cumE); s.cost_per_competent.push(cumE > 0 ? cumC / cumE : null);
        s.I.push(I); s.D.push(Dk); s.H.push(H); s.capacity.push(cap);
        if (arm !== "comparator") {
          I = (1.0 - p.inst_dep) * I + p.inst_invest * p.capture;
          Dk = (1.0 - p.infra_dep) * Dk + p.infra_ext + (arm === "cultivate" ? p.infra_own : 0.0);
        }
      }
      out.arms[arm] = s;
    });
    var comp = out.arms.comparator;
    ["harvest", "cultivate"].forEach(function (arm) {
      var a = out.arms[arm], list = [];
      for (t = 0; t < T; t++) list.push(icer(a.cum_cost[t] - comp.cum_cost[t], a.cum_competent[t] - comp.cum_competent[t]));
      out.icer[arm] = list;
    });
    return out;
  }
  var GAME = {players: 8, R: 10.0, s: 2.0, r: 0.0, c: 6.0, f: 0.0, nb: 1.0, B: 8.0, k_star: 3};
  function gg(g) { var o = {}, k; for (k in GAME) o[k] = GAME[k]; for (k in (g || {})) o[k] = g[k]; return o; }
  function bonus(k, g) { return k >= g.k_star ? g.B : 0.0; }
  function payC(k, g) { return g.R + g.s + g.r - (g.c - g.f) + g.nb * k + bonus(k, g); }
  function payH(k, g) { return g.R + g.nb * k + bonus(k, g); }
  function equilibria(g0) { var g = gg(g0), N = Math.trunc(g.players), out = [], k;
    for (k = 0; k <= N; k++) { var ok = true; if (k > 0 && payC(k, g) < payH(k - 1, g)) ok = false; if (k < N && payH(k, g) < payC(k + 1, g)) ok = false; if (ok) out.push(k); }
    return out; }
  function welfare(k, g0) { var g = gg(g0), N = Math.trunc(g.players); return N * g.R + k * (g.s + g.r - g.c) + N * g.nb * k + N * bonus(k, g); }
  function optimum(g0) { var g = gg(g0), N = Math.trunc(g.players), best = 0, k; for (k = 1; k <= N; k++) if (welfare(k, g) > welfare(best, g)) best = k; return best; }
  function comb(n, k) { var c = 1, i; for (i = 1; i <= k; i++) c = c * (n - k + i) / i; return c; }
  function pmf(n, k, x) { if (k < 0 || k > n) return 0.0; return comb(n, k) * Math.pow(x, k) * Math.pow(1.0 - x, n - k); }
  function gain(x, g0) { var g = gg(g0), N = Math.trunc(g.players), ks = Math.trunc(g.k_star); return g.s + g.r - g.c + g.f + g.nb + g.B * pmf(N - 1, ks - 1, x); }
  function replicator(x0, g0, steps, rate) { var g = gg(g0), xs = [x0], x = x0, i; steps = steps || 60; rate = rate || 0.05;
    for (i = 0; i < steps; i++) { x = x + rate * x * (1.0 - x) * gain(x, g); x = x > 1.0 ? 1.0 : (x < 0.0 ? 0.0 : x); xs.push(x); } return xs; }
  var api = {DEFAULTS: DEFAULTS, ARMS: ARMS, invNorm: invNorm, icer: icer, simulate: simulate,
    GAME: GAME, equilibria: equilibria, welfare: welfare, optimum: optimum, gain: gain, replicator: replicator};
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.HeconModel = api;
})(typeof globalThis !== "undefined" ? globalThis : this);
