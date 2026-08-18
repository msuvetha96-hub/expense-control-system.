import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


# ================= LOAD DATA =================

def load_expenses(tree):

    tree.delete(*tree.get_children())

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, category, amount, expense_date, description
        FROM expenses
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


# ================= DELETE =================

def delete_expense(tree):

    selected = tree.selection()

    if not selected:
        messagebox.showerror(
            "Error",
            "Please select an expense."
        )
        return

    expense_id = tree.item(selected[0])["values"][0]

    confirm = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this expense?"
    )

    if not confirm:
        return

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (expense_id,)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Expense deleted successfully."
    )

    # Stay on the same page
    load_expenses(tree)


# ================= VIEW WINDOW =================

def open_view_expenses(parent=None):

    if parent:
        window = tk.Toplevel(parent)
    else:
        window = tk.Toplevel()

    window.title("View Expenses")
    window.geometry("1100x600")
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
        text="View Expenses",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman", 24, "bold")
    ).pack(pady=15)

    # ================= TABLE =================

    columns = (
        "ID",
        "Title",
        "Category",
        "Amount",
        "Date",
        "Description"
    )

    tree = ttk.Treeview(
        window,
        columns=columns,
        show="headings",
        height=18
    )

    for col in columns:
        tree.heading(col, text=col)

    tree.column("ID", width=60, anchor="center")
    tree.column("Title", width=180)
    tree.column("Category", width=120)
    tree.column("Amount", width=100, anchor="center")
    tree.column("Date", width=120, anchor="center")
    tree.column("Description", width=350)

    tree.pack(pady=20)

    load_expenses(tree)

    # ================= BUTTONS =================

    button_frame = tk.Frame(window, bg="white")
    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="Delete Expense",
        bg="#800000",
        fg="white",
        width=18,
        height=2,
        font=("Times New Roman", 12, "bold"),
        command=lambda: delete_expense(tree)
    ).grid(row=0, column=0, padx=10)

    tk.Button(
        button_frame,
        text="Refresh",
        bg="#0B1F3A",
        fg="white",
        width=18,
        height=2,
        font=("Times New Roman", 12, "bold"),
        command=lambda: load_expenses(tree)
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        button_frame,
        text="Close",
        bg="white",
        fg="#0B1F3A",
        width=18,
        height=2,
        font=("Times New Roman", 12, "bold"),
        command=window.destroy
    ).grid(row=0, column=2, padx=10)