from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from groceries.models import Greengrocer, Post
from rest_framework.authtoken.models import Token


class RegistrationTestCase(APITestCase):

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
                "password1": "change_me_123", "password2": "change_me_123"}
        response = self.client.post("/api/dj-rest-auth/registration/", data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostViewSetTestCase(APITestCase):
    list_url = reverse("post-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase",
            password="bad_password"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.greengrocer = Greengrocer.objects.create(
            name='test_greengrocer',
            description='description',
            user=self.user,
            email='email@email.com',
            tel=3288352,
            city='campagnano di roma',
            address='via della dottrina',
            zip_code=63,

        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
   
    def test_post_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_post_create(self):
        data = {
            "title": "first_post",
            "content": "bad_content"
        }
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 1) 
        self.assertEqual(response.data["greengrocer"], "test_greengrocer") 
        self.assertEqual(response.data["title"], "first_post")   
        self.assertEqual(response.data["content"], "bad_content") 

    def test_posts_retrieve(self):
        self.post = Post.objects.create(
            title="first_post",
            content="bad_content",
            greengrocer=self.greengrocer
        )
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
           
    def test_post_detail_retrieve(self):
        self.post = Post.objects.create(
            title="first_post",
            content="bad_content",
            greengrocer=self.greengrocer
        )
        response = self.client.get("/api/posts/", pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_post_upload_immage(self):
    #     self.post = Post.objects.create(
    #         title="first_post",
    #         content="bad_content",
    #         greengrocer=self.greengrocer
    #     )
    #     files = {
    #         "immage_url": open('/home/gastone/projects/Nearby/project/groceries/tests/tests_integration/Copia.jpg', 'rb').read()
    #     }
    #     response = self.client.put("/api/immage/1", files=files)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)


class GocerieViewSetTestCase(APITestCase):
    list_url = reverse("greengrocer-list")

    def setUp(self):
        self.user = User.objects.create_user(
            username="testcase",
            password="bad_password"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        self.greengrocer = Greengrocer.objects.create(
            name='test_greengrocer',
            description='description',
            user=self.user,
            email='email@email.com',
            tel=3288352,
            city='campagnano di roma',
            address='via della dottrina',
            zip_code=63,

        )

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_greengrocer_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_greengrocer_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK) 

    def test_greengrocer_create(self):
        self.user = User.objects.create_user(
            username="testcase2",
            password="bad_password"
        )
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

        data = {
            "user": "testcase2",
            "name": "Gastone shop",
            "description": "post",
            "email": "gastonnepost@gmail.com",
            "tel": 4344124,
            "city": "CAMPAGNANO DI ROMA",
            "address": "via della dottrina 46",
            "zip_code": 63
        }   

        response = self.client.post("/api/nearby/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["id"], 2) 
        self.assertEqual(response.data["user"], "testcase2") 
        self.assertEqual(response.data["description"], "post")   
        self.assertEqual(response.data["email"], "gastonnepost@gmail.com") 
        self.assertEqual(response.data["tel"], 4344124) 
        self.assertEqual(response.data["city"], "CAMPAGNANO DI ROMA")   
        self.assertEqual(response.data["address"], "via della dottrina 46") 
        self.assertEqual(response.data["zip_code"], 63) 

    def test_greengrocers_retrieve(self):
        response = self.client.get("/api/nearby/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_greengrocer_detail_retrieve(self):
        response = self.client.get("/api/nearby/", pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_greengrocer_update(self): 
    #     data = {
    #         "name": "Gastone shop",
    #         "description": "post",
    #         "email": "gastonnepost@gmail.com",
    #         "tel": 4344124,
    #         "city": "CAMPAGNANO DI ROMA",
    #         "address": "via della dottrina 46",
    #         "zip_code": 63
    #     }   
    #     response = self.client.put("/api/nearby/", pk=1, data=data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["id"], 1) 
    #     self.assertEqual(response.data["user"], "testcase") 
    #     self.assertEqual(response.data["description"], "post")   
    #     self.assertEqual(response.data["email"], "gastonnepost@gmail.com") 
    #     self.assertEqual(response.data["tel"], 4344124) 
    #     self.assertEqual(response.data["city"], "CAMPAGNANO DI ROMA")   
    #     self.assertEqual(response.data["address"], "via della dottrina 46") 
    #     self.assertEqual(response.data["zip_code"], 63) 