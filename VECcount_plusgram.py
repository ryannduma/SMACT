import csv
import re
from collections import defaultdict
import matplotlib.pyplot as plt

def get_element_valence(element, valence_data):
    for row in valence_data:
        if row['element'] == element:
            return int(row['NValence'])
    return None

def parse_formula(formula):
    pattern = re.compile(r'([A-Z][a-z]*)(\d*)')
    elements = pattern.findall(formula)
    element_stoich = defaultdict(int)
    for (element, count) in elements:
        count = int(count) if count else 1
        element_stoich[element] += count
    return element_stoich

def validate_output(output_file):
    with open(output_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            valence_info = row['valence_info']
            if not valence_info:
                print(f"Missing valence information for {row['material_id']}")
                return False
            else:
                valence_numbers = [info.split('(Valence: ')[1].split(')')[0] for info in valence_info.split(', ')]
                if not all(valence_numbers):
                    print(f"Missing valence number for one or more elements in {row['material_id']}")
                    return False
    return True

def calculate_vec(element_stoich, valence_data):
    total_valence = 0
    total_stoich = 0
    for element, stoich in element_stoich.items():
        valence = get_element_valence(element, valence_data)
        if valence is not None:
            total_valence += stoich * valence
            total_stoich += stoich
    if total_stoich == 0:
        return 0
    return total_valence / total_stoich

def process_binary_compounds(binary_file, valence_file, output_file):
    # Read valence data from CSV
    with open(valence_file, 'r') as file:
        reader = csv.DictReader(file)
        valence_data = list(reader)

    # Process binary compounds
    with open(binary_file, 'r') as file:
        reader = csv.DictReader(file)
        output_data = []
        vec_counts = []

        for row in reader:
            formula = row['formula']
            elements = row['elements'].split(', ')
            theoretical = row['theoretical']

            # Extract element stoichiometry using the improved parser
            element_stoich = parse_formula(formula)

            # Get valence numbers for each element and calculate VEC
            valence_info = []
            for element, stoich in element_stoich.items():
                valence = get_element_valence(element, valence_data)
                if valence is not None:
                    valence_info.append(f"{element}: {stoich} (Valence: {valence})")

            vec_count = calculate_vec(element_stoich, valence_data)
            vec_counts.append(vec_count)

            # Create output row
            output_row = {
                'material_id': row['material_id'],
                'formula': formula,
                'elements': row['elements'],
                'theoretical': theoretical,
                'valence_info': ', '.join(valence_info),
                'VEC_count': vec_count
            }
            output_data.append(output_row)

    # Write output data to CSV
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['material_id', 'formula', 'elements', 'theoretical', 'valence_info', 'VEC_count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

    # Plot histogram of VEC counts
    plt.figure(figsize=(10, 6))
    plt.hist(vec_counts, bins=30, edgecolor='black')
    plt.xlabel('VEC Count')
    plt.ylabel('Frequency')
    plt.title('Histogram of VEC Counts')
    plt.grid(True)
    plt.savefig('vec_histogram.png')
    plt.show()

# Process binary compounds
binary_file = 'binary_compounds.csv'
valence_file = 'element_valence_modifiedry.csv'
output_file = 'VECcount_plusgram.csv'

process_binary_compounds(binary_file, valence_file, output_file)

# Validate output line by line
if validate_output(output_file):
    print(f"Processed data has been saved to '{output_file}' and validated successfully.")
else:
    print("Validation failed. Please check the output file.")
