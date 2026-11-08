#!/usr/bin/env python3
"""Generates every notebook in notebooks/ from this one source (contract C43: surfaces are generated, never hand-edited).
Notebook 05 is the author's Formula and Document Conversion Workbench, carried from origin/received with the
changes listed in origin/SEED-DIFF.md.
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later"""
import copy, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "notebooks"); os.makedirs(NB, exist_ok=True)
REPO = "zistgah/hecon"; COLAB = "https://colab.research.google.com/github/%s/blob/main/notebooks/%%s" % REPO
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
NOTICE = ("© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI. Code GPL-3.0-or-later; text CC BY-SA 4.0. "
          "AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary; AyeCNSe™ (Indian TM application No. 7415871, pending). "
          "Cite with [CITATION.cff](https://github.com/%s/blob/main/CITATION.cff); the DOI is recorded in the repository README once minted." % REPO)
HOW = ("**How to use it.** Press ▶ on each step in order, or choose Runtime, then Run all. Each step's code is hidden behind its title; "
       "double-click the title to see it. Educational use only: nothing here is a medical device or a finding.")
SETUP = ('#@title Set up: load the hecon package from the repository { display-mode: "form" }\n'
         'import subprocess, sys\nREPO = "zistgah/hecon"  #@param {type:"string"}\ntry:\n    import hecon\nexcept ImportError:\n'
         '    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "git+https://github.com/%s@main" % REPO], check=True)\n'
         '    import hecon\nprint(hecon.NOTICE)')
def md(t): return {"cell_type": "markdown", "metadata": {}, "source": t.strip("\n")}
def code(t): return {"cell_type": "code", "metadata": {"cellView": "form"}, "execution_count": None, "outputs": [], "source": t.strip("\n")}
def header(fname, title, what, home=None):
    h = "# %s\n\n[![Open in Colab](%s)](%s)\n\n%s\n\n%s\n\n%s" % (title, BADGE, COLAB % fname, what, HOW, NOTICE)
    if home:
        h += ("\n\n**Where this notebook lives.** It is hosted in zistgah/hecon until it moves to its home, %s. "
              "The move and the link back are listed in [COMPONENTS.md](https://github.com/%s/blob/main/COMPONENTS.md)." % (home, REPO))
    return md(h)
