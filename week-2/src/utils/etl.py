import csv
import pandas as pd
import time
import os
import uuid
import hashlib
from datetime import datetime


def extract():
    """
    Extracting the data from the CSV file into a DataFrame for Transformation.
    Returning the DataFrame for further use.
    """

    df = pd.read_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-2\data\data.csv") #read file and save to local memory


    return df
    
def split_datetime(df):

    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%d/%m/%Y %H:%M')

    # split into separate columns
    df['Date'] = df['Date/Time'].dt.date
    df['Time'] = df['Date/Time'].dt.time


    df.drop("Date/Time", axis=1, inplace=True)  


    return df



def remove_pii(df):
    #Remove PII
    df.drop(["Customer Name", "Card Number"], axis=1, inplace=True)

    return df

def check_for_missing_vals(df):
    #Check for null values
    missing_values = df.isnull().sum()
    print(f"\nMissing values per column after dropping PII:{missing_values}")

    return df , missing_values


def fill_missing_vals(df, missing_values):

    #Filling in the missing or null values

    if missing_values.any():
        df['Drink'].fillna('Unknown', inplace=True)
        df['Qty'].fillna(0, inplace=True)
        df['Price'].fillna(df['Price'].mean(), inplace=True)
        df['Branch'].fillna('Unknown', inplace=True)
        df['Payment Type'].fillna('Unknown', inplace=True)
        #Date to be added later
    
    return df

def generate_guid(*args):
    hash_input = '|'.join(str(arg).strip().lower() for arg in args) #Normalising our inputs 
    hash_digest = hashlib.md5(hash_input.encode()).hexdigest()
    return str(uuid.UUID(hash_digest[:32]))



def transform():
    """
    Cleaning the DataFrame by removing PII columns, checking for and filling any missing values.
    Adding the GUIDs
    Returning the cleaned DataFrame.
    """
    df = extract()
    df = split_datetime(df)
    df = remove_pii(df)
    df, missing_values  = check_for_missing_vals(df)
    df = fill_missing_vals(df, missing_values)

    



def load(cleaned_data):
    """
    Saving to CSV for now before migrating to the database. 
    """

    cleaned_data.to_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-1\data\output.csv", index=False)



def etl():
    """
    Combining the Extract, Transform, and Load function into one concurrent function.
    """

    df = extract() #Run the extract function and save the DataFrame to a variable

    cleaned_data = transform(df) #Run the DataFrame through the transform function to then save as a new variable.

    print(cleaned_data) #Check that the data has been processed as wanted

    print("Extraction and Transformation complete")



transform()
    
