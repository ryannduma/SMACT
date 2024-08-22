from mp_api.client import MPRester
import csv

def get_all_compounds(api_key, limit=10000):
    compounds_info = []
    with MPRester(api_key) as mpr:
        docs = mpr.materials.summary.search(
            fields=[
                "material_id", 'formula_pretty', 'elements', 'energy_above_hull', 
                'symmetry', 'spacegroup_number', 'spacegroup_symbol', 'band_gap', 'theoretical', 'nelements', 'is_metal'
            ],
            chunk_size=limit
        )
    
    for doc in docs:
        compounds_info.append({
            "material_id": doc.material_id,
            "formula": doc.formula_pretty,
            "elements": ", ".join(elem.symbol for elem in doc.elements),
            "num_elements": doc.nelements,
            "energy_above_hull": doc.energy_above_hull,
            "crystal_system": doc.symmetry.crystal_system,
            "spacegroup_number": doc.symmetry.number,
            "spacegroup_symbol": doc.symmetry.symbol,
            "band_gap": doc.band_gap,
            "theoretical": doc.theoretical,
            "is_metal": doc.is_metal
        })
    return compounds_info

def filter_binary_compounds(compounds):
    return [
        compound for compound in compounds
        if compound['num_elements'] == 2
        and isinstance(compound['energy_above_hull'], (int, float)) and compound['energy_above_hull'] <= 0.1
    ]

def filter_binary_metallic_compounds(compounds, metallic_elements):
    return [
        compound for compound in compounds
        if compound['num_elements'] == 2
        and all(element in metallic_elements for element in compound['elements'].split(', '))
        and isinstance(compound['energy_above_hull'], (int, float)) and compound['energy_above_hull'] <= 0.1
    ]

def save_to_csv(compounds, filename):
    if not compounds:
        print(f"No compounds to save to {filename}.")
        return
    
    keys = compounds[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(compounds)

api_key = 'w1FbQcBbkQZJHyhMJGxssIEttJ8JSGu8'
metallic_elements = [
    "Li", "Be", "Na", "Mg", "Al", "K", "Ca", "Sc", "Ti", "V", 
    "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Rb", "Sr", 
    "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", 
    "In", "Sn", "Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", 
    "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi"
]

# Get all compounds
print("Retrieving all compounds...")
all_compounds = get_all_compounds(api_key)
print(f"Total compounds retrieved: {len(all_compounds)}")

# Filter all binary compounds
print("Filtering all binary compounds...")
all_binary_compounds = filter_binary_compounds(all_compounds)

# Filter binary metallic compounds
print("Filtering binary metallic compounds...")
binary_metallic_compounds = filter_binary_metallic_compounds(all_compounds, metallic_elements)

# Filter binary non-metallic compounds
binary_non_metallic_compounds = [compound for compound in all_binary_compounds if compound not in binary_metallic_compounds]

# Save compounds to CSV
save_to_csv(all_binary_compounds, 'all_binary_compounds.csv')
save_to_csv(binary_metallic_compounds, 'binary_metallic_compounds.csv')
save_to_csv(binary_non_metallic_compounds, 'binary_non_metallic_compounds.csv')

# Print summary
print(f"Total binary compounds found: {len(all_binary_compounds)}")
print(f"Total binary metallic compounds found: {len(binary_metallic_compounds)}")
print(f"Total binary non-metallic compounds found: {len(binary_non_metallic_compounds)}")
print("Results have been saved to 'all_binary_compounds.csv', 'binary_metallic_compounds.csv', and 'binary_non_metallic_compounds.csv'")