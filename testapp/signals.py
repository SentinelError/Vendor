from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics_on_save(sender, instance, **kwargs):
    # Trigger updates based on the status of the order or if it's acknowledged
    if instance.status == 'Complete':
        instance.vendor.update_on_time_delivery_rate()
        instance.vendor.update_quality_rating_avg()
    if instance.acknowledgment_date:
        instance.vendor.update_average_response_time()
    instance.vendor.update_fulfillment_rate()

@receiver(post_delete, sender=PurchaseOrder)
def update_vendor_metrics_on_delete(sender, instance, **kwargs):
    # Update metrics assuming the vendor still needs accurate metrics without this order
    if instance.vendor:
        instance.vendor.update_on_time_delivery_rate()
        instance.vendor.update_quality_rating_avg()
        instance.vendor.update_average_response_time()
        instance.vendor.update_fulfillment_rate()