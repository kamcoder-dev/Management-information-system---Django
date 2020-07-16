from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User, Customer, Order, Product, Picture
from django.forms import ModelForm, ModelChoiceField
from django.forms import widgets, DateTimeField, DateField, DateInput
from crispy_forms.helper import FormHelper
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget
from django_countries.fields import CountryField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'admin', 'active')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class ProductForm(forms.ModelForm):

    name = forms.CharField(label="Name")
    product_sku = forms.CharField(label="SKU Code")
    r_price = forms.FloatField(label="Regular Price")
    d_price = forms.FloatField(label="Discount Price", required=False)
    min_stock = forms.IntegerField(label="Minimum Stock")
    stock = forms.IntegerField(label="No in Stock")
    description = forms.CharField(
        label="Description", widget=forms.Textarea)

    start_date = forms.DateTimeField(widget=DateInput(format='%d-%m-%Y'),
                                     input_formats=('%d-%m-%Y',),
                                     required=False)

    end_date = forms.DateTimeField(widget=DateInput(format='%d-%m-%Y'),
                                   input_formats=('%d-%m-%Y',),
                                   required=False)

    class Meta:
        model = Product
        fields = ['product_sku', 'name', 'category', 'description', 'r_price',
                  'd_price', 'start_date', 'end_date', 'stock', 'min_stock']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = "form-horizontal"


class CreateProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_sku', 'name', 'category', 'description', 'r_price',
                  'd_price', 'start_date', 'end_date', 'stock', 'min_stock']


class CustomerProfileForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['title', 'first_name', 'middle_name',
                  'last_name', 'phone', 'country', 'birth_year', 'gender']


class EditCustomerProfileForm(ModelForm):

    phone = forms.CharField(label="Telephone No")
    birth_year = forms.CharField(label="Birth Year")

    customer_uuid = forms.UUIDField(disabled=True, label="Customer ID")

    class Meta:
        model = Customer
        fields = ['customer_uuid', 'title', 'first_name', 'middle_name',
                  'last_name', 'phone', 'country', 'birth_year', 'gender']


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = '__all__'


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'active', 'admin']
        # exclude = ('last_login', 'staff' )


class UpdateCustomUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'password', 'active', 'admin']


class AddressUpdate(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['address1', 'address2', 'city', 'county', 'post_code']


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['customer_full_name', 'product', 'delivery_address1', 'delivery_address2',
                  'delivery_city', 'delivery_county', 'delivery_post_code', 'delivery_country']
