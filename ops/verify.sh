#!/usr/bin/env bash
# ops/verify.sh: the repository's own gate. zops runs it before every push.
# © 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
# SPDX-License-Identifier: GPL-3.0-or-later
#
# It refuses only on what a release needs (contract C39): the tests, the parity of the two models,
# notebooks generated from their source, parseable citation and workflow files, one version
# everywhere, no placeholder, the copyright and trade-mark marking, the evidence ledger, no secrets,
# no oversized files, and, once sealed, a manifest that verifies. Everything else is reported.
# Everything it runs stays inside this folder and is removed afterwards.
set -uo pipefail
cd "$(dirname "$0")/.."
export PYTHONDONTWRITEBYTECODE=1
FAILED=0; REPORTED=0
trap 'rm -rf .verify-nb .nbrun' EXIT
run(){ local name="$1"; shift; local out
  if out="$("$@" 2>&1)"; then printf '   ok        %s\n' "$name"
  else printf '   FAIL      %s\n' "$name"; printf '%s\n' "$out" | tail -8 | sed 's/^/             /'; FAILED=$((FAILED+1)); fi; }
report(){ local name="$1"; shift; local out
  if out="$("$@" 2>&1)"; then printf '   ok        %s\n' "$name"; [ -n "$out" ] && printf '%s\n' "$out" | tail -3 | sed 's/^/             /'
  else printf '   REPORTED  %s\n' "$name"; printf '%s\n' "$out" | tail -8 | sed 's/^/             /'; REPORTED=$((REPORTED+1)); fi; return 0; }
