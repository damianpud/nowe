import re
from datetime import date

from django.forms import CharField, DateField, IntegerField, FloatField, ModelChoiceField, Textarea, BooleanField, ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit, Button

from courses.models import Technology, Course


def capitalized_validator(value):
    if value[0].islower():
        raise ValidationError('Value must be capitalized.')


class FutureMonthField(DateField):

    def validate(self, value):
        super().validate(value)
        if value <= date.today():
            raise ValidationError('Only future dates allowed here.')

    def clean(self, value):
        result = super().clean(value)
        return date(year=result.year, month=result.month, day=1)


class CourseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title'),
                Column('technology')
            ),
            'description',
            Row(
                Column('starts'),
                Column('finishes'),
                Column('remote')
            ),
            Row(
                Column('max_attendees_counts'),
                Column('price')
            ),
            Row(
                Submit('submit', 'Dodaj kurs', css_class="btn-success"),
                Button('cancel', 'Anuluj', css_class="btn-outline-danger")
            ),
        )

    class Meta:
        model = Course
        exclude = ['max_atendees_counts']

    title = CharField(validators=[capitalized_validator])
    technology = ModelChoiceField(queryset=Technology.objects)
    description = CharField(widget=Textarea, required=False)
    starts = FutureMonthField()
    finishes = FutureMonthField()
    max_attendees_counts = IntegerField(min_value=5, max_value=30)
    price = FloatField()
    remote = BooleanField(required=False)

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        self.cleaned_data['description'] = cleaned
        return cleaned

    # def clean_price(self):
    #     initial = self.cleaned_data['price']
    #     cleaned = round(initial, 2)
    #     self.cleaned_data['price'] = cleaned
    #     return cleaned


