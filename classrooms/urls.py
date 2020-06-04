from django.urls import path
from .views import ClassroomListView,ClassroomDetailView

app_name='classrooms'

urlpatterns = [
    path("", ClassroomListView.as_view(), name="list"),
    path("<int:pk>/", ClassroomDetailView.as_view(), name="detail")
]
