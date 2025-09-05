import mysql.connector
import os
from dotenv import load_dotenv
import csv

# DB functions 

load_dotenv(dotenv_path=r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-4\docker\.env") #specfify path to dotenv file
host_name = os.environ.get("MYSQL_HOST")
database_name = os.environ.get("MYSQL_DB")
user_name = os.environ.get("MYSQL_USER")
user_password = os.environ.get("MYSQL_PASSWORD")

print(host_name, database_name, user_name, user_password)


def db_connection():
    print('Opening connection...')
    try:
        conn = mysql.connector.connect(
            host=host_name,
            database=database_name, 
            user=user_name,
            password=user_password,
            connection_timeout=10
        )
        print("Connection established!")
        cursor = conn.cursor()
        print("Cursor opened...")


        return conn, cursor
        
    except Exception as e:
        print(f"Failed to connect: {e}")
        


def close_db_connection(conn, cursor):
    if cursor:
        cursor.close()
    print("Cursor closed.")
    if conn:
        conn.close()
    print("Database connection closed.")

def populate_database(conn, cursor):
    with open(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-4\docker\tables.sql", 'r') as tables_sql:
        tables_command = tables_sql.read()

        # Split into individual statements
        statements = [s.strip() for s in tables_command.split(';') if s.strip()]

        for stmt in statements:
            cursor.execute(stmt)

        conn.commit()

        # Confirmation that tables have been created
        print("All tables added!")

def check_tables(conn, cursor):
    required_tables = ["branches", "transactions", "products"]

    for table in required_tables:
        cursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_schema = DATABASE() AND table_name = %s;
        """, (table,))
        exists = cursor.fetchone()[0]

        if not exists:
            print(f"Tables does not exist. Populating database...")
            populate_database(conn, cursor)   # <-- your custom function that runs CREATE TABLE
            break
        else:
            print(f"Tables already exists")
