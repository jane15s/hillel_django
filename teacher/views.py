from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
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
    current_teacher = get_object_or_404(User, pk=teacher_id)
    if request.method == "GET":
        t_lessons = Lesson.objects.filter(teacher=current_teacher)
        return render(request, 'teacher/t_dashboard.html', {'current_teacher': current_teacher, 't_lessons': t_lessons})
    return None

class Lessons(View):
    @staticmethod
    @check_if_teacher
    def get(request, teacher_id):
        get_object_or_404(User, pk=teacher_id)
        all_lessons = Lesson.objects.filter(teacher_id=teacher_id)
        all_classes = SchoolClass.objects.all()
        return render(request, 'teacher/lessons.html', {'lessons': all_lessons, 'all_classes': all_classes})

    @staticmethod
    @check_if_teacher
    def post(request, teacher_id):
        get_object_or_404(User, pk=teacher_id)

        sclass_id = request.POST.get("sclass_id")
        if not sclass_id:
            return HttpResponseBadRequest("Missing sclass_id")

        current_class = get_object_or_404(SchoolClass, pk=sclass_id)

        current_lesson = Lesson(
            name=request.POST.get("name", ""),
            description=request.POST.get("description", ""),
            date=request.POST.get("date"),
            homework=request.POST.get("homework", ""),
            room=request.POST.get("room", ""),
            sclass=current_class,
            teacher=request.user
        )
        current_lesson.save()
        return redirect(f'/teacher/{teacher_id}/lessons/#lesson_{current_lesson.id}')

@check_if_teacher
def lesson_details(request, teacher_id, lesson_id):
    current_teacher = get_object_or_404(User, pk=teacher_id)
    current_lesson = get_object_or_404(Lesson, pk=lesson_id, teacher=current_teacher)

    if request.method == 'GET':
        grades = Grade.objects.filter(lesson=current_lesson)
        current_class = current_lesson.sclass
        current_students = list(StudentClass.objects.filter(sclass=current_class))
        grade_choices = range(0, 13)
        return render(request, 'teacher/lesson.html', {'lesson': current_lesson, 'grades': grades, 'students': current_students, 'grade_choices': grade_choices})
    return None

@check_if_teacher
def set_grade(request, teacher_id, lesson_id):
    get_object_or_404(User, pk=teacher_id)
    current_lesson = get_object_or_404(Lesson, pk=lesson_id)

    if request.method == 'POST':
        student_id = request.POST.get("student_id")
        if not student_id:
            return HttpResponseBadRequest("Missing student_id")

        current_student = get_object_or_404(User, pk=student_id)

        try:
            grade_obj = Grade.objects.get(student=current_student, lesson=current_lesson)
        except Grade.DoesNotExist:
            grade_obj = Grade(student=current_student, lesson=current_lesson)

        grade = request.POST.get("grade")
        if grade != "":
            grade_obj.grade = int(grade)

        homework_grade = request.POST.get("homework_grade")
        if homework_grade != "":
            grade_obj.homework_grade = int(homework_grade)

        grade_obj.save()
        return redirect(f'/teacher/{teacher_id}/lessons/{lesson_id}/')

    return None

