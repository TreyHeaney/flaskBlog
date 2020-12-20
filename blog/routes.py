"""
Here, we set the app's routes to their according html sheets and implement most
backend logic.
"""

# TODO:
# > Better unit tests
# > Markdown editor.
# > Markdown parser.
# > Change SQL datatype for posts to BLOB and statically store assets.

# Standard library.
from random import randint, choice
from os import getenv

# Third party.
from flask import render_template, url_for, redirect
from flask_login import login_user, logout_user, current_user, login_required

# Local.
from blog.models import Post, User, Login, PostForm, splashes
from blog import app, crpt, db

posts = Post.query.all()
projects = [post for post in posts if post.project]
blogs = [post for post in posts if not post.project]


def build_site():
    # Home/projects only page.
    @app.route('/')
    @app.route('/home')
    @app.route('/home/')
    def home():
        splash = choice(splashes)
        return render_template('home.html', posts=projects, splash=splash)

    # Blog posts only page.
    @app.route('/blog')
    @app.route('/blog/')
    def blog():
        splash = choice(splashes)

        return render_template('blog_page.html', title='Blog', posts=blogs,
                               splash=splash)

    # About page.
    @app.route('/about')
    @app.route('/about/')
    def about():
        splash = choice(splashes)

        return render_template('about.html', title='About', splash=splash)

    # Individual post pages.
    @app.route('/posts/<int:post_id>')
    def post(post_id):
        splash = choice(splashes)

        # Get post by ID entered in URL.
        post = Post.query.get_or_404(post_id)

        return render_template('post.html', title=post.title, post=post,
                               splash=splash)

    # Admin login page.
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        if current_user.is_authenticated:
            return redirect(url_for('new_post'))
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
                    return redirect(url_for('new_post'))

        admin_splashes = ['Secret admin page!', 'No funny business!',
                          'Oooooh... mysterious!', 'Login to the mainframe!']
        admin_splash = choice(admin_splashes)
        return render_template('login.html', title='Admin Login', form=login,
                               splash=admin_splash)

    # Update individual post pages.
    @app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        global projects, blogs
        # Double login check.
        if not current_user.is_authenticated:
            return redirect(url_for('home'))

        post = Post.query.get_or_404(post_id)
        form = PostForm()
        # Runs if the form is submitted.
        if form.validate_on_submit():
            # Updates queried posts' information and recommits it.
            post.title = form.title.data
            post.content = form.body.data
            db.session.commit()
            # Updates posts in memory for current session.
            # !DEV!
            posts = Post.query.all()
            projects = [post for post in posts if post.project]
            blogs = [post for post in posts if not post.project]

            return redirect(url_for('post', post_id=post.id))

        form.title.data = post.title
        form.body.data = post.content
        return render_template('newpost.html', title='Update Post', form=form)

    # Delete individual post pages
    @app.route('/posts/<int:post_id>/delete', methods=['GET', 'POST'])
    @login_required
    def delete_post(post_id):
        global projects, blogs

        if not current_user.is_authenticated:
            return redirect(url_for('home'))

        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()

        # !DEV!
        posts = Post.query.all()
        projects = [post for post in posts if post.project]
        blogs = [post for post in posts if not post.project]
        return redirect(url_for('home'))

    @app.route('/new_post', methods=['GET', 'POST'])
    @login_required
    def new_post():
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
            # !DEV!
            posts = Post.query.all()
            projects = [post for post in posts if post.project]
            blogs = [post for post in posts if not post.project]
            return redirect(url_for('home'))
        return render_template('newpost.html', title='New Post', form=form)

    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))


    @app.route('/playground')
    def play():
        return render_template('playground.html',
                               title='Garbage')


build_site()
