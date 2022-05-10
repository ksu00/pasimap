import pytest

import src.modules.pairwise as pairwise


class TestIsPairwise:

    def test_true_one(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_true_two(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '',
            '1 2 0.8123',
            '2 1 0.8123',
            '  1    3  0.5123    ',
            '  1    4  -0.5123   ',
            '  2    4  0         '])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_false_empty(self):
        # Input parameter.
        s = '\n'.join([
            ''])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Incorrect number of ssv-elements.
    def test_false_one(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 3'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Incorrect type of object_a_number.
    def test_false_two(self):
        # Input parameter.
        s = '\n'.join([
            '1. 2 0.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Incorrect type of object_b_number.
    def test_false_three(self):
        # Input parameter.
        s = '\n'.join([
            '1 2. 0.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Incorrect type of pairwise_relation.
    def test_false_four(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 asdf',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Diagonal element.
    def test_false_five(self):
        # Input parameter.
        s = '\n'.join([
            '1 1 0.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Pairwise relation is NOT in value range [-1; 1].
    def test_false_six(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 1.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Pairwise relation is NOT in value range [-1; 1].
    def test_false_seven(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 -1.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Redundant pair with NON-identical pairwise relation value.
    def test_false_eight(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 2 0.8100',
            '1 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Numbering is NOT continuous from 1 to n
    # (n: number of objects).
    def test_false_nine(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 4 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    # Numbering is NOT continuous from 1 to n
    # (n: number of objects).
    def test_false_ten(self):
        # Input parameter.
        s = '\n'.join([
            '0 2 0.8123',
            '0 3 0.5123'])
        # Observed output.
        obs_bool = pairwise.is_pairwise(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool


class TestCountObjects:

    def test_one(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123'])
        # Observed output.
        obs_count = pairwise.count_objects(s)
        # Expected output.
        exp_count = 2
        # Test.
        assert obs_count == exp_count

    def test_two(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 3 0.5123'])
        # Observed output.
        obs_count = pairwise.count_objects(s)
        # Expected output.
        exp_count = 3
        # Test.
        assert obs_count == exp_count

    def test_three(self):
        # Input parameter.
        s = '\n'.join([
            '1 2 0.8123',
            '1 3 0.5123',
            '2 4 -0.5123'])
        # Observed output.
        obs_count = pairwise.count_objects(s)
        # Expected output.
        exp_count = 4
        # Test.
        assert obs_count == exp_count
