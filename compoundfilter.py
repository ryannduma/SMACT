import csv
from typing import Dict, List


def load_compounds(filename: str) -> List[Dict[str, str]]:
    """Load compound data from a CSV file."""
    with open(filename, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)


def filter_compounds(compounds: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Filter compounds based on is_metal and theoretical flags."""
    return [
        compound for compound in compounds
        if compound['is_metal'].lower() == 'false' and compound['theoretical'].lower() == 'false'
    ]


def save_filtered_compounds(compounds: List[Dict[str, str]], filename: str) -> None:
    """Save filtered compounds to a new CSV file."""
    if not compounds:
        print("No compounds match the criteria.")
        return

    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=compounds[0].keys())
        writer.writeheader()
        writer.writerows(compounds)


def main():
    input_file = "binary_non_metallic_compounds.csv"
    output_file = "binary_non_metallic_compounds_filtered.csv"

    compounds = load_compounds(input_file)
    filtered_compounds = filter_compounds(compounds)
    save_filtered_compounds(filtered_compounds, output_file)

    print(f"Filtered compounds saved to {output_file}")


if __name__ == "__main__":
    main()
