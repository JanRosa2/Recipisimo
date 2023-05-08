from flask import Blueprint, flash, render_template, redirect, url_for, request
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import rstpass

auth = Blueprint("auth",__name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    """
    The function login user. In case the user exists, it is going to check the provided password.
    If successful the user is logged in. The function "login_user" from module flask_login is used here 
    to remember the user with session.
    """
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            check = check_password_hash(user.password, password)
            if check:
                flash("You are logged in!")
                # This remembers that user is logged in. Until we restart server or use clear history.
                login_user(user, remember=True)
                return redirect(url_for("views.search_recipes"))
            else:
                flash("User or password is wrong!") 
        else:
            flash("User or password is wrong!")

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    """
    The function for logout the user and remove the session.
    """
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    # when authenticated redirect
    if current_user.is_authenticated:
        return redirect("/search")
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        c_password = request.form.get("c_password")
        # search if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already in use.")
        # check the password
        elif password != c_password:
            flash("Both passwords has to match.")
        elif len(password) < 8:
            flash("Your password should be atleast 8 characters long.") 
        else:
            # if everythin is alright with the password... hash it
            password = generate_password_hash(password, method="sha256")
            # Create new_user object 
            new_user = User(email=email, password=password)
            # Add the new_user to the database
            db.session.add(new_user)
            db.session.commit()
            # Login the new user
            login_user(new_user, remember=True)
            flash("You are successfuly registered")
            # Redirect user to recipes
            return redirect(url_for("views.search_recipes"))
    
    return render_template("register.html", user=current_user)

@auth.route("/resetpassword", methods=["GET", "POST"])
@login_required
def reset_password():
    """
    Changes password to authenticated user.
    """
    if request.method == "POST":
        new_password = request.form.get("new_password")
        c_new_password = request.form.get("c_new_password")
        if new_password != c_new_password:
            flash("Both passwords has to match.")
        elif len(new_password) < 8:
            flash("Your password should be atleast 8 characters long.") 
        else:
            new_password = generate_password_hash(new_password, method="sha256")
            current_user.password = new_password
            db.session.commit()
            flash("You successfuly changed your password.")
        
    return render_template("reset_password.html", user=current_user)

@auth.route("/recoverpassword", methods=["GET", "POST"])
def recover_password():
    """
    Recover password through email.
    """
    if request.method == "POST":
        email = request.form.get("email")
        if rstpass.change_and_inform(email) != False:
            flash("Password was successfuly changed and email send.")          
        else:
            flash("Sorry, we have encountered a problem.")  

        return render_template("recover_password.html", user=current_user)

    return render_template("recover_password.html", user=current_user)
            

