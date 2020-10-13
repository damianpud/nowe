from courses.views import CourseListView


class IndexView(CourseListView):
    title = 'Welcome to SDA world!'
    template_name = 'index.html'
