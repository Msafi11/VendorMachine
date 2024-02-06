from django.contrib import admin
from api.models import CustomUser, Buyer, Seller, Product

admin.site.register(CustomUser)
admin.site.register(Buyer)
admin.site.register(Seller)
admin.site.register(Product)
