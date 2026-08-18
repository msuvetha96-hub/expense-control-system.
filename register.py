import tkinter as tk
from tkinter import messagebox
import sqlite3


def save_user(fullname, email, password, confirm_password, error_label):

    error_label.config(text="", fg="red")

    fullname = fullname.strip()
    email = email.strip()
    password = password.strip()
    confirm_password = confirm_password.strip()

    # Validation
    if fullname == "":
        error_label.config(text="Please enter Full Name")
        return

    if email == "":
        error_label.config(text="Please enter Email")
        return

    if "@" not in email or "." not in email:
        error_label.config(text="Invalid Email Address")
        return

    if password == "":
        error_label.config(text="Please enter Password")
        return

    if len(password) < 6:
        error_label.config(text="Password must be at least 6 characters")
        return

    if confirm_password == "":
        error_label.config(text="Please confirm Password")
        return

    if password != confirm_password:
        error_label.config(text="Passwords do not match")
        return

    conn = sqlite3.connect("database/expense.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    if user:
        error_label.config(text="Email already exists")
        conn.close()
        return

    cursor.execute(
        """
        INSERT INTO users(fullname,email,password)
        VALUES(?,?,?)
        """,
        (fullname, email, password)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Registration Successful!"
    )


def open_register(main_window):

    window = tk.Toplevel(main_window)

    window.title("Register")

    window.geometry("500x600")

    window.configure(bg="white")

    window.resizable(False, False)

    # Header
    header = tk.Frame(
        window,
        bg="#0B1F3A",
        height=70
    )

    header.pack(fill="x")

    tk.Label(
        header,
        text="User Registration",
        bg="#0B1F3A",
        fg="white",
        font=("Times New Roman", 24, "bold")
    ).pack(pady=15)

    body = tk.Frame(window, bg="white")
    body.pack(pady=20)

    error_label = tk.Label(
        body,
        text="",
        bg="white",
        fg="red",
        font=("Times New Roman", 12, "bold")
    )

    error_label.grid(
        row=0,
        column=0,
        columnspan=2,
        pady=10
    )

    # Full Name
    tk.Label(
        body,
        text="Full Name",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=1, column=0, pady=10, sticky="w")

    fullname = tk.Entry(
        body,
        width=30,
        font=("Times New Roman", 14)
    )

    fullname.grid(row=1, column=1)

    # Email
    tk.Label(
        body,
        text="Email",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=2, column=0, pady=10, sticky="w")

    email = tk.Entry(
        body,
        width=30,
        font=("Times New Roman", 14)
    )

    email.grid(row=2, column=1)

    # Password
    tk.Label(
        body,
        text="Password",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=3, column=0, pady=10, sticky="w")

    password = tk.Entry(
        body,
        show="*",
        width=30,
        font=("Times New Roman", 14)
    )

    password.grid(row=3, column=1)

    # Confirm Password
    tk.Label(
        body,
        text="Confirm Password",
        bg="white",
        font=("Times New Roman", 14)
    ).grid(row=4, column=0, pady=10, sticky="w")

    confirm = tk.Entry(
        body,
        show="*",
        width=30,
        font=("Times New Roman", 14)
    )

    confirm.grid(row=4, column=1)

    # Register Button
    tk.Button(
        window,
        text="Register",
        bg="#0B1F3A",
        fg="white",
        width=18,
        height=2,
        font=("Times New Roman", 12, "bold"),
        command=lambda: save_user(
            fullname.get(),
            email.get(),
            password.get(),
            confirm.get(),
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