have(){ command -v "$1" >/dev/null 2>&1; }
yaml_ok(){ python3 - "$1" <<'PY'
import re, sys
p = sys.argv[1]; t = open(p, encoding="utf-8").read()
try:
    import yaml; yaml.safe_load(t)
except ImportError:
    first = next((l for l in t.splitlines() if l.strip() and not l.lstrip().startswith("#")), "")
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:", first): sys.exit("%s: the first content line is not a YAML key" % p)
PY
}
versions_agree(){ python3 - <<'PY'
import json, re, sys
cff = re.search(r"(?m)^version:\s*['\"]?([^'\"\s]+)", open("CITATION.cff", encoding="utf-8").read()).group(1)
meta = json.load(open("misty.json", encoding="utf-8"))["version"]
pyp = re.search(r'(?m)^version\s*=\s*"([^"]+)"', open("pyproject.toml", encoding="utf-8").read()).group(1)
pkg = re.search(r'__version__\s*=\s*"([^"]+)"', open("hecon/__init__.py", encoding="utf-8").read()).group(1)
if len({cff, meta, pyp, pkg}) != 1: sys.exit("versions differ: CITATION.cff %s, misty.json %s, pyproject %s, package %s" % (cff, meta, pyp, pkg))
PY
}
no_placeholder(){ local pat='DOI-''PENDING|ZENODO-DOI-''PENDING|zenodo\.''NNN'; ! grep -rIlE "$pat" --exclude-dir=.git . ; }
copyright_marked(){ local miss=0 f
  for f in README.md CONTRACT.md CONTEXT.md AGENTS.md CONTRIBUTING.md SECURITY.md COMPONENTS.md PROVENANCE.md REFERENCES.md hecon/*.py tools/*.py tests/*.py tests/*.js docs/*.js docs/index.html ops/*.sh notebooks/*.ipynb legal/TRADEMARKS.md; do
    grep -q '1993.\{0,3\}2026 Abhishek Choudhary' "$f" || { echo "no copyright line: $f"; miss=1; }; done; return $miss; }
mark_ok(){ local pat='AyeCNSe''®'; local hits; hits="$(grep -rIl "$pat" --exclude-dir=.git --exclude-dir=origin . | grep -v '^\./legal/TRADEMARKS\.md$' || true)"; [ -z "$hits" ] || { echo "$hits"; return 1; }; }
affiliation_ok(){ local pat='Independent ''Researcher'; ! grep -rIl "$pat" --exclude-dir=.git --exclude-dir=origin . ; }
ledger_ok(){ python3 - <<'PY'
import json, sys
bad = []
for r in json.load(open("docs/data/references.json", encoding="utf-8"))["references"]:
    if r.get("state") not in ("verified", "open", "reachable"): bad.append(r["id"] + ": no state")
    if r.get("state") == "verified" and not (r.get("sources") and r.get("verified_on") and r.get("checked")): bad.append(r["id"] + ": verified without sources")
    if r.get("state") == "open" and not r.get("note"): bad.append(r["id"] + ": open without how it will be checked")
if bad: sys.exit("\n".join(bad))
PY
}
notebooks_from_source(){ python3 tools/build_notebooks.py .verify-nb >/dev/null && for f in notebooks/*.ipynb; do cmp -s "$f" ".verify-nb/$(basename "$f")" || { echo "differs from its source: $f"; return 1; }; done; }
no_secrets(){ local pat hits
  pat='ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[0-9A-Za-z_-]{35}|pypi-AgEI''cHlwaS5vcmc'
  hits="$(grep -rIoE "$pat" --exclude-dir=.git . || true)"; [ -z "$hits" ] || { printf '%s\n' "$hits"; return 1; }; }
no_oversized(){ local big; big="$(find . -path ./.git -prune -o -type f -size +50M -print)"; [ -z "$big" ] || { printf '%s\n' "$big"; return 1; }; }
no_artefacts(){ local a
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then a="$(git ls-files -co --exclude-standard | grep -E '(^|/)(__pycache__|hecon_outputs|[^/]*\.egg-info)(/|$)|\.pyc$' || true)"
  else a="$(find . -path ./.git -prune -o \( -name __pycache__ -o -name '*.pyc' -o -name '*.egg-info' -o -name hecon_outputs \) -print)"; fi
  [ -z "$a" ] || { printf '%s\n' "$a"; return 1; }; }
manifest_ok(){ [ ! -f MANIFEST.sha256 ] || sha256sum --quiet -c MANIFEST.sha256; }
em_dash(){ local hits; hits="$(grep -rIl $'\xe2\x80\x94' --exclude-dir=.git --exclude-dir=origin --exclude-dir=paper . || true)"; [ -z "$hits" ] || { echo "em dashes in: $hits"; return 1; }; }
notebooks_run(){ if [ "${HECON_RUN_NOTEBOOKS:-0}" = 1 ]; then python3 tests/run_notebooks.py; else echo "UNJUDGED: not executed here; set HECON_RUN_NOTEBOOKS=1 in CI or a container (nothing is installed on a host)"; fi; }

echo "verify: hecon"
run "unit tests (tests/test_hecon.py)"                       python3 -m unittest discover -s tests -p 'test_*.py'
if have node; then run "browser model equals the Python model"  node tests/parity.js
else echo "   UNJUDGED  browser model parity: node is absent"; fi
run "notebooks are generated from tools/build_notebooks.py"   notebooks_from_source
run "CITATION.cff parses"                                    yaml_ok CITATION.cff
run "the workflow parses"                                    yaml_ok .github/workflows/verify.yml
run "one version everywhere"                                 versions_agree
run "no DOI placeholder"                                     no_placeholder
run "copyright line on every authored file"                  copyright_marked
run "trade marks: AyeCNSe is marked TM, never R"             mark_ok
run "affiliation AyeAI only"                                 affiliation_ok
run "every reference carries its evidence state"             ledger_ok
run "no secrets"                                             no_secrets
run "no file over 50 MB"                                     no_oversized
run "no build artefacts"                                     no_artefacts
run "manifest verifies, when sealed"                         manifest_ok
report "no em dashes in authored files"                      em_dash
report "notebooks execute"                                   notebooks_run
if [ "$FAILED" -eq 0 ]; then echo "verify: PASS ($REPORTED reported)"; else echo "verify: $FAILED check(s) failed"; exit 1; fi
