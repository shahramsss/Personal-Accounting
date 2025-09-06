"""
URL configuration for Accounting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),
    path("accounts/", views.AccountsView.as_view(), name="accounts"),
    path("accountregister/", views.AccountRegisterView.as_view(), name="accountregister"),
    path("deleteaccount/<int:pk>/", views.DeleteAccountView.as_view(), name="deleteaccount"),
    path("editaccount/<int:pk>/", views.EditAccountView.as_view(), name="editaccount"),
    path("account/<int:pk>/", views.SelectAccountView.as_view(), name="account"),
    # transaction
    path("transactions/", views.TransactionsView.as_view(), name="transactions"),
    path("accounttransactions/<int:account_pk>/", views.AccountTransactionsView.as_view(), name="accounttransactions"),
    path("registertransaction/<int:account_pk>/<str:transaction_type>/", views.RegisterTransactionsView.as_view(), name="registertransaction"),
    path("deletetransaction/<int:account_pk>/<int:pk>/", views.DeleteTransactionsView.as_view(), name="deletetransaction"),
    path("updatetransaction/<int:account_pk>/<int:pk>/", views.UpdateTransactionsView.as_view(), name="updatetransaction"),
]
