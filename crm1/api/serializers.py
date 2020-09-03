from rest_framework import serializers
from django.contrib.auth import authenticate

from accounts.models import Customer, User


# Customer Serializers
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('title', 'first_name', 'middle_name',
                  'last_name', 'phone', 'country', 'birth_year', 'gender')

# Register Serializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    customer = CustomerSerializer(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'customer')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        customer_data = validated_data.pop('customer')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Customer.objects.create(user=user, **customer_data)
        return user

    def update(self, instance, validated_data):
        customer_data = validated_data.pop('customer')
        customer = instance.customer
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        customer.title = customer_data.get('title', customer.title)
        customer.first_name = customer_data.get(
            'first_name', customer.first_name)
        customer.middle_name = customer_data.get(
            'middle_name', customer.middle_name)
        customer.last_name = customer_data.get('last_name', customer.last_name)
        customer.phone = customer_data.get('phone', customer.phone)
        customer.country = customer_data.get('country', customer.country)
        customer.birth_year = customer_data.get(
            'birth_year', customer.birth_year)
        customer.gender = customer_data.get('gender', customer.gender)
        customer.save()

        return instance


# Register API
# class RegisterSerializer(generics.ModelSerializer):
 #   class Meta:
  #      model = User
    #    fields = ('id', 'email', 'password')
   #     extra_kwargs = {'password':{'write_only:True'}}

#    def create(self, validated_data):
 #       user = User.objects.create_user(validated_data['email']), validated_data['password'])

  #      return user

# login serializer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Wrong Details Entered")
