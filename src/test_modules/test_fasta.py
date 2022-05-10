import io

import pytest

import src.modules.fasta as fasta


class TestIsFasta:

    def test_true_one(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_true_two(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_true_three(self):
        # Input parameter.
        s = '\n'.join([
            '',
            '>seq_a',
            '',
            'ASDF',
            '',
            '>seq_b',
            '',
            'TS',
            '',
            'DF',
            ''])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_false_empty(self):
        # Input parameter.
        s = ''
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_false_one(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_false_two(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            '>seq_b'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_false_three(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF',
            '>seq_b'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_false_four(self):
        # Input parameter.
        s = '\n'.join([
            'ASDF'])
        # Observed output.
        obs_bool = fasta.is_fasta(s)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_header_true(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF'])
        # Observed output.
        obs_bool = fasta.is_fasta(s, check_header=True)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_header_false(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_ä',
            'ASDF'])
        # Observed output.
        obs_bool = fasta.is_fasta(s, check_header=True)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool

    def test_body_true(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF-asdf*'])
        # Observed output.
        obs_bool = fasta.is_fasta(s, check_body=True)
        # Expected output.
        exp_bool = True
        # Test.
        assert obs_bool == exp_bool

    def test_body_false(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF-asdf*J'])
        # Observed output.
        obs_bool = fasta.is_fasta(s, check_body=True)
        # Expected output.
        exp_bool = False
        # Test.
        assert obs_bool == exp_bool


class TestCountFasta:

    def test_empty(self):
        # Input parameter.
        s = '\n'.join([])
        # Observed output.
        obs_count = fasta.count_fasta(s)
        # Expected output.
        exp_count = 0
        # Test.
        assert obs_count == exp_count

    def test_one(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF'])
        # Observed output.
        obs_count = fasta.count_fasta(s)
        # Expected output.
        exp_count = 1
        # Test.
        assert obs_count == exp_count

    def test_two(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        # Observed output.
        obs_count = fasta.count_fasta(s)
        # Expected output.
        exp_count = 2
        # Test.
        assert obs_count == exp_count

    def test_two_difficult(self):
        # Input parameter.
        s = '\n'.join([
            '>>seq>_a>',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        # Observed output.
        obs_count = fasta.count_fasta(s)
        # Expected output.
        exp_count = 2
        # Test.
        assert obs_count == exp_count


class TestIterateFasta:

    def test_one(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile))
        # Expected output.
        exp = [('>seq_a', 'ASDF')]
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile))
        # Expected output.
        exp = [('>seq_a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp

    def test_two_difficult(self):
        # Input parameter.
        s = '\n'.join([
            '',
            '>seq_a',
            '',
            'ASDF',
            '>seq_b',
            'TS',
            '',
            'DF',
            ''])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile))
        # Expected output.
        exp = [('>seq_a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp

    def test_replace_one(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_|:a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile,
                                       header_forbidden_char_s=':|+'))
        # Expected output.
        exp = [('>seq___a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp

    def test_replace_two(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_|:a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile,
                                       header_forbidden_char_s=':|+',
                                       header_replacement_char='@'))
        # Expected output.
        exp = [('>seq_@@a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp

    def test_replace_three(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_|:a',
            'ASDF',
            '>seq_b',
            'TS',
            'DF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile,
                                       header_forbidden_char_s=':|+',
                                       header_replacement_char=''))
        # Expected output.
        exp = [('>seq_a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp

    def test_upper_false(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'AsdF',
            '>seq_b',
            'tS',
            'dF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile,
                                       body_upper=False))
        # Expected output.
        exp = [('>seq_a', 'AsdF'), ('>seq_b', 'tSdF')]
        # Test.
        assert obs == exp

    def test_upper_true(self):
        # Input parameter.
        s = '\n'.join([
            '>seq_a',
            'AsdF',
            '>seq_b',
            'tS',
            'dF'])
        opened_infile = io.StringIO(s)
        # Observed output.
        obs = list(fasta.iterate_fasta(opened_infile,
                                       body_upper=True))
        # Expected output.
        exp = [('>seq_a', 'ASDF'), ('>seq_b', 'TSDF')]
        # Test.
        assert obs == exp
