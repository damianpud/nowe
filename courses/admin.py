from django.contrib import admin
from .models import Technology, Course, Module

admin.site.register(Technology)
admin.site.register(Module)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'technology', 'starts', 'finishes', 'price']
    list_filter = ['technology']
    search_fields = ['title']
