from courses.models import Course, Technology, Module, Content
from courses.forms import CourseForm, ModuleFormSet
from courses.serializers import TechnologySerializer, CourseSerializer, CourseShortSerializer

from sdaworld.mixins import TitleMixin, SuccessMessagedFormMixin

from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework_xml.renderers import XMLRenderer

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils.text import slugify
from django.utils.html import escape
from django.utils.safestring import SafeString
from django.forms.models import modelform_factory

from accounts.forms import CourseEnrollForm


class TechnologyViewSet(ModelViewSet):
    queryset = Technology.objects
    serializer_class = TechnologySerializer
    renderer_classes = APIView.renderer_classes + [XMLRenderer]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    class pagination_class(PageNumberPagination):
        page_query_param = 'p'
        page_size = 10
        page_size_query_param = 'per_page'

    def get_serializer_class(self):
        if self.action == 'list':
            return CourseShortSerializer
        return super().get_serializer_class()


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class OwnerMixin(object):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(owner=self.request.user)


class OwnerEditMixin(object):
    def form_valid(self, form):
        course = form.save(commit=False)
        form.instance.owner = self.request.user
        course.save()
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin):
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'form.html'
    form_class = CourseForm
    success_url = reverse_lazy('index')


class CourseListView(TitleMixin, ListView):
    title = 'Courses list'
    template_name = 'course_list.html'
    model = Course
    paginate_by = 5


class OwnerCourseListView(TitleMixin,
                          OwnerCourseMixin,
                          ListView):
    title = 'Your courses'
    template_name = 'course_list.html'
    paginate_by = 5


class CourseDetailView(TitleMixin, DetailView):
    title = 'Detail'
    template_name = 'course_detail.html'
    model = Course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        return context


class CourseCreateView(TitleMixin,
                       SuccessMessagedFormMixin,
                       PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       CreateView):
    title = 'Create course'
    permission_required = 'courses.add_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> added!')

    def form_valid(self, form):
        course = form.save(commit=False)
        course.slug = slugify(str(f'{course.pk}-') + course.title)
        course.owner = self.request.user
        course.save()
        return super().form_valid(form)


class CourseUpdateView(TitleMixin,
                       StaffRequiredMixin,
                       SuccessMessagedFormMixin,
                       PermissionRequiredMixin,
                       OwnerCourseEditMixin,
                       UpdateView):
    title = 'Update course'
    permission_required = 'courses.change_course'

    def get_success_message(self):
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        return SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> updated!')

    def form_valid(self, form):
        course = form.save(commit=False)
        course.slug = slugify(str(f'{course.pk}-') + course.title)
        course.save()
        return super().form_valid(form)


class CourseDeleteView(TitleMixin,
                       StaffRequiredMixin,
                       PermissionRequiredMixin,
                       OwnerCourseMixin,
                       DeleteView):
    title = 'Confirm delete course'
    template_name = 'course_confirm_delete.html'
    model = Course
    success_url = reverse_lazy('index')
    permission_required = 'courses.delete_course'

    def test_func(self):
        return super().test_func() and self.request.user.is_superuser

    def get_title(self):
        safe_title = escape(self.object.title)
        return SafeString(f'Delete <em>{safe_title}</em>')

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        safe_title = escape(self.object.title)
        safe_technology = escape(self.object.technology)
        message = SafeString(f'Course <strong>{safe_title} {safe_technology}</strong> removed.')
        messages.success(request, message)
        return result


class CourseModuleUpdateView(TemplateResponseMixin, View):

    template_name = 'formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course': self.course, 'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:owner_courses_list')
        return self.render_to_response({'course': self.course, 'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'content_form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model, id=id, owner=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form, 'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj, data=request.POST, files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                Content.objects.create(module=self.module, item=obj)
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content, id=id, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, course__owner=request.user)
        return self.render_to_response({'module': module})
