"""\
Handle FASTA-format.

FASTA-format:
    >= 1 FASTA-entries.

FASTA-entry:
    - FASTA-header:
        1 line starting with '>'
    - FASTA-body:
        >= 1 line
"""

from typing import Generator, TextIO, Tuple

from src.modules.utils import is_ascii


def is_fasta(
        s: str,
        check_header: bool = False,
        check_body: bool = False
        ) -> bool:
    """\
    Check whether the given string is in FASTA-format.

    :param s:
        str

    :param check_header:
        bool

        Only allow ASCII-characters.

    :param check_body:
        bool

        Only allow:
            - residues of the BLOSUM-matrix:
                A, R, N, D, C, Q, E, G, H, I, L, K, M, F, P, S, T, W, Y, V,
                B, Z, X
            - lowercase residues of the BLOSUM-matrix
            - stop-codon of the BLOSUM-matrix:
                *
            - gaps:
                -

    :return:
        bool
    """
    # Initialise state machine.
    state = 'start'

    # If content of the body should be checked.
    if check_body:
        # Residue-types of BLOSUM-matrix.
        allowed_chars = 'ARNDCQEGHILKMFPSTWYVBZX'
        # Lowercase residue-types of BLOSUM-matrix.
        allowed_chars += allowed_chars.lower()
        # Stop-codon of BLOSUM-matrix.
        allowed_chars += '*'
        # Gap.
        allowed_chars += '-'

    for line in s.splitlines():

        # Ignore empty lines.
        if not line:
            continue

        # If it is a header-line.
        if line.startswith('>'):

            # Sanity check: fail.
            # Previous line was also a header-line.
            if state == 'header':
                return False

            # Update state machine.
            state = 'header'

            # If content of header should be checked.
            if check_header:
                # Sanity check: fail.
                # header-line contains NON-ASCII-characters.
                if not is_ascii(line):
                    return False

        # If it is a body-line.
        else:

            # Sanity check: fail.
            # Previous line was start of file.
            if state == 'start':
                return False

            # Update state machine.
            state = 'body'

            # If content of the body should be checked.
            if check_body:
                for char in line:
                    # Sanity check: fail.
                    # body-line contains forbidden characters.
                    if char not in allowed_chars:
                        return False

    # After parsing all lines.
    #
    # Sanity check: pass.
    # Previous line was a body-line.
    if state == 'body':
        return True
    # Sanity check: fail.
    # Previous line was start of file or a header-line.
    else:
        return False


def count_fasta(
        s: str
        ) -> int:
    """\
    Count FASTA-entries.

    Presumes valid FASTA-format.

    :param s:
        str

    :return:
        int
    """
    # Initialise.
    count = 0

    # Count lines starting with the character '>'.
    for line in s.splitlines():
        if line.startswith('>'):
            count += 1

    return count


def iterate_fasta(
        opened_infile: TextIO,
        header_forbidden_char_s: str = '',
        header_replacement_char: str = '_',
        body_upper: bool = False,
        ) -> Generator[Tuple[str, str], None, None]:
    """\
    Iterate over FASTA-entries of FASTA-file.

    Ignore empty lines, if present.

    Throw ValueError, if the file does NOT have FASTA-format.

    :param opened_infile:
        TextIO

    :param header_forbidden_char_s:
        str

        String of characters that are forbidden in the header
        (but are allowed in the body).

    :param header_replacement_char:
        str

        Replace forbidden characters (header_forbidden_char_s) with this
        character.
        (Only in the header, NOT in the body.)

    :param body_upper:
        bool

        Convert characters of body to uppercase.

    :yield:
        Tuple: FASTA-entry
        - str: header
        - str: body (without '\n')
    """
    # Initialise state machine.
    state = 'start'

    # FB.
    line_num = 0

    # For each line.
    # Before EOF is reached.
    for line in opened_infile:

        #FB.
        line_num += 1

        # Remove trailing newline character.
        parsed_line = line.rstrip()

        # Ignore empty lines.
        if not parsed_line:
            continue

        # If it is a header-line.
        if parsed_line.startswith('>'):

            # Sanity check: fail.
            # Previous line was also a header-line.
            if state == 'header':
                # FB.
                raise ValueError(
                    f'Faulty infile (line: {line_num})!\n'
                    f'  The previous line was also a header-line.')

            # If it is NOT the first FASTA-entry.
            if state != 'start':
                # Yield previous FASTA-entry.
                yield (header, body)

            # Update state machine.
            state = 'header'

            # Initialise memory for new FASTA-entry.
            header = parsed_line
            body = ''

            # Replace forbidden characters in header.
            for c in header_forbidden_char_s:
                header = header.replace(c, header_replacement_char)

        # If it is a body-line.
        else:

            # Sanity check: fail.
            # Previous line was start of file.
            if state == 'start':
                # FB.
                raise ValueError(
                    f'Faulty infile (line: {line_num})!\n'
                    f'  The infile does NOT start with a header-line.')

            # Update state machine.
            state = 'body'

            # If characters of body should be in uppercase.
            if body_upper:
                parsed_line = parsed_line.upper()

            # Update memory for current FASTA-entry.
            body += parsed_line

    # Once EOF is reached.
    else:

        # Sanity check: fail.
        # Previous line was NOT a body-line.
        if state != 'body':
            # FB.
                raise ValueError(
                    f'Faulty infile (line: {line_num})!\n'
                    f'  The infile does NOT end with a body-line.')

        # Yield last FASTA-entry.
        yield (header, body)
