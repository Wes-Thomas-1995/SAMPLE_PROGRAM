from django.shortcuts import render, redirect
from ERP_Company_Overview.models import Client_Directory, Parent_Company_Information, Child_Company_Information, Company_Permissions
from ERP_Inventory.models import Manufacture, Product_Library, Inventory, Price_List
from .models import Sales_Order, Sales_Order_Detail
from django.db.models import Sum, ExpressionWrapper, F, DecimalField, Case, When, Value




def sales_order_AJAX_TRIAL(request):
    location = "All Locations"
    droplist = Child_Company_Information.objects.values('company_location', 'child_company_id')
    sales_order = Inventory.objects.values('product_code__product_code', 'product_code__categorisation', 'product_code__manufacturer__manufacturer', 'product_code__product_type', 'product_code__description', 'quantity').distinct().annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00))))
    context = {'droplist': droplist, 'inventory':sales_order, 'location':location}
    return render(request, 'sales-order/sales-order-template-AJAX-TRIAL.html', context)


def search_AJAX_TRIAL(request):

    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''


    print(search_text)
    sales_order = Inventory.objects.values('product_code__product_code').distinct().annotate(
        total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00))),
        product_code__categorisation=F('product_code__categorisation'),
        product_code__manufacturer__manufacturer=F('product_code__manufacturer__manufacturer'),
        product_code__product_type=F('product_code__product_type'),
        product_code__description=F('product_code__description')).filter(product_code__product_code__contains=search_text)
    context ={'sales_order': sales_order}
    return render(request,'sales-order/ajax_search1.html', context)






def create_sales_order(request):
    A = "East Grinstead"

    sales_order = Inventory.objects.values('product_code__product_code').annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00))),product_code__manufacturer__manufacturer = F('product_code__manufacturer__manufacturer'),product_code__description = F('product_code__description'))
    local_sales_order = Inventory.objects.values('product_code__product_code').annotate(local_total=Case(When(inventory_location__company_location__exact=A, then=F('quantity'))),product_code__manufacturer__manufacturer = F('product_code__manufacturer__manufacturer'),product_code__description = F('product_code__description')).exclude(local_total__isnull=True)
    context = {'sales_order': sales_order, 'local_sales_order': local_sales_order}



    if request.method == 'POST':
        client_name     =request.POST['subject']


        so_no = Sales_Order.objects.create(
                client_name         = Client_Directory.objects.get(client_name=request.POST['subject']),
                order_location      = Child_Company_Information.objects.get(company_location='Haywards Heath'),
                sales_reference     =request.POST['email'],                                                           #find a way to pull the location of the logged in user for retrieving the sales location
                order_status        = True
                )

        so_no.save()
        tosave = request.POST.getlist('sendtoseller')

        for sel in tosave:
            sod_no = Sales_Order_Detail.objects.create(
                product_code    = Product_Library.objects.get(product_code=sel),
                order_id_no     = Sales_Order.objects.get(order_id_no=so_no.order_id_no),
                quantity        = request.POST['order_qty_' + sel])



        return redirect('home-page')
    else:
        return render(request, 'sales-order/create-sales-order.html', context)


def ind_salesorder(request, pk):
    salesorderObj = Sales_Order_Detail.objects.all().filter(order_id_no=pk).values('product_code__description', 'product_code__product_code', 'item_added_date', 'quantity', 'order_id_no__client_name__client_name')
    order_id_dis = Sales_Order_Detail.objects.all().values('order_id_no__client_name__client_name', 'order_id_no__order_id_no').filter(order_id_no=pk)[0]

    price_list = Price_List.objects.all().values('product_code__product_code', 'client_name__client_name', 'sales_price').exclude(price_update_date__isnull=False)

    #saleso = salesorderObj.union(price_list)

    tsp = 0
    #for i in salesorderObj[:]:
        #tsp = tsp + i['total_price']


    context = {'ind_salesorder': salesorderObj, 'order_id_dis': order_id_dis, 'tsp': tsp, 'price_list': price_list}
    return render(request, 'sales-order/individual-sales-order.html', context)




def sales_order_distinct_table(request):
    distinct_salesorder = Sales_Order_Detail.objects.all().values('order_id_no', 'order_id_no__client_name__client_name', 'order_id_no__order_location__company_location', 'order_id_no__sales_reference').distinct().annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00)))).order_by('-order_id_no')
    context = {'distinct_salesorder':distinct_salesorder}
    VAT = 20
    return render(request, 'sales-order/distinct-sales-order.html', context)
