"""
Script: Oxidation-state probability analysis for Bi-Te-In system.

Generates plausible Bi-Te-In compositions via SMACT's smact_filter,
computes their compound probabilities using the oxidation-state probability model,
and plots how the search space narrows as a function of probability threshold.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pymatgen.core import Composition

from smact import Element, Species
from smact.oxidation_states import Oxidation_state_probability_finder
from smact.screening import smact_filter


def main():
    """Run the oxidation-state probability analysis for the Bi-Te-In system."""
    # Instantiate the oxidation-state probability finder
    oxfinder = Oxidation_state_probability_finder()

    # Define the Bi-Te-In element system
    elements = [Element("Bi"), Element("Te"), Element("In")]

    # Generate plausible compositions (max stoich threshold = 8)
    comps = smact_filter(elements, threshold=8, oxidation_states_set="icsd24")

    # Prepare lists for species lists and formulas
    species_lists = []
    formulas = []
    for syms, oxs, ratios in comps:
        # Build list of SMACT Species objects
        slist = [Species(sym, ox) for sym, ox in zip(syms, oxs, strict=False)]
        species_lists.append(slist)
        # Construct formula string and reduce it
        raw_formula = "".join(f"{sym}{amt}" for sym, amt in zip(syms, ratios, strict=False))
        reduced = Composition(raw_formula).reduced_formula
        formulas.append(reduced)

    # Compute compound probabilities, skipping species not in probability table
    valid_formulas = []
    valid_probs = []
    for slist, formula in zip(species_lists, formulas, strict=False):
        try:
            p = oxfinder.compound_probability(slist)
        except NameError as e:
            # Skip species pairs not in the probability table
            print(f"Skipping {formula}: {e}")
            continue
        valid_formulas.append(formula)
        valid_probs.append(p)

    # Create a DataFrame of successfully scored compounds
    df = pd.DataFrame({"formula_pretty": valid_formulas, "compound_probability": valid_probs})

    # Print example entries
    print("First 10 compounds and their probabilities:")
    print(df.head(10))

    # Threshold sweep: how many compounds exceed each probability threshold
    thresh_vals = np.linspace(0, 1, 100)
    counts = [(df.compound_probability >= t).sum() for t in thresh_vals]

    # Plot search-space narrowing
    plt.figure(figsize=(8, 4))
    plt.plot(thresh_vals, counts, marker="x", color="orange")
    plt.xlabel("Probability threshold")
    plt.ylabel("Number of valid compounds")
    plt.title("Search-space narrowing for Bi-Te-In system")
    plt.grid(visible=True)
    plt.tight_layout()
    plt.show()

    # -----------------------------------------------------------------------------
    # Plotly ternary: composition distribution at various probability thresholds
    # Select probability thresholds to visualize
    prob_thresholds = [0.0, 0.2, 0.4, 0.6, 0.8]
    fig_t = go.Figure()
    for thr in prob_thresholds:
        # Subset compounds above threshold
        df_thr = df[df.compound_probability >= thr]
        a_vals, b_vals, c_vals = [], [], []
        for formula in df_thr["formula_pretty"]:
            comp = Composition(formula)
            bi = comp.get("Bi", 0)
            te = comp.get("Te", 0)
            in_ = comp.get("In", 0)
            total = bi + te + in_
            a_vals.append(bi / total)
            b_vals.append(te / total)
            c_vals.append(in_ / total)
        fig_t.add_trace(
            go.Scatterternary(
                a=a_vals, b=b_vals, c=c_vals, mode="markers", marker=dict(size=8, opacity=0.7), name=f"P ≥ {thr:.1f}"
            )
        )
    # Layout styling
    fig_t.update_layout(
        title="Bi-Te-In composition narrowing with probability threshold",
        font=dict(size=12),
        width=600,
        height=600,
        ternary=dict(
            aaxis=dict(title="Bi"),
            baxis=dict(title="Te"),
            caxis=dict(title="In"),
        ),
        margin=dict(l=50, r=50, b=50, t=50),
    )
    fig_t.show()


if __name__ == "__main__":
    main()
