import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer



@pytest.mark.django_db
class TestLogInAPI:
    def test_register_view(self,client):
        """ This method will test the post method is registering the user-data or not."""
        url = reverse('user_registration')
        data = {'first_name':'soumyaranjan',
                 'last_name':'panda', 
                 'email':'soumyaranjan111@gmail.com',
                 'username':'soumya0', 
                 'password':'soumya1'
                }
        response = client.post(url, data)
        print(response)
        assert response.status_code == 200

    def test_registration_with_duplicate_username(self, client):
        """ This method will test the post method is accepting duplicate username or not"""
        url = reverse('user_registration')
        user = mixer.blend(User, username='soumya0')
        user.save()
        data = {'first_name':'soumyaranjan',
                 'last_name':'panda', 
                 'email':'soumyaranjan111@gmail.com',
                 'username':'soumya0', 
                 'password':'soumya1'
                }
        response = client.post(url, data)
        assert response.status_code == 400

    def test_login_successful_with_valid_credentials(self, client):
        """ This method will test the login-post method is loggedin with the valid-values or not."""
        url = reverse('user_login')
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        data = {
            "username": "raghu",
            "password": "raghu123"
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == 200

    def test_login_unsuccessful_with_invalid_credentials(self, client):
        """ This method will test the login-post method is loggedin with the invalid-values or not."""
        url = reverse('user_login')
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        data = {
            "username": "raghu",
            "password": "raghu"
        }
        response = client.post(url, data, content_type='application/json')
        assert response.status_code == 400