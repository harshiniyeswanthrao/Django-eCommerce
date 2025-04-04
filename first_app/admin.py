from django.contrib import admin
from .models import Product, Order, OrderItem, Product_detail

admin.site.register(Product)
admin.site.register(Product_detail)
admin.site.register(Order)
admin.site.register(OrderItem)




