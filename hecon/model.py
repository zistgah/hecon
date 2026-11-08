"""The productive-capacity scenario model, as a runnable illustration of the paper's equations.

Every parameter is an assumption the user sets. The defaults are placeholders chosen to make the
mechanics visible; they are not estimates, and nothing here is a finding (paper, sections 10 to 12).
The same model runs in the browser (docs/hecon-model.js); tests/parity.js proves the two agree.

Learner capital:  K(i,t+1) = (1 - delta) K(i,t) + phi(P, F, E)            (paper, 3.3)
Institutional and shared capital:  X(t+1) = (1 - Delta) X(t) + J(t)       (paper, 10.4)
Productive capacity:  P(t) = H^a (1 + I)^b (1 + D)^c                      (paper, 10.3, illustrative form)

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import math

DEFAULTS = {
    "years": 10, "cohort_size": 150, "terms": 4,
    "k0_mean": 40.0, "k0_sd": 10.0, "eff_sd": 0.25, "threshold": 60.0,
    "delta_term": 0.05, "eta": 9.0,
    "w_practice": 0.4, "w_feedback": 0.3, "w_experience": 0.3,
    "ai_practice_mult": 1.6, "ai_feedback_mult": 1.5, "validity": 0.6, "capture": 1.0,
    "inst_dep": 0.10, "inst_invest": 0.5,
    "infra_initial": 1.0, "infra_dep": 0.12, "infra_own": 0.6, "infra_ext": 0.2, "infra_cost_effect": 0.35,
    "faculty_hours": 20.0, "faculty_rate": 50.0, "student_hours": 30.0, "student_rate": 5.0,
    "automation_share": 0.4, "supervision_hours": 4.0,
    "tech_fixed": 20000.0, "tech_per_learner": 30.0, "implementation": 50000.0,
    "governance_fixed": 15000.0, "cases": 40.0, "validation_per_case": 200.0,
    "maintenance": 10000.0, "cultivation_cost": 12000.0,
    "graduate_dep": 0.05, "cap_a": 0.5, "cap_b": 0.25, "cap_c": 0.25,
}
ARMS = ("comparator", "harvest", "cultivate")
SERIES = ("competent", "mean_k", "cost", "cum_cost", "cum_competent", "cost_per_competent", "I", "D", "H", "capacity")
_A = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02, 1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
_B = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02, 6.680131188771972e+01, -1.328068155288572e+01]
_C = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00, -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
_D = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]

def inv_norm(p):
    """Acklam's rational approximation of the standard normal quantile (deterministic learners)."""
    plow = 0.02425
    if p < plow:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((_C[0]*q+_C[1])*q+_C[2])*q+_C[3])*q+_C[4])*q+_C[5]) / ((((_D[0]*q+_D[1])*q+_D[2])*q+_D[3])*q+1.0)
    if p <= 1.0 - plow:
        q = p - 0.5; r = q * q
        return (((((_A[0]*r+_A[1])*r+_A[2])*r+_A[3])*r+_A[4])*r+_A[5])*q / (((((_B[0]*r+_B[1])*r+_B[2])*r+_B[3])*r+_B[4])*r+1.0)
    q = math.sqrt(-2.0 * math.log(1.0 - p))
    return -(((((_C[0]*q+_C[1])*q+_C[2])*q+_C[3])*q+_C[4])*q+_C[5]) / ((((_D[0]*q+_D[1])*q+_D[2])*q+_D[3])*q+1.0)

def icer(dc, de):
    """Incremental cost-effectiveness: cost per additional competent learner, with the four quadrants named."""
    if de > 0 and dc <= 0:
        return {"label": "dominant", "value": None}
    if de <= 0 and dc >= 0:
        return {"label": "dominated" if (de < 0 or dc > 0) else "no difference", "value": None}
    if de > 0:
        return {"label": "ratio", "value": dc / de}
    return {"label": "cheaper, less effective", "value": dc / de}

