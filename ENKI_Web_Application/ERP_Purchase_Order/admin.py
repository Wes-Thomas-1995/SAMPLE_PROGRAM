from django.contrib import admin
from .models import Purchase_Order, Purchase_Order_Detail


admin.site.register(Purchase_Order)
admin.site.register(Purchase_Order_Detail)

