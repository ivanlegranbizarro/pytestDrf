from django.urls import path

from . import views

app_name = "classroom"

urlpatterns = [
    path("classrooms/", views.ClassroomList.as_view(), name="classroom-list"),
    path(
        "classrooms/<int:pk>/", views.ClassroomDetail.as_view(), name="classroom-detail"
    ),
    path("students/", views.StudentList.as_view(), name="students-list"),
    path("students/<int:pk>/", views.StudentDetail.as_view(), name="student-detail"),
]
