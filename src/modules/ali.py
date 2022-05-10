"""\
Handle sequence alignments.
"""

from typing import Tuple


def is_valid_ali(
        ali: Tuple[str, str]
        ) -> bool:
    """\
    Check whether the input alignment is valid.

    An alignment is considered valid, if the two aligned sequences have
    the same length.

    :param ali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment may contain gap-gap-pairs.

    :return:
        bool
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = ali

    # If the 2 aligned sequences have the same length.
    if len(seq_a) == len(seq_b):
        # The alignment is considered valid.
        validity = True
    # If the 2 aligned sequences do NOT have the same length.
    else:
        # The alignment is considered NON-valid.
        validity = False

    return validity


def ali_to_dense_ali(
        ali: Tuple[str, str]
        ) -> Tuple[str, str]:
    """\
    Remove gap-gap-pairs from input alignment.

    :param ali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment may contain gap-gap-pairs.

    :return:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment does NOT contain gap-gap-pairs.
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = ali

    # Initialise results.
    seq_a_dense = ''
    seq_b_dense = ''

    # For each aligned pair.
    for el_a, el_b in zip(seq_a, seq_b):

        # If it is a gap-gap-pair.
        if el_a == '-' and el_b == '-':
            # Ignore this pair.
            pass

        # If it is NOT a gap-gap-pair.
        else:
            # Update results.
            seq_a_dense += el_a
            seq_b_dense += el_b

    # Return result.
    return (seq_a_dense, seq_b_dense)


def ali_to_indelfree_ali(
        ali: Tuple[str, str]
        ) -> Tuple[str, str]:
    """\
    Remove gap-gap- and gap-residue-pairs from input alignment.

    :param ali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment may contain gap-gap-pairs.

    :return:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment does NOT contain gaps.
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = ali

    # Initialise results.
    seq_a_indelfree = ''
    seq_b_indelfree = ''

    # For each aligned pair.
    for el_a, el_b in zip(seq_a, seq_b):

        # If it is a residue-residue-pairing.
        if el_a != '-' and el_b != '-':
            # Update results.
            seq_a_indelfree += el_a
            seq_b_indelfree += el_b

    # Return result.
    return (seq_a_indelfree, seq_b_indelfree)


def get_ali_length(
        ali: Tuple[str, str]
        ) -> int:
    """\
    Get length of the alignment.

    :param ali:
        Tuple: alignment
        - str: sequence A
        - str: sequence B

        The alignment may contain gaps.
        The alignment should NOT contain gap-gap-pairs,
        because these would lead to unintended results.

    :return:
        int

        Length of the alignment.
    """
    # Unpack the 2 sequences of the input alignment.
    seq_a, seq_b = ali

    # Sanity check: fail.
    # The 2 aligned sequences do NOT have the same length.
    if not is_valid_ali(ali):
        # FB.
        raise ValueError(
            f'Faulty alignment:\n'
            f'  seq_a: {seq_a}\n'
            f'  seq_b: {seq_b}\n'
            f'  The 2 aligned sequences do NOT have the same length.')

    # Length of the alignment
    # is length of any of the 2 aligned sequences (e.g. sequence A).
    result = len(seq_a)

    return result
