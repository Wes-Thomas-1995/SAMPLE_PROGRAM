import csv
import io
import datetime
import xlwt
from django.contrib import messages
from django.db.models import Sum, ExpressionWrapper, F, DecimalField, Case, When
from django.http import HttpResponse
from django.shortcuts import render
from .models import Inventory, Product_Library, Manufacture, Price_List
from ERP_Company_Overview.models import Client_Directory, Parent_Company_Information, Child_Company_Information, Company_Permissions


#Inventory related views
def inventory_specific(request, pk):
    location = Child_Company_Information.objects.values('company_location', 'child_company_id').filter(child_company_id__exact=pk)[0]
    droplist = Child_Company_Information.objects.values('company_location', 'child_company_id')
    inventory = Inventory.objects.values('product_code__product_code', 'product_code__categorisation', 'product_code__manufacturer__manufacturer', 'product_code__product_type', 'product_code__description', 'quantity', 'inventory_location__company_location', 'inventory_location__child_company_id').filter(inventory_location__child_company_id__exact=pk).annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00))))
    context = {'droplist':droplist, 'inventory':inventory, 'location': location}
    return render(request, 'inventory/inventory-specific.html', context)


def inventory(request):
    location = "All Locations"
    droplist = Child_Company_Information.objects.values('company_location', 'child_company_id')
    inventory = Inventory.objects.values('product_code__product_code').distinct().annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00))), product_code__categorisation=F('product_code__categorisation'), product_code__manufacturer__manufacturer=F('product_code__manufacturer__manufacturer'), product_code__product_type=F('product_code__product_type'), product_code__description=F('product_code__description'))
    context = {'droplist': droplist, 'inventory':inventory, 'location':location}
    return render(request, 'Inventory/inventory.html', context)


def product_library(request):
    product_library = Product_Library.objects.all().values('product_code', 'categorisation', 'product_type', 'manufacturer__manufacturer', 'description')
    context = {'product_library': product_library}
    return render(request, 'product-library/product-library.html', context)


def stock_export(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Inventory - ' + str(datetime.date.today()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Inventory')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['Product Code', 'Product Category', 'Product Type', 'Product Manufacturer', 'Cost Price',
               'General Sales Price', 'Account Sales Price', 'Product Description', 'Quantity']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Inventory.objects.all().values_list('product_code', 'categorisation', 'product_type', 'manufacturer',
                                               'cost_price', 'general_sales_price', 'account_sales_price',
                                               'description', 'quantity')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response


def stock_upload(request):
    template = 'inventory/stock-upload.html'

    if request.method == 'GET':
        return render(request, template)

    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file. Please re-save file as such.')

    dataset = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(dataset)
    next(io_string)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Inventory.objects.update_or_create(
            product_code=column[0],
            categorisation=column[1],
            product_type=column[2],
            manufacturer=column[3],
            cost_price=column[4],
            general_sales_price=column[5],
            account_sales_price=column[6],
            description=column[7],
            quantity=column[8], )

    context = {}
    return render(request, template, context)





