from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializer import VendorSerializer, PurchaseOrderSerializer


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given vendor,
        by filtering against a `vendor_id` query parameter in the URL.
        """
        queryset = self.queryset
        vendor_id = self.request.query_params.get('vendor_id', None)
        if vendor_id is not None:
            queryset = queryset.filter(vendor_id=vendor_id)
        return queryset

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
