from django.urls import path, include

from rest_framework.routers import DefaultRouter

from courses.views import CourseCreateView, CourseDetailView, CourseUpdateView, CourseDeleteView,\
    CourseListView, TechnologyViewSet, CourseViewSet, OwnerCourseListView, CourseModuleUpdateView,\
    ContentCreateUpdateView

router = DefaultRouter()
router.register('technology', TechnologyViewSet)
router.register('course', CourseViewSet)

app_name = 'courses'
urlpatterns = [
    path('list', CourseListView.as_view(), name='course_list'),
    path('owner_courses_list', OwnerCourseListView.as_view(), name='owner_courses_list'),
    path('create', CourseCreateView.as_view(), name='course_create'),
    path('update/<pk>', CourseUpdateView.as_view(), name='course_update'),
    path('delete/<pk>', CourseDeleteView.as_view(), name='course_delete'),
    path('detail/<pk>', CourseDetailView.as_view(), name='course_detail'),
    path('<pk>/module', CourseModuleUpdateView.as_view(), name='course_module_update'),
    path('module/<int:module_id>/content/<model_name>/create/',
         ContentCreateUpdateView.as_view(),
         name='module_content_create'),
    path('module/<int:module_id>/content/<model_name>/<id>/',
         ContentCreateUpdateView.as_view(),
         name='module_content_update'),
    path('api/', include(router.urls))
]
