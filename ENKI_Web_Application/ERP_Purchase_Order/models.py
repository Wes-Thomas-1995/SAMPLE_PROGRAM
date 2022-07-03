from django.db import models
from ERP_Company_Overview.models import Client_Directory, Parent_Company_Information, Child_Company_Information, Company_Permissions
from ERP_Inventory.models import Manufacture, Product_Library, Inventory, Price_List
from django.urls import reverse


class Purchase_Order(models.Model):
    order_id_no         = models.AutoField(primary_key=True)
    manufacturer        = models.ForeignKey(Manufacture, on_delete=models.PROTECT, null=True, blank=True)
    order_location      = models.ForeignKey(Child_Company_Information, on_delete=models.PROTECT, null=True, blank=True)
    order_status        = models.BooleanField(default=False)
    order_creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('purchase_order_form', kwargs={'pk': self.pk})

    def __str__(self):
        return str("PO " + str(self.order_id_no))


class Purchase_Order_Detail(models.Model):
    order_id_no         = models.ForeignKey(Purchase_Order, on_delete=models.CASCADE, null=True, blank=True)
    product_code        = models.ForeignKey(Product_Library, on_delete=models.CASCADE, null=True, blank=True)
    quantity            = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.order_id_no)

