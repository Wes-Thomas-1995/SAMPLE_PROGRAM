
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ERP_Home.urls')),
    path('', include('ERP_Company_Overview.urls')),
    path('', include('ERP_Inventory.urls')),
    path('', include('ERP_Purchase_Order.urls')),
    path('', include('ERP_Sales_Order.urls')),
]

urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns  += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)