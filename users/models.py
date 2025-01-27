from django.db import models
from django.contrib.auth.models import User
from main.models import Attendance
from math import floor
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

    def days_attended(self):
        return Attendance.objects.filter(student=self, present=True).count()
    
    def days_passed(self):
        return Attendance.objects.filter(student=self).count()

    def bmi(self):
        return self.weight / ((self.height * 0.308) ** 2)

    def grant_xp(self, xp):
        required_xp = next_level(self.level)
        self.xp += xp
        if self.xp >= required_xp:
            self.level += 1
            self.xp -= required_xp
        self.save()

    def grant_points(self, points):
        self.points += points
        self.save()
    

    def __str__(self):
        # Use the related User's first and last name
        return f"{self.user.first_name} {self.user.last_name} - Grade {self.grade}"


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
    profile_border = models.ForeignKey("main.ShopItem", blank=True, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return f"User_Profile of {self.user.first_name}_{self.user.last_name}"

def next_level(level):
    base_xp = 20
    exponent = 1.5
    return floor(base_xp * (level ** exponent))