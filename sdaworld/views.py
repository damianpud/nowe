from courses.views import CourseListView


class IndexView(CourseListView):
    title = 'Welcome to Courses world!'
    template_name = 'index.html'
