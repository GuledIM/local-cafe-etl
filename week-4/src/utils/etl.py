import csv
import pandas as pd
import time
import os
import uuid
import hashlib
from datetime import datetime
from utils.db_utils import *

def fix_df_structure(df):

    df['Date/Time'] = df['Payment Type']
    df['Card Number'] = df['Branch']
    df['Payment Type'] = df['Price']
    df['Branch'] = df['Qty']

    return df

def split_items(df):
    print("Original DF:\n", df)

    # Split Drink column
    order_items = df["Drink"].str.split(", ", expand=True)

    # Ensure the split has at least 3 columns
    while order_items.shape[1] < 3:
        order_items[order_items.shape[1]] = None  # add missing column(s)

    # Rename columns
    order_items = order_items.rename(columns={0: "Drink", 1: "Qty", 2: "Price"})

    # Assign back the data
    df["Drink"] = order_items["Drink"]
    df["Qty"] = pd.to_numeric(order_items["Qty"], errors="coerce").fillna(0).astype(int)
    df["Price"] = (
        order_items["Price"]
        .str.replace("£", "", regex=False)
        .astype(float)
        .fillna(0.0)
    )

    print("After splitting Drink:\n", df)
    return df
    
def split_datetime(df):
    print("Date/Time column values before parsing:\n", df['Date/Time'].head(10))  # check first 10

    df['Date/Time'] = pd.to_datetime(
        df['Date/Time'], 
        format='%d/%m/%Y %H:%M', 
        errors='coerce'  # invalid ones become NaT instead of breaking
    )

    df['Date'] = df['Date/Time'].dt.strftime("%Y-%m-%d")
    df['Time'] = df['Date/Time'].dt.strftime("%H:%M:%S")

    print("After splitting datetime:\n", df.head(10))
    return df



def remove_pii(df):

    df.drop(["Customer Name", "Card Number"], axis=1, inplace=True, errors="ignore")
    
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
                    "price": price
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


    return branches, transactions, products


def extract():
    """
    Extracting the data from the CSV file into a DataFrame for Transformation.
    Returning the DataFrame for further use.
    """

    df = pd.read_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-4\data\data.csv", skipinitialspace=True) #read file and save to local memory


    return df


def transform(df):
    """
    Cleaning the DataFrame by removing PII columns, checking for and filling any missing values.
    Adding the GUIDs
    Returning the cleaned DataFrame.
    """
    df = remove_pii(df)
    df = fix_df_structure(df)
    df = split_items(df)
    df = split_datetime(df)
    df, missing_values  = check_for_missing_vals(df)
    df = fill_missing_vals(df, missing_values)


    return df




def load(branches, transactions, products):
    """
    Saving to Database. 
    """


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
           or nothing is inserted.
        '''
    
    except Exception as e:
        conn.rollback()


