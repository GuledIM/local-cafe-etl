from utils.etl import *

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
                extract()
                print("The data has been extracted and is now ready for transformation...")
            elif x == 2:
                transform()
            elif x == 3:
                load()
        else:
            print("Invalid Input. Enter an integer like 1 or 2.")



def clr_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')#clear terminal

if __name__ == '__main__':
    main()