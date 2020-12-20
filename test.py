"""Hyper basic unit tests"""

import unittest
from blog import app
from blog.models import Post


routes = ['/', '/home', '/blog', '/about', '/admin', '/new_post']

posts = Post.query.all()
for post in posts:
    routes.append(f'/posts/{post.id}')
    routes.append(f'/posts/{post.id}/edit')


class FlaskTest(unittest.TestCase):

    def test_status(self):
        for route in routes:
            tester = app.test_client(self)
            response = tester.get(route, content_type='html/text')
            try:
                self.assertIn(response.status_code, [200, 302, 308])
            except AssertionError as e:
                print(e)
                print(f'_-_-STATUS ERROR: {response.status_code} ON {route}_-_-')
                self.fail()


if __name__ == '__main__':
    unittest.main()