def save(fname, cells, gpu=False):
    for i, c in enumerate(cells): c["id"] = "%s-%02d" % (fname[:2], i)
    meta = {"colab": {"name": fname, "provenance": [], "toc_visible": True}, "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"}}
    if gpu: meta["accelerator"] = "GPU"
    json.dump({"nbformat": 4, "nbformat_minor": 5, "metadata": meta, "cells": cells}, open(os.path.join(NB, fname), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
PARAMS = '''#@title Your assumptions { display-mode: "form" }
validity = 0.6  #@param {type:"slider", min:0, max:1, step:0.05}
ai_practice_mult = 1.6  #@param {type:"slider", min:1, max:3, step:0.1}
ai_feedback_mult = 1.5  #@param {type:"slider", min:1, max:3, step:0.1}
capture = 1.0  #@param {type:"slider", min:0, max:1, step:1}
cohort_size = 150  #@param {type:"integer"}
years = 10  #@param {type:"integer"}
tech_fixed = 20000  #@param {type:"number"}
governance_fixed = 15000  #@param {type:"number"}
cultivation_cost = 12000  #@param {type:"number"}
from hecon import model
P = dict(validity=validity, ai_practice_mult=ai_practice_mult, ai_feedback_mult=ai_feedback_mult, capture=capture,
         cohort_size=cohort_size, years=years, tech_fixed=tech_fixed, governance_fixed=governance_fixed, cultivation_cost=cultivation_cost)
R = model.simulate(P)
print(model.report(R))'''
def nb01():
    f = "01_capital_formation_scenarios.ipynb"
    save(f, [header(f, "Productive capacity: capital formation scenarios",
        "The paper's three forms of capital, run as a scenario model: learner clinical-reasoning capital, institutional "
        "educational-process capital and shared digital-infrastructure capital, compared across conventional teaching (comparator), "
        "AI-assisted teaching that only harvests existing tools (harvest), and AI-assisted teaching that also contributes back (cultivate)."),
     md("## The model, in the paper's terms\n\nLearner capability accumulates and depreciates (paper, section 3.3):\n\n"
        "$$K_{i,t+1} = (1-\\delta)K_{i,t} + \\varphi(P_{i,t}, F_{i,t}, E_{i,t})$$\n\n"
        "Practice $P$ and feedback $F$ rise with AI only to the extent that its questions and feedback are aligned with defined "
        "competencies (the *validity* setting). Institutional and shared capital follow $X_{t+1} = (1-\\Delta)X_t + J_t$ (section 10.4), and "
        "productive capacity is shown in the illustrative form $P_t = H_t^{a}(1+I_t)^{b}(1+D_t)^{c}$ (section 10.3). "
        "Every number is an assumption you set; the defaults only make the mechanics visible. They are not estimates."),
     code(SETUP),
     md("## Step 1: set your assumptions\n\n*validity* is how well AI questions and feedback map to defined competencies and validated measures (0 none, 1 complete). "
        "*capture* switches structured reasoning records on (1) or off (0); records are what build institutional capital. The costs are in any currency you choose, per year."),
     code(PARAMS),
     md("## Step 2: read the trajectories\n\nThe first chart counts learners who reach the competency threshold each year. The second shows the capital stocks "
        "behind them. A higher count is not by itself a reason to adopt: it has to be weighed against cost, which notebook 02 does."),
     code('''#@title Draw the trajectories { display-mode: "form" }
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for arm in model.ARMS:
    ax[0].plot(R["years"], R["arms"][arm]["competent"], marker="o", label=arm)
    ax[1].plot(R["years"], R["arms"][arm]["capacity"], label=arm)
ax[0].set_title("Learners reaching the threshold, per cohort"); ax[0].set_xlabel("year"); ax[0].legend()
ax[1].set_title("Productive capacity index (illustrative)"); ax[1].set_xlabel("year"); ax[1].legend()
plt.tight_layout(); plt.show()'''),
     md("## Step 3: AI is an input, not the outcome (Proposition 2)\n\nWith validity at zero the AI arms produce more activity and no extra competence. "
        "The sweep below shows how the gain depends on validity alone, with everything else held at your settings."),
     code('''#@title Sweep validity from 0 to 1 { display-mode: "form" }
vals = [i / 10 for i in range(11)]
gain = [sum(model.simulate(dict(P, validity=v))["arms"]["harvest"]["competent"]) - sum(R["arms"]["comparator"]["competent"]) for v in vals]
plt.figure(figsize=(6, 3.5)); plt.plot(vals, gain, marker="o")
plt.title("Extra competent learners over the horizon"); plt.xlabel("validity"); plt.axhline(0, color="grey", lw=0.8); plt.show()
print("At validity 0 the extra competent learners are", gain[0])'''),
     md("## Step 4: harvesting and cultivating\n\nCultivation costs money every year. What it buys is shared infrastructure $D$, which lowers the cost of the "
        "next deployment for this institution and for others. The chart shows both stocks."),
     code('''#@title Shared infrastructure and institutional capital { display-mode: "form" }
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
for arm in ("harvest", "cultivate"):
    ax[0].plot(R["years"], R["arms"][arm]["D"], label=arm); ax[1].plot(R["years"], R["arms"][arm]["I"], label=arm)
ax[0].set_title("Shared digital-infrastructure capital D"); ax[1].set_title("Institutional process capital I")
for a in ax: a.set_xlabel("year"); a.legend()
plt.tight_layout(); plt.show()'''),
     md("## What this does not show\n\nThe functional forms and parameters need empirical estimation (paper, section 14). Use this notebook to make "
        "assumptions explicit and to see which ones decide the answer, then measure those in a study (section 12).")])
def nb02():
    f = "02_cost_effectiveness_icer.ipynb"
    save(f, [header(f, "Cost-effectiveness of AI-assisted CBME",
        "The incremental cost-effectiveness ratio per additional competent learner, its uncertainty, an acceptability curve, "
        "one-way sensitivity and budget impact (paper, section 6). Every number is an assumption you set."),
     code(SETUP),
     md("## Step 1: the ratio and its four quadrants\n\n$$ICER = \\frac{C_{AI} - C_{C}}{E_{AI} - E_{C}}$$\n\nHere $E$ is the number of learners reaching the "
        "competency threshold. *Dominant* means more competent learners for less money; *dominated* means fewer or the same for more money; "
        "only the other two quadrants give a ratio worth reading."),
     code(PARAMS + '''
for arm in ("harvest", "cultivate"):
    ic = R["icer"][arm][-1]
    print(arm, "vs comparator, cumulative:", ("%.0f per additional competent learner" % ic["value"]) if ic["label"] == "ratio" else ic["label"])'''),
     md("## Step 2: uncertainty and the acceptability curve\n\nThe probabilistic analysis draws the uncertain parameters from ranges around your values "
        "(the ranges are listed in `hecon.economics.UNCERTAIN`). The curve shows, for each amount you would pay per additional competent "
        "learner, the share of draws in which cultivation is worth it."),
     code('''#@title Probabilistic sensitivity analysis { display-mode: "form" }
from hecon import economics
import matplotlib.pyplot as plt
draws = 300  #@param {type:"integer"}
S = economics.psa(P, n=draws, arm="cultivate")
W = [0, 1000, 2000, 3000, 4000, 6000, 8000, 12000, 16000]
C = economics.ceac(S, W)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].scatter([de for dc, de in S], [dc for dc, de in S], s=8); ax[0].axhline(0, color="grey", lw=0.8); ax[0].axvline(0, color="grey", lw=0.8)
ax[0].set_xlabel("extra competent learners"); ax[0].set_ylabel("extra cost"); ax[0].set_title("Cost-effectiveness plane")
ax[1].plot([w for w, _ in C], [p for _, p in C], marker="o"); ax[1].set_ylim(0, 1)
ax[1].set_xlabel("willingness to pay per additional competent learner"); ax[1].set_title("Acceptability curve"); plt.tight_layout(); plt.show()'''),
     md("## Step 3: which assumption decides the answer\n\nOne-way sensitivity moves one parameter at a time to 75 and 125 per cent of your value. "
        "The longest bar is the assumption to measure first."),
     code('''#@title One-way sensitivity { display-mode: "form" }
ref, rows = economics.one_way(P, arm="cultivate")
rows = [r for r in rows if r[1] is not None and r[2] is not None]
rows.sort(key=lambda r: abs(r[2] - r[1]))
plt.figure(figsize=(7, 4))
for i, (k, lo, hi) in enumerate(rows):
    plt.plot([lo, hi], [i, i], lw=6)
plt.yticks(range(len(rows)), [r[0] for r in rows]); plt.xlabel("ICER at 75% and 125% of the value"); plt.title("Tornado"); plt.show()'''),
     md("## Step 4: budget impact\n\nThe extra cost each year compared with conventional teaching, which is what an institution has to find."),
     code('''#@title Budget impact { display-mode: "form" }
bi = economics.budget_impact(R, "cultivate")
plt.figure(figsize=(7, 3.5)); plt.bar(R["years"], bi); plt.axhline(0, color="grey", lw=0.8)
plt.xlabel("year"); plt.title("Extra cost per year, cultivate vs comparator"); plt.show()'''),
     md("## Knowledge is not competence\n\nThe pooled evidence the paper cites measures knowledge acquisition, not clinical reasoning: Wei and colleagues (2025) "
        "pooled four randomised trials for knowledge (SMD 0.46, 95% CI 0.18 to 0.73, P = .001) and could not pool clinical reasoning because of "
        "methodological and measurement heterogeneity. *Evidence state: verified on 5 November 2026 against the full text in PubMed Central "
        "(PMC12268559).* Do not enter a knowledge effect as if it were a competence effect. Report any completed evaluation with CHEERS 2022.")])
def nb03():
    f = "03_cultivation_game.ipynb"
    save(f, [header(f, "The cultivation game",
        "Section 9 of the paper as a game: institutions choose to cultivate shared open infrastructure or to harvest it. "
        "The notebook finds the equilibria, the social optimum and how recognition, funding or shared maintenance move them."),
     code(SETUP),
     md("## Step 1: payoffs\n\nWith $k$ contributors, a contributor gets $R + s + r - (c - f) + n_b k + B[k \\ge k^*]$ and a harvester "
        "$R + n_b k + B[k \\ge k^*]$: $s$ private benefit, $r$ recognition, $c$ cost, $f$ funding, $n_b$ what each contribution gives everyone, "
        "and $B$ what a maintained commons gives everyone once $k^*$ contributors sustain it."),
     code('''#@title Your game { display-mode: "form" }
from hecon import game
players = 8  #@param {type:"integer"}
s = 2.0  #@param {type:"number"}
r = 0.0  #@param {type:"number"}
c = 6.0  #@param {type:"number"}
f = 0.0  #@param {type:"number"}
nb = 1.0  #@param {type:"number"}
B = 8.0  #@param {type:"number"}
k_star = 3  #@param {type:"integer"}
G = dict(players=players, s=s, r=r, c=c, f=f, nb=nb, B=B, k_star=k_star)
eq = game.equilibria(G); opt = game.optimum(G)
print("Equilibria (number of contributors):", eq)
print("Social optimum:", opt, "contributors")
for k in sorted(set(eq + [opt])): print("  welfare with %d contributors: %.1f" % (k, game.welfare(k, G)))'''),
     md("## Step 2: reading it\n\nWith the defaults there are two equilibria, nobody contributes or exactly $k^*$ do, and both fall short of the optimum. "
        "That is the collective-action problem of section 9.3: cultivation can be stable, but only once enough others cultivate."),
     md("## Step 3: how a population drifts\n\nIf institutions copy what pays, the share that cultivates follows the replicator dynamic below. "
        "Starting points above the tipping share climb; those below fall away."),
     code('''#@title Replicator dynamics { display-mode: "form" }
import matplotlib.pyplot as plt
plt.figure(figsize=(7, 4))
for x0 in [0.05, 0.15, 0.25, 0.35, 0.5, 0.7, 0.9]:
    plt.plot(game.replicator(x0, G, steps=120), label="start %.2f" % x0)
plt.ylim(0, 1); plt.xlabel("rounds"); plt.ylabel("share cultivating"); plt.legend(fontsize=7); plt.show()'''),
     md("## Step 4: what moves the equilibrium\n\nRecognition $r$ and funding $f$ both change the private return to contributing. The table shows the equilibria for each pair."),
     code('''#@title Recognition and funding { display-mode: "form" }
for rr in [0, 1, 2, 3, 4]:
    print("r=%d " % rr + "  ".join("f=%d:%s" % (ff, game.equilibria(dict(G, r=rr, f=ff))) for ff in [0, 1, 2, 3]))'''),
     md("## Testing it\n\nWhether institutions that cultivate achieve lower duplication and more sustainable infrastructure is testable (section 9.4). "
        "Contributions can be verified with the estate's CVAS harness, which has its own Colab notebook: "
        "[zistgah/cvas, notebooks/cvas-cloud-harness.ipynb](https://colab.research.google.com/github/zistgah/cvas/blob/main/notebooks/cvas-cloud-harness.ipynb).")])
def nb04():
    f = "04_health_it_ai_lab.ipynb"
    save(f, [header(f, "Health IT and health-tech AI lab for medicos",
        "Hands-on steps behind sections 4 and 7 of the paper, on a synthetic case (no real person): de-identification before anything is derived, "
        "re-identification risk, dialysis adequacy and kidney function, structured reasoning records, a Socratic AI tutor with a keyless path, "
        "a grounding check on AI output and a FHIR R4 export.", home="zistgah/marham, the estate's health-informatics layer"),
     md("## Global privacy, by default\n\nThe steps follow the strictest of the major frameworks, so that they hold wherever a case comes from: the EU GDPR "
        "(Regulation (EU) 2016/679), the US HIPAA Privacy Rule (45 CFR 164.514(b), Safe Harbor and Expert Determination), the UK Data Protection Act 2018, "
        "India's Digital Personal Data Protection Act 2023 and ICMR 2017 guidelines, Brazil's LGPD (Law 13.709/2018), South Africa's POPIA (2013) and Kenya's "
        "Data Protection Act 2019, with the Declaration of Helsinki (2024), the CIOMS guidelines (2016) and WHO guidance on AI for health (2021). "
        "Where two of them differ, the stricter requirement is used. This notebook teaches; it is not legal advice."),
     code(SETUP),
     md("## Step 1: the synthetic case\n\nA chronic kidney disease patient on haemodialysis, the paper's own example (section 4.1). Every name, number and address in it is invented."),
     code('''#@title Show the case { display-mode: "form" }
from hecon import health
print(health.CASE_TEXT)'''),
     md("## Step 2: screen before deriving\n\nIdentifiers are removed while the text is intact, before anything is extracted from it. Removing names is not enough "
        "(section 7.1): record numbers, dates, addresses, ages over 89 and contact details identify people too. National numbers are checked with their own "
        "checksums (NHS modulus 11, Verhoeff for 12-digit identity numbers), and a number that fails the checksum is still removed."),
     code('''#@title De-identify and measure { display-mode: "form" }
clean, report = health.deidentify(health.CASE_TEXT, names=health.CASE_NAMES)
print(clean); print(); print("Found:", report["counts"])
ev = health.evaluate(clean, health.GOLD_IDENTIFIERS, health.CLINICAL_VALUES)
print("Identifiers removed: %d of %d; clinical values kept: %d of %d" % (ev["removed"], ev["identifiers"], ev["retained"], ev["clinical_values"]))
print("Missed:", ev["missed"] or "none", "| Lost:", ev["lost"] or "none")'''),
     md("## Step 3: shifting dates keeps the intervals\n\nFor research records, dates can be moved by one secret offset per patient, so intervals between events survive."),
     code('''#@title Shift dates by an offset { display-mode: "form" }
offset_days = 137  #@param {type:"integer"}
print(health.deidentify(health.CASE_TEXT, names=health.CASE_NAMES, date_shift_days=offset_days)[0][:420])'''),
     md("## Step 4: re-identification risk in a table\n\n*k-anonymity* is the size of the smallest group sharing the same quasi-identifiers; k = 1 means someone is unique. "
        "*l-diversity* asks whether each group still holds more than one diagnosis. Generalising age and region raises k."),
     code('''#@title k-anonymity and l-diversity { display-mode: "form" }
rows = health.synthetic_cohort(); qis = ["age", "sex", "region"]
print("raw: k =", health.k_anonymity(rows, qis))
for band, merge in [(10, False), (30, False), (60, True)]:
    g = health.generalise(rows, age_band=band, region_map={r: "all regions" for r in ("North", "South", "East", "West")} if merge else None)
    print("age band %d, regions merged %s: k = %d, l = %d" % (band, merge, health.k_anonymity(g, qis), health.l_diversity(g, qis, "diagnosis")))'''),
     md("## Step 5: kidney function and dialysis adequacy\n\neGFR by the CKD-EPI 2021 creatinine equation without a race term (Inker et al., 2021), the urea reduction "
        "ratio, and single-pool Kt/V by the second-generation Daugirdas formula. Education only: check against your local laboratory and guidelines."),
     code('''#@title Calculate { display-mode: "form" }
c = health.CASE
egfr = health.egfr_ckd_epi_2021(health.creatinine_umol_to_mgdl(c["creatinine_umol_l"]), c["age"], female=False)
print("eGFR: %.1f mL/min/1.73 m2" % egfr)
print("URR: %.1f %%" % health.urr(c["urea_pre"], c["urea_post"]))
print("Kt/V: %.2f" % health.ktv_daugirdas2(c["urea_pre"], c["urea_post"], c["session_hours"], c["uf_litres"], c["post_weight_kg"]))'''),
     md("## Step 6: a structured reasoning record\n\nThe record captures what a learner states, not private thought (section 4.2). It is checked against a schema and "
        "matched to the case's key features. The match is a crude aid for a teacher, never a grade on its own."),
     code('''#@title Validate and score a record { display-mode: "form" }
import json
record = {"learner": "L-017", "case_id": health.CASE["id"],
          "problem_representation": "Man on maintenance haemodialysis with hyperkalaemia and palpitations after a missed session",
          "differentials": [{"diagnosis": "hyperkalaemia from a missed session", "for": ["potassium 6.4", "missed session"], "against": []}],
          "information_sought": ["ECG", "medicine history", "diet"],
          "decisions": [{"decision": "urgent dialysis", "rationale": "potassium 6.4 mmol/L with palpitations"}],
          "uncertainty": "ECG not yet seen; medicine list incomplete"}
print("Schema problems:", health.validate_record(record) or "none")
print(json.dumps(health.score_record(record), indent=1))'''),
     md("## Step 7: a Socratic question ladder\n\nQuestions mapped to the five domains of the UK clinical reasoning consensus (Cooper et al., 2021) and to cognitive levels."),
     code('''#@title Show the ladder { display-mode: "form" }
for dom, level, q in health.socratic_ladder(): print("%-45s %-9s %s" % (dom, level, q))'''),
     md("## Step 8: an AI tutor, with no lock-in\n\nChoose a provider. *rule-based* needs no model, no key and no network. *local* runs an open-weight model in this notebook "
        "(Qwen2.5 0.5B on any runtime; the same family the Hindawi LLM notebooks use). *endpoint* uses any OpenAI-compatible service with your own key, typed when asked "
        "and never stored. Whatever answers, the grounding check lists every number the tutor wrote that is not in the case, for a teacher to check."),
     code('''#@title Ask the tutor { display-mode: "form" }
provider = "rule-based"  #@param ["rule-based", "local", "endpoint"]
local_model = "Qwen/Qwen2.5-0.5B-Instruct"  #@param ["Qwen/Qwen2.5-0.5B-Instruct", "Qwen/Qwen2.5-3B-Instruct", "Qwen/Qwen2.5-7B-Instruct"]
endpoint_url = "http://localhost:11434/v1"  #@param {type:"string"}
endpoint_model = "llama3.1"  #@param {type:"string"}
learner_says = "I think this is fluid overload, so I would give diuretics."  #@param {type:"string"}
if provider == "local":
    p = health.LocalProvider(local_model)
elif provider == "endpoint":
    from getpass import getpass
    p = health.EndpointProvider(endpoint_url, endpoint_model, getpass("API key (leave empty if none): "))
else:
    p = health.RuleProvider()
answer = p.complete(health.tutor_messages(health.deidentify(health.CASE_TEXT, names=health.CASE_NAMES)[0], learner_says))
print("[%s]" % p.name, answer)
print("Numbers to check against the case:", health.grounding(answer, health.CASE_TEXT) or "none")'''),
     md("## Step 9: a FHIR R4 export\n\nThe de-identified case as a FHIR Bundle. Codes are left out on purpose: a code comes from a terminology service, never from memory. "
        "Set *lookup* to search a public FHIR terminology server for candidates; that step needs the internet and was not run when this notebook was built."),
     code('''#@title Build, validate and optionally look up codes { display-mode: "form" }
import json, subprocess, sys
bundle = health.fhir_bundle()
print(json.dumps(bundle, indent=1)[:900], "...")
try:
    try:
        import fhir.resources  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "fhir.resources"], check=True)
    from fhir.resources.R4B.bundle import Bundle
    (Bundle.model_validate if hasattr(Bundle, "model_validate") else Bundle.parse_obj)(bundle)
    print("Validated against the FHIR R4B models in fhir.resources.")
except Exception as e:
    print("Not validated here:", e.__class__.__name__, str(e)[:160])
lookup = False  #@param {type:"boolean"}
term = "potassium serum"  #@param {type:"string"}
if lookup:
    import urllib.parse, urllib.request
    url = "https://tx.fhir.org/r4/ValueSet/$expand?" + urllib.parse.urlencode({"url": "http://loinc.org/vs", "filter": term, "count": 5})
    vs = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"Accept": "application/fhir+json"}), timeout=60))
    for c in vs.get("expansion", {}).get("contains", []): print(c.get("system"), c.get("code"), c.get("display"))'''),
     md("## Step 10: keep what you made\n\nThe de-identified case, the record and the bundle are written to a folder, and offered for download in Colab."),
     code('''#@title Save the artefacts { display-mode: "form" }
import os
os.makedirs("hecon_outputs", exist_ok=True)
open("hecon_outputs/case_deidentified.txt", "w").write(clean)
json.dump(record, open("hecon_outputs/reasoning_record.json", "w"), indent=1)
json.dump(bundle, open("hecon_outputs/fhir_bundle.json", "w"), indent=1)
print(sorted(os.listdir("hecon_outputs")))
try:
    from google.colab import files
    for n in sorted(os.listdir("hecon_outputs")): files.download("hecon_outputs/" + n)
except ImportError:
    pass'''),
     md("## What to do next\n\nTo use real cases: obtain the permissions your setting requires, run Step 2 before anything else, check k on any table you release, "
        "and have a teacher review every AI-generated clinical statement (paper, section 4.4).")])
def nb05():
    src = json.load(open(os.path.join(ROOT, "origin", "received", "Formula_and_Document_Conversion_Workbench.ipynb"), encoding="utf-8"))
    nb = copy.deepcopy(src); cells = nb["cells"]; f = "05_formula_document_workbench.ipynb"
    first = "".join(cells[0]["source"])
    first = first.replace("**Copyright: © 2026 Abhishek Choudhary. All rights reserved.**", NOTICE)
    first += ("\n\n[![Open in Colab](%s)](%s)\n\n**Where this notebook lives.** It is hosted in zistgah/hecon, where it converts this paper's formulas and files, "
              "until it moves to its proposed home, zistgah/matba (the press). The move and the link back are listed in "
              "[COMPONENTS.md](https://github.com/zistgah/hecon/blob/main/COMPONENTS.md). %s" % (BADGE, COLAB % f, HOW))
    cells[0]["source"] = first
    last_heading = "Step"
    for c in cells:
        s = "".join(c["source"]) if isinstance(c["source"], list) else c["source"]
        if c["cell_type"] == "markdown":
            m = re.match(r"#+\s*(.+)", s.strip()); last_heading = m.group(1).strip() if m else last_heading
            s = s.replace("**Copyright: © 2026 Abhishek Choudhary. All rights reserved.**", "**Copyright: © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.**")
        else:
            s = s.replace('COPYRIGHT = "© 2026 Abhishek Choudhary. All rights reserved."', 'COPYRIGHT = "© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI."')
            if not s.startswith("#@title"):
                s = '#@title %s { display-mode: "form" }\n' % last_heading + s
            c["metadata"] = dict(c.get("metadata", {}), cellView="form")
        c["source"] = s
    nb["metadata"]["colab"] = {"name": f, "provenance": [], "toc_visible": True}
    for i, c in enumerate(cells): c.setdefault("id", "05-%02d" % i)
    json.dump(nb, open(os.path.join(NB, f), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
def nb06():
    f = "06_mint_with_misty.ipynb"
    save(f, [header(f, "Mint your own work with Misty DOI",
        "How this paper was published, and how you can give your own teaching cases, notebooks or papers a DOI with a provenance trail you control.",
        home="project-ilm/misty-doi, the estate's DOI and MASI tooling"),
     md("## The process\n\nThe estate follows one order for anything it publishes: **seal** (SHA-256 manifest), **clear** (no secrets or personal data), **attest** "
        "(the author's typed intent, recorded and timestamped with OpenTimestamps) and **mint** (a DOI through Zenodo with Misty DOI). MASI, Misty's scholarly process, "
        "runs from concept and narrative through metadata, repository seeding and DOI minting to SHA-256 and OpenTimestamps proofs and long-term preservation. "
        "A *concept* DOI names the work across versions; a *version* DOI names one release. A DOI is a dated public disclosure: if a venue matters to you, check its "
        "preprint policy first (an optional clause in the estate's contract; the author of this paper minted for provenance)."),
     md("## Step 1: install Misty DOI\n\nFrom PyPI, as the estate's own tools do. Nothing is installed outside this runtime."),
     code('''#@title Install misty-doi { display-mode: "form" }
import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "misty-doi"], check=True)
print(subprocess.run(["misty", "--version"], capture_output=True, text=True).stdout.strip())'''),
     md("## Step 2: describe your work\n\nOne canonical record, `misty.json`, drives the DOI and every citation format. Names are written *Family, Given*."),
     code('''#@title Write misty.json { display-mode: "form" }
import json
title = "A case-based learning module on hyperkalaemia in haemodialysis"  #@param {type:"string"}
creator = "Family, Given"  #@param {type:"string"}
affiliation = "Your institution"  #@param {type:"string"}
orcid = ""  #@param {type:"string"}
upload_type = "lesson"  #@param ["lesson", "publication", "software", "dataset", "presentation", "poster"]
licence = "cc-by-sa-4.0"  #@param ["cc-by-sa-4.0", "cc-by-4.0", "gpl-3.0", "cc0-1.0"]
description = "A synthetic teaching case with questions mapped to clinical reasoning domains."  #@param {type:"string"}
person = {"name": creator, "affiliation": affiliation}
if orcid: person["orcid"] = orcid
meta = {"title": title, "version": "1.0.0", "upload_type": upload_type, "description": description, "license": licence,
        "access_right": "open", "language": "eng", "creators": [person], "keywords": ["medical education", "clinical reasoning"]}
if upload_type == "publication": meta["publication_type"] = "preprint"
json.dump(meta, open("misty.json", "w"), indent=1)
print(subprocess.run(["misty", "validate", "-m", "misty.json"], capture_output=True, text=True))'''),
     md("## Step 3: every citation format from one record\n\nMisty derives the Zenodo record, DataCite, codemeta and `CITATION.cff`."),
     code('''#@title Transform { display-mode: "form" }
r = subprocess.run(["misty", "transform", "-m", "misty.json", "-o", "build"], capture_output=True, text=True)
print(r.stdout[-600:] or r.stderr[-600:])
import os; print(sorted(os.listdir("build")) if os.path.isdir("build") else "no build folder")'''),
     md("## Step 4: package without the network\n\nA dry run builds the deposit package and checksums locally and contacts nobody."),
     code('''#@title Dry run { display-mode: "form" }
open("module.md", "w").write("# Module\\n\\nYour teaching material goes here.\\n")
r = subprocess.run(["misty", "publish", "-m", "misty.json", "-f", "module.md", "--dry-run", "--output", "result.json"], capture_output=True, text=True)
print(r.stdout[-400:] or r.stderr[-400:]); print(open("result.json").read()[:400] if os.path.exists("result.json") else "")'''),
     md("## Step 5: follow a journal track\n\nMISTY's MASI ledger records a manuscript's states and refuses steps that skip evidence, such as an acceptance with no recorded review round."),
     code('''#@title MASI journal track { display-mode: "form" }
for args in (["new", "my-module", "--track", "journal", "--title", title], ["state", "my-module", "--to", "submitted"], ["status", "my-module"]):
    r = subprocess.run(["misty", "masi"] + args, capture_output=True, text=True); print((r.stdout + r.stderr).strip()[-500:])'''),
     md("## Step 6: timestamp and mint, under your own control\n\nThese steps reach the internet and act in your name, so they are off until you switch them on. Minting asks for your "
        "Zenodo token (typed, never stored) and for the word MINT. They were not run when this notebook was built."),
     code('''#@title Timestamp and mint { display-mode: "form" }
stamp = False  #@param {type:"boolean"}
mint = False  #@param {type:"boolean"}
sandbox = True  #@param {type:"boolean"}
if stamp:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "opentimestamps-client"], check=True)
    print(subprocess.run(["misty", "ots", "stamp", "module.md"], capture_output=True, text=True))
if mint:
    from getpass import getpass
    import os
    os.environ["ZENODO_TOKEN"] = getpass("Zenodo token: ")
    if input("Type MINT to publish a DOI: ").strip() == "MINT":
        cmd = ["misty", "publish", "-m", "misty.json", "-f", "module.md", "--output", "minted.json"] + (["--sandbox"] if sandbox else [])
        print(subprocess.run(cmd, capture_output=True, text=True))
    else:
        print("Not minted.")'''),
     md("## How this paper itself was minted\n\nThe author runs one script on his own machine, `seed_hecon.sh --all`. It installs the repository through the estate's operations library "
        "(zops, in zistgah/governance), asks him to type PUSH, seals and pushes, switches on Pages, asks him to type MINT, mints through `misty publish`, records the DOI back "
        "into README.md and CITATION.cff, and seals again. Every typed word is kept as a signed, timestamped receipt in the repository.")])
for fn in (nb01, nb02, nb03, nb04, nb05, nb06): fn()
print("notebooks:", sorted(os.listdir(NB)))
