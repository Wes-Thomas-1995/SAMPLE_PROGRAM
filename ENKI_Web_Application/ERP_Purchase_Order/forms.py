from django import forms
from django.forms import inlineformset_factory, ModelForm
from .models import Purchase_Order, Purchase_Order_Detail
from ERP_Inventory.models import Manufacture, Product_Library, Inventory, Price_List

class ProfileForm(ModelForm):
    class Meta:
        model = Purchase_Order
        exclude = ()

class PurchaseOrderForm(ModelForm):
    class Meta:
        model = Purchase_Order_Detail
        exclude = ()


PurchaseOrderFormset = inlineformset_factory(Purchase_Order, Purchase_Order_Detail, form=PurchaseOrderForm, extra=2)


