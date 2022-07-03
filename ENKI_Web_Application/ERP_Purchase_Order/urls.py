from . import views
from django.urls import path

urlpatterns = [

    path('distinct-purchaseorder/', views.purchase_order_distinct_table, name="distinct_purchaseorder"),
    path('ind_purchaseorder/<str:pk>/', views.ind_purchaseorder, name="ind_purchaseorder"),
    path('purchase-order/create', views.Purchase_Order_Detail_Create.as_view(), name="purchase_order_form"),
    ]