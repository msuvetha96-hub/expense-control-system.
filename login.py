import tkinter as tk
from tkinter import messagebox
import sqlite3
from dashboard import open_dashboard


def login_user(email, password, window, main_window, error_label):

    error_label.config(text="")

    email = email.strip()
    password = password.strip()

    # Validation
    if email == "":
        error_label.config(text="Please enter Email")
        return

    if password == "":
        error_label.config(text="Please enter Password")
        return

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:
        error_label.config(text="Invalid Email or Password")
        return

    messagebox.showinfo("Success", "Login Successful!")

    window.destroy()

    open_dashboard(main_window)


def open_login(main_window):

    window = tk.Toplevel(main_window)

    window.title("Login")
    window.geometry("500x450")
    window.configure(bg="white")
    window.resizable(False, False)

    # Header
    header = tk.Frame(window, bg="#0B1F3A", height=70)
    header.pack(fill="x")

    tk.Label(
        header,
        text="User Login",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman", 24, "bold")
    ).pack(pady=15)

    body = tk.Frame(window, bg="white")
    body.pack(pady=30)

    error_label = tk.Label(
        body,
        text="",
        fg="red",
        bg="white",
        font=("Times New Roman", 12, "bold")
    )
    error_label.grid(row=0, column=0, columnspan=2, pady=10)

    # Email
    tk.Label(
        body,
        text="Email",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=1, column=0, pady=10, sticky="w")

    email = tk.Entry(
        body,
        width=30,
        font=("Times New Roman", 14)
    )
    email.grid(row=1, column=1)

    # Password
    tk.Label(
        body,
        text="Password",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=2, column=0, pady=10, sticky="w")

    password = tk.Entry(
        body,
        show="*",
        width=30,
        font=("Times New Roman", 14)
    )
    password.grid(row=2, column=1)

    # Login Button
    tk.Button(
        window,
        text="Login",
        bg="#0B1F3A",
        fg="white",
        width=18,
        height=2,
        font=("Times New Roman", 12, "bold"),
        command=lambda: login_user(
            email.get(),
            password.get(),
            window,
            main_window,
            error_label
        )
    ).pack(pady=20)

    # Close Button
    tk.Button(
        window,
        text="Close",
        bg="white",
        fg="#0B1F3A",
        width=18,
        font=("Times New Roman", 12, "bold"),
        command=window.destroy
    ).pack()