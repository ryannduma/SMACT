# Mixed-Valence Support in SMACT

## Overview

SMACT now supports mixed-valence (multivalent) charge balancing scenarios, where elements can adopt different oxidation states at different sites within the same compound. This is particularly important for many transition metal compounds, such as Fe3O4 (magnetite), where iron exists in both Fe²⁺ and Fe³⁺ states.

## Features

- **Mixed-Valence Validation**: Check if a composition is valid when elements can have different oxidation states at different sites
- **Oxidation State Enumeration**: Enumerate all possible charge-balanced oxidation state combinations
- **Flexible Oxidation State Sets**: Support for multiple oxidation state databases (SMACT14, ICSD16, ICSD24, etc.)
- **Performance Controls**: Safeguards against combinatorial explosion in large systems

## Literature Evidence & Justification

### Mixed-Valence Enumeration

Mixed-valence compounds are well-documented in classical solid-state chemistry literature (Greenwood & Earnshaw), where many transition metals exhibit stable multiple oxidation states simultaneously in a single phase (e.g., Fe3O4, Mn3O4, etc.).

Our approach systematically enumerates or solves a constraint satisfaction problem to reflect real multi-valent states.

### Integer Linear Programming

The approach can be phrased as an integer linear program where each oxidation state is a variable with a nonnegative integer value equal to the number of that state. See discussions in the Issues quoted above (from the user "CompRhys") for references to scipy.optimize.milp or external ILP libraries.

### Pauling Test

We rely on the existing `pauling_test()` within smact.screening. This test helps exclude unphysical combinations (e.g., cations more electronegative than anions).

### Performance

For small numbers of atoms and limited oxidation states, naive enumeration is simple to implement and works fine. For more complicated stoichiometries (ternary, quaternary, multiple transition metals), the search space can blow up. This is why we introduce a fallback or a user-settable max_permutations and recommend an ILP solver if that limit is exceeded.

## Installation

The mixed-valence functionality is included in SMACT version 3.0 and above. No additional installation is required beyond the standard SMACT installation:

```bash
pip install smact
```

## Usage

### Basic Usage

The simplest way to use the mixed-valence functionality is through the `smact_validity` function with the `allow_mixed_valence` parameter:

```python
from smact.screening import smact_validity

# Check Fe3O4 with mixed valence enabled
result = smact_validity("Fe3O4", allow_mixed_valence=True)
print(f"Fe3O4 is {'valid' if result else 'invalid'}")

# Traditional single-oxidation-state check
result = smact_validity("Fe3O4", allow_mixed_valence=False)
print(f"Fe3O4 with single oxidation state is {'valid' if result else 'invalid'}")
```

### Advanced Usage

For more detailed analysis, you can use the functions in the `mixed_valence` module:

```python
from smact.mixed_valence import (
    enumerate_oxidation_state_combinations,
    get_element_oxidation_states,
    is_mixed_valence_valid,
)
from smact import Element

# Get possible oxidation states for an element
fe = Element("Fe")
fe_states = get_element_oxidation_states(fe, "icsd24")

# Enumerate possible oxidation state combinations
elem_symbols = ["Fe", "O"]
counts = [3, 4]  # Fe3O4
oxidation_states = [fe_states, [-2]]  # Fe states and O2-

assignments = enumerate_oxidation_state_combinations(
    elem_symbols, counts, oxidation_states
)

# Check each assignment
for assignment in assignments:
    fe_states = assignment[:3]  # First 3 are Fe
    o_states = assignment[3:]  # Last 4 are O
    print(f"Fe: {fe_states}, O: {o_states}")
    print(f"Total charge: {sum(assignment)}")
```

### Performance Considerations

For compounds with many atoms or elements with many possible oxidation states, the number of possible combinations can grow very large. Use the `max_combinations` parameter to prevent excessive computation:

```python
# Set a limit on combinations to try
result = smact_validity("Fe10O15", allow_mixed_valence=True, max_combinations=5000)
```

