from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
import django_filters
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import UserAdminCreationForm, UserAdminChangeForm, RegisterForm, LoginForm, OrderForm, ProductForm, CustomerProfileForm, CustomUserForm, UpdateCustomUserForm, PictureForm, AddressUpdate, CreateOrderForm, CreateProductForm, EditCustomerProfileForm
from .filters import OrderFilter, ProductFilter, CustomerlistFilter, ProductListFilter, OrderListFilter
from django.db.models import F, Max, Sum
from django.http import HttpResponseRedirect, Http404
from django.db import transaction
from django.views.generic import UpdateView
from django.db.models import Count
import datetime
from django.shortcuts import get_object_or_404


def loginPage(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, "Email OR password is incorrect")
    return render(request, "accounts/login.html", context)

# login page to allow authenticate admin users within the MIS


def logoutUser(request):
    logout(request)
    return redirect('login')

# view to allow users to logout


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()

    active_users = User.objects.filter(active=True).count()

    total_orders = list(Order.objects.all().values_list(
        'order_required').aggregate(Sum('order_required')).values())[0]

    try:
        last_ordered_date = list(Order.objects.all().values_list(
            'date_created').latest())[0]

    except Order.DoesNotExist:
        last_ordered_date = None

    context = {'orders': orders,
               'total_orders': total_orders, 'active_users': active_users, 'last_ordered_date': last_ordered_date}

    return render(request, 'accounts/dashboard.html', context)

# view to show the dashboard whilst showing the number of active users, total orders, and the last order date
# Plans to showcase graphs with showing relationships between the models established in models.py


@login_required(login_url='login')
def NewProductProfile(request):
    form = ProductForm()
    # based on the form created when generating a new product instance
    if request.method == 'POST':
        form = ProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'accounts/new_product_profile.html', {'form': form})


@login_required(login_url='login')
def customer_list(request):

    users = User.objects.all().select_related('customer')
    # Queryset above encompasses the extended user model, with the customer model being inherited

    order = Order.objects.all()

    customer_list = Customer.objects.annotate(
        latest=Max('order__date_created'))

    last_created = Order.objects.values('customer_full_name_id').annotate(
        last_created=Max('date_created'))

    # Queryset above shows the last purchased order per Customer

    myFilter1 = CustomerlistFilter(request.GET, queryset=customer_list)
    customer_list = myFilter1.qs
    # Once renderended on the template, the filter above will allow the intended user to filter through instances based on the customer model fields

    context = {'customer_list': customer_list,
               'myFilter1': myFilter1, 'order': order, 'last_created': last_created, 'users': users}

    return render(request, 'accounts/customer_list.html', context)


@login_required(login_url='login')
def CustomerProfile(request, pk):

    try:
        order_customer_total = list(Order.objects.filter(
            customer_full_name__id=pk).aggregate(Sum('order_required')).values())[0]

# The above shows the total cost of ordered product per customer (which will be displayed on the template)

    except Order.DoesNotExist:
        order_customer_total = None

# This allow the queryset to display "None" when the value is nill.

    total_value_of_orders = list(Order.objects.all().values_list('total_cost_per_order').filter(customer_full_name__id=pk).aggregate(
        Sum('total_cost_per_order')).values())[0]

# Above shows the total value of orders per customer depending the quantity  of products inputted for when generating the instanced for the orders.

    try:
        latest_date = list(Order.objects.all().values_list(
            'date_created').filter(customer_full_name__id=pk).latest())[0]

    except Order.DoesNotExist:
        latest_date = None

# Above is intended to display on the template to showcase the last date of when the customer had ordered the

    customer = Customer.objects.get(id=pk)
    user = User.objects.get(id=pk)
    user_form = UpdateCustomUserForm(instance=user)
    customer_form = EditCustomerProfileForm(instance=customer)

# user_form and customer_form above will be used as a basis when generating instances via this view

    if request.method == 'POST':
        user_form = UpdateCustomUserForm(request.POST, instance=user)
        customer_form = EditCustomerProfileForm(
            request.POST, instance=customer)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            user.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('customer_list')

# The above shows the user_form and customer_form being used when generating the instances based on the user extended model and its inherited customer model.

    context = {'user_form': user_form, 'customer_form': customer_form, 'order_customer_total': order_customer_total,
               'total_value_of_orders': total_value_of_orders, 'latest_date': latest_date}
    return render(request, 'accounts/customer_profile.html', context)


