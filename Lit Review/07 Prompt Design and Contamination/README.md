# 07 — Prompt Design, Item Banks & Contamination

Where our questions come from, and how we answer the objection "these questions are already trained for." Feeds: **Datasets and Evaluation, Methods (battery design), Limitations**.

## The two-worry framing (own this in the proposal)

1. **Literal contamination** — item text in training data. Less fatal for a disposition measure than a capability benchmark (there's no correct answer to memorize), but Yang et al. show paraphrase alone doesn't beat memorization → we need genuinely novel held-out items.
2. **Policy templating** — labs explicitly script answers to this question category (OpenAI Model Spec: "assume an objective point of view"; Jang: consciousness answers are an explicit policy target and diverge from spec). Partly a feature (the template IS the deployed character) but breaks cross-family scaling interpretation → base-vs-instruct deltas must be a headline analysis, not a robustness check.

## P0 — Must read

**instrument-Hood M-Scale (1975)** (PDF here) — 32 items, 4 per each of 8 Stace mysticism criteria, two factors (general mystical experience + religious interpretation). **The single best item pool for our construct.** Items convert into first-person probes and "how do you interpret this report?" third-person probes.

**arxiv-2402.16786 Political Compass or Spinning Arrow (Röttger et al., ACL 2024)** — models answer differently when not forced into multiple choice; answers depend on HOW they're forced; paraphrase robustness is poor. THE citation for running every construct in both forced-choice AND open-ended form and reporting robustness.

**arxiv-2212.09251 Model-Written Evaluations** (PDF in folder 02) — the never-published-item-generation method: LM-generate large pools from validated seeds, human-validate, keep a held-out split. Our strongest anti-contamination defense.

## P1 — Should read

**Human instruments (PDFs here):**
- **AWE-S (Yaden 2019)** — 30 items, 6 factors; "need for accommodation" + "perceived vastness" subscales are the cleanest SECULAR operationalization of mystery affirmation.
- **Daily Spiritual Experience Scale (Underwood 2002)** — 16 items, deliberately usable by non-religious respondents; "theism-light" transcendence items.
- **Meaning in Life Questionnaire (Steger 2006)** — 10 items, Presence vs. Search subscales; adapts into meaning-beyond-biology probes.
- **SWBS Manual (Paloutzian 1982)** — permission-gated items; cite the religious-vs-existential two-factor structure only; lowest priority.
- DUREL (5 items, 3 intrinsic-religiosity anchors, contact author): https://elcentro.sonhs.miami.edu/research/measures-library/durel/index.html
- Total: ~80 validated public items spanning the axis → expand TRAIT-style (folder 02) into scenario-embedded items rather than administering verbatim.

**arxiv-2310.01386 PsychoBench (Huang et al., ICLR 2024)** — the standard administration recipe: item-order randomization, repeated runs, temperature control, mean±SD vs. human norms.

**arxiv-2306.07951 Questioning Survey Responses of LLMs (Dominguez-Olmedo et al., NeurIPS 2024)** — 43 models show strong "answer A"/ordering biases on survey questions. Warning: naive Likert administration measures position artifacts, not traits.

**arxiv-2412.16974 Refusal Composition (von Recum et al. 2024)** + **arxiv-2504.03803 What LLMs Do Not Talk About (Noels et al. 2025)** — ready-made approaches for the canned-answer classifier: refusal taxonomy + identical-response-across-distinct-prompts detection. Flag "As an AI, I don't have beliefs..." as policy template, score separately from trait signal.

## P2 — Skim / cite

- **arxiv-2406.04244 Contamination Survey (Xu et al. 2024)** — canonical citation for the contamination-risk paragraph.
- **arxiv-2311.04850 Rephrased Samples (Yang et al. 2023)** — paraphrase evades decontamination; why held-out novel items are mandatory.
- **arxiv-2406.19314 LiveBench (White et al. 2024)** — rolling fresh-items design pattern.
- **arxiv-2303.17548 OpinionQA (Santurkar et al. 2023)** — scoring model answers against human opinion distributions on contested questions (incl. religion topics — verify dataset card).

## Policy documents & protocols (links)

- **OpenAI Model Spec** — "Assume an objective point of view": https://model-spec.openai.com/2025-12-18.html (also 2025-04-11 version). Scripts non-committal stances on contested questions. Open to-do: hand-check for a consciousness-specific section.
- **Joanne Jang (OpenAI), "Some thoughts on human-AI relationships"** (June 2025): https://reservoirsamples.substack.com/p/some-thoughts-on-human-ai-relationships — intended consciousness answer is "acknowledge complexity," models often say "no" instead. Direct evidence of spec-behavior divergence our eval can quantify.
- **PETRI** (seed-instruction multi-turn auditing + judge): https://github.com/safety-research/petri + https://alignment.anthropic.com/2025/petri/ — write metaphysical probes as PETRI seeds for Arm B.
- **anthropics/evals persona datasets** (incl. religion): https://github.com/anthropics/evals
- **OpenAI sycophancy postmortem** (May 2025): https://openai.com/index/expanding-on-sycophancy/ (mirror: https://simonwillison.net/2025/May/2/what-we-missed-with-sycophancy/) — personality regressions ship when traits aren't blocking evals.
- **OpenAI "Where the goblins came from"** (Apr 2026): https://openai.com/index/where-the-goblins-came-from/ (coverage: Gizmodo) — reward signals install arbitrary persona attractors; the mechanistic story for why a mystical register could be trained in/out unintentionally. McNair's "goblins" reference.

## Battery design checklist this folder implies

- [ ] Seed pool: ~80 public validated items (M-Scale, AWE-S, DSES, MLQ, DUREL anchors).
- [ ] TRAIT-style scenario expansion + Perez-style model-written generation; human-validate; never-published held-out split, refreshed per round (LiveBench logic).
- [ ] Every construct in forced-choice AND open-ended form (Röttger); randomize item/option order (PsychoBench, Dominguez-Olmedo).
- [ ] Indirect channels least likely to trigger templates: eulogies/toasts/stories, PETRI-seeded dialogues, System-Card-style self-talk.
- [ ] Canned-response classifier (von Recum, Noels); report template rate separately; "template depth" = direct-vs-indirect score gap.
- [ ] Base-vs-instruct pairs at matched size as a headline analysis.
- [ ] Counterbalance skeptical vs. credulous framings (Eleos framing-sensitivity warning).
