# 01 — Scaling Laws & the Capability Axis (X-axis)

This folder is the methodological backbone: how to place models of different families on one capability axis, fit trait-vs-capability curves, and validate them on held-out models. Feeds: **Methods, Experimental Setup, Benchmarks**.

## P0 — Must read

**arxiv-2405.10938 Observational Scaling Laws (Ruan NeurIPS 2024)** — THE method paper (McNair linked it directly).
- What it does: PCA over 8 benchmark scores (MMLU, ARC-C, HellaSwag, Winogrande, TruthfulQA, GSM8K, XWinograd, HumanEval) for 77 base models / 21 families → PC1 alone explains ~80% of variance → downstream metric fit as `E ≈ h·σ(β᛫S + α)` by least squares → validated by holding out the strongest models and extrapolating (train = 47 weak, test = 30 strong).
- Extract: **§5 + Table E.1 — 10–20 well-chosen models (V-optimality subsets) replicate the core findings.** This is our feasibility argument. Also Appendix B connects PC1 to item response theory in psychometrics — quote this when pitching "psychometrics for model character." PCA works for API models with no compute info (Eq. 5) — frontier models can sit on the same axis as open ladders. Code: https://github.com/ryoungj/ObsScaling

**arxiv-2407.21792 Safetywashing (Ren, NeurIPS 2024 D&B)** — the strongest methodological overlap; read to differentiate, and to steal infrastructure.
- What it does: correlates many safety/behavioral benchmarks with a capabilities PC across dozens of models.
- Why it matters: proves "behavior vs. capability PC" is not new — our wedge is a new construct + predictive functional-form fitting + holdout extrapolation, not correlation. Check its appendix for anything persona-like (open to-do).

**arxiv-2304.15004 Are Emergent Abilities a Mirage (Schaeffer, NeurIPS 2023 — Outstanding Paper)** — the metric-design trap.
- Core claim: discontinuous/binary metrics manufacture fake emergence; continuous metrics yield smooth curves.
- Why it matters: dictates our design — judge scores each response continuously; emergence (if any) must appear in the fitted curve, not in a thresholded judge verdict. Reviewers WILL ask about this; cite it preemptively in Methods.

## P1 — Should read

**arxiv-2502.08640 Utility Engineering (Mazeika, NeurIPS 2025)** — precedent that helps us: plots an emergent psychological property (value coherence) against MMLU across many models. Proves our template is top-venue publishable. Extract their framing language for "emergence with capability."

**arxiv-2502.15850 Forecasting Frontier Agent Capabilities (Pimpale, Apollo 2025)** — the other paper McNair linked. Two-step pipeline (release date → Elo/PC1 → benchmark). Extract: their backtesting protocol and how they handle models without Arena Elo. Blog version: https://www.apolloresearch.ai/science/forecasting-frontier-language-model-agent-capabilities/

**arxiv-2601.17637 Scaling Laws for Moral Machine Judgment (Takemoto 2026, Royal Society Open Science)** — literal published "scaling law" for a values behavior (power law vs. parameter count, 75 configs). Differentiate: raw parameter count is a bad cross-family axis; we use observational capability coordinates. Cite as nearest "behavioral scaling law" precedent.

## P2 — Skim / cite

**arxiv-2306.09479 Inverse Scaling (McKenzie 2023, TMLR)** — canonical evidence that behavior-vs-scale curves can be non-monotone. Protects us if we find a U-shape instead of a sigmoid: any robust curve shape is a finding.

**arxiv-2412.06540 Sloth Skill Scaling Laws (2024)** — follow-up in the observational-scaling family; confirms the follow-up literature is capability-only (part of the novelty argument). Skim abstract.

## Links (not downloadable / reference)

- Ruan et al. code + model lists: https://github.com/ryoungj/ObsScaling
- Open LLM Leaderboard (benchmark score source): https://huggingface.co/open-llm-leaderboard
- Chatbot Arena / lmarena (Elo robustness check for larger models): https://lmarena.ai
