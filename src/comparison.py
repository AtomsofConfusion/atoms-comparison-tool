import pandas as pd
import json
import re
from pathlib import Path
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

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

which_columns = []

### CHANGE
# plan: add more functions here in case more tools are introduced to comparison
def compare_codeql(path, relative):
    which_columns.append('CQL')

    for file_path in path.glob('*.sarif'):
        file_content = file_path.read_text()
        filename = Path(file_path).stem
        dataframe_key = filename
        json_value = json.loads(file_content)
        p = pd.DataFrame(["Type", "File", "Line", "CQL", "CQL_Column", "CQL_Code"])
        rows = []
        for i in range(len(json_value["runs"][0]["results"])):
            s = pd.Series({
                "Type": filename,
                "File": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["artifactLocation"]["uri"], 
                "Line": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["region"]["startLine"],
                "CQL": '+',
                "CQL_Column": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["region"].get("startColumn", None),
                "CQL_Code": json_value["runs"][0]["results"][i]["locations"][0]["physicalLocation"]["contextRegion"]["snippet"]["text"]
            })
            rows.append(s)
        p = pd.concat(rows, axis=1).T
        
        p["CQL_Code"] = p["CQL_Code"].apply(lambda x: '\n'.join(x) if isinstance(x, list) else x)
        p["File"] = p["File"].apply(lambda x: '\n'.join(x) if isinstance(x, list) else x)
        p["File"] = p["File"].apply(lambda x: re.sub(relative, '', x, count=1))
        p["CQL_Column"] = p["CQL_Column"].astype(float)
        toMerge = dataframes[dataframe_key]
        k = pd.merge(toMerge, p, on = ['File', 'Type', 'Line'], how = 'outer')
        k['CQL'] = k['CQL'].fillna('-')
        dataframes[dataframe_key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)

def compare_clojure(path, relative):
    which_columns.append('CLJ')

    for file_path in Path(path).glob('*.csv'):
        p = pd.read_csv(file_path)
        p["file"] = p["file"].apply(lambda x: re.sub(relative, '', x, count=1))
        p["CLJ"] = '+'
        p.rename(columns = {
            'atom': 'Type',
            'file': 'File',
            'line': 'Line',
            'code': 'CLJ_Code'
        }, inplace=True)
        p.drop(columns = ['offset'], inplace = True)
        p["Type"] = p["Type"].map(combined_mapping)

        for key, df in dataframes.items():
            k = pd.merge(p[p["Type"] == key], df, on = ['File', 'Type', 'Line'], how = 'outer')
            k['CLJ'] = k['CLJ'].fillna('-')
            dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)

def compare_coccinelle(path, relative):
    which_columns.append('CNL')

    coccinelle_dataframes = {}
    for file_path in path.glob('*.csv'):
        filename = Path(file_path).stem
        dataframe_key = filename
        p = pd.read_csv(file_path)
        p.columns = ["Type", "File", "Line", "CNL_Column", "CNL_Code"]

        p["File"] = p["File"].apply(lambda x: re.sub(relative, '', x, count=1))
        p["CNL"] = '+'

        coccinelle_dataframes[dataframe_key] = p        

    for i in coccinelle_dataframes.values():
        i['Type'] = i['Type'].map(combined_mapping)
        key = i.loc[0, "Type"]
        toMerge = dataframes[key]
        k = pd.merge(toMerge, i, on = ['File', 'Type', 'Line'], how = 'outer')
        k['CNL'] = k['CNL'].fillna('-')
        dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)

def count_plus_specific_columns(row, columns):
    count = 0
    for col in columns:
        if col in row.index:
            count += (row[col] == '+')
    return count

def merge(output_path):
    for key, df in dataframes.items():
        df = df[df.apply(count_plus_specific_columns, axis=1, columns=which_columns) >= 2]
        file_name = f'{key}_comparison.csv'
        path = Path(output_path, file_name)
        df.to_csv(path, index = False)
        print(f"{key} has been saved to {file_name}.")
