from . import views
from django.urls import path

urlpatterns = [

    path('client-directory/', views.client_directory_overview, name="client_overview"),
    path('client-profile/<int:pk>/', views.individual_client_profile, name="client_profile"),
    path('client-price-list/', views.client_price_list, name="client_price_list"),
    path('client-price-list/<int:pk>/', views.individual_client_price_list, name="ind_client_price_list"),

    path('login/', views.login, name="login"),
    path('create-account/', views.create_account, name="create-account"),
    path('export-template/', views.export_excel_template, name="export-template")
]