"""Tests for mixed valence functionality."""

from __future__ import annotations

import unittest
import warnings

import pytest

from smact.mixed_valence import (
    enumerate_oxidation_state_combinations,
    get_element_oxidation_states,
    is_mixed_valence_valid,
)
from smact.screening import smact_validity


class TestMixedValence(unittest.TestCase):
    """Test the mixed valence functionality."""

    def test_enumerate_oxidation_state_combinations(self):
        """Test enumeration of oxidation state combinations."""
        # Simple case: Fe2O3
        elem_symbols = ["Fe", "O"]
        counts = [2, 3]
        oxidation_states = [[2, 3], [-2]]  # Fe can be +2/+3, O is -2

        assignments = enumerate_oxidation_state_combinations(elem_symbols, counts, oxidation_states)

        # Should find Fe3+ Fe3+ O2- O2- O2- as a valid combination
        self.assertTrue(any(sum(a) == 0 and a.count(3) == 2 and a.count(-2) == 3 for a in assignments))

    def test_get_element_oxidation_states(self):
        """Test getting oxidation states for elements."""
        from smact import Element

        # Test Fe with different sets
        fe = Element("Fe")

        states = get_element_oxidation_states(fe, "icsd24")
        self.assertIn(2, states)  # Fe2+ should be in ICSD set
        self.assertIn(3, states)  # Fe3+ should be in ICSD set

        # Test invalid set
        with pytest.raises(ValueError):
            get_element_oxidation_states(fe, "invalid_set")

    def test_is_mixed_valence_valid(self):
        """Test mixed valence validity checking."""
        # Fe3O4 should be valid (mixed Fe2+/Fe3+)
        self.assertTrue(is_mixed_valence_valid("Fe3O4"))

        # Fe2O3 should be valid (all Fe3+)
        self.assertTrue(is_mixed_valence_valid("Fe2O3"))

        # NaCl should be valid (simple case)
        self.assertTrue(is_mixed_valence_valid("NaCl"))

        # Invalid composition should be invalid
        self.assertFalse(is_mixed_valence_valid("Fe3O5"))

    def test_smact_validity_mixed_valence(self):
        """Test the mixed valence option in smact_validity."""
        # Fe3O4 should be invalid with default settings
        self.assertFalse(smact_validity("Fe3O4", allow_mixed_valence=False))

        # Fe3O4 should be valid with mixed valence
        self.assertTrue(smact_validity("Fe3O4", allow_mixed_valence=True))

        # Test max_combinations limit
        with warnings.catch_warnings(record=True) as w:
            # Should warn about too many combinations
            result = smact_validity("Fe10O15", allow_mixed_valence=True, max_combinations=10)
            self.assertFalse(result)
            self.assertTrue(any("exceeds max_combinations" in str(warning.message) for warning in w))


if __name__ == "__main__":
    unittest.main()
