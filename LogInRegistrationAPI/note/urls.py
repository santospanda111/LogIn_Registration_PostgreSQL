from django.urls import path
from note import views as NoteView

urlpatterns = [
    path('notes', NoteView.NotesAPI.as_view(), name='notes'),
]
