from django.db import models
from django.db.models import ForeignKey
from django.contrib.auth.models import User


class SchoolClass(models.Model):
    class_name = models.CharField(max_length=20)

    def __str__(self):
        return self.class_name

    def __repr__(self):
        return self.class_name

class StudentClass(models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.sclass.class_name}"

    def __repr__(self):
        return f"{self.student.username} - {self.sclass.class_name}"

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    teacher = ForeignKey(User, on_delete=models.CASCADE)
    sclass = ForeignKey(SchoolClass, on_delete=models.CASCADE)
    homework = models.TextField()
    room = models.CharField(max_length=20)
    lesson_type = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.teacher.username} - {self.sclass.class_name} - {self.date}"

    def __repr__(self):
        return f"{self.name} - {self.teacher.username} - {self.sclass.class_name} - {self.date}"

class Grade(models.Model):
    student = ForeignKey(User, on_delete=models.CASCADE)
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.IntegerField()
    homework_grade = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.name} - {self.grade} - {self.homework_grade}"

    def __repr__(self):
        return f"{self.student.username} - {self.lesson.name} - {self.grade} - {self.homework_grade}"