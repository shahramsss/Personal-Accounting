from django.db import models
from django.contrib.auth import get_user_model

class Account(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    user = models.ForeignKey(get_user_model() , on_delete=models.DO_NOTHING, related_name="transactions")

    

    def __str__(self):
        return self.full_name



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("RE", "دریافت"),
        ("EX", "پرداخت"),
    ]

    account = models.ForeignKey(
        "Account", on_delete=models.PROTECT, related_name="transactions"
    )
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=0)
    category = models.CharField(max_length=100)  
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sign = "+" if self.type == "RE" else "-"
        return f"{self.account.user} | {self.account} | {sign}  {self.amount}"
    
    # @property
    # def balance(self):
    #     # جمع دریافتی‌ها
    #     received = self.transactions.filter(type="RE").aggregate(models.Sum("amount"))["amount__sum"] or 0
    #     # جمع پرداختی‌ها
    #     paid = self.transactions.filter(type="EX").aggregate(models.Sum("amount"))["amount__sum"] or 0
    #     # موجودی = دریافتی - پرداختی
    #     return received - paid


class Product(models.Model):
    user = models.ForeignKey(get_user_model() , on_delete=models.DO_NOTHING, related_name="user")
    name = models.CharField(max_length=256)
    unit = models.IntegerField(max_length=20, default=0)  # واحد اندازه‌گیری (عدد، کیلوگرم، متر و ...)
    price = models.DecimalField(max_digits=15, decimal_places=0)  # قیمت واحد
    purchaseprice = models.DecimalField(max_digits=15, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ({self.sku})"

# class factor(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='inventories')
#     quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ('product', 'warehouse')  # هر کالا در هر انبار فقط یک رکورد موجودی

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} در {self.warehouse.name}"
