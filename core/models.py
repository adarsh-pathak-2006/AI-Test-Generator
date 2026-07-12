from django.db import models
from django.contrib.auth.models import User

class MainDB(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    document=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.document[:100]
    
class Quesans(models.Model):
    input=models.ForeignKey(MainDB, on_delete=models.CASCADE, related_name='questionsanswers')
    question=models.TextField()
    option1=models.TextField()
    option2=models.TextField()
    option3=models.TextField()
    option4=models.TextField()
    answer=models.CharField(max_length=1, choices=[('A','A'), ('B','B'), ('C','C'), ('D','D')])
    correct_ans=models.TextField()

    def __str__(self):
        return self.input.__str__

