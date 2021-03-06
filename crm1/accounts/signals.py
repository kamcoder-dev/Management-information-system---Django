from django.db.models.signals import post_save
from .models import Product, Order, User, Customer
from django.dispatch import receiver

# The receiver below allow automatic decrement for when the order instance is generated based upon the quantity of the product


@receiver(post_save, sender=Order)
def update_stock(sender, instance, created, **kwargs):

    if created:
        instance.product.stock = instance.product.stock - instance.order_required
        instance.product.save()
        instance.save()

# The reciever below allows the record the accumalation of the total cost of the order being generated for each product
@receiver(post_save, sender=Order)
def total_cost(sender, instance, created, **kwargs):

    if created:
        instance.total_cost_per_order = instance.product.r_price * instance.order_required
        instance.save()

# when the superuser is created via terminal, below will allow to extend the user towards the customer model


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      Customer.objects.get_or_create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_customer(sender, instance, **kwargs):
 #   instance.customer.save()
