from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
import django_filters
from django.contrib.auth.decorators import login_required

# Create your views here.
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


def registerPage(request):

    form = RegisterForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        form.save()

    return render(request, "accounts/register.html", context)


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
            messages.info(request, "Username OR password is incorrect")
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    last_ordered_date = Order.objects.all().values_list(
        'date_created').latest()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'pending': pending, 'total_customers': total_customers, 'last_ordered_date': last_ordered_date}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def NewProductProfile(request):
    form = CreateProductForm()
    if request.method == 'POST':
        form = CreateProductForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    return render(request, 'accounts/new_product_profile.html', {'form': form})


@login_required(login_url='login')
def customer_orders(request):

    form = ProductForm()

    context = {'form': form}
    return render(request, 'accounts/customer_orders.html', context)


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders,
               'order_count': order_count, 'myFilter': myFilter}

    return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('customer_order_list')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('customer_order_list')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('customer_order_list')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
def customer_list(request):

    users = User.objects.all().select_related('customer')

    # customer_list = Customer.objects.all().order_by('id')

    customer_list = Customer.objects.annotate(
        latest=Max('order__date_created'))

    # dingo = Order.objects.all().values_list('date_created')

    # last_purchase_order = dingo.filter(customer__id).latest()

    order = Order.objects.all()
    # k = Customer.objects.annotate(last_purchase=Max('order__date_created'))
    k = Order.objects.values('customer_id').annotate(
        last_created=Max('date_created'))
    myFilter1 = CustomerlistFilter(request.GET, queryset=customer_list)
    customer_list = myFilter1.qs
    context = {'customer_list': customer_list,
               'myFilter1': myFilter1, 'order': order, 'k': k, 'users': users}

    return render(request, 'accounts/customer_list.html', context)

    # order =  Order.objects.all()

    # latest_order_per_user = Order.objects.annotate(latest=Max('customer__order__date_created')).filter(date_created=F('latest'))
    # latest_dates = latest_order_per_user.values('date_created' )
    # last_date = latest_dates.last()

    # date_created = Customer.objects.annotate(last_purchase=Max('order__date_created'))

# @login_required(login_url='login')
# def CustomerProfile(request, pk):

#	customer = Customer.objects.get(id=pk)
#	formie = CustomerProfileForm(instance=customer)
#	if 'edit_customer' in request.POST:
#		if request.method == 'POST':
#			formie = CustomerProfileForm(request.POST, instance=customer)
#			if formie.is_valid():
#				formie.save()
#				return redirect('/')


#	context = {'formie':formie}
#	return render(request, 'accounts/customer_profile.html', context)


@login_required(login_url='login')
def CustomerProfile(request, pk):

    customer_no = Order.objects.filter(customer__id=pk)
    order_customer_total = customer_no.count()

    customer_s = Order.objects.all().values_list('product__r_price')

    r = customer_s.filter(customer__id=pk).aggregate(
        Sum('product__r_price'))
    total_value_of_orders = list(r.values())[0]

    try:
        latest_date = Order.objects.all().values_list(
            'date_created').filter(customer__id=pk).latest()

    except Order.DoesNotExist:
        latest_date = None

    customer = Customer.objects.get(id=pk)
    user = User.objects.get(id=pk)
    user_form = UpdateCustomUserForm(instance=user)
    # customer_form = CustomerProfileForm(instance=request.user.customer)
    customer_form = EditCustomerProfileForm(instance=customer)

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

    context = {'user_form': user_form, 'customer_form': customer_form, 'order_customer_total': order_customer_total,
               'total_value_of_orders': total_value_of_orders, 'latest_date': latest_date}
    return render(request, 'accounts/customer_profile.html', context)

    # if user_form.is_valid() and customer_form.is_valid():
    #    user = user_form.save()
    #    user.save()
    #    customer = customer_form.save(commit=False)
    #    customer.user = user
    #    customer.save()
    #    return redirect('/')


@login_required(login_url='login')
def deleteProfile(request, pk):
    customer = User.objects.get(id=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')

    context = {'customer': customer}
    return render(request, 'accounts/delete_profile.html', context)


@login_required(login_url='login')
def NewCustomerProfile(request):
    user_form = RegisterForm()
    customer_form = CustomerProfileForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        customer_form = CustomerProfileForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('customer_list')

    return render(request, 'accounts/new_customer_profile.html', {'user_form': user_form, 'customer_form': customer_form})


@login_required(login_url='login')
def product_list(request):

    product_list = Product.objects.annotate(
        norders=Count('order')).order_by('product_sku')

    myFilter2 = ProductListFilter(request.GET, queryset=product_list)

    product_list = myFilter2.qs

    context = {'product_list': product_list, 'myFilter2': myFilter2}

    return render(request, 'accounts/product_list.html', context)


@login_required(login_url='login')
def EditProduct(request, pk):

    product_no = Order.objects.filter(product__id=pk)
    order_total = product_no.count()

    r = product_no.aggregate(Sum('product__r_price'))
    total_value_of_orders = list(r.values())[0]

    try:
        last_ordered_date = Order.objects.all().values_list(
            'date_created').filter(product__id=pk).latest()

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
def editOrder(request, pk):
    order = Order.objects.get(id=pk)
    sho = Order.objects.all().values_list('date_created')
    order_date = sho.filter(id=pk)
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
