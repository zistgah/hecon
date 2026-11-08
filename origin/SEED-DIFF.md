# Seed diff: what changed in the received files, and why

© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.

Every received file is kept unchanged under origin/received ([PROVENANCE.md](../PROVENANCE.md) lists their hashes). The published copies differ only as listed here.

| File | Change | Why |
|:--|:--|:--|
| manuscript_source.md, .tex, .docx | Author block (Abhishek Choudhary, AyeAI, ORCID, correspondence ayeai.ayeam@gmail.com), copyright and licence. | The author's instruction. |
| manuscript_source.md, .tex, .docx | A paragraph in section 7.2 on the international and other national frameworks (Declaration of Helsinki 2024, CIOMS 2016, WHO 2021, GDPR, HIPAA), with references 15 to 19. ICMR's paragraph is kept as it was. | The author's ruling of 5 November 2026: global privacy is satisfied by default. |
| manuscript_source.md, .docx | Reference 9 reads "Consolidated Health Economic Evaluation Reporting Standards 2022", as the LaTeX file already did. | The two files disagreed; the LaTeX matches the published title. |
| manuscript_source.md, .tex, .docx | The submission checklist moved word for word to docs/paper/WORKING-NOTES.md; the manuscript keeps its integrity sentence, now under a research-integrity statement, with an author contribution and a pointer to the evidence ledger. | Print-ready documents carry no instructions or blanks. |
| .tex | Three literal "\n" sequences replaced by line breaks; amsmath and amssymb moved before unicode-math; PDF author and title set. | The received file stops with "Command \eth already defined" when compiled with errors halting; the received PDF was produced past these errors. |
| .pdf | Rebuilt from the updated LaTeX with XeLaTeX: 0 errors, 18 pages. | It must match its source. |
| .pptx | Slide 1 gains the author and contact line and the copyright line (its text box set to shrink on overflow); six literal "\n" sequences on the slides became line breaks. | The author's instruction; the received slides showed "\n" as text. |
| Workbench notebook | Copyright line to the estate's form (1993–2026); where it lives and how to open it in Colab; each code cell hidden behind its step's title; cell ids. | The author's instruction to hide code behind explanation; nbformat 4.5 requires cell ids. |

## Unified diff, Markdown

