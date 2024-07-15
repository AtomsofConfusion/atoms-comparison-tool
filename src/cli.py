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
@click.argument('input_path', type = click.STRING)
@click.argument('output_path', nargs = -1, type = click.STRING)
@click.argument('clojure_path', type = click.STRING)
@click.argument('codeql_path', type = click.STRING)
@click.argument('coccinelle_path', type = click.STRING)
def cli(input_path, output_path, clojure_path, codeql_path, coccinelle_path):
    if len(output_path)==0:
        output_path = None
    else:
        output_path = output_path[0]
    
    try:
        checked_input_path, checked_output_path = validate_paths(input_path, output_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    print(f"Input path: {checked_input_path}")
    print(f"Output path: {checked_output_path}")
    print(f"CodeQL_path is:{codeql_path}")
    print(f"Clojure_path is:{clojure_path}")
    print(f"Coccinelle_path is:{coccinelle_path}")

    compare_and_output(checked_input_path, checked_output_path, codeql_path, clojure_path, coccinelle_path)

    print(f"Process completed, check output at: \033[1m{checked_output_path}\033[0m")


