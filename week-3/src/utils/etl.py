import csv
import pandas as pd
import time
import os
import uuid
import hashlib
from datetime import datetime
from db_utils import *

def fix_df_structure(df):

    df['Date/Time'] = df['Payment Type']
    df['Card Number'] = df['Branch']
    df['Payment Type'] = df['Price']
    df['Branch'] = df['Qty']

    return df

def split_items(df):

    print("Original DF:\n", df)

    # Split Drink into separate columns
    order_items = df['Drink'].str.split(", ", expand=True)
    df['Drink'] = order_items[0]
    df['Qty'] = order_items[1].astype(int)
    df['Price'] = order_items[2].str.replace('£','').astype(float)

    # Print the cleaned DataFrame to check
    print("After splitting Drink:\n", df)

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
    print(f"\nMissing values per column after dropping PII:\n{missing_values}")

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

def normalisation(df):
    """
    Normalising the data in preparation for loading into the MySQL Database.
    Ensuring that we account for any branches or products that have been already been added into the database to stop duplicates
    """

    print(df)

    
    branches = [] 
    products = []
    transactions = []

    seen_branches = {}
    seen_products = {}

    for idx , row in df.iterrows():
        branch_name = row['Branch']
        if branch_name not in seen_branches:
            branch_id = generate_guid(branch_name)
            seen_branches[branch_name] = branch_id
            branches.append({
                    "branch_id": branch_id,
                    "branch_name": branch_name
                })
        else:
            branch_id = seen_branches[branch_name]

        product_name = row['Drink']
        price = row['Price']
        if product_name not in seen_products:
            product_id = generate_guid(product_name, price)
            seen_products[product_name] = product_id
            products.append({
                    "product_id": product_id,
                    "product_name": product_name,
                    "Price": price
                })
        else:
            product_id = seen_products[product_name]

        transaction_id = generate_guid(branch_id, row['Date'], row['Time'], row['Price']* row['Qty'] , row['Payment Type'])

        total = row['Price']* row['Qty']
        rounded_total = round(total, 2)
        print(rounded_total)

        transactions.append({
                "transaction_id": transaction_id,
                "branch_id": branch_id,
                "date": row['Date'],
                "time": row['Time'],
                "total": total,
                "trans_type": row['Payment Type']
            })

    print(transactions)

    return branches, transactions, products


def extract():
    """
    Extracting the data from the CSV file into a DataFrame for Transformation.
    Returning the DataFrame for further use.
    """

    df = pd.read_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-3\data\data.csv", skipinitialspace=True) #read file and save to local memory


    return df


def transform():
    """
    Cleaning the DataFrame by removing PII columns, checking for and filling any missing values.
    Adding the GUIDs
    Returning the cleaned DataFrame.
    """
    df = extract()
    df = fix_df_structure(df)
    df = split_items(df)
    df = split_datetime(df)
    df = remove_pii(df)
    df, missing_values  = check_for_missing_vals(df)
    df = fill_missing_vals(df, missing_values)
    branches, products, transactions = normalisation(df)


    return branches, products, transactions




def load(branches, products, transactions):
    """
    Saving to CSV for now before migrating to the database. 
    """

    populate_database()

    try:

        # Preparing our data for batch insertion
        branch_values = [(d["branch_id"], d["branch_name"]) for d in branches]

        transaction_values = [
            (t["transaction_id"], t["branch_id"], t["date"], t["time"], t["total"], t["trans_type"])
            for t in transactions
        ]

        product_values = [
            (p["product_id"], p["product_name"], p["price"])
            for p in products
        ]

        branch_query = '''
        INSERT IGNORE INTO branches (branch_id, branch_name)
        VALUES (%s, %s);
        '''
        cursor.executemany(branch_query, branch_values)

        transaction_query = '''
        INSERT IGNORE INTO transactions (transaction_id, branch_id, date, time, total, trans_type)
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
        cursor.executemany(transaction_query, transaction_values)

        product_query = '''
        INSERT IGNORE INTO products (product_id, product_name, price)
        VALUES (%s, %s, %s);
        '''
        cursor.executemany(product_query, product_values)

        conn.commit()

        '''Having them in the same block of code and only commting once at the end ensures that this part is atomic either they all work \
           nothing is inserted.
        '''
    
    except Exception as e:
        conn.rollback()


    
