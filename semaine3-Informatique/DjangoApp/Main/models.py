from django.db import models

# Create your models here.
class Question(models.Model):
    ListeQuestion = models.FileField(upload_to='question/')
 
