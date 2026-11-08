# From Educational Harvesting to Productive Capacity

A health economics framework for AI-assisted clinical reasoning, competency-based medical education and open knowledge infrastructure: the paper, a scenario simulator and six Colab notebooks for medicos.

**Abhishek Choudhary**, AyeAI, Hyderabad, India. ORCID [0009-0002-0684-8320](https://orcid.org/0009-0002-0684-8320). Correspondence: ayeai.ayeam@gmail.com

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.

## Read it

- The site, with the simulator: [zistgah.github.io/hecon](https://zistgah.github.io/hecon/)
- The paper: [PDF](docs/paper/productive_capacity_health_economics_manuscript.pdf), [Word](docs/paper/productive_capacity_health_economics_manuscript.docx), [LaTeX](docs/paper/productive_capacity_health_economics_manuscript.tex), [Markdown](docs/paper/manuscript_source.md) and the [slides](docs/paper/productive_capacity_health_economics_presentation.pptx)
- Every reference with its evidence state: [REFERENCES.md](REFERENCES.md)

## Run it in Colab

| Notebook | What it does | Lives |
|:--|:--|:--|
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/01_capital_formation_scenarios.ipynb) Capital formation scenarios | The three forms of capital over time; AI as an input, not the outcome | here |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/02_cost_effectiveness_icer.ipynb) Cost-effectiveness | ICER per additional competent learner, uncertainty, acceptability, tornado, budget impact | here |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/03_cultivation_game.ipynb) The cultivation game | Equilibria, the social optimum, and what recognition and funding change | here |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/04_health_it_ai_lab.ipynb) Health IT and health-tech AI lab | De-identification, re-identification risk, dialysis adequacy, reasoning records, a keyless AI tutor, FHIR | hosted; home zistgah/marham |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/05_formula_document_workbench.ipynb) Formula and document conversion workbench | LaTeX, Unicode, MathML and Word equations; batch conversion of this paper's files | hosted; proposed home zistgah/matba |
| [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/zistgah/hecon/blob/main/notebooks/06_mint_with_misty.ipynb) Mint your own work with Misty DOI | Metadata, citation formats, a dry run, a MASI journal track, minting under your own account | hosted; home project-ilm/misty-doi |

Each step's code is hidden behind its explanation. Every number in the models is an assumption you set; nothing is an estimate or a finding. Why three notebooks are hosted here, and where they go, is in [COMPONENTS.md](COMPONENTS.md).

## Run it locally

```bash
python3 -m hecon scenario                      # the console rung: a plain-language summary
python3 -m hecon scenario --set validity=0     # AI without validated alignment adds no competence
bash ops/verify.sh                             # the repository's gate
```

## Status

| Piece | State |
|:--|:--|
| Paper, all five files | Author details, copyright and global privacy frameworks added; received defects fixed; every change in [origin/SEED-DIFF.md](origin/SEED-DIFF.md) |
| References | Five verified with their figures; the rest checked by `tools/refcheck.py` when the repository is seeded |
| Python model and browser model | Executed; equal on 1,516 values (`tests/parity.js`) |
| Notebooks 01 to 06 | Executed headless; the steps that reach the internet or act in your name are off by default and were not run |
| Immersive view | Not built |

## How it is published

Seal (SHA-256 manifest), clear (this repository's gate), attest (the author's typed intent, kept as a timestamped receipt) and mint (Misty DOI on Zenodo, the DOI recorded back here). Notebook 06 shows the same process for your own work.

## Licence

The text is CC BY-SA 4.0 ([LICENSE-docs](LICENSE-docs)); the code is GPL-3.0-or-later ([LICENSE](LICENSE)); the metadata is CC0-1.0. Cite with [CITATION.cff](CITATION.cff). Contract and context: [CONTRACT.md](CONTRACT.md), [CONTEXT.md](CONTEXT.md), [AGENTS.md](AGENTS.md).

<!-- trademarks:begin -->
---
AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary in India; AyeCNSe™ (Indian TM application No. 7415871, pending) is his trade mark. The names of his products and projects are his trademarks; see [legal/TRADEMARKS.md](legal/TRADEMARKS.md). Code licences in this repository grant copyright permissions only and no right in any mark.
© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
<!-- trademarks:end -->
