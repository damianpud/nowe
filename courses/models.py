from django.db.models import CharField, Model, IntegerField, TextField, DateField, BooleanField, ForeignKey, DO_NOTHING


class Technology(Model):
    name = CharField(max_length=32)

    def __str__(self):
        return self.name


class Course(Model):
    title = CharField(max_length=128)
    technology = ForeignKey(Technology, on_delete=DO_NOTHING)
    description = TextField(null=True, blank=True)
    starts = DateField()
    finishes = DateField()
    max_atendees_counts = IntegerField()
    price = IntegerField()
    remote = BooleanField()

    def __str__(self):
        return self.title
