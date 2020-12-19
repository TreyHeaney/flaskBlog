# Here the apps' routes and their according html sheets are set.

# TODO:
# - Split blogs/projects into two individual CSVs upon adding each post so an
#   SQL query isn't done every time someone loads the page.

from random import randint, choice
from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required
from os import getenv
from blog.models import Post, User, Login, PostForm,splashes
from blog import app, crpt, db

posts = Post.query.all()
projects = [post for post in posts if post.project]
blogs = [post for post in posts if not post.project]


def build_site():
    @app.route('/')
    @app.route('/home')
    @app.route('/home/')
    def home():
        splash = choice(splashes)
        return render_template('home.html', posts=projects, splash=splash)

    @app.route('/blog')
    @app.route('/blog/')
    def blog():
        splash = choice(splashes)

        return render_template('blog_page.html', title='Blog', posts=blogs,
                               splash=splash)

    @app.route('/about')
    @app.route('/about/')
    def about():
        splash = choice(splashes)

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

        admin_splashes = ['Secret admin page!', 'No funny business!',
                          'Oooooh... mysterious!', 'Login to the mainframe!']
        admin_splash = choice(admin_splashes)
        return render_template('login.html', title='Admin Login', form=login,
                               splash=admin_splash)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))

    # PAGE FOR NEW POSTS.
    @app.route('/newpost', methods=['GET', 'POST'])
    @login_required
    def newpost():
        global projects, blogs

        form = PostForm()

        if form.validate_on_submit():
            # Creates a new row in the post table.
            post = Post(title=form.title.data, content=form.body.data,
                        project=form.project.data)
            # Adds the post and commits the modified table to the database.
            db.session.add(post)
            db.session.commit()
            # Refreshes the posts in memory with the new post. 
            posts = Post.query.all()
            projects = [post for post in posts if post.project]
            blogs = [post for post in posts if not post.project]
            return redirect(url_for('home'))

        return render_template('newpost.html', title='New Post', form=form)

    @app.route('/playground')
    def play():
        return render_template('playground.html',
                               title='Garbage')


build_site()
