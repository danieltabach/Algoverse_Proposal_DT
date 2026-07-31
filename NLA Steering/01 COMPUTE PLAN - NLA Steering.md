# Compute and Setup Plan: Natural Language Autoencoder Steering

**Status:** Planning. Nothing implemented yet.
**Date:** 30 July 2026
**Companion to:** `dgaa Research Doc Template Summer 2026.md`

---

## Table of Contents

1. [Read this first: what the moving parts actually are](#1-read-this-first-what-the-moving-parts-actually-are)
2. [Where the code lives](#2-where-the-code-lives)
3. [Three things in the proposal that need fixing](#3-three-things-in-the-proposal-that-need-fixing)
4. [Why it took 12 minutes per prompt](#4-why-it-took-12-minutes-per-prompt)
5. [The pipeline, restructured](#5-the-pipeline-restructured)
6. [Where to run it](#6-where-to-run-it)
7. [What it should cost](#7-what-it-should-cost)
8. [Free credits worth chasing](#8-free-credits-worth-chasing)
9. [First week checklist](#9-first-week-checklist)
10. [Open decisions](#10-open-decisions)

---

## 1. Read this first: what the moving parts actually are

Before the plan makes sense, here is the vocabulary, in plain language.

### The base model

**Qwen2.5-7B-Instruct.** This is the model you are studying. It is an ordinary open-weights chat model, about 7 billion parameters. When it processes text, information flows through 28 stacked layers. At each layer there is a running vector of 3,584 numbers per token, called the residual stream. That vector is the model's internal state at that point. This whole project is about reading and editing that vector.

You care about **layer 20** specifically, because that is the only layer the released tools were trained on.

### The two special models

The research this project builds on trained two extra models that work as a pair. Think of them as a translator in each direction.

**The verbalizer.** Takes one residual-stream vector (3,584 numbers) and writes an English sentence describing what the model appears to be thinking at that moment. Something like "the model is planning to end the line with a word rhyming with rabbit."

**The reconstructor.** Takes an English sentence and produces a residual-stream vector back. It is the reverse direction.

They were trained together so that vector → sentence → vector lands you close to where you started. The "closeness" is measured by a score. The released number is **0.752**, where 1.0 would be perfect. That is the round-trip fidelity your proposal cites.

### Why this is interesting for steering

Standard steering methods give you a vector of 3,584 numbers and no way to know what it means. You find out by trying it. This approach gives you a **sentence you can read and edit**. You verbalize a state, edit the sentence by hand, reconstruct it, and inject the result. If it works, you have a steering method you can inspect before you use it. That is the whole pitch.

### The comparison method

**Contrastive activation addition.** The standard baseline. You collect activations on prompts that show a behavior and prompts that do not, average each group, subtract. The difference is your steering vector. Cheap, well-understood, completely opaque.

### What "steering" means mechanically

You run the model normally, and at layer 20 you add your vector to the residual stream, scaled by some coefficient. The model continues generating with a nudged internal state. That is it. The whole intervention is one addition.

---

## 2. Where the code lives

Everything is public and Apache 2.0 licensed. I found it.

### Repositories

| Repo | What it is | Use it for |
|---|---|---|
| [`kitft/nla-inference`](https://github.com/kitft/nla-inference) | Single self-contained `nla_inference.py` plus documentation | **Clone this first.** It is all you need to run the pair |
| [`kitft/natural_language_autoencoders`](https://github.com/kitft/natural_language_autoencoders) | Full training and inference codebase | Reference only. You are not retraining anything |

"kitft" is Kit Fraser-Taliente, first author on the original post.

### Model checkpoints

Both public on Hugging Face, both bfloat16.

| Piece | Checkpoint | Size on disk | What it is |
|---|---|---|---|
| Verbalizer | `kitft/nla-qwen2.5-7b-L20-av` | ~16 GB | Full fine-tune of Qwen2.5-7B-Instruct |
| Reconstructor | `kitft/nla-qwen2.5-7b-L20-ar` | ~10 GB | Same model cut off at layer 20, final layer-norm removed, one linear head added |

Both are for **layer 20 of 28**, which is why the proposal pins the method to that layer. There are matching checkpoints for Gemma-3 12B, Gemma-3 27B, and Llama-3.3-70B if a second model ever becomes useful.

The reconstructor is smaller because it only needs the first 21 layers. That also means it is **cheap to run**: one forward pass, no text generation.

### The detail that will waste your week if you miss it

The verbalizer does not take text as input. It takes a vector, injected into the middle of a prompt at a specific character position. Getting that injection right requires several constants that ship with the checkpoint in a file called `nla_meta.yaml`:

| Constant | Value for Qwen | What breaks if wrong |
|---|---|---|
| `injection_scale` | **150** | Vector is the wrong magnitude. Output looks plausible but is meaningless |
| `injection_char` | `㈎` (U+320E) | Vector goes to the wrong position |
| `embed_scale` | 1.0 for Qwen | Only matters for Gemma, which needs √hidden_size |
| `layer_index` | 20 | Wrong layer, wrong distribution |

The `injection_scale` value ranges from 30 to 80,000 across the four model families. Using another model's number is the most common failure mode, and it **fails silently**. Their docs have a ranked debugging checklist. Read it before you write code, not after.

Also mandatory: when serving the verbalizer, disable prefix caching. The cache keys on token IDs, and these requests carry embeddings instead, so the cache silently mixes up different requests.

---

## 3. Three things in the proposal that need fixing

These are not nitpicks. Each one changes what the experiment tests.

### Problem 1: the steering demo was on Claude, not Qwen

The proposal (line 123) flags this as an open verification item. It is now answered.

The rhyming-couplet steering demo, where they edited "rabbit" to "mouse" in the verbalized sentence and the model changed its rhyme, was run on **Claude Opus 4.6**. Not on Qwen2.5-7B.

**Why this matters.** There is no published steering result on the open checkpoints at all. "Does this work on the weights we can actually download" is not a formality you can assume passes. It is an open question and it is your first real experiment.

**What to do.** Rewrite the reproduction step. It is not a same-setup validation, it is a genuine first test. Also budget for the possibility that it does not work, which your doc already handles well in the negative-result framing.

### Problem 2: Step 4 describes the wrong vector

Your Method Step 4 says: pass the edited sentence through the reconstructor to get the steering vector.

The paper does not do that. It uses a **difference of two reconstructions**:

```
Δ  =  Reconstructor(edited sentence)  −  Reconstructor(original sentence)

h  →  h  +  α · ‖h‖ · (Δ / ‖Δ‖)
```

In words: reconstruct both the original and the edited sentence, subtract to get a direction, normalize it, rescale it to match the size of the activation you are modifying, multiply by a strength coefficient, add. Applied **at one token position only**, not across the whole sequence.

**Why this matters.** A difference of two vectors is structurally the same shape as contrastive activation addition. Both methods are "take a difference between two conditions and add it." The real difference between them is *how you obtain the contrast*, not the algebra. That is a narrower and more honest framing than "language editing versus vector arithmetic," and it should be stated that way in the writeup.

**What to do.** Rewrite Steps 4 and 5. Decide and record whether you inject at one position or many, since the paper uses one and your proposal does not specify.

### Problem 3: the 0.752 fidelity number does not apply to your data

That score was measured **in-distribution**, on the training mix: half WildChat conversations, half Ultra-FineWeb web text.

Your prompts come from AxBench Concept500, HarmBench-style red-teaming sets, and a synthetic hedging set you build yourself. None of that resembles the training distribution.

**Why this matters.** If round-trip fidelity collapses on your prompts, every downstream result is noise and you will not know why.

**What to do.** Measure it on your own data before anything else. It is cheap, it takes about two hours of GPU time, and it is a clean go/no-go signal.

### Expectation setter

Even on Claude Opus 4.6, their strongest model, the paper reports steering worked **roughly half the time**, with occasional incoherent output. That is the published ceiling. On a 7B open model, out of distribution, expect less.

---

## 4. Why it took 12 minutes per prompt

Almost certainly not the GPU.

Twelve minutes for a few hundred generated tokens means the time went to setup, not computation. Ranked by likelihood:

| Cause | Why it costs so much |
|---|---|
| Reloading weights from disk every prompt | The verbalizer alone is 16 GB. Cold-loading three models per prompt is minutes on its own |
| Starting and stopping the serving process per prompt | Server startup is 30 to 90 seconds |
| Batch size of one | A 7B model on a modern GPU sits nearly idle processing one sequence at a time |
| Running the full chain per prompt | The vectors do not change between prompts. Computing them repeatedly is wasted work |
| CPU offloading on a card too small to hold the weights | 20x to 50x slowdown, and it looks like it is "working" |

**The fix is architectural, not hardware.** A bigger GPU makes a badly structured pipeline slightly less slow. Restructuring makes it 100x faster. That restructuring is the next section.

---

## 5. The pipeline, restructured

### The key insight

**Steering vectors are cached artifacts.** Almost nothing needs to run per prompt at experiment time.

Once you have computed a steering vector, it is a small file. Applying it is one addition during generation. The expensive machinery (verbalizer, reconstructor) runs a few hundred times total across the entire project, not once per prompt per condition.

### The stages

```
  STAGE                    RUNS ON        SCALES WITH        COST
  ─────────────────────────────────────────────────────────────────
  0  Build datasets        laptop         nothing            free
  1  Harvest activations   GPU            # of prompts       minutes
  2  Build CAA vectors     laptop         nothing            seconds
  3  Verbalize             GPU            # of edits (~300)  minutes
  4  Edit sentences        laptop         nothing            free
  5  Reconstruct           GPU            # of edits (~300)  seconds
  6  Steered generation    GPU        ★  THE FULL GRID       hours
  7  Score results         laptop + API   nothing            cents
```

Stages 1 through 5 produce **one small file of vectors**. After that file exists, you never touch the verbalizer or reconstructor again unless the method changes.

Stage 6 is the only stage that grows with your experiment design, and it is plain batched text generation with one extra addition per forward pass.

### Stage detail

| Stage | What actually happens |
|---|---|
| **1. Harvest** | Run base Qwen over every contrast prompt once, batched. Save the layer-20 vector at the positions you care about into a parquet file. This file is small |
| **2. CAA vectors** | Group the parquet by positive and negative, average each, subtract. This is a few lines of numpy on your laptop. No GPU |
| **3. Verbalize** | Only verbalize the activations you will actually edit. That is a few hundred, not thousands. About 200 generated tokens each |
| **4. Edit** | Apply your fixed per-category template to flip the target property. Text substitution |
| **5. Reconstruct** | One forward pass per sentence, no generation. Batched, this is seconds of GPU time for the whole set |
| **6. Generate** | Every prompt × every condition × every coefficient. The grid. See sizing below |
| **7. Score** | Deterministic probes (count ellipses, em-dashes, list markers, emoji) cost nothing. Judge model via API for hedging and refusal |

### How big is stage 6, actually

Rough sizing from your proposal:

```
  600 prompts        (3 categories × ~200)
×  26 conditions     (1 baseline + 15 CAA + 5 NLA + 5 ablation)
= 15,600 generations
× 250 tokens each
= ~4 million tokens
```

Four million tokens of batched 7B generation on an H100 is **under 30 minutes of actual compute**. Even allowing for 5x overhead from hooks and inefficiency, it is a couple of hours.

The experiments are not the expensive part. Debugging is.

### The tool that makes this work

[**vllm-lens**](https://github.com/UKGovernmentBEIS/vllm-lens), from the UK AI Safety Institute. It plugs into vLLM (a fast serving engine) and does exactly the two things you need:

- Capture residual-stream activations at chosen layers. That is Stage 1.
- Apply steering vectors at a chosen layer and chosen token positions during generation. That is Stage 6.

Position-specific injection is supported, which you need because the paper injects at one token only.

```bash
uv add vllm-lens
```

It auto-registers as a vLLM plugin. **Verify it works with Qwen2.5 on day one.** It is demonstrated on Llama and GLM. Qwen is standard vLLM-supported so it should be fine, but confirm rather than assume.

### One wrinkle to resolve early

The official code serves the verbalizer with **SGLang**, a different engine, because the verbalizer needs vector injection into the prompt embeddings. Stage 6 wants **vLLM** plus vllm-lens. That is two serving stacks.

Since the stages are separate anyway, running both is tolerable. But I would first try replacing SGLang with plain Hugging Face `generate(inputs_embeds=...)` for the verbalizer.

Reasoning: you only verbalize a few hundred activations, so raw throughput does not matter there. Dropping SGLang removes a dependency and a whole class of bugs. The existing `nla_inference.py` already handles the fiddly tokenization and rescaling, so you are only swapping out the HTTP call at the end. Half a day of work, and it simplifies the stack permanently.

---

## 6. Where to run it

### Recommendation: RunPod, one team account, one network volume, one region

This directly satisfies the "one location, keep it all intact" requirement.

```
  ┌─────────────────────────────────────────┐
  │  Network volume  (persistent, ~$11/mo)  │
  │                                          │
  │   • the 3 checkpoints (~41 GB)          │
  │   • Hugging Face cache                   │
  │   • datasets                             │
  │   • cached steering vectors              │
  │   • all result files                     │
  └─────────────────┬───────────────────────┘
                    │ mounts into
         ┌──────────┴──────────┐
         │  Pod (disposable)   │
         │  A100 or H100       │
         │  stopped when idle  │
         └─────────────────────┘
```

Pods are disposable. The volume is permanent. Nobody's laptop is in the loop. When you stop the pod, you stop paying for GPU but keep everything.

### GPU options and prices

| GPU | Secure Cloud | Community Cloud | Verdict |
|---|---|---|---|
| **A100 80GB PCIe** | $1.39/hr | ~$0.80 to $1.10 | **Start here.** All three models fit in 80 GB at once |
| **H100 PCIe 80GB** | $2.89/hr | $1.99/hr | ~2x faster for ~1.5x price. Use for the big grid |
| L40S 48GB | $0.99/hr | lower | Workable if you load models in stages, but you will be juggling |
| RTX 4090 24GB | $0.69/hr | lower | Too small. Avoid |

Storage: **$0.07 per GB per month.** Budget ~150 GB, so about $11/month.

Memory math for the 80 GB recommendation: base Qwen (15 GB) + verbalizer (16 GB) + reconstructor (10 GB) = 41 GB of weights, plus room for the key-value cache and a decent batch size. Everything coexists comfortably. Below 80 GB you have to load and unload models between stages, which is survivable but annoying.

### Two warnings

**Network volumes are region-locked.** Pick a region with good A100 and H100 stock or you will sit waiting for capacity while your volume is stranded somewhere else.

**Pods bill while idle.** This is the single biggest way to burn the budget. A forgotten pod over a weekend is $50 gone with zero work done. Agree on a team rule now: **stop the pod, keep the volume.**

### Alternative worth considering: Modal

[Modal](https://modal.com/pricing) bills **per second, only while your job actually runs**. Idle burn is structurally impossible.

| | RunPod | Modal |
|---|---|---|
| Mental model | A machine you SSH into | Run a command, it executes remotely |
| H100 rate | $1.99 to $2.89/hr | ~$3.95/hr equivalent |
| Idle cost | **Yes, this is the risk** | Zero, by design |
| Free credits | none standard | **$30/month** |
| Learning curve | low | moderate |
| Persistent servers | natural | awkward |

Modal is arguably the better fit for "keep it all intact," since code lives in git, everyone runs the same command, and results land in a shared volume. The higher hourly rate is offset by never paying for idle time, which in practice is where most of the waste goes.

The tradeoff is the learning curve, and that running a persistent server for the verbalizer is more awkward on serverless.

**This is a real decision, not a formality.** It shapes how the whole codebase gets structured. Decide before anyone writes the first script.

---

## 7. What it should cost

| Item | GPU hours | Cost |
|---|---|---|
| Setup, debugging, getting injection correct | 8 to 15 | $15 to $30 |
| Fidelity check plus verbalization pass | 2 | $3 to $5 |
| Main generation grid | 3 to 6 | $6 to $15 |
| Reruns and a second pass after you find problems | 5 to 10 | $10 to $25 |
| Storage, one month | | ~$11 |
| **Total** | **20 to 35** | **$50 to $90** |

Comfortably under $100, but not by a huge margin, which is why the pod discipline and the staged pipeline both matter.

### Two levers that keep it down

**Lean on the deterministic probes.** Your doc already lists fifteen of them (counting ellipses, em-dashes, list markers, emoji, contractions, and so on). These cost nothing to score and remove judge noise from your results entirely. Make them the primary metrics wherever they fit.

**Do not host a judge model on your own GPU.** Use a cheap fast model through an API for the hedging and refusal categories where you genuinely need judgment. This costs cents and frees your GPU for generation.

---

## 8. Free credits worth chasing

Ordered by how quickly they pay off.

| Program | What you get | Barrier | Timeline |
|---|---|---|---|
| **Modal free tier** | $30/month | Sign up | Immediate |
| **NSF ACCESS "Explore"** | GPU allocation | One-page abstract | Days |
| **Anthropic research credits** | ~$500+ API credits | Application | Weeks |
| **NAIRR Pilot (NSF)** | Free H100/A100, 12-month project | Likely needs institutional sponsorship | ~2 weeks (Start-Up track) |
| **NVIDIA Academic Hardware Grant** | Physical GPUs, AI-safety track exists | Full application | Too slow for this project |

**Start with ACCESS Explore.** Lowest barrier by a wide margin.

**NAIRR is worth a conversation with McNair**, since it likely needs a sponsoring institution and he would be the one to provide it. If it comes through, your compute problem disappears for a year.

**Anthropic credits cover your evaluation costs entirely**, which is not GPU but is a real line item once you start running judge models over thousands of completions.

---

## 9. First week checklist

Steps 3 through 5 are the whole project in miniature. If they work, everything after is grinding through a grid, which is cheap. If step 4 comes back bad, you have learned the most important thing in the study for about ten dollars, and the negative-result framing in your proposal becomes the paper.

- [ ] **1. Clone `kitft/nla-inference` into this folder.** Read `docs/inference.md` end to end. This is the highest-value document in the project. Every failure mode is written down in it, ranked by likelihood

- [ ] **2. Spin up one A100 80GB on RunPod with a network volume.** Pull all three checkpoints onto the volume once, so you never download them again

- [ ] **3. Reproduce the round trip on a handful of activations.** Take a layer-20 vector, verbalize it, reconstruct it, check the score. Target is roughly 0.2 mean-squared-error, which their docs call a "good decode." If you cannot hit that, you have an injection bug, and their checklist tells you where to look

- [ ] **4. Measure round-trip fidelity on YOUR data.** Fifty prompts from each of your three categories. **This is the go/no-go gate.** About two GPU hours

- [ ] **5. Reproduce one steering effect.** Use the difference-of-reconstructions formula from Section 3. Pick the simplest deterministic probe you have, ellipsis or emoji, since both have a near-zero baseline so any movement is unambiguous

- [ ] **6. Verify vllm-lens works with Qwen2.5** and can inject at a single token position

- [ ] **7. Update the proposal** with the three corrections from Section 3

---

## 10. Open decisions

These need answers before implementation starts.

| # | Decision | Options | Why it matters |
|---|---|---|---|
| 1 | **Hosting model** | RunPod persistent pod, or Modal serverless | Shapes the entire codebase structure |
| 2 | **Verbalizer serving** | Keep SGLang, or switch to plain Hugging Face | Removes a dependency and a bug class if you switch |
| 3 | **Injection positions** | One token (as in the paper), or all positions | Paper uses one. Your proposal does not specify. Changes the result |
| 4 | **Primary metrics** | Deterministic probes only, or probes plus judge | Cost and noise. Probes are free and clean |
| 5 | **Who owns the account** | One shared team account, or per-person | "One location" argues for shared. Billing argues for a named owner |

---

## Sources

- [Transformer Circuits post: Natural Language Autoencoders](https://transformer-circuits.pub/2026/nla/)
- [Repo: natural_language_autoencoders](https://github.com/kitft/natural_language_autoencoders)
- [Repo: nla-inference](https://github.com/kitft/nla-inference)
- [Checkpoint: verbalizer](https://huggingface.co/kitft/nla-qwen2.5-7b-L20-av)
- [Checkpoint: reconstructor](https://huggingface.co/kitft/nla-qwen2.5-7b-L20-ar)
- [vllm-lens (UK AI Safety Institute)](https://github.com/UKGovernmentBEIS/vllm-lens)
- [RunPod pricing](https://www.runpod.io/pricing)
- [Modal pricing](https://modal.com/pricing)
- [Free cloud GPU credit programs](https://www.thundercompute.com/blog/free-cloud-gpu-credits)
- [AI compute grants guide](https://grantedai.com/blog/ai-compute-grants-gpu-credits-guide)
