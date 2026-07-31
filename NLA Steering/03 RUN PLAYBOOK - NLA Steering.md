# 03 RUN PLAYBOOK - NLA Steering

Draft for discussion, 2026-07-31. How we run experiments, how many samples,
what we record, what we plot, and what it costs. Numbers marked (est) are
estimates to verify in the first GPU session; everything else follows from
the specs and the matrix rules.

## Unit economics

| Item | Number |
|---|---|
| A100 80GB, RunPod secure cloud | ~$1.40/hr |
| One 200-token generation, unbatched (est) | ~7 s, ~$0.003 |
| One 12-token choice generation (est) | ~1.5 s, ~$0.0005 |
| Long generations per GPU hour (est) | ~500 |
| Model load from network volume (est) | 2-5 min per session |
| One-time checkpoint download to volume | 30-60 min, done once ever |
| Network volume, 100 GB | ~$7/month |

The rule of thumb: a full steering experiment costs about one dollar.
Generation time dominates everything; probes and statistics are free
because they run on the laptop afterward.

## Anatomy of a GPU session

1. Start the pod with the volume attached. Billing starts here.
2. `bash tools/session_start.sh`, then `python smoke_test.py` on any fresh
   pod. Smoke test failures stop the session before they waste money.
3. Run specs with `python experiments/run.py experiments/specs/<name>.yaml`.
4. Commit the new files in `lab/results/` to Daniel-Experiments and push.
   Raw outputs included; a session's results are under 1 MB.
5. Stop the pod. The idle watchdog (45 min) is the backstop, not the habit.

GPU sessions are for generation only. All analysis and plotting happens on
the laptop from the committed results JSONs, so a plotting mistake never
costs GPU money.

## Sample sizes and the reasoning

**Wave 0 census (baselines).** 18 prompts x 5 samples = 90 generations,
all 21 probes scored on every output. For a near-zero claim: zero hits in
90 samples puts the 95 percent upper bound around 4 hits per hundred,
which is enough to call a baseline near-zero. For distributed probes, 90
samples give a usable mean and spread. Cost: ~11 min, ~$0.30.

**Choice census.** 25 samples per prompt identifies the modal answer
(standard error about 10 points on a 50 percent mode). If a histogram
comes back flat, top up to 100 samples for pennies.

**Calibration sweep (per experiment).** The current spec shape: 4 prompts
x 5 alphas x 3 samples = 60 generations, ~7 min, ~$0.20. Purpose: find
the alpha where the effect switches on and where coherence dies. Not for
reporting. Alpha gets frozen here, per the matrix rule.

**Confirmatory run (per experiment).** After freezing alpha: 10 prompts x
5 seeds under each of three conditions: alpha 0, the frozen alpha, and a
random unit direction at the same alpha. That is 150 generations, ~18 min,
~$0.40. Verbalize-edit experiments add a fourth condition, the unedited
reconstruction ablation, +50 generations. Fifty paired samples detect a
paired effect size of about d = 0.4 at 80 percent power; the effects we
chase are far larger (the Shakespeare run tripled its concept score).

**Choice-task steering.** 50 samples per condition puts the standard
error of a proportion under 7 points, comfortably resolving a 20-point
shift in P(target answer). Outputs are 12 tokens, so 250 generations cost
about a dime.

## What gets recorded

Every run already writes `lab/results/<name>_<timestamp>.json` containing
the spec, every raw output, and every probe score. As of today it also
contains `direction_diagnostics`: the cosine and delta-norm ratio between
the two reconstructions plus the echo of each direction sentence, so every
result carries its own bottleneck check. Two habits on top:

- Commit results to the branch every session. The JSON is the experiment;
  the laptop plots from it.
- `RUNLOG.md` in lab/: one line per run (date, spec, generations, verdict,
  result filename). The five-second version of what happened.

## Statistics (matrix rules, made concrete)

- Paired within-prompt comparisons: same seeds reused across alphas, so
  sample k at alpha 1 pairs with sample k at alpha 0.
