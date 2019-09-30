from django.test import TestCase, Client
from bs4 import BeautifulSoup
from. models import Post
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

def create_post(title, content, author):
    blog_post = Post.obects.create(
        title = title,
        content =  content,
        created = timezone.now(),
        author = author
    )

    return blog_post


class TestView(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)