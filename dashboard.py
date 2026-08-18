import tkinter as tk
from tkinter import ttk
import sqlite3

from expense import open_expense
from view_expense import open_view_expenses
from report import open_report


# ==========================
# Database Summary
# ==========================

def get_summary():

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute("SELECT IFNULL(SUM(amount),0) FROM expenses")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM expenses")
    count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT title, category, amount, expense_date
        FROM expenses
        ORDER BY id DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    conn.close()

    return total, count, rows


# ==========================
# Dashboard
# ==========================

def open_dashboard(main_window):

    main_window.withdraw()

    root = tk.Toplevel()

    root.title("Expense Control System")
    root.geometry("1200x700")
    root.configure(bg="white")
    root.resizable(False, False)

    total, count, rows = get_summary()

    # ==========================
    # Header
    # ==========================

    header = tk.Frame(root, bg="#0B1F3A", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="Expense Control System",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman", 24, "bold")
    ).pack(side="left", padx=20, pady=15)

    # ==========================
    # Logout
    # ==========================

    def logout():

        root.destroy()

        main_window.deiconify()

    tk.Button(
        header,
        text="Logout",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman",12,"bold"),
        width=10,
        command=logout
    ).pack(side="right", padx=20)

    # ==========================
    # Body
    # ==========================

    body = tk.Frame(root,bg="white")
    body.pack(fill="both",expand=True)

    # Sidebar

    sidebar = tk.Frame(
        body,
        bg="#0B1F3A",
        width=220
    )

    sidebar.pack(side="left",fill="y")
    sidebar.pack_propagate(False)

    btn_font=("Times New Roman",14,"bold")
        # ==========================
    # Sidebar Buttons
    # ==========================

    tk.Button(
        sidebar,
        text="Dashboard",
        bg="#0B1F3A",
        fg="white",
        bd=0,
        font=btn_font
    ).pack(fill="x", pady=20)

    # Refresh dashboard function
    def refresh_dashboard():

        total, count, new_rows = get_summary()

        total_value.config(text=f"₹ {total:.2f}")
        transaction_value.config(text=str(count))
        month_value.config(text=f"₹ {total:.2f}")

        tree.delete(*tree.get_children())

        for row in new_rows:
            tree.insert("", tk.END, values=row)

    tk.Button(
        sidebar,
        text="Add Expense",
        bg="#0B1F3A",
        fg="white",
        bd=0,
        font=btn_font,
        command=lambda: open_expense(root, refresh_dashboard)
    ).pack(fill="x", pady=20)

    tk.Button(
        sidebar,
        text="View Expenses",
        bg="#0B1F3A",
        fg="white",
        bd=0,
        font=btn_font,
       command=lambda: open_view_expenses(root)
    ).pack(fill="x", pady=20)

    tk.Button(
        sidebar,
        text="Reports",
        bg="#0B1F3A",
        fg="white",
        bd=0,
        font=btn_font,
        command=open_report
    ).pack(fill="x", pady=20)

    # ==========================
    # Content
    # ==========================

    content = tk.Frame(body, bg="white")
    content.pack(side="left", fill="both", expand=True)

    tk.Label(
        content,
        text="Dashboard",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman", 28, "bold")
    ).pack(pady=20)

    # Summary Cards

    cards = tk.Frame(content, bg="white")
    cards.pack(pady=20)

    def card(parent, title, value):

        frame = tk.Frame(
            parent,
            bg="white",
            bd=2,
            relief="solid",
            width=220,
            height=110
        )

        frame.pack(side="left", padx=20)
        frame.pack_propagate(False)

        tk.Label(
            frame,
            text=title,
            bg="white",
            fg="#0B1F3A",
            font=("Times New Roman",16,"bold")
        ).pack(pady=10)

        lbl = tk.Label(
            frame,
            text=value,
            bg="white",
            fg="black",
            font=("Times New Roman",20,"bold")
        )
        lbl.pack()

        return lbl

    total_value = card(cards, "Total Expense", f"₹ {total:.2f}")
    transaction_value = card(cards, "Transactions", str(count))
    month_value = card(cards, "This Month", f"₹ {total:.2f}")

    # Recent Expenses

    tk.Label(
        content,
        text="Recent Expenses",
        bg="white",
        fg="#0B1F3A",
        font=("Times New Roman",20,"bold")
    ).pack(pady=10)

    columns = ("Title","Category","Amount","Date")

    tree = ttk.Treeview(
        content,
        columns=columns,
        show="headings",
        height=10
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(pady=10)

    for row in rows:
        tree.insert("", tk.END, values=row)

    tk.Button(
        content,
        text="Refresh",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman",12,"bold"),
        width=15,
        command=refresh_dashboard
    ).pack(pady=20)

    root.protocol("WM_DELETE_WINDOW", logout)

    root.mainloop()