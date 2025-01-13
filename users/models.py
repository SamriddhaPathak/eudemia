from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Class(models.Model):
    grade  = models.IntegerField(primary_key= True)
    name = models.CharField(max_length= 10)
    score = models.IntegerField()

    def __str__(self):
        return self.name    
    
class Student(models.Model):
    dob = models.DateField()
    points = models.IntegerField()
    grade = models.ForeignKey(Class, on_delete = models.CASCADE)
    height = models.FloatField()
    weight = models.IntegerField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        # Use the related User's first and last name
        return f"{self.user_id.first_name}_{self.user_id.last_name}"


class Teacher(models.Model):
    ph_number = models.CharField(max_length=20)
    grade = models.IntegerField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id.first_name}_{self.user_id.last_name}"


class Parent(models.Model):
    ph_number = models.CharField(max_length=20)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)  

    def __str__(self):
        return f"{self.user_id.first_name}_{self.user_id.last_name}"
