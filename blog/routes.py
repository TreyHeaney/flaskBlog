"""
Here, we set the app's routes to their according html sheets and implement most
backend logic.
"""

# TODO:
# > Better unit tests

# Standard library.
from random import randint, choice
from datetime import datetime

# Third party.
from flask import render_template, url_for, redirect, request, Flask
from flask_login import login_user, logout_user, current_user, login_required

# Local.
from blog.models import Post, User, Login, PostForm
from blog.backend import log, splashes
from blog import app, crypt, db, markdown


# Refresh our posts-in memory for changes to the database.
# DEV-like, might remove later; This isn't necessary for new instances, but
# only for the instance used to edit/delete/make the post.
def refresh_posts():
    global projects, blogs
    posts = Post.query.order_by(Post.date_posted.desc())
    projects = [post for post in posts if post.project]
    blogs = [post for post in posts if not post.project]


refresh_posts()


def build_site():
    @app.before_request
    def logger():
        POST = request.path
        print(dir(request))
        print(request.origin)
        print(request.referrer)
        log(request)

    # Home/projects only page.
    @app.route('/')
    @app.route('/home')
    @app.route('/home/')
    def home():
        return render_template('home.html', posts=projects,
                               splash=choice(splashes))

    # Blog posts only page.
    @app.route('/blog')
    @app.route('/blog/')
    def blog():
        return render_template('blog_page.html', title='Blog', posts=blogs,
                               splash=choice(splashes))

    # About page.
    @app.route('/about')
    @app.route('/about/')
    def about():
        return render_template('about.html', title='About',
                               splash=choice(splashes))

    # Individual post pages.
    @app.route('/posts/<int:post_id>')
    def post(post_id):
        # Get post by ID entered in URL.
        post = Post.query.get_or_404(post_id)

        # Read/parse markdown file for post in URL.
        content = open(f'./var/{post.content}')
        content = markdown(content.read())

        return render_template('post.html', title=post.title, post=post,
                               splash=choice(splashes), content=content)

    # Admin login page.
    @app.route('/admin', methods=['GET', 'POST'])
    def admin():
        # This entire login structure can support multiple users with the SQL
        # backend, but I'll probably only have a single 'admin' user.

        # Checks if the user is currently logged in.
        if current_user.is_authenticated:
            return redirect(url_for('new_post'))
        login = Login()  # Login input form.
        # Runs if the login button is clicked (SEE login.html LINE 24)
        if login.validate_on_submit():
            password = login.password.data
            user = User.query.filter_by(username=login.username.data).first()

            # Checks if a user has the current name
            if user:
                # Check if the password is correct for the current user DB row.
                if crypt.check_password_hash(user.password_hash, password):
                    login_user(user, remember=login.remember.data)
                    return redirect(url_for('new_post'))

        admin_splashes = ['Secret admin page!', 'No funny business!',
                          'Oooooh... mysterious!', 'Login to the mainframe!']
        admin_splash = choice(admin_splashes)
        return render_template('login.html', title='Admin Login', form=login,
                               splash=admin_splash)

    # Update- individual post pages.
    @app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_post(post_id):
        global projects, blogs
        if not current_user.is_authenticated:
            return redirect(url_for('home'))

        # Query post in URL and open static .md file.
        post = Post.query.get_or_404(post_id)
        content = open(f'./var/{post.content}', 'r+')

        form = PostForm()
        # Runs if the form is submitted.
        if form.validate_on_submit():
            # Updates queried posts' information and recommits it.
            if post.title != form.title.data:
                post.title = form.title.data
                db.session.commit()
                # !DEV!
                refresh_posts()

            content.write(form.body.data)

            return redirect(url_for('post', post_id=post.id))

        # Populate form with pre-existing data.
        form.title.data = post.title
        form.body.data = content.read()
        return render_template('newpost.html', title='Update Post', form=form)

    # Delete- individual post pages
    @app.route('/posts/<int:post_id>/delete', methods=['GET', 'POST'])
    @login_required
    def delete_post(post_id):
        global projects, blogs

        if not current_user.is_authenticated:
            return redirect(url_for('home'))

        # Query for post id in URL and delete it from the db.
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()

        # !DEV!
        refresh_posts()

        return redirect(url_for('home'))

    # New post creation.
    @app.route('/new_post', methods=['GET', 'POST'])
    @login_required
    def new_post():
        global projects, blogs

        form = PostForm()
        if form.validate_on_submit():
            # Generate a random hash for our .md filename
            hash_ = ''.join(choice('ABCDEFGHIJK1234567890') for i in range(16))
            path = f'var/{hash_}.md'  # Path to our new .md file.
            # Create and write to the new .md file.
            content_file = open(path, 'x')
            content_file.write(form.body.data)
            # Creates a new row in the post table.
            post = Post(title=form.title.data, content=hash_ + '.md',
                        project=form.project.data)
            # Adds the post and commits the modified table to the database.
            db.session.add(post)
            db.session.commit()
            # Refreshes the posts in memory with the new post.
            # !DEV!
            refresh_posts()

            return redirect(url_for('home'))
        return render_template('newpost.html', title='New Post', form=form)

    # Logout.
    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('home'))


build_site()
