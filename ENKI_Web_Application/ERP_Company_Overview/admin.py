from django.contrib import admin
from .models import Client_Directory, Child_Company_Information, Company_Permissions, Parent_Company_Information


admin.site.register(Client_Directory)
admin.site.register(Company_Permissions)
admin.site.register(Child_Company_Information)
admin.site.register(Parent_Company_Information)