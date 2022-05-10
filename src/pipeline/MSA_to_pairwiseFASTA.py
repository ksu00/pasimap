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
        Re-format MSA to pairwise alignments.

        STDOUT:
        - entry_1 (pair 1)
        - entry_1 (pair 1)
        - entry_2 (pair 2)
        - entry_1 (pair 2)
        - entry_3 (pair 3)
        - entry_1 (pair 3)
        - [...]
        - entry_n (pair n*n)
        - entry_n (pair n*n)
        """))
    parser.add_argument(
        "infile", type=str,
        help=textwrap.dedent("""\
        str
        infile

        MSA containing n FASTA-entries.
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
    entry_s = list(iterate_fasta(f))

# FB.
num = len(entry_s)

# Iterate over all pairs of FASTA-entries.
for entry_a_header, entry_a_body in entry_s:
    for entry_b_header, entry_b_body in entry_s:

        # STDOUT.
        # Print pairwise alignment.
        print(entry_b_header)
        print(entry_b_body)
        print(entry_a_header)
        print(entry_a_body)

# FB.
if args.verbose:
    print(f"Success:\n"
          f"  Parsed '{num}' FASTA-entries.",
          file=sys.stderr, flush=True)
