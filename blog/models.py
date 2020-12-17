from datetime import datetime
from blog import db


class Admin(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	username = db.Column(db.String(20), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)

	def __rep__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True, nullable=False)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	link = db.Column(db.Text, nullable=False)
	
	def __rep__(self):
		return f"Post('{self.title}', '{self.date_posted}')"
