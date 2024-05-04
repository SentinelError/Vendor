from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import VendorViewSet, PurchaseOrderViewSet

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
