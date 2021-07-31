import jwt
from django.conf import settings
from rest_framework.response import Response

def encode_token_userid(user_id):
    '''This function will return the encoded token'''
    try:
        encoded_token = jwt.encode({'user_id':user_id}, key=settings.SECRET_KEY, algorithm='HS256')
        return encoded_token
    except Exception as e:
        return Response({"message":str(e)})

def encode_token(user_id,user_name):
    '''This function will return the encoded token'''
    try:
        encoded_token_id = jwt.encode({'user_id':user_id,'username':user_name}, key=settings.SECRET_KEY, algorithm='HS256')
        return encoded_token_id
    except Exception as e:
        return Response({"message":str(e)})

def decode_token(encoded_token_id):
    '''This function will return the decoded token'''
    try:
        decoded_token = jwt.decode(encoded_token_id,key=settings.SECRET_KEY,algorithms="HS256")
        return decoded_token
    except Exception as e:
        return Response({"message":str(e)})
