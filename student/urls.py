from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_main_page, name="student_main_page"),
    path("lessons/", views.lessons_list, name="lessons"),
    path("lessons/<int:lesson_id>/", views.lesson_details, name="lesson_details"),
    path("my_homework", views.my_homework, name="my_homework"),
    path("my-grades/", views.my_grades, name="my_grades")
]