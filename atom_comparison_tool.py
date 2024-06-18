#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os

codeQL_directory = "./codeQL_data"
clojure_directory = "./clojure_data"
coccinelle_directory = "./coccinelle_data"
dataframes = {}


# In[2]:


# Load CodeQL .sarif files and store them in dataframes dictionary

import json
from pathlib import Path

for filename in os.listdir(codeQL_directory):
    if filename.endswith('.sarif'):
        file_path = os.path.join(codeQL_directory, filename)
        dataframe_key = filename[:-6]
        pt = Path(file_path)
        file_content = pt.read_text()
        json_value = json.loads(file_content)
        p = pd.DataFrame(columns = ["Type", "File", "Line", "CQL", "CQL_Column", "CQL_CodeQL"])
        rows = []
    print("Loading:", filename)
    # These are the index paths of the data we are looking for. Each is located inside nested dictionaries.
    for i in range(len(json_value["runs"][0]["results"])):
        s = pd.Series({
            "Type": filename[:-6],
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
    p["File"] = p["File"].str.split('/').str[-1]
    dataframes[dataframe_key] = p
    
print("DataFrame Names:", dataframes.keys())
# for i in dataframes.values():
#     display(i)


# In[3]:


# Load Clojure dataset

clojure_master = pd.read_csv("./clojure_data/atomsClojure.csv")
# Get only the filename, removing the path
clojure_master['file'] = clojure_master['file'].str.split('/').str[-1]
# display(clojure_master)
print("Clojure Types:", clojure_master["atom"].unique())


# In[4]:


# Prepare Clojure dataset for merge

name_mapping = {
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

clojure_master['atom'] = clojure_master['atom'].map(name_mapping)
clojure_master.rename(columns = {
    'atom': 'Type',
    'file': 'File',
    'line': 'Line',
    'code': 'CLJ_Code'
}, inplace=True)

clojure_master["CLJ"] = '+'

clojure_master.drop(columns = ['offset'], inplace = True)
# display(clojure_master)


# In[5]:


# Merge Clojure and CodeQL dataframes

for key, df in dataframes.items():
    k = pd.merge(clojure_master[clojure_master["Type"] == key], df, on = ['File', 'Type', 'Line'], how = 'outer')
    k = k[["Type", "File", "Line", "CLJ", "CQL", "CLJ_Code", "CQL_Column", "CQL_Code"]]
    k = k.drop_duplicates(subset = ["Type", "File", "Line", "CLJ", "CQL"], keep = 'first')
    k['CLJ'] = k['CLJ'].fillna('-')
    k['CQL'] = k['CQL'].fillna('-')
    dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)
    print(f"Merged DataFrame for {key}:")
#     display(dataframes[key].head())


# In[6]:


# Load Coccinelle dataframes

coccinelle_dataframes = {}
for filename in os.listdir(coccinelle_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(coccinelle_directory, filename)
        dataframe_key = filename[:-4]
        p = pd.read_csv(file_path)
        p.columns = ["Type", "File", "Line", "CNL_Column", "CNL_Code"]
        p["File"] = p["File"].str.split('/').str[-1]
        p["CNL"] = '+'
        coccinelle_dataframes[dataframe_key] = p
print(coccinelle_dataframes.keys())

coccinelle_mapping = {
    'post-increment': 'postIncr',
    'assignment-as-value': 'assignment_as_value',
    'conditional' : 'conditional',
    'pre-increment': 'preIncr',
    'comma-operator': 'comma_atoms',
}


for i in coccinelle_dataframes.values():
    i['Type'] = i['Type'].map(coccinelle_mapping)
#     display(i)


# In[7]:


# Merge Coccinelle DataFrames

for i in coccinelle_dataframes.values():
    key = i.loc[0, "Type"]
    toMerge = dataframes[key]
    k = pd.merge(toMerge, i, on = ['File', 'Type', 'Line'], how = 'outer')
    k['CLJ'] = k['CLJ'].fillna('-')
    k['CQL'] = k['CQL'].fillna('-')
    k['CNL'] = k['CNL'].fillna('-')
    # Reordering columns
    k = k[["Type", "File", "Line", "CLJ", "CQL", "CNL", "CLJ_Code", "CQL_Column", "CQL_Code", "CNL_Column", "CNL_Code"]]
    k = k.drop_duplicates(subset = ["Type", "File", "Line", "CLJ", "CQL", "CNL"], keep = 'first')
    # Float type For consistency with CQL_Column, which is forced as a float because of NaN values
    k["CQL_Column"] = k["CQL_Column"].astype(float)
    dataframes[key] = k.sort_values(by = ["File", "Line"]).reset_index().drop("index", axis = 1)
    print(f"Merged DataFrame for {key}:")
#     display(dataframes[key].head())


# In[8]:


# Output merged CSVs to output_directory

output_directory = 'output'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

for key, df in dataframes.items():
    file_name = f'{key}_comparison.csv'
    path = os.path.join(output_directory, file_name)
    df.to_csv(path, index = False)
    print(f"DataFrame '{key}' has been saved to {file_name}.")


# In[ ]:




