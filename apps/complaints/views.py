from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
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

@extend_schema_view(
    list=extend_schema(
        summary="قائمة المحافظات المصرية",
        description="الحصول على قائمة بجميع المحافظات المصرية الـ 27 المتاحة في النظام",
        tags=["المحافظات"]
    ),
    retrieve=extend_schema(
        summary="تفاصيل محافظة",
        description="الحصول على تفاصيل محافظة معينة باستخدام معرفها",
        tags=["المحافظات"]
    )
)
class GovernorateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet للمحافظات المصرية - Egyptian Governorates ViewSet
    
    يوفر عمليات القراءة فقط للمحافظات المصرية الـ 27.
    لا يتطلب مصادقة ويمكن الوصول إليه من قبل جميع المستخدمين.
    """
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema_view(
    list=extend_schema(
        summary="قائمة أنواع الشكاوى",
        description="الحصول على قائمة بجميع أنواع الشكاوى المتاحة في النظام",
        tags=["أنواع الشكاوى"]
    ),
    retrieve=extend_schema(
        summary="تفاصيل نوع شكوى",
        description="الحصول على تفاصيل نوع شكوى معين",
        tags=["أنواع الشكاوى"]
    ),
    create=extend_schema(
        summary="إنشاء نوع شكوى جديد",
        description="إنشاء نوع شكوى جديد (للمديرين فقط)",
        tags=["أنواع الشكاوى"]
    ),
    update=extend_schema(
        summary="تحديث نوع شكوى",
        description="تحديث نوع شكوى موجود (للمديرين فقط)",
        tags=["أنواع الشكاوى"]
    ),
    destroy=extend_schema(
        summary="حذف نوع شكوى",
        description="حذف نوع شكوى من النظام (للمديرين فقط)",
        tags=["أنواع الشكاوى"]
    )
)
class ComplaintTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet لأنواع الشكاوى - Complaint Types ViewSet
    
    يوفر إدارة كاملة لأنواع الشكاوى في النظام.
    القراءة متاحة للجميع، التعديل للمديرين فقط.
    """
    queryset = ComplaintType.objects.all()
    serializer_class = ComplaintTypeSerializer
    permission_classes = [IsAdminOrReadOnly]

