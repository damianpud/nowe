from django.shortcuts import render
from django.views.generic import FormView, CreateView
from django.views import View
from django.urls import reverse_lazy

from courses.models import Course
from courses.forms import CourseForm


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


class CourseCreateView(CreateView):
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')


