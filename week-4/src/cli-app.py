from utils.etl import *
from utils.db_utils import *

def main():

    conn, cursor = db_connection()
    check_tables(conn, cursor)

    clr_terminal()


    state = {}


    while True: 
        
        print("\n\tETL Menu:")
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
                print("The data has been extracted and is now ready for transformation...")
            elif x == 2:
                state["transformed"] = transform(state["raw"])
            elif x == 3:
                branches, transactions, products = normalisation(state["transformed"])
                load(conn, cursor, branches, transactions, products)


        else:
            print("Invalid Input. Enter an integer like 1 or 2.")



def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

if __name__ == '__main__':
    main()