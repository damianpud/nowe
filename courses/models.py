from django.db import models
from django.db.models import CharField, Model, IntegerField, TextField, DateField


class Courses(Model):
    name = CharField(max_length=128)
    hours = IntegerField()
    price = IntegerField()
    description = TextField()
    start = DateField()

    def __str__(self):
        return self.name
