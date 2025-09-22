import subprocess
import sys
from utils.db_utils import *
from flask_app import *
from tkinter_app import *
from cli_app import *


def main_menu():

    conn, cursor = db_connection()

    check_tables(conn, cursor)



    while True:
        print("\n=== ETL Application Launcher ===")
        print("1) Flask Web App")
        print("2) Tkinter GUI App")
        print("3) CLI App")
        print("4) Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            print("Launching Flask Web App...")
            # Run Flask app
            flask_app(conn, cursor)

        elif choice == "2":
            print("Launching Tkinter GUI App...")
            # Run Tkinter app
            run_tkinter_app(conn, cursor)
        elif choice == "3":
            print("Launching CLI App...")
            # Run CLI app
            cli_app(conn, cursor)
        elif choice == "4":
            print("Exiting. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main_menu()