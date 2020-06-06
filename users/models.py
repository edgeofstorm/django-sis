from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    joined_date = models.DateTimeField() # timestamp
    phone = models.CharField(max_length=11)

    def __str__(self):
        return self.user.username
    

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    stud_id = models.PositiveSmallIntegerField()
    joined_date = models.DateTimeField() # timestamp
    classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
