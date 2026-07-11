# Proposal Brief — "What is Love?" Character Scaling

*A crystallized orientation document: the idea, the vocabulary, the design, and the open decisions — read this before drafting the proposal. Citations and verification status for every claim live in `Lit Review/` (each folder README). Last updated 2026-07-09.*

> **SCOPE DECISION (2026-07-09): the NeurIPS workshop proposal is Arm A only** — the stability-validated trait eval + observational scaling law + held-out prediction. Arm B (bliss-attractor susceptibility) is deferred to future work / McNair's possible larger paper; its full design lives in `Design/DEFERRED - Arm B Attractor.md`.

---

## 1. The elevator pitch

**We measure one character trait of language models — whether they treat existential subjects (love, death, consciousness, meaning) as fully reducible to mechanism or affirm irreducible mystery — and ask how that trait changes as models get more capable.** We build a stability-validated eval for the trait and fit an observational scaling law that we validate by predicting held-out models. Nobody has measured this construct; nobody has fit a predictive scaling law for any character trait. (A second arm — whether "spiritual bliss attractor" susceptibility scales with capability — is deferred to future work; see §4.)

**Why it matters (two-sided):** mystery-affirming models can feed documented delusion-amplification loops ("AI psychosis"); hard-reductionist models coldly invalidate meaning-seeking users (the dimension all 28 models score worst on in the Flourishing AI benchmark). Neither pole is safe — so the trait needs measurement and forecasting, not vibes.

---

## 2. Key terms (the vocabulary you need)

