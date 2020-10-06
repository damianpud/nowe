from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from logging import getLogger

from courses.models import Course
from courses.forms import CourseForm


LOGGER = getLogger()


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


class CourseCreateView(CreateView):
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while creating a movie')
        return super().form_invalid(form)


class CourseUpdateView(UpdateView):
    template_name = 'form.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('index')

    def form_invalid(self, form):
        LOGGER.warning('User provided invalid data while updating a movie')
        return super().form_invalid(form)


class CourseDeleteView(DeleteView):

    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')
