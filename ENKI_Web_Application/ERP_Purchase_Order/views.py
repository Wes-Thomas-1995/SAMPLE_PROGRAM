import csv
import io
import datetime
import xlwt
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect
from .models import Purchase_Order, Purchase_Order_Detail
from .forms import PurchaseOrderForm, PurchaseOrderFormset, ProfileForm
from django.db.models import Sum, ExpressionWrapper, F, DecimalField, Case, When
from django.forms import modelformset_factory
from django.shortcuts import render, get_object_or_404
from django.views.generic import UpdateView, ListView, CreateView
from django.urls import reverse, reverse_lazy
from ERP_Inventory.models import Manufacture, Product_Library, Inventory, Price_List


#Purchase Order related views
def ind_purchaseorder(request, pk):
    purchaseorderObj = Purchase_Order_Detail.objects.all().filter(order_id_no__order_id_no=pk).annotate(total_price=Sum(ExpressionWrapper(Case(When(product_code__price_update_date__isnull=False,  then=F('product_code__cost_price'))) * F('quantity'), output_field=DecimalField(0.00))), cost_price=Sum(ExpressionWrapper(Case(When(product_code__price_update_date__isnull=False,  then=F('product_code__cost_price'))), output_field=DecimalField(0.00)))).values('product_code__description', 'product_code__product_code', 'order_id_no__order_status', 'quantity', 'total_price', 'cost_price')
    order_id_dis = Purchase_Order_Detail.objects.all().values('product_code__description', 'order_id_no__manufacturer__manufacturer', 'order_id_no__order_id_no', 'product_code__product_code', 'order_id_no__order_status', 'quantity', 'product_code__cost_price',).filter(order_id_no__order_id_no=pk)[0]

    tsp = 0
    for i in purchaseorderObj[:]:
        tsp = tsp + i['total_price']

    context = {'ind_purchaseorder': purchaseorderObj, 'order_id_dis': order_id_dis, 'tsp': tsp}
    return render(request, 'purchase-order/individual-purchase-order.html', context)


def purchase_order_distinct_table(request):
    distinct_purchaseorder = Purchase_Order_Detail.objects.all().values('order_id_no','product_code__manufacturer__manufacturer','order_id_no__order_status', 'order_id_no__order_location__company_location').distinct().annotate(total=Sum(ExpressionWrapper(Case(When(product_code__price_update_date__isnull=False,  then=F('product_code__cost_price'))) * F('quantity'), output_field=DecimalField(0.00)))).order_by('-order_id_no')
    context = {'distinct_purchaseorder':distinct_purchaseorder}
    return render(request, 'purchase-order/distinct-purchase-order.html', context)





#EXAMPLE OF HOW TO TAKE FORWARDS
#Look into JS and AJAX filtering based on conditions without refreshing - https://simpleisbetterthancomplex.com/tutorial/2018/01/29/how-to-implement-dependent-or-chained-dropdown-list-with-django.html


class Purchase_Order_List(ListView):
    model = Purchase_Order


class PurchaseOrderCreate(CreateView):
    model = Purchase_Order
    fields = ['manufacturer', 'order_location']


class Purchase_Order_Detail_Create(CreateView):
    model = Purchase_Order
    fields = ['manufacturer', 'order_location']
    success_url = reverse_lazy('distinct_purchaseorder')
    template_name = 'purchase-order/purchase_order_form.html'


    def get_context_data(self, **kwargs):
        data = super(Purchase_Order_Detail_Create, self).get_context_data(**kwargs)
        product_code_query = Product_Library.objects.all().values('product_code', 'manufacturer__manufacturer').filter(manufacturer__manufacturer=self.object)

        if self.request.POST:
            data['purchaseorderdetail'] = PurchaseOrderFormset(self.request.POST, instance=self.object)
            #for form in data['purchaseorderdetail']:
                #form.fields['product_code'].queryset = product_code_query
        else:
            data['purchaseorderdetail'] = PurchaseOrderFormset(instance=self.object)
            #for form in data['purchaseorderdetail']:
                #form.fields['product_code'].queryset = product_code_query
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        purchaseorderdetail = context['purchaseorderdetail']
        with transaction.atomic():
            self.object = form.save()

            if purchaseorderdetail.is_valid():
                purchaseorderdetail.instance = self.object
                purchaseorderdetail.save()


        return super(Purchase_Order_Detail_Create, self).form_valid(form)






