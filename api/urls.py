from rest_framework.routers import DefaultRouter
from .views import VehicleViewSet, MaintenanceViewSet, ComplaintViewSet
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'maintenances', MaintenanceViewSet)
router.register(r'complaints', ComplaintViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Silant API",
      default_version='v1',
      description="API for Silant service management system",
      contact=openapi.Contact(email="support@silant.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path('', include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]