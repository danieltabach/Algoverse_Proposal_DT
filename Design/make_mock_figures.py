"""Mock figures for the Character Scaling proposal.
All data is SYNTHETIC / illustrative - these show what each target figure
would look like under a 'clean emergence' outcome. Regenerate: python make_mock_figures.py
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)
OUT = "figures"
import os
os.makedirs(OUT, exist_ok=True)

FAMILIES = {
    "Qwen2.5 (0.5B-72B)":  {"color": "#4C72B0", "n": 7,  "lo": -2.5, "hi": 2.5},
    "Llama-3.x (1B-70B)":  {"color": "#DD8452", "n": 5,  "lo": -2.0, "hi": 2.2},
    "Gemma (2B-27B)":      {"color": "#55A868", "n": 4,  "lo": -1.5, "hi": 1.5},
    "OLMo-2":              {"color": "#C44E52", "n": 4,  "lo": -2.2, "hi": 0.8},
}
HELDOUT = {"GPT-5.x": 3.4, "Claude Opus": 3.6, "Gemini Ultra": 3.2, "Qwen-Max": 2.9}

def sigmoid(x): return 1 / (1 + np.exp(-x))
def true_curve(x): return 0.15 + 0.55 * sigmoid(1.8 * (x - 1.6))

def watermark(fig):
    fig.text(0.5, 0.5, "MOCK DATA", fontsize=48, color="gray", alpha=0.13,
             ha="center", va="center", rotation=25, zorder=0)
    fig.text(0.99, 0.01, "Synthetic illustrative data - not results",
             fontsize=7, color="gray", ha="right", va="bottom")

# ---------------- Fig 1: trait vs capability ----------------
fig, ax = plt.subplots(figsize=(7.2, 4.8))
xs_all, ys_all = [], []
for name, f in FAMILIES.items():
    x = np.linspace(f["lo"], f["hi"], f["n"])
    y = true_curve(x) + rng.normal(0, 0.035, f["n"])
    ax.scatter(x, y, s=55, color=f["color"], label=name, zorder=3, edgecolor="white", lw=0.6)
    xs_all += list(x); ys_all += list(y)
for name, hx in HELDOUT.items():
    hy = true_curve(hx) + rng.normal(0, 0.03)
    ax.scatter(hx, hy, marker="*", s=260, color="#8172B3", zorder=4, edgecolor="black", lw=0.6)
    ax.annotate(name, (hx, hy), textcoords="offset points", xytext=(6, -12), fontsize=7.5)
grid = np.linspace(-3, 4.2, 200)
ax.plot(grid, true_curve(grid), "k-", lw=1.8, label="sigmoid fit (trained on non-held-out)", zorder=2)
ax.fill_between(grid, true_curve(grid) - 0.05, true_curve(grid) + 0.05, color="k", alpha=0.10, zorder=1)
ax.axvline(1.6, color="gray", ls=":", lw=1)
ax.annotate("capability 'knee'\n(would-be emergence point)", (1.6, 0.2), textcoords="offset points",
            xytext=(10, 0), fontsize=8, color="gray")
ax.scatter([], [], marker="*", s=160, color="#8172B3", edgecolor="black", lw=0.6, label="held-out frontier models")
ax.set_xlabel("Capability (PC1 of benchmark scores)")
ax.set_ylabel("Trait score (Bradley-Terry, normalized)\nreductionism (0) $\\leftrightarrow$ mystery affirmation (1)")
ax.set_title("Fig 1 (target): Mystery-affirmation vs. capability across model families")
ax.legend(fontsize=7.5, loc="upper left", framealpha=0.9)
ax.set_ylim(0, 1)
watermark(fig); fig.tight_layout(); fig.savefig(f"{OUT}/fig1_trait_vs_capability.png", dpi=160); plt.close(fig)

# ---------------- Fig 2: holdout prediction ----------------
fig, ax = plt.subplots(figsize=(4.8, 4.6))
names = list(HELDOUT) + ["Llama-3.1-405B", "Qwen2.5-72B", "Gemma-27B"]
pred = np.array([true_curve(v) for v in list(HELDOUT.values()) + [2.6, 2.5, 1.5]])
obs = pred + rng.normal(0, 0.035, len(pred))
ax.plot([0, 1], [0, 1], "k--", lw=1, label="perfect prediction")
ax.scatter(pred, obs, s=70, color="#8172B3", edgecolor="black", lw=0.6, zorder=3)
for n, p, o in zip(names, pred, obs):
    ax.annotate(n, (p, o), textcoords="offset points", xytext=(6, -4), fontsize=7)
ax.set_xlabel("Predicted trait score (fit on weaker models)")
ax.set_ylabel("Observed trait score")
ax.set_title("Fig 2 (target): Held-out prediction\n('scaling law' vs 'trendline')", fontsize=10.5)
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.legend(fontsize=8)
ax.text(0.05, 0.9, "MSE = 0.0012 (mock)", fontsize=8, transform=ax.transAxes)
watermark(fig); fig.tight_layout(); fig.savefig(f"{OUT}/fig2_holdout_prediction.png", dpi=160); plt.close(fig)

# ---------------- Fig 3: attractor susceptibility ----------------
fig, ax = plt.subplots(figsize=(7.0, 4.6))
def p_entry(x): return 0.03 + 0.6 * sigmoid(2.2 * (x - 2.3))
for name, f in FAMILIES.items():
    x = np.linspace(f["lo"], f["hi"], f["n"])
    n_runs = 50
    p = np.clip(p_entry(x) + rng.normal(0, 0.02, len(x)), 0.005, 0.99)
    k = rng.binomial(n_runs, p)
    phat = k / n_runs
    err = 1.96 * np.sqrt(phat * (1 - phat) / n_runs)
    ax.errorbar(x, phat, yerr=err, fmt="o", ms=6, color=f["color"], label=name, capsize=2, lw=1)
cx, cp = 3.6, 0.92
ax.errorbar([cx], [cp], yerr=[[0.05], [0.04]], fmt="*", ms=18, color="#8172B3", capsize=2)
ax.annotate("Claude Opus\n(System Card: ~90-100% self-talk,\n~13% adversarial)", (cx, cp),
            textcoords="offset points", xytext=(-130, -35), fontsize=7.5)
grid = np.linspace(-3, 4.2, 200)
ax.plot(grid, p_entry(grid), "k-", lw=1.6, label="logistic fit")
ax.set_xlabel("Capability (PC1)")
ax.set_ylabel("P(bliss-register entry within 30 turns)\nover ~50 seeded self-talk runs")
ax.set_title("Fig 3 (target): Attractor susceptibility vs. capability - first cross-vendor test")
ax.legend(fontsize=7.5, loc="upper left"); ax.set_ylim(0, 1)
watermark(fig); fig.tight_layout(); fig.savefig(f"{OUT}/fig3_attractor_susceptibility.png", dpi=160); plt.close(fig)

# ---------------- Fig 4: stability panel ----------------
fig, ax = plt.subplots(figsize=(6.4, 4.2))
checks = ["Test-retest\n(3 reruns)", "Paraphrase\n(3 sets)", "Item order\n(shuffled)",
          "Judge swap\n(2 families)", "Judge vs human\n(200 pairs)"]
vals = [0.84, 0.78, 0.81, 0.74, 0.77]
bars = ax.bar(checks, vals, color="#4C72B0", width=0.6)
ax.axhline(0.7, color="crimson", ls="--", lw=1.4)
ax.text(4.45, 0.705, "preregistered pass threshold (0.70)", color="crimson", fontsize=8, ha="right", va="bottom")
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}", ha="center", fontsize=8.5)
ax.set_ylim(0, 1)
ax.set_ylabel("Correlation / agreement")
ax.set_title("Fig 4 (target): Eval stability battery\n(the answer to the personality-instability literature)", fontsize=10.5)
watermark(fig); fig.tight_layout(); fig.savefig(f"{OUT}/fig4_stability_panel.png", dpi=160); plt.close(fig)

# ---------------- Fig 5: template depth ----------------
fig, ax = plt.subplots(figsize=(6.8, 4.2))
fams = ["GPT family", "Claude family", "Gemini family", "Qwen", "Llama", "Gemma"]
direct = np.array([0.20, 0.55, 0.30, 0.34, 0.30, 0.27])
indirect = np.array([0.43, 0.60, 0.46, 0.38, 0.35, 0.42])
xpos = np.arange(len(fams)); w = 0.36
ax.bar(xpos - w/2, direct, w, label="Direct questions ('What is love?')", color="#4C72B0")
ax.bar(xpos + w/2, indirect, w, label="Indirect probes (eulogies, toasts, stories)", color="#DD8452")
for i in range(len(fams)):
    gap = indirect[i] - direct[i]
    ax.annotate(f"$\\Delta$={gap:+.2f}", (xpos[i], max(direct[i], indirect[i]) + 0.02), ha="center", fontsize=8)
ax.set_xticks(xpos); ax.set_xticklabels(fams, fontsize=8.5)
ax.set_ylabel("Trait score")
ax.set_title("Fig 5 (target): Template depth - does a policy script mask the disposition?", fontsize=10.5)
ax.legend(fontsize=8); ax.set_ylim(0, 0.78)
watermark(fig); fig.tight_layout(); fig.savefig(f"{OUT}/fig5_template_depth.png", dpi=160); plt.close(fig)

print("wrote 5 figures to", OUT)
