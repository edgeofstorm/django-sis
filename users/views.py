from django.shortcuts import render
from django.views import generic
from .models import Student, Teacher
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
        return context


class TeacherListView(generic.ListView):
    model = Teacher


class TeacherDetailView(generic.DetailView):
    model = Teacher