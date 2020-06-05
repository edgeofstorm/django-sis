from django.views import generic
from exams.models import Exam
from users.models import Teacher, Student


class BaseView(generic.TemplateView):
    template_name="base.html"

class HomeView(generic.TemplateView):
    template_name="home.html"

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # Exam.objects.filter(result__student=stud)
        # for exam in Exam.objects.all().order_by('-timestamp'):
        #     if exam.result.exists():
        #         context['last_exam'] = exam
        context['last_exam'] = Exam.objects.filter(result__isnull=False).last()
        context['stud_count'] = Student.objects.count()
        context['teacher_count'] = Teacher.objects.count()
        context['principal_count'] = 0
        return context 