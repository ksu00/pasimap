"""\
Handle file containing pairwise relations in space-separated-format.

Each line contains 3 space-separated values:
- object_a_num
- object_b_num
- pairwise_relation

The numbering starts with 1. Additionally, object_a_num < object_b_num.
"""


def is_pairwise(
        s: str
        ) -> bool:
    """\
    Check whether the given string is in pairwise format.

    :param s:
        str

    :return:
        bool
    """
    # Memory of pairwise relations.
    pair_to_relation = {}

    # Memory of all numbers.
    num_s = set()

    for line in s.splitlines():

        # Ignore empty lines.
        if not line:
            continue

        # Parse ssv-elements.
        el_s = line.split()

        # Sanity check: fail.
        # Incorrect number of ssv-elements.
        if len(el_s) != 3:
            return False

        # Interpret ssv-elements.
        a_num, b_num, relation = el_s

        # Convert to ssv-elements to correct types.
        try:
            a_num = int(a_num)
            b_num = int(b_num)
            relation = float(relation)
        # Sanity check: fail.
        # Impossible to convert to correct types.
        except ValueError:
            return False

        # Sanity check: fail.
        # Diagonal element.
        if a_num == b_num:
            return False

        # Sanity check: fail.
        # Pairwise relation is NOT in the value range [-1; 1].
        if relation < -1 or relation > 1:
            return False

        # Create identifier for pair.
        # (sort numbers in ascending order).
        pair = tuple(sorted([a_num, b_num]))

        # If this is a new pair.
        if pair not in pair_to_relation:
            # Create new entry.
            pair_to_relation[pair] = relation
            # Also update memory of all numbers.
            num_s.add(a_num)
            num_s.add(b_num)
        # If it is a redundant pair.
        else:
            # Sanity check: fail.
            # Redundant pair with NON-identical pairwise relation value.
            if relation != pair_to_relation[pair]:
                return False

    # Get n:
    # number of objects.
    n = len(num_s)

    # Sanity check: fail.
    # There are NO numbers,
    # i.e. input did NOT contain any lines with pairwise information.
    if n == 0:
        return False

    # Sanity check: fail.
    # Numbering is NOT continuous from 1 to n.
    if min(num_s) != 1 or max(num_s) != n:
        return False

    # Passed all checks.
    return True


def count_objects(
        s: str
        ) -> int:
    """\
    Count number of objects, of which the pairwise relations are given.

    Assumes that given file has the correct format.

    :param s:
        str

    :return:
        int
    """
    # Initialise.
    max_num = 0

    for line in s.splitlines():

        # Ignore empty lines.
        if not line:
            continue

        # Parse ssv-elements.
        a_num, b_num, _ = line.split()

        # Convert to correct type.
        a_num = int(a_num)
        b_num = int(b_num)

        # Do the same for both numbers.
        for num in [a_num, b_num]:
            # If a new maximum number is necessary.
            if num > max_num:
                # Update.
                max_num = num

    return max_num
