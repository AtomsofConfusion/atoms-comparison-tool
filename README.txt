### Instruction
1. Open the terminal in the project directory.

2. Download the Python libraries using "pip install -r requirement.txt".

3. By default, we assume the input folder already has three sub-folders, containing the source data for all three tools.

4. python src/__main__.py "/path/to/input/folder" "/path/to/output/folder". *The output path can be omitted. The default output path is in the project directory.

### Possible Errors
 - Permission to write to folder/file is denied. Possible solution: check if the path is valid. E.g. the folder does not exist and needs to be created.

### Modification Done to atom_comparsion_tool.py (line number is accorded to main.py)
1. Line 70, replacing orginal path with clojure_directory
2. 
