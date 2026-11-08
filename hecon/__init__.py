"""hecon: scenario models and teaching tools for "From Educational Harvesting to Productive Capacity".

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
Code: GPL-3.0-or-later. Text: CC BY-SA 4.0. Metadata: CC0-1.0.
AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary; AyeCNSe™ (Indian TM application No. 7415871, pending).
Cite with CITATION.cff in https://github.com/zistgah/hecon; the DOI is recorded there once minted.
"""
__version__ = "1.0.0"
NOTICE = ("hecon " + __version__ + "\n© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.\n"
          "Code GPL-3.0-or-later; text CC BY-SA 4.0; metadata CC0-1.0.\n"
          "AyeAI® and AyeAM® are registered trade marks of Abhishek Choudhary; AyeCNSe™ (Indian TM application No. 7415871, pending).\n"
          "Citation and DOI: CITATION.cff at https://github.com/zistgah/hecon")
from . import model, economics, game, health  # noqa: E402,F401
