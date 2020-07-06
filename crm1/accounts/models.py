from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django_countries.fields import CountryField
import os
from django.utils import timezone
from uuid import uuid4
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from activatable_model.models import BaseActivatableModel
from django.db.models import Max
import uuid
from datetime import datetime


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have email address")
        user_obj = self.model(email=self.normalize_email(email))
        if not password:
            raise ValueError("Users must have a password")

        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(email, password=password, is_staff=True)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password=password,
                                is_staff=True, is_admin=True)

        return user


class User(AbstractBaseUser):

    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # email and password are required by default
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Customer(models.Model):

    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    TITLE = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
        ('Sir', 'Sir'),
        ('Madam', 'Madam'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, choices=TITLE)
    first_name = models.CharField(max_length=200, null=True)
    middle_name = models.CharField(max_length=200, blank=True, default='')
    last_name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    country = CountryField()
    birth_year = models.CharField(max_length=4, null=True)
    gender = models.CharField(max_length=200, null=True, choices=GENDER)
    date_created = models.DateTimeField(auto_now=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True)
    last_purchase = models.DateTimeField(blank=True, null=True)
    address1 = models.CharField(max_length=1000, null=True)
    address2 = models.CharField(
        max_length=1000, null=True, blank=True, default='')
    city = models.CharField(max_length=1000, null=True)
    county = models.CharField(max_length=1000, null=True)
    post_code = models.CharField(max_length=1000, null=True)
    customer_uuid = models.UUIDField(default=uuid.uuid4)

    def __str__(self):
        return self.user.email


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created,**kwargs):
#    if created:
#        Customer.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#    instance.customer.save()

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    CATEGORY = (
        ('Sports', 'Sports'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Kitchen', 'Kitchen'),
        ('Jewellery', 'Jewellery'),
    )

    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    r_price = models.FloatField(null=True)
    d_price = models.FloatField(null=True, blank=True, default='')
    start_date = models.DateField(null=True, blank=True, default='')
    end_date = models.DateField(null=True, blank=True, default='')
    tags = models.ManyToManyField(Tag)
    stock = models.IntegerField(null=True)
    min_stock = models.IntegerField(null=True)
    is_active = models.BooleanField(default=False)
    product_sku = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.product_sku

  #  def clean(self):
   #     if self.start_date < datetime.now() < self.end_date:
    #        self.r_price = None

     #   elif self.end_date < datetime.now():
      #      self.d_price = None


class Order(models.Model):

    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(
        Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)
    delivery_address1 = models.CharField(max_length=1000, null=True)
    delivery_address2 = models.CharField(
        max_length=1000, null=True, blank=True, default='')
    delivery_city = models.CharField(max_length=1000, null=True)
    delivery_county = models.CharField(max_length=1000, null=True)
    delivery_post_code = models.CharField(max_length=1000, null=True)
    delivery_country = CountryField()

    class Meta:
        get_latest_by = 'date_created'

    def __str__(self):
        return self.product.name


def get_image_filename(instance, filename):
    id = instance.product.id
    return "picture_image/%s" % (id)


def path_and_rename(instance, filename):
    upload_to = 'images'
    ext = filename.split('.'[-1])
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Picture(models.Model):
    product_pic = models.ImageField(
        null=True, blank=True, upload_to=path_and_rename)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


def __str__(self):
    return self.product.name
