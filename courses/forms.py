import re
from datetime import date

from django.forms import CharField, DateField, IntegerField, FloatField, ModelChoiceField, Textarea, BooleanField, ModelForm
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit

from courses.models import Technology, Course


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
            'title',
            Row(Column('technology'), Column('starts'), Column('finishes'), Column('max_attendees_counts')),
            'description',
            'price',
            'remote',
            Submit('submit', 'Submit')
        )

    class Meta:
        model = Course
        fields = '__all__'
        exclude = ['max_atendees_counts']

    title = ModelChoiceField(queryset=Course.objects)
    technology = ModelChoiceField(queryset=Technology.objects)
    description = CharField(widget=Textarea, required=False)
    starts = FutureMonthField()
    finishes = FutureMonthField()
    max_attendees_counts = IntegerField()
    price = FloatField(min_value=5, max_value=30)
    remote = BooleanField(required=False)

    def clean_description(self):
        initial = self.cleaned_data['description']
        sentences = re.sub(r'\s*\.\s*', '.', initial).split('.')
        cleaned = '. '.join(sentence.capitalize() for sentence in sentences)
        self.cleaned_data['description'] = cleaned
        return cleaned

    def clean_price(self):
        initial = self.cleaned_data['price']
        cleaned = round(initial, 2)
        self.cleaned_data['price'] = cleaned
        return cleaned
