from courses.models import Course
from courses.forms import CourseForm

from sdaworld.mixins import TitleMixin

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )


class CourseView(ListView):
    template_name = 'courses.html'
    model = Course


class CourseListView(TitleMixin, ListView):
    title = 'Lista kursow'
    template_name = 'course_list.html'
    model = Course


class CourseDetailView(TitleMixin, DetailView):
    title = 'Szczegóły'
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


class CourseDeleteView(TitleMixin, LoginRequiredMixin, DeleteView):
    title = 'Potwierdz usuniecie kursu'
    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')

