from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import request

from common_data.models import Lesson, Grade, StudentClass

def check_if_student(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if not request.user.groups.filter(name='student').exists():
            raise PermissionDenied("Student access only")
        return func(request, *args, **kwargs)
    return wrapper

@check_if_student
def student_main_page(request, student_id): # уроки студента (класа) з оцінками студента
    if request.method == 'GET':
        student_class = StudentClass.objects.filter(student_id=student_id).first().sclass
        lessons = Lesson.objects.filter(sclass=student_class).order_by('date')
        grades = Grade.objects.filter(student=request.user)
        grades_dict = {}
        for grade in grades:
            grades_dict[grade.lesson.id] = grade
        return render(request, 'student/s_dashboard.html', {'lessons': lessons, 'grades_dict': grades_dict, 'student_class': student_class, 'student_id': student_id})
    return None

@check_if_student
def lessons_list(request, student_id): # всі уроки класа за розкладом
    if request.method == 'GET':
        student_class = StudentClass.objects.filter(student_id=student_id).first().sclass
        lessons = Lesson.objects.filter(sclass=student_class).order_by('date')
    return render(request, 'student/lessons.html',
                  {'lessons': lessons, 'student_class': student_class, 'student_id': student_id})

@check_if_student
def lesson_details(request, student_id, lesson_id): # конкретний урок при кліку на нього
    if request.method == 'GET':
        lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'student/lesson.html',
                  {'lesson': lesson, 'student_id': student_id})

