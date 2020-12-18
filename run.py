#####################################################################
## APP STRUCTURE
## run.py > __init__.py > routes.py
## 1. run.py is ran directly or through flask run
## 2. run.py imports blog and blog runs __init__.py
## 3. __init__.py runs routes.py
## 
## APP TREE
##
## flaskblog
## ├── blog
## │   ├── __init__.py
## │   │   # Initializes environment, configs, db, and bcrypt.
## │   ├── models.py
## │   │   # Holds our input forms and SQL models.
## │   ├── routes.py
## │   │   # Buillds the site and and ties together html.
## │   └── templates
## │       │   # Holds the HTML for pages in routes.py. 
## │       ├── about.html
## │       ├── blog_page.html
## │       ├── home.html
## │       ├── layout.html
## │       ├── login.html
## │       ├── newpost.html
## │       └── playground.html
## ├── Pipfile
## ├── Pipfile.lock
## ├── requirements.txt
## └── run.py
##     # Specifcally for starting the app.
#####################################################################
from blog import app

# ... and runs the app if ran manually.
if __name__ == '__main__':
	app.run(debug=True)

