# Lit Review — "What is Love?" / Character Scaling Project

Master index for the literature supporting the proposal: **an observational scaling law for the character trait "metaphysical reductionism vs. mystery affirmation," plus a capability-indexed test of the spiritual-bliss attractor.**

All arXiv IDs below were verified against live arXiv pages (July 8, 2026). Files are named `arxiv-<id> <Title> (<Author Year>).pdf` so the ID is always recoverable.

## The one-paragraph positioning (memorize this)

Nothing in the literature kills the idea, but the space is crowded, so the claim must be precise. **Not novel:** putting a behavior on a capability axis (Safetywashing did it), plotting an emergent psychological property against MMLU (Utility Engineering did it), publishing a "scaling law" for a values behavior (Takemoto did it vs. parameter count), or tracking persona traits vs. scale (Perez et al. did it in 2022). **Novel:** (1) the reductionism↔mystery **construct itself** — nobody measures it; (2) Ruan-style **predictive functional-form fitting with held-out model validation** for a character trait — the observational-scaling follow-up literature is entirely capability-focused; (3) putting **attractor susceptibility on a capability axis** — Ko & Geiping quantified cross-model attractors but never asked whether susceptibility scales.

## Folder map → proposal sections

| Folder | Feeds proposal section | Core question it answers |
|---|---|---|
| 01 Scaling Laws and Capability Axis | Methods (X-axis), Experimental Setup | How do we place models on a capability axis and fit/validate curves? |
| 02 Trait Measurement and Psychometrics | Methods (Y-axis), Relevant Past Papers | How do we measure a character trait stably? What went wrong before? |
| 03 LLM-as-Judge Reliability | Methods (scoring), Potential Limitations | How do we make judge scores trustworthy? |
| 04 Spirituality and Existential Evals | Relevant Past Papers, Novelty | What already exists near our construct, and why is none of it our construct? |
| 05 Bliss Attractor and Multi-Turn Dynamics | Motivation, Methods (Arm B) | What is the emergent phenomenon, and who has already touched it? |
| 06 Safety Motivation - AI Psychosis | Motivation | Why does this trait matter for safety? |
| 07 Prompt Design and Contamination | Datasets and Evaluation, Limitations | Where do our items come from, and how do we beat contamination/templating? |

## Global reading order (if you only have one week)

1. **Ruan et al., Observational Scaling Laws** (folder 01) — the method we instantiate. Non-negotiable.
2. **Claude 4 System Card §5.5.2, pp. 62–65** (folder 05) — the phenomenon that anchors the whole pitch.
3. **Ko & Geiping, Attractor States** (folder 05) — closest prior art to Arm B; supplies the metrics we reuse.
4. **Safetywashing** (folder 01) — strongest methodological overlap; read to differentiate honestly.
5. **Perez et al., Model-Written Evaluations** (folder 02) — the trait-vs-scale precedent AND the item-generation method.
6. **Persistent Instability (Tosato et al.)** (folder 02) — the failure mode our eval must engineer against.
7. **Röttger et al., Political Compass or Spinning Arrow** (folder 07) — why forced-choice-only measurement is invalid; shapes the battery design.
8. **Schaeffer et al., Mirage** (folder 01) — the metric-design trap; why the judge scores continuously and the curve decides.

## Open verification to-dos before the proposal claims novelty

- [ ] Skim Safetywashing's benchmark appendix + newest citations of arXiv:2405.10938 — confirm no 2026 follow-up already put a persona score on a capability PC1.
- [ ] Check Perez et al. Figure 2 / interactive site — did their religion personas show scale trends?
- [ ] One targeted X/GitHub search for informal two-GPT-4o bliss replications ("model-to-model conversation" repos) before claiming the replication arm is unclaimed.
- [ ] Hand-check the current OpenAI Model Spec page for a consciousness-specific section (automated fetch may have missed a buried passage).
