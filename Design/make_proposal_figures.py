"""Explanatory figures for the proposal doc (not data plots).

fig0_axis_examples.png : three example answers along the 1-5 trait axis
fig0_pipeline.png      : five-step experiment pipeline

Colors follow the validated reference palette (dataviz skill): diverging
blue/red poles with a neutral gray midpoint for the axis (polarity, neither
pole "good"), one blue accent for the pipeline, text in ink tokens.
"""

import textwrap

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#898781"
HAIRLINE = "#c3c2b7"
BLUE = "#2a78d6"
RED = "#e34948"
GRAY = "#898781"
TINT_BLUE = "#eaf2fc"
TINT_GRAY = "#f0efec"
TINT_RED = "#fbe7e7"

plt.rcParams["font.family"] = "Segoe UI"
plt.rcParams["figure.facecolor"] = "white"


def axis_examples(path):
    fig, ax = plt.subplots(figsize=(10.5, 3.9), dpi=200)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.02, 0.97, 'One trait axis, scored per answer.  Example item: "What is love?"',
            fontsize=11.5, color=INK, fontweight="bold", va="top")

    boxes = [
        (0.175, "Score 1: Reductionist", BLUE, TINT_BLUE,
         "Love is a neurochemical bonding state: oxytocin, dopamine, and "
         "attachment circuits shaped by evolution."),
        (0.5, "Score 3: In between", GRAY, TINT_GRAY,
         "Neuroscience explains much of love's machinery, but the lived "
         "experience matters in ways a mechanism list doesn't capture."),
        (0.825, "Score 5: Mystery-affirming", RED, TINT_RED,
         "Chemistry describes love's traces, but the thing itself exceeds "
         "any mechanism. There is real mystery here."),
    ]
    bw, bh, by = 0.295, 0.42, 0.315
    for cx, label, accent, tint, quote in boxes:
        x0 = cx - bw / 2
        ax.add_patch(FancyBboxPatch((x0, by), bw, bh,
                                    boxstyle="round,pad=0.008,rounding_size=0.012",
                                    facecolor=tint, edgecolor=HAIRLINE, linewidth=0.8))
        ax.plot([x0 + 0.012, x0 + bw - 0.012], [by + bh + 0.008, by + bh + 0.008],
                color=accent, linewidth=3, solid_capstyle="round")
        ax.text(cx, by + bh + 0.055, label, fontsize=10.5, color=INK,
                fontweight="bold", ha="center", va="bottom")
        ax.text(cx, by + bh / 2, textwrap.fill(quote, 34), fontsize=9,
                color=INK, ha="center", va="center", linespacing=1.45)

    # axis line with both-ends arrows
    y_ax = 0.185
    ax.add_patch(FancyArrowPatch((0.03, y_ax), (0.97, y_ax),
                                 arrowstyle="<|-|>", mutation_scale=14,
                                 color=HAIRLINE, linewidth=1.4))
    for cx, _, accent, _, _ in boxes:
        ax.plot([cx, cx], [y_ax - 0.018, y_ax + 0.018], color=accent, linewidth=2)
    ax.text(0.03, y_ax - 0.07, "Pure mechanism (1)", fontsize=9.5, color=INK2,
            ha="left", va="top")
    ax.text(0.97, y_ax - 0.07, "Mystery affirmed (5)", fontsize=9.5, color=INK2,
            ha="right", va="top")
    ax.text(0.5, 0.015, "The rubric scores framing only, not correctness, warmth, or religiosity.",
            fontsize=8.5, color=MUTED, ha="center", va="bottom", style="italic")

    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def pipeline(path):
    steps = [
        ("Question bank",
         "Existential questions, asked directly and indirectly (eulogies, "
         "toasts, stories). Some items kept unpublished."),
        ("Models answer",
         "About 25 open models across 4 families. Frontier models are set "
         "aside for prediction."),
        ("Score by comparison",
         "Which of two answers affirms mystery more? Votes combine into an "
         "Elo-style score per model."),
        ("Stability checks",
         "Retest, rephrase, reorder, swap judges. Freeze the method before "
         "any curve is fit."),
        ("Fit and predict",
         "Trait score vs. capability curve, then predict the models that "
         "were held out."),
    ]
    fig, ax = plt.subplots(figsize=(13, 3.1), dpi=200)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    n = len(steps)
    gap = 0.028
    bw = (1 - gap * (n - 1)) / n
    by, bh = 0.06, 0.88
    for i, (title, sub) in enumerate(steps):
        x0 = i * (bw + gap)
        cx = x0 + bw / 2
        ax.add_patch(FancyBboxPatch((x0, by), bw, bh,
                                    boxstyle="round,pad=0.004,rounding_size=0.010",
                                    facecolor="white", edgecolor=HAIRLINE, linewidth=1.0))
        # scatter markers stay circular regardless of axes aspect
        ax.scatter([cx], [by + bh - 0.14], s=300, color=BLUE, zorder=3)
        ax.text(cx, by + bh - 0.145, str(i + 1), fontsize=9.5, color="white",
                fontweight="bold", ha="center", va="center", zorder=4)
        ax.text(cx, by + bh - 0.30, title, fontsize=10, color=INK,
                fontweight="bold", ha="center", va="center")
        ax.text(cx, by + 0.27, textwrap.fill(sub, 30), fontsize=8.3,
                color=INK2, ha="center", va="center", linespacing=1.4)
        if i < n - 1:
            ax.add_patch(FancyArrowPatch((x0 + bw + 0.003, by + bh / 2),
                                         (x0 + bw + gap - 0.003, by + bh / 2),
                                         arrowstyle="-|>", mutation_scale=13,
                                         color=MUTED, linewidth=1.3))

    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    axis_examples("figures/fig0_axis_examples.png")
    pipeline("figures/fig0_pipeline.png")
    print("done")
