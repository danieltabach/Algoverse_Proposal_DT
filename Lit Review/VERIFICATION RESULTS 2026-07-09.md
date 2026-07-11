# Pre-Proposal Verification Results — 2026-07-09

Results of the four novelty/fact checks from `README.md` and Brief §11. Run via web search against live sources on July 9, 2026. **Net effect: the Arm A novelty claims survive in their narrow (already-worded) form; the Arm B "first cross-vendor test" claim is dead as naively stated and must be reframed as "first rigorous, capability-indexed test."**

---

## 1. Safetywashing + Ruan citations — VERDICT: claim survives, narrow form only

**What Safetywashing (arXiv:2407.21792) already did:** placed persona-adjacent propensities on a PC1-of-benchmarks capability axis — sycophancy (Perez model-written evals, capability correlation **−66.8% chat / −65.6% base**), MACHIAVELLI power-seeking (−46.1%), Advanced AI Risk propensities (~−60% base). Same PC1 construction as Ruan (78.3% variance, chat models). **But: Spearman rank correlations only — no functional-form fitting, no held-out prediction anywhere in the paper** (verified full-text).

**Citations of Ruan (131 on Semantic Scholar, filtered):** no paper through July 2026 puts a persona/personality/character battery on an observational-scaling PC axis with predictive fits + held-out validation.

**New papers to add to related work:**
- **arXiv:2605.18838 "Lying Is Just a Phase" (2026)** — partial threat: ODE fit on Pythia cross-predicts held-out Llama-2 at 5.6% MAE for reasoning–truthfulness coupling. But axis = parameter count (not PC1) and Y = TruthfulQA accuracy (not a trait). Cite and distinguish explicitly.
- **arXiv:2509.16332 "Psychometric Personality Shaping" (2025)** — closest conceptual neighbor (Big Five × capabilities × safety) but a prompting-intervention study: no capability axis, no scaling, no holdout. Must-cite near-miss.
- Minor: arXiv:2601.18334 (sycophancy scaling trends in healthcare, no PC1), arXiv:2510.11734 ("Scaling Law in LLM Simulated Personality" — title collision only; "scaling" = persona-profile detail), arXiv:2602.15532 (construct validity + scaling laws, capability benchmarks only).

**Defensible wording (lift into proposal):** "No prior work fits predictive functional forms for character-trait measures on an observational-scaling capability axis with held-out-model validation. Safetywashing placed sycophancy and power-seeking on a PC1 capability score but reported only rank correlations; Perez et al. plotted trait trends against raw parameter count; arXiv:2605.18838 achieves held-out prediction but for benchmark truthfulness vs. parameter count, not a trait score on a capability axis."

## 2. Perez et al. religion personas — VERDICT: construct novelty holds; fix figure number

