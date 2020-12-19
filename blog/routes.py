# Here the apps' routes and their according html sheets are set.

# TODO:
# - Split blogs/projects into two individual CSVs upon adding each post so an
#   SQL query isn't done every time someone loads the page.

from random import randint
from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, current_user
from os import getenv
from blog.models import Post, User, Login, splashes
from blog import app, crpt, db

# REPLACE THIS WITH TWO STATIC FILES CREATED BY SPLITTING POSTS UPON NEW POST.
posts = Post.query.all()
projects = [post for post in posts if post.project]
blogs = [post for post in posts if not post.project]


def build_site():
    @app.route('/')
    @app.route('/home')
    @app.route('/home/')
    def home():
        splash = splashes[randint(0, len(splashes) - 1)]
        return render_template('home.html', posts=projects, splash=splash)

    @app.route('/blog')
    @app.route('/blog/')
    def blog():
        splash = splashes[randint(0, len(splashes) - 1)]

        return render_template('blog_page.html', title='Blog', posts=blogs,
                               splash=splash)

    @app.route('/about')
    @app.route('/about/')
    def about():
        splash = splashes[randint(0, len(splashes) - 1)]

        return render_template('about.html', title='About', splash=splash)

    # ADMIN LOGIN PAGE.
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if current_user.is_authenticated:
            return redirect(url_for('newpost'))
        # Holds the login form input variables
        login = Login()
        # Runs if the login button is clicked (SEE login.html LINE 20)
        if login.validate_on_submit():
            password = login.password.data
            print(login.username.data)
            user = User.query.filter_by(username=login.username.data).first()

            # Checks if a user has the current name
            if user:
                # Check if the password is correct for the current user DB row.
                if crpt.check_password_hash(user.password_hash, password):
                    login_user(user, remember=login.remember.data)
                    return redirect(url_for('newpost'))

        return render_template('login.html', title='Admin Login', form=login)

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('home'))

    # PAGE FOR NEW POSTS.
    @app.route('/newpost', methods=['GET', 'POST'])
    def newpost():
        if not current_user.is_authenticated:
            return redirect(url_for('admin'))
        return render_template('newpost.html', title='New Post')

    @app.route('/playground')
    def play():
        return render_template('playground.html',
                               title='Garbage')


build_site()
