"""\
Handle substitution matrices (e.g. BLOSUM-matrices).
"""

from typing import TextIO

import pandas as pd


def parse_substmat_as_df(
        opened_infile: TextIO
        ) -> pd.DataFrame:
    """\
    Parse the input substitution matrix as a Pandas DataFrame.

    :param opened_infile:
        TextIO

    :return:
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
    """
    # State.
    # Whether line containing column-labels has already been parsed.
    column_label_line_parsed = False

    # Initialise.
    # (-> columns of pd.Dataframe.)
    row_label_s = []

    # Initialise.
    # (-> data of pd.DataFrame.)
    mat = []

    # For each line.
    # Before EOF is reached.
    for line in opened_infile:

        # Remove trailing newline character.
        parsed_line = line.rstrip()

        # Handle comment-lines:
        #
        # Comment-lines start with the character '#'.
        if parsed_line.startswith('#'):
            # Ignore comment-lines.
            pass

        # Handle column-labels-line:
        #
        # The 1st non-comment-line contains the column-labels.
        elif not column_label_line_parsed:
            # Parse line containing column-labels.
            # (-> index of pd.DataFrame.)
            column_label_s = parsed_line.split()
            # Toggle state.
            column_label_line_parsed = True

        # Handle normal lines:
        #
        # After the 1st non-comment-line.
        else:
            # Parse elements.
            parsed_line = parsed_line.split()

            # 1st element of label of the current row.
            row_label_s.append(parsed_line[0])

            # 2nd, 3rd, ... and last elements are cells in the matrix.
            cell_s = parsed_line[1:]
            # Convert cell-contents to int.
            cell_s = [int(el) for el in cell_s]
            # Append cells of current row to matrix.
            mat.append(cell_s)

    # After parsing input.
    #
    # Create pd.DataFrame as result.
    result = pd.DataFrame(data=mat,
                          index=row_label_s,
                          columns=column_label_s)

    return result
