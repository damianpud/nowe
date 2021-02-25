from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.forms import Form, CharField, Textarea, ImageField, EmailField
from django.db.transaction import atomic

from accounts.models import Profile


class SubmittableForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(*self.fields, Submit('submit', 'Submit'))


class SubmittableAuthenticationForm(SubmittableForm, AuthenticationForm):
    pass


class SubmittablePasswordChangeForm(SubmittableForm, PasswordChangeForm):
    pass


class SignUpForm(SubmittableForm, UserCreationForm):

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'email']

    email = EmailField(required=True)
    biography = CharField(label='Tell us your story with courses', widget=Textarea, max_length=250, required=False)
    image = ImageField(required=False)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        biography = self.cleaned_data['biography']
        image = self.cleaned_data['image']
        profile = Profile(biography=biography, image=image, user=result)
        if commit:
            profile.save()
        return result
