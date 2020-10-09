"""sdaworld URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth.views import LoginView

from courses.models import Technology, Course
from courses.views import CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView,\
    CourseView, CourseListView


admin.site.register(Technology)
admin.site.register(Course)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login', LoginView.as_view, name='login'),
    path('', CourseView.as_view(), name='index'),
    path('course/list', CourseListView.as_view(), name='course_list'),
    path('course/create', CourseCreateView.as_view(), name='course_create'),
    path('course/update/<pk>', CourseUpdateView.as_view(), name='course_update'),
    path('course/delete/<pk>', CourseDeleteView.as_view(), name='course_delete'),
    path('course/detail/<pk>', CourseDetailView.as_view(), name='course_detail')
]
