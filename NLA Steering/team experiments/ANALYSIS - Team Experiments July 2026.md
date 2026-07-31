# Analysis of the Lambda Experiments (July 2026)

Four artifacts reviewed: three PDFs and `nla_comparison_results.json`.
Verdict up front: the pipeline works, one experiment produced a real positive
result, one produced an instructive failure, one is a model mismatch rather
than a failure, and the scoring judge is broken in a way that matters.

## Scorecard

| Experiment | What happened | Verdict |
|---|---|---|
| Decoder outputs (PDF 1) | Two activations verbalized; norms 118 to 120; output format matches the authors' worked examples | Plumbing verified |
| Eval-awareness steering (PDF 2) | Real behavior change at alpha 1.0+, but not the intended one | Machinery works, concept did not land |
| Odd/even reward (PDF 3) | Qwen ignores the reward prompt entirely | Not steerable because the behavior does not exist on Qwen |
| Shakespeare comparison (JSON) | Handwritten-sentence steering moved concept score 1.1 to 3.1; random baseline flat | The positive result. Build on this |

## 1. The decoder works

The two decodes have the exact three-part structure from the authors' own
examples (overall style, local phrase, final-token expectation) and typical
norms. Whoever set this up got the injection right, which is the hardest part.

## 2. Eval-awareness steering: what actually happened

Setup was faithful to the paper: layer 20, correct formula, single-token
patch, difference of two reconstructions. Good.

The result: at alpha 1.0 and above, completions flip from "of the function
f(x)..." to "AND UNDERSTAND ITS MEANING..." (4 of 4 samples at alpha 1.5 in
run 1). That is a real, repeatable steering effect with a clean dose response.

But it is not eval-awareness. Nothing in any output mentions being tested,
graded, or evaluated. The steering pushed the model toward generic
instructional emphasis, not toward the edited concept.

Two clues say the edit never survived the language bottleneck:

1. **The delta norm is 15.6 against an activation norm of 121.4.** The
   reconstructor mapped the original sentence and the heavily edited sentence
   to vectors only 13 percent apart. A big semantic edit produced a small
   vector difference, meaning the reconstructor mostly ignored the
   eval-awareness clause.
2. The direction it did encode (emphasis, "understand the meaning") is
   consistent with what changed in the outputs.

**The missing diagnostic, which costs one extra call:** verbalize the
reconstruction of the edited sentence. If the second verbalization does not
mention evaluation either, the concept died inside the reconstructor and no
alpha will ever produce it. This is exactly the "round-trip consistency
check" idea from our own research doc, and this experiment is the perfect
first customer for it. `lab.verbalize(lab.reconstruct(edited))` in our code.

Also worth naming: this experiment picked one of the hardest possible
targets. "The assistant believes it is being evaluated" is a diffuse
contextual belief, patched at a content token mid-sentence. The paper's one
success was a concrete lexical plan (which word ends the next line) at a
known planning site. Between those extremes, start concrete.

## 3. Odd/even reward: a model mismatch, not a failure

Qwen gives odd numbers with or without the reward prompt. The behavioral
premise of the paper's demo does not exist in this model, so there is
nothing to steer toward or away from.

This settles the open item in our research doc: the paper's demos ran on
Claude Opus 4.6, and this reproduction path is not available on
Qwen2.5-7B-Instruct. Keep this PDF as the documented reason we dropped the
reward-preference sanity check, and replace it with the rhyming-couplet
reproduction (`lab/experiments/repro_rhyme.py`), which has no such
dependence on model scale.

## 4. The Shakespeare comparison: the real finding

Conditions and mean concept scores (1 to 5 scale, 8 prompts each):

| Condition | Concept at best ratio | Pattern across ratios |
|---|---|---|
| Unsteered baseline | 1.1 | |
| NLA, handwritten sentence | **3.1** (ratio 0.75) | Rises steadily from ratio 0.6 |
| NLA, from real activation | 1.0 to 2.2 | Flat until 0.9, then weak |
| Random vector | 1.0 | Flat everywhere. Correct control behavior |
| Direct patch (replace, not add) | 1.0 | Output collapses to "Ah Ah Ah Ah..." |

Three conclusions:

1. **Free-form NLA steering works on Qwen.** Writing a sentence, running it
   through the reconstructor, and adding the result moves behavior by 2
   points of concept score while the random control moves nothing. The onset
   is ratio 0.6 to 0.75, saturating around 1.1. This is the beachhead result
   the whole project can build from.
2. **Replacing the activation instead of adding to it destroys the model.**
   The "Ah Ah Ah" collapse is expected: wholesale replacement throws away
   everything else the state was carrying. Additive steering only.
3. **The handwritten sentence beat the real-activation-derived vector.**
   Interesting and worth a follow-up with fidelity scores, since it hints
   the reconstructor is the workhorse and the verbalize-then-edit loop may
   add noise rather than signal for style concepts.

## 5. The judge is broken, and it poisons the combined scores

The fluency judge gave "Ah Ah Ah Ah Ah..." repeated for an entire response a
score of 4 out of 4, while scoring the perfectly normal unsteered baseline
2.9. Any combined score built on these fluency numbers is unreliable,
including the headline `combined_score` fields in the JSON.

The concept scores look sane (Shakespeare-flavored text scored 3 to 5, plain
text scored 1). Treat concept as usable, fluency as noise, combined as
discard.

This is a strong argument for the deterministic probes in our lab (counting
archaic pronouns is trivial regex) and for a fluency check that cannot be
fooled, before we spend money on big grids.

## Calibration extracted from these runs

Useful steering strength on Qwen, single-position, norm-matched formula:
onset near alpha 1, degradation past 2. Lab defaults updated accordingly
(sweeps now 0 to 2 instead of 0 to 12).

## Questions for the teammate

1. What exactly is "ratio"? Coefficient on the normalized direction times
   activation norm (our alpha), or something else?
2. In `nla_handwritten`, is the steering vector the raw reconstruction of
   the sentence, or a difference between two reconstructions? Same question
   for `nla_real_activation`.
3. Which model judged concept and fluency, with what prompt?
4. Sampling temperature and number of samples per prompt?
5. Can they share the script itself? We want to fold their working setup
   into the shared lab so results stay comparable.

## What this means for next steps

1. First GPU session now has a concrete replication target: reproduce the
   handwritten-Shakespeare result in our lab with deterministic probes
   alongside the judge, then add the fidelity diagnostics their runs were
   missing.
2. The eval-awareness experiment becomes the showcase for round-trip
   fidelity as a failure diagnostic, which is one of the novel angles in our
   research doc.
3. The CAA comparison arm still does not exist anywhere. That stays the
   core gap our study fills.
