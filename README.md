# Localhost DB Explorer

A lightweight Python desktop application built with Tkinter to explore local MySQL databases. It provides a visual tree hierarchy of databases, tables, columns, and data types directly from a `localhost` environment.

## Features
* **Service Status Check:** Automatically checks if the local MySQL service is running on port 3306.
* **Service Control (macOS):** Allows starting the local MySQL environment (configured for XAMPP default paths) with standard system authentication prompts via AppleScript.
* **Database Browser:** Fetches and displays all available databases, tables, and column attributes (including data types) in a clean, hierarchical tree view.
* **System DB Filter:** Automatically filters out default internal system databases (like `information_schema`, `performance_schema`, etc.) for a cleaner view.

## Requirements
* Python 3.x
* PyMySQL (`pip install pymysql`)
* macOS (required for the integrated XAMPP startup command functionality)

## Usage
1. Make sure your local database server is accessible.
2. Run the script:
   ```bash
   python localhost_db_explorer.py