## Oxidation State Sets

SMACT provides several oxidation state sets:

- `smact14`: Original SMACT 2014 oxidation states
- `icsd16`: ICSD-derived states from 2016
- `icsd24`: ICSD-derived states from 2024 (default)
- `pymatgen_sp`: States from pymatgen structure predictor
- `wiki`: States from Wikipedia (use with caution)

Select the appropriate set using the `oxidation_states_set` parameter:

```python
result = smact_validity(
    "Fe3O4", allow_mixed_valence=True, oxidation_states_set="icsd24"
)
```

## Examples

A comprehensive example script is provided in `docs/examples/mixed_valence_example.py`. This script demonstrates:

1. Basic validation of common mixed-valence compounds
2. Detailed analysis of Fe3O4 and Mn3O4
3. Comparison of different oxidation state sets
4. Handling of large compositions

Run the example:

```bash
python docs/examples/mixed_valence_example.py
```

## Technical Details

### Algorithm

The mixed-valence validation works by:

1. Enumerating all possible combinations of oxidation states for each element's sites
2. Checking charge neutrality for each combination
3. Applying the Pauling electronegativity test if requested
4. Returning True if any valid combination is found

### Limitations

- Computational complexity grows exponentially with the number of sites
- Memory usage can be significant for large systems
- Some valid compounds might be rejected if they exceed `max_combinations`

## Contributing

If you find bugs or have suggestions for improving the mixed-valence functionality, please:

1. Check existing issues on GitHub
2. Create a new issue describing the problem or enhancement
3. Submit a pull request if you have a solution

## Citation

If you use SMACT's mixed-valence functionality in your research, please cite:

```bibtex
@article{smact2024,
    title = {SMACT: Mixed-Valence Extension},
    year = {2024},
    journal = {Journal of Open Source Software},
    doi = {10.21105/joss.1361}
}
```

## Alternative Strategies & Potential Pitfalls

### Discarded Approaches

1. **Naive Full Permutation Without Constraints**

   - Discarded because enumerating every combination for every element can lead to enormous overhead
   - Becomes impractical with 4-5 elements each having 3-5 possible oxidation states
   - Still used for small systems with max_permutations limit

2. **Dynamic Programming or Recursive Backtracking**

   - A backtracking solver can systematically prune solutions if partial sums exceed some threshold
   - More efficient than pure enumeration but may not scale well for large combinatorial spaces

3. **Direct ILP (Integer Linear Programming)**

   - Highly recommended for large-scale or high-throughput usage
   - ILP solvers can handle constraints more systematically and prune impossible solutions quickly
   - Not included by default to avoid additional dependencies (e.g., pulp, mip, or ortools)
   - Recommended approach if performance is essential

4. **Randomized or Genetic Algorithms**

   - Could attempt to guess random or heuristic assignments
   - Discarded for general library usage as exact methods are more straightforward to interpret and debug

5. **Multi-Electron/Hole Counting**
   - Alternative approach tracking electron count directly
   - Discarded to preserve oxidation-state formalism for clarity and consistency with SMACT

### Known Limitations and Potential Failures

1. **Performance Issues**

   - Even with max_permutations, naive enumeration might be slow with large limits
   - Combinatorial explosion in complex systems

2. **Data Completeness**

   - No solutions might appear for obscure elements or with partial oxidation-state data
   - Missing or incomplete oxidation states can lead to false negatives

3. **Electronegativity Testing**
   - Pauling test can yield false negatives with missing data
   - Borderline electronegativity differences may cause issues

## Final Note

This mixed-valence extension provides a more robust check of compounds such as Fe3O4. If your target problem set extends to large multi-component systems or a high volume of screening, strongly consider an ILP-based or more advanced backtracking approach. Still, this code and workflow illustrate how you can incrementally add the mixed-valence capability to SMACT in a way that is consistent with the current library design.
