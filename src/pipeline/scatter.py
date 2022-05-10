import argparse
import sys
import textwrap

import matplotlib.pyplot as plt


def parse_args() -> argparse.Namespace:
    """\
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent("""\
        Create 2D scatter-plot.
        """))
    parser.add_argument(
        "in_file", type=str,
        help=textwrap.dedent("""\
        str
        input-file
        """))
    parser.add_argument(
        "x_col_idx", type=int,
        help=textwrap.dedent("""\
        Column-index of x-coordinates (interval-scale) in input-file.
        """))
    parser.add_argument(
        "y_col_idx", type=int,
        help=textwrap.dedent("""\
        Column-index of y-coordinates (interval-scale) in input-file.
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
        "-xl", "--x_label", type=str, default="x",
        help=textwrap.dedent("""\
        Label for the x-axis.
        (default: "x")
        """))
    parser.add_argument(
        "-yl", "--y_label", type=str, default="y",
        help=textwrap.dedent("""\
        Label for the y-axis.
        (default: "y")
        """))
    parser.add_argument(
        "-xi", "--x_invert", action="store_true",
        help=textwrap.dedent("""\
        Invert the x-values.
        I.e. multiply each x-value with -1.
        """))
    parser.add_argument(
        "-yi", "--y_invert", action="store_true",
        help=textwrap.dedent("""\
        Invert the y-values.
        I.e. multiply each y-value with -1.
        """))
    parser.add_argument(
        "-a", "--alpha", type=float, default=0.5,
        help=textwrap.dedent("""\
        Opacity of marker.
        (value range: [0; 1])
        """))
    parser.add_argument(
        "-ms", "--marker_size", type=float, default=30,
        help=textwrap.dedent("""\
        Marker size in points.
        """))
    parser.add_argument(
        "-ec", "--edge_colour", type=str, default=None,
        help=textwrap.dedent("""\
        Edge-colour of the datapoints.
        (default: Omit edge-colour.)
        """))
    parser.add_argument(
        "-el", "--edge_linewidth", type=float, default=None,
        help=textwrap.dedent("""\
        Edge-linewidth of the datapoints.
        (default: Automatically choose edge-linewidth.)
        """))
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help=textwrap.dedent("""\
        Be verbose with printing to STDERR.
        """))

    description_group = parser.add_argument_group(
        "description_filter_group",
        textwrap.dedent("""\
        Plot description-text on top of markers.

        Triggered by specifying description_col_idx.
        """))
    description_group.add_argument(
        "-d", "--description_col_idx", type=int,
        help=textwrap.dedent("""\
        Column-index of description (nominal-scale) in input-file.
        """))
    description_group.add_argument(
        "-dfs", "--description_font_size", type=int, default=5,
        help=textwrap.dedent("""\
        Font-size of the description.
        (default: 5)
        """))

    origin_group = parser.add_argument_group(
        "origin_group",
        textwrap.dedent("""\
        Plot origin.

        Triggered with the parameter origin.
        """))
    origin_group.add_argument(
        "-r", "--origin", action="store_true",
        help=textwrap.dedent("""\
        Plot origin.
        """))
    origin_group.add_argument(
        "-rc", "--origin_colour", type=str, default='red',
        help=textwrap.dedent("""\
        Colour of the origin.
        (default: red.)
        """))

    outfile_group = parser.add_argument_group(
        "outfile_group",
        textwrap.dedent("""\
        Create output-file instead of interactive view.

        Triggered with the parameter outfile.
        """))
    outfile_group.add_argument(
        "-o", "--outfile", type=str,
        help=textwrap.dedent("""\
        Output-file
        with file-suffix specifying file-type:
          e.g. '.png', '.pdf', '.svg'.
        (If NO file-suffix is given, the default file-type 'png' will
         be used.)
        """))
    outfile_group.add_argument(
        "-ob", "--outfile_bbox", type=str, default=None,
        help=textwrap.dedent("""\
        Set boundary box for output-file.
        If 'tight', try to figure out the tight bbox of the figure.
        (default: None)
        """))

    args = parser.parse_args()

    return args


# ---------------------------------------------------------------------|------|
# Parse command-line arguments.

args = parse_args()

# ---------------------------------------------------------------------|------|
# Initialise memory.

