"""
Serializers لخدمة الشكاوى - مشروع نائبك
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Governorate, ComplaintType, Complaint, 
    ComplaintAttachment, ComplaintUpdate, ComplaintSettings
)


class GovernorateSerializer(serializers.ModelSerializer):
    """Serializer للمحافظات"""
    
    class Meta:
        model = Governorate
        fields = ['id', 'name', 'name_en', 'code', 'is_active']
        read_only_fields = ['id']


class ComplaintTypeSerializer(serializers.ModelSerializer):
    """Serializer لأنواع الشكاوى"""
    
    resolution_rate = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintType
        fields = [
            'id', 'name', 'name_en', 'description', 'category',
            'target_council', 'priority_level', 'icon', 'color',
            'requires_attachments', 'max_attachments', 
            'estimated_resolution_days', 'is_active', 'is_public',
            'total_complaints', 'resolved_complaints', 
            'average_resolution_time', 'resolution_rate'
        ]
        read_only_fields = [
            'id', 'total_complaints', 'resolved_complaints', 
            'average_resolution_time', 'resolution_rate'
        ]
    
    def get_resolution_rate(self, obj):
        return obj.get_resolution_rate()


class ComplaintAttachmentSerializer(serializers.ModelSerializer):
    """Serializer لمرفقات الشكاوى"""
    
    file_size_mb = serializers.SerializerMethodField()
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ComplaintAttachment
        fields = [
            'id', 'file', 'file_name', 'file_size', 'file_size_mb',
            'file_type', 'mime_type', 'description', 'is_verified',
            'uploaded_at', 'file_url'
        ]
        read_only_fields = [
            'id', 'file_size', 'file_type', 'mime_type', 
            'is_verified', 'uploaded_at', 'file_size_mb', 'file_url'
        ]
    
    def get_file_size_mb(self, obj):
        return obj.get_file_size_mb()
    
    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
        return None


class ComplaintUpdateSerializer(serializers.ModelSerializer):
    """Serializer لتحديثات الشكاوى"""
    
    updated_by_name = serializers.CharField(source='updated_by.get_full_name', read_only=True)
    
    class Meta:
        model = ComplaintUpdate
        fields = [
            'id', 'update_type', 'title', 'description',
            'updated_by', 'updated_by_name', 'old_status', 'new_status',
            'notify_complainant', 'is_public', 'created_at'
        ]
        read_only_fields = ['id', 'updated_by_name', 'created_at']


class ComplaintListSerializer(serializers.ModelSerializer):
    """Serializer لقائمة الشكاوى (عرض مختصر)"""
    
    complainant_name = serializers.CharField(source='complainant.get_full_name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    governorate_name = serializers.CharField(source='governorate.name', read_only=True)
    complaint_type_name = serializers.CharField(source='complaint_type.name', read_only=True)
    complaint_type_icon = serializers.CharField(source='complaint_type.icon', read_only=True)
    complaint_type_color = serializers.CharField(source='complaint_type.color', read_only=True)
    status_color = serializers.SerializerMethodField()
    age_in_days = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    attachments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'complaint_number', 'title', 'priority', 'status',
            'complainant_name', 'assigned_to_name', 'governorate_name',
            'complaint_type_name', 'complaint_type_icon', 'complaint_type_color',
            'status_color', 'age_in_days', 'is_overdue', 'attachments_count',
            'created_at', 'updated_at', 'views_count'
        ]
    
    def get_status_color(self, obj):
        return obj.get_status_color()
    
    def get_age_in_days(self, obj):
        return obj.get_age_in_days()
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()
    
    def get_attachments_count(self, obj):
        return obj.attachments.count()


class ComplaintDetailSerializer(serializers.ModelSerializer):
    """Serializer لتفاصيل الشكوى الكاملة"""
    
    complainant_name = serializers.CharField(source='complainant.get_full_name', read_only=True)
    complainant_email = serializers.CharField(source='complainant.email', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)
    governorate_name = serializers.CharField(source='governorate.name', read_only=True)
    complaint_type_name = serializers.CharField(source='complaint_type.name', read_only=True)
    complaint_type_icon = serializers.CharField(source='complaint_type.icon', read_only=True)
    complaint_type_color = serializers.CharField(source='complaint_type.color', read_only=True)
    status_color = serializers.SerializerMethodField()
    age_in_days = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    
    attachments = ComplaintAttachmentSerializer(many=True, read_only=True)
    updates = ComplaintUpdateSerializer(many=True, read_only=True)
    
    class Meta:
        model = Complaint
        fields = [
            'id', 'complaint_number', 'title', 'description', 'priority', 'status',
            'complainant', 'complainant_name', 'complainant_email',
            'assigned_to', 'assigned_to_name', 'governorate', 'governorate_name',
            'city', 'district', 'detailed_location', 'contact_phone',
            'preferred_contact_time', 'complaint_type', 'complaint_type_name',
            'complaint_type_icon', 'complaint_type_color', 'admin_notes',
            'resolution_notes', 'complainant_satisfaction', 'satisfaction_comment',
            'is_public', 'is_anonymous', 'status_color', 'age_in_days',
            'is_overdue', 'created_at', 'updated_at', 'assigned_at',
            'resolved_at', 'views_count', 'updates_count', 'attachments', 'updates'
        ]
        read_only_fields = [
            'id', 'complaint_number', 'complainant', 'complainant_name',
            'complainant_email', 'assigned_to_name', 'governorate_name',
            'complaint_type_name', 'complaint_type_icon', 'complaint_type_color',
            'status_color', 'age_in_days', 'is_overdue', 'created_at',
            'updated_at', 'assigned_at', 'resolved_at', 'views_count',
            'updates_count', 'attachments', 'updates'
        ]
    
    def get_status_color(self, obj):
        return obj.get_status_color()
    
    def get_age_in_days(self, obj):
        return obj.get_age_in_days()
    
    def get_is_overdue(self, obj):
        return obj.is_overdue()


class ComplaintCreateSerializer(serializers.ModelSerializer):
    """Serializer لإنشاء شكوى جديدة"""
    
    class Meta:
        model = Complaint
        fields = [
            'title', 'description', 'complaint_type', 'priority',
            'governorate', 'city', 'district', 'detailed_location',
            'contact_phone', 'preferred_contact_time', 'is_public', 'is_anonymous'
        ]
    
    def validate_title(self, value):
        """التحقق من طول العنوان"""
        settings = ComplaintSettings.get_settings()
        if len(value) > settings.max_title_length:
            raise serializers.ValidationError(
                f'العنوان طويل جداً. الحد الأقصى {settings.max_title_length} حرف'
            )
        return value
    
    def validate_description(self, value):
        """التحقق من طول الوصف"""
        settings = ComplaintSettings.get_settings()
        if len(value) > settings.max_description_length:
            raise serializers.ValidationError(
                f'الوصف طويل جداً. الحد الأقصى {settings.max_description_length} حرف'
            )
        return value
    
    def validate(self, attrs):
        """التحقق من البيانات العامة"""
        # التحقق من نوع الشكوى
        complaint_type = attrs.get('complaint_type')
        if not complaint_type.is_active:
            raise serializers.ValidationError('نوع الشكوى غير متاح حالياً')
        
        # التحقق من المحافظة
        governorate = attrs.get('governorate')
        if not governorate.is_active:
            raise serializers.ValidationError('المحافظة غير متاحة حالياً')
        
        return attrs
    
    def create(self, validated_data):
        """إنشاء شكوى جديدة"""
        # إضافة المستخدم الحالي كمشتكي
        validated_data['complainant'] = self.context['request'].user
        
        # إنشاء الشكوى
        complaint = super().create(validated_data)
        
        # تحديث إحصائيات نوع الشكوى
        complaint.complaint_type.increment_complaint_count()
        
        return complaint


class ComplaintUpdateStatusSerializer(serializers.ModelSerializer):
    """Serializer لتحديث حالة الشكوى"""
    
    update_notes = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    notify_complainant = serializers.BooleanField(default=True)
    
    class Meta:
        model = Complaint
        fields = ['status', 'admin_notes', 'resolution_notes', 'update_notes', 'notify_complainant']
    
    def validate_status(self, value):
        """التحقق من صحة الحالة الجديدة"""
        current_status = self.instance.status
        
        # قواعد انتقال الحالات
        valid_transitions = {
            'pending': ['under_review', 'assigned', 'rejected'],
            'under_review': ['assigned', 'rejected', 'pending'],
            'assigned': ['in_progress', 'resolved', 'rejected'],
            'in_progress': ['resolved', 'assigned'],
            'resolved': ['closed'],
            'rejected': ['pending', 'under_review'],
            'closed': []  # لا يمكن تغيير الحالة من مغلقة
        }
        
        if value not in valid_transitions.get(current_status, []):
            raise serializers.ValidationError(
                f'لا يمكن تغيير الحالة من {current_status} إلى {value}'
            )
        
        return value
    
    def update(self, instance, validated_data):
        """تحديث حالة الشكوى مع إنشاء تحديث"""
        old_status = instance.status
        new_status = validated_data.get('status', old_status)
        update_notes = validated_data.pop('update_notes', '')
        notify_complainant = validated_data.pop('notify_complainant', True)
        
        # تحديث الشكوى
        instance = super().update(instance, validated_data)
        
        # إنشاء تحديث إذا تغيرت الحالة
        if old_status != new_status:
            ComplaintUpdate.objects.create(
                complaint=instance,
                update_type='status_change',
                title=f'تم تغيير حالة الشكوى إلى {instance.get_status_display()}',
                description=update_notes or f'تم تغيير الحالة من {old_status} إلى {new_status}',
                updated_by=self.context['request'].user,
                old_status=old_status,
                new_status=new_status,
                notify_complainant=notify_complainant
            )
            
            # تحديث عداد التحديثات
            instance.updates_count += 1
            instance.save(update_fields=['updates_count'])
            
            # تحديث إحصائيات نوع الشكوى إذا تم الحل
            if new_status == 'resolved':
                instance.complaint_type.increment_resolved_count()
        
        return instance


class ComplaintSettingsSerializer(serializers.ModelSerializer):
    """Serializer لإعدادات الشكاوى"""
    
    class Meta:
        model = ComplaintSettings
        fields = [
            'max_complaints_per_day', 'max_title_length', 'max_description_length',
            'max_files_per_complaint', 'max_file_size_mb', 'max_total_size_mb',
            'allowed_file_types', 'auto_assign_enabled', 'auto_assign_by_location',
            'auto_assign_by_type', 'send_email_notifications', 'send_sms_notifications',
            'notify_on_status_change', 'notify_on_assignment', 'require_admin_approval',
            'auto_moderate_content', 'block_offensive_language', 'allow_anonymous_complaints',
            'require_phone_verification', 'updated_at'
        ]
        read_only_fields = ['updated_at']


class ComplaintStatsSerializer(serializers.Serializer):
    """Serializer لإحصائيات الشكاوى"""
    
    total_complaints = serializers.IntegerField()
    pending_complaints = serializers.IntegerField()
    resolved_complaints = serializers.IntegerField()
    rejected_complaints = serializers.IntegerField()
    resolution_rate = serializers.FloatField()
    average_resolution_time = serializers.FloatField()
    complaints_by_type = serializers.DictField()
    complaints_by_governorate = serializers.DictField()
    complaints_by_status = serializers.DictField()
    complaints_by_priority = serializers.DictField()
    monthly_complaints = serializers.ListField()
    top_complaint_types = serializers.ListField()
    overdue_complaints = serializers.IntegerField()


class UserComplaintStatsSerializer(serializers.Serializer):
    """Serializer لإحصائيات شكاوى المستخدم"""
    
    total_submitted = serializers.IntegerField()
    pending = serializers.IntegerField()
    resolved = serializers.IntegerField()
    rejected = serializers.IntegerField()
    average_satisfaction = serializers.FloatField()
    recent_complaints = ComplaintListSerializer(many=True)
