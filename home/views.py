from django.shortcuts import render
from django.views import View
from .models import Account, Transaction
from .forms import AccountForm


class HomeView(View):
    def get(self, request):
        return render(
            request,
            "home/home.html",
        )


class AccountsView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return render(request, "home/accounts.html", {"accounts": accounts})


class AccountRegisterView(View):
    form_class = AccountForm

    def get(self, request):
        form = self.form_class
        return render(request, "home/account_register.html", {"form": form})
    