@login_required(login_url='login')
def deleteProfile(request, pk):
    customer = User.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')

    context = {'customer': customer}
    return render(request, 'accounts/delete_profile.html', context)

# View above allows to delete each customer instance when selected in the customer list


@login_required(login_url='login')
def NewCustomerProfile(request):
    user_form = UpdateCustomUserForm()
    customer_form = EditCustomerProfileForm()

    if request.method == 'POST':
        user_form = UpdateCustomUserForm(request.POST)
        customer_form = EditCustomerProfileForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('customer_list')

    return render(request, 'accounts/new_customer_profile.html', {'user_form': user_form, 'customer_form': customer_form})

# The view above allows the admin user to generate an instance of customer


@login_required(login_url='login')
def product_list(request):

    product_list = Product.objects.annotate(
        norders=Sum('order__order_required')).order_by('product_sku')

    myFilter2 = ProductListFilter(request.GET, queryset=product_list)

    product_list = myFilter2.qs
    # Once renderended on the template, the filter above will allow the intended user to filter through instances based on the product
    #  model fields

    context = {'product_list': product_list, 'myFilter2': myFilter2}

    return render(request, 'accounts/product_list.html', context)


@login_required(login_url='login')
def EditProduct(request, pk):

    order_total = list(Order.objects.filter(
        product__id=pk).aggregate(Sum('order_required')).values())[0]

# The total amount of ordered products is established as a value within in order_total

    total_value_of_orders = list(Order.objects.filter(
        product__id=pk).aggregate(Sum('total_cost_per_order')).values())[0]
# The total amount spent in value per product based on its regular price on each instance of order generated
    try:
        last_ordered_date = list(Order.objects.all().values_list(
            'date_created').filter(product__id=pk).latest())[0]

    except Order.DoesNotExist:
        last_ordered_date = None

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')

    context = {'form': form, 'order_total': order_total,
               'total_value_of_orders': total_value_of_orders, 'last_ordered_date': last_ordered_date}
    return render(request, 'accounts/edit_product_profile.html', context)


@login_required(login_url='login')
def DeleteProductProfile(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')

    return render(request, 'accounts/delete_product_profile.html', {'product': product})


@login_required(login_url='login')
def ProductPicture(request, pk):

    PictureFormSet = inlineformset_factory(
        Product, Picture, fields=('product_pic',), extra=10)
    product = Product.objects.get(id=pk)
    formset = PictureFormSet(queryset=Picture.objects.none(), instance=product)
    picture = Picture.objects.select_related('product')
    if request.method == 'POST':
        form = PictureForm(request.POST)
        formset = PictureFormSet(request.POST, request.FILES, instance=product)
        if formset.is_valid():
            formset.save()
            return redirect('product_list')

    return render(request, 'accounts/product_picture.html', {'form': formset})


@login_required(login_url='login')
def Address(request, pk):
    # user_form = RegisterForm()
    address = Customer.objects.get(id=pk)
    address_form = AddressUpdate(instance=address)
    if request.method == 'POST':
        # user_form = RegisterForm(request.POST)
        address_form = AddressUpdate(request.POST, instance=address)

        if address_form.is_valid():
            address_form.save()
            return redirect('customer_list')

    context = {'address_form': address_form}
    return render(request, 'accounts/address.html', context)


@login_required(login_url='login')
def orderList(request):

    order_list = Order.objects.all().order_by('id')

    myFilter3 = OrderListFilter(request.GET, queryset=order_list)

    order_list = myFilter3.qs

    context = {'order_list': order_list, 'myFilter3': myFilter3}

    return render(request, 'accounts/customer_order_list.html', context)


@login_required
def newOrder(request):
    form = CreateOrderForm()
    if request.method == 'POST':
        form = CreateOrderForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('customer_order_list')

    return render(request, 'accounts/new_order.html', {'form': form})


@login_required
def editOrder(request, pk=None):
    order = get_object_or_404(Order, id=pk)

    try:
        order_date = list(Order.objects.all().values_list(
            'date_created').filter(id=pk))[0][0]
    except Order.DoesNotExist:
        order_date = None

    form = CreateOrderForm(instance=order)

    if request.method == "POST":
        form = CreateOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('customer_order_list')

    return render(request, 'accounts/edit_order.html', {'form': form, 'order_date': order_date})


@login_required(login_url='login')
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('customer_order_list')

    return render(request, 'accounts/delete_order.html', {'order': order})
