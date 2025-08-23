from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        labels = {
            'full_name': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'phone_number': 'شماره تلفن',
            'address': 'آدرس',
        }
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی را وارد کنید'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل را وارد کنید'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره تلفن را وارد کنید'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس را وارد کنید',
                'rows': 1
            }),
        }
