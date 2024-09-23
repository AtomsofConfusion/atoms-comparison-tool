logic:
1. Check input path and read from input path
2. Collect what is in the input folder based on the mapping. For instance, if there is a folder called "codeQL_data", we check whether the input_mapping already knew that key. 
3. If yes, then we check whether that input exist, we check that source folder with a specialized method just from input_validation.py. Return false if the criteria isn't met. For instance, Clojure contains no .csv files or that CodeQL contains no .sarif files.
4. Remove terms from the input_list whenever that input_source returned false. Now raise a warning if the input_list size is only one or zero.
5. Create the empty dataframe such that later we are going to add data from each source into it one by one. Then start looping through the input_list and call the methods from comparison.py.


### Instruction
1. Open the terminal in the project directory.

2. Download the Python libraries using "pip install -r requirement.txt".

3. Ensure that there are at least two sub folders containing the source data for comparison.

4. To build the tool, enter the following in terminal. Note that the output directory can be omitted.

> pip install --editable .

5. Run the tool via the command below. Note that the output directory can be omitted, and in this case the output is where this folder locates in your system. By default, a folder named "output" will be created if not so.

> compare \
--input "/home/usr/Documents/Atoms of Confusion/atoms-comparison-tool" \
--output "/home/usr/Documents/Atoms of Confusion/atoms_comparsion_tool_cli/output1" \
--codeql-relative "" \
--clojure-relative "/Users/anuraagpandhi/VSCode/AtomFinder/atom-finder/GitSourceCode/git/" \
--coccinelle-relative "/home/ubuntu/atoms/projects/git/" \
--exclude ""

6. After successful execution, check the folder indicated by the bolded directory in the terminal. 

### Possible Warnings

