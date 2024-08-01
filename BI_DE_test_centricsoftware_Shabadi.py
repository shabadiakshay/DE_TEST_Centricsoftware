#Imports and Configuration
import pandas as pd
from typing import List, Dict, Any
import logging
import unittest

# Configure logging
logging.basicConfig(level=logging.INFO)


# Main Functionality
def checking_for_duplicates(df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
    """
    Check for duplicates in a dataframe based on the specified columns.
    Args:
        df (pd.DataFrame): pandas DataFrame that contains the data to be checked for duplicates.
       columns (List[str]): list of the columns names to checking the duplicates within the DataFrame.
    Returns:
        Dict[str, Any]: A dictionary containing - count: number of cases where duplicates occur. and samples: dataframe with group count of duplicate rows for the columns.
    Raises:
       ValueError: If the input arguments are not valid.
    
    """
    logging.info("Starting the checking for the duplicates.")
    
    # Input validation -The function includes input validation to ensure the DataFrame and columns list are valid.
    if not isinstance(df, pd.DataFrame):
        logging.error("1st argument is not a pd.dataFrame.")
        raise ValueError("1st arguement needs be a pd.DataFrame.")
    
    if not isinstance(columns, list):
        logging.error("2nd argument is not a list.")
        raise ValueError("2 has to be list of column names.")
    
    if not all(isinstance(col, str) for col in columns):
        logging.error("all the elements in the columns list are not strings.")
        raise ValueError("All elements in columns list has to be strings.")
    
    if not all(col in df.columns for col in columns):
        logging.error(" all the columns specified not exist in the dataframe.")
        raise ValueError("All columns specified has to exist in dataframe.")
    
    # Handle edge case: Empty dataframe
    if df.empty:
        logging.info("The dataframe seems to be empty.")
        return {"count": 0, "samples": pd.DataFrame(columns=columns + ['number_of_duplicates'])}
    #If the df is empty, the function returns a dictionary with a count of 0 and an empty DataFrame with related columns

    # Group by the specified columns and count occurrences
    grouped = df.groupby(columns).size().reset_index(name='number_of_duplicates')
    # Groups the df by the specified columns and counts the occurrences of each group
    
    # Filter groups with more than one occurrence (showinf the duplicates)
    duplicates = grouped[grouped['number_of_duplicates'] > 1]
    #Filtering all the groups to include only those with more than one occurrence, which shows rhe duplicates.

    logging.info("\ncompleted the duplicate checking successfully.")
    
    return {
        "count": duplicates.shape[0],
        "samples": duplicates
    }



# Given Assignment Data for Testing
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

print("Sample DataFrame:")
print(df_1)


#Testing the Function
print("Checking the duplicates for ['col_1']:")
print(checking_for_duplicates(df_1, ['col_1']))
print("\nChecking the duplicates for combination of ['col_1', 'col_2']:")
print(checking_for_duplicates(df_1, ['col_1', 'col_2']))
print("\nChecking the duplicates for combination of ['col_1', 'col_2', 'col_3']:")
print(checking_for_duplicates(df_1, ['col_1', 'col_2', 'col_3']))

# Unit tests using unittest - defined to cover various scenarios, including no duplicates, duplicates in different column combinations, and invalid inputs.
class Unit_Test_Checking_Duplicates(unittest.TestCase):

    def setUp(self):
        self.df_1 = pd.DataFrame(
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
        #Same test dataFrame df_1 for use in test cases.

    def test1_no_duplicates(self):
        result = checking_for_duplicates(self.df_1, ['col_4'])
        self.assertEqual(result['count'], 0)
        """
        Checking for duplicates based on col_4 which has one value in the sample data ( 4th column) 
        so 1 group duplicates expected but test case is asserting as 0 group, so test case shoukd fail.
        """
        
    def test2_duplicates_col1(self):
        result = checking_for_duplicates(self.df_1, ['col_1'])
        self.assertEqual(result['count'], 1)
        self.assertTrue('number_of_duplicates' in result['samples'].columns)
        """
        Checking the duplicates based on col_1 where 'A' and 'B' exists more times,
        so 2 douplicate group is expected and verifies the same with the number_of_duplicates column in the result..
        but test case is asserted to check for 1 group, so test case should fail
        """
        
    def test3_duplicates_col1_col2(self):
        result = checking_for_duplicates(self.df_1, ['col_1', 'col_2'])
        self.assertEqual(result['count'], 1)
        self.assertTrue('number_of_duplicates' in result['samples'].columns)
        """
        Checking for duplicates based on combination of col_1 and col_2 where the combination ('A', 'a') appears multiple times.
        Expects a count of 1 duplicate group and verifies the same in the the number_of_duplicates column in  result.
        """
        
    def test4_duplicates_col1_col2_col3(self):
        result = checking_for_duplicates(self.df_1, ['col_1', 'col_2', 'col_3'])
        self.assertEqual(result['count'], 0)
        """
        Checks for duplicates based on combination of col_1, col_2, and col_3 where all combinations are unique.
        Expects a count of 0 duplicates.
        """
        
    def test5_invalid_dataframe(self):
        with self.assertRaises(ValueError):
            checking_for_duplicates("not_dataframe", ['col_1'])
        """Testing of the function with an invalid DataFrame input (a string).
        """
        
    def test6_invalid_columns(self):
        with self.assertRaises(ValueError):
            checking_for_duplicates(self.df_1, "not a list")
        """Testing the function with an invalid columns as input (a string instead of a list).
        """
        
    def test7_nonexistent_column(self):
        with self.assertRaises(ValueError):
            checking_for_duplicates(self.df_1, ['nonexistent_column'])
        """Testing the function with a column name that does not exist in the DataFrame.
        """

# Run the tests
unittest.main(argv=[''], verbosity=2, exit=False)

