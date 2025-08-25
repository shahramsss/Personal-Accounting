from django import template

register = template.Library()

@register.filter
def fa_digits(value):
    fa_numbers = {
        '0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴',
        '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'
    }
    return ''.join(fa_numbers.get(ch, ch) for ch in str(value))
