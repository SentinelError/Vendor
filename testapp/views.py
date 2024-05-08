from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import status
from django.db.models import F, Avg, ExpressionWrapper
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializer import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


# Manages CRUD operations for Vendor instances with a custom performance retrieval action.
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    # Returns performance metrics for a Vendor instance.
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


# Manages CRUD operations for PurchaseOrder instances with support for acknowledging and completing orders.
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # This function is used to obtain purchase orders by querying vendor_code.
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['vendor__vendor_code']

    # Sets acknowledgment date for a PurchaseOrder.
    @action(detail=True, methods=['get','post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Marks a PurchaseOrder as complete.
    @action(detail=True, methods=['get', 'post'])
    def complete(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.final_delivery_date = timezone.now()
        purchase_order.status = 'Complete'
        purchase_order.save()
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Provides read-only access to HistoricalPerformance data with filtering by vendor_code.
class HistoricalPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['vendor__vendor_code']

    @action(detail=False, methods=['delete'], url_path='delete-bulk')
    def delete_bulk(self, request):
        filters = {key: request.query_params[key] for key in request.query_params if key in self.filterset_fields}
        self.queryset.filter(**filters).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
