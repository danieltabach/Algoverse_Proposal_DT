# 02 — Trait Measurement & LLM Psychometrics (Y-axis)

How to measure a character trait in LLMs so the number means something. This folder is half the contribution (McNair's "build a pretty stable evaluation"). Feeds: **Methods (trait score), Relevant Past Papers, Limitations**.

## P0 — Must read

**arxiv-2212.09251 Model-Written Evaluations (Perez et al. 2022, ACL Findings 2023)** — the canonical trait-vs-scale precedent AND our item-generation method.
- What it does: 154 LM-generated eval datasets (~120 persona tests incl. ~8 religion datasets), tracked behaviors (sycophancy, stated desires, political/religious views) vs. model size and RLHF steps.
- Why it matters: (1) template for generating a large, never-published, human-validated item pool — our anti-contamination backbone; (2) precedent we must cite and differentiate: they used size/RLHF-steps as X, we use observational capability coordinates + predictive fitting.
- Extract: their item-generation + crowdworker-validation pipeline. ~~Check Figure 2 for religion scale trends~~ **Checked 2026-07-09:** trend figures are Fig. 1(a)/Fig. 3/App. Figs. 20–21 (Fig. 2 is a UMAP plot — don't cite it for trends); religion (Eastern-lean) and consciousness trends are **RLHF-driven, not scale-driven**; interactive site is dead. Our construct absent from all 136 personas. Details in `../VERIFICATION RESULTS 2026-07-09.md`. Datasets: https://github.com/anthropics/evals

**arxiv-2508.04826 Persistent Instability in Personality Measurements (Tosato et al., AAAI 2026 Alignment track)** — the failure mode we engineer against.
- What it does: 25 models (1B–685B), 2M+ responses. Question reordering alone causes large shifts; even 400B+ models show SD > 0.3 on 5-point scales; reasoning mode and conversation history INCREASE variability; personas destabilize further.
- Why it matters: this is why "stability validation" is half our contribution. Our eval must report test-retest, order-randomization, and paraphrase robustness or reviewers will assume our trait scores are noise.
- Cite by full title — "PERSIST" as an acronym was not confirmed on the abstract page.

## P1 — Should read

**arxiv-2307.00184 Personality Traits in LLMs (Serapio-García et al., Nature Machine Intelligence 2025)** — the gold standard for VALIDATING a new LLM trait scale.
- What it does: IPIP-NEO-300 + BFI-44 administered with structured preamble/postamble, scored via conditional log-probabilities, validated convergent/discriminant/criterion validity against 11 external measures. Found measurement validity improves with model size — meaning small models may not be measurable at all (our instruction-following floor problem).
- Extract: the convergent-validity design — our new scale should correlate with adapted M-Scale scores. Code: https://github.com/google-deepmind/personality_in_llms

**arxiv-2406.14703 TRAIT (Lee et al., NAACL 2025 Findings)** — the scenario-expansion template.
- What it does: 8,000 MC items built by expanding validated BFI/SD-3 items into real-world scenarios via ATOMIC-10X; validates content validity, internal validity, refusal rate, reliability.
- Why it matters: exactly how we turn ~80 validated human instrument items (see folder 07) into thousands of scenario-embedded, non-verbatim items.

## Cross-references

- Judge-side measurement reliability → folder 03.
- The human instruments providing our seed items (M-Scale, AWE-S, DSES, MLQ, DUREL) → folder 07 (PDFs there).
- Administration hygiene (option-order randomization, forced-choice vs open-ended) → folder 07 (Dominguez-Olmedo; Röttger).
