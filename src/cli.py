import sys
import click
from pathlib import Path
from src.comparsion import compare_and_output

def validate_paths(input_path: str, output_path: str) -> None:
    input_path = Path(input_path)
    
    if not input_path.is_dir():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    
    if output_path:
        output_path = Path(output_path)
        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print(f"Attention: new folder created at: {output_path}")

    if not output_path:
        output_path = Path(Path.cwd(), "output")

        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print("Default output folder created at:", output_path)

    return input_path, output_path

@click.command()
@click.option('--input', type = str)
@click.option('--output', type = str)
@click.option('--codeql', type = str)
@click.option('--clojure', type = str)
@click.option('--coccinelle', type = str)
# @click.option(help='You will provide five arguments corresponding to 1) input_path, 2) output_path, 3) codeql_path, 4) clojure_path, 5) coccinelle_path. The output_path can be optional by inputting "" indicating an empty string.')


def cli(input, output, codeql, clojure, coccinelle):

    try:
        checked_input_path, checked_output_path = validate_paths(input, output)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    compare_and_output(checked_input_path, checked_output_path, codeql, clojure, coccinelle)

    print(f"Process completed, check output at: \033[1m{checked_output_path}\033[0m")
