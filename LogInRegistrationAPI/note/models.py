from django.db import models
from django.contrib.auth.models import User

class Notes(models.Model):
    user_note = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
