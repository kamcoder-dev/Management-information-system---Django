from django.test import SimpleTestCase
from django.urls import reverse, resolve
from accounts.views import *


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)

    def test_logout_url_is_resolved(self):
        url = reverse('logout')
        print(resolve(url))
        self.assertEquals(resolve(url).func, logoutUser)

    def test_login_url_is_resolved(self):
        url = reverse('login')
        print(resolve(url))
        self.assertEquals(resolve(url).func, loginPage)

    def test_new_product_profile_url_is_resolved(self):
        url = reverse('new_product_profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, NewProductProfile)

    def test_customer_list_url_is_resolved(self):
        url = reverse('customer_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, customer_list)

    def test_customer_profile_url_is_resolved(self):
        url = reverse('customer_profile', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, CustomerProfile)

    def test_delete_profile_url_is_resolved(self):
        url = reverse('delete_profile', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, deleteProfile)

    def test_address_url_is_resolved(self):
        url = reverse('address_customer', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, Address)

    def test_new_customer_profile_url_is_resolved(self):
        url = reverse('new_customer_profile')
        print(resolve(url))
        self.assertEquals(resolve(url).func, NewCustomerProfile)

    def test_product_list_url_is_resolved(self):
        url = reverse('product_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, product_list)

    def test_edit_product_profile_url_is_resolved(self):
        url = reverse('edit_product_profile', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, EditProduct)

    def test_delete_product_url_is_resolved(self):
        url = reverse('delete_product_profile', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, DeleteProductProfile)

    def test_product_picture_url_is_resolved(self):
        url = reverse('product_picture', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, ProductPicture)

    def test_edit_order_url_is_resolved(self):
        url = reverse('edit_order', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, editOrder)

    def test_delete_order_url_is_resolved(self):
        url = reverse('delete_order', args=['pk'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, DeleteOrder)

    def test_customer_order_list_url_is_resolved(self):
        url = reverse('customer_order_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, orderList)

    def test_new_order_url_is_resolved(self):
        url = reverse('customer_order_list')
        print(resolve(url))
        self.assertEquals(resolve(url).func, orderList)
