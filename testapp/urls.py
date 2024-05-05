from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import VendorViewSet, PurchaseOrderViewSet

# This router redirects to the respective vendors or purchase_orders page from root /api/
router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'purchase_orders', PurchaseOrderViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
]
