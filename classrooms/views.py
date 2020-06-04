from django.shortcuts import render
from django.views import generic
from .models import Classroom


class ClassroomListView(generic.ListView):
    model = Classroom


class ClassroomDetailView(generic.DetailView):
    model = Classroom