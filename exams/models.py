from django.db import models
from users.models import Student
from django.core.validators import MaxLengthValidator, MaxValueValidator, FileExtensionValidator
from .validators import validate_file_extension
from django.shortcuts import reverse
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
import datetime
# Create your models here.

# CUSTOM QUERYSET
class ExamQuerySet(models.QuerySet):
    def get_by_id(self,pk):
        if self.filter(id=pk).count() == 1:
            return self.filter(id=pk).first()
        return None
    
    def has_results(self,pk):
        try:
            self.get_by_id(pk).result.exists()
            return True
        except: # doesnotexist
            return False
        #return False if self.filter(id=pk).first().result is None else True
    
    def get_results(self,pk):
        if self.has_results(pk):
            total=0
            count=0
            for result in self.get_by_id(pk).result.all():
                total += int(result.result)
                count +=1
            if count == 0:
                return 0
            mean = total/count #(self.get_by_id(pk).result.count())
            return mean
        return 0

    def get_result(self,pk):
        if self.has_results(pk):
            total = 0
            for result in self.get_by_id(pk).result.all():
                # for key,value in result.result.items:
                #     print(key, value)
                total += int(result.result['Net'])
            return total/self.get_by_id(pk).result.all().count()
        return 0

    def get_mean(self):
        means=[]
        for exam in self.all():
            means.append(self.get_result(exam.pk))
        return means

    def get_results_mean(self):
        means=[]
        for exam in self.all():
            if self.has_results(exam.pk):
                means.append(self.get_results(exam.pk))
        return ignore_zeros(means)

# CUSTOM MODEL MANAGER           
class ExamManager(models.Manager):
    def get_queryset(self):
        return ExamQuerySet(self.model, using=self._db)
    
    def get_by_id(self,pk):
        return self.get_queryset().get_by_id(pk)
    
    def has_results(self,pk):
        return self.get_queryset().has_results(pk)

    def get_results(self,pk):
        return self.get_queryset().get_results(pk)

    def get_result(self,pk):
        return self.get_queryset().get_result(pk)
    
    def get_mean(self):
        return self.get_queryset().get_mean()


class Exam(models.Model):
    title = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default = datetime.datetime.now()) # auto_now_add=True
    klass = models.IntegerField(validators=[MaxValueValidator(8)])
    sheet = models.FileField(null=True,blank=True, validators=[FileExtensionValidator(allowed_extensions=['pdf','.pdf','.txt','txt','.docx','docx'])])
    answers = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True) #, default = dict
    #tur = models.CharField() sinav, yazili, sozlu etc ?

    objects = ExamManager()

    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("exams:detail", kwargs={"pk": self.pk})    
    

class ExamResult(models.Model):
    #onetone gave error(std1-dnm1, std2-dnm1 gave error ->Exam result with this Exam already exists.)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='result')
    student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='exam_results')
    result = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True) #, default = dict


    class Meta:
        ordering = ['-exam']
        unique_together = ('exam', 'student',)
    
    def __str__(self):
        return f'{self.student}-{self.exam.title}'

# student answers ?
class ExamStudentAnswer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name = 'student_answers')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name = 'exam_answers')
    answers = JSONField(encoder=DjangoJSONEncoder, null=True, blank=True)

    class Meta:
        unique_together = ('exam', 'student',)
    
    def __str__(self):
        return f'{self.exam}-{self.student}'
    



def mean(objects,*args, **kwargs):
    total=0
    for obj in objects:
        total+=obj
    return total/(len(objects))

def ignore_zeros(val,*args, **kwargs):
    cleansed = []
    for value in val:
        if value != 0:
            cleansed.append(value)
    return cleansed