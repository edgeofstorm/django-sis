from django.urls import path
from . import views

app_name='exams'

urlpatterns = [
    #path("", views.HomeView.as_view(), name="home"),
    path("", views.ExamListView.as_view(), name="list"),
    path("<int:pk>/", views.ExamDetailView.as_view(), name="detail"),
    path("create/", views.ExamCreateView.as_view(), name="create")
]
