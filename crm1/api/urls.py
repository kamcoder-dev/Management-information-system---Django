from django.urls import path
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from knox import views as knox_views
from rest_framework import routers
from .views import RegistrationAPI, LoginAPI, UserAPI

#router = routers.SimpleRouter()
# router.register(r'register', RegistrationAPI basename=register)
#router.register(r'login', LoginAPI)

# urlpatterns = [
#   url('auth', include('knox.urls')),
#  url(r'^', include(router.urls)),
# ]

urlpatterns = [

    path('auth', include('knox.urls')),
    path('auth/register', RegistrationAPI.as_view()),
    path('auth/login', LoginAPI.as_view()),
    path('auth/logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('auth/user', UserAPI.as_view()),
]
