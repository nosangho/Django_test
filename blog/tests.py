from django.test import TestCase, Client
from bs4 import BeautifulSoup
from. models import Post, Category
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

def create_post(title, content, author, category=None):
    blog_post = Post.obects.create(
        title = title,
        content =  content,
        created = timezone.now(),
        author = author,
        category = category,
    )

    return blog_post

def create_category(name='life', description=''):
    category, is_created = Category.objects.get_or_create(
        name = name,
        description = description
    )
    return category


class TestView(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)


class TestModel(TestCase):
    def setUp(self):
        self.client = Client()
        self.author_000 = User.objects.create(username='nosangho', password='8121438n')

    def test_category(self):
        category = create_category()

    # def test_post(self):
    #     category = create_category()
    #     post_000 = create_post(
    #         title='first post',
    #         content = 'hello world welcome to python',
    #         author = self.author_000,
    #         category = category
    #     )