from django import template
from khayyam import JalaliDate

register = template.Library()

@register.filter
def jalali(value):
    if not value:
        return ""
    return JalaliDate(value).strftime('%Y/%m/%d')
