import tkinter as tk
from tkinter import ttk
import sqlite3


def open_report():

    report = tk.Toplevel()
    report.title("Expense Report")
    report.geometry("800x600")
    report.configure(bg="white")
    report.resizable(False, False)

    # ================= Header =================

    header = tk.Frame(report, bg="#0B1F3A", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Expense Report",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman", 24, "bold")
    ).pack(pady=15)

    # ================= Database =================

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses")
    total_expense = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM expenses")
    total_transactions = cursor.fetchone()[0]

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    category_data = cursor.fetchall()

    conn.close()

    # ================= Summary =================

    summary = tk.Frame(report, bg="white")
    summary.pack(pady=20)

    tk.Label(
        summary,
        text=f"Total Expense : ₹ {total_expense:.2f}",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman", 18, "bold")
    ).pack(pady=10)

    tk.Label(
        summary,
        text=f"Total Transactions : {total_transactions}",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman", 18, "bold")
    ).pack(pady=10)

    # ================= Category Report =================

    tk.Label(
        report,
        text="Category Wise Expense",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman", 20, "bold")
    ).pack(pady=10)

    columns = ("Category", "Amount")

    tree = ttk.Treeview(
        report,
        columns=columns,
        show="headings",
        height=10
    )

    tree.heading("Category", text="Category")
    tree.heading("Amount", text="Total Amount")

    tree.column("Category", width=300, anchor="center")
    tree.column("Amount", width=300, anchor="center")

    tree.pack(pady=20)

    for row in category_data:
        tree.insert("", tk.END, values=row)

    # ================= Close Button =================

    tk.Button(
        report,
        text="Close",
        bg="#0B1F3A",
        fg="white",
        width=15,
        font=("Times New Roman", 12, "bold"),
        command=report.destroy
    ).pack(pady=15)