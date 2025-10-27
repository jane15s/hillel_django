from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_main_page, name="student_main_page"),
    path("lessons/", views.lessons_list, name="lessons"),
    path("lessons/<int:lesson_id>/", views.lesson_details, name="student_lesson_details")
]