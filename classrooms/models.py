from django.db import models
from django.core.validators import MaxValueValidator
from users.models import Teacher

# Create your models here.

class Classroom(models.Model):
    grade = models.IntegerField(validators=[MaxValueValidator(9)])
    section = models.CharField(max_length=1)
    advisor = models.OneToOneField(Teacher,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.grade}-{self.section}'
    