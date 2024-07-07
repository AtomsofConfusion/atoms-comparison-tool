import sys
from src.cli import parse_args, validate_paths
from src.comparsion import compare_and_output

def main():
    input_path, output_path, clojure_path, codeQL_path, coccinelle_path = parse_args()
    try:
        checked_input_path, checked_output_path = validate_paths(input_path, output_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    print(f"Input path: {checked_input_path}")
    print(f"Output path: {checked_output_path}")
    print(f"Clojure_path is:{clojure_path}")
    
    compare_and_output(checked_input_path, checked_output_path, clojure_path)

    print("Process completed, check output at: ", checked_output_path)

if __name__ == "__main__":
    main()
