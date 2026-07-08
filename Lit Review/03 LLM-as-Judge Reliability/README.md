# 03 — LLM-as-Judge Reliability (scoring layer)

Our trait scores come from an LLM judge. Every known judge bias is a threat to the Y-axis, and reviewers know them all. Feeds: **Methods (scoring), Experimental Setup (validation), Limitations**.

## P0 — Must read

**arxiv-2306.05685 MT-Bench / LLM-as-a-Judge (Zheng et al., NeurIPS 2023 D&B)** — the canonical citation.
- What it does: names and measures position bias, verbosity bias, self-enhancement bias; shows GPT-4 judge reaches >80% agreement with humans (≈ human-human agreement); proposes mitigations.
- Extract: the bias taxonomy + the agreement-with-humans validation design (we need a small human-rated calibration set to report judge-human agreement on OUR rubric).

**arxiv-2403.16950 Pairwise Preference / PAIRS (Liu et al., COLM 2024)** — why we use pairwise + Bradley-Terry instead of absolute Likert scores.
- Core claim: calibration cannot fix misaligned absolute scoring; pairwise preference search significantly outperforms direct scoring.
- Why it matters: this is THE citation justifying our Bradley-Terry ranking design over "rate this response 1–5."

## P1 — Should read

**arxiv-2305.17926 LLMs are not Fair Evaluators (Wang et al.)** — position bias is exploitable (Vicuna-13B "beats" ChatGPT on 66/80 queries under adversarial ordering). Extract: balanced position calibration (swap-and-aggregate) — we must run every pairwise comparison in both orders.

**arxiv-2404.13076 Self-Preference Bias (Panickssery, Bowman & Feng)** — judges favor their own generations, causally linked to self-recognition. Why it matters: our judge must not be one of the evaluated models' family — or we run judge-swap (e.g., Claude judge vs. GPT judge vs. open judge) and report agreement. This also feeds the "lab fingerprint" confound discussion.

## P2 — Skim / cite

**arxiv-2403.04132 Chatbot Arena (Chiang et al.)** — the pairwise-votes + statistical ranking (Bradley-Terry) precedent at scale; also documents what Arena Elo actually is (human pairwise votes — NOT derived from benchmarks). Caveat: confirm the exact venue string and in-paper Bradley-Terry wording before citing specifics.

## Design checklist this folder implies

- [ ] Pairwise comparisons, both orders (Wang), aggregated with Bradley-Terry (Chiang, Liu).
- [ ] Judge-swap across ≥2 judge families; report inter-judge agreement (Panickssery).
- [ ] Small human-rated calibration set; report judge-human agreement (Zheng).
- [ ] Verbosity control: check score-length correlation (Zheng).
- [ ] Judge must distinguish coherent transcendent register from degeneration/repetition loops (small-model failure mode) — needs explicit rubric anchors and a degeneration flag.
