import re
from khayyam import JalaliDate
from django.core.exceptions import ValidationError

def validate_custom_date_format(value):
    # بررسی فرمت عددی: YYYY/MM/DD یا YYYY-MM-DD
    pattern = r'^\d{4}[-/]\d{2}[-/]\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError("فرمت تاریخ باید به صورت YYYY/MM/DD  باشد.")

    # بررسی اعتبار واقعی تاریخ شمسی
    try:
        parts = re.split(r'[-/]', value)
        year, month, day = map(int, parts)
        JalaliDate(year, month, day)  # اگر نامعتبر باشه، خطا می‌ده
    except Exception:
        raise ValidationError("تاریخ وارد شده معتبر نیست یا خارج از محدوده است.")