```diff
--- origin/received/manuscript_source.md
+++ docs/paper/manuscript_source.md
@@ -2,6 +2,14 @@
 
 ## A Health Economics Framework for AI-Assisted Clinical Reasoning, Competency-Based Medical Education and Open Knowledge Infrastructure
 
+**Abhishek Choudhary**  
+AyeAI, Hyderabad, India  
+ORCID: [0009-0002-0684-8320](https://orcid.org/0009-0002-0684-8320)  
+Correspondence: Abhishek Choudhary, AyeAI, Hyderabad, India. Email: ayeai.ayeam@gmail.com
+
+© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.  
+The text of this manuscript is licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0).
+
 Manuscript type: Conceptual analysis and proposed economic evaluation framework
 Disciplinary orientation: Health Economics, Health Professions Education, Digital Health, Innovation Economics and Institutional Economics
 
@@ -218,6 +226,8 @@
 
 The Indian Council of Medical Research's 2017 National Ethical Guidelines for Biomedical and Health Research Involving Human Participants provides an important Indian framework for privacy, confidentiality and informed consent. The applicable requirements depend on whether the activity constitutes routine teaching, educational research, a clinical case report or another form of research or publication.
 
+The same obligations arise under international and other national instruments. The World Medical Association's Declaration of Helsinki, revised in 2024, and the CIOMS International Ethical Guidelines for Health-related Research Involving Humans (2016) set out requirements for consent, confidentiality and ethical review in research involving human participants and their data. The World Health Organization's guidance on the ethics and governance of artificial intelligence for health (2021) addresses the use of AI systems with health information. Data-protection law applies in addition: the European Union's General Data Protection Regulation (Regulation (EU) 2016/679) treats health data as a special category and distinguishes pseudonymised from anonymous data, and the United States HIPAA Privacy Rule (45 CFR Parts 160 and 164) defines de-identification through its Safe Harbor and Expert Determination methods. An educational workflow that uses clinical cases across institutions or countries should satisfy the requirements of every jurisdiction in which a case originates or is used, including those of low-resource settings, and should adopt the strictest applicable standard where requirements differ.
+
 7.3 Privacy as an economic variable
 
 Privacy is not merely a compliance expense. It contributes to trust, participation and the sustainability of educational data infrastructure.
@@ -514,7 +524,7 @@
 
 8. Grossman M. On the concept of health capital and the demand for health. Journal of Political Economy. 1972;80(2):223-255. https://doi.org/10.1086/259880
 
-9. Husereau D, Drummond M, Augustovski F, et al. Consolidated Health Economic Evaluation Standards 2022 (CHEERS 2022) statement: updated reporting guidance for health economic evaluations. BMJ. 2022;376:e067975. https://doi.org/10.1136/bmj-2021-067975
+9. Husereau D, Drummond M, Augustovski F, et al. Consolidated Health Economic Evaluation Reporting Standards 2022 (CHEERS 2022) statement: updated reporting guidance for health economic evaluations. BMJ. 2022;376:e067975. https://doi.org/10.1136/bmj-2021-067975
 
 10. Lerner J, Tirole J. Some simple economics of open source. The Journal of Industrial Economics. 2002;50(2):197-234. https://doi.org/10.1111/1467-6451.00174
 
@@ -526,16 +536,29 @@
 
 14. Indian Council of Medical Research. National Ethical Guidelines for Biomedical and Health Research Involving Human Participants. New Delhi: ICMR; 2017. https://www.icmr.gov.in/icmrobject/custom_data/pdf/resource-guidelines/ICMR_Ethical_Guidelines_2017.pdf
 
+15. World Medical Association. World Medical Association Declaration of Helsinki: ethical principles for medical research involving human participants. JAMA. 2025;333(1):71-74. https://doi.org/10.1001/jama.2024.21972
+
+16. Council for International Organizations of Medical Sciences (CIOMS). International Ethical Guidelines for Health-related Research Involving Humans. 4th ed. Geneva: CIOMS; 2016.
+
+17. World Health Organization. Ethics and governance of artificial intelligence for health: WHO guidance. Geneva: World Health Organization; 2021.
+
+18. Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 (General Data Protection Regulation). Official Journal of the European Union. 2016;L 119:1-88. https://eur-lex.europa.eu/eli/reg/2016/679/oj
+
+19. United States Department of Health and Human Services. Standards for Privacy of Individually Identifiable Health Information (HIPAA Privacy Rule). 45 CFR Parts 160 and 164; de-identification standard at 45 CFR 164.514(b). https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164
+
+
+## Author contribution
+
+Abhishek Choudhary is the sole author of this manuscript.
+
+## Research-integrity statement
+
+This is a developed conceptual manuscript, not a completed empirical health economics study. No intervention results, participant data, cost estimates or empirical Nash-equilibrium findings have been invented in this manuscript.
 
-## Submission and research-integrity note
+The verification state of each reference, and of each figure quoted from a source, is recorded in the repository that publishes this manuscript: https://github.com/zistgah/hecon (REFERENCES.md).
 
-This is a developed conceptual manuscript, not a completed empirical health economics study. Before submission to a peer-reviewed journal, the following items must be completed:
+## Copyright and licence
 
-1. Author names, affiliations, corresponding-author details and contributions.
-2. A declared conceptual-review or scoping-review methodology, including databases, search dates, selection criteria and synthesis procedure if the paper is to claim a formal literature review.
-3. A target-journal-specific abstract, word count and reference style.
-4. A declaration of funding, conflicts of interest and any applicable ethics statement.
-5. A more extensive review of economic evaluation and implementation literature if the target journal expects a systematic evidence synthesis.
-6. A clearly specified empirical protocol if the manuscript is to claim tested cost-effectiveness or causal educational effects.
+© 1993–2026 Abhishek Choudhary. All rights reserved. AyeAI.
 
-No intervention results, participant data, cost estimates or empirical Nash-equilibrium findings have been invented in this manuscript.
+The text of this manuscript is licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0).
```

## Unified diff, LaTeX

