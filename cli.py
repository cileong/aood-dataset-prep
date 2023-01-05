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
        "-o",
        "--output-path",
        type=str,
        default="output.json",
        help="path to the output JSON file",
    )

    parser.add_argument(
        "--clean-path",
        action="store_true",
    )

    return parser


if __name__ == "__main__":
    from converter import *
    from path_wrangler import *
    import json
    from pathlib import Path

    # Retrieve the CLI arguments.
    parser = build_parser()
    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    clean_path = args.clean_path

    if clean_path:
        with open(input_path) as file:
            data = json.load(file)
        for entry in data:
            entry["image"] = str(to_local_path(entry["image"]))
        converter = DataConverter(data)
    else:
        converter = DataConverter.from_json(input_path)

    # Dump the JSON file.
    converter.to_json(output_path)
