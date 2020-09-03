from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from accounts.models import Customer, User


from rest_framework.test import force_authenticate


factory = APIRequestFactory()

user = User.objects.get(email="mazharis@msn.com")
view = LoginAPI.as_view()
