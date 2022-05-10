import argparse
import sys
import textwrap

from src.modules.fasta import iterate_fasta


def parse_args() -> argparse.Namespace:
    """\
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Create secure FASTA-format.

        For header:
            Problematic characters
            (that would cause problems for the program 'needle'):
            - ':':  would truncate the header.
            - '|':  would cause the program to hang.
            -> Replace with the default replacement character '_'.

            Annoying characters
            (NOT really a problem, but are modified by 'needle'):
            - ',':  will be replaced with '_' by 'needle'.
            - '/':  will be replaced with '_' by 'needle'.
            - '\':  will be replaced with '_' by 'needle'.
            -> Replace with the default replacement character '_'.

        For body:
            Convert sequence to uppercase.
        """))
    parser.add_argument(
        "infile", type=str,
        help=textwrap.dedent("""\
        str
        infile

        Contains >= 1 FASTA-entries.
        """))
    parser.add_argument(
        "-w", "--wrap", action="store_true",
        help=textwrap.dedent("""\
        Wrap the FASTA-body to 60 residues per line.
        """))
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help=textwrap.dedent("""\
        Be verbose with printing to STDERR.
        """))
    args = parser.parse_args()

    return args


# Parse command-line arguments.
args = parse_args()

# Parse infile.
with open(args.infile) as f:

    # Get FASTA-entries from infile.
    #
    # header: replace forbidden characters.
    # body: convert sequence to uppercase.
    entry_s = iterate_fasta(f,
                            header_forbidden_char_s=':|,/\\',
                            header_replacement_char='_',
                            body_upper=True)

    # For each FASTA-entry.
    # FB: start numbering at 1.
    for num, (header, body) in enumerate(entry_s, 1):

        # STDOUT.
        # Print FASTA-header.
        print(header)

        # If FASTA-body should be wrapped.
        if args.wrap:
            # Wrap at 60 characters
            # (= sequence-width of needleall-output).
            for body_line in textwrap.wrap(body, width=60):
                # STDOUT.
                # Print wrapped line of FASTA-body.
                print(body_line)
        # If FASTA-body should NOT be wrapped.
        else:
            # STDOUT.
            # Print FASTA-body.
            print(body)

# FB.
if args.verbose:
    print(f"Success:\n"
          f"  Parsed '{num}' FASTA-entries.",
          file=sys.stderr, flush=True)