```diff
--- origin/received/productive_capacity_health_economics_manuscript.tex
+++ docs/paper/productive_capacity_health_economics_manuscript.tex
@@ -1,24 +1,24 @@
 \documentclass[11pt,a4paper]{article}
 \usepackage[margin=25mm]{geometry}
+\usepackage{amsmath,amssymb}
 \usepackage{fontspec}
 \usepackage{unicode-math}
 \setmainfont{TeX Gyre Termes}
 \setmathfont{TeX Gyre Termes Math}
 \usepackage{microtype}
 \usepackage{setspace}
-\usepackage{amsmath,amssymb}
 \usepackage{hyperref}
 \usepackage{xcolor}
 \usepackage{enumitem}
 \usepackage{titlesec}
 \definecolor{navy}{HTML}{17365D}
 \definecolor{teal}{HTML}{287C8E}
-\hypersetup{colorlinks=true,linkcolor=navy,citecolor=teal,urlcolor=teal}
+\hypersetup{pdfauthor={Abhishek Choudhary},pdftitle={From Educational Harvesting to Productive Capacity},colorlinks=true,linkcolor=navy,citecolor=teal,urlcolor=teal}
 \titleformat{\section}{\Large\bfseries\color{navy}}{\thesection}{0.7em}{}
 \titleformat{\subsection}{\large\bfseries\color{teal}}{\thesubsection}{0.7em}{}
 \setstretch{1.12}
 \title{\textbf{From Educational Harvesting to Productive Capacity}\\[0.5em]\large A Health Economics Framework for AI-Assisted Clinical Reasoning, Competency-Based Medical Education and Open Knowledge Infrastructure}
-\author{Author details to be supplied}
+\author{Abhishek Choudhary\\[0.35em]\normalsize AyeAI, Hyderabad, India\\\normalsize ORCID: \href{https://orcid.org/0009-0002-0684-8320}{0009-0002-0684-8320}\\\normalsize Correspondence: \href{mailto:ayeai.ayeam@gmail.com}{ayeai.ayeam@gmail.com}}
 \date{}
 \begin{document}
 \maketitle
@@ -204,6 +204,8 @@
 
 The Indian Council of Medical Research's 2017 National Ethical Guidelines for Biomedical and Health Research Involving Human Participants provides an important Indian framework for privacy, confidentiality and informed consent. The applicable requirements depend on whether the activity constitutes routine teaching, educational research, a clinical case report or another form of research or publication.
 
+The same obligations arise under international and other national instruments. The World Medical Association's Declaration of Helsinki, revised in 2024, and the CIOMS International Ethical Guidelines for Health-related Research Involving Humans (2016) set out requirements for consent, confidentiality and ethical review in research involving human participants and their data. The World Health Organization's guidance on the ethics and governance of artificial intelligence for health (2021) addresses the use of AI systems with health information. Data-protection law applies in addition: the European Union's General Data Protection Regulation (Regulation (EU) 2016/679) treats health data as a special category and distinguishes pseudonymised from anonymous data, and the United States HIPAA Privacy Rule (45 CFR Parts 160 and 164) defines de-identification through its Safe Harbor and Expert Determination methods. An educational workflow that uses clinical cases across institutions or countries should satisfy the requirements of every jurisdiction in which a case originates or is used, including those of low-resource settings, and should adopt the strictest applicable standard where requirements differ.
+
 \subsection{Privacy as an economic variable}
 Privacy is not merely a compliance expense. It contributes to trust, participation and the sustainability of educational data infrastructure.
 
@@ -446,7 +448,8 @@
 
 A harvest is worth celebrating. A cultivated field is worth returning to. The enduring economic value lies in the productive capacity that remains after the harvest.
 
-\section*{References}\begin{enumerate}[leftmargin=*]\n\item Lucas HC, Upperman JS, Robinson JR. A systematic review of large language models and their implications in medical education. Medical Education. 2024;58(11):1276-1285. https://doi.org/10.1111/medu.15402
+\section*{References}\begin{enumerate}[leftmargin=*]
+\item Lucas HC, Upperman JS, Robinson JR. A systematic review of large language models and their implications in medical education. Medical Education. 2024;58(11):1276-1285. https://doi.org/10.1111/medu.15402
 \item Pham TD, et al. The impact of generative AI on health professional education: A systematic review in the context of student learning. Medical Education. 2025;59(12):1280-1289. https://doi.org/10.1111/medu.15746
 \item Wei H, Dai Y, Yuan K, et al. AI-Powered Problem- and Case-based Learning in Medical and Dental Education: A Systematic Review and Meta-analysis. International Dental Journal. 2025;75(4):100858. https://doi.org/10.1016/j.identj.2025.100858
 \item Cooper N, Bartlett M, Gay S, et al. Consensus statement on the content of clinical reasoning curricula in undergraduate medical education. Medical Teacher. 2021;43(2):152-159. https://doi.org/10.1080/0142159X.2020.1842343
@@ -460,16 +463,20 @@
 \item Lerner J, Tirole J. The economics of technology sharing: open source and beyond. Journal of Economic Perspectives. 2005;19(2):99-120. https://doi.org/10.1257/0895330054048678
 \item Johnson JP. Open source software: private provision of a public good. Journal of Economics \& Management Strategy. 2002;11(4):637-662. https://doi.org/10.1111/j.1430-9134.2002.00637.x
 \item Indian Council of Medical Research. National Ethical Guidelines for Biomedical and Health Research Involving Human Participants. New Delhi: ICMR; 2017. https://www.icmr.gov.in/icmrobject/custom\_data/pdf/resource-guidelines/ICMR\_Ethical\_Guidelines\_2017.pdf
-\end{enumerate}\n\section*{Submission and research-integrity note}\nSubmission and research-integrity note
-
-This is a developed conceptual manuscript, not a completed empirical health economics study. Before submission to a peer-reviewed journal, the following items must be completed:
-
-1. Author names, affiliations, corresponding-author details and contributions.
-2. A declared conceptual-review or scoping-review methodology, including databases, search dates, selection criteria and synthesis procedure if the paper is to claim a formal literature review.
-3. A target-journal-specific abstract, word count and reference style.
-4. A declaration of funding, conflicts of interest and any applicable ethics statement.
-5. A more extensive review of economic evaluation and implementation literature if the target journal expects a systematic evidence synthesis.
-6. A clearly specified empirical protocol if the manuscript is to claim tested cost-effectiveness or causal educational effects.
+\item World Medical Association. World Medical Association Declaration of Helsinki: ethical principles for medical research involving human participants. JAMA. 2025;333(1):71-74. \url{https://doi.org/10.1001/jama.2024.21972}
+\item Council for International Organizations of Medical Sciences (CIOMS). International Ethical Guidelines for Health-related Research Involving Humans. 4th ed. Geneva: CIOMS; 2016.
+\item World Health Organization. Ethics and governance of artificial intelligence for health: WHO guidance. Geneva: World Health Organization; 2021.
+\item Regulation (EU) 2016/679 of the European Parliament and of the Council of 27 April 2016 (General Data Protection Regulation). Official Journal of the European Union. 2016;L 119:1-88. \url{https://eur-lex.europa.eu/eli/reg/2016/679/oj}
+\item United States Department of Health and Human Services. Standards for Privacy of Individually Identifiable Health Information (HIPAA Privacy Rule). 45 CFR Parts 160 and 164; de-identification standard at 45 CFR 164.514(b). \url{https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-C/part-164}
+\end{enumerate}
+\section*{Author contribution}
+Abhishek Choudhary is the sole author of this manuscript.
+\section*{Research-integrity statement}
+This is a developed conceptual manuscript, not a completed empirical health economics study. No intervention results, participant data, cost estimates or empirical Nash-equilibrium findings have been invented in this manuscript.
+
+The verification state of each reference, and of each figure quoted from a source, is recorded in the repository that publishes this manuscript: \url{https://github.com/zistgah/hecon} (REFERENCES.md).
+\section*{Copyright and licence}
+© 1993--2026 Abhishek Choudhary. All rights reserved. AyeAI.
 
-No intervention results, participant data, cost estimates or empirical Nash-equilibrium findings have been invented in this manuscript.
+The text of this manuscript is licensed under the Creative Commons Attribution-ShareAlike 4.0 International licence (CC BY-SA 4.0).
 \end{document}
```
