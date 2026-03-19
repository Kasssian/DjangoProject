from django.contrib import admin

from .models import Region, Nationality, Faculty, Specialty, Group, Student, Teacher, Subject, ProgressInStudy, Lecture

admin.site.register(Region)
admin.site.register(Nationality)
admin.site.register(Subject)


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('name',)


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty')
    list_filter = ('specialty',)
    search_fields = ('name',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'region', 'nationality')
    list_filter = ('group', 'region', 'nationality')
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name',)


@admin.register(ProgressInStudy)
class ProgressInStudyAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'term', 'prize')
    list_filter = ('term', 'subject', 'prize')
    search_fields = ('student__name', 'subject__name')


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ('subject', 'group', 'teacher')
    list_filter = ('subject', 'group', 'teacher')
