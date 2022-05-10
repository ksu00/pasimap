import io

import pytest

import src.modules.gali as gali
import src.modules.substmat as substmat


# Substitution matrix.
s = '\n'.join([
            '#  Matrix made by matblas from blosum62.iij',
            '#  * column uses minimum score',
            '#  BLOSUM Clustered Scoring Matrix in 1/2 Bit Units',
            '#  Blocks Database = /data/blocks_5.0/blocks.dat',
            '#  Cluster Percentage: >= 62',
            '#  Entropy =   0.6979, Expected =  -0.5209',
            '   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V  B  Z  X  *',
            'A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0 -2 -1  0 -4 ',
            'R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3 -1  0 -1 -4 ',
            'N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3  3  0 -1 -4 ',
            'D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3  4  1 -1 -4 ',
            'C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1 -3 -3 -2 -4 ',
            'Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2  0  3 -1 -4 ',
            'E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4 ',
            'G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3 -1 -2 -1 -4 ',
            'H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3  0  0 -1 -4 ',
            'I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3 -3 -3 -1 -4 ',
            'L -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1 -4 -3 -1 -4 ',
            'K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2  0  1 -1 -4 ',
            'M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1 -3 -1 -1 -4 ',
            'F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1 -3 -3 -1 -4 ',
            'P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2 -2 -1 -2 -4 ',
            'S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2  0  0  0 -4 ',
            'T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0 -1 -1  0 -4 ',
            'W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3 -4 -3 -2 -4 ',
            'Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1 -3 -2 -1 -4 ',
            'V  0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4 -3 -2 -1 -4 ',
            'B -2 -1  3  4 -3  0  1 -1  0 -3 -4  0 -3 -3 -2  0 -1 -4 -3 -3  4  1 -1 -4 ',
            'Z -1  0  0  1 -3  3  4 -2  0 -3 -3  1 -1 -3 -1  0 -1 -3 -2 -2  1  4 -1 -4 ',
            'X  0 -1 -1 -1 -2 -1 -1 -1 -1 -1 -1 -1 -1 -1 -2  0  0 -2 -1 -1 -1 -1 -1 -4 ',
            '* -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4 -4  1 '])
opened_infile = io.StringIO(s)
smat = substmat.parse_substmat_as_df(opened_infile)


class TestGaliToScore:

    def test_one(self):
        # Input parameter.
        ga = ('-',
              '-')
        # Observed output.
        obs = gali.gali_to_score(ga,
                                 smat,
                                 gapopen_penalty=10.0, gapextend_penalty=0.5)
        # Expected output.
        exp = 0.0
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        ga = ('ARN',
              'ARN')
        # Observed output.
        obs = gali.gali_to_score(ga,
                                 smat,
                                 gapopen_penalty=10.0, gapextend_penalty=0.5)
        # Expected output.
        exp = 15.0
        # Test.
        assert obs == exp

    def test_three(self):
        # Input parameter.
        ga = ('ARNDC',
              'ARNDC')
        # Observed output.
        obs = gali.gali_to_score(ga,
                                 smat,
                                 gapopen_penalty=10.0, gapextend_penalty=0.5)
        # Expected output.
        exp = 30.0
        # Test.
        assert obs == exp

    def test_four(self):
        # Input parameter.
        ga = ('---DC',
              'AR---')
        # Observed output.
        obs = gali.gali_to_score(ga,
                                 smat,
                                 gapopen_penalty=10.0, gapextend_penalty=0.5)
        # Expected output.
        exp = -21.0
        # Test.
        assert obs == exp

    def test_five(self):
        # Input parameter.
        ga = ('--NDC',
              'ARN--')
        # Observed output.
        obs = gali.gali_to_score(ga,
                                 smat,
                                 gapopen_penalty=10.0, gapextend_penalty=0.5)
        # Expected output.
        exp = -15.0
        # Test.
        assert obs == exp


