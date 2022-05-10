import pytest

import src.modules.ali as ali


class TestIsValidAli:

    def test_true_one(self):
        # Input parameter.
        a = ('AAA',
             'CCC')
        # Observed output.
        obs_bool = ali.is_valid_ali(a)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_true_two(self):
        # Input parameter.
        a = ('-AA',
             'CC-')
        # Observed output.
        obs_bool = ali.is_valid_ali(a)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_true_three(self):
        # Input parameter.
        a = ('A-A',
             'C-C')
        # Observed output.
        obs_bool = ali.is_valid_ali(a)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_false_one(self):
        # Input parameter.
        a = ('AAA',
             'CC')
        # Observed output.
        obs_bool = ali.is_valid_ali(a)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_false_two(self):
        # Input parameter.
        a = ('AA',
             'CCC')
        # Observed output.
        obs_bool = ali.is_valid_ali(a)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool


class TestAliToDenseAli:

    def test_one(self):
        # Input parameter.
        a = ('A--',
             'D-F')
        # Observed output.
        obs = ali.ali_to_dense_ali(a)
        # Expected output.
        exp = ('A-',
               'DF')
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        a = ('A-C',
             'DE-')
        # Observed output.
        obs = ali.ali_to_dense_ali(a)
        # Expected output.
        exp = ('A-C',
               'DE-')
        # Test.
        assert obs == exp


class TestAliToIndelfreeAli:

    def test_one(self):
        # Input parameter.
        a = ('A-C',
             'DE-')
        # Observed output.
        obs = ali.ali_to_indelfree_ali(a)
        # Expected output.
        exp = ('A',
               'D')
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        a = ('A-C',
             'D-E')
        # Observed output.
        obs = ali.ali_to_indelfree_ali(a)
        # Expected output.
        exp = ('AC',
               'DE')
        # Test.
        assert obs == exp


class TestGetAliLength:

    def test_empty(self):
        # Input parameter.
        a = ('',
             '')
        # Observed output.
        obs = ali.get_ali_length(a)
        # Expected output.
        exp = 0
        # Test.
        assert obs == exp

    def test_one(self):
        # Input parameter.
        a = ('AA',
             'CC')
        # Observed output.
        obs = ali.get_ali_length(a)
        # Expected output.
        exp = 2
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        a = ('AAA',
             'CCC')
        # Observed output.
        obs = ali.get_ali_length(a)
        # Expected output.
        exp = 3
        # Test.
        assert obs == exp
