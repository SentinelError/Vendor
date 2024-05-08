from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import status
from django.db.models import F, Avg, ExpressionWrapper
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializer import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


# This viewset accomplishes all CRUD functionalities.
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    @action(detail=True, methods=['get'], url_path='performance')
    def performance(self, request, pk=None):
        vendor = self.get_object()  # Retrieves the Vendor based on vendor_code
        # Extracting performance metrics
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }
        return Response(performance_data, status=status.HTTP_200_OK)


# This viewset accomplishes all CRUD functionalities.
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # This function is used to obtain purchase orders by querying vendor_code.

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['vendor__vendor_code']

    @action(detail=True, methods=['get','post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=True, methods=['get', 'post'])
    def complete(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.final_delivery_date = timezone.now()
        purchase_order.status = 'Complete'
        purchase_order.save()
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HistoricalPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['vendor__vendor_code']

