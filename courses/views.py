from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, ListView
from django.views import View

from courses.models import Course
from courses.forms import CourseForm


def hello(request):
    return render(request, template_name='hello.html')


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )


class CourseView(View):
    def get(self, request):
        return render(
            request, template_name='courses.html',
            context={'courses': Course.objects.all().order_by('price')}
        )


class CourseCreateView(FormView):
    template_name = 'form.html'
    form_class = CourseForm