from django.db.models.signals import post_save
from .models import Product, Order, User, Customer
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def update_stock(sender, instance, created, **kwargs):

    if created:
        instance.product.stock = instance.product.stock - instance.order_required
        instance.product.save()
        instance.save()


@receiver(post_save, sender=Order)
def total_cost(sender, instance, created, **kwargs):

    if created:
        instance.total_cost_per_order = instance.product.r_price * instance.order_required
        instance.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()
