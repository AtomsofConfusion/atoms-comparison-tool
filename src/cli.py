from pathlib import Path
import click

@click.command
@click.argument('input_path', type = click.Path())
@click.argument('output_path', nargs = -1, type = click.Path())
@click.argument('clojure_path', type = click.STRING)
@click.argument('codeql_path', type = click.STRING)
@click.argument('coccinelle_path', type = click.STRING)
def parse_args(input_path, output_path, clojure_path, codeql_path, coccinelle_path):
    if len(output_path)==0:
        output_path = None
    else:
        output_path = output_path[0]
    return input_path, output_path, clojure_path, codeql_path, coccinelle_path

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