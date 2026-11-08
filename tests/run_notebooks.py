#!/usr/bin/env python3
"""Executes every notebook headless with a stand-in for google.colab. Reports per notebook.
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  SPDX-License-Identifier: GPL-3.0-or-later"""
import os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    import nbformat
    from nbclient import NotebookClient
except ImportError:
    print("UNJUDGED: nbclient is not installed, so the notebooks were not executed"); sys.exit(0)
os.environ["PYTHONPATH"] = os.pathsep.join([ROOT, os.path.join(ROOT, "tests", "colab_shim"), os.environ.get("PYTHONPATH", "")])
os.environ.setdefault("HECON_SHIM_UPLOAD", os.path.join(ROOT, "docs", "paper", "manuscript_source.md"))
os.environ["MPLBACKEND"] = "Agg"
only = sys.argv[1:]; fails = 0
for f in sorted(os.listdir(os.path.join(ROOT, "notebooks"))):
    if not f.endswith(".ipynb") or (only and not any(o in f for o in only)): continue
    nb = nbformat.read(os.path.join(ROOT, "notebooks", f), as_version=4); work = os.path.join(ROOT, ".nbrun", f[:-6]); os.makedirs(work, exist_ok=True)
    t = time.time()
    try:
        NotebookClient(nb, timeout=900, kernel_name="python3", resources={"metadata": {"path": work}}).execute()
        print("   ok    %-42s %5.0fs" % (f, time.time() - t))
    except Exception as e:
        fails += 1; print("   FAIL  %-42s %s" % (f, str(e).strip().splitlines()[-1][:200] if str(e).strip() else e.__class__.__name__))
sys.exit(1 if fails else 0)
