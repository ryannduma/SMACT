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

def calculate_atomic_concentrations(formula):
    """Calculate atomic concentrations from the chemical formula."""
    parsed_formula = parse_formula(formula)
    total_atoms = sum(parsed_formula.values())
    return {elem: count / total_atoms for elem, count in parsed_formula.items()}

def calculate_electronegativity_difference(formula, electronegativity):
    """Calculate the electronegativity difference."""
    concentrations = calculate_atomic_concentrations(formula)
    
    # Calculate average electronegativity
    avg_electronegativity = sum(electronegativity[elem] * conc for elem, conc in concentrations.items())
    
    # Calculate electronegativity difference
    diff_sum = sum(
        concentrations[elem] * (electronegativity[elem] - avg_electronegativity) ** 2
        for elem in concentrations.keys()
    )
    
    return sqrt(diff_sum)

def process_compound_file(input_file, output_file, electronegativity):
    """Process a compound file and write the results with electronegativity differences."""
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['electronegativity_difference', 'atomic_concentrations']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                concentrations = calculate_atomic_concentrations(row['formula'])
                en_diff = calculate_electronegativity_difference(row['formula'], electronegativity)
                row['electronegativity_difference'] = en_diff
                row['atomic_concentrations'] = '; '.join(f"{elem}: {conc:.4f}" for elem, conc in concentrations.items())
                writer.writerow(row)
            except KeyError as e:
                print(f"Warning: Could not calculate for {row['formula']}. Missing electronegativity value for {e}")

    print(f"Processing complete. Results written to {output_file}")

# Load electronegativity data
electronegativity = load_electronegativity_data('magpiery.csv')

# Process Binary, Ternary, and Quaternary compound files
compound_types = ['binary', 'ternary', 'quaternary']

for compound_type in compound_types:
    input_file = f'{compound_type}_compounds.csv'
    output_file = f'{compound_type}_compounds_with_electronegativity.csv'
    process_compound_file(input_file, output_file, electronegativity)

print("All compound types have been processed.")