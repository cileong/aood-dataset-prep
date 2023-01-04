from argparse import ArgumentParser


def build_parser():
    """
    Build the argument parser for the command line interface.
    """
    parser = ArgumentParser(
        description="Convert Label Studio data to COCO-like format.",
    )

    parser.add_argument(
        "input_path",
        metavar="INPUT",
        type=str,
        help="path to the input JSON file",
    )

    parser.add_argument(
        "-o", "--output-path",
        type=str,
        default="output.json",
        help="path to the output JSON file",
    )

    return parser


if __name__ == "__main__":
    from converter import *
    from pathlib import Path

    # Retrieve the path arguments.
    parser = build_parser()
    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    # Dump the output.
    converter = DataConverter.from_json(input_path)
    converter.to_json(output_path)
