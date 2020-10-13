from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib import messages
from accounts.forms import SubmittableAuthenticationForm, SubmittablePasswordChangeForm
from django.urls import reverse_lazy
from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin


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
