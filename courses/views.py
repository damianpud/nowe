from courses.models import Course, Technology
from courses.forms import CourseForm
from courses.serializers import TechnologySerializer, CourseSerializer, CourseShortSerializer

from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.html import escape
from django.utils.safestring import SafeString

from accounts.forms import CourseEnrollForm


def courses(request):
    return render(
        request, template_name='courses.html',
        context={'courses': Course.objects.all().order_by('price')}
    )


class TechnologyViewSet(ModelViewSet):
    queryset = Technology.objects
    serializer_class = TechnologySerializer
    renderer_classes = APIView.renderer_classes + [XMLRenderer]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    class pagination_class(PageNumberPagination):
        page_query_param = 'p'
        page_size = 10
        page_size_query_param = 'per_page'

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseShortSerializer
        return super().get_serializer_class()


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


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        course = form.save(commit=False)
        form.instance.owner = self.request.user
        course.save()
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')


class OwnerCourseListView(OwnerCourseMixin,
                          ListView):
    template_name = 'course_list.html'
    paginate_by = 5


class CourseDetailView(TitleMixin,
                       LoginRequiredMixin,
                       DetailView):
    title = 'Detail'
    template_name = 'course_detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


class CourseCreateView(TitleMixin,
                       SuccessMessagedFormMixin,
                       PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    title = 'Create course'
    permission_required = 'courses.add_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> added!')


class CourseUpdateView(TitleMixin,
                       StaffRequiredMixin,
                       SuccessMessagedFormMixin,
                       PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    title = 'Update course'
    permission_required = 'courses.change_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> updated!')


class CourseDeleteView(TitleMixin,
                       StaffRequiredMixin,
                       PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
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
