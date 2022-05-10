import argparse
import sys
import textwrap

from src.modules.ali import is_valid_ali
from src.modules.ali import ali_to_dense_ali
from src.modules.gali import dense_gali_to_quantifier
from src.modules.substmat import parse_substmat_as_df


def parse_args() -> argparse.Namespace:
    """\
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Calculate quantifier for the pairwise global alignments.

        The quantifier has the value range [0; 1]:
        Short low-similarity alignments yield values closer to zero,
        while long high-similarity alignments result in values closer to
        1.

        Special case:
        If the quantifier can NOT be calculated, it will be omitted.
        """))
    parser.add_argument(
        "in_alignment_file", type=str,
        help=textwrap.dedent("""\
        str
        infile

        Pairwise alignments:

        each line of file:
        csv-elements of a single pairwise alignment:
        - entry_a_header
        - entry_b_header
        - entry_a_body
        - entry_b_body

        If there are redundant pairs (e.g.: A<->B and B<->A), only the
        1st occurrence will be quantified.

        Self-alignments (e.g.: A<->A) will NOT be quantified.
        """))
    parser.add_argument(
        "in_substmat_file", type=str,
        help=textwrap.dedent("""\
        str
        infile

        Substitution matrix:

        each line of file:
        csv-elements of a single pairwise alignment:
        - entry_a_header
        - entry_b_header
        - entry_a_body
        - entry_b_body
        """))
    parser.add_argument(
        "out_map_file", type=str,
        help=textwrap.dedent("""\
        str
        outfile

        Map each entry to a number:

        each line of file:
        csv-elements of a single entry:
        - FASTA-header
        - number (starts with 1)
        """))
    parser.add_argument(
        "-go", "--gapopen_penalty", type=float, default=10.0,
        help=textwrap.dedent("""\
        float (positive)

        (default: 10.0,
         same default as for needleall.)
        """))
    parser.add_argument(
        "-ge", "--gapextend_penalty", type=float, default=0.5,
        help=textwrap.dedent("""\
        float (positive)

        (default: 0.5,
         same default as for needleall.)
        """))
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help=textwrap.dedent("""\
        Be verbose with printing to STDERR.
        """))
    args = parser.parse_args()

    return args


# ---------------------------------------------------------------------|------|
# Preparations.

# Parse command-line arguments.
args = parse_args()

# Parse substitution-matrix.
with open(args.in_substmat_file) as f:
    substmat = parse_substmat_as_df(f)

# ---------------------------------------------------------------------|------|
# FB:
# Initialise counters.

# Number of parsed lines.
parsed_line_count = 0

# Number of self-alignment-pairs.
self_pair_count = 0
# Number of redundant alignment-pairs.
redundant_pair_count = 0
# Number of unique alignment-pairs.
unique_pair_count = 0

# Number of omitted (unique) alignment-pairs.
# (Quantifier could NOT be calculated).
omitted_unique_pair_count = 0
# Number of output (unique) alignment-pairs.
# (Quantifier could be calculated.)
output_unique_pair_count = 0

# ---------------------------------------------------------------------|------|
# Initialise memory.

# Map each entry to a number:
# - key:   entry-header
# - value: number (starts with 1).
header_to_num = {}

# Calculated quantifiers.
# - key:   tuple: pair of aligned sequences
#                 (num_smaller, num_larger)
# - value: quantifier
#          (if there are redundant pairs, only store the 1st result).
pair_to_quantifier = {}

# ---------------------------------------------------------------------|------|
# Calculate quantifier for each pairwise alignment.

