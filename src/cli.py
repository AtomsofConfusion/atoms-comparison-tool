import sys
import click
from pathlib import Path
from src.comparsion import compare_and_output

def validate_paths(input_path: str, output_path: str, whichtwo) -> None:
    input_path = Path(input_path)
    codeQL_directory = Path(input_path, "codeQL_data")
    clojure_directory = Path(input_path, "clojure_data/atomsClojure.csv")
    coccinelle_directory = Path(input_path, "coccinelle_data")

    codeQL_exists = codeQL_directory.is_dir()
    clojure_exists = clojure_directory.exists()
    coccinelle_exists = coccinelle_directory.is_dir()

    if not codeQL_exists and (whichtwo == "CQLvCNL" or whichtwo == "CLJvCQL" or whichtwo == "all"):
        raise FileNotFoundError(f"\033[91mCodeQL source does not exist: \033[0m{codeQL_directory}")
    
    if not clojure_exists and (whichtwo == "CLJvCNL" or whichtwo == "CLJvCQL" or whichtwo == "all"):
        raise FileNotFoundError(f"\033[91mClojure source does not exist: \033[0m{clojure_directory}")
    
    if not coccinelle_exists and (whichtwo == "CQLvCNL" or whichtwo == "CLJvCNL" or whichtwo == "all"):
        raise FileNotFoundError(f"\033[91mCoccinelle source does not exist: \033[0m{coccinelle_directory}")
    
    if not whichtwo:
        if codeQL_exists and clojure_exists and coccinelle_exists:
            whichtwo = "all"
        elif codeQL_exists and clojure_exists:
            whichtwo = "CLJvCQL"
        elif coccinelle_exists and clojure_exists:
            whichtwo = "CLJvCNL"
        elif codeQL_exists and coccinelle_exists:
            whichtwo = "CQLvCNL"
        else:
            print(f"\033[91mWARNING: \033[0mOnly one or fewer input source for comparsion, and the output could be meaningless.")
            sys.exit(0)
        print(f"whichtwo:", whichtwo)

    if output_path:
        output_path = Path(output_path)
        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print(f"\033[34mATTENTION: \033[0mnew folder created at: {output_path}")

    if not output_path:
        output_path = Path(Path.cwd(), "output")

        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print(f"\033[34mATTENTION: \033[0mDefault output folder created at:", output_path)

    return output_path, codeQL_directory, clojure_directory, coccinelle_directory, whichtwo

@click.command()
@click.option('--input', type = str, required = True, help = 'Directory containing three folders of source data.')
@click.option('--output', type = str, help = 'Directory to store output files. The input is optional.')
@click.option('--codeql_relative', type = str, required = True, help = 'Relative path to truncate from file names in the CodeQL data.')
@click.option('--clojure_relative', type = str, help = 'Relative path to truncate from file names in the Clojure data.')
@click.option('--coccinelle_relative', type = str, required = True, help = 'Relative path to truncate from file names in the Coccinelle data.')
@click.option('--whichtwo', type=click.Choice(['CLJvCQL', 'CLJvCNL', 'CQLvCNL', 'all']), help = "This option selects two, or all, of the three tools to be compared. Four possible inputs are supported: 'CLJvCQL', 'CLJvCNL', 'CQLvCNL', and 'all'. If omitted, the program will assign a value to this option by checking input folder availiability.")
def cli(input, output, codeql_relative, clojure_relative, coccinelle_relative, whichtwo):
    """The Atoms Comparison tool gathers and compares output from three sources previously developed by the team. Please refer to the README page for more info on each source. To use this project, you will enter four mandatory and two optional options. The usage of each option is listed below. Sample usage: compare --input "/home/usr/Documents/Atoms of Confusion/atoms-comparison-tool" --output "/home/usr/Documents/temp" --codeql "" --clojure "/Users/VSCode/AtomFinder/atom-finder/GitSourceCode/git/" --coccinelle "/home/ubuntu/atoms/projects/git/" --whichtwo CLJvCNL"""
    try:
        checked_output_path, codeQL_directory, clojure_directory, coccinelle_directory, whichtwo = validate_paths(input, output, whichtwo)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    compare_and_output(checked_output_path, codeql_relative, clojure_relative, coccinelle_relative, whichtwo, codeQL_directory, clojure_directory, coccinelle_directory)

    print(f"Process completed, check output at: \033[1m{checked_output_path}\033[0m")
