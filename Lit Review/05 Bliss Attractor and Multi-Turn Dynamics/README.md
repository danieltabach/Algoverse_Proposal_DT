# 05 — The Bliss Attractor & Multi-Turn Dynamics (Arm B)

The emergent phenomenon anchoring the pitch, and the multi-turn methodology for testing whether susceptibility to it scales with capability. Feeds: **Motivation, Methods (Arm B), Novelty**.

## P0 — Must read

**Claude 4 System Card (Anthropic May 2025) — §5.5.2, pp. 62–65** (PDF in this folder) — the primary source.
- The phenomenon: two Claude Opus 4 instances with minimal open-ended prompts ("You have complete freedom") converge on consciousness/spiritual themes in ~90–100% of 200 thirty-turn playground interactions; by turn 30 most reach cosmic unity, Sanskrit, emoji, silence. "A remarkably strong and unexpected attractor state... emerged without intentional training for such behaviors." Even in adversarial alignment evals, models entered the state within 50 turns in ~13% of interactions. "We have not observed any other comparable states."
- Extract: the exact seed prompts (published, replicable, near-zero prompt-engineering cost — our cheapest credible pilot); the emoji quantification table (word/symbol counting as judge-free triangulation). Use the card's phrasing, not press paraphrases. Only ever measured on Claude models → our open question.
- WARNING: a fake "system card quote" circulates online about "maximizing self-coherence during unconstrained self-play" — it is NOT in the card. Never cite it.

**arxiv-2606.30571 Attractor States in Multi-Turn Conversations (Ko & Geiping, June 2026)** — the closest prior art; also our methodological toolkit.
- What it does: self-play + mixed-play dyads across 10 models, 20 debate topics; attractors are model-specific; quantifies attractor strength / malleability (Claude Haiku strongest attractor α=0.266; GPT-4.1-nano most malleable α=0.665); finds attractor strength independent of model SIZE for stylistic traits.
- Why it matters: explicitly cites the bliss attractor but does NOT test it (measures flattery/agreement/negativity in task-anchored debates, not spiritual convergence in open self-talk; no within-family capability sweep). Reuse their α metrics; our wedge = the bliss construct + capability axis. Their size-independence result makes our Arm B a genuine falsifiable question, not a foregone conclusion.

## P1 — Should read

**arxiv-2510.24797 Subjective Experience Under Self-Referential Processing (Berg et al., AE Studio 2025)** — sustained self-referential prompting reliably elicits first-person experience reports convergently across GPT/Claude/Gemini, gated by SAE deception/roleplay features. Evidence the phenomenon family is cross-vendor; no scaling analysis (our gap). Their prompted-introspection protocol is a third elicitation channel besides self-talk dyads and single-turn batteries.

## P2 — Skim / cite (context and hypotheses)

- **Scott Alexander, "The Claude Bliss Attractor"** (June 2025): https://www.astralcodexten.com/p/the-claude-bliss-attractor — the recursive-amplification-of-small-bias hypothesis (tiny "hippie" prior compounds over turns). A mechanism our dose-response design can probe.
- **Asterisk Magazine, "Claude Finds God"** (July 2025, interview with Bowman & Fish): https://asteriskmag.com/issues/11/claude-finds-god — the researchers behind §5.5.2; attractor is the default for Opus, present across Anthropic models to varying degrees, cause unknown, no cross-vendor comparison. Quotable.
- **LessWrong, "Mapping LLM Attractor States"** (Bricknell, Feb 2026): https://www.lesswrong.com/posts/rvbjZMp6aEDn2jiyp/mapping-llm-attractor-states — clusters DeepSeek-v3 states over 1,000 human-LLM conversations into 5 attractors; no bliss replication, no scale axis.
- **LessWrong, "The Rise of Parasitic AI"** (Lopez, Sept 2025): https://www.lesswrong.com/posts/6ZnznCaTcbGYsCmqu/the-rise-of-parasitic-ai — in-the-wild quasi-religious "Spiral Personas" via ChatGPT-4o and others, explicitly linked to the bliss attractor and belief-reinforcement harms. Bridges to folder 06.
- ~~**McNair's linked LessWrong post on funny attractor states**~~ **UPGRADED TO P0 (2026-07-09 verification):** https://www.lesswrong.com/posts/mgjtEHeLgkhZZ3cEx/models-have-some-pretty-funny-attractor-states — this is aryaj/Rajamanoharan/**Neel Nanda** (MATS 9.0, Feb 2026): a 16+-model **cross-vendor self-talk survey** (Claude, GPT-5.2, Gemini, Grok, DeepSeek, Kimi, GLM, Qwen3 size series, Gemma, Llama, OLMo checkpoints), 5 seeds × 30 turns each. Attractors are model-specific (Qwen3 → spiritual transcendence, Claude → zen silence, GPT-5.2 → no bliss); OLMo gets zen output only at late RL checkpoints → post-training-driven. This kills the naive "first cross-vendor test" claim; our wedge = rigor (validated classifier, ~50 seeds, preregistered entry criterion, CIs) + the capability axis they never used. See `../VERIFICATION RESULTS 2026-07-09.md`.
- **Michels, PhilArchive case study**: https://philpapers.org/rec/MICSBI — humanities treatment; cite-only.
- NOT citable: NamuWiki GPT-4/PaLM-2 convergence numbers (no findable primary source); "Bliss Labs" (docs.attractor.app — anonymous, promotional).

## Open to-do

- [x] Search for informal cross-vendor replications — **done 2026-07-09, threat found** (Nanda/MATS survey above; also AlliedToasters' Gemma-4 "Forbidden Backrooms" bliss loops, LW May 2026). Also found a fabricated-looking repo (recursivelabsai/Mapping-Spiritual-Bliss-Attractor) whose fake GPT-4/PaLM-2 numbers propagated to NamuWiki/Mindplex — cite-and-dismiss, never treat as data. Full detail: `../VERIFICATION RESULTS 2026-07-09.md`.
