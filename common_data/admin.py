from django.contrib import admin

from common_data.models import SchoolClass, StudentClass, Grade, Lesson

admin.site.register(SchoolClass)
admin.site.register(StudentClass)
admin.site.register(Grade)
admin.site.register(Lesson)