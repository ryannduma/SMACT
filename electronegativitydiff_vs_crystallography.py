import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(metallic_file, non_metallic_file):
    metallic_data = pd.read_csv(metallic_file)
    non_metallic_data = pd.read_csv(non_metallic_file)

    # Clean and convert electronegativity_difference to numeric
    for data in [metallic_data, non_metallic_data]:
        data["electronegativity_difference"] = pd.to_numeric(
            data["electronegativity_difference"], errors="coerce"
        )
        data.dropna(subset=["electronegativity_difference"], inplace=True)

    metallic_data["is_metal"] = True
    non_metallic_data["is_metal"] = False

    return pd.concat([metallic_data, non_metallic_data])


def plot_electronegativity_vs_crystal_system(data, compound_type):
    plt.figure(figsize=(14, 7))

    # Plot for metallic compounds
    sns.boxplot(
        x="crystal_system",
        y="electronegativity_difference",
        data=data[data["is_metal"]],
        color="darkblue",
        width=0.5,
        positions=np.arange(len(data["crystal_system"].unique())) - 0.2,
    )

    # Plot for non-metallic compounds
    sns.boxplot(
        x="crystal_system",
        y="electronegativity_difference",
        data=data[~data["is_metal"]],
        color="red",
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
        color="darkblue",
        alpha=0.5,
        label="Metallic",
    )

    # Plot for non-metallic compounds
    sns.scatterplot(
        x="spacegroup_number",
        y="electronegativity_difference",
        data=data[~data["is_metal"]],
        color="red",
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


def plot_electronegativity_distribution(data, compound_type):
    plt.figure(figsize=(12, 6))

    # Plot for metallic compounds
    sns.histplot(
        data=data[data["is_metal"]],
        y="electronegativity_difference",
        kde=True,
        color="darkblue",
        label="Metallic",
        alpha=0.5,
    )

    # Plot for non-metallic compounds
    sns.histplot(
        data=data[~data["is_metal"]],
        y="electronegativity_difference",
        kde=True,
        color="red",
        label="Non-metallic",
        alpha=0.5,
    )

    plt.title(
        f"Distribution of Electronegativity Differences for {compound_type.capitalize()} Compounds"
    )
    plt.xlabel("Count")
    plt.ylabel("Electronegativity Difference")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"electronegativity_distribution_{compound_type}.png")
    plt.close()


compound_types = ["binary"]

for compound_type in compound_types:
    metallic_file = f"{compound_type}_metallic_compounds_with_electronegativity.csv"
    non_metallic_file = f"{compound_type}_non_metallic_compounds_with_electronegativity.csv"

    data = load_data(metallic_file, non_metallic_file)

    plot_electronegativity_vs_crystal_system(data, compound_type)
    plot_electronegativity_vs_spacegroup(data, compound_type)
    plot_electronegativity_distribution(data, compound_type)

    print(f"Plots for {compound_type} compounds have been generated.")

print("All compound types have been processed and plotted.")
