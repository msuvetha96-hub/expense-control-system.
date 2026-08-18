from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "expense-control-secret-key"

DATABASE = "database/expense.db"


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if not re.match(email_pattern, email):
            return render_template(
                "login.html",
                error="Please enter a valid email address."
            )

        if password == "":
            return render_template(
                "login.html",
                error="Please enter your password."
            )

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT id, fullname, password
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        conn.close()

        if user and check_password_hash(user["password"], password):

            session["user_id"] = user["id"]
            session["fullname"] = user["fullname"]

            return redirect(url_for("dashboard"))

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if fullname == "":
            return render_template(
                "register.html",
                error="Please enter your full name."
            )

        if email == "":
            return render_template(
                "register.html",
                error="Please enter your email."
            )

        email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"

        if not re.match(email_pattern, email):
            return render_template(
                "register.html",
                error="Please enter a valid email address."
            )

        if password == "":
            return render_template(
                "register.html",
                error="Please enter a password."
            )

        if len(password) < 6:
            return render_template(
                "register.html",
                error="Password must be at least 6 characters."
            )

        if password != confirm_password:
            return render_template(
                "register.html",
                error="Passwords do not match."
            )

        conn = get_db_connection()

        # Check existing email
        existing_user = conn.execute(
            """
            SELECT id
            FROM users
            WHERE email=?
            """,
            (email,)
        ).fetchone()

        if existing_user:
            conn.close()

            return render_template(
                "register.html",
                error="Email already exists."
            )

        # Hash password before saving
        hashed_password = generate_password_hash(password)

        # Insert new user
        conn.execute(
            """
            INSERT INTO users
            (fullname, email, password)
            VALUES (?, ?, ?)
            """,
            (
                fullname,
                email,
                hashed_password
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            "register.html",
            success="Registration successful! You can now login."
        )

    return render_template("register.html")


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()

    # Total expense
    total = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchone()[0]

    # Number of transactions
    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM expenses
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchone()[0]

    # This month's expense
    current_month = datetime.date.today().strftime("%Y-%m")

    month_total = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id=?
        AND expense_date LIKE ?
        """,
        (
            user_id,
            current_month + "%"
        )
    ).fetchone()[0]

    # Recent expenses
    expenses = conn.execute(
        """
        SELECT title,
               category,
               amount,
               expense_date
        FROM expenses
        WHERE user_id=?
        ORDER BY id DESC
        LIMIT 10
        """,
        (user_id,)
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        fullname=session["fullname"],
        total=total,
        count=count,
        month_total=month_total,
        expenses=expenses
    )


# --------------------------------------------------
# ADD EXPENSE
# --------------------------------------------------

@app.route("/add-expense", methods=["GET", "POST"])
def add_expense():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        amount = request.form.get("amount", "").strip()
        expense_date = request.form.get("expense_date", "").strip()
        description = request.form.get("description", "").strip()

        if title == "":
            return render_template(
                "add_expense.html",
                error="Please enter expense title."
            )

        if category == "":
            return render_template(
                "add_expense.html",
                error="Please select a category."
            )

        if amount == "":
            return render_template(
                "add_expense.html",
                error="Please enter amount."
            )

        try:
            amount = float(amount)

            if amount <= 0:
                return render_template(
                    "add_expense.html",
                    error="Amount must be greater than 0."
                )

        except ValueError:
            return render_template(
                "add_expense.html",
                error="Invalid amount."
            )

        if expense_date == "":
            return render_template(
                "add_expense.html",
                error="Please select date."
            )

        try:
            datetime.datetime.strptime(
                expense_date,
                "%Y-%m-%d"
            )

        except ValueError:
            return render_template(
                "add_expense.html",
                error="Invalid date format."
            )

        conn = get_db_connection()

        # Save expense for logged-in user
        conn.execute(
            """
            INSERT INTO expenses
            (
                user_id,
                title,
                category,
                amount,
                expense_date,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                session["user_id"],
                title,
                category,
                amount,
                expense_date,
                description
            )
        )

        conn.commit()
        conn.close()

        return render_template(
            "add_expense.html",
            success="Expense saved successfully!"
        )

    return render_template("add_expense.html")


# --------------------------------------------------
# VIEW EXPENSES
# --------------------------------------------------

@app.route("/view-expenses")
def view_expenses():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get(
        "search",
        ""
    ).strip()

    filter_date = request.args.get(
        "filter_date",
        ""
    ).strip()

    user_id = session["user_id"]

    conn = get_db_connection()

    query = """
        SELECT id,
               title,
               category,
               amount,
               expense_date,
               description
        FROM expenses
        WHERE user_id=?
    """

    parameters = [user_id]

    # Search
    if search:

        query += """
            AND (
                title LIKE ?
                OR category LIKE ?
                OR description LIKE ?
            )
        """

        search_value = "%" + search + "%"

        parameters.extend(
            [
                search_value,
                search_value,
                search_value
            ]
        )

    # Date filter
    if filter_date:

        query += """
            AND expense_date=?
        """

        parameters.append(filter_date)

    query += """
        ORDER BY id DESC
    """

    expenses = conn.execute(
        query,
        parameters
    ).fetchall()

    conn.close()

    return render_template(
        "view_expenses.html",
        expenses=expenses,
        search=search,
        filter_date=filter_date
    )


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

