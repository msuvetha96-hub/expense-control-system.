import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ================= SAVE EXPENSE =================

def save_expense(
    title,
    category,
    amount,
    date,
    description,
    window,
    error_label,
    refresh_callback=None
):
    # Remove previous error
    error_label.config(text="")

    title = title.strip()
    category = category.strip()
    amount = amount.strip()
    date = date.strip()
    description = description.strip()

    # Title Validation
    if title == "":
        error_label.config(text="* Please enter Expense Title.")
        return

    # Category Validation
    if category == "":
        error_label.config(text="* Please select Category.")
        return

    # Amount Validation
    if amount == "":
        error_label.config(text="* Please enter Amount.")
        return

    try:
        amount = float(amount)

        if amount <= 0:
            error_label.config(text="* Amount must be greater than zero.")
            return

    except ValueError:
        error_label.config(text="* Amount must contain numbers only.")
        return

    # Date Validation
    if date == "":
        error_label.config(text="* Please enter Date.")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")

    except ValueError:
        error_label.config(
            text="* Date must be in YYYY-MM-DD format."
        )
        return

    # Save Database

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (title,category,amount,expense_date,description)
        VALUES(?,?,?,?,?)
    """,
    (
        title,
        category,
        amount,
        date,
        description
    ))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Expense Added Successfully."
    )

    window.destroy()


# ================= ADD EXPENSE WINDOW =================

def open_expense(parent, refresh_callback=None):

    window = tk.Toplevel(parent)

    window.title("Add Expense")
    window.geometry("700x700")
    window.configure(bg="white")
    window.resizable(False, False)

    # ================= HEADER =================

    header = tk.Frame(
        window,
        bg="#0B1F3A",
        height=70
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="Add Expense",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman",24,"bold")
    ).pack(pady=15)

    # ================= BODY =================

    body = tk.Frame(window,bg="white")
    body.pack(pady=20)

    # Error Label

    error_label = tk.Label(
        body,
        text="",
        bg="white",
        fg="red",
        font=("Times New Roman",12,"bold")
    )

    error_label.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=(0,20)
    )

    # ================= TITLE =================

    tk.Label(
        body,
        text="Expense Title",
        bg="white",
        font=("Times New Roman",14)
    ).grid(row=1,column=0,pady=10,sticky="w")

    title = tk.Entry(
        body,
        width=30,
        font=("Times New Roman",14)
    )

    title.grid(row=1,column=1,pady=10)

    # ================= CATEGORY =================

    tk.Label(
        body,
        text="Category",
        bg="white",
        font=("Times New Roman",14)
    ).grid(row=2,column=0,pady=10,sticky="w")

    category = ttk.Combobox(
        body,
        width=28,
        state="readonly",
        values=[
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Education",
            "Medical",
            "Entertainment",
            "Other"
        ]
    )

    category.grid(row=2,column=1,pady=10)
    category.current(0)

    # ================= AMOUNT =================

    tk.Label(
        body,
        text="Amount",
        bg="white",
        font=("Times New Roman",14)
    ).grid(row=3,column=0,pady=10,sticky="w")

    amount = tk.Entry(
        body,
        width=30,
        font=("Times New Roman",14)
    )

    amount.grid(row=3,column=1,pady=10)

    # ================= DATE =================

    tk.Label(
        body,
        text="Date (YYYY-MM-DD)",
        bg="white",
        font=("Times New Roman",14)
    ).grid(row=4,column=0,pady=10,sticky="w")

    date = tk.Entry(
        body,
        width=30,
        font=("Times New Roman",14)
    )

    date.insert(0,datetime.now().strftime("%Y-%m-%d"))

    date.grid(row=4,column=1,pady=10)

    # ================= DESCRIPTION =================

    tk.Label(
        body,
        text="Description",
        bg="white",
        font=("Times New Roman",14)
    ).grid(row=5,column=0,pady=10,sticky="nw")

    description = tk.Text(
        body,
        width=30,
        height=6,
        font=("Times New Roman",12)
    )

    description.grid(row=5,column=1,pady=10)

    # ================= BUTTONS =================

    button_frame = tk.Frame(
        window,
        bg="white"
    )

    button_frame.pack(pady=20)

    tk.Button(
        button_frame,
        text="Save Expense",
        width=16,
        height=2,
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman",12,"bold"),
        command=lambda: save_expense(
            title.get(),
            category.get(),
            amount.get(),
            date.get(),
            description.get("1.0",tk.END),
            window,
            error_label
        )
    ).grid(row=0,column=0,padx=10)

    tk.Button(
        button_frame,
        text="Close",
        width=16,
        height=2,
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman",12,"bold"),
        command=window.destroy
    ).grid(row=0,column=1,padx=10)