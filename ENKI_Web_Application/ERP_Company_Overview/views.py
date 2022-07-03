
from django.shortcuts import render, HttpResponse, redirect
from .models import Client_Directory, Child_Company_Information, Parent_Company_Information, Company_Permissions
from ERP_Inventory.models import Price_List, Inventory, Manufacture, Product_Library
from django.db.models import Sum, ExpressionWrapper, F, DecimalField, Case, When
from xlrd import open_workbook
from xlutils.copy import copy
import os
from django.shortcuts import redirect
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError
from ERP_Sales_Order.models import Sales_Order_Detail


def client_directory_overview(request):
    A = 'Haywards Heath'
    local_client_details = Client_Directory.objects.all().values('client_id', 'client_name', 'client_email', 'client_telephone', 'point_of_contact_first', 'point_of_contact_last', 'child_company_name__company_location').filter(account_status=True, child_company_name__company_location__exact=A)
    other_client_details = Client_Directory.objects.all().values('client_id', 'client_name', 'client_email', 'client_telephone', 'point_of_contact_first', 'point_of_contact_last', 'child_company_name__company_location').filter(account_status=True).exclude(child_company_name__company_location__exact=A)
    context = {'local_client_details': local_client_details, 'other_client_details': other_client_details, 'A': A}
    return render(request, 'company-overview/client_directory.html', context)


def individual_client_profile(request, pk):
    clientObj = Client_Directory.objects.all().filter(client_id=pk)
    client_id_dis = Client_Directory.objects.all().filter(client_id=pk)[0]
    distinct_salesorder = Sales_Order_Detail.objects.all().values('order_id_no', 'order_id_no__client_name__client_name', 'order_id_no__order_location__company_location', 'order_id_no__sales_reference', 'order_id_no__order_creation_date').filter(order_id_no__client_name__client_id=pk).distinct().annotate(total=Sum(ExpressionWrapper(F('quantity'), output_field=DecimalField(0.00)))).order_by('-order_id_no')

    context = {'clientObj': clientObj, 'client_id_dis': client_id_dis, 'distinct_salesorder':distinct_salesorder}
    return render(request, 'company-overview/individual_client_profile.html', context)



def client_price_list(request):
    client_details = Client_Directory.objects.all().values('client_id', 'client_name', 'client_email', 'client_telephone', 'point_of_contact_first', 'point_of_contact_last').filter(account_status=True)
    context = {'client_details': client_details}
    return render(request, 'company-overview/price_list.html', context)


def individual_client_price_list(request, pk):
    priceObj = Price_List.objects.all().filter(client_name__client_id=pk).annotate(sales_margin=Sum(ExpressionWrapper(((F('sales_price') - F('product_code__cost_price')) / F('product_code__cost_price'))*100, output_field=DecimalField(0.00))))
    price_id_dis = Price_List.objects.all().filter(client_name__client_id=pk)[0]
    context = {'priceObj': priceObj, 'price_id_dis': price_id_dis}
    return render(request, 'company-overview/client_price_list.html', context)


def login(request):
    return render(request, 'login/login_page.html')


