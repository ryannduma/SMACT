import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def load_data(file_name):
    data = pd.read_csv(file_name)
    
    # Filter for metallic compounds
    data = data[data['is_metal'].astype(str).str.lower() == 'true']
    
    # Clean and convert electronegativity_difference to numeric
    data['electronegativity_difference'] = pd.to_numeric(data['electronegativity_difference'], errors='coerce')
    
    # Remove any rows with NaN values in electronegativity_difference
    data = data.dropna(subset=['electronegativity_difference'])
    
    return data

def plot_electronegativity_vs_crystal_system(data, compound_type):
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='crystal_system', y='electronegativity_difference', data=data)
    plt.title(f'Electronegativity Difference vs Crystal System for {compound_type.capitalize()} Compounds')
    plt.xlabel('Crystal System')
    plt.ylabel('Electronegativity Difference')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'electronegativity_vs_crystal_system_{compound_type}.png')
    plt.close()

def plot_electronegativity_vs_spacegroup(data, compound_type):
    plt.figure(figsize=(15, 8))
    sns.scatterplot(x='spacegroup_number', y='electronegativity_difference', data=data)
    plt.title(f'Electronegativity Difference vs Space Group for {compound_type.capitalize()} Compounds')
    plt.xlabel('Space Group Number')
    plt.ylabel('Electronegativity Difference')
    plt.tight_layout()
    plt.savefig(f'electronegativity_vs_spacegroup_{compound_type}.png')
    plt.close()

compound_types = ['binary', 'ternary', 'quaternary']

for compound_type in compound_types:
    file_name = f'{compound_type}_compounds_with_electronegativity.csv'
    
    data = load_data(file_name)
    
    plot_electronegativity_vs_crystal_system(data, compound_type)
    plot_electronegativity_vs_spacegroup(data, compound_type)
    
    print(f"Plots for {compound_type} compounds have been generated.")

print("All compound types have been processed and plotted.")