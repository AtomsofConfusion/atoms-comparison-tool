import sys
from cli import parse_args, validate_paths
from comparsion import compare_and_output

def main():
    args = parse_args(sys.argv[1:])
    print(args.output_path)
    try:
        checked_input_path, checked_output_path = validate_paths(args.input_path, args.output_path)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)

    print(f"Input path: {checked_input_path}")
    print(f"Output path: {checked_output_path}")
    print(f"Clojure_path is:{args.clojure_path}")
    
    compare_and_output(checked_input_path, checked_output_path, args.clojure_path)

    print("Process completed, check output at: ", checked_output_path)

if __name__ == "__main__":
    main()
