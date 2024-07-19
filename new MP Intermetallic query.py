from mp_api.client import MPRester
import csv
import time

def get_all_compounds(api_key):
    compounds_info = []
    with MPRester(api_key) as mpr:
        # We'll use a loop to handle pagination
        offset = 0
        limit = 1000  # Maximum allowed by the API
        while True:
            print(f"Fetching compounds {offset} to {offset + limit}...")
            docs = mpr.materials.summary.search(
                fields=[
                    "material_id", 'formula_pretty', 'elements', 'energy_above_hull', 
                    'symmetry', 'band_gap', 'theoretical', 'nelements'
                ]
            )
            
            if not docs:
                break  # No more results
            
            for doc in docs:
                compounds_info.append({
                    "material_id": doc.material_id,
                    "formula": doc.formula_pretty,
                    "elements": ", ".join(elem.symbol for elem in doc.elements),
                    "num_elements": doc.nelements,
                    "energy_above_hull": doc.energy_above_hull,
                    "crystal_system": doc.symmetry.crystal_system,
                    "band_gap": doc.band_gap,
                    "theoretical": doc.theoretical
                })
            
            offset += limit
            time.sleep(1)  # To avoid overwhelming the API
    
    return compounds_info

def save_to_csv(compounds, filename):
    if not compounds:
        print(f"No compounds to save for {filename}.")
        return

    keys = compounds[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(compounds)

def main():
    api_key = 'w1FbQcBbkQZJHyhMJGxssIEttJ8JSGu8'  # Replace with your actual API key

    all_compounds = get_all_compounds(api_key)

    save_to_csv(all_compounds, 'all_compounds.csv')

    print(f"Total compounds saved: {len(all_compounds)}")
    print("Results have been saved to 'all_compounds.csv'")

if __name__ == "__main__":
    main()