class TestIndelfreeGaliToMaxScore:

    def test_one(self):
        # Input parameter.
        ga = ('ARN',
              'ARN')
        # Observed output.
        obs = gali.indelfree_gali_to_max_score(ga,
                                               smat)
        # Expected output.
        exp = 15.0
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        ga = ('ARW',
              'ARW')
        # Observed output.
        obs = gali.indelfree_gali_to_max_score(ga,
                                               smat)
        # Expected output.
        exp = 20.0
        # Test.
        assert obs == exp

    def test_three(self):
        # Input parameter.
        ga = ('ARN',
              'ARW')
        # Observed output.
        obs = gali.indelfree_gali_to_max_score(ga,
                                               smat)
        # Expected output.
        exp = 15.0
        # Test.
        assert obs == exp

    def test_four(self):
        # Input parameter.
        ga = ('ARW',
              'ARN')
        # Observed output.
        obs = gali.indelfree_gali_to_max_score(ga,
                                               smat)
        # Expected output.
        exp = 15.0
        # Test.
        assert obs == exp


class TestIndelfreeGaliToMeanScore:

    def test_one(self):
        # Input parameter.
        ga = ('RARARR',
              'AAAAAA')
        # Observed output.
        obs = gali.indelfree_gali_to_mean_score(ga,
                                                smat)
        # Expected output.
        exp = 4.0
        # Test.
        assert obs == exp

    def test_two(self):
        # Input parameter.
        ga = ('ARA',
              'AAA')
        # Observed output.
        obs = gali.indelfree_gali_to_mean_score(ga,
                                                smat)
        # Expected output.
        exp = 7.0
        # Test.
        assert obs == exp

    def test_three(self):
        # Input parameter.
        ga = ('ARAA',
              'AARR')
        # Observed output.
        obs = gali.indelfree_gali_to_mean_score(ga,
                                                smat)
        # Expected output.
        exp = 6.5
        # Test.
        assert obs == exp


class TestDenseGaliToQuantifier:

    def test_perfect_alignment(self):
        # Input parameter.
        ga = ('MTAEQRHNLQAYSDYVRKSLDPTHILSYMTPWLPENEVQSIQAEKNNKGPMEAASLFLRLLLELQVEGWFRGFLDALNHAGYSGLYEAIENWD',
              'MTAEQRHNLQAYSDYVRKSLDPTHILSYMTPWLPENEVQSIQAEKNNKGPMEAASLFLRLLLELQVEGWFRGFLDALNHAGYSGLYEAIENWD')
        # Observed output.
        obs = gali.dense_gali_to_quantifier(
            ga,
            smat,
            gapopen_penalty=10.0, gapextend_penalty=0.5)
        obs = round(obs, 4)
        # Expected output.
        exp = 1.0000
        # Test.
        assert obs == exp

    def test_bad_alignment(self):
        # Input parameter.
        ga = ('----------------------------------------------DKVLKEKRKLFIRSM----GEGTINGLLDEL-------LQTRVLNKEEMEKVKRENATVMDKTRALIDSVIPKGAQACQICITYICEEDSYLAGTLGLS',
              'MTAEQRHNLQAYSDYVRKSLDPTHILSYMTPWLPENEVQSIQAEKNNKGPMEAASLFLRLLLELQVEGWFRGFLDALNHAGYSGLYEAIENWD----------------------------------------------------')
        # Observed output.
        obs = gali.dense_gali_to_quantifier(
            ga,
            smat,
            gapopen_penalty=10.0, gapextend_penalty=0.5)
        obs = round(obs, 4)
        # Expected output.
        exp = 0.1571
        # Test.
        assert obs == exp

    def test_horrible_alignment(self):
        # Input parameter.
        ga = ('-----------------------------------------------------------------------------------NDDLDLEAAVARVRPQLVEFLSHCPDWLLTTCQRFLPEVALNGLDGITDHKEKVSALLELLEKAGPATWKQFAQYLCMECDLPLDLEIQLISSAG',
              'REQFYNKGIRPYMGRFATDIKVREILPYLQCLTISDREEIEAKKEQYGNYNAVQTLLDNLRRRENWIDEFITALRKCELGSLANEMSDIY----------------------------------------------------------------------------------------')
        # Observed output.
        obs = gali.dense_gali_to_quantifier(
            ga,
            smat,
            gapopen_penalty=10.0, gapextend_penalty=0.5)
        obs = round(obs, 4)
        # Expected output.
        exp = 0.0214
        # Test.
        assert obs == exp
