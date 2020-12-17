# Here the apps' routes and their according html sheets are set.

from flask import render_template, url_for, redirect
from os import getenv
from blog.models import Post, Login
from blog import app, crpt


# TODO: REPLACE THIS WITH THE SQL DATABASE
posts = [
    {
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018',
        'project': False,
    },
    {
        'title': 'Project 1',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
        'project': True,
    },
    {
        'title': 'Project 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018',
        'project': True,
    },
]

projects = [post for post in posts if post['project']]
blogs = [post for post in posts if not post['project']]


def build_site():
	@app.route('/')
	@app.route('/home')
	@app.route('/home/')
	def home():
		return render_template('home.html', posts=projects)
		
	@app.route('/blog')
	@app.route('/blog/')
	def blog():
		return render_template('blog_page.html', 
							   title='Blog', 
							   posts=blogs)

	@app.route('/about')
	@app.route('/about/')
	def about():
		return render_template('about.html', title='About')	
#####################################################################

	# ADMIN LOGIN PAGE.
	@app.route('/admin', methods=['GET', 'POST'])
	def admin():
		# Empty Login class.
		login = Login()
		# Runs if the login button is clicked (SEE login.html LN 20)
		if login.validate_on_submit():
			password = login.password.data
			# Check if the admin username is correct.
			if login.username.data == getenv('ADMIN_USER'):
				# Check if the password is correct.
				if crpt.check_password_hash(getenv('ADMIN_PASS'), 
											password):
					return redirect(url_for('newpost'))
		return render_template('login.html', 
							   title='Admin Login',
							   form=login)


	# PAGE FOR NEW POSTS.
	@app.route('/newpost', methods=['GET', 'POST'])
	def newpost():
		return render_template('newpost.html', title='New Post')


	@app.route('/playground')
	def play():
		return render_template('playground.html', 
							   title='Garbage')


build_site()

