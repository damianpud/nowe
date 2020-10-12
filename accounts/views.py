from django.contrib.auth.views import LoginView, PasswordChangeView
from accounts.forms import SubmittableAuthenticationForm, SubmittablePasswordChangeForm
from django.urls import reverse_lazy


class SubmittableLoginView(LoginView):
    form_class = SubmittableAuthenticationForm
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    form_class = SubmittablePasswordChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('index')