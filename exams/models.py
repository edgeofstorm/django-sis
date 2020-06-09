from django.db import models
from users.models import Student, Teacher
from django.core.validators import MaxLengthValidator, MaxValueValidator, FileExtensionValidator
from .validators import validate_file_extension
from django.shortcuts import reverse
from django.contrib.postgres.fields import JSONField
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.signals import post_save
import datetime, json
# Create your models here.

# CUSTOM QUERYSET FOR EXAM MODEL
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
    
    def success_status(self,stud_pk):
        pass
        #self.filter()result.filter(student.pk=stud_pk)
    
    def evaluate(self,stud_pk,exam_pk):
        exam_answers = json.loads(json.dumps(self.filter(pk=exam_pk).first().answers))
        stud_answers = json.loads(json.dumps(self.filter(pk=exam_pk).first().student_answers.filter(student__pk=stud_pk).first().answers))
        #print (list(stud_answers['F']))
        #print(compare_and_create(stud_answers, exam_answers))

# CUSTOM MODEL MANAGER FOR EXAM MODEL         
class ExamManager(models.Manager):
    def get_queryset(self):
        return ExamQuerySet(self.model, using=self._db)
    
    def get_by_id(self,pk):
        return self.get_queryset().get_by_id(pk)
    
    def has_results(self,pk):
        return self.get_queryset().has_results(pk)

    def get_result(self,pk):
        return self.get_queryset().get_result(pk)
    
    def get_mean(self):
        return self.get_queryset().get_mean()
    
    def evaluate(self,stud_pk,exam_pk):
        return self.get_queryset().evaluate(stud_pk,exam_pk)


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
    #onetone gave error(std1-dnm1, std2-dnm1 gave error ->Exam result with this Exam already exists.) what you want is unique_together
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE,related_name='result')# make it results(its not 1-1 rel. foreign key returns many objects(1-* rel))
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

class QSolution(models.Model):
    question = models.SmallIntegerField(validators=[MaxValueValidator(20)])
    solution = models.ImageField(upload_to='solutions')

    def __str__(self):
        return f'{self.question}'
    
    class Meta:
        ordering=['question']
    

class ExamSolution(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='solutions')
    # teacher brans ?
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='contributed_solutions')
    # make it choicefield -> SAME AS users.Teacher.subject 
    subject = models.CharField(max_length=1)
    solutions = models.ForeignKey(QSolution, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('subject', 'solutions',)

    def __str__(self):
        return f'{self.exam}-{self.teacher.subject}-{self.solutions}'

    #def validate_unique(self):


def examstudentanswer_post_save_receiver(sender, instance, *args, **kwargs):
    if instance.answers and instance.exam.answers:
        result_json = compare_and_create(instance.answers,instance.exam.answers)
        er = ExamResult.objects.create(exam= instance.exam,student= instance.student, result= result_json)
        er.save()

post_save.connect(receiver= examstudentanswer_post_save_receiver,sender=ExamStudentAnswer)


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

def compare_and_create(stud_answers,exam_answers):
    result = {
        "Yanlislar":{
            "T":[],
            "S":[],
            "M":[],
            "F":[]
        },
        "Boslar":{
            "T":[],
            "S":[],
            "M":[],
            "F":[]
        },
        "Net":0
    }
    #    "Puan":0
    for c in ['M','S','T','F']:
        result.update(get_wrongs(result,stud_answers,exam_answers,c))
    # for index,exam_answers_mat in enumerate(exam_answers['M']): # , start=1
    #     if not stud_answers['M'][index]:
    #         result['Boslar']['M'].append(index+1)
    #         continue
    #     if exam_answers_mat != stud_answers['M'][index]:
    #         result['Yanlislar']['M'].append(index+1)
    # result['Net'] += 20 - (len(result['Yanlislar']['M']) + len(result['Yanlislar']['M'])/3 + len(result['Boslar']['M']))

    # for index,exam_answers_turkce in enumerate(exam_answers['T']):
    #     if not stud_answers['T'][index]:
    #         result['Boslar']['T'].append(index+1)
    #         continue
    #     if exam_answers_turkce != stud_answers['T'][index]:
    #         result['Yanlislar']['T'].append(index+1)
    # result['Net'] += 20 - (len(result['Yanlislar']['T']) + len(result['Yanlislar']['T'])/3 + len(result['Boslar']['T']))

    # for index,exam_answers_sosyal in enumerate(exam_answers['S']):
    #     if not stud_answers['S'][index]:
    #         result['Boslar']['S'].append(index+1)
    #         continue
    #     if exam_answers_sosyal != stud_answers['S'][index]:
    #         result['Yanlislar']['S'].append(index+1)
    # result['Net'] += 20 - (len(result['Yanlislar']['S']) + len(result['Yanlislar']['S'])/3 + len(result['Boslar']['S']))

    # for index,exam_answers_fen in enumerate(exam_answers['F']):
    #     if not stud_answers['F'][index]:
    #         result['Boslar']['F'].append(index+1)
    #         continue
    #     if exam_answers_fen != stud_answers['F'][index]:
    #         result['Yanlislar']['F'].append(index+1)
    # result['Net'] += 20 - (len(result['Yanlislar']['F']) + len(result['Yanlislar']['F'])/3 + len(result['Boslar']['F']))

    try:
        # creating JSON object from str
        # jstr = '{{ "T":{0},"S":{1},"M":{2},"F":{3} }}'
        # jobj = json.loads(jstr)
        
        # creating JSON obj from dict
        result = json.loads(json.dumps(result)) # json.loads() ->err ?string indices must be integers (json fields were fucked up '/' everywhere, json.loadds fixed it)
        print(result)
        return result
    except: # KeyErro
        return None


# compare_and_create helper function
def get_wrongs(jobj,stud_answers,exam_answers,ders):
    for index,exam_answers in enumerate(exam_answers[ders]): # , start=1
        if not stud_answers[ders][index]:
            jobj['Boslar'][ders].append(index+1)
            continue
        if exam_answers != stud_answers[ders][index]:
            jobj['Yanlislar'][ders].append(index+1)
    jobj['Net'] += 20 - (len(jobj['Yanlislar'][ders]) + len(jobj['Yanlislar'][ders])/3 + len(jobj['Boslar'][ders]))
    return jobj

# PUAN HESAPLAMA (STANDART SAPMAYLA PUANLAR DEGISIKLIK GOSTEREBILIR)
# Türkçe 5,3 Puan
# Fen Bilimleri 5,3 Puan
# Matematik 5,3 Puan
# İnkılap Tarihi ve Atatürkçülük 2,6 Puan
# Din Kültürü ve Ahlak Bilgisi 2,6 Puan
# Yabancı Dil 2,6 Puan
# 4-Derslere ait puanlar ayrı ayrı hesaplandıktan sonra her öğrenciye verilen taban puan eklenir
# Yapılan netlerin dışında MEB her öğrenciye 104 taban puan vermektedir