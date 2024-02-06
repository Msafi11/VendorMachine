from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class CustomUser(AbstractUser):
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    role = models.CharField(max_length=10, choices=[('buyer', 'buyer'), ('seller', 'seller')], null=False, blank=False)

class Seller(models.Model):
    custom_user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Buyer(models.Model):
    custom_user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    total_spendings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Product(models.Model):
    amount_available = models.IntegerField(default=0)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    product_name = models.CharField(max_length=100)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='products')