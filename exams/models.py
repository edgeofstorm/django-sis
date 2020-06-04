from django.db import models
from users.models import Student
from django.core.validators import MaxLengthValidator, MaxValueValidator, FileExtensionValidator
from .validators import validate_file_extension
from django.shortcuts import reverse
# Create your models here.

class Exam(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    klass = models.IntegerField(validators=[MaxValueValidator(8)])
    sheet = models.FileField(null=True,blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf','.pdf','.txt','txt'])])
    #tur = models.CharField() sinav, yazili, sozlu etc ?

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("exams:detail", kwargs={"pk": self.pk})
    
    

class ExamResult(models.Model):
    #onetone gave error(std1-dnm1, std2-dnm1 gave error ->Exam result with this Exam already exists.)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='result')
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='exam_results')
    result = models.CharField(max_length=255)

    class Meta:
        ordering = ['-result']
    
    def __str__(self):
        return f'{self.student}-{self.exam.title}'


    


# class Student(models.Model):
#     stud_id = models.PositiveSmallIntegerField()
#     classroom = models.ForeignKey(Classroom, on_delete= models.CASCADE,related_name='students') # onetomany ?


# class Classroom(models.Model):
#     grade # 8
#     section # A
#     #examresults
#     guide_teach
#     #from django.contrib.auth import get_user_model