"""\
Handle global sequence alignments.
"""

import sys
from typing import Tuple, Union

import pandas as pd

from src.modules.ali import get_ali_length
from src.modules.ali import ali_to_indelfree_ali


def gali_to_score(
        gali: Tuple[str, str],
        substmat: pd.DataFrame,
        gapopen_penalty: float = 10.0,
        gapextend_penalty: float = 0.5
        ) -> float:
    """\
    Calculate total score for input global alignment.

    :param gali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment may contain gap-gap-pairs.

    :param substmat:
        pd.DataFrame

        Substitution matrix:
        - index:
            row-labels
            (each label is a str).
        - columns:
            column-labels
            (each label is a str).
        - data:
            cells of the substitution matrix
            (each element is an int).

            [[row1_col1, row1_col2, ..., row1_colN],
             [row2_col1, row2_col2, ..., row2_colN],
             ...,
             [rowN_col1, rowN_col2, ..., rowN_colN]]

    :param gapopen_penalty:
        float (positive)

        (default: 10.0,
         same default as for needleall.)

    :param gapextend_penalty:
        float (positive)

        (default: 0.5,
         same default as for needleall.)

    :return:
        float
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = gali

    # Initialise result.
    total_score = 0.0

    # Initialise states.
    #
    # If the element in the sequence happens to be a gap:
    # is it an opening (or an extending) gap?
    gap_a_is_opening_gap = True
    gap_b_is_opening_gap = True

    # For each aligned pair.
    for el_a, el_b in zip(seq_a, seq_b):

        # If it is a gap-gap-pair.
        if el_a == '-' and el_b == '-':

            # Ignore the current position.
            position_score = 0

        # If sequence A has a gap
        # (and sequence B does NOT).
        elif el_a == '-':

            # If it is an opening gap.
            if gap_a_is_opening_gap:
                # Apply gapopen-penalty.
                position_score = -1 * gapopen_penalty
                # Toggle state for potential following gaps.
                gap_a_is_opening_gap = False

            # If it is an extending gap.
            else:
                # Apply gapextend-penalty.
                position_score = -1 * gapextend_penalty

        # If sequence B has a gap
        # (and sequence A does NOT).
        elif el_b == '-':

            # If it is an opening gap.
            if gap_b_is_opening_gap:
                # Apply gapopen-penalty.
                position_score = -1 * gapopen_penalty
                # Toggle state for potential following gaps.
                gap_b_is_opening_gap = False

            # If it is an extending gap.
            else:
                # Apply gapextend-penalty.
                position_score = -1 * gapextend_penalty

        # If it is a residue-residue-pair.
        else:

            # Refer to substitution matrix.
            position_score = substmat.at[el_a, el_b]

            # Reset states for potential following gaps.
            gap_a_is_opening_gap = True
            gap_b_is_opening_gap = True

        # Update result.
        total_score += position_score

    # Return final result.
    return total_score


def indelfree_gali_to_max_score(
        gali: Tuple[str, str],
        substmat: pd.DataFrame
        ) -> float:
    """\
    Calculate the maximum score for the input indel-free global
    alignment.

    The maximum score is determined with the self-alignment-scores of
    the two aligned sequences.  Of these two self-alignment-scores the
    lower value is chosen.

    :param gali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment does NOT contain gaps.

    :param substmat:
        pd.DataFrame

        Substitution matrix:
        - index:
            row-labels
            (each label is a str).
        - columns:
            column-labels
            (each label is a str).
        - data:
            cells of the substitution matrix
            (each element is an int).

            [[row1_col1, row1_col2, ..., row1_colN],
             [row2_col1, row2_col2, ..., row2_colN],
             ...,
             [rowN_col1, rowN_col2, ..., rowN_colN]]

    :return:
        float
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = gali

    # Score of the self-alignments (global).
    seq_a_self_score = gali_to_score((seq_a, seq_a), substmat)
    seq_b_self_score = gali_to_score((seq_b, seq_b), substmat)

    # Use the lower self-alignment score.
    max_score = min(seq_a_self_score,
                    seq_b_self_score)

    # Return result.
    return max_score


