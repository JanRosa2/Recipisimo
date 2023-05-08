from flask import Blueprint, render_template, redirect, flash, request
from website.recipes import get_recipes, process_json
from .models import User
from flask_login import login_required, current_user

views = Blueprint("views",__name__)

@views.route("/")
def index():
    """
    Renders index page.
    """
    return render_template("index.html", user=current_user)

@views.route("/search", methods=["GET", "POST"])
@login_required
def search_recipes():
    """
    Searches for recipes.
    """
    if request.method == "POST":
        ingredients = request.form.get("ingredients")
        ranking = request.form.get("minimaze")
        raw_recipes = get_recipes(ingredients, ranking)

        if (raw_recipes != False):
            processed_recipes = process_json(raw_recipes)
            if (processed_recipes == False):
                flash("Be sure you input existing ingredients separated by commas.")
                return render_template("search.html", user=current_user)
            else:      
                return render_template("search.html", recipes=processed_recipes, user=current_user)
        else:
            print("Api request failure.")
            flash("Something is wrong. We are sorry.")
            return render_template("search.html", user=current_user)
    else:
        return render_template("search.html", user=current_user)

