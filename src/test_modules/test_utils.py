import pytest

import src.modules.utils as utils


class TestIsAscii:

    def test_true(self):
        # Input parameter.
        s = 'asdf'
        # Observed output.
        obs_bool = utils.is_ascii(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_false(self):
        # Input parameter.
        s = 'äsdf'
        # Observed output.
        obs_bool = utils.is_ascii(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool
