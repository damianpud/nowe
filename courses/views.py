from courses.models import Course, Technology
from courses.forms import CourseForm
from courses.serializers import TechnologySerializer

from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin

from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.html import escape
from django.utils.safestring import SafeString


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )


class TechnologyViewSet(ModelViewSet):
    queryset = Technology.objects
    serializer_class = TechnologySerializer


class CourseView(ListView):
    template_name = 'courses.html'
    model = Course


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CourseListView(TitleMixin, ListView):
    title = 'Courses list'
    template_name = 'course_list.html'
    model = Course
    paginate_by = 5


class CourseDetailView(TitleMixin, LoginRequiredMixin, DetailView):
    title = 'Detail'
    template_name = 'course_detail.html'
    model = Course


class CourseCreateView(TitleMixin, SuccessMessagedFormMixin, PermissionRequiredMixin, CreateView):
    title = 'Create course'
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')
    permission_required = 'courses.add_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> added!')


class CourseUpdateView(TitleMixin, StaffRequiredMixin, SuccessMessagedFormMixin, PermissionRequiredMixin, UpdateView):
    title = 'Update course'
    template_name = 'form.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy('index')
    permission_required = 'courses.change_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> updated!')


class CourseDeleteView(TitleMixin, StaffRequiredMixin, PermissionRequiredMixin, DeleteView):
    title = 'Confirm delete course'
    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')
    permission_required = 'courses.delete_course'

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser

    def get_title(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Delete <em>{safe_title}</em>')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        message = SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> removed.')
        messages.success(request, message)
        return result
