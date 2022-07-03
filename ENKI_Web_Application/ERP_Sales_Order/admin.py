from django.contrib import admin
from .models import Sales_Order, Sales_Order_Detail


admin.site.register(Sales_Order)
admin.site.register(Sales_Order_Detail)

