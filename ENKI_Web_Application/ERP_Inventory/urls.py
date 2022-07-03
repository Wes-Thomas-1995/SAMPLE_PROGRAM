from . import views
from django.urls import path

urlpatterns = [

    path('inventory/', views.inventory, name="inventory"),
    path('product-library/', views.product_library, name='product-library'),
    path('store-specific-inventory/<str:pk>/', views.inventory_specific, name="inventory-specific"),


    #path('export-stock/', views.stock_export, name='stock-export'),
    #path('upload-stock/', views.stock_upload, name="stock-upload"),


    ]