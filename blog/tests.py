from django.test import TestCase, Client
from bs4 import BeautifulSoup

# Create your tests here.
class TestView(TestCase):
    def SetUp(self):
        self.client = Client()

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content, 'html.parser')

        navbar = soup.find('div', id='navbar')
        self.assertIn('Blog', navbar.text)