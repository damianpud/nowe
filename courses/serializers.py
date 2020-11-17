from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer

from courses.models import Technology


class TechnologySerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='courses:technology-detail')

    class Meta:
        model = Technology
        exclude = []

