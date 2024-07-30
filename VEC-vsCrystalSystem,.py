import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def load_data(vec_file, compound_file):
    vec_data = pd.read_csv(vec_file)
    compound_data = pd.read_csv(compound_file)
    
    # Merge the data based on material_id
    merged_data = pd.merge(vec_data, compound_data, on='material_id')
    
    # Filter for metallic compounds
    metallic_data = merged_data[merged_data['is_metal'] == True]
    
    return metallic_data

def plot_vec_vs_crystal_system(data, compound_type):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='crystal_system', y='VEC_count', data=data)
    plt.title(f'VEC vs Crystal System for {compound_type.capitalize()} Compounds')
    plt.xlabel('Crystal System')
    plt.ylabel('VEC')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'vec_vs_crystal_system_{compound_type}.png')
    plt.close()

def plot_vec_vs_spacegroup(data, compound_type):
    plt.figure(figsize=(15, 8))
    sns.scatterplot(x='spacegroup_number', y='VEC_count', data=data)
    plt.title(f'VEC vs Space Group for {compound_type.capitalize()} Compounds')
    plt.xlabel('Space Group Number')
    plt.ylabel('VEC')
    plt.tight_layout()
    plt.savefig(f'vec_vs_spacegroup_{compound_type}.png')
    plt.close()

def plot_heatmap(data, compound_type):
    pivot = pd.pivot_table(data, values='VEC_count', index='crystal_system', columns='spacegroup_number', aggfunc='mean')
    plt.figure(figsize=(20, 10))
    sns.heatmap(pivot, cmap='viridis', annot=False)
    plt.title(f'VEC Heatmap: Crystal System vs Space Group for {compound_type.capitalize()} Compounds')
    plt.xlabel('Space Group Number')
    plt.ylabel('Crystal System')
    plt.tight_layout()
    plt.savefig(f'vec_heatmap_{compound_type}.png')
    plt.close()

compound_types = ['binary', 'ternary', 'quaternary']

for compound_type in compound_types:
    vec_file = f'VECcount_plusgram_{compound_type}.csv'
    compound_file = f'{compound_type}_compounds.csv'
    
    data = load_data(vec_file, compound_file)
    
    plot_vec_vs_crystal_system(data, compound_type)
    plot_vec_vs_spacegroup(data, compound_type)
    plot_heatmap(data, compound_type)
    
    print(f"Plots for {compound_type} compounds have been generated.")

print("All compound types have been processed and plotted.")
