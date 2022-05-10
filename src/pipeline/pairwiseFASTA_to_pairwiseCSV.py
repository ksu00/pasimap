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
        Reformat pairwise alignments from FASTA-format to csv-format.

        STDOUT:
        n lines

        each line of STDOUT:
        csv-elements of a single pairwise alignment:
        - entry_a_header
        - entry_b_header
        - entry_a_body
        - entry_b_body
        """))
    parser.add_argument(
        "infile", type=str,
        help=textwrap.dedent("""\
        str
        infile

        FASTA-entries in the order:
        - pair_1_entry_a
        - pair_1_entry_b
        - pair_2_entry_a
        - pair_2_entry_b
        - [...]
        - pair_n_entry_a
        - pair_n_entry_b
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

# Iterate over all pairwise alignments,
# i.e. pairs of FASTA-entries.
# FB: start numbering at 1.
for num, (entry_a, entry_b) in enumerate(zip(entry_s[0::2], entry_s[1::2]),
                                         1):

    # Unpack FASTA-entries.
    entry_a_header, entry_a_body = entry_a
    entry_b_header, entry_b_body = entry_b

    # Remove starting '>'-character(s) from FASTA-headers.
    entry_a_header = entry_a_header.lstrip('>')
    entry_b_header = entry_b_header.lstrip('>')

    # STDOUT.
    # Print as csv-elements.
    print(','.join([entry_a_header,
                    entry_b_header,
                    entry_a_body,
                    entry_b_body]))

# FB.
if args.verbose:
    print(f"Success:\n"
          f"  Parsed '{num}' pairwise alignments.",
          file=sys.stderr, flush=True)
