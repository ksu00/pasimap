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
        Get number of undirected connections for each datapoint.

        Only the non-self unique connections are counted,
        i.e.:
        - A<->A is NOT a connection.
        - A<->B, A<->B and B<->A only count as a single connection.

        STDOUT (sorted by number of connections):
        2 csv-elements:
        - datapoint
        - number of connections
        """))
    parser.add_argument(
        "in_file", type=str,
        help=textwrap.dedent("""\
        str
        infile

        each line of file:
        >= 2 elements:
        - datapoint_a
        - datapoint_b
        - [...]

        The infile may contain self-pairs (e.g.: A<->A).
        """))
    parser.add_argument(
        "-s", "--separator", type=str, default=None,
        help=textwrap.dedent("""\
        Separator between the elements in the input-file.

        Default:
        The elements are separated by (runs of consecutive) whitespace,
        i.e. they are treated as ssv-elements.
        """))
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help=textwrap.dedent("""\
        Be verbose with printing to STDERR.
        """))
    args = parser.parse_args()

    return args


# ---------------------------------------------------------------------|------|
# Parse command-line arguments.

args = parse_args()

# ---------------------------------------------------------------------|------|
# FB:
# Initialise counters.

# Number of parsed lines.
parsed_line_count = 0

# Number of self-pairs.
# -> do NOT contribute to number of connections.
self_pair_count = 0
# Number of redundant pairs.
# -> do NOT contribute to number of connections.
redundant_pair_count = 0
# Number of unique pairs.
# -> number of connections.
unique_pair_count = 0

# ---------------------------------------------------------------------|------|
# Initialise memory.

# Initialise set.
# Contains each datapoint (even those that only have self-pairs).
datapoint_s = set()

# Initialise set.
# Each element:
#   (datapoint_first, datapoint_second) <- alphanumerically sorted.
connection_s = set()

# ---------------------------------------------------------------------|------|
# Parse infile.

# Open infile.
with open(args.in_file) as f:

    # For each line.
    for line in f:

        # -------------------------------------------------------------|------|
        # Parse pairwise information.

        # Remove trailing newline character.
        parsed_line = line.rstrip()
        # Split elements.
        parsed_line = parsed_line.split(sep=args.separator)

        # Get relevant elements.
        datapoint_a = parsed_line[0]
        datapoint_b = parsed_line[1]

        # FB.
        parsed_line_count += 1

        # -------------------------------------------------------------|------|
        # Update memory:
        # - set of all datapoints
        # - set of all connections

        # If it is a self-pair:
        # - set of all datapoints -> update
        # - set of all connections -> pass.
        if datapoint_a == datapoint_b:

            # Process datapoints.
            datapoint_s.add(datapoint_a)

            # FB.
            self_pair_count += 1

        # If it is NOT a self-pair:
        # - set of all datapoints -> update
        # - set of all connections -> update.
        else:

            # Process datapoints.
            datapoint_s.add(datapoint_a)
            datapoint_s.add(datapoint_b)

            # Sort alphanumerically.
            # -> ensure that A<->B and B<->A are treated as the same
            #    connection.
            datapoint_first, datapoint_second = sorted([datapoint_a,
                                                        datapoint_b])

            # Potential connection.
            pair = (datapoint_first, datapoint_second)

            # If it is a known connection.
            if pair in connection_s:
                # FB.
                redundant_pair_count += 1
            # If it is a new connection.
            else:
                # Process connection.
                connection_s.add(pair)
                # FB.
                unique_pair_count += 1

# ---------------------------------------------------------------------|------|
# Prepare counter of connections.

# Initialise dict.
# - key:   datapoint
# - value: number of connections
datapoint_to_count = {}

# Initialise entries in dict.
for datapoint in datapoint_s:
    datapoint_to_count[datapoint] = 0

# ---------------------------------------------------------------------|------|
# Count connections.

# For all connections.
for datapoint_first, datapoint_second in connection_s:

    # Do the same for both datapoints.
    for datapoint in [datapoint_first, datapoint_second]:

        # Update memory.
        datapoint_to_count[datapoint] += 1

# ---------------------------------------------------------------------|------|
# STDOUT.

# Sort by count.
for datapoint, count in sorted(datapoint_to_count.items(),
                               key=lambda d: d[1]):

    # STDOUT.
    print(f"{datapoint},{count}")

# ---------------------------------------------------------------------|------|
# FB.

if args.verbose:
    print(f"Success:\n"
          f"  parsed pairs: {parsed_line_count}\n"
          f"  - self-pairs:      {self_pair_count}\n"
          f"  - redundant pairs: {redundant_pair_count}\n"
          f"  - unique pairs:    {unique_pair_count}",
          file=sys.stderr, flush=True)
