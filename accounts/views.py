from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.html import escape
from django.utils.safestring import SafeString

from courses.models import Course
from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin
from .forms import (
    SubmittableAuthenticationForm,
    SubmittablePasswordChangeForm,
    SignUpForm,
    CourseEnrollForm
)


class SubmittableLoginView(TitleMixin,
                           SuccessMessagedFormMixin,
                           LoginView):
    title = 'Login'
    success_message = 'You are successfully logged in!'
    form_class = SubmittableAuthenticationForm
    template_name = 'form.html'


class SubmittablePasswordChangeView(TitleMixin,
                                    SuccessMessagedFormMixin,
                                    PasswordChangeView):
    title = 'Password Change'
    success_message = 'Password successfully changed!'
    form_class = SubmittablePasswordChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')


class SuccessMessagedLogoutView(LogoutView):
    def get_next_page(self):
        result = super().get_next_page()
        messages.success(self.request, 'Successfully logged out!')
        return result


class SignUpView(TitleMixin,
                 SuccessMessagedFormMixin,
                 CreateView):
    title = 'Sign up'
    success_message = 'You are successfully sign in!'
    form_class = SignUpForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class ProfileView(TitleMixin, LoginRequiredMixin, TemplateView):
    title = 'Profile'
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        result = super().get_context_data(**kwargs)
        courses = Course.objects.get_queryset().filter(students__in=[self.request.user])
        if courses is not None:
            result['courses'] = courses
        return result


class StudentEnrollCourseView(LoginRequiredMixin,
                              SuccessMessagedFormMixin,
                              FormView):
    course = None
    form_class = CourseEnrollForm
    success_message = None

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        safe_title = escape(self.course)
        self.success_message = SafeString(
            f'Congratulations you have successfully enrolled the <strong>{safe_title}</strong> course!'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'student_course_detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
        else:
            context['module'] = course.modules.all()[0]
        return context
