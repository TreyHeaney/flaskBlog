from flask import render_template, url_for, redirect
from blog.models import Post
from blog.login_form import Login
from blog import app


posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route('/')
@app.route('/home')
@app.route('/home/')
def home():
    return render_template('home.html', posts=posts)
    
    
#####################################################################
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
    

@app.route('/admin', methods=['GET', 'POST'])
def admin():
	login = Login()
	if login.validate_on_submit():
		if login.username.data == 'admin' and login.password.data == 'password':
			return redirect(url_for('newpost'))
	return render_template('login.html', 
						   title='Admin Login',
						   form=login)


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
	return render_template('newpost.html', title='New Post')


@app.route('/playground')
def play():
    return render_template('playground.html', 
    					   title='Garbage')
