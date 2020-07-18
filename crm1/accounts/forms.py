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
        fields = ['product', 'customer_full_name', 'delivery_address1', 'delivery_address2', 'delivery_county','delivery_city', 'delivery_country','delivery_post_code']
   # fproduct_sku = forms.CharField(label="SKU name", max_length=70)
    # fproduct_name = forms.CharField(
    #   label="Product Name", max_length=70, disabled=True)
    #fuser_email = forms.CharField(label="Customer Email", max_length=70)
    #fcustomer_phone = forms.CharField(label="Phone")
    #fcustomer_full_name = forms.CharField(label="Full Name", max_length=70)
    #delivery_address1 = forms.CharField(label="Delivery to")
    #delivery_address2 = forms.CharField(label="")
    #delivery_city = forms.CharField(label="")
    #delivery_country = CountryField().formfield(label="Country")
    #delivery_post_code = forms.CharField(label="Post Code")
    #order_required = forms.IntegerField(label="Order Required")
    #fid = forms.IntegerField(label="id", disabled=True)

    # def save(self, datas):
    #   ord1 = Order()
    #  ord1.pk = datas['fid']

    # product = Product()
    #product_name = Product()
    #user_email = Customer()
    #customer_phone = Customer()
    #user_full_name = Customer()

    #product.pk = datas['fproduct_sku']
    #product_name.pk = datas['fproduct_name']
    #user_email.pk = datas['fuser_email']
    #customer_phone.pk = datas['fcustomer_phone']
    #customer_full_name.pk = ['customer_full_name']

    # product.save()
    # product_name.save()
    # user_email.save()
    # customer_phone.save()
    # user_full_name.save()

    #ord1.product = product
    # ord1.product_name = product_name
    #ord1.user_email = user_email
    #ord1.customer_phone = customer_phone
    #ord1.user_full_name = user_full_name

    # ord1.save()
    # return ord1
