import tkinter as tk
from PIL import Image, ImageTk
from login import open_login
from register import open_register

# ==========================
# Main Window
# ==========================
root = tk.Tk()
background_image = Image.open("assets/background.jpg")
background_image = background_image.resize((1200, 700))
background_photo = ImageTk.PhotoImage(background_image)


background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

root.title("Expense Control System")
root.geometry("1000x600")
root.configure(bg="white")
root.resizable(False, False)

# ==========================
# Header
# ==========================
header = tk.Frame(root, bg="#0B1F3A", height=80)
header.pack(fill="x")

title = tk.Label(
    header,
    text="Expense Control System",
    bg="#0B1F3A",
    fg="white",
    font=("Times New Roman", 28, "bold")
)
title.pack(pady=18)

# ==========================
# Main Content
# ==========================
content = tk.Frame(root, bg="white")
content.pack(expand=True)

welcome = tk.Label(
    content,
    text="WELCOME",
    bg="white",
    fg="#0B1F3A",
    font=("Times New Roman", 30, "bold")
)
welcome.pack(pady=20)

subtitle = tk.Label(
    content,
    text="Manage Your Expenses Efficiently",
    bg="white",
    fg="black",
    font=("Times New Roman", 18)
)
subtitle.pack(pady=10)

# ==========================
# Buttons
# ==========================
button_frame = tk.Frame(content, bg="white")
button_frame.pack(pady=40)

login_btn = tk.Button(
    button_frame,
    text="Login",
    bg="#0B1F3A",
    fg="white",
    font=("Times New Roman", 16, "bold"),
    width=15,
    height=2,
    command=lambda: open_login(root)
)
login_btn.grid(row=0, column=0, padx=20)

register_btn = tk.Button(
    button_frame,
    text="Register",
    bg="white",
    fg="#0B1F3A",
    font=("Times New Roman", 16, "bold"),
    width=15,
    height=2,
    relief="solid",
    borderwidth=2,
    command=lambda: open_register(root)
)
register_btn.grid(row=0, column=1, padx=20)

# ==========================
# Run Application
# ==========================
root.mainloop()