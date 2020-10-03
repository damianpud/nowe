from django.shortcuts import render
from django.http import HttpResponse

from courses.models import Course


def hello(request):
    return render(request, template_name='hello.html')


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )