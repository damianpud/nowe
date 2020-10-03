from django.forms import Form, CharField, DateField, IntegerField, ModelChoiceField, Textarea, BooleanField
from courses.models import Technology, Course


class CourseForm(Form):
    title = ModelChoiceField(queryset=Course.objects)
    tech = ModelChoiceField(queryset=Technology.objects)
    description = CharField(widget=Textarea, required=False)
    starts = DateField()
    finishes = DateField()
    max_atendees_counts = IntegerField(min_value=5, max_value=30)
    price = IntegerField()
    remote = BooleanField()
