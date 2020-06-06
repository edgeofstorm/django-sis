from django.shortcuts import render
from django.views import generic
from .models import Student, Teacher
from exams.models import Exam
import json
# Create your views here.


class StudentListView(generic.ListView):
    model = Student


class StudentDetailView(generic.DetailView):
    model = Student

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        student = context.get('object')
        context['last_exams_results'] = student.exam_results.all().reverse()[:5]
        if student.user.first_name and student.user.last_name is not None:
            context['fullname'] = f'{student.user.first_name} {student.user.last_name}'
        context['exams_all'] = student.exam_results.all()
        # mat_list = []
        # for result in student.exam_results.all():
        #     mat_list.append(20-len(result.result['Yanlislar']['M']))
        # context['mat_yanlislar'] = mat_list
        context['mat_yanlislar'] = get_yanlis_count(student,'M')
        context['fen_yanlislar'] = get_yanlis_count(student,'F')
        context['sosyal_yanlislar'] = get_yanlis_count(student,'S')
        context['turkce_yanlislar'] = get_yanlis_count(student,'T')

        # item_dict = json.loads(json.dumps(context['exams_all'].first().result))
        # print (len(item_dict['Yanlislar']['M']))
        #context['exams_all_results'] = Exam.objects.filter(result__student=student)
        return context


class TeacherListView(generic.ListView):
    model = Teacher


class TeacherDetailView(generic.DetailView):
    model = Teacher


def get_yanlis_count(student,ders,*args, **kwargs):
    yanlis_list = []
    for result in student.exam_results.all():
        yanlis_list.append(20-len(result.result['Yanlislar'][ders]))
    return yanlis_list