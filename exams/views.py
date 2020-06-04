from django.shortcuts import render , reverse, HttpResponseRedirect
from django.views import generic
from .models import Exam, ExamResult
from .forms import ExamCreateForm
import datetime
from django.urls import reverse_lazy



class ExamListView(generic.ListView):
    model = Exam


class ExamDetailView(generic.DetailView):
    model = Exam
    template_name="exams/exam_detail.html"


class ExamCreateView(generic.CreateView): # generic.edit.FormView
    model = Exam
    form_class = ExamCreateForm
    template_name_suffix='_create_form'
    #template_name = 'exams/exam_create_form.html'  # Replace with your template.
    success_url = reverse_lazy('exams:list')  # Replace with your URL or reverse().

    def form_valid(self,form,*args, **kwargs):
        form.instance.timestamp = datetime.datetime.now()
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     sheet = request.FILES.get('sheet')
    #     if form.is_valid():
    #         for f in files:
    #             ...  # Do something with each file.

    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)