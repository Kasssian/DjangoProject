from django.contrib.auth.models import User
from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Регион")

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"

    def __str__(self):
        return self.name


class Nationality(models.Model):
    name = models.CharField(max_length=100, verbose_name="Национальность")

    class Meta:
        verbose_name = "Национальность"
        verbose_name_plural = "Национальности"

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=150, verbose_name="Факультет")

    class Meta:
        verbose_name = "Факультет"
        verbose_name_plural = "Факультеты"

    def __str__(self):
        return self.name


class Specialty(models.Model):
    name = models.CharField(max_length=150, verbose_name="Специальность")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Факультет")

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=50, verbose_name="Группа")
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name="Специальность")

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Аккаунт пользователя")
    name = models.CharField(max_length=150, verbose_name="ФИО Студента")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, verbose_name="Регион")
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, verbose_name="Национальность")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Аккаунт пользователя")
    name = models.CharField(max_length=150, verbose_name="ФИО Преподавателя")
    address = models.TextField(verbose_name="Адрес")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=150, verbose_name="Предмет")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return self.name


class ProgressInStudy(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    term = models.IntegerField(verbose_name="Семестр")
    prize = models.CharField(max_length=50, verbose_name="Оценка/Награда")

    class Meta:
        verbose_name = "Запись об успеваемости"
        verbose_name_plural = "Успеваемость"

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"


class Lecture(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="Преподаватель")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name="Группа")

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Расписание лекций"

    def __str__(self):
        return f"{self.subject.name} ({self.group.name}) - {self.teacher.name}"
