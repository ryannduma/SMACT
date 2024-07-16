from mp_api.client import MPRester
from itertools import combinations

def get_binary_compounds(api_key, metallic_elements):
    compounds_info = []
    with MPRester(api_key) as mpr:
        # Generate all possible pairs of metallic elements
        element_pairs = list(combinations(metallic_elements, 2)) #  
        
        for pair in element_pairs:
            # Query for binary compounds for each pair
            binary_docs = mpr.materials.summary.search(
                elements=list(pair),
                num_elements=(2,2),
                energy_above_hull=(0, 0.1),  # Ensuring stability
                fields=["material_id", 'formula_pretty', 'elements', 'energy_above_hull', 'symmetry', 'band_gap']
            )
            
            # Extract relevant information from the binary compounds
            for doc in binary_docs:
                if not any(elem.symbol in ["O", "S", "Se", "Te", "F", "Cl", "Br", "I", "N", "P", "As"] for elem in doc.elements):
                    compounds_info.append({
                        "material_id": doc.material_id,
                        "formula": doc.formula_pretty,
                        "elements": [elem.symbol for elem in doc.elements],
                        "energy_above_hull": doc.energy_above_hull,
                        "crystal_system": doc.symmetry.crystal_system,
                        "band_gap": doc.band_gap
                    })
    
    return compounds_info

api_key = 'w1FbQcBbkQZJHyhMJGxssIEttJ8JSGu8'
metallic_elements = [
    "Li", "Be", "Na", "Mg", "Al", "K", "Ca", "Sc", "Ti", "V", 
    "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Rb", "Sr", 
    "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", 
    "In", "Sn", "Cs", "Ba", "La", "Hf", "Ta", "W", "Re", "Os", 
    "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi"
]

# Get binary compounds
binary_compounds = get_binary_compounds(api_key, metallic_elements)

# Print the list of binary compounds
for compound in binary_compounds:
    print(f"Material ID: {compound['material_id']}")
    print(f"Formula: {compound['formula']}")
    print(f"Elements: {', '.join(compound['elements'])}")
    print(f"Energy above hull: {compound['energy_above_hull']} eV/atom")
    print(f"Crystal system: {compound['crystal_system']}")
    print(f"Band gap: {compound['band_gap']} eV")
    print("---")