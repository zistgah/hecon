"""Console rung: python -m hecon scenario [--set key=value ...] [--json] | --version

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
SPDX-License-Identifier: GPL-3.0-or-later
"""
import json, sys
from . import NOTICE, model
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__); print(NOTICE); return 0
    if argv[0] == "--version":
        print(NOTICE); return 0
    if argv[0] != "scenario":
        print("unknown command: " + argv[0]); return 2
    params, as_json, i = {}, False, 1
    while i < len(argv):
        if argv[i] == "--set":
            k, v = argv[i + 1].split("=", 1); params[k] = float(v); i += 2
        elif argv[i] == "--json":
            as_json = True; i += 1
        else:
            print("unknown option: " + argv[i]); return 2
    r = model.simulate(params)
    if as_json:
        print(json.dumps(r, indent=1)); return 0
    print(model.report(r)); return 0
if __name__ == "__main__":
    sys.exit(main())
