import tkinter as tk
from tkinter import messagebox
from utils.etl import extract, transform, normalisation, load
from utils.db_utils import db_connection, close_db_connection, check_tables

conn, cursor = db_connection()
check_tables(conn, cursor)

def run_tkinter_app(conn, cursor):

    state = {}
    
    def exit_app(conn, cursor):

        close_db_connection(conn, cursor)

        root.destroy()

    def run_extract():
        state["raw"] = extract()
        messagebox.showinfo("Extract", "Extract complete")

    def run_transform():
        if "raw" not in state:
            messagebox.showerror("Error", "Run extract first")
            return
        state["transformed"] = transform(state["raw"])
        messagebox.showinfo("Transform", "Transform complete")

    def run_load():
        if "transformed" not in state:
            messagebox.showerror("Error", "Run transform first")
            return
        state["transformed"] = transform(state["raw"])
        load(conn, cursor, state["transformed"])
        messagebox.showinfo("Load", " Load complete")

    root = tk.Tk()
    root.title("ETL Controller")

    tk.Button(root, text="Run Extract", command=run_extract).pack(pady=10)
    tk.Button(root, text="Run Transform", command=run_transform).pack(pady=10)
    tk.Button(root, text="Run Load", command=run_load).pack(pady=10)
    tk.Button(root, text="Exit Application", command=lambda: exit_app(cursor, conn)).pack(pady=10)

    root.mainloop()