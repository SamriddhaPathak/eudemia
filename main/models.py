from django.db import models

class Challenge(models.Model):
    question = models.TextField(max_length = 400)
    answer = models.CharField(max_length =100)


    def __str__(self):
        return f"Challenge {self.id}"
    

class Quiz(models.Model):
    question = models.CharField(max_length = 150)
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    correct = models.IntegerField()

    def __str__(self):
        return f"Quiz {self.id}"