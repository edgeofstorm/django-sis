from django.shortcuts import render
from django.views import generic
from .models import Student, Teacher
from exams.models import Exam, ExamResult, ExamSolution, QSolution
import json
# Create your views here.


class StudentListView(generic.ListView):
    model = Student

# class ModalTemplateView(generic.TemplateView):
#     template_name="users/snippets/student/modal.html"

#     def get_context_data(self,*args, **kwargs):
#         context = super().get_context_data(*args,**kwargs)
#         context["a"] = 'adgadgad'
#         return context
        

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
        context['mat_yanlislar'] = get_yanlis_count(student,"M")
        context['fen_yanlislar'] = get_yanlis_count(student,'F')
        context['sosyal_yanlislar'] = get_yanlis_count(student,'S')
        context['turkce_yanlislar'] = get_yanlis_count(student,'T')
        context['success_status'] = success_status(student)
        context['image'] = student.exam_results.filter(exam__title='LGS HAZIRLIK - 5').first().exam.solutions.first().solutions.solution.url
        #student.exam_results.first().exam.solutions.first().solutions.solution.url

        # item_dict = json.loads(json.dumps(context['exams_all'].first().result))
        # print (len(item_dict['Yanlislar']['M']))
        #context['exams_all_results'] = Exam.objects.filter(result__student=student)
        return context


class TeacherListView(generic.ListView):
    model = Teacher


class TeacherDetailView(generic.DetailView):
    model = Teacher


class QTemplateView(generic.TemplateView):
    template_name="users/snippets/student/modals/q_modal.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = 'Q_Q'
        return context
    


def get_net_count(student,ders,*args, **kwargs):
    net=0
    for result in student.exam_results.all():
        yanlis_list.append(20-len(result.result["Yanlislar"][ders]))
    return yanlis_list

def get_yanlis_count(student,ders,*args, **kwargs):
    yanlis_list = []
    for result in student.exam_results.all():
        Exam.objects.filter(id=result.exam_id).evaluate(student.pk,Exam.objects.filter(id=result.exam_id).first().pk)
        yanlis_list.append(20-len(result.result["Yanlislar"][ders]))
    return yanlis_list

def success_status(student):
    success=""
    last=""
    between=""
    mean=0
    last2_mean=0
    for index,exam in enumerate(ExamResult.objects.filter(student=student)):
        if index >= ExamResult.objects.filter(student=student).count() - 2:
            last2_mean += int(exam.result['Net'])  
        mean+=int(exam.result['Net'])
    mean = mean / (ExamResult.objects.filter(student=student).count())
    last2_mean /= 2 
    if 70 < mean < 80:
        success="basarili"
        if last2_mean < mean:
            between="fakat"
        else:
            between="ve"
    elif 60 < mean < 70:
        success="vasat"
        if last2_mean < mean:
            between="ve"
        else:
            between="fakat"
    else:
        success="basarisiz"
        if last2_mean < mean:
            between="ve"
        else:
            between="fakat"
    if last2_mean < mean:
        last="dususte"
    else:
        last="yukseliste"
    #between = "ve" if 70 < mean < 80 and last2_mean > mean else "fakat" || "fakat" if mean < 70 and last2_mean > mean else "ve" ! Check nested ternary operator
    print(f' sounc -> {success} {between} {last}')
    return f'{success} {between} {last}'
    