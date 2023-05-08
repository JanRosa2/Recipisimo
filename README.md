# PROJECT RECIPISIMO
### Video Demo:  https://youtu.be/LEBgw-EPX1w
### Description:
-------------------------------------------------------------------------------------------------------------
```
This web application helps people to discover meals that they can cook from the specified ingredients. So if you don't know what to cook from the ingredients in your fridge, this is exactly for you. It is powered by Spoonacular API ("https://spoonacular.com/food-api/docs#Search-Recipes-by-Ingredients"). The use is limited (when free) so it requires to register for now. So the registration, login, logout, changing password and recovering password by email is included in this project.
```

### Design:
--------------------------------------------------------------------------------------------------------------
```
The RECIPISIMO uses a framework Flask. Because Flask demands specific folders for storing the files, the folders "static" and "templates" are created. "Static" for storing the static parts of the web application and "templates" which are used for rendering routes. In the folder "templates" is a file called "layout.html" and this is the main layout for other templates thanks to "Jinja" templating engine. "Jinja" is also used here for a dynamic web pages. In the folder "static" there is a file styles.css storing all of the css styles used for this project. Note that in this project a CSS framework "bootstrap" is mainly used for the design. There is also script.js taking care of active links. 

The RECIPISIMO uses a database solution for everything around the user authentication. It uses SQLite3 system, but to make it less vulnerable to injection attacks, all the queries are made by the object relational mapper SQLAlchemy - here it is Flask-SQLAlchemy. The database file itself can be found in the folder "instance". 

The main app function is written in the "__init__.py" file so whole website folder is treated as a package. And the app itself is created and launched in the "main.py". The routes are organized into two python files. A file "auth.py" defines routes for an authentication purpose. A file "views.py" defines routes for other purposes. The main reason is to make whole app into smaller modules, so it is easier to maintain it as the app grows.
```

### Common files
-------------------------------------------------------------------------------------------------------------
1. __init__.py 
```
The definition of the app itself is in the function "Create_app()". The function returns the app itself. It is there where the SQLAlchemy integration object is set up and connected with the app and also the database is created. The database is created thanks to a model Class User from the "models.py" by function create_all() from SQLAlchemy. The blueprints for the routes (in files "auth.py", "views.py") are registered there and also the url prefixes are set up for them. It also configures sessions and set up a login manager.
```
2. .env
```
Is used for storing environment variables separately. The logic behind is we don't want to hardcode our sensitive data, because everyone working with the code can see it. 
```
3. models.py
```
Is there to make the model of the database we are going to communicate with. So we can communicate and commit to the database itself through this "template". It declares a class User which represent a database table. 
```
### The route files
--------------------------------------------------------------------------------------------------------------
```
The route files holds the blueprints. Those blueprints are registered to the main app in file "__init__.py". The routes are associated with those blueprints and provides a modularity to the flask app (see https://flask.palletsprojects.com/en/2.2.x/blueprints/ for more).
```

1. auth.py
```
Contains the authentication routes. It tackles user registration, login, logout and changing the passwords. Note that almost every route is decorated by login_required. It makes sure that the user is authenticated and has rights to view the route. It is registered in the Flask app with the url prefix "/auth".

route("/login")
def login():
A function for login a user. In case the user exists, it is going to check the provided password. If successful the user is logged in. The function "login_user" from module flask_login is used here to remember the user with session.
    
route("/logout")
def logout():
The function for logout the user and remove the session.

route("/register")
def register():
It will make instance of the User model and will pass password and email to it. With this instance of the User model it will add new_user to the database a set up new session as well.
    
route("/resetpassword")
def reset_password():
The main purpose is to give an authenticated user an option for changing the password.
    
route("/recoverpassword")
def recover_password():
If the user does not remember a password. The password can be recovered and the email with the new password will be send. Note for that we use helper function "change_and_inform()" from the "rstpass.py" file. This function will be discussed later in this file.
```
2. views.py
```
Containes the routes that tackles other problems than the authentication.

route("/")
def index():
Renders index page.
    
route("/search")
def search_recipes():
Searches for recipes. It uses helper functions from the file "recipes.py" to get response from the Spoonacular API.
```

### The helper files
-------------------------------------------------------------------------------------------------------------
```
There are two helper files - rstpass.py and recipes.py. 
```
1. recipes.py
```
The purpose is to provide functions for requesting the "Spoonacular API" and return formated data for the project needs.

def get_recipes(ingredients, ranking): 
This function returns recipes in JSON format through API "Spoonacular" depending on users ingrediens.
Also the parameters for the request are declared there. It returns False if something is wrong.
    
def process_json(data_json):
This function processes the json data requested through "Spoonacular" API to make it more organized and more relevant for the project. If there are no data it returns False.
```
2. rstpass.py
```
Provides functions for generating new random password. It also sending email with new password to the user and updates the password in the database itself.

def generate_password():
Generates random password. It generates random lower and upper characters + random numbers. In the end it returns as the string.
    
def change_and_inform(email):
Function changes the user password and send email with the new password.
```

### main.py
--------------------------------------------------------------------------------------------------------------
```
In the main.py is actually where the instance of the app is created and where we run our app. The app can be only run from that file. It is because it checks if we run the app exactly by running this file.
```

### Future plans:
--------------------------------------------------------------------------------------------------------------
```
The thing is it would be nice to build own database of ingredients and the descriptions of the recipes. 
Also allow users to make their own recipes and enable to manage their already created recipes is planned in the future. Also building API endpoints is considered.
```















    