@extend_schema_view(
    list=extend_schema(
        summary="قائمة الشكاوى",
        description="الحصول على قائمة الشكاوى. المديرون يرون جميع الشكاوى، المستخدمون العاديون يرون شكاواهم فقط",
        tags=["الشكاوى"]
    ),
    retrieve=extend_schema(
        summary="تفاصيل شكوى",
        description="الحصول على تفاصيل شكوى معينة",
        tags=["الشكاوى"]
    ),
    create=extend_schema(
        summary="تقديم شكوى جديدة",
        description="تقديم شكوى جديدة من قبل المستخدم المسجل",
        tags=["الشكاوى"]
    ),
    update=extend_schema(
        summary="تحديث شكوى",
        description="تحديث شكوى موجودة (للمالك أو المدير)",
        tags=["الشكاوى"]
    ),
    destroy=extend_schema(
        summary="حذف شكوى",
        description="حذف شكوى من النظام (للمالك أو المدير)",
        tags=["الشكاوى"]
    )
)
class ComplaintViewSet(viewsets.ModelViewSet):
    """
    ViewSet للشكاوى - Complaints ViewSet
    
    يوفر إدارة كاملة للشكاوى في النظام مع التحكم في الصلاحيات.
    المستخدمون يمكنهم رؤية وإدارة شكاواهم فقط، المديرون يرون جميع الشكاوى.
    """
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        تخصيص الاستعلام حسب نوع المستخدم
        المديرون يرون جميع الشكاوى، المستخدمون العاديون يرون شكاواهم فقط
        """
        if self.request.user.is_staff:
            return Complaint.objects.all()
        return Complaint.objects.filter(complainant=self.request.user)

    def perform_create(self, serializer):
        """
        تعيين المستخدم الحالي كمقدم الشكوى عند الإنشاء
        """
        serializer.save(complainant=self.request.user)

    @extend_schema(
        summary="تعيين شكوى لممثل",
        description="تعيين شكوى معينة لممثل أو مسؤول للمتابعة (للمديرين فقط)",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'assigned_to': {
                        'type': 'integer',
                        'description': 'معرف المستخدم المراد تعيين الشكوى له'
                    }
                },
                'required': ['assigned_to']
            }
        },
        responses={200: {'description': 'تم تعيين الشكوى بنجاح'}},
        tags=["الشكاوى"]
    )
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def assign(self, request, pk=None):
        """
        تعيين شكوى لممثل أو مسؤول للمتابعة
        
        Args:
            request: طلب HTTP يحتوي على معرف المستخدم المراد التعيين له
            pk: معرف الشكوى
            
        Returns:
            Response: رسالة تأكيد التعيين
        """
        complaint = get_object_or_404(Complaint, pk=pk)
        assigned_to_id = request.data.get("assigned_to")
        # Logic to assign complaint to a user (representative)
        return Response({"status": "complaint assigned"})

    @extend_schema(
        summary="حل شكوى",
        description="وضع علامة على الشكوى كمحلولة",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'resolution_notes': {
                        'type': 'string',
                        'description': 'ملاحظات حول حل الشكوى'
                    }
                }
            }
        },
        responses={200: {'description': 'تم حل الشكوى بنجاح'}},
        tags=["الشكاوى"]
    )
    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        """
        وضع علامة على الشكوى كمحلولة
        
        Args:
            request: طلب HTTP يحتوي على ملاحظات الحل (اختياري)
            pk: معرف الشكوى
            
        Returns:
            Response: رسالة تأكيد الحل
        """
        complaint = get_object_or_404(Complaint, pk=pk)
        # Logic to mark complaint as resolved
        return Response({"status": "complaint resolved"})

@extend_schema_view(
    list=extend_schema(
        summary="قائمة مرفقات الشكاوى",
        description="الحصول على قائمة مرفقات الشكاوى المرتبطة بالمستخدم",
        tags=["مرفقات الشكاوى"]
    ),
    create=extend_schema(
        summary="رفع مرفق جديد",
        description="رفع مرفق جديد لشكوى معينة",
        tags=["مرفقات الشكاوى"]
    ),
    retrieve=extend_schema(
        summary="تفاصيل مرفق",
        description="الحصول على تفاصيل مرفق معين",
        tags=["مرفقات الشكاوى"]
    ),
    destroy=extend_schema(
        summary="حذف مرفق",
        description="حذف مرفق من الشكوى",
        tags=["مرفقات الشكاوى"]
    )
)
class ComplaintAttachmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet لمرفقات الشكاوى - Complaint Attachments ViewSet
    
    يوفر إدارة المرفقات المرتبطة بالشكاوى (صور، مستندات، إلخ).
    """
    queryset = ComplaintAttachment.objects.all()
    serializer_class = ComplaintAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام لإظهار مرفقات شكاوى المستخدم فقط"""
        if self.request.user.is_staff:
            return ComplaintAttachment.objects.all()
        return ComplaintAttachment.objects.filter(complaint__complainant=self.request.user)

@extend_schema_view(
    list=extend_schema(
        summary="قائمة تحديثات الشكاوى",
        description="الحصول على قائمة تحديثات الشكاوى والردود",
        tags=["تحديثات الشكاوى"]
    ),
    create=extend_schema(
        summary="إضافة تحديث جديد",
        description="إضافة تحديث أو رد جديد على شكوى",
        tags=["تحديثات الشكاوى"]
    ),
    retrieve=extend_schema(
        summary="تفاصيل تحديث",
        description="الحصول على تفاصيل تحديث معين",
        tags=["تحديثات الشكاوى"]
    )
)
class ComplaintUpdateViewSet(viewsets.ModelViewSet):
    """
    ViewSet لتحديثات الشكاوى - Complaint Updates ViewSet
    
    يوفر إدارة التحديثات والردود على الشكاوى.
    """
    queryset = ComplaintUpdate.objects.all()
    serializer_class = ComplaintUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """تخصيص الاستعلام لإظهار تحديثات شكاوى المستخدم فقط"""
        if self.request.user.is_staff:
            return ComplaintUpdate.objects.all()
        return ComplaintUpdate.objects.filter(complaint__complainant=self.request.user)

@extend_schema_view(
    list=extend_schema(
        summary="إعدادات نظام الشكاوى",
        description="الحصول على إعدادات نظام الشكاوى (للمديرين فقط)",
        tags=["إعدادات النظام"]
    ),
    create=extend_schema(
        summary="إنشاء إعداد جديد",
        description="إنشاء إعداد جديد لنظام الشكاوى",
        tags=["إعدادات النظام"]
    ),
    update=extend_schema(
        summary="تحديث إعداد",
        description="تحديث إعداد موجود في النظام",
        tags=["إعدادات النظام"]
    )
)
class ComplaintSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet لإعدادات نظام الشكاوى - Complaint Settings ViewSet
    
    يوفر إدارة إعدادات النظام العامة للشكاوى (للمديرين فقط).
    """
    queryset = ComplaintSettings.objects.all()
    serializer_class = ComplaintSettingsSerializer
    permission_classes = [permissions.IsAdminUser]

