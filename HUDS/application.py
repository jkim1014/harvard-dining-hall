from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from threading import Timer
from helpers import apology, login_required, repeatScrape
# import time to know when transactions occur
from time import ctime

# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///information.db")


# def refresher():

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """index home page"""
    return render_template("index.html")


@app.route("/personal_info", methods=["GET"])
@login_required
def personal_info():
    """Display personal information for each user"""

    # Collect information from databases about the user's personal info and meal history
    personal_info = db.execute("SELECT * FROM user_information WHERE id=:id", id=session["user_id"])
    name = db.execute("SELECT name FROM users WHERE id=:id", id=session["user_id"])
    meals = db.execute("SELECT * FROM meals WHERE id=:id", id=session["user_id"])

    # Send information to html form
    return render_template("personal_info.html",
                           name=name[0]["name"],
                           weight=personal_info[0]["weight"],
                           height=personal_info[0]["height"],
                           age=personal_info[0]["age"],
                           gender=personal_info[0]["gender"],
                           meals=meals)


@app.route("/update_personal_info", methods=["GET", "POST"])
@login_required
def update_personal_info():
    """Update personal information to store user information"""

    if request.method == "POST":
        # For each item, update user information only if given a new value
        if request.form.get("age"):
            db.execute("UPDATE user_information SET age=:age WHERE id=:id",
                       id=session["user_id"],
                       age=request.form.get("age"))
        if request.form.get("height"):
            db.execute("UPDATE user_information SET height=:height WHERE id=:id",
                       id=session["user_id"],
                       height=request.form.get("height"))
        if request.form.get("weight"):
            db.execute("UPDATE user_information SET weight=:weight WHERE id=:id",
                       id=session["user_id"],
                       weight=request.form.get("weight"))
        return redirect("/personal_info")

    # Shows users the form
    else:
        return render_template("update_personal_info.html")


@app.route("/meal_plan", methods=["GET", "POST"])
@login_required
def meal_plan():
    """Display webscraped stuff and make meal plan"""

    # Select information to pass into the meal_plan template
    food_information = db.execute("SELECT * FROM food_table")
    if request.method == "GET":
        return render_template("meal_plan.html", all=food_information)

    # Send users to nutrition page (calculated totals)
    elif request.method == "POST":
        return redirect("/nutrition")


@app.route("/nutrition", methods=["GET", "POST"])
@login_required
def nutrition():
    """Display nutritional information of each meal"""
    if request.method == "POST":
        # Collect information about food from database
        food_information = db.execute("SELECT * FROM food_table")

        # Initialize two arrays containing the quantities selected by the user for each food, and the food names
        inputs = []
        names = []

        # Number of rows in the food table
        rows = db.execute("SELECT COUNT(*) FROM food_table")

        # Populate the two arrays we initialized
        for i in range(rows[0]["COUNT(*)"]):
            name = food_information[i]["name"]
            quantity = request.form.get(name)
            names.append(name)
            inputs.append(quantity)

        # Initialize variables for the nutrients we want to keep track of
        calories = 0
        protein = 0
        fat = 0
        carbs = 0

        # Cycle through the foods
        for i in range(len(inputs)):
            # If the user actually selected the food
            if inputs[i] != '':
                # Get nutrient information of the food
                selected = db.execute("SELECT * FROM food_table WHERE name=:name", name=names[i])
                # Add once to our cumulative totals the nutrient information of the food for the number of times the user selected the food
                for j in range(int(inputs[i])):
                    calories += round(float(selected[0]["calories"]))
                    protein += round(float(selected[0]["protein"]))
                    fat += round(float(selected[0]["fat"]))
                    carbs += round(float(selected[0]["carbs"]))
            else:
                i += 1

        # Add user meal information into sql table for use in history (personal info)
        db.execute("INSERT INTO meals (calories, protein, fat, carbs, id) VALUES (:calories, :protein, :fat, :carbs, :id)",
                   calories=calories,
                   protein=protein,
                   fat=fat,
                   carbs=carbs,
                   id=session["user_id"])

        # Load html with the nutrients
        return render_template("nutrition.html", calories=calories, protein=protein, fat=fat, carbs=carbs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            print(rows)
            return apology("invalid username and/or password", 403)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation password was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure that passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Checks that username doesn't already exist
        userlist = db.execute("SELECT username FROM users WHERE username = :username",
                              username=request.form.get("username"))
        if len(userlist) != 0:
            return apology("username taken", 400)

        # Hash the password to protect security
        hash = generate_password_hash(request.form.get("password"))

        # Add user to database
        result = db.execute("INSERT INTO users (username, name, hash) VALUES(:username, :name, :hash)",
                            username=request.form.get("username"), name=request.form.get("name"), hash=hash)
        # Apologize if db execution failed
        if not result:
            return apology("username taken!", 400)

        # Log user in
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        # Add user to user information database
        db.execute("INSERT into user_information (id, age, gender, height, weight) VALUES(:id, :age, :gender, :height, :weight)",
                   id=session["user_id"],
                   age=request.form.get("age"),
                   gender=request.form.get("gender"),
                   height=request.form.get("height"),
                   weight=request.form.get("weight"))

        return redirect("/")


@app.route("/table_helper", methods=["GET", "POST"])
@login_required
def table_helper():
    """ Display a table of people's positions in Annenberg"""

    # Select the most recent 500 posts from the seating chart
    name = db.execute("SELECT name FROM users WHERE id=:id", id=session["user_id"])

    # Reverses the order so that it goes in order from most recent
    total = db.execute(
        "SELECT * FROM (SELECT * FROM records ORDER BY time DESC LIMIT 500) as foo ORDER BY foo.time DESC;")

    # Shows the posts
    if request.method == "GET":
        return render_template("table_helper.html", all=total)

    # Shows the posts after adding the one the user submitted
    elif request.method == "POST":
        # Makes sure that the input of table is valid
        table = request.form.get("table").upper()
        possible = {'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16', 'A17',
                    'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13', 'B14', 'B15', 'B16', 'B17',
                    'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17'}
        add = False
        if table in possible:
            add = True

        # If valid table, add the new post and refresh the table
        if add:
            db.execute("INSERT INTO records ('table', 'name') VALUES (:table, :name)",
                       table=table, name=name[0]["name"])
            totals = db.execute(
                "SELECT * FROM (SELECT * FROM records ORDER BY time DESC LIMIT 500) as foo ORDER BY foo.time DESC;")
            return render_template("table_helper.html", all=totals)

        # If invalid table, flash error and show the table
        flash('Invalid table')
        return render_template("table_helper.html", all=total)


@app.route("/history")
@login_required
def history():
    """Show history of meals"""
    # Access history table, return necessary information within history template
    items = db.execute("SELECT name, symbol, price, shares, time FROM history WHERE id=:id",
                       id=session["user_id"])

    return render_template("history.html", items=items)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


repeatScrape()

# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)