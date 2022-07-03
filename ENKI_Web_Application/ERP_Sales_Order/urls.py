from . import views
from django.urls import path

urlpatterns = [

    path('SALES-ORDER/', views.sales_order_AJAX_TRIAL, name="sales-order-create"),
    path('SALES-ORDER/sales-order/search/', views.search_AJAX_TRIAL, name='sales-order-search'),

    path('sales-order/create/', views.create_sales_order, name="create_sales_order"),
    path('sales-order/list/', views.sales_order_distinct_table, name="all_sales_orders"),
    path('ind_salesorder/<str:pk>/', views.ind_salesorder, name="ind_salesorder")

    ]