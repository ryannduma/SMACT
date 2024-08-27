import csv

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(vec_file, compound_file):
    vec_data = pd.read_csv(vec_file)
    compound_data = pd.read_csv(compound_file)

    # Filter for metallic and non-metallic compounds
    metal_data = vec_data[
        vec_data["is_metal"].astype(str).str.lower() == "true"
    ]
    non_metal_data = vec_data[
        vec_data["is_metal"].astype(str).str.lower() == "false"
    ]

    # Clean and convert VEC_count to numeric
    metal_data["VEC_count"] = pd.to_numeric(
        metal_data["VEC_count"], errors="coerce"
    )
    non_metal_data["VEC_count"] = pd.to_numeric(
        non_metal_data["VEC_count"], errors="coerce"
    )

    # Merge the data based on material_id
    metal_merged_data = pd.merge(metal_data, compound_data, on="material_id")
    non_metal_merged_data = pd.merge(
        non_metal_data, compound_data, on="material_id"
    )

    # Remove any rows with NaN values in VEC_count
    metal_merged_data = metal_merged_data.dropna(subset=["VEC_count"])
    non_metal_merged_data = non_metal_merged_data.dropna(subset=["VEC_count"])

    return metal_merged_data, non_metal_merged_data


def plot_vec_vs_crystal_system(metal_data, non_metal_data, compound_type):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="crystal_system", y="VEC_count", data=metal_data, color="red")
    sns.boxplot(
        x="crystal_system", y="VEC_count", data=non_metal_data, color="green"
    )
    plt.title(
        f"VEC vs Crystal System for {compound_type.capitalize()} Compounds"
    )
    plt.xlabel("Crystal System")
    plt.ylabel("VEC")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"vec_vs_crystal_system2_{compound_type}.png")
    plt.close()


def plot_vec_vs_spacegroup(metal_data, non_metal_data, compound_type):
    plt.figure(figsize=(15, 8))
    sns.scatterplot(
        x="spacegroup_number",
        y="VEC_count",
        data=metal_data,
        color="red",
        label="Metal",
    )
    sns.scatterplot(
        x="spacegroup_number",
        y="VEC_count",
        data=non_metal_data,
        color="green",
        label="Non-Metal",
    )
    plt.title(f"VEC vs Space Group for {compound_type.capitalize()} Compounds")
    plt.xlabel("Space Group Number")
    plt.ylabel("VEC")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"vec_vs_spacegroup_{compound_type}.png")
    plt.close()


def plot_heatmap(metal_data, non_metal_data, compound_type):
    metal_pivot = pd.pivot_table(
        metal_data,
        values="VEC_count",
        index="crystal_system",
        columns="spacegroup_number",
        aggfunc="mean",
    )
    non_metal_pivot = pd.pivot_table(
        non_metal_data,
        values="VEC_count",
        index="crystal_system",
        columns="spacegroup_number",
        aggfunc="mean",
    )

    plt.figure(figsize=(20, 10))
    sns.heatmap(metal_pivot, cmap="Reds", annot=False)
    sns.heatmap(non_metal_pivot, cmap="Greens", annot=False, alpha=0.5)
    plt.title(
        f"VEC Heatmap: Crystal System vs Space Group for {compound_type.capitalize()} Compounds"
    )
    plt.xlabel("Space Group Number")
    plt.ylabel("Crystal System")
    plt.tight_layout()
    plt.savefig(f"vec_heatmap_{compound_type}.png")
    plt.close()


compound_types = ["binary", "ternary", "quaternary"]

for compound_type in compound_types:
    vec_file = f"VECcount_plusgram_{compound_type}.csv"
    compound_file = f"{compound_type}_compounds.csv"

    metal_data, non_metal_data = load_data(vec_file, compound_file)

    plot_vec_vs_crystal_system(metal_data, non_metal_data, compound_type)
    plot_vec_vs_spacegroup(metal_data, non_metal_data, compound_type)
    plot_heatmap(metal_data, non_metal_data, compound_type)

    print(f"Plots for {compound_type} compounds have been generated.")

print("All compound types have been processed and plotted.")
