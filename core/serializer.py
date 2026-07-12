from rest_framework.serializers import ModelSerializer
from core.models import MainDB, Quesans
from django.contrib.auth.models import User


class RegisterSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email', 'password']

class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email'] 

class MainDBSerializer(ModelSerializer):
    class Meta:
        model=MainDB
        fields=['user', 'document', 'created_by']

class QuesAnsSerializer(ModelSerializer):
    input=MainDBSerializer(read_only=True)
    class Meta:
        model=Quesans
        fields='__all__'

