from django.db import models
from django.db.models.signals import post_save


class Parent_Company_Information(models.Model):
    parent_company_name = models.CharField(max_length=200)
    parent_company_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.parent_company_name


class Child_Company_Information(models.Model):
    parent_company_name = models.ForeignKey(Parent_Company_Information, on_delete=models.DO_NOTHING)
    child_company_name = models.CharField(max_length=200, null=True, blank=True)
    child_company_id = models.AutoField(primary_key=True)
    company_location = models.CharField(max_length=200)

    def __str__(self):
        return self.child_company_name


class Company_Permissions(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    permission_level = models.IntegerField()
    user_first_name = models.CharField(max_length=200, null=True, blank=True)
    user_last_name = models.CharField(max_length=200, null=True, blank=True)
    user_email = models.CharField(max_length=200)
    parent_company_name = models.ForeignKey(Parent_Company_Information, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.username)


class Client_Directory(models.Model):
    client_id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=200)
    client_email = models.CharField(max_length=200)
    client_telephone = models.CharField(max_length=200)
    client_address = models.CharField(max_length=200)
    client_postcode = models.CharField(max_length=200)
    point_of_contact_first = models.CharField(max_length=200)
    point_of_contact_last = models.CharField(max_length=200)
    account_status = models.BooleanField(default=True)
    child_company_name = models.ForeignKey(Child_Company_Information, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.client_name



