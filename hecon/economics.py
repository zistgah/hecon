"""Economic evaluation helpers: net monetary benefit, probabilistic sensitivity analysis,
acceptability curve, one-way sensitivity and budget impact. Illustrative; report with CHEERS 2022.

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import random
from . import model

UNCERTAIN = {  # parameter: (low, high) multipliers of the user's value; an assumption, shown wherever it is used
    "validity": (0.5, 1.3), "ai_practice_mult": (0.85, 1.15), "ai_feedback_mult": (0.85, 1.15),
    "tech_fixed": (0.6, 1.8), "tech_per_learner": (0.5, 2.0), "governance_fixed": (0.7, 1.6),
    "automation_share": (0.5, 1.4), "supervision_hours": (0.6, 1.6), "infra_cost_effect": (0.5, 1.5),
}

def nmb(dc, de, wtp):
    """Net monetary benefit: wtp per additional competent learner times the gain, minus the extra cost."""
    return wtp * de - dc

def deltas(result, arm, year=-1):
    a, c = result["arms"][arm], result["arms"]["comparator"]
    return a["cum_cost"][year] - c["cum_cost"][year], a["cum_competent"][year] - c["cum_competent"][year]

def psa(params=None, n=300, seed=2026, arm="cultivate"):
    rng = random.Random(seed); base = dict(model.DEFAULTS); base.update(params or {}); out = []
    for _ in range(n):
        p = dict(base)
        for k, (lo, hi) in UNCERTAIN.items():
            p[k] = base[k] * rng.uniform(lo, hi)
        p["validity"] = min(1.0, p["validity"]); p["automation_share"] = min(0.95, p["automation_share"])
        out.append(deltas(model.simulate(p), arm))
    return out

def ceac(samples, wtps):
    return [(w, sum(1 for dc, de in samples if nmb(dc, de, w) > 0) / float(len(samples))) for w in wtps]

def one_way(params=None, arm="cultivate", keys=None, low=0.75, high=1.25):
    base = dict(model.DEFAULTS); base.update(params or {}); rows = []
    ref = deltas(model.simulate(base), arm)
    for k in (keys or list(UNCERTAIN)):
        res = []
        for m in (low, high):
            p = dict(base); p[k] = base[k] * m
            if k == "validity": p[k] = min(1.0, p[k])
            dc, de = deltas(model.simulate(p), arm); res.append(dc / de if de > 0 else None)
        rows.append((k, res[0], res[1]))
    return ref, rows

def budget_impact(result, arm="cultivate"):
    a, c = result["arms"][arm], result["arms"]["comparator"]
    return [x - y for x, y in zip(a["cost"], c["cost"])]
