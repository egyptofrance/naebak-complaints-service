from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Governorate, ComplaintType, Complaint, ComplaintAttachment, ComplaintUpdate, ComplaintSettings
from .serializers import (
    GovernorateSerializer, ComplaintTypeSerializer, ComplaintSerializer,
    ComplaintAttachmentSerializer, ComplaintUpdateSerializer, ComplaintSettingsSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class GovernorateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer
    permission_classes = [permissions.AllowAny]

class ComplaintTypeViewSet(viewsets.ModelViewSet):
    queryset = ComplaintType.objects.all()
    serializer_class = ComplaintTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Complaint.objects.all()
        return Complaint.objects.filter(complainant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(complainant=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign(self, request, pk=None):
        complaint = get_object_or_404(Complaint, pk=pk)
        assigned_to_id = request.data.get("assigned_to")
        # Logic to assign complaint to a user (representative)
        return Response({"status": "complaint assigned"})

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        complaint = get_object_or_404(Complaint, pk=pk)
        # Logic to mark complaint as resolved
        return Response({"status": "complaint resolved"})

class ComplaintAttachmentViewSet(viewsets.ModelViewSet):
    queryset = ComplaintAttachment.objects.all()
    serializer_class = ComplaintAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ComplaintAttachment.objects.all()
        return ComplaintAttachment.objects.filter(complaint__complainant=self.request.user)

class ComplaintUpdateViewSet(viewsets.ModelViewSet):
    queryset = ComplaintUpdate.objects.all()
    serializer_class = ComplaintUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ComplaintUpdate.objects.all()
        return ComplaintUpdate.objects.filter(complaint__complainant=self.request.user)

class ComplaintSettingsViewSet(viewsets.ModelViewSet):
    queryset = ComplaintSettings.objects.all()
    serializer_class = ComplaintSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

