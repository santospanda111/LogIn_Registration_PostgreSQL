import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from mixer.backend.django import mixer
from note.models import Notes
import json

@pytest.mark.django_db
class TestNoteAPI:
    def test_create_note(self,client):
        """ This method will test the post method is creating the Note or not."""
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        url = reverse('user_login')
        data = {
            "username": "raghu",
            "password": "raghu123"
        }
        response= client.post(url, data)
        content= json.loads(response.content)
        print(response.content)
        token= content['data']['token']
        data = {
                 'title':'san', 
                 'description':'descsan'
                }
        header= {"HTTP_AUTHORIZATION": token}
        url = reverse('notes')
        response = client.post(url, data, **header, content_type='application/json')
        print(response.content)
        assert response.status_code == 200

    def test_get_data(self,client):
        """ This method will test the get method is getting the data or not."""
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        url = reverse('user_login')
        data = {
            "username": "raghu",
            "password": "raghu123"
        }
        response= client.post(url, data)
        content= json.loads(response.content)
        print(response.content)
        token= content['data']['token']
        header= {"HTTP_AUTHORIZATION": token}
        url = reverse('notes')
        note1 = mixer.blend(Notes,pk=1)
        response1 = client.get(url,**header,content_type='application/json')
        assert response1.status_code == 200

    def test_update_note(self,client):
        """ This method will test the put method is updating the values or not."""
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        url = reverse('user_login')
        data = {
            "username": "raghu",
            "password": "raghu123"
        }
        response= client.post(url, data)
        content= json.loads(response.content)
        print(response.content)
        token= content['data']['token']
        header= {"HTTP_AUTHORIZATION": token}
        url = reverse('notes')
        user = mixer.blend(Notes,id=1, title="san", description="descsan")
        data = {'note_id':1,
                 'title':'santo', 
                 'description':'descsan'
                }
        response=client.put(url,data, **header, content_type='application/json')
        assert response.status_code == 200

    def test_delete_note(self,client):
        """ This method will test the delete method is deleting the note or not."""
        user = User.objects.create_user(username="raghu", password="raghu123", email="raghu@gmail.com", first_name="raghu",
                                    last_name="Ram")
        user.save()
        url = reverse('user_login')
        data = {
            "username": "raghu",
            "password": "raghu123"
        }
        response= client.post(url, data)
        content= json.loads(response.content)
        print(response.content)
        token= content['data']['token']
        header= {"HTTP_AUTHORIZATION": token}
        url = reverse('notes')
        user = mixer.blend(Notes,id=1, title="san", description="descsan")
        data = {'note_id':1}
        response=client.delete(url,data, **header, content_type='application/json')
        assert response.status_code == 200