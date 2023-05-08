import string
import secrets
import smtplib as spl
import os
from dotenv import load_dotenv
from pathlib import Path
from . import db
from .models import User
from werkzeug.security import generate_password_hash

# In secret.env are secret variables, so we will load that file
load_dotenv()
# And get the variables from
MY_EMAIL=os.getenv('EMAIL')
KEY=os.getenv('PASSWORD')
# generate a random password
def generate_password():
    """
    Generates random password.
    """
    char_list = [secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) 
                for i in range(15)]
    return "".join(char_list)

def change_and_inform(email):
    """
    Function changes the user password and send email with the new password.
    """
    new_password = generate_password()
    try:
        # Try to send the email.
        with spl.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=KEY)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject:Your new password!\n\nYour new password for Recipisimo is: {new_password}"
            )
        # Update the password
        user = User.query.filter_by(email=email).first()
        user.password = generate_password_hash(new_password)
        db.session.commit()
    # if problem return False.
    except spl.SMTPException as e:
        print(e)
        return False

