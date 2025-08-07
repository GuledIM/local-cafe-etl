import csv
import pandas as pd
import time
import os

def main():

    while True: 
        
        print("\n\tMain Menu:")
        print("0 - Exit App")
        print("1 - Extract & Transform")
        print("2 - Load")


        x = input("Please select an option: \n")

        if x.isdigit(): # again ensures the user can only enter numbers
            x = int(x)
            if x == 0:
                print("Closing down...")
                exit() #exit the loop after printing closing down
                time.sleep(2) #delay the clearing of the terminal
                clr_terminal()
            elif x == 1:
                extract_transform()
                # time.sleep(5)
                # clr_terminal()
            elif x == 2:
                load()
        else:
            print("Invalid Input. Enter an integer like 1 or 2.")

def extract():
    """
    Extracting the data from the CSV file into a DataFrame for Transformation.
    Returning the DataFrame for further use.
    """

    df = pd.read_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-1\data\data.csv") #read file and save to local memory


    return df
    
    
def transform(df):
    """
    Cleaning the DataFrame by removing PII columns and checking for missing values.
    Returning the cleaned DataFrame.
    """

    #Remove PII
    df.drop(["Customer Name", "Card Number"], axis=1, inplace=True)

    #Check for null values
    missing_values = df.isnull().sum()
    print(f"\nMissing values per column after dropping PII:{missing_values}")

    #Filling in the missing or null values

    if missing_values.any():
        df['Drink'].fillna('Unknown', inplace=True)
        df['Qty'].fillna(0, inplace=True)
        df['Price'].fillna(df['Price'].mean(), inplace=True)
        df['Branch'].fillna('Unknown', inplace=True)
        df['Payment Type'].fillna('Unknown', inplace=True)
        #Date to be added later
    
    return df


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




    


def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

if __name__ == '__main__':
    main()