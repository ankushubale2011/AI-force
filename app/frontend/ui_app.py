import tkinter as tk
from tkinter import messagebox
import psycopg2

# Database connection details (replace with actual values)
db_connection_details = {
    "host": "localhost",
    "port": 5432,
    "database": "test_db",
    "user": "postgres",
    "password": "your_password"
}

def check_user_in_db(user_name):
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(**db_connection_details)
        cur = conn.cursor()

        # Read SQL query from backend file
        with open("../backend/check_user.sql", "r") as sql_file:
            query = sql_file.read()

        # Execute query
        cur.execute(query, {"user_name": user_name})
        result = cur.fetchone()

        cur.close()
        conn.close()

        # Check result
        if result and result[0] > 0:
            return True
        else:
            return False

    except Exception as e:
        messagebox.showerror("Database Error", f"Error connecting to database:\n{e}")
        return False

def on_submit():
    user_name = entry_name.get().strip()
    if not user_name:
        messagebox.showwarning("Input Error", "Please enter your name.")
        return

    exists = check_user_in_db(user_name)
    if exists:
        messagebox.showinfo("Result", "User search successful")
    else:
        messagebox.showinfo("Result", "User does not exist")

# Tkinter UI setup
root = tk.Tk()
root.title("User Verification App")

tk.Label(root, text="Enter your name:").pack(pady=5)
entry_name = tk.Entry(root)
entry_name.pack(pady=5)

submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=10)

root.mainloop()