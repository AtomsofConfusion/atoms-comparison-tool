from argparse import ArgumentParser
from typing import Any, List
from pathlib import Path

def parse_args(args: List[str]) -> Any:
    parser = ArgumentParser(description="A simple CLI tool that processes files.")
    parser.add_argument(
        'input_path', 
        type=str, 
        help='Path to the input folder. There should already be three subfolders containing source data for CodeQL, Clojure, and Coccinelle.'
    )
    parser.add_argument(
        'output_path', 
        type=str, 
        nargs='?',
        default=None,  # Default output path if not provided
        help='Path to the output folder. Defaults to ' + str(Path(Path.cwd(), "output"))
    )

    # input("Enter the next three path for Clojure, CodeQL, and Coccinelle...\n")

    # Arguments to truncate from global path
    parser.add_argument("clojure_path", type = str, help="Third argument")
    # parser.add_argument("codeQL_path", type = str, help="Fourth argument")
    # parser.add_argument("coccinelle_path", type = str, help="Fifth argument")

    return parser.parse_args(args)

def validate_paths(input_path: str, output_path: str) -> None:
    input_path = Path(input_path)
    
    if (output_path) and (not output_path.is_dir()):
        output_path = Path(output_path)
        output_path.mkdir(parents = True, exist_ok = True)
    
    if(not output_path):
        output_path = Path(Path.cwd(), "output")

        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print("Default output folder created at:", output_path)

    if not input_path.is_dir():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    
    if not output_path.is_dir():
        raise FileNotFoundError(f"Output path does not exist: {output_path}")

    return input_path, output_path