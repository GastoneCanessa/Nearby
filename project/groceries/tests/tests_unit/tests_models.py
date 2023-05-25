from django.test import TestCase
from groceries.models import Greengrocer, Post
from django.contrib.auth.models import User
from datetime import datetime


class SetUp(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Test_user",
            password="una_password_non_decifrabile",
        )

        self.greengrocer = Greengrocer.objects.create(
            name='Test_seller', 
            description='Test description',
            user=self.user, 
            email='test.user@email.com', 
            tel=123456789,
            city='Campagnano di Roma',
            address='Via della dottrina 46',
            zip_code=63            
            )


class GreengrocerTestCase(SetUp):

    def test_greengrocer_object(self):
        
        self.assertEqual(self.greengrocer.name, 'Test_seller')
        self.assertEqual(self.greengrocer.description, 'Test description')
        self.assertEqual(self.greengrocer.email, 'test.user@email.com')
        self.assertEqual(self.greengrocer.city, 'Campagnano di Roma')
        self.assertEqual(self.greengrocer.address, 'Via della dottrina 46')
        self.assertEqual(self.greengrocer.user, self.user)
        self.assertEqual(self.greengrocer.location.coords, (42.1497108, 12.381129))
        self.assertEqual(self.greengrocer.zip_code, 63)


class PostTestCase(SetUp):

    def test_post_object(self):
        self.post = Post.objects.create(
            title='Test_post',
            content='Test description',
            greengrocer=self.greengrocer
        )

        self.assertEqual(self.post.title, 'Test_post')
        self.assertEqual(self.post.content, 'Test description')
        self.assertEqual(self.post.greengrocer.name, 'Test_seller')
        self.assertEqual(self.post.date_posted.strftime("%d/%m/%Y %H:%M"), datetime.now().strftime("%d/%m/%Y %H:%M"))
