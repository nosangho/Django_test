from django.test import TestCase, Client
from bs4 import BeautifulSoup
from. models import Post, Category, Tag
from django.utils import timezone
from django.contrib.auth.models import User

# Create your tests here.

def create_post(title, content, author, category=None):
    blog_post = Post.objects.create(
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

def create_tag(name='test_tag'):
    tag, is_created = Tag.objects.get_or_create(
        name=name,
    )
    tag.slug = tag.name.replace(' ', '-').replace('/','')
    tag.save()
    
    return tag



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

        post_000 = create_post(
            title = 'first post',
            content = 'good day comando',
            author=self.author_000,
            category = category
        )

    def test_tag(self):
        tag_000 = create_tag(name='good_boy')
        tag_001 = create_tag(name='korea')

        post_000 = create_post(
            title = 'first post',
            content = 'good day comando',
            author = self.author_000,
        )

        post_001 = create_post(
            title = 'Have a nice day post',
            content = 'This is Friday',
            author = self.author_000,
        )

        post_000.tags.add(tag_000)
        post_000.tags.add(tag_001)
        post_000.save()

        post_001.tags.add(tag_001)
        post_001.save()


        self.assertEqual(post_000.tags.count(), 2)
        self.assertEqual(tag_001.post_set.count(), 2)
        self.assertEqual(tag_001.post_set.first(), post_000)
        self.assertEqual(tag_001.post_set.last(), post_001)
        


    # def test_post(self):
    #     category = create_category()
    #     post_000 = create_post(
    #         title='first post',
    #         content = 'hello world welcome to python',
    #         author = self.author_000,
    #         category = category
    #     )