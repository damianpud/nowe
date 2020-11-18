from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer

from courses.models import Technology, Course


class TechnologySerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='courses:technology-detail')

    class Meta:
        model = Technology
        exclude = []


class CourseSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='courses:course-detail')

    class Meta:
        model = Course
        exclude = []