x_s = []
y_s = []

# If descriptions should be added to each datapoint.
if args.description_col_idx is not None:

    description_s = []

# ---------------------------------------------------------------------|------|
# Default values.

default_label = 'data'
default_colour = 'black'
default_marker = 'o'

# ---------------------------------------------------------------------|------|
# Parse infile.

# FB:
# Number of parsed lines.
parsed_line_count = 0

# Open infile.
with open(args.in_file) as f:

    # For each line.
    for line in f:

        # -------------------------------------------------------------|------|
        # Parse line.

        # Remove trailing newline character.
        parsed_line = line.rstrip()
        # Split elements.
        parsed_line = parsed_line.split(sep=args.separator)

        # -------------------------------------------------------------|------|
        # Parse x-/y-elements.

        # Get elements.
        x = parsed_line[args.x_col_idx]
        y = parsed_line[args.y_col_idx]

        # Convert.
        x = float(x)
        y = float(y)

        # Update memory.
        x_s.append(x)
        y_s.append(y)

        # -------------------------------------------------------------|------|
        # Parse descriptions.

        # If descriptions should be added to each datapoint.
        if args.description_col_idx is not None:

            # Get description.
            description = parsed_line[args.description_col_idx]

            # Update memory.
            description_s.append(description)

        # -------------------------------------------------------------|------|
        # FB.

        parsed_line_count += 1

# FB.
if args.verbose:
    print(f"parsed lines: {parsed_line_count}",
          file=sys.stderr, flush=True)

# ---------------------------------------------------------------------|------|
# Inversion of the x-/y-values.

# If x-values should be inverted.
if args.x_invert:

    # Inversion:
    # Multiply each x-value with -1.
    x_s = [(-1) * x for x in x_s]

# If y-values should be inverted.
if args.y_invert:

    # Inversion:
    # Multiply each y-value with -1.
    y_s = [(-1) * y for y in y_s]

# ---------------------------------------------------------------------|------|
# Prepare plot.

# Prepare figure.
fig = plt.figure()

# Prepare standard 2d-axes.
ax = fig.add_subplot(111)

# ---------------------------------------------------------------------|------|
# Plot datapoints.

scatter_plot = plt.scatter(x_s, y_s,
                           c=default_colour,
                           s=args.marker_size,
                           label=default_label,
                           marker=default_marker,
                           edgecolors=args.edge_colour,
                           linewidth=args.edge_linewidth,
                           alpha=args.alpha)

# ---------------------------------------------------------------------|------|
# Plot descriptions.

# If descriptions should be added to each datapoint.
if args.description_col_idx is not None:

    # Plot description on top of markers.
    for x, y, description in zip(x_s, y_s, description_s):
        ax.text(x, y, description,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=args.description_font_size)

# ---------------------------------------------------------------------|------|
# Plot origin.

# If origin should be plotted.
if args.origin:

    # Plot origin.
    ax.scatter(0, 0,
               c=args.origin_colour,
               s=args.marker_size,
               label='origin',
               marker='+',
               linewidth=1)

# ---------------------------------------------------------------------|------|
# Plot legend.

ax.legend(bbox_to_anchor=(1.05, 1),
          loc=2,
          borderaxespad=0.)

# ---------------------------------------------------------------------|------|
# Fine-tune axes.

# Equal increments of x and y should have the same length.
ax.set_aspect("equal")

# ---------------------------------------------------------------------|------|
# Fine-tune title and labels of axes.

# Space (in points) between label and axes.
padspace = 10

# Add x-/y-labels.
ax.set_xlabel(
    args.x_label, labelpad=padspace)
ax.set_ylabel(
    args.y_label, labelpad=padspace)

# ---------------------------------------------------------------------|------|
# Fine-tune layout.

# Reduce white borders of plot.
plt.tight_layout()

# ---------------------------------------------------------------------|------|
# Output plot.

# If output-file should be created.
if args.outfile is not None:

    # Save the figure.
    plt.savefig(args.outfile, bbox_inches=args.outfile_bbox)

# If output-file should NOT be created.
else:

    # Start interactive view.
    plt.show()

# FB.
if args.verbose:
    print("-> finished plot",
          file=sys.stderr, flush=True)
