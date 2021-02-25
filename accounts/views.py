from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin
from accounts.forms import (
    SubmittableAuthenticationForm,
    SubmittablePasswordChangeForm,
    SignUpForm
)


class SubmittableLoginView(TitleMixin, SuccessMessagedFormMixin, LoginView):
    title = 'Login'
    success_message = 'You are successfully logged in!'
    form_class = SubmittableAuthenticationForm
    template_name = 'form.html'


class SubmittablePasswordChangeView(TitleMixin, SuccessMessagedFormMixin, PasswordChangeView):
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


class SignUpView(TitleMixin, SuccessMessagedFormMixin, CreateView):
    title = 'Sign up'
    success_message = 'You are successfully sign in!'
    form_class = SignUpForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super(SignUpView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result


class ProfileView(TitleMixin, TemplateView):
    title = 'Profile'
    template_name = 'profile.html'
