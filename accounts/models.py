from django.db.models import CASCADE, Model, OneToOneField, TextField, ImageField
from django.contrib.auth.models import User


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    image = ImageField(null=True, blank=True)
    biography = TextField(null=True, blank=True)

