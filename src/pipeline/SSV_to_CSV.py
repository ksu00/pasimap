import argparse
import sys
import textwrap


def parse_args() -> argparse.Namespace:
    """\
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Convert ssv-format to csv-format.
        """))
    parser.add_argument(
        "in_file", type=str,
        help=textwrap.dedent("""\
        str
        infile
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

# FB.
# Number of parsed lines.
parsed_line_count = 0

# ---------------------------------------------------------------------|------|
# Parse infile.

# Open infile.
with open(args.in_file) as f:

    # For each line.
    for line in f:

        # -------------------------------------------------------------|------|
        # Parse ssv-elements.

        # Remove trailing newline character.
        parsed_line = line.rstrip()
        # Split ssv-elements.
        parsed_line = parsed_line.split()

        # FB.
        parsed_line_count += 1

        # -------------------------------------------------------------|------|
        # STDOUT.

        print(",".join(parsed_line))

# ---------------------------------------------------------------------|------|
# FB.

if args.verbose:
    print(f"Success:\n"
          f"  parsed lines: {parsed_line_count}",
          file=sys.stderr, flush=True)
