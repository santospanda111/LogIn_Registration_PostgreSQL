from rest_framework import serializers
from .models import LogInData

'''This will serialize the complex data'''
class UserSerializer(serializers.ModelSerializer):
 class Meta:
  model = LogInData
  fields = "__all__"