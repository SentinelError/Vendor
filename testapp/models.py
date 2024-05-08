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

    def save_historical_performance(self):
        HistoricalPerformance.objects.create(
            vendor=self,
            date=timezone.now(),
            on_time_delivery_rate=self.on_time_delivery_rate,
            quality_rating_avg=self.quality_rating_avg,
            average_response_time=self.average_response_time,
            fulfillment_rate=self.fulfillment_rate
        )

    def update_on_time_delivery_rate(self):
        # Filter completed orders for this vendor
        completed_orders = self.purchase_orders.filter(status='Complete')
        # Count orders where final delivery is on or before the expected delivery
        on_time_orders = completed_orders.filter(final_delivery_date__lte=F('expected_delivery_date')).count()
        total_completed = completed_orders.count()

        # Calculate the on-time delivery rate
        if total_completed > 0:
            new_rate = (on_time_orders / total_completed) * 100
        else:
            new_rate = 0  # Avoid division by zero

        if new_rate != self.on_time_delivery_rate:
            self.on_time_delivery_rate = new_rate
            self.save()
            self.save_historical_performance()  # Save the updated rate to the vendor

    def update_quality_rating_avg(self):
        ratings = self.purchase_orders.filter(quality_rating__isnull=False)
        new_avg = ratings.aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
        if new_avg != self.quality_rating_avg:
            self.quality_rating_avg = new_avg
            self.save()
            self.save_historical_performance()

    def update_average_response_time(self):
        responses = self.purchase_orders.exclude(acknowledgment_date__isnull=True).annotate(
            response_time=ExpressionWrapper(
                F('acknowledgment_date') - F('issue_date'),
                output_field=models.DurationField()
            )
        )
        average_response = responses.aggregate(average_time=Avg('response_time'))['average_time']

        # Ensure the calculation is performed only if average_response is not None
        new_avg_response_time = 0  # Default to 0
        if average_response is not None:
            new_avg_response_time = average_response.total_seconds() / 3600.0  # Convert to hours

        # Check if there is a change from the current average_response_time
        if new_avg_response_time != self.average_response_time:
            self.average_response_time = new_avg_response_time
            self.save()
            self.save_historical_performance()

    def update_fulfillment_rate(self):
        total_orders = self.purchase_orders.count()
        fulfilled_orders = self.purchase_orders.filter(status='Complete', quality_rating__isnull=False).count()
        new_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
        if new_rate != self.fulfillment_rate:
            self.fulfillment_rate = new_rate
            self.save()
            self.save_historical_performance()

    def __str__(self):
        return self.name + ' ' + self.vendor_code


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('incomplete', 'Incomplete'),
        ('complete', 'Complete'),
    )

    po_number = models.CharField(max_length=100, unique=True, primary_key=True)
    vendor = models.ForeignKey(Vendor, related_name='purchase_orders', on_delete=models.CASCADE)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, null=True, blank=True)
    quality_rating = models.FloatField(null=True, blank=True)
    order_date = models.DateTimeField()
    expected_delivery_date = models.DateTimeField()
    final_delivery_date = models.DateTimeField(null=True, blank=True)
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
