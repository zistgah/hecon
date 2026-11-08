# Components: what this repository reuses, hosts and owns

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.

The rule this file serves: nothing in the estate is built twice. Before anything is written it is looked for in the estate, and what is found is used where it lives. Anything that had no home yet is hosted here with its proper home named, so it can move there and be linked back. The machine-readable form is [components.json](components.json), in the card schema of zistgah/rahnuma.

## Reused, by repository and commit

| id | component | repository | commit | how |
|---|---|---|---|---|
| zops | zops 1.2.0 | zistgah/governance | f62ab9c | sourced by seed_hecon.sh for push, Pages and mint; fetched from governance when absent |
| misty | Misty DOI 1.2.0 | project-ilm/misty-doi | 5093260 | misty publish and misty newversion through zops_mint; misty validate, transform, masi in notebook 06 |
| licences | GPL-3.0 and CC BY-SA 4.0 texts | zistgah/rahnuma | 2653126 | LICENSE and LICENSE-docs copied byte for byte |
| cards | component card schema | zistgah/rahnuma | 2653126 | the fields of data/components.json |
| llm-models | open-weight model choice | hindawiai/hindawi2026.10 | b53530f | the Qwen2.5 family offered in notebooks/llm/hindawi_llm.ipynb, used for the local tutor in notebook 04 |
| cvas | CVAS cloud harness notebook | zistgah/cvas | 0060f0a | linked from notebook 03 for verifying contributions |
| matba | matba Colab conventions | zistgah/matba | 8c4f0ec | form-view titles, tokens typed and never stored, a typed word before anything permanent |
| trademarks | trade-mark notice template | received estate fix of 5 Nov 2026 | DISCLAIMER_TRADEMARKS.md sha256 3c0f4c5789d67718 | legal/TRADEMARKS.md filled for zistgah/hecon |

## Hosted here until they move home

| id | component | path | home | state | note |
|---|---|---|---|---|---|
| health-it-lab | Health IT and health-tech AI lab | notebooks/04_health_it_ai_lab.ipynb, hecon/health.py | zistgah/marham | executed | marham holds only its charter today; move both files there and link back from here |
| workbench | Formula and Document Conversion Workbench | notebooks/05_formula_document_workbench.ipynb | zistgah/matba (proposed; the author's ruling) | executed | the author's notebook; its PDF export produced no PDF for the paper's Markdown in the build environment, the other five formats were produced; cause not diagnosed |
| mint-notebook | Mint your own work with Misty DOI | notebooks/06_mint_with_misty.ipynb | project-ilm/misty-doi | executed offline; the timestamp and mint steps are off by default and were not run | misty-doi has no notebook today |
| refcheck | refcheck | tools/refcheck.py | zistgah/governance ops/ (proposed), with the verification clause | tested against a stand-in; live checks run on the author's machine at seed time | generic: any repository's references.json |

## Native to this repository

The scenario model, its economics and the cultivation game (`hecon/`), their browser twin (`docs/hecon-model.js`, proved equal by `tests/parity.js`) and notebooks 01 to 03.

## How the estate was searched

On 5 November 2026 every public repository in the estate catalogue (zistgah.org, walked 19 September 2026) and the repositories created since were listed with blobless clones: 98 of 100 were reachable (project-ilm/record and zistgah/asab were not). None held a notebook for health economics, document conversion or minting; the reusable pieces above are what was found.
