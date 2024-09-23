### Instruction
1. Open the terminal in the project directory, and set up python virtual environment if needed.

2. To build the tool, enter the following in terminal.

> pip install --editable .

3. Everytime before you run the tool, ensure that there are at least two sub folders containing the source data for comparison. Otherwise, error will occur as this comparison tool is intended for two or more sources.

4. Run the tool via the command below. By default, a folder named "output" will be created if not so.

> compare \
--input "/home/usr/Documents/Atoms of Confusion/atoms-comparison-tool" \
--output "/home/usr/Documents/Atoms of Confusion/atoms_comparsion_tool_cli/output1" \
--codeql-relative "" \
--clojure-relative "/Users/anuraagpandhi/VSCode/AtomFinder/atom-finder/GitSourceCode/git/" \
--coccinelle-relative "/home/ubuntu/atoms/projects/git/" \
--exclude ""

5. After successful execution, check the folder indicated by the bolded directory printed as the last line. 
