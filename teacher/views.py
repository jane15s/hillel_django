from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from common_data.models import Lesson, StudentClass, Grade, SchoolClass

def check_if_teacher(func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("/login/")
        if not request.user.groups.filter(name='teacher').exists():
            raise PermissionDenied("Teacher access only")
        return func(request, *args, **kwargs)
    return wrapper

@check_if_teacher
def teacher_dashboard(request, teacher_id):
    if request.method == 'GET':
        current_teacher = get_object_or_404(User, pk=teacher_id)
        t_lessons = Lesson.objects.filter(teacher=current_teacher)
        return render(request, 'teacher/t_dashboard.html', {'current_teacher': current_teacher, 't_lessons': t_lessons})
    return None

class Lessons(View):
    @staticmethod
    @check_if_teacher
    def get(request, *args, **kwargs):
        all_lessons = Lesson.objects.all()
        all_classes = SchoolClass.objects.all()
        return render(request, 'teacher/lessons.html', {'lessons': all_lessons, 'all_classes': all_classes})

    @staticmethod
    @check_if_teacher
    def post(request, *args, **kwargs):
        current_class_id = int(request.POST["sclass_id"])
        current_class = SchoolClass.objects.get(pk=current_class_id)

        current_lesson = Lesson(
            name=request.POST["name"],
            description=request.POST["description"],
            date=request.POST["date"],
            homework=request.POST["homework"],
            room=request.POST["room"],
            sclass=current_class,
            teacher=request.user
        )
        current_lesson.save()
        teacher_id = kwargs.get("teacher_id")
        return redirect(f'/teacher/{teacher_id}/lessons/#lesson_{current_lesson.id}')

@check_if_teacher
def lesson_details(request, teacher_id, lesson_id):
    if request.method == 'GET':
        current_lesson = Lesson.objects.get(pk=lesson_id)
        grades = Grade.objects.filter(lesson=current_lesson)
        current_class = current_lesson.sclass
        current_students = list(StudentClass.objects.filter(sclass=current_class))
        grade_choices = range(0, 13)
        return render(request, 'teacher/lesson.html', {'lesson': current_lesson, 'grades': grades, 'students': current_students, 'grade_choices': grade_choices})
    return None

@check_if_teacher
def set_grade(request, teacher_id, lesson_id):
    if request.method == 'POST':
        current_student = User.objects.get(pk=int(request.POST["student_id"]))
        grade_obj, created = Grade.objects.get_or_create(
            student=current_student,
            lesson=Lesson.objects.get(pk=lesson_id)
        )
        if request.POST.get("grade"):
            grade_obj.grade = int(request.POST["grade"])
        if request.POST.get("homework_grade"):
            grade_obj.homework_grade = int(request.POST["homework_grade"])

        grade_obj.save()

        return redirect(f'/teacher/{teacher_id}/lessons/{lesson_id}/')
    return None