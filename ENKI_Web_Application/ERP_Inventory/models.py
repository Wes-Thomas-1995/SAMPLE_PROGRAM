from django.db import models
from django.contrib.auth.models import User
import uuid
from ERP_Company_Overview.models import Client_Directory, Parent_Company_Information, Child_Company_Information, Company_Permissions


class Manufacture(models.Model):
    manufacturer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.manufacturer


class Product_Library(models.Model):
    product_code            = models.CharField(max_length=200)
    categorisation          = models.CharField(max_length=200)
    product_type            = models.CharField(max_length=200)
    manufacturer            = models.ForeignKey(Manufacture, on_delete=models.DO_NOTHING, null=True, blank=True)
    cost_price              = models.DecimalField(max_digits=10, decimal_places=2)
    description             = models.CharField(max_length=200)
    price_creation_date     = models.DateTimeField(auto_now_add=True, auto_now=False)
    price_update_date       = models.DateTimeField(auto_now_add=False, auto_now=True, null=True, blank=True)


    def __str__(self):
        return self.product_code


class Inventory(models.Model):
    product_code            = models.ForeignKey(Product_Library, on_delete=models.DO_NOTHING, null=True, blank=True)
    quantity                = models.IntegerField(default=0, null=True, blank=True)
    inventory_location      = models.ForeignKey(Child_Company_Information, on_delete=models.DO_NOTHING, null=True, blank=True)


    def __str__(self):
        return self.product_code.product_code



class Price_List(models.Model):
    client_name = models.ForeignKey(Client_Directory, on_delete=models.DO_NOTHING, null=True, blank=True)
    product_code = models.ForeignKey(Product_Library, on_delete=models.DO_NOTHING, null=True, blank=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_creation_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    price_update_date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)


    def sales_margin(self):
        return format((((self.sales_price / self.product_code.cost_price)-1)*100),'.0f')


    def __str__(self):
        return self.client_name.client_name
