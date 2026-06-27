import os
import socket
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import pymysql
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()


def get_databases():
    try:
        # Retrieve database configuration from environment variables (with local fallbacks)
        db_host = os.getenv("DB_HOST", "localhost")
        db_user = os.getenv("DB_USER", "root")
        db_password = os.getenv("DB_PASSWORD", "")

        # Connect to the server (no specific database selected to list all)
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            cursorclass=pymysql.cursors.Cursor  # Ensure standard cursor behavior
        )
        cursor = conn.cursor()

        # Clear treeview
        for i in tree.get_children():
            tree.delete(i)

        # 1. Fetch databases
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]

        for db_name in databases:
            # Skip system databases (optional)
            if db_name in ['information_schema', 'performance_schema', 'mysql', 'sys']:
                continue

            db_id = tree.insert("", "end", text=db_name, open=False, values=("Database",))

            # 2. Fetch tables for each database
            cursor.execute(f"SHOW TABLES FROM `{db_name}`")
            tables = [table[0] for table in cursor.fetchall()]

            # List comprehension: Extract table names from the query's list of tuples
            #
            # Equivalent verbose approach:
            # tables = []
            # for table in cursor.fetchall():
            #     name = table[0]
            #     tables.append(name)

            for table_name in tables:
                table_id = tree.insert(db_id, "end", text=table_name, values=("Table",))

                # 3. Fetch attributes (columns) for each table
                cursor.execute(f"DESCRIBE `{db_name}`.`{table_name}`")
                columns = cursor.fetchall()
                for col in columns:
                    tree.insert(table_id, "end", text=col[0], values=(f"Type: {col[1]}",))

        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Connection failed: {e}")


def check_mysql_status():
    # Retrieve port configuration or default to standard MySQL port
    db_port = int(os.getenv("DB_PORT", 3306))

    # Attempt to establish a connection to the MySQL port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)  # Short timeout to avoid hanging
        result = s.connect_ex(('127.0.0.1', db_port))
        if result == 0:
            status_label.config(text="Status: MySQL running", foreground="green")
            return True
        else:
            status_label.config(text="Status: MySQL stopped", foreground="red")
            return False


def start_mysql():
    # Retrieve the core command to execute from environment variables
    mysql_command = os.getenv("MYSQL_START_CMD", "/Applications/XAMPP/xamppfiles/bin/mysql.server start")

    # Wrap the command properly to avoid AppleScript parsing issues.
    # We use double quotes for the shell command inside AppleScript.
    auth_cmd = f'osascript -e "do shell script \\"{mysql_command}\\" with administrator privileges"'

    try:
        # Use subprocess instead of os.system for better reliability
        subprocess.run(auth_cmd, shell=True, check=True)

        messagebox.showinfo("Info", "Password request sent. Checking status...")
        # Wait 3 seconds to allow MySQL to start up
        root.after(3000, check_mysql_status)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start service: {e}")


# GUI setup
root = tk.Tk()
root.title("Localhost DB Explorer")
root.geometry("600x600")

# Status label
status_label = tk.Label(root, text="Status: Unknown", font=("Arial", 14, "bold"))
status_label.pack(pady=5)

# Button: Check status manually
refresh_status_btn = ttk.Button(root, text="Check Status Manually", command=check_mysql_status)
refresh_status_btn.pack(pady=5)

# Button: Start MySQL service
start_btn = ttk.Button(root, text="Start MySQL Service", command=start_mysql)
start_btn.pack(pady=(5, 5))  # Add slight top padding

# --- Separator ---
ttk.Separator(root, orient='horizontal').pack(fill='x', padx=10, pady=5)

# Header
label = tk.Label(root, text="MySQL Localhost Databases:", font=("Arial", 14, "bold"))
label.pack(pady=10)

# Treeview component
tree = ttk.Treeview(root, columns="Info")
tree.heading("#0", text="Name")
tree.heading("Info", text="Details")
tree.pack(fill="both", expand=True, padx=20, pady=10)

# Refresh button
btn = ttk.Button(root, text="Load Databases", command=get_databases)
btn.pack(pady=10)

# Automatically check MySQL status on startup
check_mysql_status()

root.mainloop()