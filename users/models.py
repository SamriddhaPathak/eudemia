from django.db import models
from django.contrib.auth.models import User
# Create your models here.

choices = (
    ("A+", "A+"),
    ("A-", "A-"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)

class Class(models.Model):
    grade  = models.IntegerField(primary_key=True)
    name = models.CharField(max_length= 10)
    score = models.IntegerField()

    def __str__(self):
        return self.name    
    
class Student(models.Model):
    dob = models.DateField()
    points = models.IntegerField()
    grade = models.ForeignKey(Class, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default = 1)
    xp = models.PositiveIntegerField(default = 0)
    blood_group = models.CharField(max_length = 10, blank=True, null=True, choices = choices)
    completed_challenge_questions = models.ManyToManyField("main.Question", blank=True, related_name="completed_challenge_questions")
    correct_challenge_questions = models.ManyToManyField("main.Question", blank=True, related_name="correct_challenge_questions")
    completed_quiz_questions = models.ManyToManyField("main.QuizQuestion", blank=True, related_name="completed_quiz_questions")
    correct_quiz_questions = models.ManyToManyField("main.QuizQuestion", blank=True, related_name="correct_quiz_questions")

    def bmi(self):
        return self.weight / ((self.height * 0.308) ** 2)
    

    def __str__(self):
        # Use the related User's first and last name
        return f"{self.user.first_name}_{self.user.last_name}"


class Teacher(models.Model):
    ph_number = models.CharField(max_length=20)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"


class Parent(models.Model):
    ph_number = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)  

    def __str__(self):
        return f"{self.user.first_name}_{self.user.last_name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = "profile_pictures/", blank = False, null = False, default = "profile_pictures/profile.png")
    def __str__(self):
        return f"User_Profile of {self.user.first_name}_{self.user.last_name}"