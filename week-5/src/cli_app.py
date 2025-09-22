from utils.etl import *
from utils.db_utils import *

def cli_app(conn, cursor):



    clr_terminal()


    state = {}


    while True: 
        
        print("\n\tETL Menu:")
        print("0 - Return to Main Menu")
        print("1 - Extract")
        print("2 - Transform")
        print("3 - Load")

        


        x = input("Please select an option: \n")

        if x.isdigit(): # again ensures the user can only enter numbers
            x = int(x)
            if x == 0:
                clr_terminal()
                
                return
            elif x == 1:
                state["raw"] = extract()
                print("The data has been extracted and is now ready for transformation...")
            elif x == 2:
                state["transformed"] = transform(state["raw"])
                print("The data has been transformed and is now ready for loading...")
            elif x == 3:
                load(conn, cursor, state["transformed"])
                print("The data has been successfully loaded!")


        else:
            print("Invalid Input. Enter an integer like 1 or 2.")



def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

