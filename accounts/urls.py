from django.urls import path

from accounts.views import (
    SubmittableLoginView,
    SubmittablePasswordChangeView,
    SuccessMessagedLogoutView,
    SignUpView,
    ProfileView,
    StudentEnrollCourseView,
    StudentCourseDetailView
)


app_name = 'accounts'
urlpatterns = [
    path('login/', SubmittableLoginView.as_view(), name='login'),
    path('logout/', SuccessMessagedLogoutView.as_view(), name='logout'),
    path('password-change/', SubmittablePasswordChangeView.as_view(), name='password_change'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('enroll-course', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('course/<slug:slug>', StudentCourseDetailView.as_view(), name='student_course_detail'),
    path('course/<slug:slug>/<module_id>', StudentCourseDetailView.as_view(), name='student_course_detail_module')
]
