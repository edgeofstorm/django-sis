from django.views import generic
from exams.models import Exam
from users.models import Teacher, Student


class BaseView(generic.TemplateView):
    template_name="base.html"

class HomeView(generic.TemplateView):
    template_name="home.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['last_exam'] = Exam.objects.last()
        context['stud_count'] = Student.objects.count()
        context['teacher_count'] = Teacher.objects.count()
        context['principal_count'] = 0
        return context 