from django.db import models

# Create your models here.

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField('Student')

class Student(models.Model):
    name = models.CharField(max_length=100)

