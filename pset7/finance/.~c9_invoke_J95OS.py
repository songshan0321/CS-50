from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user = db.execute("SELECT * FROM users WHERE id=:id",id=session["user_id"])
    cash = round(user[0]["cash"],2)

    # Pass in an array of stock
    stocks = db.execute("SELECT symbol, name, SUM(shares), price FROM portfolio WHERE id=:id GROUP BY symbol",id=session["user_id"])
    total = {}
    grand_total = cash
    for stock in stocks:
        quote = lookup(stock["symbol"])
        total[stock["symbol"]] = round(float(quote["price"]) * int(stock["SUM(shares)"]),2)
        grand_total += total[stock["symbol"]]
    return render_template("index.html", user=user, cash=cash, stocks=stocks, total=total, grand_total=grand_total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Lookup for a stock, return a dict
        quote = lookup(request.form.get("symbol"))

        # Check stock exist
        if not quote:
            return apology("Stock unavailable", 400)

        # Ensure shares was submitted
        elif request.form.get("shares").isdigit() == False or int(request.form.get("shares")) <= 0:
            return apology("Shares must be positive integer", 400)

        shares = int(request.form.get("shares"))
        price = float(quote["price"])
        cost = shares * price

        # Query database for cash
        cash = db.execute("SELECT cash FROM users WHERE id = :id", id=session["user_id"])

        # Check if user can afford to buy
        if cash[0]["cash"] < cost:
            return apology("Sorry, you don't have enough budget!", 400)


        db.execute("INSERT INTO portfolio (id,symbol,name,shares,price) VALUES (:id,:symbol,:name,:shares,:price)",id=session["user_id"],symbol=quote["symbol"],name=quote["name"], shares=shares,price=quote["price"])
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :id",cost = cost,id=session["user_id"])

        flash('Bought!')

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Pass in an array of stock
    stocks = db.execute("SELECT symbol, shares, price, time FROM portfolio WHERE id=:id ",id=session["user_id"])

    return render_template("history.html",stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
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
    """Get stock quote."""
    if request.method == "POST":
        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Lookup for a stock, return a dict (name,price,symbol)
        quote = lookup(request.form.get("symbol"))

        # Check stock exist
        if not quote:
            return apology("Stock unavailable", 400)

        # Display info
        return render_template("quoted.html",name = quote["name"], price = quote["price"],symbol = quote["symbol"])

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Missing username!", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Missing password!", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("Missing confirmation", 400)

        # Make sure password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Confirmation doesn't match", 400)

        # Hash password
        hashed = generate_password_hash(str(request.form.get("password")))
        if not hashed:
            return apology("Hash failed", 500)

        # Insert new user into databse
        result = db.execute("INSERT INTO users (username,hash) \
                            VALUES(:username,:hashed)",username=str(request.form.get("username")),hashed = hashed)

        # Check if username exist
        if not result:
            return apology("The username existed." , 400)

        # Remember which user has logged in
        session["user_id"] = result

        # Redirect user to home page
        flash('Successfully registered!')
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
def change():
    """Change password"""
    if request.method == "POST":
        # Ensure old password was submitted
        if not request.form.get("old_password"):
            return apology("Missing old password!", 400)

        # Ensure new password was submitted
        elif not request.form.get("new_password"):
            return apology("Missing new password!", 400)

        # Ensure new confirmation password was submitted
        elif not request.form.get("conf_password"):
            return apology("Missing confirmation password", 400)

        db.execute("UPDATE users SET password = :new_pass WHERE id = :id",new_pass=, id=session["user_id"])
        elif request.form.get("new_password") != request.form.get("conf_password"):
            return apology("Confirmation doesn't match", 400)

        # Hash password
        hashed = generate_password_hash(str(request.form.get("new_password")))
        if not hashed:
            return apology("Hash failed", 500)

        db.execute("UPDATE users SET hash = :new_pass WHERE id = :id",new_pass=hashed, id=session["user_id"])

        flash("Changed password successfully!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure symbol was selected correctly
        if not request.form.get("symbol"):
            return apology("Invalid Symbol!", 400)

        # Ensure shares was provided
        elif not request.form.get("shares"):
            return apology("Missing shares!", 400)

        # Lookup for a stock, return a dict
        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid Symbol", 400)
        curr_cost = round(float(quote["price"]) * int(request.form.get("shares")),2)
        
        

        db.execute("INSERT INTO portfolio (id,symbol,name,shares,price) VALUES (:id,:symbol,:name,:shares,:price)",id=session["user_id"],symbol=quote["symbol"],name=quote["name"], shares=-int(request.form.get("shares")),price=quote["price"])
        db.execute("UPDATE users SET cash = cash + :cost WHERE id = :id",cost = curr_cost,id=session["user_id"])

        flash("Sold!")
        return redirect("/")

    else:
        # Pass in an array of stock
        stocks = db.execute("SELECT symbol, name, SUM(shares), price FROM portfolio WHERE id=:id GROUP BY symbol",id=session["user_id"])

        return render_template("sell.html",stocks=stocks)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
