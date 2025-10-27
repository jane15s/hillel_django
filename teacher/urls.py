from django.urls import path

from . import views

urlpatterns = [
    path("<int:teacher_id>/", views.teacher_dashboard, name="teacher_dashboard"),
    path("lessons/", views.Lessons.as_view(), name="lessons"),
    path("lessons/<int:lesson_id>/", views.lesson_details, name="lesson_details"),
    path("lessons/<int:lesson_id>/set_grade/", views.set_grade, name="set_grade")
]