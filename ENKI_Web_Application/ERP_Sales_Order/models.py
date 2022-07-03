from django.db import models
from ERP_Company_Overview.models import Client_Directory, Parent_Company_Information, Child_Company_Information, Company_Permissions
from ERP_Inventory.models import Manufacture, Product_Library, Inventory, Price_List
from django.urls import reverse


class Sales_Order(models.Model):
    order_id_no         = models.AutoField(primary_key=True)
    client_name         = models.ForeignKey(Client_Directory, on_delete=models.PROTECT, null=True, blank=True)
    sales_reference     = models.CharField(max_length=200)
    order_location      = models.ForeignKey(Child_Company_Information, on_delete=models.PROTECT, null=True, blank=True)
    order_status        = models.BooleanField(default=False)
    order_creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)


    def __str__(self):
        return str("SO " + str(self.order_id_no))


class Sales_Order_Detail(models.Model):
    order_id_no         = models.ForeignKey(Sales_Order, on_delete=models.CASCADE, null=True, blank=True)
    product_code        = models.ForeignKey(Product_Library, on_delete=models.PROTECT, null=True, blank=True)
    quantity            = models.IntegerField(default=0, null=True, blank=True)
    item_added_date     = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.order_id_no)
