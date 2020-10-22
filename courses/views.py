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
    title = 'Courses list'
    template_name = 'course_list.html'
    model = Course
    paginate_by = 5


class CourseDetailView(TitleMixin, DetailView):
    title = 'Detail'
    template_name = 'course_detail.html'
    model = Course


class CourseCreateView(TitleMixin, LoginRequiredMixin, CreateView):
    title = 'Create course'
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')


class CourseUpdateView(TitleMixin, LoginRequiredMixin, UpdateView):
    title = 'Update course'
    template_name = 'form.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('index')


class CourseDeleteView(TitleMixin, LoginRequiredMixin, DeleteView):
    title = 'Confirm delete course'
    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')
