import sqlite3
import os

# Create database folder if needed
if not os.path.exists("database"):
    os.makedirs("database")

# Connect to database
conn = sqlite3.connect("database/expense.db")
cursor = conn.cursor()

# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Create Expenses table
cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    expense_date TEXT NOT NULL,
    description TEXT
)
""")

# Check whether user_id already exists
cursor.execute("PRAGMA table_info(expenses)")
columns = [column[1] for column in cursor.fetchall()]

# Add user_id to an old expenses table if needed
if "user_id" not in columns:
    cursor.execute(
        "ALTER TABLE expenses ADD COLUMN user_id INTEGER"
    )

# Save changes BEFORE closing the database
conn.commit()

# Now close the database
conn.close()

print("Database created successfully!")