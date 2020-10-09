from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit

from django.contrib.auth.forms import AuthenticationForm


class SubmittableAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(*self.fields, Submit('submit', 'Submit'))
