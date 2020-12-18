from blog import db
from blog.models import Post

# db.create_all()

# content1 = 'In this project post, I say absolutely nothing of substance'
# post1 = Post(title='A new way to do stuff', content=content1, project=True, link='/the-project')
# post2 = Post(title='A predictive model for your company!', content=content1, project=True, link='/second-project')
# post3 = Post(title='Ipsum Lorem', content=content1, project=True, link='/third-project')
# posts = [post1, post2, post3]

posts = Post.query.all()

for post in posts:
	print(posts.date_posted)

