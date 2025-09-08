from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Account, Transaction
from .forms import (
    AccountForm,
    TransactionForm,
    SignUpForm,
    LoginForm,
    ResetPasswordForm,
)
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


class HomeView(View):
    def get(self, request):
        return render(
            request,
            "home/home.html",
        )


class AccountsView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "")
        accounts = Account.objects.filter(user=request.user).order_by("-id")

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


class AccountRegisterView(LoginRequiredMixin, View):
    form_class = AccountForm

    def get(self, request):
        form = self.form_class
        return render(request, "home/account_register.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, "حساب جدید ثبت شد.", "success")
            return redirect("home:accounts")
        return render(request, "home/account_register.html", {"form": form})


class DeleteAccountView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, user=request.user, pk=pk)
        transactions = Transaction.objects.filter(account=account)
        if transactions.exists():
            messages.warning(
                request,
                "باید همه تراکنش های حساب "
                + account.full_name
                + " حذف شوند تا امکان حذف وجود داشته باشد!",
                "warning",
            )
            return redirect("home:accounts")

        return render(request, "home/delete_confirm.html", {"account": account})

    def post(self, request, pk):
        account = get_object_or_404(Account, user=request.user, pk=pk)
        account.delete()
        return redirect("home:accounts")


class EditAccountView(LoginRequiredMixin, View):
    def get(self, request, pk):
        account = get_object_or_404(Account, user=request.user, pk=pk)
        form = AccountForm(instance=account)
        return render(
            request, "home/edit_account.html", {"form": form, "account": account}
        )

    def post(self, request, pk):
        account = get_object_or_404(Account, user=request.user, pk=pk)
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.warning(request, "حساب با موفقیت ویرایش شد.", "warning")
            return redirect("home:accounts")
        # یا هر صفحه‌ای که لیست حساب‌ها رو نشون می‌ده
        return render(
            request, "home/edit_account.html", {"form": form, "account": account}
        )


class SelectAccountView(LoginRequiredMixin, View):
    form_class = TransactionForm

    def get(self, request, pk):
        account = get_object_or_404(Account, user=request.user, id=pk)
        form = self.form_class
        return render(
            request,
            "home/select_account.html",
            {
                "form": form,
                "account": account,
            },
        )


class TransactionsView(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("q", "")
        transactions = Transaction.objects.filter(account__user=request.user)
        if query:
            transactions = transactions.filter(description__icontains=query)

        transactions = transactions.order_by("-created_at")  # اختیاری
        paginator = Paginator(transactions, 20)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "transactions": page_obj,
            "query": query,
        }
        return render(request, "home/transactions.html", context)


class AccountTransactionsView(LoginRequiredMixin, View):
    def get(self, request, account_pk):
        account = get_object_or_404(Account, user=request.user, id=account_pk)
        transactions = account.transactions.all().order_by("-created_at")
        summary = transactions.aggregate(
            total_income=Sum("amount", filter=Q(type="RE")),
            total_expense=Sum("amount", filter=Q(type="EX")),
        )
        if summary["total_income"] == None:
            summary["total_income"] = 0
        if summary["total_expense"] == None:
            summary["total_expense"] = 0
        summary = summary["total_income"] - summary["total_expense"]
        if summary < 0:
            summary = summary

        paginator = Paginator(transactions, 20)  # ۲۰ تراکنش در هر صفحه
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "home/accoount_transactions.html",
            {"transactions": page_obj, "account": account, "summary": summary},
        )


class RegisterTransactionsView(LoginRequiredMixin, View):
    form_class = TransactionForm

    def get(self, request, account_pk, transaction_type):
        form = self.form_class()
        account = get_object_or_404(Account, user=request.user, pk=account_pk)
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
            account = get_object_or_404(Account, user=request.user, id=account_pk)
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


class DeleteTransactionsView(LoginRequiredMixin, View):
    def get(self, request, account_pk, pk):
        account = get_object_or_404(Account, user=request.user, id=account_pk)
        transaction = get_object_or_404(Transaction, id=pk)
        if transaction.account.user == request.user and transaction.account == account:
            return render(
                request,
                "home/delete_confirm_transaction.html",
                {"transaction": transaction, "account": account},
            )
        else:
            messages.warning(request, "این تراکنش مربوط به شما نمی باشد!", "warning")
        return redirect("home:accounttransactions", account.id)

    def post(self, request, account_pk, pk):
        account = get_object_or_404(Account, user=request.user, id=account_pk)
        transaction = get_object_or_404(Transaction, id=pk)
        if transaction.account.user == request.user and transaction.account == account:
            transaction.delete()
            messages.success(request, "تراکنش با موفقیت حذف شد.", "success")
        else:
            messages.warning(request, "این تراکنش مربوط به شما نمی باشد!", "warning")
        return redirect("home:accounttransactions", account.id)


class UpdateTransactionsView(LoginRequiredMixin, View):
    form_class = TransactionForm

    def get(self, request, account_pk, pk):
        account = get_object_or_404(Account, user=request.user, id=account_pk)
        transaction = get_object_or_404(Transaction, id=pk)
        form = self.form_class(instance=transaction)
        return render(
            request,
            "home/update_transaction.html",
            {"transaction": transaction, "account": account, "form": form},
        )

    def post(self, request, account_pk, pk):
        account = get_object_or_404(Account, user=request.user, id=account_pk)
        transaction = get_object_or_404(Transaction, id=pk)
        form = self.form_class(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "تراکنش با موفقیت ویرایش شد.", "success")
        return redirect("home:accounttransactions", account.id)
       


class SignupView(View):
    form_class = SignUpForm
    template = "home/signup_user.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "شما با موفقیت وارد شدید.", "success")
            return redirect("home:home")
        return render(request, self.template, {"form": form})


class LoginView(View):
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            messages.warning(request, "شما قبلاً وارد شده‌اید!")
            return redirect("home:home")
        form = self.form_class()
        next_url = request.GET.get("next", "")
        return render(request, "home/login_user.html", {"form": form, "next": next_url})

    def post(self, request):
        form = self.form_class(request.POST)
        next_url = request.GET.get("next", "") or request.POST.get("next", "")
        if form.is_valid():
            cd = form.cleaned_data
            username = cd["username"]
            password = cd["password"]
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.warning(request, "نام کاربری یا رمز عبور اشتباه است!")
                return redirect("home:login")
            login(request, user)
            messages.success(request, "شما با موفقیت وارد شدید.")
            return redirect(next_url or "home:home")
        return render(request, "home/login_user.html", {"form": form, "next": next_url})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "شما با موفقیت خارج شدید.", "success")
        return redirect("home:home")


class ResetPassword(LoginRequiredMixin, View):
    form_class = ResetPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, "home/reset_password.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            old_password = cd["old_password"]
            new_password = cd["new_password"]
            confirm_password = cd["confirm_password"]

            if not request.user.check_password(old_password):
                messages.warning(request, "رمز عبور فعلی اشتباه است!", "warning")
                return redirect("home:resetpassword")

            if len(new_password) < 4:
                messages.warning(
                    request, "رمز عبور جدید باید حداقل ۴ کاراکتر باشد!", "warning"
                )
                return redirect("home:resetpassword")

            if new_password != confirm_password:
                messages.warning(
                    request, "رمز عبور و تکرار آن باید با هم یکسان باشند!", "warning"
                )
                return redirect("home:resetpassword")

            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, "رمز عبور شما با موفقیت تغییر یافت.", "success")
            return redirect("home:login")

        return render(request, "home/reset_password.html", {"form": form})
