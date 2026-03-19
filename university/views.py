import random

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets

from .models import Region, Nationality, Faculty, Specialty, Group, Student, Teacher, Subject, ProgressInStudy, Lecture
from .serializers import (RegionSerializer, NationalitySerializer, FacultySerializer,
                          SpecialtySerializer, GroupSerializer, StudentSerializer,
                          TeacherSerializer, SubjectSerializer, ProgressInStudySerializer, LectureSerializer)


def universal_login_view(request):
    if request.user.is_authenticated:
        return redirect('students-list')

    if request.method == 'POST':
        user_param = request.POST.get('username')
        pass_param = request.POST.get('password')

        user = authenticate(request, username=user_param, password=pass_param)

        if user is not None:
            # 1. Если это ПРЕПОДАВАТЕЛЬ -> отправляем на 2FA
            if hasattr(user, 'teacher'):
                otp = str(random.randint(100000, 999999))
                request.session['pre_2fa_user_id'] = user.id
                request.session['2fa_code'] = otp
                print(f"\n{'=' * 40}\nКОД ДЛЯ ВХОДА ПРЕПОДАВАТЕЛЯ {user.username}: {otp}\n{'=' * 40}\n")
                return redirect('verify-2fa')

            else:
                login(request, user)
                return redirect('students-list')
        else:
            return render(request, 'university/login.html', {'error': 'Неверный логин или пароль.'})

    return render(request, 'university/login.html')


def teacher_login_view(request):
    if request.method == 'POST':
        user_param = request.POST.get('username')
        pass_param = request.POST.get('password')

        # Шаг 1: Проверяем логин и пароль (здесь под капотом работает хеширование Argon2/bcrypt)
        user = authenticate(request, username=user_param, password=pass_param)

        if user is not None:
            # Проверяем, является ли этот пользователь преподавателем
            if hasattr(user, 'teacher'):
                # Генерируем 6-значный код
                otp = str(random.randint(100000, 999999))

                # Сохраняем ID пользователя и код во временной сессии
                request.session['pre_2fa_user_id'] = user.id
                request.session['2fa_code'] = otp

                # СИМУЛЯЦИЯ ОТПРАВКИ: Выводим код в консоль
                print(f"\n{'=' * 40}\nКОД ДЛЯ ВХОДА ПРЕПОДАВАТЕЛЯ {user.username}: {otp}\n{'=' * 40}\n")

                return redirect('verify-2fa')
            else:
                return render(request, 'university/login.html', {'error': 'Этот аккаунт не принадлежит преподавателю.'})
        else:
            return render(request, 'university/login.html', {'error': 'Неверный логин или пароль.'})

    return render(request, 'university/login.html')


def verify_2fa_view(request):
    # Проверяем, прошел ли человек первый этап (ввод пароля)
    if 'pre_2fa_user_id' not in request.session:
        return redirect('teacher-login')

    if request.method == 'POST':
        entered_code = request.POST.get('otp_code')
        correct_code = request.session.get('2fa_code')

        if entered_code == correct_code:
            # Код верный! Логиним пользователя по-настоящему
            user_id = request.session.get('pre_2fa_user_id')
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)
            login(request, user)

            # Очищаем сессию от временных данных
            del request.session['pre_2fa_user_id']
            del request.session['2fa_code']

            # Перенаправляем на страницу расписания (или любую другую)
            return redirect('lectures-list')
        else:
            return render(request, 'university/verify_2fa.html', {'error': 'Неверный код. Попробуйте снова.'})

    return render(request, 'university/verify_2fa.html')


def students_page(request):
    all_students = Student.objects.select_related('group', 'region').all()

    context = {
        'students': all_students
    }
    return render(request, 'university/students_list.html', context)


@login_required(login_url='/login/')
def progress_page(request):
    user = request.user

    if user.is_superuser:
        progresses = ProgressInStudy.objects.select_related('student', 'subject').all()

    elif hasattr(user, 'teacher'):
        teacher_subjects = Lecture.objects.filter(teacher=user.teacher).values_list('subject', flat=True)
        progresses = ProgressInStudy.objects.filter(subject__in=teacher_subjects).select_related('student', 'subject')

    elif hasattr(user, 'student'):
        progresses = ProgressInStudy.objects.filter(student=user.student).select_related('subject')

    else:
        progresses = []

    return render(request, 'university/progress_list.html', {'progresses': progresses})


@login_required(login_url='/login/')
def lectures_page(request):
    user = request.user

    if user.is_superuser:
        lectures = Lecture.objects.select_related('subject', 'group', 'teacher').all()

    elif hasattr(user, 'teacher'):
        lectures = Lecture.objects.filter(teacher=user.teacher).select_related('subject', 'group')

    elif hasattr(user, 'student'):
        lectures = Lecture.objects.filter(group=user.student.group).select_related('subject', 'teacher')

    else:
        lectures = []

    return render(request, 'university/lectures_list.html', {'lectures': lectures})


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class ProgressInStudyViewSet(viewsets.ModelViewSet):
    queryset = ProgressInStudy.objects.all()
    serializer_class = ProgressInStudySerializer


class LectureViewSet(viewsets.ModelViewSet):
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer


class NationalityViewSet(viewsets.ModelViewSet):
    queryset = Nationality.objects.all()
    serializer_class = NationalitySerializer


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class SpecialtyViewSet(viewsets.ModelViewSet):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer
