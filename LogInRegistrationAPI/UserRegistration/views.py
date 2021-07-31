from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializer import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError,AuthenticationFailed
from django.core.mail import EmailMultiAlternatives
from UserRegistration.utils import encode_token,decode_token,encode_token_userid
from django.db.models import Q


class Index(APIView):
    """
    [This method will return welcome message]
    """
    def get(self,request):
        return Response('Welcome to Login and Registration App')

class RegisterAPI(APIView):
    def get(self,request,pk=None):
        """This method will read the data from the table."""
        id = pk
        if id is not None:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


    def post(self,request):
        """[This method will take the required input and register it]

        Returns:
            [returns the message if successfully registered]
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if User.objects.filter(username=serializer.data.get('username')).exists():
                return Response({'message': 'Username is already registered with another user.'}, status=status.HTTP_400_BAD_REQUEST)
            # Register user
            user = User.objects.create_user(first_name=serializer.data.get('first_name'), last_name=serializer.data.get('last_name'), email=serializer.data.get('email'), username=serializer.data.get('username'), password=serializer.data.get('password'))
            # Save user
            user.save()
            user_name=serializer.data.get('username')
            user_id= User.objects.get(username=user_name).id
            print(user_id)
            token = encode_token(user_id,user_name)
            email= serializer.data.get("email")
            subject, from_email, to='Register yourself by complete this verification','santospanda111@gmail.com',email
            html_content= f'<a href="http://127.0.0.1:8000/verify/{token}">Click here</a>'
            text_content='Verify yourself'
            msg=EmailMultiAlternatives(subject,text_content,from_email,[to])
            msg.attach_alternative(html_content,"text/html")
            msg.send()
            return Response({"message":"CHECK EMAIL for verification"})
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)  
        except Exception as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogInAPI(APIView):

    def get(self,request):
        """This method will give the string response as given below."""
        return Response("This is LogInAPI")
        
    def post(self,request):
        """[This method will take the required input and do login]

        Returns:
            [returns the message if successfully loggedin]
        """
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            id = User.objects.get(username=username).id
            print(id)
            token=encode_token_userid(id)
            if user is not None:
                return Response({"msg": "Loggedin Successfully", 'data' : {'username': username, 'token': token}}, status=status.HTTP_200_OK)
            return Response({"msg": 'Wrong username or password'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST) 
        except AuthenticationFailed:
            return Response({'message': 'Authentication Failed'}, status=status.HTTP_400_BAD_REQUEST) 
        except Exception:
            return Response({"msg": "wrong credentials"}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmail(APIView):

    def get(self,request,token=None):
        try:
            user= decode_token(token)
            user_id=user.get("user_id")
            username=user.get("username")
            if User.objects.filter(Q(id=user_id) & Q(username=username)):
                return Response({"message":"Email Verified and Registered successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Try Again......Wrong credentials"})
        except Exception as e:
            return Response({"message":str(e)})
