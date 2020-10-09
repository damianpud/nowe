from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from courses.models import Course
from courses.forms import CourseForm


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )


class CourseView(ListView):
    template_name = 'courses.html'
    model = Course


class CourseListView(ListView):
    template_name = 'course_list.html'
    model = Course


class CourseDetailView(DetailView):
    template_name = 'course_detail.html'
    model = Course


class CourseCreateView(LoginRequiredMixin, CreateView):
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'form.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('index')


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')
