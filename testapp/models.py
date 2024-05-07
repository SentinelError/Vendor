from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.db.models import F, Avg, ExpressionWrapper
from django.utils import timezone


class Vendor(models.Model):
    vendor_code = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def update_on_time_delivery_rate(self):
        completed_orders = self.purchase_orders.filter(status='completed')
        on_time_orders = completed_orders.filter(delivery_date__lte=F('order_date'))
        total_completed = completed_orders.count()
        if total_completed > 0:
            self.on_time_delivery_rate = (on_time_orders.count() / total_completed) * 100
            self.save()

    def update_quality_rating_avg(self):
        ratings = self.purchase_orders.filter(quality_rating__isnull=False)
        self.quality_rating_avg = ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        self.save()

    def update_average_response_time(self):
        responses = self.purchase_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=models.DurationField()
            )
        )
        average_response = responses.aggregate(average_time=Avg('response_time'))['average_time']
        self.average_response_time = average_response.total_seconds() / 3600.0  # convert to hours
        self.save()

    def update_fulfillment_rate(self):
        total_orders = self.purchase_orders.count()
        fulfilled_orders = self.purchase_orders.filter(status='completed', quality_rating__isnull=False).count()
        if total_orders > 0:
            self.fulfillment_rate = (fulfilled_orders / total_orders) * 100
            self.save()

    def __str__(self):
        return self.name + ' ' + self.vendor_code




class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)




class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='historical_performances', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

# This section is to create an authentication token for users on the site.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
