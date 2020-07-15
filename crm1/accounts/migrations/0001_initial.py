# Generated by Django 3.0.6 on 2020-07-15 18:29

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Miss', 'Miss'), ('Ms', 'Ms'), ('Dr', 'Dr'), ('Sir', 'Sir'), ('Madam', 'Madam')], max_length=200, null=True)),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('middle_name', models.CharField(blank=True, default='', max_length=200)),
                ('last_name', models.CharField(max_length=200, null=True)),
                ('phone', models.CharField(max_length=200, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('birth_year', models.CharField(max_length=4, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='')),
                ('last_purchase', models.DateTimeField(blank=True, null=True)),
                ('address1', models.CharField(max_length=1000, null=True)),
                ('address2', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('city', models.CharField(max_length=1000, null=True)),
                ('county', models.CharField(max_length=1000, null=True)),
                ('post_code', models.CharField(max_length=1000, null=True)),
                ('customer_uuid', models.UUIDField(default=uuid.uuid4)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('category', models.CharField(choices=[('Sports', 'Sports'), ('Fashion', 'Fashion'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Kitchen', 'Kitchen'), ('Jewellery', 'Jewellery')], max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('r_price', models.FloatField(null=True)),
                ('d_price', models.FloatField(blank=True, default='', null=True)),
                ('start_date', models.DateField(blank=True, default='', null=True)),
                ('end_date', models.DateField(blank=True, default='', null=True)),
                ('stock', models.IntegerField(null=True)),
                ('min_stock', models.IntegerField(null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('product_sku', models.CharField(max_length=200, null=True)),
                ('tags', models.ManyToManyField(to='accounts.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_pic', models.ImageField(blank=True, null=True, upload_to=accounts.models.path_and_rename)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=200, null=True)),
                ('note', models.CharField(max_length=1000, null=True)),
                ('delivery_address1', models.CharField(max_length=1000, null=True)),
                ('delivery_address2', models.CharField(blank=True, default='', max_length=1000, null=True)),
                ('delivery_city', models.CharField(max_length=1000, null=True)),
                ('delivery_county', models.CharField(max_length=1000, null=True)),
                ('delivery_post_code', models.CharField(max_length=1000, null=True)),
                ('delivery_country', django_countries.fields.CountryField(max_length=2)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Customer')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.Product')),
            ],
            options={
                'get_latest_by': 'date_created',
            },
        ),
    ]
