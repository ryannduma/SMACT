"""Tools for handling mixed-valence (multivalent) charge balancing scenarios."""

from __future__ import annotations

import itertools
import warnings

from pymatgen.core import Composition

from smact import Element, element_dictionary
from smact.screening import pauling_test


def enumerate_oxidation_state_combinations(
    elem_symbols: list[str],
    counts: list[int],
    oxidation_states_by_element: list[list[int]],
    max_combinations: int = 5000,
) -> list[list[int]]:
    """
    Enumerate all possible oxidation state combinations for a composition where
    elements can have different oxidation states at different sites.

    Args:
        elem_symbols: List of element symbols in the composition
        counts: List of stoichiometric counts for each element
        oxidation_states_by_element: List of possible oxidation states for each element
        max_combinations: Maximum number of combinations to try before giving up

    Returns:
        List of valid oxidation state assignments that sum to charge neutrality
    """
    # For each element, we need to try all possible ways to assign oxidation states
    # to its stoichiometric count of atoms
    valid_assignments = []
    total_combinations = 1

    # Calculate total possible combinations to check against max_combinations
    for ox_states, count in zip(oxidation_states_by_element, counts, strict=False):
        total_combinations *= len(ox_states) ** count

    if total_combinations > max_combinations:
        warnings.warn(
            f"Number of possible combinations ({total_combinations}) exceeds max_combinations "
            f"({max_combinations}). Consider using a constraint solver for large systems."
        )
        return []

    # For each element, generate all possible assignments of oxidation states to its atoms
    element_assignments = []
    for ox_states, count in zip(oxidation_states_by_element, counts, strict=False):
        # Get all possible ways to assign oxidation states to this element's atoms
        element_ox_combinations = list(itertools.product(ox_states, repeat=count))
        element_assignments.append(element_ox_combinations)

    # Try all combinations of assignments across elements
    for ox_assignment in itertools.product(*element_assignments):
        # Flatten the assignment into a single list of oxidation states
        flat_assignment = [ox for elem_ox in ox_assignment for ox in elem_ox]

        # Check if this assignment is charge neutral
        if sum(flat_assignment) == 0:
            valid_assignments.append(flat_assignment)

    return valid_assignments


def get_element_oxidation_states(element: Element, oxidation_states_set: str = "icsd24") -> list[int]:
    """Get the oxidation states for an element from the specified set.

    Args:
        element: SMACT Element object
        oxidation_states_set: Which oxidation states set to use

    Returns:
        List of possible oxidation states for the element
    """
    if oxidation_states_set == "smact14":
        return element.oxidation_states_smact14
    elif oxidation_states_set == "icsd16":
        return element.oxidation_states_icsd16
    elif oxidation_states_set == "icsd24":
        return element.oxidation_states_icsd24
    elif oxidation_states_set == "pymatgen_sp":
        return element.oxidation_states_sp
    elif oxidation_states_set == "wiki":
        warnings.warn(
            "Using wiki-based oxidation states which may be questionable for serious use.",
            stacklevel=2,
        )
        return element.oxidation_states_wiki
    else:
        raise ValueError(
            f"{oxidation_states_set} is not valid. Enter either 'smact14', 'icsd16', "
            "'icsd24', 'pymatgen_sp', 'wiki' or a filepath to a textfile of oxidation states."
        )


def is_mixed_valence_valid(
    composition: str | Composition,
    use_pauling_test: bool = True,
    oxidation_states_set: str = "icsd24",
    max_combinations: int = 5000,
) -> bool:
    """Check if a composition is valid considering mixed-valence possibilities.

    Args:
        composition: Chemical composition as string or pymatgen Composition
        use_pauling_test: Whether to apply the Pauling electronegativity test
        oxidation_states_set: Which oxidation states set to use
        max_combinations: Maximum number of combinations to try

    Returns:
        True if a valid mixed-valence assignment exists, False otherwise
    """
    if isinstance(composition, str):
        composition = Composition(composition)

    # Get composition info
    elem_symbols = list(composition.as_dict().keys())
    counts = [int(v) for v in composition.as_dict().values()]

    # Get SMACT elements
    space = element_dictionary(elem_symbols)
    smact_elems = [e[1] for e in space.items()]

    # Get oxidation states and electronegativities
    oxidation_states_by_element = [get_element_oxidation_states(elem, oxidation_states_set) for elem in smact_elems]
    electronegs = [e.pauling_eneg for e in smact_elems]

    # Try to find valid oxidation state assignments
    valid_assignments = enumerate_oxidation_state_combinations(
        elem_symbols, counts, oxidation_states_by_element, max_combinations
    )

    if not valid_assignments:
        return False

    if use_pauling_test:
        return any(pauling_test(assignment, electronegs) for assignment in valid_assignments)

    return True
