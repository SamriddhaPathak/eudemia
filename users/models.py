from django.db import models
from django.contrib.auth.models import User
# Create your models here.

choices = (
    ("A+", "A-"),
    ("B+", "B-"),
    ("AB+", "AB-"),
    ("O+", "O-"),
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
    level = models.PositiveIntegerField(default = 0)
    xp = models.PositiveIntegerField(default = 0)
    blood_group = models.CharField(max_length = 10,choices = choices, default = " ")

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
    profile_pic = models.ImageField(upload_to = "profile_pictures/", blank = False, null = False, default = "media/profile_pictures/profile.png")