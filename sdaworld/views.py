from courses.views import CourseListView


class IndexView(CourseListView):
    template_name = 'index.html'
