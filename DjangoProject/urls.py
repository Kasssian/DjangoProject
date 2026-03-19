"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from university.views import students_page, progress_page, lectures_page, teacher_login_view, verify_2fa_view, \
    edit_grade_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', students_page, name='students-list'),
    path('progress/', progress_page, name='progress-list'),
    path('lectures/', lectures_page, name='lectures-list'),
    path('login/', teacher_login_view, name='teacher-login'),
    path('verify-2fa/', verify_2fa_view, name='verify-2fa'),
    path('progress/edit/<int:pk>/', edit_grade_view, name='edit-grade'),
]
