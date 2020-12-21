"""Table formats for the database and website post forms"""

# Standard library.
from datetime import datetime
from random import randint

# Third party.
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    TextAreaField
from wtforms.validators import DataRequired

# Local.
from blog import db, logins


@logins.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# An empty row for our SQL post database.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    project = db.Column(db.Boolean, nullable=False)
    # link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"POST:: ID: {self.id}, TITLE: {self.title}, DATE: {self.date_posted}, CONTENT: {self.content}, PROJECT: {self.project}"


# An empty row for our SQL user database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    date_registered = db.Column(db.DateTime(), nullable=False,
                                default=datetime.utcnow)
    password_hash = db.Column(db.Text, nullable=False)

    def __rep__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# Form for our admin page login.
class Login(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Content', validators=[DataRequired()])
    project = BooleanField('Project')
    submit = SubmitField('Post')


# Splash text
splashes = ['Not a work in progress!', 'Not FDA approved!',
            'Everything is logged!', "He's reading the splash text!",
            'Is this thing on?!', '　Welcome to my blog!', '　Your text here!',
            "　　<class 'str'>", f"Here's a random number: {randint(0, 1000)}!",
            '　　Hosted on AWS!', 'SECRET PAGE: /admin!',
            'Open source, closed enviornment!', '　Cloud computing!',
            '　PEP8 compliant!', 'Do not redistribute!', '　　idspispopd!',
            '<a style="color:yellow;">', '　　I love my mom!',
            'Written with Pycharm!', 'Made with Flask!', '　　　P is NP!',
            'The Heaney is Irish!']