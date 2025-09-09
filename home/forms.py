from django import forms
from .models import Account, Transaction
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from khayyam import JalaliDate
from datetime import date
from .validators import validate_custom_date_format


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        exclude = [
            "user",
        ]

        labels = {
            "full_name": "نام و نام خانوادگی",
            "email": "ایمیل",
            "phone_number": "شماره تلفن",
            "address": "آدرس",
        }
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "نام و نام خانوادگی را وارد کنید",
                }
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "ایمیل را وارد کنید"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "شماره تلفن را وارد کنید",
                }
            ),
            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "آدرس را وارد کنید",
                    "rows": 1,
                }
            ),
        }

    # class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].initial = timezone.now().date()

    class Meta:
        model = Transaction
        fields = ["amount", "type", "date", "description"]
        labels = {
            "amount": "مبلغ",
            "type": "نوع تراکنش",
            "date": "تاریخ",
            "description": "توضیحات",
        }
        exclude = [
            "type",
        ]
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مبلغ را وارد کنید",
                    "dir": "rtl",
                }
            ),
            "type": forms.Select(attrs={"class": "form-select", "dir": "rtl"}),
            "date": forms.DateInput(
                attrs={"class": "form-control", "type": "date", "dir": "rtl"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "توضیحات تراکنش",
                    "dir": "rtl",
                }
            ),
        }


class TransactionForm(forms.ModelForm):
    now = timezone.now().date()
    jalali_date = JalaliDate(now)  # یا: JalaliDate.fromdate(now)
    formatted = f"{jalali_date.year}/{jalali_date.month:02}/{jalali_date.day:02}"

    date = forms.CharField(
        label="تاریخ",
        max_length=10,
        validators=[validate_custom_date_format],
        widget=forms.TextInput(
            attrs={
                "placeholder": "مثلاً 1402/07/18",
                "class": "form-control",
                "dir": "rtl",
            }
        ),
        initial=formatted,
    )

    def clean_date(self):
        value = self.cleaned_data.get("date")
        if not value:
            raise forms.ValidationError("تاریخ وارد نشده است.")

        parts = value.split("/")
        if len(parts) != 3:
            raise forms.ValidationError("فرمت تاریخ باید به صورت yyyy/mm/dd باشد.")

        try:
            year, month, day = map(int, parts)
            jalali_date = JalaliDate(year, month, day)
            gregorian_date = jalali_date.todate()
            print('*'*90)
            print(gregorian_date)
            return gregorian_date
        except ValueError:
            raise forms.ValidationError("فرمت تاریخ اشتباه است.")
        except Exception:
            raise forms.ValidationError("تاریخ وارد شده معتبر نیست یا قابل تبدیل نیست.")

    class Meta:
        model = Transaction
        fields = ["amount", "date", "description"]  # حذف type چون در exclude بود
        labels = {
            "amount": "مبلغ",
            "date": "تاریخ",
            "description": "توضیحات",
        }
        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "مبلغ را وارد کنید",
                    "dir": "rtl",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "توضیحات تراکنش",
                    "dir": "rtl",
                }
            ),
        }


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(
        label="نام کاربری",
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام کاربری را وارد کنید"}
        ),
    )
    password = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور را وارد کنید"}
        ),
    )


class ResetPasswordForm(forms.Form):
    old_password = forms.CharField(
        label="رمز عبور قبلی",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور قبلی را وارد کنید"}
        ),
    )
    new_password = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور جدید را وارد کنید"}
        ),
    )
    confirm_password = forms.CharField(
        label="تکرار رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "رمز عبور جدید را دوباره وارد کنید",
            }
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="نام کاربری",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "نام کاربری", "dir": "rtl"}
        ),
    )
    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "رمز عبور", "dir": "rtl"}
        ),
    )
    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "تکرار رمز عبور",
                "dir": "rtl",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
