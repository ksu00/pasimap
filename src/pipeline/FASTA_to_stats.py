import argparse
import textwrap


from src.modules.fasta import iterate_fasta


def parse_args() -> argparse.Namespace:
    """\
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Check which FASTA-headers and -bodies are redundant,
        i.e. exist more than once.

        Also report number of unique FASTA-headers and -bodies.
        """))
    parser.add_argument(
        "in_file", type=str,
        help=textwrap.dedent("""\
        str
        input file

        Contains >= 1 FASTA-entries.
        """))
    parser.add_argument(
        "out_redundant_headers_file", type=str,
        help=textwrap.dedent("""\
        str
        output file

        Report redundant headers:
            by listing each redundant header with its frequency

            in the format:
                'header': frequency
        """))
    parser.add_argument(
        "out_redundant_bodies_file", type=str,
        help=textwrap.dedent("""\
        str
        output file

        Report redundant bodies:
            by listing header for each redundant body

            in the format:
                'header_1','header_2',[...],'header_N'
        """))
    parser.add_argument(
        "out_unique_headers_count_file", type=str,
        help=textwrap.dedent("""\
        str
        output file

        Number of unique headers.
        """))
    parser.add_argument(
        "out_unique_bodies_count_file", type=str,
        help=textwrap.dedent("""\
        str
        output file

        Number of unique bodies.
        """))
    args = parser.parse_args()

    return args


# ---------------------------------------------------------------------|------|
# Preparations.

# Parse command-line arguments.
args = parse_args()

# Memory for redundant headers.
header_to_count = {}

# Memory for redundant bodies.
# - key:   body
# - value: list of headers
body_to_headers = {}

# ---------------------------------------------------------------------|------|
# Process FASTA-entries.

# Parse infile.
with open(args.in_file) as f:

    # Get FASTA-entries from infile.
    entry_s = iterate_fasta(f)

    # Iterate over FASTA-headers.
    for header_raw, body in entry_s:

        # -------------------------------------------------------------|------|
        # Preparation.

        # Remove starting '>' from header.
        header = header_raw[1:]

        # -------------------------------------------------------------|------|
        # Process FASTA-header.

        # If FASTA-header is new to memory.
        if header not in header_to_count:
            # Initialise entry.
            header_to_count[header] = 0

        # Update count.
        header_to_count[header] += 1

        # -------------------------------------------------------------|------|
        # Process FASTA-body.

        # If FASTA-body is new to memory.
        if body not in body_to_headers:
            # Initialise entry.
            body_to_headers[body] = []

        # Update list of headers.
        body_to_headers[body].append(header)

# ---------------------------------------------------------------------|------|
# Report redundant FASTA-headers.

# Prepare file for writing.
with open(args.out_redundant_headers_file, 'w') as f:

    # Parse memory.
    for header, count in header_to_count.items():

        # If the header is redundant.
        if count != 1:

            # Write to file.
            f.write(f"'{header}': {count}\n")

# ---------------------------------------------------------------------|------|
# Report redundant FASTA-bodies.

# Prepare file for writing.
with open(args.out_redundant_bodies_file, 'w') as f:

    # Parse memory.
    for _, header_s in body_to_headers.items():

        # If the body is redundant.
        if len(header_s) > 1:

            # Write to file.
            # List header of each redundant body.
            f.write(','.join([f"'{header}'" for header in header_s]))
            f.write('\n')

# ---------------------------------------------------------------------|------|
# Report number of unique FASTA-headers.

# Prepare file for writing.
with open(args.out_unique_headers_count_file, 'w') as f:

    # Number of unique FASTA-headers.
    count = len(header_to_count.keys())

    # Write to file.
    f.write(f"{count}\n")

# ---------------------------------------------------------------------|------|
# Report number of unique FASTA-bodies.

# Prepare file for writing.
with open(args.out_unique_bodies_count_file, 'w') as f:

    # Number of unique FASTA-headers.
    count = len(body_to_headers.keys())

    # Write to file.
    f.write(f"{count}\n")
