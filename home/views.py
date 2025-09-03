from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Account, Transaction
from .forms import AccountForm, TransactionForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum


class HomeView(View):
    def get(self, request):
        return render(
            request,
            "home/home.html",
        )


class AccountsView(View):
    def get(self, request):
        query = request.GET.get("q", "")
        accounts = Account.objects.all().order_by("-id")

        if query:
            accounts = accounts.filter(
                Q(full_name__icontains=query)
                | Q(address__icontains=query)
                | Q(email__icontains=query)
                | Q(phone_number__icontains=query)
            ).order_by("-id")
        paginator = Paginator(accounts, 20)  # نمایش ۱۰ حساب در هر صفحه
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, "home/accounts.html", {"accounts": page_obj})


class AccountRegisterView(View):
    form_class = AccountForm

    def get(self, request):
        form = self.form_class
        return render(request, "home/account_register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "حساب جدید ثبت شد.", "success")
            return redirect("home:accounts")
        return render(request, "home/account_register.html", {"form": form})


class DeleteAccountView(View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        return render(request, "home/delete_confirm.html", {"account": account})

    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return redirect("home:accounts")


class EditAccountView(View):
    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        form = AccountForm(instance=account)
        return render(
            request, "home/edit_account.html", {"form": form, "account": account}
        )

    def post(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.warning(request, "حساب با موفقیت ویرایش شد.", "warning")
            return redirect("home:accounts")
        # یا هر صفحه‌ای که لیست حساب‌ها رو نشون می‌ده
        return render(
            request, "home/edit_account.html", {"form": form, "account": account}
        )


class SelectAccountView(View):
    form_class = TransactionForm

    def get(self, request, pk):
        account = get_object_or_404(Account, id=pk)
        form = self.form_class
        return render(
            request,
            "home/select_account.html",
            {
                "form": form,
                "account": account,
            },
        )


class TransactionsView(View):
    def get(self, request):
        transactions = Transaction.objects.all()
        return render(request, "home/transactions.html", {"transactions": transactions})


class AccountTransactionsView(LoginRequiredMixin, View):
    def get(self, request, account_pk):
        account = get_object_or_404(Account, id=account_pk)
        transactions = account.transactions.all().order_by("-created_at")
        summary = transactions.aggregate(
            total_income=Sum("amount", filter=Q(type="RE")),
            total_expense=Sum("amount", filter=Q(type="EX")),
        )
        if summary["total_income"]== None:
            summary["total_income"]=0
        if summary["total_expense"]== None:
            summary["total_expense"]=0
        summary = summary["total_income"] - summary["total_expense"]
        if summary<0 :
            summary = summary

        paginator = Paginator(transactions, 2)  # ۲۰ تراکنش در هر صفحه
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "home/accoount_transactions.html",
            {"transactions": page_obj, "account": account, "summary": summary},
        )


class RegisterTransactionsView(View):
    form_class = TransactionForm

    def get(self, request, account_pk, transaction_type):
        form = self.form_class()
        account = get_object_or_404(Account, pk=account_pk)
        print(account.full_name)
        if transaction_type == "re":
            transaction_type = "درآمد"

        if transaction_type == "ex":
            transaction_type = "هزینه"

        return render(
            request,
            "home/register_transaction.html",
            {
                "form": form,
                "account": account,
                "transaction_type": transaction_type,
            },
        )

    def post(self, request, account_pk, transaction_type):
        form = self.form_class(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            account = get_object_or_404(Account, id=account_pk)
            transaction.user = request.user
            transaction.account = account
            if transaction_type == "re":
                transaction.type = "RE"
            elif transaction_type == "ex":
                transaction.type = "EX"
            else:
                messages.warning(request, "نوع تراکنش مشخص نیست!", "warning")
                return redirect("home:transactions")
            messages.success(request, "تراکنش با موفقیت ثب شد.", "success")
            transaction.save()
            return redirect("home:accounttransactions", account.id)


class RetrieveTransactionsView(View):
    pass


class DeleteTransactionsView(View):
    pass


class UpdateTransactionsView(View):
    pass
