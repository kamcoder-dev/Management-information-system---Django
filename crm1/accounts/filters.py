import django_filters
from django_filters import DateFilter, CharFilter
from django.db.models import Q
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import *

# The filter class below is based upon the customer model, which will allow the user to filter through the  instances of the customer model


class CustomerlistFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method="my_custom_filter", field_name="name", label=" ", widget=forms.TextInput(attrs={'placeholder': 'Search by name, email address or customer id', 'class': 'form-control', 'size': 45}))

    class Meta:
        model = Customer
        fields = ['q']

# The function below is intended to allow the user to filter through the basis of the fields of the customer as shown
    def my_custom_filter(self, queryset, name, value):
        return Customer.objects.filter(
            Q(id__icontains=value)
            | Q(first_name__icontains=value)
            | Q(middle_name__icontains=value)
            | Q(last_name__icontains=value)
        )

# The filter class below is based upon the product model, which will allow the user to filter through the instances of the product model


class ProductListFilter(django_filters.FilterSet):

    q1 = django_filters.CharFilter(
        method="my_custom_product_filter", field_name="name", label=" ", widget=forms.TextInput(attrs={'placeholder': 'Search by SKU or Product Name', 'class': 'form-control', 'size': 45}))

    class Meta:
        model = Product
        fields = ['q1']

# The function below is intended to allow the user to filter through the basis of the fields of the product as shown

    def my_custom_product_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(product_sku__icontains=value)
            | Q(name__icontains=value))


# The filter class below is based upon the order model, which will allow the user to filter through the instances of the order model

class OrderListFilter(django_filters.FilterSet):

    q2 = django_filters.CharFilter(
        method="my_custom_order_filter", field_name="name", label=" ", widget=forms.TextInput(attrs={'placeholder': 'Search by Customer Name or Product Name', 'class': 'form-control', 'size': 45}))

    class Meta:
        model = Order
        fields = ['q2']

# The function below is intended to allow the user to filter through the basis of the fields of the order as shown

    def my_custom_order_filter(self, queryset, name, value):
        return Order.objects.filter(
            Q(status__icontains=value)
            | Q(customer_full_name__first_name__icontains=value)
            | Q(customer_full_name__middle_name__icontains=value)
            | Q(customer_full_name__last_name__icontains=value)
            | Q(product__name__icontains=value))
