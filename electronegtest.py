import csv
import re
from math import sqrt
from typing import Dict, List, Any


def load_electronegativity_data(filename: str) -> Dict[str, float]:
    """Load electronegativity data from the magpiery.csv file."""
    electronegativity = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            element = row["element"]
            en = float(row["Electronegativity"])
            electronegativity[element] = en
    return electronegativity


def parse_formula(formula: str) -> Dict[str, int]:
    """Parse chemical formula and return a dictionary of elements and their counts."""
    pattern = re.compile(r"([A-Z][a-z]*)(\d*)")
    elements = pattern.findall(formula)
    return {elem: int(count) if count else 1 for elem, count in elements}


def calculate_atomic_concentrations(formula: str) -> Dict[str, float]:
    """Calculate atomic concentrations from the chemical formula."""
    parsed_formula = parse_formula(formula)
    total_atoms = sum(parsed_formula.values())
    return {elem: count / total_atoms for elem, count in parsed_formula.items()}


def calculate_electronegativity_difference(formula: str, electronegativity: Dict[str, float]) -> float:
    """Calculate the electronegativity difference."""
    concentrations = calculate_atomic_concentrations(formula)

    # Calculate average electronegativity
    avg_electronegativity = sum(
        electronegativity[elem] * conc for elem, conc in concentrations.items()
    )

    # Calculate electronegativity difference
    diff_sum = sum(
        concentrations[elem]
        * (electronegativity[elem] - avg_electronegativity) ** 2
        for elem in concentrations.keys()
    )

    return sqrt(diff_sum)


def process_compound_file(input_file: str, output_file: str, electronegativity: Dict[str, float]) -> None:
    """Process a compound file and write the results with electronegativity differences."""
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + [
            "electronegativity_difference",
            "atomic_concentrations",
        ]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                concentrations = calculate_atomic_concentrations(row["formula"])
                en_diff = calculate_electronegativity_difference(
                    row["formula"], electronegativity
                )
                row["electronegativity_difference"] = f"{en_diff:.4f}"
                row["atomic_concentrations"] = "; ".join(
                    f"{elem}: {conc:.4f}"
                    for elem, conc in concentrations.items()
                )
                writer.writerow(row)
            except KeyError as e:
                print(
                    f"Warning: Could not calculate for {row['formula']}. Missing electronegativity value for {e}"
                )

    print(f"Processing complete. Results written to {output_file}")


def main() -> None:
    # Load electronegativity data
    electronegativity = load_electronegativity_data("magpiery.csv")

    # Process Binary Metallic and Non-Metallic compound files
    compound_types = [
        ("binary_metallic_compounds_filtered.csv", "binary_metallic_compounds_with_electronegativity.csv"),
        ("binary_non_metallic_compounds_filtered.csv", "binary_non_metallic_compounds_with_electronegativity.csv")
    ]

    for input_file, output_file in compound_types:
        process_compound_file(input_file, output_file, electronegativity)

    print("All compound types have been processed.")


if __name__ == "__main__":
    main()
