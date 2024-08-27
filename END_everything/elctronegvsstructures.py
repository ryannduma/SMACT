import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(file_name):
    data = pd.read_csv(file_name)

    # Clean and convert electronegativity_difference to numeric
    data["electronegativity_difference"] = pd.to_numeric(
        data["electronegativity_difference"], errors="coerce"
    )

    # Remove any rows with NaN values in electronegativity_difference
    data = data.dropna(subset=["electronegativity_difference"])

    # Convert is_metal to boolean
    data["is_metal"] = data["is_metal"].astype(str).str.lower() == "true"

    return data


def plot_electronegativity_vs_crystal_system(data, compound_type):
    plt.figure(figsize=(14, 7))

    # Plot for metallic compounds
    sns.boxplot(
        x="crystal_system",
        y="electronegativity_difference",
        data=data[data["is_metal"]],
        color="lightblue",
        width=0.5,
        positions=np.arange(len(data["crystal_system"].unique())) - 0.2,
    )

    # Plot for non-metallic compounds
    sns.boxplot(
        x="crystal_system",
        y="electronegativity_difference",
        data=data[~data["is_metal"]],
        color="lightgreen",
        width=0.5,
        positions=np.arange(len(data["crystal_system"].unique())) + 0.2,
    )

    plt.title(
        f"Electronegativity Difference vs Crystal System for {compound_type.capitalize()} Compounds"
    )
    plt.xlabel("Crystal System")
    plt.ylabel("Electronegativity Difference")
    plt.xticks(rotation=45)
    plt.legend(["Metallic", "Non-metallic"])
    plt.tight_layout()
    plt.savefig(f"electronegativity_vs_crystal_system_{compound_type}.png")
    plt.close()


def plot_electronegativity_vs_spacegroup(data, compound_type):
    plt.figure(figsize=(15, 8))

    # Plot for metallic compounds
    sns.scatterplot(
        x="spacegroup_number",
        y="electronegativity_difference",
        data=data[data["is_metal"]],
        color="blue",
        alpha=0.5,
        label="Metallic",
    )

    # Plot for non-metallic compounds
    sns.scatterplot(
        x="spacegroup_number",
        y="electronegativity_difference",
        data=data[~data["is_metal"]],
        color="green",
        alpha=0.5,
        label="Non-metallic",
    )

    plt.title(
        f"Electronegativity Difference vs Space Group for {compound_type.capitalize()} Compounds"
    )
    plt.xlabel("Space Group Number")
    plt.ylabel("Electronegativity Difference")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"electronegativity_vs_spacegroup_{compound_type}.png")
    plt.close()


compound_types = ["binary", "ternary", "quaternary"]

for compound_type in compound_types:
    file_name = f"{compound_type}_compounds_with_electronegativity.csv"

    data = load_data(file_name)

    plot_electronegativity_vs_crystal_system(data, compound_type)
    plot_electronegativity_vs_spacegroup(data, compound_type)

    print(f"Plots for {compound_type} compounds have been generated.")

print("All compound types have been processed and plotted.")
