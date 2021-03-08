from django.db.models import CharField, Model, IntegerField, TextField, DateField, BooleanField, ForeignKey,\
    DO_NOTHING, FloatField, FileField, ImageField, ManyToManyField, CASCADE, PositiveIntegerField, DateTimeField, \
    URLField
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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
    price = FloatField()
    file = FileField(null=True, blank=True)
    remote = BooleanField()
    image = ImageField(null=True, blank=True)
    students = ManyToManyField(User, related_name='courses_joined', blank=True)

    def __str__(self):
        return self.title


class Module(Model):
    course = ForeignKey(Course, on_delete=CASCADE)
    title = CharField(max_length=256)
    description = TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Content(Model):
    module = ForeignKey(Module, related_name='contents', on_delete=DO_NOTHING)
    content_type = ForeignKey(ContentType,
                              limit_choices_to={'model__in': ('text', 'video', 'image', 'file')},
                              on_delete=DO_NOTHING)
    object_id = PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(Model):
    owner = ForeignKey(User, related_name='%(class)s_related', on_delete=CASCADE)
    title = CharField(max_length=250)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = TextField()


class File(ItemBase):
    file = FileField(upload_to='files')


class Image(ItemBase):
    file = ImageField(upload_to='images')


class Video(ItemBase):
    url = URLField()
