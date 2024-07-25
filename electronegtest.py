import csv
import re
from math import sqrt

def load_electronegativity_data(filename):
    """Load electronegativity data from the magpiery.csv file."""
    electronegativity = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            element = row['element']
            en = float(row['Electronegativity'])
            electronegativity[element] = en
    return electronegativity

def parse_formula(formula):
    """Parse chemical formula and return a dictionary of elements and their counts."""
    pattern = re.compile(r'([A-Z][a-z]*)(\d*)')
    elements = pattern.findall(formula)
    return {elem: int(count) if count else 1 for elem, count in elements}

def calculate_electronegativity_difference(formula, electronegativity):
    """Calculate the electronegativity difference using the provided formula."""
    parsed_formula = parse_formula(formula)
    total_atoms = sum(parsed_formula.values())
    
    # Calculate average electronegativity
    avg_electronegativity = sum(electronegativity[elem] * count / total_atoms 
                                for elem, count in parsed_formula.items())
    
    # Calculate electronegativity difference
    diff_sum = sum(
        (count / total_atoms) * (electronegativity[elem] - avg_electronegativity) ** 2
        for elem, count in parsed_formula.items()
    )
    
    return sqrt(diff_sum)

# Load electronegativity data
electronegativity = load_electronegativity_data('magpiery.csv')

# Process the binary intermetallics CSV file
input_file = 'binary_compounds.csv'  # Replace with your actual file name
output_file = 'binary_intermetallics_with_electronegativity.csv'

with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['electronegativity_difference']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            en_diff = calculate_electronegativity_difference(row['formula'], electronegativity)
            row['electronegativity_difference'] = en_diff
            writer.writerow(row)
        except KeyError as e:
            print(f"Warning: Could not calculate electronegativity difference for {row['formula']}. Missing electronegativity value for {e}")

print(f"Processing complete. Results written to {output_file}")