from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_on_time_delivery_rate()
        instance.vendor.update_quality_rating_avg()
    if instance.acknowledgment_date:
        instance.vendor.update_average_response_time()
    instance.vendor.update_fulfillment_rate()
