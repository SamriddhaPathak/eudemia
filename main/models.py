from django.db  import models
from users.models import Student, Class
from django.contrib.auth.models import User

quiz_choices = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
)

challenge_type_choices = (
    ("Weekly", "Weekly"),
    ("daily", "Daily"),
)

class Subject(models.Model):
    name = models.CharField(max_length = 50, unique=True)
    def __str__(self):
        return f"{self.name}"


class Challenge(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Class, default=4, on_delete=models.CASCADE)
    name = models.CharField(max_length = 50)
    challenge_type = models.CharField(max_length = 50, choices = challenge_type_choices)
    def __str__(self):
        return f"Challenge for {self.name}"
    
class Quiz(models.Model):
    grade = models.ForeignKey(Class, default=4, on_delete=models.CASCADE)
    question = models.TextField(max_length = 150)
    option1 = models.CharField(max_length = 100)
    option2 = models.CharField(max_length = 100)
    option3 = models.CharField(max_length = 100)
    option4 = models.CharField(max_length = 100)
    correct = models.PositiveIntegerField(choices = quiz_choices)

    def __str__(self):
        return f"Quiz {self.grade}"
    
    
class Question(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    question  = models.TextField(max_length = 200)
    answer = models.CharField(max_length = 50)
    
    def __str__(self):
        return f"{self.id}"

class Attendence(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    days_attended = models.PositiveIntegerField()
    days_passed = models.PositiveIntegerField(default = 60)
    
    def __str__(self):
        return f"Attendence {self.id}"
