from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializer import VendorSerializer, PurchaseOrderSerializer


# This viewset accomplishes all CRUD functionalities.
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


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
