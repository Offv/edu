import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)

from helpers import apology, login_required as login_required_decorator, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.urandom(24)
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Set up Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# Define User model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    portfolio = db.execute(
        """
        SELECT symbol, shares, price, (shares * price) AS total
        FROM portfolio
        WHERE user_id = ?
    """,
        session["user_id"],
    )
    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash = user[0]["cash"]

    total_value = cash + sum([item["total"] for item in portfolio])

    return render_template(
        "main.html", portfolio=portfolio, cash=cash, total=total_value
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            flash("Must provide symbol", "danger")
            return redirect("/buy")

        if not shares or not shares.isdigit() or int(shares) <= 0:
            flash("Must provide valid number of shares", "danger")
            return redirect("/buy")

        shares = int(shares)

        stock = lookup(symbol)
        if stock is None:
            flash("Invalid symbol", "danger")
            return redirect("/buy")

        user_id = session["user_id"]
        user = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]
        cash = user["cash"]

        total_cost = shares * stock["price"]

        if total_cost > cash:
            flash("Not enough cash for this purchase", "danger")
            return redirect("/buy")

        updated_cash = cash - total_cost
        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)

        existing_stock = db.execute(
            "SELECT shares FROM portfolio WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )

        if existing_stock:

            new_shares = existing_stock[0]["shares"] + shares
            db.execute(
                "UPDATE portfolio SET shares = ?, price = ? WHERE user_id = ? AND symbol = ?",
                new_shares,
                stock["price"],
                user_id,
                symbol,
            )
        else:

            total = shares * stock["price"]

            db.execute(
                "INSERT INTO portfolio (user_id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
                user_id,
                symbol,
                shares,
                stock["price"],
                total,
            )

        db.execute(
            "INSERT INTO history (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            user_id,
            symbol,
            shares,
            stock["price"],
            "BUY",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        flash("Stock purchased successfully!", "success")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():

    history = History.get_user_history(session["user_id"])

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)
        elif not password:
            return apology("must provide password", 403)

        user = User.get_by_username(username)

        if user is None or not user.check_password(password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = user.id
        login_user(user)

        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    stock = None
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 403)

        stock = lookup(symbol)
        if stock is None:
            return apology("invalid symbol", 403)

    return render_template("quote.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        if not username or not password or not password2:
            return apology("Forms can't be empty!", 403)

        if password != password2:
            return apology("Passwords do not match!", 403)

        if User.get_by_username(username) is not None:
            return apology("Username already taken!", 403)

        User.create(username, password)

        db.execute("DROP TABLE IF EXISTS portfolio")

        db.execute(
            """
        CREATE TABLE portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        symbol TEXT NOT NULL,
        shares INTEGER NOT NULL,
        price REAL NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """
        )

        db.execute("DROP TABLE IF EXISTS history")

        db.execute(
            """CREATE TABLE history (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         user_id INTEGER NOT NULL,
         symbol TEXT NOT NULL,
         shares INTEGER NOT NULL,
         price REAL NOT NULL,
         transaction_type TEXT NOT NULL,
         timestamp TEXT NOT NULL,
         FOREIGN KEY (user_id) REFERENCES users(id)
         )"""
        )

        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        user_id = session["user_id"]
        symbol = request.form.get("symbol").upper()
        shares_to_sell = int(request.form.get("shares"))

        # Fetch the current holdings for the user
        portfolio = db.execute(
            "SELECT shares, price FROM portfolio WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )
        if len(portfolio) != 1:
            return apology("You don't own this stock", 400)

        # Check if user has enough shares to sell
        shares_owned = portfolio[0]["shares"]
        if shares_to_sell > shares_owned:
            return apology("Not enough shares", 400)

        # Calculate the total sale amount
        current_price = lookup(symbol)["price"]
        total_sale_value = current_price * shares_to_sell

        # Update the portfolio: reduce shares or remove the stock if all shares are sold
        if shares_to_sell == shares_owned:
            db.execute(
                "DELETE FROM portfolio WHERE user_id = ? AND symbol = ?",
                user_id,
                symbol,
            )
        else:
            db.execute(
                "UPDATE portfolio SET shares = shares - ? WHERE user_id = ? AND symbol = ?",
                shares_to_sell,
                user_id,
                symbol,
            )

        # Update the user's cash
        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", total_sale_value, user_id
        )

        # Record the transaction in the history
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, 'SELL', ?)",
            user_id,
            symbol,
            -shares_to_sell,
            current_price,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        flash("Sold!")
        return redirect("/")

    else:
        # Fetch the user's portfolio to display in the sell form
        user_id = session["user_id"]
        portfolio = db.execute(
            "SELECT symbol, shares FROM portfolio WHERE user_id = ?", user_id
        )
        return render_template("sell.html", portfolio=portfolio)


@login_manager.user_loader
def load_user(user_id):
    return User.query(user_id)


class History:
    def __init__(self, user_id, symbol, shares, price, transaction_type):
        self.user_id = user_id
        self.symbol = symbol
        self.shares = shares
        self.price = price
        self.transaction_type = transaction_type
        self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save(self):
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, price, transaction_type, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            self.user_id,
            self.symbol,
            self.shares,
            self.price,
            self.transaction_type,
            self.timestamp,
        )

    @staticmethod
    def get_user_history(user_id):
        rows = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)
        return rows


class Portfolio:
    def __init__(self, user_id, symbol, shares, price):
        self.user_id = user_id
        self.symbol = symbol
        self.shares = shares
        self.price = price
        self.total = shares * price

    def save(self):
        db.execute(
            "INSERT INTO portfolio (user_id, symbol, shares, price, total) VALUES (?, ?, ?, ?, ?)",
            self.user_id,
            self.symbol,
            self.shares,
            self.price,
            self.total,
        )

    @staticmethod
    def get_user_portfolio(user_id):
        rows = db.execute("SELECT * FROM portfolio WHERE user_id = ?", user_id)
        return rows

    @staticmethod
    def update_shares(user_id, symbol, new_shares, new_price):
        total = new_shares * new_price
        db.execute(
            "UPDATE portfolio SET shares = ?, price = ?, total = ? WHERE user_id = ? AND symbol = ?",
            new_shares,
            new_price,
            total,
            user_id,
            symbol,
        )

    @staticmethod
    def delete_stock(user_id, symbol):
        db.execute(
            "DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", user_id, symbol
        )


class User:
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        if len(rows) == 0:
            return None
        return User(
            user_id=rows[0]["id"],
            username=rows[0]["username"],
            password_hash=rows[0]["hash"],
        )

    @staticmethod
    def get_by_username(username):
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) == 0:
            return None
        return User(
            user_id=rows[0]["id"],
            username=rows[0]["username"],
            password_hash=rows[0]["hash"],
        )

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):

        return True

    @property
    def is_authenticated(self):

        return True

    @property
    def is_anonymous(self):

        return False

    @staticmethod
    def create(username, password):

        password_hash = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)", username, password_hash
        )


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
