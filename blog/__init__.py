from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b7f21a51321de54dce0c6b3fda7277bdf59dac281204a00b9e40a3a11ea7f858'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///env/site.db"

db = SQLAlchemy(app) 

from blog import routes
