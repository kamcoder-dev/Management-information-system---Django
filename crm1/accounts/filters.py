import django_filters
from django_filters import DateFilter, CharFilter
from django.db.models import Q
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']


class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    category = CharFilter(field_name='category', lookup_expr='icontains')

    class Meta:
        model = Product
        field = '__all__'
        exclude = ['start_date', 'end_date']


class CustomerlistFilter(django_filters.FilterSet):

    q = django_filters.CharFilter(
        method="my_custom_filter", field_name="name", label=" ", widget=forms.TextInput(attrs={'placeholder': 'Search by name, email address or customer id'}))

    class Meta:
        model = Customer
        fields = ['q']

    def my_custom_filter(self, queryset, name, value):
        return Customer.objects.filter(
            Q(id__icontains=value)
            | Q(first_name__icontains=value)
            | Q(middle_name__icontains=value)
            | Q(last_name__icontains=value)
        )


class ProductListFilter(django_filters.FilterSet):

    q1 = django_filters.CharFilter(
        method="my_custom_product_filter", field_name="name", label=" ", widget=forms.TextInput(attrs={'placeholder': 'search'}))

    class Meta:
        model = Product
        fields = ['q1']

    def my_custom_product_filter(self, queryset, name, value):
        return Product.objects.filter(
            Q(product_sku__icontains=value)
            | Q(name__icontains=value))


class OrderListFilter(django_filters.FilterSet):

    q2 = django_filters.CharFilter(
        method="my_custom_order_filter", field_name="name", label=" ")

    class Meta:
        model = Order
        fields = ['q2']

    def my_custom_order_filter(self, queryset, name, value):
        return Order.objects.filter(
            Q(status__icontains=value)
            | Q(customer__first_name__icontains=value)
            | Q(customer__middle_name__icontains=value)
            | Q(customer__last_name__icontains=value)
            | Q(product__name__icontains=value))
