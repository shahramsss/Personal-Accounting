from django.db import models
from django.contrib.auth import get_user_model

class Account(models.Model):
    full_name = models.CharField(max_length=128)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=512, null=True, blank=True)
    

    def __str__(self):
        return self.full_name



class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("RE", "درآمد"),
        ("EX", "هزینه"),
    ]

    user = models.ForeignKey(get_user_model() , on_delete=models.DO_NOTHING, related_name="transactions")
    account = models.ForeignKey(
        "Account", on_delete=models.DO_NOTHING, related_name="transactions"
    )
    type = models.CharField(max_length=2, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    category = models.CharField(max_length=100)  # منبع درآمد یا دسته‌بندی هزینه
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        sign = "+" if self.type == "RE" else "-"
        return f"{sign}{self.amount} تومان - {self.category}"


# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     sku = models.CharField(max_length=50, unique=True)  # کد کالا یا شناسه
#     description = models.TextField(blank=True, null=True)
#     unit = models.CharField(max_length=20, default="عدد")  # واحد اندازه‌گیری (عدد، کیلوگرم، متر و ...)
#     price = models.DecimalField(max_digits=15, decimal_places=2)  # قیمت واحد
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.name} ({self.sku})"

# class Inventory(models.Model):
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='inventories')
#     warehouse = models.ForeignKey('Warehouse', on_delete=models.CASCADE, related_name='inventories')
#     quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     last_updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ('product', 'warehouse')  # هر کالا در هر انبار فقط یک رکورد موجودی

#     def __str__(self):
#         return f"{self.product.name} - {self.quantity} در {self.warehouse.name}"
