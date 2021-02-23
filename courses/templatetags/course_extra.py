from django.template import Library
from django.utils.html import escape
from django.utils.safestring import SafeString

register = Library()


@register.simple_tag
def course_format(course, short=False):
    if short:
        return f'{course.title} ({course.technology})'
    return f'{course.title} ({course.technology}) - {course.price} PLN'


@register.filter
def attr_as_p(obj, attrname):
    label = escape(attrname.capitalize())
    value = escape(getattr(obj, attrname))
    if label == 'File':
        return SafeString(f'<p><strong>{label}:</strong> <a href="/media/{value}">{value}</a></p>')
    elif label == 'Description':
        return SafeString(f'<p><strong>{label}:</strong><p><p>{value}</p>')
    elif label == 'Price':
        return SafeString(f'<p><strong>{label}:</strong> {value} PLN</p>')
    return SafeString(f'<p><strong>{label}:</strong> {value}</p>')
