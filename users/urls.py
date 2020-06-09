from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("teachers/", views.TeacherListView.as_view(), name="teacher_list"),
    path("teachers/<int:pk>/", views.TeacherDetailView.as_view(), name="teacher_detail"),
    path("students/<int:pk>/exam/<int:pk2>/<int:pk3>", views.QTemplateView.as_view(),name="q_solution")
]
