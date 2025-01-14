from django.db import models

class Challenge(models.Model):
    grade = models.IntegerField(default=4)
    question = models.TextField(max_length = 400)
    answer = models.CharField(max_length =100)


    def __str__(self):
        return f"Challenge {self.id}"

class monthly_challenge(models.Model):
    grade = models.IntegerField(default=4)
    question = models.TextField(max_length = 400)
    answer = models.CharField(max_length = 100)
    def __str__(self):
        return f"Monthly Challenge {self.id}"

class Quiz(models.Model):
    grade = models.IntegerField(default=4)
    question = models.TextField(max_length = 150)
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    correct = models.PositiveIntegerField()

    def __str__(self):
        return f"Quiz {self.id}"