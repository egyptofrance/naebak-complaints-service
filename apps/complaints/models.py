"""
نماذج خدمة الشكاوى - مشروع نائبك
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid


class Governorate(models.Model):
    """
    نموذج المحافظات المصرية - Egyptian Governorates Model
    
    يحتوي على جميع المحافظات المصرية الـ 27 مع معلوماتها الأساسية.
    يستخدم لتصنيف الشكاوى جغرافياً وتوجيهها للممثلين المناسبين.
    
    Attributes:
        name (CharField): اسم المحافظة بالعربية
        name_en (CharField): اسم المحافظة بالإنجليزية
        code (CharField): كود المحافظة الرسمي (3 أحرف)
        is_active (BooleanField): حالة تفعيل المحافظة
        display_order (PositiveIntegerField): ترتيب العرض في القوائم
        
    Business Logic:
        - تستخدم لتصنيف الشكاوى حسب المنطقة الجغرافية
        - تساعد في توجيه الشكاوى للممثلين المناسبين
        - يمكن إلغاء تفعيل محافظة مؤقتاً دون حذف بياناتها
        - ترتيب العرض يحدد أولوية ظهور المحافظات في القوائم
        
    Usage:
        - في نماذج تقديم الشكاوى لاختيار المحافظة
        - في تصفية الشكاوى حسب المنطقة
        - في إحصائيات الشكاوى الجغرافية
    """
    name = models.CharField('اسم المحافظة', max_length=50, unique=True)
    name_en = models.CharField('الاسم بالإنجليزية', max_length=50)
    code = models.CharField('الكود', max_length=3, unique=True)
    is_active = models.BooleanField('نشط', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    
    class Meta:
        db_table = 'governorates'
        verbose_name = 'محافظة'
        verbose_name_plural = 'المحافظات'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['code']),
        ]
    
    def __str__(self):
        return self.name


class ComplaintType(models.Model):
    """
    نموذج أنواع الشكاوى - Complaint Types Model
    
    يحدد أنواع الشكاوى المختلفة المتاحة في النظام مع تصنيفاتها وأولوياتها.
    يساعد في توجيه الشكاوى للجهات المختصة وتحديد مستوى الأولوية.
    
    Attributes:
        name (CharField): اسم نوع الشكوى بالعربية
        name_en (CharField): اسم نوع الشكوى بالإنجليزية
        description (TextField): وصف مفصل لنوع الشكوى
        category (CharField): التصنيف العام (بنية تحتية، صحة، تعليم، إلخ)
        target_council (CharField): المجلس المختص (نواب، شيوخ، أو كلاهما)
        priority_level (CharField): مستوى الأولوية الافتراضي
        icon (CharField): اسم الأيقونة للعرض في الواجهة
        
    Business Logic:
        - كل شكوى يجب أن تنتمي لنوع محدد
        - النوع يحدد المجلس المختص بالمتابعة
        - مستوى الأولوية يؤثر على ترتيب المعالجة
        - التصنيف يساعد في الإحصائيات والتقارير
        - الأيقونة تحسن تجربة المستخدم في الواجهة
        
    Categories:
        - infrastructure: البنية التحتية (طرق، مياه، كهرباء)
        - health: الصحة (مستشفيات، أدوية، خدمات طبية)
        - education: التعليم (مدارس، جامعات، مناهج)
        - security: الأمن (شرطة، أمن عام)
        - public_services: الخدمات العامة (بريد، اتصالات)
        - transportation: النقل والمواصلات
        - environment: البيئة (تلوث، نظافة)
        - housing: الإسكان (مشاريع إسكان، عقارات)
        - employment: العمل والتوظيف
        - social: الشؤون الاجتماعية
        - legislation: القوانين والتشريعات
        - constitutional: الشؤون الدستورية
        - foreign_policy: السياسة الخارجية
        - economic: الشؤون الاقتصادية
    """
    
    COUNCIL_CHOICES = [
        ('parliament', 'مجلس النواب'),
        ('senate', 'مجلس الشيوخ'),
        ('both', 'كلا المجلسين'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة'),
    ]
    
    CATEGORY_CHOICES = [
        ('infrastructure', 'البنية التحتية'),
        ('health', 'الصحة'),
        ('education', 'التعليم'),
        ('security', 'الأمن'),
        ('public_services', 'الخدمات العامة'),
        ('transportation', 'النقل والمواصلات'),
        ('environment', 'البيئة'),
        ('housing', 'الإسكان'),
        ('employment', 'العمل والتوظيف'),
        ('social', 'الشؤون الاجتماعية'),
        ('legislation', 'القوانين والتشريعات'),
        ('constitutional', 'الشؤون الدستورية'),
        ('foreign_policy', 'السياسة الخارجية'),
        ('economic', 'الشؤون الاقتصادية'),
    ]
    
    name = models.CharField('اسم النوع', max_length=100, unique=True)
    name_en = models.CharField('الاسم بالإنجليزية', max_length=100)
    description = models.TextField('الوصف', max_length=300, blank=True)
    
    category = models.CharField('التصنيف', max_length=50, choices=CATEGORY_CHOICES)
    target_council = models.CharField('المجلس المختص', max_length=20, choices=COUNCIL_CHOICES)
    priority_level = models.CharField('مستوى الأولوية', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    icon = models.CharField('الأيقونة', max_length=50, blank=True)
    color = models.CharField('اللون', max_length=7, default='#007BFF', help_text='كود اللون بصيغة hex')
    
    requires_attachments = models.BooleanField('يتطلب مرفقات', default=False)
    max_attachments = models.PositiveIntegerField('الحد الأقصى للمرفقات', default=5)
    estimated_resolution_days = models.PositiveIntegerField('الأيام المتوقعة للحل', default=30)
    
    is_active = models.BooleanField('نشط', default=True)
    is_public = models.BooleanField('ظاهر للمواطنين', default=True)
    display_order = models.PositiveIntegerField('ترتيب العرض', default=0)
    
    # إحصائيات
    total_complaints = models.PositiveIntegerField('إجمالي الشكاوى', default=0)
    resolved_complaints = models.PositiveIntegerField('الشكاوى المحلولة', default=0)
    average_resolution_time = models.FloatField('متوسط وقت الحل (بالأيام)', default=0.0)
    
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='أنشئ بواسطة')
    
    class Meta:
        db_table = 'complaint_types'
        verbose_name = 'نوع شكوى'
        verbose_name_plural = 'أنواع الشكاوى'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['target_council']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_resolution_rate(self):
        """حساب معدل الحل"""
        if self.total_complaints == 0:
            return 0
        return round((self.resolved_complaints / self.total_complaints) * 100, 2)
    
    def increment_complaint_count(self):
        """زيادة عداد الشكاوى"""
        self.total_complaints += 1
        self.save(update_fields=['total_complaints'])
    
    def increment_resolved_count(self):
        """زيادة عداد الشكاوى المحلولة"""
        self.resolved_complaints += 1
        self.save(update_fields=['resolved_complaints'])


class Complaint(models.Model):
    """
    نموذج الشكوى الرئيسي - Main Complaint Model
    
    النموذج الأساسي لإدارة الشكاوى في النظام. يحتوي على جميع المعلومات
    اللازمة لتتبع الشكوى من التقديم حتى الحل النهائي.
    
    Attributes:
        id (UUIDField): معرف فريد للشكوى (UUID)
        complaint_number (CharField): رقم الشكوى المرئي للمستخدمين
        title (CharField): عنوان الشكوى
        description (TextField): وصف مفصل للشكوى
        complaint_type (ForeignKey): نوع الشكوى
        priority (CharField): مستوى الأولوية
        complainant (ForeignKey): المستخدم مقدم الشكوى
        assigned_to (ForeignKey): المسؤول المعين للمتابعة
        governorate (ForeignKey): المحافظة المرتبطة بالشكوى
        city (CharField): المدينة
        district (CharField): الحي (اختياري)
        detailed_location (TextField): الموقع التفصيلي
        contact_phone (CharField): رقم التواصل
        status (CharField): حالة الشكوى الحالية
        admin_notes (TextField): ملاحظات الإدارة
        resolution_notes (TextField): ملاحظات الحل
        complainant_satisfaction (PositiveIntegerField): تقييم المشتكي (1-5)
        
    Status Flow (تدفق الحالات):
        1. pending: في الانتظار (الحالة الافتراضية)
        2. under_review: قيد المراجعة (بدء المراجعة الإدارية)
        3. assigned: تم التعيين (تعيين مسؤول للمتابعة)
        4. in_progress: قيد التنفيذ (بدء العمل على الحل)
        5. resolved: تم الحل (انتهاء المعالجة)
        6. rejected: مرفوضة (شكوى غير صالحة)
        7. closed: مغلقة (إغلاق نهائي)
        
    Business Logic:
        - كل شكوى لها رقم فريد يتم توليده تلقائياً
        - الأولوية تؤثر على ترتيب المعالجة
        - التعيين للمسؤولين يتم حسب المحافظة ونوع الشكوى
        - التقييم يتم بعد الحل من قبل المشتكي
        - الملاحظات الإدارية للاستخدام الداخلي فقط
        
    Security Considerations:
        - المشتكي يرى شكاواه فقط
        - المديرون يرون جميع الشكاوى
        - المسؤولون المعينون يرون الشكاوى المعينة لهم
        - معلومات التواصل محمية ولا تظهر للعامة
    """
    
    STATUS_CHOICES = [
        ('pending', 'في الانتظار'),
        ('under_review', 'قيد المراجعة'),
        ('assigned', 'تم التعيين'),
        ('in_progress', 'قيد التنفيذ'),
        ('resolved', 'تم الحل'),
        ('rejected', 'مرفوضة'),
        ('closed', 'مغلقة'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'منخفضة'),
        ('medium', 'متوسطة'),
        ('high', 'عالية'),
        ('urgent', 'عاجلة'),
    ]
    
    # معرف فريد للشكوى
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    complaint_number = models.CharField('رقم الشكوى', max_length=20, unique=True, blank=True)
    
    # البيانات الأساسية
    title = models.CharField('عنوان الشكوى', max_length=200)
    description = models.TextField('وصف الشكوى', max_length=1500)
    
    # التصنيف والنوع
    complaint_type = models.ForeignKey(ComplaintType, on_delete=models.PROTECT, verbose_name='نوع الشكوى')
    priority = models.CharField('الأولوية', max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # المواقع
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_complaints', verbose_name='المشتكي')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints', verbose_name='المعين إليه')
    
    # الموقع الجغرافي
    governorate = models.ForeignKey(Governorate, on_delete=models.PROTECT, verbose_name='المحافظة')
    city = models.CharField('المدينة', max_length=100)
    district = models.CharField('الحي', max_length=100, blank=True)
    detailed_location = models.TextField('الموقع التفصيلي', max_length=300, blank=True)
    
    # معلومات التواصل
    contact_phone = models.CharField(
        'رقم التواصل',
        max_length=15,
        blank=True,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'رقم الهاتف غير صحيح')]
    )
    preferred_contact_time = models.CharField('الوقت المفضل للتواصل', max_length=100, blank=True)
    
    # الحالة والمتابعة
    status = models.CharField('الحالة', max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField('ملاحظات الإدارة', max_length=1000, blank=True)
    resolution_notes = models.TextField('ملاحظات الحل', max_length=1000, blank=True)
    
    # التقييم
    complainant_satisfaction = models.PositiveIntegerField(
        'تقييم المشتكي',
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        null=True,
        blank=True,
        help_text='تقييم من 1 إلى 5'
    )
    satisfaction_comment = models.TextField('تعليق التقييم', max_length=500, blank=True)
    
    # إعدادات الخصوصية
    is_public = models.BooleanField('عامة', default=True, help_text='هل يمكن عرض الشكوى للعامة؟')
    is_anonymous = models.BooleanField('مجهولة', default=False, help_text='هل تريد إخفاء هويتك؟')
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    assigned_at = models.DateTimeField('تاريخ التعيين', null=True, blank=True)
    resolved_at = models.DateTimeField('تاريخ الحل', null=True, blank=True)
    
    # إحصائيات
    views_count = models.PositiveIntegerField('عدد المشاهدات', default=0)
    updates_count = models.PositiveIntegerField('عدد التحديثات', default=0)
    
    class Meta:
        db_table = 'complaints'
        verbose_name = 'شكوى'
        verbose_name_plural = 'الشكاوى'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['governorate']),
            models.Index(fields=['complaint_type']),
            models.Index(fields=['complainant']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.complaint_number} - {self.title[:50]}"
    
    def save(self, *args, **kwargs):
        # إنشاء رقم الشكوى تلقائياً
        if not self.complaint_number:
            year = timezone.now().year
            count = Complaint.objects.filter(created_at__year=year).count() + 1
            self.complaint_number = f"C{year}{count:06d}"
        
        # تحديث تاريخ التعيين
        if self.assigned_to and not self.assigned_at:
            self.assigned_at = timezone.now()
        
        # تحديث تاريخ الحل
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_age_in_days(self):
        """
        حساب عمر الشكوى بالأيام منذ تاريخ الإنشاء
        
        Returns:
            int: عدد الأيام منذ إنشاء الشكوى
            
        Usage:
            يستخدم في حساب الإحصائيات ومراقبة الأداء
            مفيد لتحديد الشكاوى المتأخرة
        """
        return (timezone.now() - self.created_at).days
    
    def is_overdue(self):
        """
        التحقق من تجاوز الشكوى للوقت المتوقع للحل
        
        Returns:
            bool: True إذا كانت الشكوى متأخرة، False إذا كانت في الوقت المحدد
            
        Business Logic:
            - الشكاوى المحلولة أو المغلقة لا تعتبر متأخرة
            - يتم المقارنة مع الوقت المتوقع للحل حسب نوع الشكوى
            - يساعد في تحديد أولويات المتابعة
        """
        if self.status in ['resolved', 'closed']:
            return False
        expected_days = self.complaint_type.estimated_resolution_days
        return self.get_age_in_days() > expected_days
    
    def get_status_color(self):
        """
        إرجاع لون الحالة للعرض في الواجهة
        
        Returns:
            str: كود اللون بصيغة HEX
            
        Color Scheme:
            - pending: أصفر (#FFC107) - في الانتظار
            - under_review: أزرق فاتح (#17A2B8) - قيد المراجعة  
            - assigned: أزرق (#007BFF) - تم التعيين
            - in_progress: بنفسجي (#6F42C1) - قيد التنفيذ
            - resolved: أخضر (#28A745) - تم الحل
            - rejected: أحمر (#DC3545) - مرفوضة
            - closed: رمادي (#6C757D) - مغلقة
        """
        colors = {
            'pending': '#FFC107',
            'under_review': '#17A2B8',
            'assigned': '#007BFF',
            'in_progress': '#6F42C1',
            'resolved': '#28A745',
            'rejected': '#DC3545',
            'closed': '#6C757D',
        }
        return colors.get(self.status, '#6C757D')
    
    def get_priority_weight(self):
        """
        إرجاع وزن الأولوية للترتيب والفلترة
        
        Returns:
            int: وزن الأولوية (1-4)
            
        Priority Weights:
            - low: 1 (أولوية منخفضة)
            - medium: 2 (أولوية متوسطة) - الافتراضي
            - high: 3 (أولوية عالية)
            - urgent: 4 (أولوية عاجلة)
            
        Usage:
            يستخدم في ترتيب الشكاوى حسب الأولوية
            مفيد في خوارزميات التعيين التلقائي
        """
        weights = {'low': 1, 'medium': 2, 'high': 3, 'urgent': 4}
        return weights.get(self.priority, 2)


class ComplaintAttachment(models.Model):
    """نموذج مرفقات الشكوى"""
    
    FILE_TYPE_CHOICES = [
        ('image', 'صورة'),
        ('document', 'مستند'),
        ('video', 'فيديو'),
        ('audio', 'صوت'),
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='attachments', verbose_name='الشكوى')
    
    # معلومات الملف
    file = models.FileField('الملف', upload_to='complaints/attachments/%Y/%m/')
    file_name = models.CharField('اسم الملف', max_length=255)
    file_size = models.PositiveIntegerField('حجم الملف (بايت)')
    file_type = models.CharField('نوع الملف', max_length=20, choices=FILE_TYPE_CHOICES)
    mime_type = models.CharField('نوع MIME', max_length=100)
    
    # وصف الملف
    description = models.TextField('وصف المرفق', max_length=200, blank=True)
    
    # الحالة
    is_verified = models.BooleanField('تم التحقق', default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='تم التحقق بواسطة')
    verified_at = models.DateTimeField('تاريخ التحقق', null=True, blank=True)
    
    # التواريخ
    uploaded_at = models.DateTimeField('تاريخ الرفع', auto_now_add=True)
    
    class Meta:
        db_table = 'complaint_attachments'
        verbose_name = 'مرفق شكوى'
        verbose_name_plural = 'مرفقات الشكاوى'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_number} - {self.file_name}"
    
    def get_file_size_mb(self):
        """حساب حجم الملف بالميجابايت"""
        return round(self.file_size / (1024 * 1024), 2)
    
    def is_image(self):
        """التحقق من كون الملف صورة"""
        return self.file_type == 'image'
    
    def is_document(self):
        """التحقق من كون الملف مستند"""
        return self.file_type == 'document'


class ComplaintUpdate(models.Model):
    """نموذج تحديثات الشكوى"""
    
    UPDATE_TYPE_CHOICES = [
        ('status_change', 'تغيير الحالة'),
        ('assignment', 'تعيين'),
        ('comment', 'تعليق'),
        ('resolution', 'حل'),
        ('rejection', 'رفض'),
    ]
    
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='updates', verbose_name='الشكوى')
    update_type = models.CharField('نوع التحديث', max_length=20, choices=UPDATE_TYPE_CHOICES)
    
    # محتوى التحديث
    title = models.CharField('عنوان التحديث', max_length=200)
    description = models.TextField('وصف التحديث', max_length=1000)
    
    # المستخدم المسؤول عن التحديث
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='محدث بواسطة')
    
    # الحالة السابقة والجديدة (للتتبع)
    old_status = models.CharField('الحالة السابقة', max_length=20, blank=True)
    new_status = models.CharField('الحالة الجديدة', max_length=20, blank=True)
    
    # إعدادات الإشعار
    notify_complainant = models.BooleanField('إشعار المشتكي', default=True)
    is_public = models.BooleanField('عام', default=True)
    
    # التواريخ
    created_at = models.DateTimeField('تاريخ الإنشاء', auto_now_add=True)
    
    class Meta:
        db_table = 'complaint_updates'
        verbose_name = 'تحديث شكوى'
        verbose_name_plural = 'تحديثات الشكاوى'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.complaint.complaint_number} - {self.title}"


class ComplaintSettings(models.Model):
    """نموذج إعدادات نظام الشكاوى"""
    
    # إعدادات عامة
    max_complaints_per_day = models.PositiveIntegerField('الحد الأقصى للشكاوى يومياً', default=5)
    max_title_length = models.PositiveIntegerField('الحد الأقصى لطول العنوان', default=200)
    max_description_length = models.PositiveIntegerField('الحد الأقصى لطول الوصف', default=1500)
    
    # إعدادات المرفقات
    max_files_per_complaint = models.PositiveIntegerField('الحد الأقصى للملفات', default=10)
    max_file_size_mb = models.PositiveIntegerField('الحد الأقصى لحجم الملف (ميجابايت)', default=10)
    max_total_size_mb = models.PositiveIntegerField('الحد الأقصى للحجم الإجمالي (ميجابايت)', default=50)
    allowed_file_types = models.TextField('أنواع الملفات المسموحة', default='pdf,doc,docx,jpg,jpeg,png,gif')
    
    # إعدادات التوجيه التلقائي
    auto_assign_enabled = models.BooleanField('التوجيه التلقائي مفعل', default=True)
    auto_assign_by_location = models.BooleanField('التوجيه حسب الموقع', default=True)
    auto_assign_by_type = models.BooleanField('التوجيه حسب النوع', default=True)
    
    # إعدادات الإشعارات
    send_email_notifications = models.BooleanField('إرسال إشعارات البريد', default=True)
    send_sms_notifications = models.BooleanField('إرسال إشعارات SMS', default=False)
    notify_on_status_change = models.BooleanField('إشعار عند تغيير الحالة', default=True)
    notify_on_assignment = models.BooleanField('إشعار عند التعيين', default=True)
    
    # إعدادات المراجعة
    require_admin_approval = models.BooleanField('يتطلب موافقة الإدارة', default=False)
    auto_moderate_content = models.BooleanField('المراجعة التلقائية للمحتوى', default=True)
    block_offensive_language = models.BooleanField('حظر الألفاظ المسيئة', default=True)
    
    # إعدادات الخصوصية
    allow_anonymous_complaints = models.BooleanField('السماح بالشكاوى المجهولة', default=False)
    require_phone_verification = models.BooleanField('يتطلب تحقق الهاتف', default=True)
    
    # التواريخ
    updated_at = models.DateTimeField('تاريخ التحديث', auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='محدث بواسطة')
    
    class Meta:
        db_table = 'complaint_settings'
        verbose_name = 'إعدادات الشكاوى'
        verbose_name_plural = 'إعدادات الشكاوى'
    
    def __str__(self):
        return f"إعدادات الشكاوى - آخر تحديث: {self.updated_at.strftime('%Y-%m-%d')}"
    
    @classmethod
    def get_settings(cls):
        """إرجاع الإعدادات الحالية أو إنشاء إعدادات افتراضية"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
