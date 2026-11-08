"""Health IT and health-tech teaching tools for medicos: de-identification, re-identification risk,
dialysis and kidney-function calculators, structured reasoning records, a Socratic question ladder,
an AI tutor behind a provider abstraction (a keyless path always exists), a grounding check and a
FHIR R4 export. Educational use only: not a medical device and not for patient care.

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import datetime, json, math, re, urllib.request, uuid

# ------------------------------------------------------------------ identifiers and checksums
_VD = [[0,1,2,3,4,5,6,7,8,9],[1,2,3,4,0,6,7,8,9,5],[2,3,4,0,1,7,8,9,5,6],[3,4,0,1,2,8,9,5,6,7],[4,0,1,2,3,9,5,6,7,8],
       [5,9,8,7,6,0,4,3,2,1],[6,5,9,8,7,1,0,4,3,2],[7,6,5,9,8,2,1,0,4,3],[8,7,6,5,9,3,2,1,0,4],[9,8,7,6,5,4,3,2,1,0]]
_VP = [[0,1,2,3,4,5,6,7,8,9],[1,5,7,6,2,8,3,0,9,4],[5,8,0,3,7,9,6,1,4,2],[8,9,1,6,0,4,3,5,2,7],
       [9,4,5,3,1,2,6,8,7,0],[4,2,8,6,5,7,3,9,0,1],[2,7,9,3,8,0,6,4,1,5],[7,0,4,6,9,1,3,2,5,8]]

def verhoeff_valid(num):
    """Verhoeff check, used by India's 12-digit Aadhaar number."""
    digits = [int(ch) for ch in re.sub(r"\D", "", num)]
    if not digits: return False
    c = 0
    for i, dg in enumerate(reversed(digits)):
        c = _VD[c][_VP[i % 8][dg]]
    return c == 0

def nhs_valid(num):
    """Modulus 11 check, used by the 10-digit NHS number (England, Wales and the Isle of Man)."""
    d = re.sub(r"\D", "", num)
    if len(d) != 10: return False
    chk = 11 - (sum(int(d[i]) * (10 - i) for i in range(9)) % 11)
    chk = 0 if chk == 11 else chk
    return chk != 10 and chk == int(d[9])

