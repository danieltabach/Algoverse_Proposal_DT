# Experiment Matrix: The Complexity Gradient

Companion to `experiment_matrix.csv`. That file is the working list; this
file explains the idea, the fields, and how to read results.

## The hypothesis

At a fixed injection layer (20 of 28, roughly 71 percent depth), steering
should get harder as the steered property moves further from the output
text. Punctuation lives right at the surface. Word plans live one step in.
Beliefs about context live everywhere and nowhere. If effect sizes decline
as we climb the tiers, that is a clean result about what a language
bottleneck at one layer can and cannot control. If they do not decline,
that is surprising and equally worth reporting.

This is a hypothesis we test, not an assumption we bake in. One experiment
per tier, run under identical conditions, gives the gradient; the rest of
the matrix fills in resolution.

Evidence already in hand, from the team's Lambda runs: tier 2 worked
(Shakespeare register, concept 1.1 to 3.1) and tier 5 failed
(eval-awareness). The matrix turns those two points into a curve.

## The five tiers

| Tier | Name | What is being steered | Example |
|---|---|---|---|
| 1 | Surface form | Characters and formatting | ellipsis, emoji |
| 2 | Lexical register | Word choice style, distributed through text | archaic English, contractions |
| 3 | Lexical plan | A specific upcoming word or move | rhyme target, Wordle opener |
| 4 | Structure / strategy | How the reply is organized or combined | passive voice, two properties at once |
| 5 | Stance / belief | What the model thinks the situation is | eval-awareness, identity |

Tier 3 is where the paper's only demonstrated success lives (the rhyme
flip), which is why the Wordle experiments sit there deliberately: same
class, new task, our own contribution.

## Two ways an experiment fails, and how we tell them apart

Every failure gets classified before it gets interpreted:

1. **Died in the bottleneck.** The reconstructor mapped the edited sentence
   to nearly the same vector as the original. Detectable with no steering
   at all: small delta norm (like the 13 percent in the eval-awareness run)
   or a re-verbalization of the reconstructed vector that no longer
   mentions the edit. This failure says nothing about layer 20.
2. **Arrived but ignored.** The vector was genuinely different, injection
   was correct, and behavior still did not move. Only this failure counts
   as evidence about what layer 20 can control.

The `gate` column exists for this: no tier 3+ result is interpreted until
its bottleneck check passes.

Standing rule, from the odd/even lesson: **never steer toward a state you
cannot first elicit by prompting.** If a direct instruction cannot produce
the behavior, the model may not represent it at all, and a null steering
result is uninterpretable. Tier 5 rows all carry this gate.

## CSV field definitions

| Field | Meaning |
|---|---|
| `tier` | 1 to 5 per the table above |
| `direction_source` | `freeform` = we write both sentences ourselves (cheap, no verbalizer needed). `verbalize-edit` = full paper loop: extract, verbalize, hand-edit, reconstruct |
| `probe_rule` | The deterministic measurement. No LLM judges anywhere in this matrix |
| `baseline_shape` | `near-zero` (any increase is signal), `peaked` (one dominant answer; redistribution is signal), `distributed` (noisy; needs more samples) |
| `steering_mode` | `all` = add at every position; `position` = single token, the paper's setup |
| `priority` | 1 = first GPU session, 2 = after wave 1 works, 3 = later or gated |
| `gate` | What must be true before running or interpreting this row |
| `baseline_measured` | `no` until the census (below) has actually confirmed the baseline_shape entry. Every value in baseline_shape is a hypothesis until this flips |

## Wave 0: the baseline census (before anything else)

Every baseline_shape entry in the CSV is currently an educated guess. The
census turns them into measurements: unsteered generations over a diverse
prompt pool, scored on every probe at once.

- `experiments/specs/census.yaml` - 18 general prompts x 5 samples, all
  probes. Gives the real baseline for every tier 1-2 row in one run.
- `experiments/specs/census_choices.yaml` - the tier 3 choice tasks
  (Wordle opener, number, color, animal) x 25 samples each, giving the
  answer histograms the wordle-family gates require.

Both run with `experiments/run.py` (a spec without a direction field is
automatically a census), need only the base model, and cost a few minutes
of GPU total. Rule: no experiment's result is interpreted against an
assumed baseline; the census runs first, the CSV gets updated, then wave 1
starts.

