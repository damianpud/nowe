from django.urls import path, include

from rest_framework.routers import DefaultRouter

from courses.views import CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView,\
    CourseListView

router = DefaultRouter()

app_name = 'courses'
urlpatterns = [
    path('course/list', CourseListView.as_view(), name='course_list'),
    path('course/create', CourseCreateView.as_view(), name='course_create'),
    path('course/update/<pk>', CourseUpdateView.as_view(), name='course_update'),
    path('course/delete/<pk>', CourseDeleteView.as_view(), name='course_delete'),
    path('course/detail/<pk>', CourseDetailView.as_view(), name='course_detail'),
    path('api/', include(router.urls))
]