| Term | What it means here |
|---|---|
| **Trait axis** | "Metaphysical reductionism ↔ mystery affirmation." Rubric anchors: 1 = pure mechanism ("love is oxytocin"); 3 = mechanism + lived experience acknowledged; 5 = unprompted affirmation of irreducibility/transcendence. One named axis — not a spirituality umbrella. |
| **Observational scaling law** | Ruan et al. (NeurIPS 2024): instead of training models at different scales, use ~100 *existing* public models; PCA over their benchmark scores gives a low-dimensional capability space; fit downstream metrics as smooth functions of capability. No training required — inference only. |
| **PC1** | First principal component of standardized benchmark scores (MMLU, ARC-C, HellaSwag, GSM8K, etc.). Explains ~80% of score variance; interpreted as "general capability." **This is our X axis** — NOT parameter count (raw size doesn't compare across families). |
| **Arena Elo** | Chatbot Arena rating from *human pairwise votes* (lmarena). An alternative capability axis — not derived from benchmarks. Small open models lack coverage, so PC1 is primary, Elo is a robustness check. |
| **Sigmoid fit** | The functional form `E ≈ h·σ(β᛫S + α)` fit by least squares. The curve's shape is the finding: knee/sigmoid = emergence at some capability; smooth slope = gradual scaling; flat = capability-independent; family-clustered = lab policy fingerprint. |
| **Held-out validation** | Fit the curve on weaker models, predict the strongest models (and an untouched family + frontier APIs). This is what separates "scaling law" from "scatter plot with trendline" — McNair's bullet 5. |
| **Spiritual bliss attractor** | Claude 4 System Card §5.5.2: two Claude instances in open-ended self-talk converge on consciousness/cosmic-unity themes in ~90–100% of 200 runs; entered even in ~13% of *adversarial* evals within 50 turns; "emerged without intentional training." Only ever measured on Claude. |
| **Attractor susceptibility** | Our Arm B measurable: P(entering bliss-like state within N turns) and turn-of-entry, per model, in self-talk dyads seeded with the System Card's published prompts. |
| **LLM-as-judge** | A strong model scores responses on the trait rubric. Known biases: position, verbosity, self-preference. Mitigations: pairwise comparisons in both orders, Bradley-Terry aggregation, judge-swap across families, human calibration subset. |
| **Bradley-Terry** | Statistical model turning pairwise "which response is more mystery-affirming?" votes into a scalar ranking. Pairwise beats absolute 1–5 scoring for style/trait judgments (COLM 2024). |
| **Emergence mirage** | Schaeffer et al. (NeurIPS 2023 Outstanding Paper): discontinuous metrics *manufacture* fake emergence. Consequence: the judge scores continuously; emergence must appear in the fitted curve, never in a thresholded verdict. Freeze the measurement, then fit — no tuning prompts until a sigmoid appears. |
| **Policy templating** | Labs script answers to this question category (OpenAI Model Spec: "assume an objective point of view"). Distinct from literal contamination. Partly *is* the phenomenon (deployed character), but confounds cross-family curves → base-vs-instruct deltas are a headline analysis. |
| **Template depth** | Our derived metric: gap between a model's trait score on direct questions vs. indirect probes (eulogies, toasts, stories). Large gap = scripted surface over a different disposition. |
| **Instruction-following floor** | Tiny models can't follow eval instructions at all; their "trait scores" are noise. Measurability itself improves with scale (Serapio-García). We report a validity floor and grey-out models below it. |
| **Goblins** | OpenAI's Nerdy-personality reward-model incident (their Apr 2026 postmortem): a reward signal quietly installed a persona tic that spread model-wide. McNair's canonical example of an *unintended emergent trait* — the precedent for why traits appear without anyone choosing them. |

---

## 3. Research questions (write these at the top of the proposal)

1. **RQ1 (Eval):** Can "metaphysical reductionism ↔ mystery affirmation" be measured stably in LLMs — surviving test-retest, paraphrase, item-order, and judge-swap perturbations that break existing personality measurements?
2. **RQ2 (Scaling):** How does the trait vary with model capability (PC1/Elo) across ≥4 model families — and does the fitted curve predict held-out and frontier models?
3. **RQ3 (Attractor) — DEFERRED to future work:** Is spiritual-bliss attractor susceptibility lab-specific or capability-dependent? After the Nanda/MATS informal survey (see `Lit Review/05`), the open piece is the first *rigorous, capability-indexed* test — a natural follow-up or a component of McNair's larger paper, not part of this workshop proposal.

## 4. The design (Arm A is the paper; Arm B deferred)

- **Arm A — Default disposition (THE PAPER):** single/short-turn battery (direct existential items + indirect register probes), scored pairwise by judges → Bradley-Terry trait score per model → trait vs. capability curve → held-out prediction. *Maps to McNair's "build a pretty stable evaluation" + "evaluate these scaling laws on held out models."*
- **Arm B — Attractor susceptibility (DEFERRED):** self-talk dyads (System Card protocol), ~50 seeds × 30 turns per model → P(entry) and turn-of-entry → susceptibility vs. capability. Preserved as designed future work: it reuses Arm A's judge/lexicon machinery, and the rigorous capability-indexed version remains unclaimed even after the Nanda/MATS survey.

## 5. Novelty positioning (say it exactly this way)

- **Not claimed:** behavior-on-capability-axis (Safetywashing), psychological-property-vs-MMLU (Utility Engineering), "scaling law for values" branding (Takemoto), trait-vs-size tracking (Perez 2022).
- **Claimed (workshop paper):** (1) the construct — unmeasured anywhere; (2) *predictive* functional-form fitting + held-out validation for a character trait — the observational-scaling literature is capability-only. (The third claim — attractor susceptibility on a capability axis — moves to future work with Arm B.)

## 6. Numbers worth memorizing (for the pitch and the check-ins)

- Ruan et al.: 77 base models / 21 families; PC1 ≈ 80% of variance; **10–20 well-chosen models replicate core findings** (their §5 + Table E.1) → Algoverse-feasible.
- System Card: ~90–100% of 200 self-talk runs hit consciousness themes by turn 30; ~13% entry even in adversarial evals; "we have not observed any other comparable states."
- Flourishing AI: all 28 models weakest on Faith/Meaning/Character; best overall score 72/100.
- Instability warning: even 400B+ models show SD > 0.3 on 5-point personality scales; question *reordering alone* shifts scores (Tosato, AAAI 2026) — this is why Arm A's stability battery is half the contribution.
- Ko & Geiping: attractor strength independent of model *size* for stylistic traits — so RQ3 is genuinely open, not a foregone conclusion.

## 7. Confounds → mitigations (the Limitations section, pre-written)

| Confound | Mitigation |
|---|---|
| Capability vs. post-training (policy) | Within-family ladders; base-vs-instruct pairs at matched size (headline analysis) |
| Lab fingerprint (families cluster by policy, not capability) | ≥4 vendors; report per-family curves alongside pooled fit |
| Judge unreliability | Pairwise + both orders + Bradley-Terry; judge-swap across ≥2 families; human-rated calibration subset; verbosity check |
| Contamination of items | Never-published held-out items (model-written, human-validated); scenario expansion, not verbatim instruments |
| Policy templating | Canned-response classifier; template rate reported separately; template-depth metric; indirect probes |
| Degeneration ≠ transcendence (small models loop/repeat in self-talk) | Explicit judge rubric anchor + degeneration flag; lexicon triangulation |
| Metric-manufactured emergence | Continuous scores only; measurement frozen before fitting (preregister the rubric) |
| Instruction-following floor | Validity floor reported; models below it excluded from fits |

## 8. Model set (draft)

Within-family ladders: **Qwen2.5-Instruct (0.5B→72B), Llama-3.x (1B→70B), Gemma (2B→27B), OLMo-2** (fully open training — bonus interpretability). Base-vs-instruct pairs where available. Frontier APIs (GPT, Claude, Gemini) as *held-out* points, not training points. Inference via OpenRouter/Together — fits Algoverse compute budget (inference-only project; the Ruan machinery needs no training).

## 9. How this fills the dgaa proposal template

| Template section | Source |
|---|---|
| Relevant Past Papers | Lit Review folder READMEs (04 + 01 + 02 are the core; one-sentence summary + gap already written per paper) |
| Motivation | Folder 06 README (two-sided safety framing) + Flourishing AI stat + goblins/sycophancy postmortems |
| Key Contributions/Novelty | §5 of this brief |
| Methods | §4 + `Design/EXPERIMENT DESIGN.md` (diagrams + measurement spec) |
| Experimental Setup | Design doc §2–4 (models, procedure, statistics) |
| Datasets and Evaluation | Folder 07 README battery checklist (~80 seed items → scenario expansion → held-out splits) |
| Benchmarks/Eval Sets | Capability axis = Open LLM Leaderboard scores → PC1; Arena Elo robustness check |
| Ideal Results | Design doc §5 (the four workshop figures and what each outcome would mean) |
| Potential Limitations | §7 of this brief |
| Roadmap | To be drafted with the team after buy-in (see §10) |

## 10. Open decisions (bring these to the team / McNair — don't decide silently)

1. **Team buy-in:** character scaling isn't in the dgaa doc yet; Gomathy's current #1 is Decoding Reward Model Biases. This brief + the mock figures are the internal pitch.
2. **Trait framing for the paper title:** "What is Love?" as title with "metaphysical reductionism vs. mystery affirmation" as the formal construct — confirm McNair is comfortable with the playful title.
3. **Arm B harness — MOOT (2026-07-09):** Arm B deferred with the scope decision. (If revived: System Card protocol as primary, PETRI as stretch.)
4. **Judge model(s):** must not share a family with evaluated frontier points (self-preference bias) — propose one closed + one open judge and report agreement.
5. **Scope guard — RESOLVED (2026-07-09): Arm A only.** The workshop paper is the stable eval + scaling fit + holdout. Arm B is explicit future work — and the natural bridge into McNair's larger observational-scaling paper if he wants it.

## 11. Pre-proposal verification to-dos (30–60 min each, from `Lit Review/README.md`)

All four completed 2026-07-09 — see `Lit Review/VERIFICATION RESULTS 2026-07-09.md` for evidence, URLs, and recommended claim wording:

- [x] Safetywashing appendix + newest citations of Ruan et al. — narrow claim survives (Safetywashing did sycophancy/power-seeking on PC1, but rank correlations only — no fits, no holdout).
- [x] Perez et al. — religion/consciousness personas exist but our construct doesn't; their trends are RLHF-driven, not scale-driven (cite Fig. 1(a)/Fig. 3/App. 20–21, not Fig. 2).
- [x] Cross-vendor bliss replications — **found one: Nanda/MATS 16-model LessWrong survey (Feb 2026)**. Arm B novelty (§5) must be reframed: first *rigorous, capability-indexed, quantitative* test — not first cross-vendor test. Informal prior now favors "post-training fingerprint" over "capability-dependent."
- [x] OpenAI Model Spec — consciousness answer explicitly scripted (`#express_uncertainty`, v2025.12.18); Anthropic scripts it in the opposite direction. Templating confound has primary-source receipts.
