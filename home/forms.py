from django import forms
from .models import Account, Transaction
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"  
        exclude = ['user',]
        
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


class TransactionForm(forms.ModelForm):
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
