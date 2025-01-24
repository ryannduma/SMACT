#!/usr/bin/env python
"""
Example script demonstrating SMACT's mixed-valence functionality.

This script shows how to use SMACT to validate compounds that require
mixed-valence states for charge balancing, such as Fe3O4 (magnetite)
which contains both Fe2+ and Fe3+ ions.
"""

from smact.screening import smact_validity
from smact.mixed_valence import (
    enumerate_oxidation_state_combinations,
    get_element_oxidation_states,
    is_mixed_valence_valid,
)
from smact import Element


def print_section(title):
    """Helper to print formatted section titles."""
    print(f"\n{'-' * 20} {title} {'-' * 20}\n")


def main():
    # Example 1: Basic usage with smact_validity
    print_section("Basic Usage")

    # Test some common compounds
    test_compounds = [
        "Fe3O4",  # Magnetite (mixed Fe2+/Fe3+)
        "Fe2O3",  # Hematite (all Fe3+)
        "NaCl",  # Simple compound
        "Mn3O4",  # Mixed Mn2+/Mn3+
        "Cu2O",  # Cuprous oxide
        "CuO",  # Cupric oxide
        "Fe3O5",  # Invalid compound
    ]

    print("Testing compounds with default settings (no mixed valence):")
    for compound in test_compounds:
        valid = smact_validity(compound, allow_mixed_valence=False)
        print(f"{compound:8} -> {'Valid' if valid else 'Invalid'}")

    print("\nTesting compounds with mixed valence enabled:")
    for compound in test_compounds:
        valid = smact_validity(compound, allow_mixed_valence=True)
        print(f"{compound:8} -> {'Valid' if valid else 'Invalid'}")

    # Example 2: Detailed analysis of Fe3O4
    print_section("Detailed Analysis of Fe3O4")

    # Get oxidation states for Fe
    fe = Element("Fe")
    fe_states = get_element_oxidation_states(fe, "icsd24")
    print(f"Possible Fe oxidation states (ICSD24): {fe_states}")

    # Manual enumeration of oxidation states for Fe3O4
    elem_symbols = ["Fe", "Fe", "Fe", "O", "O", "O", "O"]
    counts = [3, 4]  # 3 Fe, 4 O
    oxidation_states = [fe_states, [-2]]  # Fe states and O2-

    print("\nEnumerating possible oxidation state combinations for Fe3O4...")
    assignments = enumerate_oxidation_state_combinations(["Fe", "O"], counts, oxidation_states)

    print("\nValid oxidation state assignments:")
    for assignment in assignments:
        fe_states = assignment[:3]  # First 3 are Fe
        o_states = assignment[3:]  # Last 4 are O
        print(f"Fe: {fe_states}, O: {o_states}")
        print(f"Total charge: {sum(assignment)}")

    # Example 3: Detailed analysis of Mn3O4
    print_section("Detailed Analysis of Mn3O4")

    # Get oxidation states for Mn
    mn = Element("Mn")
    mn_states = get_element_oxidation_states(mn, "icsd24")
    print(f"Possible Mn oxidation states (ICSD24): {mn_states}")

    # Manual enumeration of oxidation states for Mn3O4
    counts = [3, 4]  # 3 Mn, 4 O
    oxidation_states = [mn_states, [-2]]  # Mn states and O2-

    print("\nEnumerating possible oxidation state combinations for Mn3O4...")
    assignments = enumerate_oxidation_state_combinations(["Mn", "O"], counts, oxidation_states)

    print("\nValid oxidation state assignments:")
    for assignment in assignments:
        mn_states = assignment[:3]  # First 3 are Mn
        o_states = assignment[3:]  # Last 4 are O
        print(f"Mn: {mn_states}, O: {o_states}")
        print(f"Total charge: {sum(assignment)}")

    # Example 4: Testing with different oxidation state sets
    print_section("Testing with Different Oxidation State Sets")

    compound = "Fe3O4"
    oxidation_sets = ["smact14", "icsd16", "icsd24", "pymatgen_sp", "wiki"]

    for ox_set in oxidation_sets:
        valid = smact_validity(compound, allow_mixed_valence=True, oxidation_states_set=ox_set)
        print(f"{ox_set:12} -> {'Valid' if valid else 'Invalid'}")

    # Example 5: Handling large compositions
    print_section("Handling Large Compositions")

    # This will trigger the max_combinations warning
    large_compound = "Fe10O15"
    print(f"Testing {large_compound} with small max_combinations...")

    valid = smact_validity(
        large_compound,
        allow_mixed_valence=True,
        max_combinations=10,  # Very small limit to demonstrate warning
    )
    print(f"Valid: {valid} (False due to combination limit)")

    # Test with more reasonable limit
    valid = smact_validity(large_compound, allow_mixed_valence=True, max_combinations=10000)
    print(f"Valid with larger combination limit: {valid}")


if __name__ == "__main__":
    main()
