# Here's pretty much all the backend for my admin login/post mgmt.
from datetime import datetime
from random import randint, choice
from blog import db, logins
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


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
    link = db.Column(db.Text, nullable=False)

    def __rep__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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


# Splash text
prefix = ['Poor ', 'Common ', 'Uncommon ', 'Rare ', 'Epic ', 'Legendary ']
midfix = ['Helm ', 'Sword ', 'Blade ', 'Spaulders ', 'Pants ', 'Vest ',
          'Boots ']
suffix = ['of the Aurora ', 'of the Wolf ', 'of the Squire', 'of the Thief',
          'of the Mind', 'of Striking', 'of the Wildfire ']

splashes = ['Not a work in progress!', 'Not FDA approved!',
            'Everything is logged!', "He's reading the splash text!",
            '　Manual breathing!', '　The cake is a lie!', 'Is this thing on?!',
            '　Welcome to my blog!', '　Your text here!', "　　<class 'str'>",
            f"Here's a random number: {randint(0, 10)}!", 'Hosted on AWS!',
            'SECRET PAGE: /admin!', 'Open source, closed enviornment!',
            '　Cloud computing!', '　PEP8 compliant!', 'Do not redistribute!',
            '　　idspispopd!', '<a style="color:yellow;">',
            'Written with Pycharm!', 'Written with Flask!',
            'Written with vim!', 'Written with gedit!',
            '　　　P is NP!', 'Funding secured!',
            choice(prefix) + choice(midfix) + choice(suffix),
            choice(prefix) + choice(midfix) + choice(suffix),
            choice(prefix) + choice(midfix) + choice(suffix),
            choice(prefix) + choice(midfix) + choice(suffix),]