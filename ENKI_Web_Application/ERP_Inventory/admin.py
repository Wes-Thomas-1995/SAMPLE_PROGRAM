from django.contrib import admin
from .models import  Inventory, Price_List, Product_Library, Manufacture

# Register your models here.

admin.site.register(Inventory)
admin.site.register(Price_List)
admin.site.register(Product_Library)
admin.site.register(Manufacture)