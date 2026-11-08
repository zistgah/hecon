// Parity: the browser model must give the same numbers as the Python model.
// © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later
const { execFileSync } = require("child_process"); const path = require("path");
const M = require(path.join(__dirname, "..", "docs", "hecon-model.js"));
const SC = [{}, {validity: 0.0, capture: 0.0}, {validity: 1.0, ai_practice_mult: 2.2, tech_fixed: 80000}, {years: 6, cohort_size: 37, infra_own: 0.0, threshold: 70}];
const GM = [{}, {r: 4}, {B: 2, k_star: 5, players: 12}, {f: 3.5, c: 7}];
const py = JSON.parse(execFileSync("python3", ["-c", `
import json,sys; sys.path.insert(0, ${JSON.stringify(path.join(__dirname, ".."))})
from hecon import model, game
sc=json.loads(sys.argv[1]); gm=json.loads(sys.argv[2])
print(json.dumps({"sims":[model.simulate(p) for p in sc],"games":[{"eq":game.equilibria(g),"opt":game.optimum(g),"w":[game.welfare(k,g) for k in range(int(dict(game.DEFAULTS,**g)["players"])+1)],"rep":game.replicator(0.3,g)} for g in gm]}))
`, JSON.stringify(SC), JSON.stringify(GM)]).toString());
let n = 0, bad = [];
function same(a, b, where) { n++;
  if (a === null || b === null || typeof a !== "number") { if (JSON.stringify(a) !== JSON.stringify(b)) bad.push(where + ": " + a + " vs " + b); return; }
  if (Number.isInteger(a) && Number.isInteger(b)) { if (a !== b) bad.push(where + ": " + a + " vs " + b); return; }
  if (Math.abs(a - b) > 1e-9 * Math.max(1, Math.abs(a), Math.abs(b))) bad.push(where + ": " + a + " vs " + b); }
SC.forEach((p, i) => { const js = M.simulate(p), pyr = py.sims[i];
  M.ARMS.forEach(arm => Object.keys(pyr.arms[arm]).forEach(key => pyr.arms[arm][key].forEach((v, t) => same(js.arms[arm][key][t], v, `sim${i}.${arm}.${key}[${t}]`))));
  ["harvest", "cultivate"].forEach(arm => pyr.icer[arm].forEach((v, t) => { same(js.icer[arm][t].label, v.label, `sim${i}.icer.${arm}[${t}].label`); same(js.icer[arm][t].value, v.value, `sim${i}.icer.${arm}[${t}].value`); })); });
GM.forEach((g, i) => { const p = py.games[i];
  same(JSON.stringify(M.equilibria(g)), JSON.stringify(p.eq), `game${i}.eq`); same(M.optimum(g), p.opt, `game${i}.opt`);
  p.w.forEach((w, k) => same(M.welfare(k, g), w, `game${i}.w[${k}]`)); p.rep.forEach((x, t) => same(M.replicator(0.3, g)[t], x, `game${i}.rep[${t}]`)); });
if (bad.length) { console.log("parity: FAIL " + bad.length + " of " + n); bad.slice(0, 12).forEach(b => console.log("   " + b)); process.exit(1); }
console.log("parity: " + n + " values agree between Python and JavaScript");
