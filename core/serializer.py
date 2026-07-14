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
        fields=['id', 'user', 'document', 'created_at']
        read_only_fields=['user']

class QuestionIdSerializer(ModelSerializer):
    class Meta:
        model=Quesans
        fields=['id']

class DashboardQuizSerializer(ModelSerializer):
    questionsanswers=QuestionIdSerializer(many=True, read_only=True)
    class Meta:
        model=MainDB
        fields=['id', 'user', 'document', 'created_at', 'questionsanswers']
        read_only_fields=['user']

class AnswerSerializer(ModelSerializer):
    class Meta:
        model=Quesans
        fields=['answer']

class QuesAnsSerializer(ModelSerializer):
    main=MainDBSerializer(read_only=True)
    class Meta:
        model=Quesans
        fields='__all__'

class QuestionSerializer(ModelSerializer):
    class Meta:
        model=Quesans
        fields=['question', 'option1', 'option2', 'option3', 'option4']
