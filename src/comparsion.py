import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

import json
import re
from pathlib import Path

# orginally clojure_mapping
combined_mapping = {
    'pre-increment': 'preIncr',
    'operator-precedence': 'operator_precedence',
    'conditional': 'conditional',
    'preprocessor-in-statement': 'preprocessor_in_statement',
    'logic-as-control-flow': 'logic_as_control_flow',
    'type-conversion': 'type_conversion',
    'comma-operator': 'comma_atoms',
    'implicit-predicate': 'implicit_predicate',
    'post-increment': 'postIncr',
    'assignment-as-value': 'assignment_as_value',
    'repurposed-variable': 'repurposed_variable',
    'omitted-curly-braces' : 'omitted_curly_braces',
    'macro-operator-precedence' : 'macro_operator_precedence',
    'literal-encoding' : 'literal_encoding'
}

CLJnCQL = ["CLJ", "CQL"]
CLJnCNL = ["CLJ", "CNL"]
CQLnCNL = ["CQL", "CNL"]
all = ["CLJ", "CQL", "CNL"]

def count_plus_specific_columns(row, columns):
    return (row[columns] == '+').sum()

def compare_and_output(output_directory, codeql_system_path, clojure_system_path, coccinelle_system_path, whichtwo, codeQL_directory, clojure_directory, coccinelle_directory):
    print(whichtwo)
    dataframes = {}
    frame = pd.DataFrame(columns= ["Type", "File", "Line"])
    dataframes["preIncr"] = frame
    dataframes["operator_precedence"] = frame
    dataframes["conditional"] = frame
    dataframes["preprocessor_in_statement"] = frame
    dataframes["logic_as_control_flow"] = frame
    dataframes["type_conversion"] = frame
    dataframes["comma_atoms"] = frame
    dataframes["implicit_predicate"] = frame
    dataframes["postIncr"] = frame
    dataframes["assignment_as_value"] = frame
    dataframes["repurposed_variable"] = frame

    which_two = []

    if whichtwo == "CQLvCNL":
        which_two = CQLnCNL
    elif whichtwo == "CLJvCQL":
        which_two = CLJnCQL
    elif whichtwo == "CLJvCNL":
        which_two = CLJnCNL
    else:
        which_two = all

    # Load CodeQL .sarif files and store them in dataframes dictionary

    if whichtwo == "CQLvCNL" or whichtwo == "CLJvCQL" or whichtwo == "all":
        for file_path in Path(codeQL_directory).glob('*.sarif'):
            file_content = file_path.read_text()
            filename = Path(file_path).stem
            dataframe_key = filename
            json_value = json.loads(file_content)
            p = pd.DataFrame(["Type", "File", "Line", "CQL", "CQL_Column", "CQL_CodeQL"])
            rows = []
            # These are the index paths of the data we are looking for. Each is located inside nested dictionaries.
            for i in range(len(json_value["runs"][0]["results"])):
                s = pd.Series({
                    "Type": filename,
                    "File": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"], 
                    "Line": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["region"]["startLine"],
                    "CQL": '+',
                    "CQL_Column": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["region"].get("startColumn", None),
                    "CQL_Code": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["contextRegion"]["snippet"]["text"].splitlines()[2:-2],
                })
                rows.append(s)
            p = pd.concat(rows, axis=1).T
            
            # These lines convert these columns to string format
            p["CQL_Code"] = p["CQL_Code"].apply(lambda x: '\n'.join(x) if isinstance(x, list) else x)
            p["File"] = p["File"].apply(lambda x: '\n'.join(x) if isinstance(x, list) else x)
            p["File"] = p["File"].apply(lambda x: re.sub(codeql_system_path, '', x, count=1))
            p["CQL_Column"] = p["CQL_Column"].astype(float)
            dataframes[dataframe_key] = p

    if whichtwo == "CLJvCNL" or whichtwo == "CLJvCQL" or whichtwo == "all":
    # Load Clojure dataset and print the atoms
        clojure_master = pd.read_csv(clojure_directory)
        clojure_master["file"] = clojure_master["file"].apply(lambda x: re.sub(clojure_system_path, '', x, count=1))

    # Prepare Clojure dataset for merge

        clojure_master['atom'] = clojure_master['atom'].map(combined_mapping)
        clojure_master.rename(columns = {
            'atom': 'Type',
            'file': 'File',
            'line': 'Line',
            'code': 'CLJ_Code'
        }, inplace=True)

        clojure_master["CLJ"] = '+'

        clojure_master.drop(columns = ['offset'], inplace = True)

    # Merge Clojure and CodeQL dataframes
        for key, df in dataframes.items():
            k = pd.merge(clojure_master[clojure_master["Type"] == key], df, on = ['File', 'Type', 'Line'], how = 'outer')
            k['CLJ'] = k['CLJ'].fillna('-')
            dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)

    # Load Coccinelle dataframes

    if whichtwo == "CQLvCNL" or whichtwo == "CLJvCNL" or whichtwo == "all":
        coccinelle_dataframes = {}
        for file_path in Path(coccinelle_directory).glob('*.csv'):
            filename = Path(file_path).stem
            dataframe_key = filename
            p = pd.read_csv(file_path)
            p.columns = ["Type", "File", "Line", "CNL_Column", "CNL_Code"]
            p["File"] = p["File"].apply(lambda x: re.sub(coccinelle_system_path, '', x, count=1))
            p["CNL"] = '+'
            coccinelle_dataframes[dataframe_key] = p

        for i in coccinelle_dataframes.values():
            i['Type'] = i['Type'].map(combined_mapping)

        # Merge Coccinelle DataFrames

        for i in coccinelle_dataframes.values():
            key = i.loc[0, "Type"]
            toMerge = dataframes[key]
            k = pd.merge(toMerge, i, on = ['File', 'Type', 'Line'], how = 'outer')
            k['CNL'] = k['CNL'].fillna('-')
            dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)

    # Output merged CSVs to output_directory

    for key, df in dataframes.items():
        df = df.reindex(columns=["Type", "File", "Line", "CLJ", "CQL", "CNL", "CLJ_Code", "CQL_Column", "CQL_Code", "CNL_Column", "CNL_Code"])
        df = pd.DataFrame(df)
        if whichtwo == "CLJvCQL":
            df = df.drop(['CNL', 'CNL_Column', 'CNL_Code'], axis = 1)
        elif whichtwo == "CLJvCNL":
            df = df.drop(['CQL', 'CQL_Column', 'CQL_Code'], axis = 1)
            None
        elif whichtwo == "CQLvCNL":
            df = df.drop(['CLJ', 'CLJ_Code'], axis = 1)
        else:
            None
        
        df = df[df.apply(count_plus_specific_columns, axis=1, columns=which_two) >= 2]
        file_name = f'{key}_comparison.csv'
        path = Path(output_directory, file_name)
        df.to_csv(path, index = False)
        print(f"{key} has been saved to {file_name}.")
