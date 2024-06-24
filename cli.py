from argparse import ArgumentParser
from typing import Any, List
import os

def parse_args(args: List[str]) -> Any:
    parser = ArgumentParser(description="A simple CLI tool that processes files.")
    parser.add_argument(
        'input_path', 
        type=str, 
        help='Path to the input file.'
    )
    parser.add_argument(
        'output_path', 
        type=str, 
        nargs='?',
        default='./output',  # Default output path if not provided
        help='Path to the output file. Defaults to "./output".'
    )
    return parser.parse_args(args)

def validate_paths(input_path: str, output_path: str) -> None:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    if not os.path.exists(output_path):
        raise FileNotFoundError(f"Output path does not exist: {output_path}")

if __name__ == "__main__":
    import sys
    args = parse_args(sys.argv[1:])
    try:
        validate_paths(args.input_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
    print(f"Input path: {args.input_path}")
    print(f"Output path: {args.output_path}")
