A blog I made for my projects with a simple SQL backend and post manager. 


PROJECT TREE

flaskBlog
├── blog			# Package wrapper for project. **
│   ├── __init__.py		# Initializes environment and backend.
│   ├── models.py		# Holds our input forms and SQL models.
│   ├── routes.py		# Builds the site and and ties together html.
│   └── templates		# Holds the HTML for pages in routes.py.
│       ├── about.html			# Page with some info about me.
│       ├── blog_page.html		# Page for blog posts only.
│       ├── home.html			# Page for project posts only.
│       ├── layout.html			# Layout that every page extends.
│       ├── login.html			# Admin login portal for...
│       ├── newpost.html		# ...the project/blog post/update page.
│	    └── playground.html		# Testing grounds.
├── Pipfile
├── Pipfile.lock
├── requirements.txt
└── run.py	# Specifically for starting the app.

**Wow this makes dealing with paths so much easier I love python.
