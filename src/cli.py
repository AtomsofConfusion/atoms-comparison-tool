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
@click.option('--input', type = str, required = True, help = 'Directory containing three folders of source data.')
@click.option('--output', type = str, help = 'Directory to store output files. The input is optional.')
@click.option('--codeql', type = str, required = True, help = 'Relative path to truncate from file names in the CodeQL data.')
@click.option('--clojure', type = str, help = 'Relative path to truncate from file names in the Clojure data.')
@click.option('--coccinelle', type = str, required = True, help = 'Relative path to truncate from file names in the Coccinelle data.')
@click.option('--whichtwo', type = str, required = True, help = "This option selects two, or all, of the three tools to be compared. Four possible inputs are supported: 'CLJvCQL', 'CLJvCNL', 'CQLnCNL', and 'all'. Anything else will behave as the 'all' option.")
def cli(input, output, codeql, clojure, coccinelle, whichtwo):
    """The Atoms Comparison tool gathers and compares output from three sources previously developed by the team. Please refer to the README page for more info on each source. To use this project, you will enter four mandatory and two optional options. The usage of each option is listed below."""
    try:
        checked_input_path, checked_output_path = validate_paths(input, output)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)


    compare_and_output(checked_input_path, checked_output_path, codeql, clojure, coccinelle, whichtwo)

    print(f"Process completed, check output at: \033[1m{checked_output_path}\033[0m")
