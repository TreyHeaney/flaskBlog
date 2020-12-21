# Standard library.
from os import getenv

# Third party.
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flaskext.markdown import Markdown  # Might be depreciated soon.

# Loads environment variables for secret things...
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = getenv('SECRET_KEY')		
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')

logins = LoginManager(app)
crypt = Bcrypt(app)
db = SQLAlchemy(app)
markdown = Markdown(app)

logins.login_view = 'admin'

from blog import routes
