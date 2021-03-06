# Generated by Django 3.2.6 on 2021-09-19 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ERP_Company_Overview', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_code', models.CharField(max_length=200)),
                ('categorisation', models.CharField(max_length=200)),
                ('product_type', models.CharField(max_length=200)),
                ('cost_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=200)),
                ('price_creation_date', models.DateTimeField(auto_now_add=True)),
                ('price_update_date', models.DateTimeField(auto_now=True, null=True)),
                ('manufacturer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ERP_Inventory.manufacture')),
            ],
        ),
        migrations.CreateModel(
            name='Price_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_creation_date', models.DateTimeField(auto_now_add=True)),
                ('price_update_date', models.DateTimeField(auto_now=True, null=True)),
                ('client_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ERP_Company_Overview.client_directory')),
                ('product_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ERP_Inventory.product_library')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('inventory_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ERP_Company_Overview.child_company_information')),
                ('product_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='ERP_Inventory.product_library')),
            ],
        ),
    ]
