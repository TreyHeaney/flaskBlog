# Here's pretty much all the backend for my admin login/post mgmt.
from datetime import datetime
from blog import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


# An empty post row for our SQL database. 
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime(), nullable=False, 
							default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	project= db.Column(db.Boolean, nullable=False)
	link = db.Column(db.Text, nullable=False)
	
	def __rep__(self):
		return f"Post('{self.title}', '{self.date_posted}')"


# Form for our admin page login.
class Login(FlaskForm):
	username = StringField('Username',
						   validators=[DataRequired()])
	password = PasswordField('Password',
							 validators=[DataRequired()])
	submit = SubmitField('Login')
