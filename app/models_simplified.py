"""
نماذج الشكاوى المبسطة لتطبيق نائبك
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Complaint(models.Model):
    """
    نموذج الشكوى المبسط
    """
    
    class Status(models.TextChoices):
        PENDING = 'pending', _('في انتظار المراجعة')
        UNDER_REVIEW = 'under_review', _('قيد المراجعة')
        RESOLVED = 'resolved', _('تم الحل')
        REJECTED = 'rejected', _('مرفوض')
    
    class Category(models.TextChoices):
        INFRASTRUCTURE = 'infrastructure', _('البنية التحتية')
        HEALTH = 'health', _('الصحة')
        EDUCATION = 'education', _('التعليم')
        SECURITY = 'security', _('الأمن')
        SERVICES = 'services', _('الخدمات العامة')
        OTHER = 'other', _('أخرى')
    
    # بيانات المشتكي
    citizen_name = models.CharField(_('اسم المواطن'), max_length=200)
    citizen_email = models.EmailField(_('البريد الإلكتروني'))
    citizen_phone = models.CharField(_('رقم الهاتف'), max_length=15, blank=True)
    citizen_national_id = models.CharField(_('الرقم القومي'), max_length=14, blank=True)
    
    # بيانات الشكوى
    title = models.CharField(_('عنوان الشكوى'), max_length=200)
    content = models.TextField(_('محتوى الشكوى'), max_length=1500)
    category = models.CharField(
        _('فئة الشكوى'),
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    
    # الموقع
    governorate = models.CharField(_('المحافظة'), max_length=50)
    city = models.CharField(_('المدينة/المركز'), max_length=100, blank=True)
    address = models.TextField(_('العنوان التفصيلي'), max_length=300, blank=True)
    
    # الحالة
    status = models.CharField(
        _('حالة الشكوى'),
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    
    # التواريخ
    created_at = models.DateTimeField(_('تاريخ الإنشاء'), auto_now_add=True)
    updated_at = models.DateTimeField(_('تاريخ التحديث'), auto_now=True)
    resolved_at = models.DateTimeField(_('تاريخ الحل'), blank=True, null=True)
    
    # ملاحظات الإدارة
    admin_notes = models.TextField(_('ملاحظات الإدارة'), blank=True)
    assigned_to = models.CharField(_('مُحال إلى'), max_length=200, blank=True)
    
    class Meta:
        verbose_name = _('شكوى')
        verbose_name_plural = _('الشكاوى')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.citizen_name}"


class ComplaintFile(models.Model):
    """
    الملفات المرفقة مع الشكوى
    """
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('الشكوى')
    )
    
    file = models.FileField(
        _('الملف'),
        upload_to='complaints/files/%Y/%m/%d/'
    )
    
    original_name = models.CharField(_('اسم الملف الأصلي'), max_length=255)
    file_size = models.PositiveIntegerField(_('حجم الملف'))
    file_type = models.CharField(_('نوع الملف'), max_length=50)
    
    uploaded_at = models.DateTimeField(_('تاريخ الرفع'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('ملف مرفق')
        verbose_name_plural = _('الملفات المرفقة')
    
    def __str__(self):
        return f"{self.original_name} - {self.complaint.title}"


class ComplaintResponse(models.Model):
    """
    ردود الإدارة على الشكاوى
    """
    complaint = models.ForeignKey(
        Complaint,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_('الشكوى')
    )
    
    response_text = models.TextField(_('نص الرد'), max_length=1000)
    responder_name = models.CharField(_('اسم المجيب'), max_length=200)
    responder_title = models.CharField(_('منصب المجيب'), max_length=100, blank=True)
    
    created_at = models.DateTimeField(_('تاريخ الرد'), auto_now_add=True)
    is_public = models.BooleanField(_('رد عام'), default=True)
    
    class Meta:
        verbose_name = _('رد على الشكوى')
        verbose_name_plural = _('الردود على الشكاوى')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"رد على: {self.complaint.title}"