_MON = "January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
PATTERNS = [
    ("EMAIL", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    ("URL", r"https?://\S+"),
    ("NHS_NUMBER", r"\b\d{3}[ -]?\d{3}[ -]?\d{4}\b"),
    ("AADHAAR_LIKE", r"\b[2-9]\d{3}[ -]?\d{4}[ -]?\d{4}\b"),
    ("US_SSN", r"\b(?!000|666|9\d\d)\d{3}-(?!00)\d{2}-(?!0000)\d{4}\b"),
    ("PHONE", r"(?:\+\d{1,3}[ -]?)?(?:\(\d{2,4}\)[ -]?)?\b\d{2,4}[ -]\d{3,4}[ -]?\d{3,4}\b"),
    ("RECORD_NUMBER", r"\b(?:MRN|UHID|IP No|Hospital (?:No|number)|Record (?:No|number))[.:#]?\s*[A-Z0-9-]{4,}\b"),
    ("DATE", r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b|\b\d{1,2}\s+(?:%s)\.?\s+\d{4}\b|\b(?:%s)\.?\s+\d{1,2},?\s+\d{4}\b" % (_MON, _MON)),
    ("UK_POSTCODE", r"\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b"),
    ("STREET_ADDRESS", r"\b\d{1,5}\s+(?:[A-Z][a-z]+\s){1,3}(?:Road|Rd|Street|St|Lane|Ln|Avenue|Ave|Close|Drive|Way|Marg|Nagar)\b"),
    ("POSTAL_CODE", r"\b(?:PIN|PIN code|ZIP|ZIP code|Postal code)[:\s]+\d{5,6}\b"),
    ("AGE_90_PLUS", r"\b(?:9\d|1[01]\d)[- ]year[- ]old\b|\baged?\s*:?\s*(?:9\d|1[01]\d)\b"),
    ("NAME_TITLED", r"\b(?:Mr|Mrs|Ms|Miss|Mx|Dr|Prof|Sri|Smt|Shri)\.?\s+[A-Z][a-z]+(?:[ -][A-Z][a-z]+){0,2}"),
]
_PRIORITY = {t: i for i, (t, _) in enumerate(PATTERNS)}
_DATE_FORMATS = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%d %B %Y", "%d %b %Y", "%B %d, %Y", "%B %d %Y", "%b %d, %Y")

def _shift(text, days):
    for f in _DATE_FORMATS:
        try:
            return (datetime.datetime.strptime(text.replace("Sept", "Sep"), f) + datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        except ValueError:
            pass
    return None

def detect(text, names=()):
    """Every identifier span, screened on the raw text before anything is derived from it."""
    found = []
    for typ, pat in PATTERNS:
        for m in re.finditer(pat, text):
            note = ""
            if typ == "NHS_NUMBER":
                if not nhs_valid(m.group(0)): continue
                note = "modulus 11 valid"
            if typ == "AADHAAR_LIKE":
                note = "Verhoeff valid" if verhoeff_valid(m.group(0)) else "Verhoeff fails: still removed"
            found.append({"type": typ, "start": m.start(), "end": m.end(), "note": note})
    for nm in names:
        for m in re.finditer(r"\b%s\b" % re.escape(nm), text):
            found.append({"type": "NAME_LISTED", "start": m.start(), "end": m.end(), "note": ""})
    found.sort(key=lambda f: (f["start"], -(f["end"] - f["start"]), _PRIORITY.get(f["type"], 99)))
    kept, last = [], -1
    for f in found:
        if f["start"] >= last:
            kept.append(f); last = f["end"]
    return kept

def deidentify(text, names=(), date_shift_days=None):
    """Replace identifiers with typed tags; dates are shifted by a fixed offset when one is given,
    which keeps the intervals between events. The report holds types and positions, never the values."""
    spans = detect(text, names); out = text
    for f in sorted(spans, key=lambda f: f["start"], reverse=True):
        rep = "[%s]" % f["type"]
        if f["type"] == "DATE" and date_shift_days is not None:
            sh = _shift(text[f["start"]:f["end"]], date_shift_days)
            rep = "[DATE %s]" % sh if sh else rep
        if f["type"] == "AGE_90_PLUS":
            rep = "[AGE 90 OR OVER]"
        out = out[:f["start"]] + rep + out[f["end"]:]
    report = {}
    for f in spans:
        report[f["type"]] = report.get(f["type"], 0) + 1
    return out, {"counts": report, "spans": [{k: f[k] for k in ("type", "start", "end", "note")} for f in spans]}

def evaluate(clean, gold_values, keep_values):
    """Recall: share of known identifiers no longer present. Retention: share of clinical values kept."""
    removed = [v for v in gold_values if v not in clean]
    kept = [v for v in keep_values if v in clean]
    return {"identifiers": len(gold_values), "removed": len(removed), "recall": len(removed) / float(len(gold_values) or 1),
            "missed": [v for v in gold_values if v in clean], "clinical_values": len(keep_values),
            "retained": len(kept), "lost": [v for v in keep_values if v not in clean]}

# ------------------------------------------------------------------ re-identification risk
def classes(rows, qis):
    groups = {}
    for r in rows:
        groups.setdefault(tuple(r[q] for q in qis), []).append(r)
    return groups

def k_anonymity(rows, qis):
    """Smallest group sharing the same quasi-identifiers; k = 1 means someone is unique."""
    return min(len(g) for g in classes(rows, qis).values())

def l_diversity(rows, qis, sensitive):
    return min(len({r[sensitive] for r in g}) for g in classes(rows, qis).values())

def generalise(rows, age_band=10, month_to_year=True, region_map=None):
    out = []
    for r in rows:
        x = dict(r); lo = (x["age"] // age_band) * age_band
        x["age"] = "90+" if x["age"] >= 90 else "%d-%d" % (lo, lo + age_band - 1)
        if month_to_year and "month" in x: x["month"] = x["month"][:4]
        if region_map and "region" in x: x["region"] = region_map.get(x["region"], x["region"])
        out.append(x)
    return out

def synthetic_cohort():
    """24 synthetic rows (no real person): deterministic, for teaching k-anonymity."""
    regions = ["North", "South", "East", "West"]; dx = ["CKD 5D", "CKD 4", "Diabetic kidney disease", "Lupus nephritis"]
    rows = []
    for i in range(24):
        rows.append({"age": 34 + (i * 7) % 50, "sex": "F" if i % 3 == 0 else "M", "region": regions[i % 4],
                     "month": "2025-%02d" % (1 + (i * 5) % 12), "diagnosis": dx[(i * 3) % 4]})
    return rows

# ------------------------------------------------------------------ calculators (education only)
def creatinine_umol_to_mgdl(umol):
    return umol / 88.4

def egfr_ckd_epi_2021(scr_mgdl, age, female):
    """CKD-EPI 2021 creatinine equation without a race term (Inker et al., N Engl J Med 2021), mL/min/1.73 m2."""
    kappa, alpha = (0.7, -0.241) if female else (0.9, -0.302)
    x = scr_mgdl / kappa
    v = 142.0 * math.pow(min(x, 1.0), alpha) * math.pow(max(x, 1.0), -1.200) * math.pow(0.9938, age)
    return v * 1.012 if female else v

def urr(pre, post):
    """Urea reduction ratio, per cent."""
    return (pre - post) / pre * 100.0

def ktv_daugirdas2(pre, post, hours, uf_litres, post_weight_kg):
    """Single-pool Kt/V, second-generation Daugirdas estimate; pre and post in the same units."""
    R = post / pre
    return -math.log(R - 0.008 * hours) + (4.0 - 3.5 * R) * uf_litres / post_weight_kg

# ------------------------------------------------------------------ the synthetic teaching case
CASE_TEXT = ("Mr Samuel Adeyemi, a 67-year-old man (MRN: 00482913, NHS number 999 000 0018, identity card 2345 6789 0124), "
             "lives at 12 Example Road, AB1 2CD, and can be reached on +44 20 7946 0958 or samuel.adeyemi@example.org. "
             "He has chronic kidney disease stage 5 on haemodialysis three times a week since 03/02/2021. He was reviewed "
             "by Dr Leila Haddad on 14 March 2025 after missing a dialysis session. His mother, aged 94, lives with him. "
             "He reports fatigue, pruritus and palpitations. Blood pressure 164/94 mmHg. Serum potassium 6.4 mmol/L, "
             "creatinine 812 umol/L, haemoglobin 92 g/L. Pre-dialysis urea 25.0 mmol/L, post-dialysis urea 8.0 mmol/L "
             "after a 4 hour session with 2.5 L ultrafiltration; post-dialysis weight 68 kg.")
CASE_NAMES = ("Samuel", "Adeyemi")
GOLD_IDENTIFIERS = ["Samuel Adeyemi", "12 Example Road", "00482913", "999 000 0018", "2345 6789 0124", "AB1 2CD", "+44 20 7946 0958",
                    "samuel.adeyemi@example.org", "03/02/2021", "14 March 2025", "Leila Haddad", "aged 94"]
CLINICAL_VALUES = ["67-year-old", "164/94", "6.4", "812", "92 g/L", "25.0", "8.0", "4 hour", "2.5 L", "68 kg"]
CASE = {"id": "synthetic-ckd-hd-001", "sex": "male", "age": 67, "potassium_mmol_l": 6.4, "creatinine_umol_l": 812.0,
        "haemoglobin_g_l": 92.0, "urea_pre": 25.0, "urea_post": 8.0, "session_hours": 4.0, "uf_litres": 2.5,
        "post_weight_kg": 68.0, "systolic": 164, "diastolic": 94}

# ------------------------------------------------------------------ structured reasoning records (paper, 4.2)
REASONING_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema", "title": "Structured reasoning record", "type": "object",
    "required": ["learner", "case_id", "problem_representation", "differentials", "information_sought", "decisions", "uncertainty"],
    "properties": {
        "learner": {"type": "string", "description": "pseudonymous learner code, never a name"},
        "case_id": {"type": "string"}, "problem_representation": {"type": "string", "minLength": 20},
        "differentials": {"type": "array", "items": {"type": "object", "required": ["diagnosis"],
                          "properties": {"diagnosis": {"type": "string"}, "for": {"type": "array"}, "against": {"type": "array"}}}},
        "information_sought": {"type": "array", "items": {"type": "string"}},
        "decisions": {"type": "array", "items": {"type": "object", "required": ["decision", "rationale"]}},
        "uncertainty": {"type": "string"}, "revisions": {"type": "array"}}}
KEY_FEATURES = [("recognises hyperkalaemia as urgent", ["potassium", "hyperkal"]), ("asks for an ECG", ["ecg", "electrocardiogram"]),
                ("links it to the missed session", ["missed"]), ("plans urgent dialysis", ["dialysis"]),
                ("reviews medicines and diet", ["medic", "drug", "diet"])]

def validate_record(rec):
    """Checks the required fields and their types (a dependency-free subset of the JSON Schema above)."""
    errs = []
    for k in REASONING_SCHEMA["required"]:
        if k not in rec: errs.append("missing " + k)
    types = {"learner": str, "case_id": str, "problem_representation": str, "differentials": list,
             "information_sought": list, "decisions": list, "uncertainty": str}
    for k, t in types.items():
        if k in rec and not isinstance(rec[k], t): errs.append("%s should be %s" % (k, t.__name__))
    if isinstance(rec.get("problem_representation"), str) and len(rec["problem_representation"]) < 20:
        errs.append("problem_representation is shorter than 20 characters")
    for d in rec.get("decisions", []) if isinstance(rec.get("decisions"), list) else []:
        if not (isinstance(d, dict) and "decision" in d and "rationale" in d): errs.append("each decision needs decision and rationale")
    return errs

def score_record(rec, features=KEY_FEATURES):
    """Key-feature match; a crude proxy that a teacher must review, never a grade on its own."""
    blob = json.dumps(rec).lower(); hits = [(name, any(w in blob for w in words)) for name, words in features]
    return {"score": sum(1 for _, h in hits if h) / float(len(hits)), "features": hits}

DOMAINS = ["Clinical reasoning concepts", "History taking and physical examination", "Choosing and interpreting diagnostic tests",
           "Problem identification and management", "Shared decision-making"]

def socratic_ladder(case=CASE):
    k = case["potassium_mmol_l"]
    return [
        (DOMAINS[0], "understand", "In one sentence, what is the problem representation for this patient?"),
        (DOMAINS[0], "analyse", "Which features make this presentation urgent rather than routine?"),
        (DOMAINS[1], "apply", "What would you ask about the missed session, diet and medicines?"),
        (DOMAINS[1], "apply", "What would you examine first, and why?"),
        (DOMAINS[2], "analyse", "A potassium of %.1f mmol/L: what test do you request at once, and what would change your plan?" % k),
        (DOMAINS[2], "evaluate", "Kt/V and URR describe dialysis adequacy. What do this patient's values tell you?"),
        (DOMAINS[3], "evaluate", "List your management steps in order, with the reason for each."),
        (DOMAINS[3], "create", "Draft a plan to prevent the next missed session."),
        (DOMAINS[4], "evaluate", "How would you explain the risk and the plan to the patient and family?")]

# ------------------------------------------------------------------ AI behind a provider abstraction (no vendor lock-in)
class RuleProvider:
    """Keyless and offline: answers with the next rung of the question ladder. Always available."""
    name = "rule-based, no model"
    def __init__(self, case=CASE): self.q = socratic_ladder(case); self.i = 0
    def complete(self, messages):
        dom, level, q = self.q[self.i % len(self.q)]; self.i += 1
        return "%s (%s, %s)" % (q, dom, level)

class EndpointProvider:
    """Any OpenAI-compatible chat endpoint, self-hosted or hosted, with the user's own key (bring your own key)."""
    def __init__(self, url, model, key=""):
        self.url, self.model, self.key = url.rstrip("/"), model, key; self.name = "endpoint " + model
    def complete(self, messages, max_tokens=300):
        body = json.dumps({"model": self.model, "messages": messages, "temperature": 0.2, "max_tokens": max_tokens}).encode()
        req = urllib.request.Request(self.url + "/chat/completions", data=body, headers={"Content-Type": "application/json", **({"Authorization": "Bearer " + self.key} if self.key else {})})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)["choices"][0]["message"]["content"]

class LocalProvider:
    """An open-weight model run locally with transformers (Colab CPU or GPU); the default is the smallest Qwen2.5."""
    def __init__(self, model_id="Qwen/Qwen2.5-0.5B-Instruct"):
        from transformers import pipeline  # imported only when chosen
        self.pipe = pipeline("text-generation", model=model_id, device_map="auto"); self.name = "local " + model_id
    def complete(self, messages, max_tokens=300):
        out = self.pipe(messages, max_new_tokens=max_tokens, do_sample=False)
        return out[0]["generated_text"][-1]["content"]

def tutor_messages(case_text, learner_answer):
    return [{"role": "system", "content": "You are a Socratic tutor for medical students. Ask one question at a time. "
             "Do not give the diagnosis. Use only facts in the case. Say when a claim needs a teacher to check it."},
            {"role": "user", "content": "Case: " + case_text + "\nMy reasoning so far: " + learner_answer}]

_NUM = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")
def grounding(output, source, allowed=()):
    """Numbers the AI wrote that appear nowhere in the case: each one needs a teacher's check."""
    src = set(_NUM.findall(source)) | {str(a) for a in allowed}
    return [n for n in _NUM.findall(output) if n not in src]

# ------------------------------------------------------------------ FHIR R4 export of the de-identified case
def fhir_bundle(case=CASE):
    ns = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/zistgah/hecon/" + case["id"])
    u = lambda tag: "urn:uuid:" + str(uuid.uuid5(ns, tag))
    pat = u("patient"); subj = {"reference": pat}
    def obs(tag, text, value, unit):
        return {"fullUrl": u(tag), "resource": {"resourceType": "Observation", "status": "final", "code": {"text": text},
                "subject": subj, "valueQuantity": {"value": value, "unit": unit, "system": "http://unitsofmeasure.org", "code": unit}}}
    entries = [
        {"fullUrl": pat, "resource": {"resourceType": "Patient", "gender": case["sex"]}},
        {"fullUrl": u("condition"), "resource": {"resourceType": "Condition", "subject": subj,
         "clinicalStatus": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": "active"}]},
         "code": {"text": "Chronic kidney disease stage 5 on maintenance haemodialysis"}}},
        obs("k", "Serum potassium", case["potassium_mmol_l"], "mmol/L"),
        obs("creat", "Serum creatinine", case["creatinine_umol_l"], "umol/L"),
        obs("hb", "Haemoglobin", case["haemoglobin_g_l"], "g/L"),
        {"fullUrl": u("hd"), "resource": {"resourceType": "Procedure", "status": "completed", "subject": subj,
         "code": {"text": "Haemodialysis session"}}}]
    return {"resourceType": "Bundle", "type": "collection", "entry": entries}