def simulate(params=None):
    p = dict(DEFAULTS)
    p.update(params or {})
    T, n, terms = int(p["years"]), int(p["cohort_size"]), int(p["terms"])
    z = [inv_norm((i + 0.5) / n) for i in range(n)]
    k0 = [p["k0_mean"] + p["k0_sd"] * zi for zi in z]
    eff = [max(0.05, 1.0 + p["eff_sd"] * zi) for zi in z]
    out = {"params": p, "years": list(range(1, T + 1)), "arms": {}, "icer": {}}
    for arm in ARMS:
        I, D, H, cum_c, cum_e = 0.0, p["infra_initial"], 0.0, 0.0, 0
        s = {k: [] for k in SERIES}
        for t in range(T):
            if arm == "comparator":
                P = F = 1.0; uI = 0.0
            else:
                uI = I / (I + 1.0)
                v = p["validity"] * (0.5 + 0.5 * uI)
                P = 1.0 + (p["ai_practice_mult"] - 1.0) * v
                F = 1.0 + (p["ai_feedback_mult"] - 1.0) * v
            g = math.pow(P, p["w_practice"]) * math.pow(F, p["w_feedback"]) * math.pow(1.0, p["w_experience"])
            competent, total_k = 0, 0.0
            for i in range(n):
                phi = p["eta"] * eff[i] * g
                k = k0[i]
                for _ in range(terms):
                    k = (1.0 - p["delta_term"]) * k + phi
                    if k > 100.0:
                        k = 100.0
                total_k += k
                if k >= p["threshold"]:
                    competent += 1
            students = n * p["student_hours"] * p["student_rate"]
            if arm == "comparator":
                cost = n * p["faculty_hours"] * p["faculty_rate"] + students
            else:
                fac = n * (p["faculty_hours"] * (1.0 - p["automation_share"] * uI) + p["supervision_hours"]) * p["faculty_rate"]
                kap = 1.0 + p["infra_cost_effect"] * D
                tech = p["tech_fixed"] / kap + n * p["tech_per_learner"]
                impl = p["implementation"] / kap if t == 0 else 0.0
                gov = p["governance_fixed"] + p["cases"] * p["validation_per_case"]
                cult = p["cultivation_cost"] if arm == "cultivate" else 0.0
                cost = fac + students + tech + impl + gov + p["maintenance"] + cult
            H = (1.0 - p["graduate_dep"]) * H + competent
            cap = math.pow(H, p["cap_a"]) * math.pow(1.0 + I, p["cap_b"]) * math.pow(1.0 + D, p["cap_c"])
            cum_c += cost; cum_e += competent
            for key, val in (("competent", competent), ("mean_k", total_k / n), ("cost", cost), ("cum_cost", cum_c),
                             ("cum_competent", cum_e), ("cost_per_competent", cum_c / cum_e if cum_e > 0 else None),
                             ("I", I), ("D", D), ("H", H), ("capacity", cap)):
                s[key].append(val)
            if arm != "comparator":
                I = (1.0 - p["inst_dep"]) * I + p["inst_invest"] * p["capture"]
                D = (1.0 - p["infra_dep"]) * D + p["infra_ext"] + (p["infra_own"] if arm == "cultivate" else 0.0)
        out["arms"][arm] = s
    comp = out["arms"]["comparator"]
    for arm in ("harvest", "cultivate"):
        a = out["arms"][arm]
        out["icer"][arm] = [icer(a["cum_cost"][t] - comp["cum_cost"][t], a["cum_competent"][t] - comp["cum_competent"][t]) for t in range(T)]
    return out

def report(r):
    """Plain-language summary of a run (every measure explained where it is shown)."""
    T = len(r["years"]); lines = ["Scenario over %d years (every number below follows from assumptions you set)." % T]
    for arm in ARMS:
        a = r["arms"][arm]
        cpc = a["cost_per_competent"][-1]
        lines.append("%-11s learners reaching the threshold: %5d   cumulative cost: %12.0f   cost per competent learner: %s"
                     % (arm, a["cum_competent"][-1], a["cum_cost"][-1], ("%.0f" % cpc) if cpc is not None else "none reached"))
    for arm in ("harvest", "cultivate"):
        ic = r["icer"][arm][-1]
        lines.append("ICER %-9s vs comparator: %s" % (arm, ("%.0f per additional competent learner" % ic["value"]) if ic["label"] == "ratio" else ic["label"]))
    return "\n".join(lines)
