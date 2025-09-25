from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GovernorateViewSet, ComplaintTypeViewSet, ComplaintViewSet,
    ComplaintAttachmentViewSet, ComplaintUpdateViewSet, ComplaintSettingsViewSet
)

router = DefaultRouter()
router.register(r'governorates', GovernorateViewSet)
router.register(r'complaint-types', ComplaintTypeViewSet)
router.register(r'complaints', ComplaintViewSet)
router.register(r'attachments', ComplaintAttachmentViewSet)
router.register(r'updates', ComplaintUpdateViewSet)
router.register(r'settings', ComplaintSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

