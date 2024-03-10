from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)