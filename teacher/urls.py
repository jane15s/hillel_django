from django.urls import path

from . import views

urlpatterns = [
    path("", views.teacher_dashboard, name="teacher_dashboard"),
    path("lessons/<int:lesson_id>/", views.lesson_details, name="lesson_details"),
    path("lessons/<int:lesson_id>/add_homework", views.add_homework, name="lesson_homework"),
    path("lessons/<int:lesson_id>/set_grade", views.set_grade, name="set_grade")
]