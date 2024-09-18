import sys
import click
from pathlib import Path
from src.comparison import *
from src.input_validation import *

### CHANGE
# make sure that the keys matches the name of the folders
source_mapping = {
    "codeQL_data": [validate_codeql, compare_codeql,],
    "clojure_data": [validate_csv, compare_clojure,],
    "coccinelle_data": [validate_csv, compare_coccinelle,],
}

class InsufficientInputSize(Exception):
    pass

TEXT = {
    'blue': '\033[34m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[32m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m',
    'bold': '\033[1m',
    'reset': "\033[0m"

}

input_list = []

def unknown(name):
    pass

def if_contains(key, items):
    return any(item in key for item in items)

def validate_paths(input_path, output_path, exclude_list):
    input_path = Path(input_path)
    
    if not input_path.is_dir():
        raise FileNotFoundError(f"{TEXT['red']}Error:{TEXT['reset']} Input path does not exist: {input_path}")

    for entry in input_path.iterdir():
        function_list = source_mapping.get(entry.name, [])
        if function_list and not if_contains(entry.name, exclude_list) and function_list[0](entry):
            input_list.append(entry.name)

    if output_path:
        output_path = Path(output_path)
        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print(f"{TEXT['blue']}ATTENTION:{TEXT['reset']} New output folder created at: {output_path}")
    else:
        output_path = Path.cwd() / "output"
        if not output_path.is_dir():        
            output_path.mkdir(parents = True, exist_ok = True)
            print(f"{TEXT['blue']}ATTENTION:{TEXT['reset']} Default output folder created at: {output_path}")

    return output_path

### CHANGE
@click.command()
@click.option('--input', type = str, required = True, help = 'Directory containing three folders of source data.')
@click.option('--output', type = str, help = 'Directory to store output files. The input is optional.')
@click.option('--codeql-relative', type = str, required = True, help = 'Relative path to truncate from file names in the CodeQL data.')
@click.option('--clojure-relative', type = str, default = "", help = 'Relative path to truncate from file names in the Clojure data.')
@click.option('--coccinelle-relative', type = str, required = True, help = 'Relative path to truncate from file names in the Coccinelle data.')
@click.option('--exclude', help = "Enter names of the tools that you wish to exclude from comparison. For instance, there are two folders in your input directory. One is named clojure_data, and the other is named clojuredata. Entering 'clojure'(case sensitive) will exclude both folders from the search. If there are more than one key word, be sure to wrap the input in parentheses, and seperate the keys with spaces or commas. Avoid leading or trailing spaces when there is only one key")
def parse_arguments(input, output, codeql_relative, clojure_relative, coccinelle_relative, exclude):
    """The Atoms Comparison tool gathers and compares output from three sources previously developed by the team. Please refer to the README page for more info on each source. To use this project, you will enter four mandatory and two optional options. The usage of each option is listed below."""

    exclude_list = []
    if exclude:
        exclude_list = re.split(r'[ ,]+', exclude)

    try:
        checked_output_path = validate_paths(input, output, exclude_list)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    print(f"{TEXT['magenta']}ATTENTION:{TEXT['reset']} Input found to include: {input_list}")
    
    input_list_size = len(input_list)
    def check_list_size(input_list_size):
        if input_list_size < 2:
            expected_inputs = []
            if exclude:
                for key in source_mapping:
                    if exclude and (not exclude in key):
                        expected_inputs.append(key)
            else:
                expected_inputs = source_mapping.keys()
            
            if not expected_inputs:
                raise InsufficientInputSize(f"{TEXT['red']}Error:{TEXT["reset"]} Check your --exclude input, or the source_mappings in cli.py, there does not exist any folder inside your input directory that satisifies as input data.")
            if input_list_size == 1:
                raise InsufficientInputSize(f"{TEXT['red']}Error:{TEXT["reset"]} List size is one, currently contains {input_list}. All attainable input folders, according to the source_mappings: {source_mapping.keys()}, and your --exclude option, may include the following: {expected_inputs}.")
            else:
                raise InsufficientInputSize(f"{TEXT['red']}Error:{TEXT["reset"]} List size is empty. All attainable input folders, according to the source_mappings: {source_mapping.keys()}, and your --exclude option, may include the following: {expected_inputs}.")
        else:
            pass

    try:
        check_list_size(input_list_size)
    except InsufficientInputSize as e:
        print(e)
        exit(1)
    
    ### CHANGE
    # relative path
    relative_mapping = {
        "codeQL_data": codeql_relative,
        "clojure_data": clojure_relative,
        "coccinelle_data": coccinelle_relative,
    }
    
    for item in input_list:
        func = source_mapping[item][1]
        func(Path(input, item), relative_mapping.get(item))

    merge(checked_output_path)
    
    print(TEXT['green'] + "Process completed, check output at: " + TEXT['reset'] + TEXT['bold'] + str(checked_output_path) + TEXT['reset'])
