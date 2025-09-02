from utils.etl import *
from utils.db_utils import *

def main():


    state = {}


    while True: 
        
        print("\n\tMain Menu:")
        print("0 - Exit App")
        print("1 - Extract")
        print("2 - Transform")
        print("3 - Load")

        


        x = input("Please select an option: \n")

        if x.isdigit(): # again ensures the user can only enter numbers
            x = int(x)
            if x == 0:
                print("Closing down...")
                close_db_connection(cursor, conn)
                exit() #exit the loop after printing closing down
                time.sleep(2) #delay the clearing of the terminal
                clr_terminal()
            elif x == 1:
                state["raw"] = extract()
                print(state)
                print("The data has been extracted and is now ready for transformation...")
            elif x == 2:
                print(state)
                state["transformed"] = transform(state["raw"])
                print(state)
            elif x == 3:
                print(state)
                state["transformed"] = transform(state["raw"])
                print(state)
                branches, transactions, products = normalisation(state["transformed"])
                print(state)
                load(branches, transactions, products)


        else:
            print("Invalid Input. Enter an integer like 1 or 2.")



def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

if __name__ == '__main__':
    main()