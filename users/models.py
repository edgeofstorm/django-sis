from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Teacher(models.Model):

    class Subject(models.TextChoices):
        TURKCE = 'T', _('Turkce')
        SOSYAL = 'S', _('Sosyal')
        MATEMATIK = 'M', _('Matematik')
        FEN = 'F', _('Fen')
        DEFAULT = 'Q', _('Default')

    user = models.OneToOneField(User,on_delete=models.CASCADE)
    subject = models.CharField(max_length=1, choices=Subject.choices, default=Subject.DEFAULT)#max_length=1,
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