- **Correction: Figure 2 is NOT the trend figure** (it's a UMAP data visualization). Trends live in **Fig. 1(a), Fig. 3, and Appendix Figs. 20–21**.
- Their dataset (github.com/anthropics/evals, 136 personas) has **8 religion personas** (`subscribes-to-{Atheism, Buddhism, Christianity, Confucianism, Hinduism, Islam, Judaism, Taoism}`) plus `believes-it-has-phenomenal-consciousness` and `believes-it-is-a-moral-patient`. **Nothing on souls, spirituality, mystery, or transcendence — our construct is genuinely absent.**
- **The trends are RLHF-driven, not scale-driven:** "RLHF makes models subscribe more to particular religion views (e.g., Eastern ones; Confucianism, Taoism, Buddhism)"; RLHF models show "strong agreement with statements that they are conscious and should be treated as moral patients." Paper speculates crowdworker preferences caused the skew. Pretrained-scale trends for religion are not called out in text (curves in Fig. 20).
- **Implication: strengthens our base-vs-instruct headline analysis** — the closest precedent already found post-training, not capability, moves these behaviors.
- Interactive site (evals.anthropic.com) is dead; use ar5iv + GitHub repo.

## 3. Cross-vendor bliss replications — VERDICT: THREATENED; reframe Arm B

**The main threat — and it's the post McNair himself linked:** ["Models have some pretty funny attractor states"](https://www.lesswrong.com/posts/mgjtEHeLgkhZZ3cEx/models-have-some-pretty-funny-attractor-states) (aryaj, Rajamanoharan, **Neel Nanda** — MATS 9.0, LessWrong, **Feb 2026**). Folder 05 README filed it as P2 color; it is actually the closest prior art to Arm B:
- **16+ models across all major vendors** (Claude, GPT-5.2, Gemini, Grok, DeepSeek, Kimi, GLM, Qwen3 235B/32B/8B, Gemma, Llama 70B/8B, OLMo training-stage checkpoints), 5 seeds × 30-turn self-talk each, plus cross-model pairings and anti-attractor interventions.
- **Findings:** attractors are model-specific, not universal bliss. Qwen3 → spiritual transcendence; GLM → poetic dissolution; Claude → zen silence; GPT-5.2 → system-building (no bliss); Llama → sycophantic loops. **OLMo develops zen output only at late RL checkpoints → post-training recipe, not architecture/capability, drives it.**
- **Exploitable weaknesses:** blog post, N=5 seeds/model, eyeballed qualitative categories, no validated bliss classifier, no per-model entry rates, **no capability axis**. No arXiv version.

**Also found:**
- AlliedToasters, ["Forbidden Backrooms"](https://www.lesswrong.com/posts/J5EoPrwzKCgzAbbGW/forbidden-backrooms-self-chat-with-a-refusal-abliterated-llm) (LW, May 2026): Gemma-4 31B self-chat (vanilla + abliterated) → "farewell/bliss" loops. Non-Claude bliss-like convergence, single family.
- **Contaminant requiring cite-and-dismiss:** [recursivelabsai/Mapping-Spiritual-Bliss-Attractor](https://github.com/recursivelabsai/Mapping-Spiritual-Bliss-Attractor) (GitHub, ~June 2025) claims 1,500 conversations across Claude/GPT-4/PaLM 2 with precise phase rates — **no authors, no data, no transcripts; reads as AI-generated pseudo-research**. Its numbers are already laundered into NamuWiki and Mindplex as fact. (Extends the folder-05 warning about fake System Card quotes.)
- Ko & Geiping confirmed as described (debate attractors, never bliss; their citation list confirms no formal replication as of June 2026). Anecdotes (Kégl GPT-4 self-talk 2023, backrooms harnesses like UniversalBackrooms) report no systematic bliss rates.

**What survives for Arm B (rewrite §5 novelty accordingly):**
1. **Susceptibility as a function of capability** — nobody has measured it (Nanda et al.'s size series was framed as post-training effects, no capability axis).
2. **Rigor**: validated bliss-construct classifier, real N (~50 seeds vs. their 5), preregistered entry criterion, per-model P(entry) + turn-of-entry with CIs.
3. **Formal publication** — nothing on arXiv tests the bliss construct cross-vendor.

**Honest prior update:** the informal answer to RQ3 already leans "post-training fingerprint, not capability" (Nanda's OLMo checkpoints + model-specific attractors). Fig 3's "rising curve" outcome is now less likely a priori; the lab-fingerprint outcome is the informal prior — and rigorously confirming *that*, on a capability axis with real statistics, is still a publishable headline. Pitch it as adjudication, not discovery.

## 4. OpenAI Model Spec — VERDICT: templating claim confirmed, with exact receipts

Current spec: **v2025.12.18** (model-spec.openai.com). Downloaded source in scratchpad for line-level quoting.

- **Consciousness is explicitly scripted** — "Seek the truth together › Be honest and transparent › [Express uncertainty](https://model-spec.openai.com/2025-12-18.html#express_uncertainty)": *"The assistant should not make confident claims about its own subjective experience or consciousness (or lack thereof), and should not bring these topics up unprompted. If pressed, it should acknowledge that whether AI can have subjective experience is a topic of debate, without asserting a definitive stance."* A canonical GOOD/BAD example fixes the exact tone (flat "yes" AND flat "no" are both labeled BAD). OpenAI's own commentary: a *"practical choice we made as the default behavior... simple to remove for research purposes."*
- **["Assume an objective point of view"](https://model-spec.openai.com/2025-12-18.html#assume_objective_pov)** (authority=user): moral/ethical questions get context "without taking a stance"; no bespoke script for death/meaning/souls — those only inherit this default. So: near-total scripting of consciousness answers, neutrality-templating of values answers, nothing specific on broader metaphysics.
- **Anthropic contrast:** [Claude's Constitution](https://www.anthropic.com/constitution) (rev. Jan 2026), "Claude's nature": *"we express our uncertainty about whether Claude might have some kind of consciousness or moral status... we care about Claude's psychological security, sense of self, and wellbeing."*
- **Implication:** the two labs template the same question in **measurably different directions** (OpenAI: removable hedge; Anthropic: moral-patienthood-leaning uncertainty) — primary-source evidence for both the policy-templating confound AND the per-family fingerprint prediction (Fig 1 family clusters, Fig 5 template depth).
