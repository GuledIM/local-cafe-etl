import mysql.connector
import os
from dotenv import load_dotenv
import csv

# DB functions 

load_dotenv()
host_name = os.environ.get("MYSQL_HOST")
database_name = os.environ.get("MYSQL_DB")
user_name = os.environ.get("MYSQL_USER")
user_password = os.environ.get("MYSQL_PASSWORD")


def db_connection():
    print('Opening connection...')
    try:
        conn = mysql.connector.connect(
            host=host_name,
            database=database_name, 
            user=user_name,
            password=user_password
        )
        print("Connection established!")
        cursor = conn.cursor()
        print("Cursor opened...")


        return conn, cursor
        
    except Exception as e:
        print(f"Failed to connect: {e}")

conn,cursor=db_connection()

def close_db_connection(cursor, conn):
    if cursor:
        cursor.close()
    print("Cursor closed.")
    if conn:
        conn.close()
    print("Database connection closed.")

def populate_database():

    with open(r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-3\docker\tables.sql", 'r') as tables_sql:
        tables_command = tables_sql.read()

        cursor.execute(tables_command)

        conn.commit

        print("All tables added!")





populate_database()