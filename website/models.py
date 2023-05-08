from website import db
from flask_login import UserMixin

# UserMixin is associated with current_user used in auth
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