# Open file containing pairwise alignments.
with open(args.in_alignment_file) as f:

    # For each line.
    for line in f:

        # -------------------------------------------------------------|------|
        # Parse pair of aligned sequences.

        # Remove trailing newline character.
        parsed_line = line.rstrip()
        # Split csv-elements.
        parsed_line = parsed_line.split(',')

        # Unpack csv-elements.
        header_a, header_b, seq_a, seq_b = parsed_line

        # FB.
        parsed_line_count += 1

        # -------------------------------------------------------------|------|
        # Ignore self-alignments.

        # If it is a self-alignment.
        if header_a == header_b:
            # FB.
            self_pair_count += 1
            # Ignore current pairwise alignment,
            # continue with next one.
            continue

        # -------------------------------------------------------------|------|
        # Map each entry to a number.

        # Do the same for both entries of pair.
        for header in [header_b, header_a]:

            # If it a new entry.
            if header not in header_to_num:

                # Generate number for new entry.
                num = len(header_to_num) + 1

                # Add new entry.
                header_to_num[header] = num

        # Get number of each entry.
        num_a = header_to_num[header_a]
        num_b = header_to_num[header_b]

        # -------------------------------------------------------------|------|
        # Prepare dense alignment.

        # Pack alignment.
        gali = seq_a, seq_b

        # Sanity check: fail.
        # If the 2 aligned sequences do NOT have the same length:
        # -> ValueError.
        if not is_valid_ali(gali):
            pass

        # Get dense alignment.
        dense_gali = ali_to_dense_ali(gali)

        # -------------------------------------------------------------|------|
        # Create key:
        # Pair of aligned sequences.

        num_smaller, num_larger = sorted([num_a, num_b])
        pair = (num_smaller, num_larger)

        # -------------------------------------------------------------|------|
        # Ignore redundant alignments.

        # If the quantifier has already been calculated for this pair.
        if pair in pair_to_quantifier:
            # FB.
            redundant_pair_count += 1
            # Ignore current pairwise alignment,
            # continue with next one.
            continue

        # -------------------------------------------------------------|------|
        # Calculate and memorise quantifier.

        # FB.
        unique_pair_count += 1

        # FB.
        if args.verbose:
            print(f"#{num_smaller}<->#{num_larger}      ",
                  end="\r",
                  file=sys.stderr, flush=True)

        # Calculate quantifier.
        quantifier = dense_gali_to_quantifier(
            dense_gali,
            substmat,
            gapopen_penalty=args.gapopen_penalty,
            gapextend_penalty=args.gapextend_penalty)

        # If quantifier could NOT be calculated.
        if quantifier is None:

            # FB.
            omitted_unique_pair_count += 1

            # FB.
            if args.verbose:
                print(
                    f"\n"
                    f"pairwise alignment:\n"
                    f"  {header_a}\n"
                    f"  {seq_a}\n"
                    f"  {header_b}\n"
                    f"  {seq_b}\n"
                    f"-> quantifier could NOT be calculated.",
                    file=sys.stderr, flush=True)

        # If quantifier could be calculated.
        else:

            # Update memory.
            pair_to_quantifier[pair] = quantifier

            # FB.
            output_unique_pair_count += 1

# FB.
if args.verbose:
    print(f"last pair: #{num_smaller}<->#{num_larger}",
          file=sys.stderr, flush=True)

# ---------------------------------------------------------------------|------|
# STDOUT.

# For sorted alignment-pairs.
for pair in sorted(pair_to_quantifier.keys()):

    # Get numbers of pair.
    num_smaller, num_larger = pair
    # Get quantifier of pair.
    quantifier = pair_to_quantifier[pair]

    # STDOUT.
    print("{0:6} {1:6} {2:7.4f}".format(num_smaller, num_larger, quantifier))

# ---------------------------------------------------------------------|------|
# Output mapping of each header to its number.

# Prepare file for writing.
with open(args.out_map_file, 'w') as f:
    # Sort by number.
    for header, num in sorted(header_to_num.items(), key=lambda d: d[1]):
        # Write in csv-format.
        f.write(f"{header},{num}\n")

# ---------------------------------------------------------------------|------|
# FB.

if args.verbose:
    print(f"\n"
          f"Success:\n"
          f"  parsed pairs: {parsed_line_count}\n"
          f"  - self-pairs:      {self_pair_count}\n"
          f"  - redundant pairs: {redundant_pair_count}\n"
          f"  - unique pairs:    {unique_pair_count}\n"
          f"    - omitted quantifiers: {omitted_unique_pair_count}\n"
          f"    - output quantifiers:  {output_unique_pair_count}",
          file=sys.stderr, flush=True)
