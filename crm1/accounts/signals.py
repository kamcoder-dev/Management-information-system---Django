from django.db.models.signals import post_save
from .models import Product, Order
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def update_stock(sender, instance, created, **kwargs):
    if created:
        instance.product.stock = instance.product.stock - 1
        instance.product.save()