@app.route("/reports")
def reports():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    conn = get_db_connection()

    # Total
    total = conn.execute(
        """
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchone()[0]

    # Count
    count = conn.execute(
        """
        SELECT COUNT(*)
        FROM expenses
        WHERE user_id=?
        """,
        (user_id,)
    ).fetchone()[0]

    # Average
    if count > 0:
        average = total / count
    else:
        average = 0

    # Category data
    category_data = conn.execute(
    """
    SELECT category,
           SUM(amount)
    FROM expenses
    WHERE user_id=?
    GROUP BY category
    ORDER BY SUM(amount) DESC
    """,
    (user_id,)
).fetchall()

    conn.close()

    categories = []

    for category, amount in category_data:

        if total > 0:
            percentage = (
                amount / total
            ) * 100
        else:
            percentage = 0

        categories.append(
            (
                category,
                amount,
                percentage
            )
        )

    return render_template(
        "reports.html",
        total=total,
        count=count,
        average=average,
        categories=categories
    )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )


# --------------------------------------------------
# DELETE EXPENSE
# --------------------------------------------------

@app.route("/delete-expense/<int:expense_id>")
def delete_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM expenses
        WHERE id=?
        AND user_id=?
        """,
        (
            expense_id,
            session["user_id"]
        )
    )

    conn.commit()
    conn.close()

    return redirect(
        url_for("view_expenses")
    )


# --------------------------------------------------
# EDIT EXPENSE
# --------------------------------------------------

@app.route(
    "/edit-expense/<int:expense_id>",
    methods=["GET", "POST"]
)
def edit_expense(expense_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = get_db_connection()

    # UPDATE
    if request.method == "POST":

        title = request.form.get(
            "title",
            ""
        ).strip()

        category = request.form.get(
            "category",
            ""
        ).strip()

        amount = request.form.get(
            "amount",
            ""
        ).strip()

        expense_date = request.form.get(
            "expense_date",
            ""
        ).strip()

        description = request.form.get(
            "description",
            ""
        ).strip()

        if title == "":
            conn.close()

            return render_template(
                "edit_expense.html",
                error="Please enter expense title.",
                expense=(
                    expense_id,
                    title,
                    category,
                    amount,
                    expense_date,
                    description
                )
            )

        if category == "":
            conn.close()

            return render_template(
                "edit_expense.html",
                error="Please select a category.",
                expense=(
                    expense_id,
                    title,
                    category,
                    amount,
                    expense_date,
                    description
                )
            )

        try:
            amount = float(amount)

            if amount <= 0:
                conn.close()

                return render_template(
                    "edit_expense.html",
                    error="Amount must be greater than 0.",
                    expense=(
                        expense_id,
                        title,
                        category,
                        amount,
                        expense_date,
                        description
                    )
                )

        except ValueError:

            conn.close()

            return render_template(
                "edit_expense.html",
                error="Invalid amount.",
                expense=(
                    expense_id,
                    title,
                    category,
                    amount,
                    expense_date,
                    description
                )
            )

        if expense_date == "":
            conn.close()

            return render_template(
                "edit_expense.html",
                error="Please select date.",
                expense=(
                    expense_id,
                    title,
                    category,
                    amount,
                    expense_date,
                    description
                )
            )

        try:
            datetime.datetime.strptime(
                expense_date,
                "%Y-%m-%d"
            )

        except ValueError:

            conn.close()

            return render_template(
                "edit_expense.html",
                error="Invalid date format.",
                expense=(
                    expense_id,
                    title,
                    category,
                    amount,
                    expense_date,
                    description
                )
            )

        # Update only current user's expense
        conn.execute(
            """
            UPDATE expenses
            SET title=?,
                category=?,
                amount=?,
                expense_date=?,
                description=?
            WHERE id=?
            AND user_id=?
            """,
            (
                title,
                category,
                amount,
                expense_date,
                description,
                expense_id,
                session["user_id"]
            )
        )

        conn.commit()
        conn.close()

        return redirect(
            url_for("view_expenses")
        )

    # GET - current user's expense only
    expense = conn.execute(
        """
        SELECT id,
               title,
               category,
               amount,
               expense_date,
               description
        FROM expenses
        WHERE id=?
        AND user_id=?
        """,
        (
            expense_id,
            session["user_id"]
        )
    ).fetchone()

    conn.close()

    if expense is None:
        return "Expense not found."

    return render_template(
        "edit_expense.html",
        expense=expense
    )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)