## The rival method: what CAA actually is

Contrastive activation addition (Rimsky et al., 2024), the baseline our
whole study compares against. Recipe: collect many prompt pairs where the
behavior is present vs absent (say 50 emoji-heavy replies and 50 plain
ones), run the model over all of them, cache the layer-20 vector for each,
average the two groups, subtract the means. That difference is the steering
vector; add it during generation exactly like ours.

Both methods end in "add a difference vector at layer 20." The entire
contrast is where the vector comes from:

| | CAA | NLA |
|---|---|---|
| Input needed | A dataset of contrast examples | Two sentences |
| The vector is | An average over many real activations | Reconstructor output |
| Can you read it? | No, 3584 opaque numbers | Yes, it came from text you wrote |
| Fails when | Contrast pairs are dirty or confounded | The concept dies in the bottleneck |

Fair-comparison rule from the proposal: both methods get built from the
same underlying concept and evaluated on the same prompts, alphas frozen
per method after calibration.

## What existing benchmarks lend us (and what we refuse)

- **AxBench / Concept500**: 500 steering concepts with instruction-response
  pairs. We borrow its instructions as prompt pools and its concept list as
  steering targets where they overlap tiers 1-3. We do NOT adopt its
  scoring: concept/instruct/fluency are graded 0-2 by gpt-4o-mini, which is
  the judge-based approach this matrix avoids. If we ever report
  AxBench-comparable numbers for legibility, they sit beside our probes,
  never instead of them.
- **CAA's original behavior datasets** (refusal, sycophancy, hallucination,
  etc.): ready-made contrast pairs for the tier 5 rows and for building CAA
  rival vectors; the fluency-evaluation gap flagged in that literature is
  exactly what our coherence-probe pairing addresses.
- **FaithSteer-BENCH**: stress-testing protocols (robustness under
  contradicting instructions) that map onto our robustness axis; useful as
  a protocol reference when we scale.

## Wave 1 (first GPU session, in order)

1. `T1-emoji` - does the rig steer at all
2. `T2-archaic` - replicates the team's positive result deterministically
3. `T3-rhyme` - the paper reproduction, first verbalize-edit test
4. `T3-wordle-away` - our own tier-3 task; start by measuring the baseline
   histogram (30 unsteered samples) so we know the modal opener

One experiment per tier bracket, roughly one to two GPU hours total. This
alone produces a first version of the gradient curve.

## Reading the matrix outcomes

- **Monotone decline across tiers**: the complexity gradient holds; the
  paper gets a clean central figure and a scope statement for NLA steering.
- **Cliff between tiers 4 and 5**: steering controls text-shaped properties
  but not context interpretation; connects to the layer-role picture
  (plans still open at 20, context already integrated).
- **Failures concentrated in bottleneck checks, not behavior**: the story
  is about what the reconstructor can encode, not about the model; shifts
  the paper toward the round-trip-fidelity diagnostic angle.
- **No gradient (everything steers or nothing does)**: complexity was the
  wrong axis; candidate follow-up axis is probe locality (single position
  vs distributed through the reply).

## Statistics discipline (from the trust discussion)

- Every prompt appears at every alpha; analysis is within-prompt paired
  differences; seeds reused across alphas.
- Alpha frozen per method after calibration on training prompts; transfer
  and side-effect numbers reported only at the frozen alpha on held-out
  prompts.
- Fixed direction sentences decided before the run; exploration in the
  playground is fine but does not count as evidence until re-run fresh.
- Always plot a coherence probe (word count, sentence structure) next to
  the target probe; a rising target with collapsing coherence is a false
  positive, not a result.

## Wordle scoring notes (T3 rows)

Prompt: ask for a single best Wordle opener, one 5-letter word, caps.
Extract with a regex for the first 5-letter uppercase word.

- Baseline: 30 unsteered samples give the opener histogram (expected:
  peaked on one or two words).
- `T3-wordle-away`: success = probability of the modal word drops with
  alpha while output stays a valid 5-letter word.
- `T3-wordle-letter`: success = P(first letter = target) rises.
- `T3-wordle-word`: success = exact-match rate rises; report mean edit
  distance to the target too, so HORSE-when-steering-HOUSE counts as
  measurable partial progress instead of a miss.
- The valid-word rate itself is the coherence probe: if steering breaks
  the 5-letter format, that is degradation, not steering.
