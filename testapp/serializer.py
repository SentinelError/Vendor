from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def __init__(self,  *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['vendor_code'].read_only = True


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        depth = 1  # This will nest the vendor details in the serialized output


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
