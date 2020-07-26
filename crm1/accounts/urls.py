from django.urls import path
from .import views


urlpatterns = [

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('new_product_profile/', views.NewProductProfile,
         name='new_product_profile'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('customer_orders/', views.customer_orders, name="customer_orders"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('customer_list/', views.customer_list, name="customer_list"),
    path('customer_profile/<str:pk>/',
         views.CustomerProfile, name="customer_profile"),
    path('delete_profile/<str:pk>/', views.deleteProfile, name="delete_profile"),
    path('address/<str:pk>/', views.Address, name="address_customer"),


    path('new_customer_profile/', views.NewCustomerProfile,
         name="new_customer_profile"),

    path('product_list/', views.product_list, name="product_list"),
    path('edit_product/<str:pk>/', views.EditProduct,
         name="edit_product_profile"),
    path('delete_product/<str:pk>/', views.DeleteProductProfile,
         name="delete_product_profile"),
    path('product_picture/<str:pk>/',
         views.ProductPicture, name="product_picture"),

    path('customer_order_list/', views.orderList, name="customer_order_list"),
    path('new_order/', views.newOrder, name="new_order"),
    path('edit_order/<str:pk>/', views.editOrder, name="edit_order"),
    path('delete_order/<str:pk>/', views.DeleteOrder, name="delete_order"),
]