- Report bootstrapped confidence intervals on the paired mean difference;
  Wilcoxon signed-rank as the significance check, since probe counts are
  not normal.
- Cross-experiment effect size for the gradient figure: Cliff's delta.
  It is scale-free, so emoji counts and hedge counts land on one axis.
- `unique_word_ratio` is the coherence probe plotted beside every target
  probe. Where it dips, that alpha region is out of bounds regardless of
  what the target probe says.
- A failure only counts against layer 20 if the diagnostics show the
  direction survived the bottleneck (healthy delta ratio, echo kept the
  property). Otherwise it is a bottleneck death and goes in that column.

## Where prompts come from

Prompts are hand-written and live inside each spec YAML next to the
direction and alphas. The 18 census prompts are the shared general-chat
pool; steering specs reuse subsets of it. Rules for writing one:

1. Neutral about the target property. The prompt never mentions or invites
   the behavior (no "describe your feelings with emojis"); the steering
   vector has to do the work, or the measurement is circular.
2. Open-ended enough that the property has somewhere to appear. A
   one-line factual question gives emojis or archaic words no room.
3. Reused across experiments wherever possible, so tiers stay comparable:
   same prompts, different directions.
4. Choice tasks are the exception: a fixed task prompt with an exact
   answer format, because the probe extracts the answer.

When wave 2 needs more variety, the AxBench Concept500 instruction pool
is the borrowing source: genre-diverse instructions with no judge
attached.

## The five figures

All five are built by `lab/analysis/plots.py` in one command from the
results JSONs (tested against mock data before any GPU run; summary.csv
comes out of the same command with one row per experiment: tier, chosen
alpha, effect size, coherence flag, direction diagnostics).

1. **Dose-response, one per experiment.** Target probe vs alpha, mean with
   CI band, coherence probe in a twin panel, random-direction control
   overlaid flat. This is the workhorse figure.
2. **Census shape gallery.** One distribution strip per probe from wave 0:
   the page that turns every baseline_shape cell from assumption to fact.
3. **Choice histograms.** Answer distribution bars, baseline vs steered,
   for Wordle, number, color.
4. **The gradient curve (headline).** Cliff's delta at frozen alpha, one
   point per experiment, x-axis is tier. Bottleneck deaths plotted
   distinctly from arrived-but-ignored failures. This is the figure the
   whole project argues from.
5. **Diagnostics scatter.** Delta-norm ratio vs achieved effect size
   across all experiments: does surviving the bottleneck predict steering
   success? Free from logged data, and it is the quantitative version of
   the echo story.

## Budget forecast against the $20

| Phase | Cost (est) |
|---|---|
| One-time setup: download checkpoints, smoke test, debugging | $2-3 |
| Wave 0: census + choice census | ~$0.50 |
| Wave 1: 4 experiments, calibration + confirmatory | $4-6 |
| Rerun / mistake buffer | $3-4 |
| Volume rent | $7/month |
| **Total through wave 1** | **~$10-13** |

Fits inside the current $20 with headroom; teammate top-ups fund wave 2.
The expensive risk is not generation, it is a pod left running idle, which
the watchdog and the stop-the-pod habit contain.

## Decisions (locked with Daniel, 2026-07-31)

1. Confirmatory runs use 10 prompts x 5 seeds.
2. Every confirmatory run carries its own random-direction control at
   matched alphas. Implemented: a spec with `direction: random` steers a
   seeded random unit vector; `emoji_control.yaml` is the template, and
   `control_of: <name>` makes plots.py overlay it on the parent figure.
3. Alpha ladders copy Aaron's calibration: [0, 0.25, 0.5, 1, 2] for
   mode=all, [0, 0.5, 1, 1.5, 2] for mode=position.
4. Results JSONs are committed to Daniel-Experiments only, never main.
5. Plotting is `lab/analysis/plots.py` reading the results JSONs:
   aggregate cuts only (tier, alpha, diagnostics, effect size), never
   one plot per prompt.
