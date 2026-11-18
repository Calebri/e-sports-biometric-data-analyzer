import sys

import pandas as pd

def open_csv(path: str) -> pd.DataFrame:
    """
    Read a .csv file and return a DataFrame.
    Catches errors and aborts the program.
    """

    try:
        with open(path, "r") as f:
            df = pd.read_csv(f)
            return df
    except Exception as e:
        print("Unexpected error when loading data file: " + str(e))
        sys.exit()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans a given DataFrame, then returns a clean DataFrame.
    """

    df = df.dropna(axis="index")
    
    return df

def get_clean_data(path: str, verbose: bool = True) -> pd.DataFrame:
    """
    Returns clean data read from a specified file.    
    """

    if verbose:
        print("Reading data...")

    df: pd.DataFrame = open_csv(path)

    if verbose:
        print("Successfully loaded data from file with " + str(df.shape[0]) + " rows.")
        print("Cleaning data...")

    df = clean_data(df)

    if verbose:
        print("Cleaned data to " + str(df.shape[0]) + " rows.")

    return df