def create_account(request):
    if request.method == "POST":

        Parent_Company_Information.objects.update_or_create(
            parent_company_name=request.POST['parent_name'],
        )


        #Child_Company_Information.objects.update_or_create(
            #parent_company_name = Parent_Company_Information.objects.get(parent_company_name=request.POST['parent_name']),
            #child_company_name = request.POST['child_name'],
            #company_location = request.POST['child_location'],
        #)

        #Company_Permissions.objects.update_or_create(
            #username = request.POST['username'],
            #password = request.POST['password'],
            #user_email = request.POST['email'],
            #permission_level = request.POST['permission_level'],
            #user_first_name=request.POST['first_name'],
            #user_last_name=request.POST['last_name'],
            #parent_company_name=Parent_Company_Information.objects.get(parent_company_name=request.POST['parent_name']),
        #)








        try:
            excel_file = request.FILES['file']
        except MultiValueDictKeyError:
            return redirect('login')

        if str(excel_file).split('.')[-1] == "xls":
            data = xls_get(excel_file)
        elif str(excel_file).split('.')[-1] == "xlsx":
            data = xlsx_get(excel_file)
        else:
            return redirect('inventory')


        child_company_information   = data["Child Company Information"]
        company_permissions         = data["Company Permissions"]
        client_directory            = data["Client Directory"]
        manufacture                 = data["Manufacture"]
        product_library             = data["Product Library"]
        inventory                   = data["Inventory"]
        price_list                  = data["Price List"]


        # ---- Child Company Information Upload ---- #
        if len(child_company_information) > 1:  # We have company data
            for company in child_company_information:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Child Company Name":  # This is not header
                        if company[0] != '':

                            Child_Company_Information.objects.create(
                                parent_company_name =Parent_Company_Information.objects.get(parent_company_name=request.POST['parent_name']),
                                child_company_name  =company[0],
                                company_location    =company[1]
                            )
                        else:
                            pass

        # ---- Company Permissions Upload ---- #
        if len(company_permissions) > 1:  # We have company data
            for company in company_permissions:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "User Name":  # This is not header
                        if company[0] != '':

                            Company_Permissions.objects.create(
                                username            =company[0],
                                password            =company[1],
                                permission_level    =int(company[2]),
                                user_first_name     =company[3],
                                user_last_name      =company[4],
                                user_email          =company[5],
                                parent_company_name =Parent_Company_Information.objects.get(parent_company_name=request.POST['parent_name'])
                            )
                        else:
                            pass


        # ---- Client Directory Upload ---- #
        if len(client_directory) > 1:  # We have company data
            for company in client_directory:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Client Name":  # This is not header
                        if company[0] != '':

                            Client_Directory.objects.create(
                                client_name             =company[0],
                                client_email            =company[1],
                                client_telephone        =company[2],
                                client_address          =company[3],
                                client_postcode         =company[4],
                                point_of_contact_first  =company[5],
                                point_of_contact_last   =company[6],
                                account_status          =company[7],
                                child_company_name      =Child_Company_Information.objects.get(child_company_name=company[8]),
                            )
                        else:
                            pass


        # ---- Manufacture Upload ---- #
        if len(manufacture) > 1:  # We have company data
            for company in manufacture:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Manufacture":  # This is not header
                        if company[0] != '':

                            Manufacture.objects.create(
                                manufacturer            =company[0],
                            )
                        else:
                            pass


        # ---- Product Library Upload ---- #
        if len(product_library) > 1:  # We have company data
            for company in product_library:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Product Code":  # This is not header
                        if company[0] != '':

                            Product_Library.objects.create(
                                product_code        =company[0],
                                categorisation      =company[1],
                                product_type        =company[2],
                                manufacturer        =Manufacture.objects.get(manufacturer=company[3]),
                                cost_price          =company[4],
                                description         =company[5],
                            )
                        else:
                            pass


        # ---- Inventory Upload ---- #
        if len(inventory) > 1:  # We have company data
            for company in inventory:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Product Code":  # This is not header
                        if company[0] != '':

                            Inventory.objects.create(
                                product_code            =Product_Library.objects.get(product_code=company[0]),
                                quantity                =int(company[1]),
                                inventory_location      =Child_Company_Information.objects.get(company_location=company[2]),
                            )
                        else:
                            pass


        # ---- Price List Upload ---- #
        if len(price_list) > 1:  # We have company data
            for company in price_list:
                if len(company) > 0:  # The row is not blank
                    if company[0] != "Client Name":  # This is not header
                        if company[0] != '':

                            Price_List.objects.create(
                                client_name            =Client_Directory.objects.get(client_name=company[0]),
                                product_code           =Product_Library.objects.get(product_code=company[1]),
                                sales_price            =float(company[2]),
                            )
                        else:
                            pass



        return redirect('home-page')
    else:
        return render(request, 'login/create_account.html')




def export_excel_template(request):

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Company data package template.xls"'


    path = os.path.dirname(__file__)
    file = os.path.join(path, 'templates/excel-template/Company data package template.xls')
    rb = open_workbook(file, formatting_info=True)
    wb = copy(rb)
    wb.save(file)
    wb.save(response)


    return response