def indelfree_gali_to_mean_score(
        gali: Tuple[str, str],
        substmat: pd.DataFrame
        ) -> float:
    """\
    Calculate the mean score for the input indel-free global alignment.

    This mean score is the score which would be expected on average for
    a pair of randomly shuffled sequences with the same composition of
    amino acids as the two aligned sequences.

    :param gali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment does NOT contain gaps.

    :param substmat:
        pd.DataFrame

        Substitution matrix:
        - index:
            row-labels
            (each label is a str).
        - columns:
            column-labels
            (each label is a str).
        - data:
            cells of the substitution matrix
            (each element is an int).

            [[row1_col1, row1_col2, ..., row1_colN],
             [row2_col1, row2_col2, ..., row2_colN],
             ...,
             [rowN_col1, rowN_col2, ..., rowN_colN]]

    :return:
        float
    """
    # -----------------------------------------------------------------|------|
    # Preparations.

    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = gali

    # Get length of the alignment.
    gali_length = get_ali_length(gali)

    # Initialise.
    mean_score = 0.0

    # Trivial case:
    # The alignment is empty.
    if gali_length == 0:
        return mean_score

    # -----------------------------------------------------------------|------|
    # For each of the 2 aligned sequences:
    # Count absolute frequency for all residues.

    # Initialise memory.
    # - key: residue
    # - value: count.
    seq_a_res_to_count = {}
    seq_b_res_to_count = {}

    # For each of the 2 aligned sequences.
    for seq, res_to_count in zip([seq_a, seq_b],
                                 [seq_a_res_to_count, seq_b_res_to_count]):

        # For each sequence-position.
        for res in seq:

            # If this residue is new to the memory.
            if res not in res_to_count:
                # Initialise new entry for residue.
                res_to_count[res] = 0

            # Update memory.
            res_to_count[res] += 1

    # -----------------------------------------------------------------|------|
    # Calculate mean score.
    #
    #                SUM   SUM  ( count_a * count_b * score_ab )
    #               res_a res_b
    # mean_score = ----------------------------------------------
    #                             gali_length

    # For all combinations of residue-pairs.
    for res_a in seq_a_res_to_count.keys():
        for res_b in seq_b_res_to_count.keys():

            # Get absolute frequency for the residues in the pair.
            count_a = seq_a_res_to_count[res_a]
            count_b = seq_b_res_to_count[res_b]

            # Get substitution-score for pair.
            score_ab = substmat.at[res_a, res_b]

            # Sum over all combinations of residue-pairs.
            mean_score += count_a * count_b * score_ab

    # Final mean score.
    mean_score /= gali_length

    # Return result.
    return mean_score


def dense_gali_to_quantifier(
        gali: Tuple[str, str],
        substmat: pd.DataFrame,
        gapopen_penalty: float = 10.0,
        gapextend_penalty: float = 0.5
        ) -> Union[float, None]:
    """\
    Quantify the quality of the input dense global alignment.

    The quantifier has the value range [0; 1]:
    Short low-similarity alignments yield values closer to zero,
    while long high-similarity alignments result in values closer to 1.

    :param gali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment does NOT contain gap-gap-pairs.

    :param substmat:
        pd.DataFrame

        Substitution matrix:
        - index:
            row-labels
            (each label is a str).
        - columns:
            column-labels
            (each label is a str).
        - data:
            cells of the substitution matrix
            (each element is an int).

            [[row1_col1, row1_col2, ..., row1_colN],
             [row2_col1, row2_col2, ..., row2_colN],
             ...,
             [rowN_col1, rowN_col2, ..., rowN_colN]]

    :param gapopen_penalty:
        float (positive)

        (default: 10.0,
         same default as for needleall.)

    :param gapextend_penalty:
        float (positive)

        (default: 0.5,
         same default as for needleall.)

    :return:
        float

        - or -

        None: Signal that quantifier can NOT be calculated
              (when max_score == mean_score).
    """
    # -----------------------------------------------------------------|------|
    # Preparations.

    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = gali

    # Get indel-free alignment.
    indelfree_gali = ali_to_indelfree_ali(gali)

    # Get length of the indel-free alignment.
    indelfree_gali_length = get_ali_length(indelfree_gali)

    # -----------------------------------------------------------------|------|
    # For indel-free alignment.

    # Get score.
    score = gali_to_score(
        indelfree_gali,
        substmat,
        gapextend_penalty=gapextend_penalty,
        gapopen_penalty=gapopen_penalty)

    # Get mean-score.
    mean_score = indelfree_gali_to_mean_score(
        indelfree_gali,
        substmat)

    # Get max-score.
    max_score = indelfree_gali_to_max_score(
        indelfree_gali,
        substmat)

    # Special case:
    #
    # The quantifier can NOT be calculated,
    # because the denominator would be zero for the quantifier of the
    # indel-free alignment.
    if max_score == mean_score:
        # Signal that quantifier can NOT be calculated.
        return None

    # Do feature scaling.
    indelfree_quanitfier = (score - mean_score) / (max_score - mean_score)

    # -----------------------------------------------------------------|------|
    # Determine coverage of indel-free alignment in relation to the
    # input alignment.

    # Count residues in sequences of input alignment.
    #
    # Input sequences without gaps.
    seq_a_gapless = seq_a.replace('-', '')
    seq_b_gapless = seq_b.replace('-', '')
    # Get residue-count for longer sequence of the input alignment.
    gali_longseq_length = max(len(seq_a_gapless),
                              len(seq_b_gapless))

    # Calculate coverage.
    coverage = indelfree_gali_length / gali_longseq_length

    # -----------------------------------------------------------------|------|
    # Adjust quantifier of indel-free alignment to input alignment.

    # Adjust quantifier.
    quantifier = indelfree_quanitfier * coverage

    # Return result.
    return quantifier
