from rest_framework.serializers import HyperlinkedIdentityField, HyperlinkedRelatedField, ModelSerializer

from courses.models import Technology, Course


class TechnologySerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='courses:technology-detail')

    class Meta:
        model = Technology
        exclude = []


class CourseShortSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='courses:course-detail')
    technology = TechnologySerializer

    class Meta:
        model = Course
        fields = ['url', 'title', 'technology', 'starts', 'price']


class CourseSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='courses:course-detail')
    technology = HyperlinkedRelatedField(
        queryset=Technology.objects, view_name='courses:technology-detail'
    )

    class Meta:
        model = Course
        exclude = []
