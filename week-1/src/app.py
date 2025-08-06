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

    df = pd.read_csv(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-1\data\data.csv") #read file and save to local memory


    return df
    
    
def transform(df):
    #Remove PII
    df.drop(["Customer Name", "Card Number"], axis = 1, inplace = True)

    return df


    #Check for null values 

def extract_transform():

    df = extract()
    cleaned_data = transform(df)

    print(cleaned_data)


    print("Extraction and Transformation complete")

#Load function
    


def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

if __name__ == '__main__':
    main()