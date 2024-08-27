import csv
from itertools import combinations

from mp_api.client import MPRester


def get_binary_compounds(api_key, metallic_elements):
    compounds_info = []
    with MPRester(api_key) as mpr:
        # Generate all possible pairs of metallic elements
        element_pairs = list(combinations(metallic_elements, 2))

        for pair in element_pairs:
            # Query for binary compounds for each pair
            binary_docs = mpr.materials.summary.search(
                elements=list(pair),
                num_elements=(2, 2),
                energy_above_hull=(0, 0.1),  # Ensuring stability
                fields=[
                    "material_id",
                    "formula_pretty",
                    "elements",
                    "energy_above_hull",
                    "symmetry",
                    "band_gap",
                    "theoretical",
                ],
            )

            # Extract relevant information from the binary compounds
            for doc in binary_docs:
                if not any(
                    elem.symbol
                    in [
                        "O",
                        "S",
                        "Se",
                        "Te",
                        "F",
                        "Cl",
                        "Br",
                        "I",
                        "N",
                        "P",
                        "As",
                    ]
                    for elem in doc.elements
                ):
                    compounds_info.append(
                        {
                            "material_id": doc.material_id,
                            "formula": doc.formula_pretty,
                            "elements": ", ".join(
                                elem.symbol for elem in doc.elements
                            ),
                            "energy_above_hull": doc.energy_above_hull,
                            "crystal_system": doc.symmetry.crystal_system,
                            "band_gap": doc.band_gap,
                            "theoretical": doc.theoretical,
                        }
                    )

    return compounds_info


def save_to_csv(compounds, filename):
    if not compounds:
        print("No compounds to save.")
        return

    keys = compounds[0].keys()
    with open(filename, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(compounds)


api_key = "w1FbQcBbkQZJHyhMJGxssIEttJ8JSGu8"
metallic_elements = [
    "Li",
    "Be",
    "Na",
    "Mg",
    "Al",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Cs",
    "Ba",
    "La",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
]

# Get binary compounds
binary_compounds = get_binary_compounds(api_key, metallic_elements)

# Save compounds to CSV
save_to_csv(binary_compounds, "binary_compounds.csv")

# Print summary
print(f"Total binary compounds found: {len(binary_compounds)}")
print("Results have been saved to 'binary_compounds.csv'")
