from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

# This serilaizer is used to convert DB entries into json to view.
class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    # This function is used to prevent changes to vendor_code which is the primary key for the testproject Model
    def __init__(self,  *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['vendor_code'].read_only = True


# This serilaizer is used to convert DB entries into json to view. The added line no.19 is used to select the testproject
# to fulfill the purchase order.
class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor = serializers.PrimaryKeyRelatedField(queryset=Vendor.objects.all())

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    # This function is used to prevent changes to po_number which is the primary key for the PurchaseOrder Model
    def __init__(self,  *args, **kwargs):
        super(PurchaseOrderSerializer, self).__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['po_number'].read_only = True


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
