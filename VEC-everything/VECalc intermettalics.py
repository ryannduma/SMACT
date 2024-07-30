import csv
from collections import defaultdict

def get_element_valence(element, valence_data):
    for row in valence_data:
        if row['element'] == element:
            return int(row['NValence'])
    return None

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

def process_binary_compounds(binary_file, valence_file, output_file):
    # Read valence data from CSV
    with open(valence_file, 'r') as file:
        reader = csv.DictReader(file)
        valence_data = list(reader)

    # Process binary compounds
    with open(binary_file, 'r') as file:
        reader = csv.DictReader(file)
        output_data = []

        for row in reader:
            formula = row['formula']
            elements = row['elements'].split(', ')
            theoretical = row['theoretical']

            # Extract element stoichiometry
            element_stoich = defaultdict(int)
            element = ''
            for char in formula:
                if char.isalpha():
                    if element:
                        element_stoich[element] += 1
                    element = char
                elif char.isdigit():
                    element_stoich[element] = int(char)

            # Get valence numbers for each element
            valence_info = []
            for element, stoich in element_stoich.items():
                valence = get_element_valence(element, valence_data)
                if valence is not None:
                    valence_info.append(f"{element}: {stoich} (Valence: {valence})")

            # Create output row
            output_row = {
                'material_id': row['material_id'],
                'formula': formula,
                'elements': row['elements'],
                'theoretical': theoretical,
                'valence_info': ', '.join(valence_info)
            }
            output_data.append(output_row)

    # Write output data to CSV
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['material_id', 'formula', 'elements', 'theoretical', 'valence_info']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_data)

# Process binary compounds
binary_file = 'binary_compounds.csv'
valence_file = 'element_valence_modifiedry.csv'
output_file = 'binary_compounds_valence.csv'

process_binary_compounds(binary_file, valence_file, output_file)

# Validate output line by line
if validate_output(output_file):
    print(f"Processed data has been saved to '{output_file}' and validated successfully.")
else:
    print("Validation failed. Please check the output file.")
