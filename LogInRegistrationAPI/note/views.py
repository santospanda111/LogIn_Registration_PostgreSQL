from note.utils import verify_token
from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import NoteSerializer
from .models import Notes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.contrib.auth.models import User
from note.utils import verify_token

class NotesAPI(APIView):
    
    @verify_token
    def get(self, request):
        """This method will read the data from the table."""
        try:
            user_note_id= request.data.get('id')
            if user_note_id is not None:
                data = Notes.objects.filter(user_note=user_note_id)
                serializer=NoteSerializer(data, many=True)
                return Response({"data":{"note-list": serializer.data}}, status=status.HTTP_200_OK)
            return Response({"message":"Put user id to get notes"}, status=status.HTTP_400_BAD_REQUEST)    
        except AssertionError as e:
            return Response({"message":"Put user id to get notes"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message":str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def post(self, request):
        """
            :param: title, description and user id as parameter.
            :return: It's return response that notes succcessfully created or not.
        """
        try:
            id= User.objects.filter(id=request.data.get("id"))
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            notes = Notes(user_note=id[0], title=serializer.data.get('title'), description=serializer.data.get('description'))
            notes.save()        
            return Response({'message': 'Notes created successfully'}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({'message': 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'message': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token  
    def put(self,request):
        """This method is used to update the data from the table by using id as a parameter"""
        try:

            id = request.data.get("note_id")
            notes = Notes.objects.get(pk=id)
            serializer = NoteSerializer(notes, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Complete Data Updated'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self,request):
        """This method is used to delete the data from the table by using id as a parameter"""
        try:
            id = request.data.get("note_id")
            user = Notes.objects.get(id=id)
            user.delete()
            return Response({'msg':'Data Deleted'}, status=status.HTTP_200_OK) 
        except ValueError:
            return Response({"message": 'Invalid Input'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
