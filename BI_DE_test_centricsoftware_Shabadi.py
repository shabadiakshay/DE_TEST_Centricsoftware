#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from typing import List, Dict, Any

def check_duplicates(df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
    """
    Check for duplicates in a dataframe based on the specified columns.

    Args:
        df (pd.DataFrame): The input dataframe.
        columns (List[str]): The list of columns to check for duplicates.

    Returns:
        Dict[str, Any]: A dictionary containing the count of duplicate cases and a dataframe with group count of duplicate rows.
    """
    # Input validation
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The first argument must be a pandas DataFrame.")
    if not isinstance(columns, list):
        raise ValueError("The second argument must be a list of column names.")
    if not all(isinstance(col, str) for col in columns):
        raise ValueError("All elements in the columns list must be strings.")
    if not all(col in df.columns for col in columns):
        raise ValueError("All columns specified must exist in the dataframe.")
    
    # Handle edge case: Empty dataframe
    if df.empty:
        return {"count": 0, "samples": pd.DataFrame(columns=columns + ['number_of_duplicates'])}

    # Group by the specified columns and count occurrences
    grouped = df.groupby(columns).size().reset_index(name='number_of_duplicates')
    
    # Filter groups with more than one occurrence (indicating duplicates)
    duplicates = grouped[grouped['number_of_duplicates'] > 1]

    return {
        "count": duplicates.shape[0],
        "samples": duplicates
    }

# Test the function with the provided dataset
df_1 = pd.DataFrame(
    data=[
        ['A','a', 'x', 1],
        ['A','b', 'x', 1],
        ['A','c', 'x', 1],
        ['B','a', 'x', 1],
        ['B','b', 'x', 1],
        ['B','c', 'x', 1],
        ['A','a', 'y', 1],
    ],
    columns=['col_1', 'col_2', 'col_3', 'col_4']
)

# Checking duplicates for different combinations of columns
result_1 = check_duplicates(df_1, ['col_1'])
result_2 = check_duplicates(df_1, ['col_1', 'col_2'])
result_3 = check_duplicates(df_1, ['col_1', 'col_2', 'col_3'])

print("Result for ['col_1']:", result_1)
print("Result for ['col_1', 'col_2']:", result_2)
print("Result for ['col_1', 'col_2', 'col_3']:", result_3)


# In[ ]:




