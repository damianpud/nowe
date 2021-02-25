from django.contrib import admin
from .models import Technology, Course

admin.site.register(Technology)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'technology', 'starts', 'finishes', 'price']
    list_filter = ['technology']
    search_fields = ['title']
