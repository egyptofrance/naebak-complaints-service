"""
أمر Django لتحميل البيانات الأساسية لخدمة الشكاوى
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.complaints.models import Governorate, ComplaintType, ComplaintSettings


class Command(BaseCommand):
    help = 'تحميل البيانات الأساسية لخدمة الشكاوى'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='إعادة تحميل البيانات حتى لو كانت موجودة',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        with transaction.atomic():
            # تحميل المحافظات
            self.load_governorates(force)
            
            # تحميل أنواع الشكاوى
            self.load_complaint_types(force)
            
            # تحميل الإعدادات الافتراضية
            self.load_default_settings(force)
        
        self.stdout.write(
            self.style.SUCCESS('تم تحميل البيانات الأساسية بنجاح!')
        )

    def load_governorates(self, force=False):
        """تحميل المحافظات المصرية"""
        governorates_data = [
            {"name": "القاهرة", "name_en": "Cairo", "code": "CAI", "display_order": 1},
            {"name": "الجيزة", "name_en": "Giza", "code": "GIZ", "display_order": 2},
            {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX", "display_order": 3},
            {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK", "display_order": 4},
            {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RSS", "display_order": 5},
            {"name": "البحيرة", "name_en": "Beheira", "code": "BEH", "display_order": 6},
            {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY", "display_order": 7},
            {"name": "الغربية", "name_en": "Gharbia", "code": "GHR", "display_order": 8},
            {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM", "display_order": 9},
            {"name": "المنوفية", "name_en": "Monufia", "code": "MNF", "display_order": 10},
            {"name": "المنيا", "name_en": "Minya", "code": "MNY", "display_order": 11},
            {"name": "القليوبية", "name_en": "Qalyubia", "code": "QLY", "display_order": 12},
            {"name": "الوادي الجديد", "name_en": "New Valley", "code": "WAD", "display_order": 13},
            {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI", "display_order": 14},
            {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI", "display_order": 15},
            {"name": "الشرقية", "name_en": "Sharqia", "code": "SHR", "display_order": 16},
            {"name": "سوهاج", "name_en": "Sohag", "code": "SOH", "display_order": 17},
            {"name": "السويس", "name_en": "Suez", "code": "SUZ", "display_order": 18},
            {"name": "أسوان", "name_en": "Aswan", "code": "ASW", "display_order": 19},
            {"name": "أسيوط", "name_en": "Asyut", "code": "ASY", "display_order": 20},
            {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS", "display_order": 21},
            {"name": "بورسعيد", "name_en": "Port Said", "code": "PTS", "display_order": 22},
            {"name": "دمياط", "name_en": "Damietta", "code": "DAM", "display_order": 23},
            {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS", "display_order": 24},
            {"name": "مطروح", "name_en": "Matrouh", "code": "MAT", "display_order": 25},
            {"name": "الأقصر", "name_en": "Luxor", "code": "LUX", "display_order": 26},
            {"name": "قنا", "name_en": "Qena", "code": "QEN", "display_order": 27}
        ]
        
        created_count = 0
        for gov_data in governorates_data:
            gov, created = Governorate.objects.get_or_create(
                code=gov_data['code'],
                defaults=gov_data
            )
            if created or force:
                if force and not created:
                    for key, value in gov_data.items():
                        setattr(gov, key, value)
                    gov.save()
                created_count += 1
        
        self.stdout.write(f'تم تحميل {created_count} محافظة')

    def load_complaint_types(self, force=False):
        """تحميل أنواع الشكاوى"""
        complaint_types_data = [
            {
                "name": "البنية التحتية والطرق",
                "name_en": "Infrastructure and Roads",
                "category": "infrastructure",
                "target_council": "parliament",
                "icon": "🛣️",
                "color": "#FF6B35",
                "estimated_resolution_days": 45,
                "requires_attachments": True,
                "priority_level": "medium",
                "display_order": 1
            },
            {
                "name": "الخدمات الصحية",
                "name_en": "Health Services", 
                "category": "health",
                "target_council": "parliament",
                "icon": "🏥",
                "color": "#28A745",
                "estimated_resolution_days": 30,
                "requires_attachments": False,
                "priority_level": "high",
                "display_order": 2
            },
            {
                "name": "التعليم والجامعات",
                "name_en": "Education and Universities",
                "category": "education", 
                "target_council": "parliament",
                "icon": "🎓",
                "color": "#007BFF",
                "estimated_resolution_days": 60,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 3
            },
            {
                "name": "الأمن والشرطة",
                "name_en": "Security and Police",
                "category": "security",
                "target_council": "parliament", 
                "icon": "🛡️",
                "color": "#DC3545",
                "estimated_resolution_days": 15,
                "requires_attachments": True,
                "priority_level": "urgent",
                "display_order": 4
            },
            {
                "name": "الخدمات العامة",
                "name_en": "Public Services",
                "category": "public_services",
                "target_council": "parliament",
                "icon": "🏛️", 
                "color": "#6F42C1",
                "estimated_resolution_days": 30,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 5
            },
            {
                "name": "النقل والمواصلات",
                "name_en": "Transportation",
                "category": "transportation",
                "target_council": "parliament",
                "icon": "🚌",
                "color": "#FFC107",
                "estimated_resolution_days": 45,
                "requires_attachments": True,
                "priority_level": "medium",
                "display_order": 6
            },
            {
                "name": "البيئة والنظافة",
                "name_en": "Environment and Cleanliness", 
                "category": "environment",
                "target_council": "parliament",
                "icon": "🌱",
                "color": "#20C997",
                "estimated_resolution_days": 30,
                "requires_attachments": True,
                "priority_level": "medium",
                "display_order": 7
            },
            {
                "name": "الإسكان والعقارات",
                "name_en": "Housing and Real Estate",
                "category": "housing",
                "target_council": "parliament",
                "icon": "🏠",
                "color": "#E83E8C",
                "estimated_resolution_days": 60,
                "requires_attachments": True,
                "priority_level": "medium",
                "display_order": 8
            },
            {
                "name": "العمل والتوظيف",
                "name_en": "Employment and Labor",
                "category": "employment",
                "target_council": "parliament",
                "icon": "💼",
                "color": "#17A2B8",
                "estimated_resolution_days": 45,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 9
            },
            {
                "name": "الشؤون الاجتماعية",
                "name_en": "Social Affairs",
                "category": "social",
                "target_council": "parliament",
                "icon": "👥",
                "color": "#6C757D",
                "estimated_resolution_days": 30,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 10
            },
            # أنواع شكاوى مجلس الشيوخ
            {
                "name": "القوانين والتشريعات",
                "name_en": "Laws and Legislation",
                "category": "legislation",
                "target_council": "senate",
                "icon": "⚖️",
                "color": "#6C757D",
                "estimated_resolution_days": 90,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 11
            },
            {
                "name": "الشؤون الدستورية",
                "name_en": "Constitutional Affairs", 
                "category": "constitutional",
                "target_council": "senate",
                "icon": "📜",
                "color": "#495057",
                "estimated_resolution_days": 120,
                "requires_attachments": False,
                "priority_level": "low",
                "display_order": 12
            },
            {
                "name": "السياسة الخارجية",
                "name_en": "Foreign Policy",
                "category": "foreign_policy", 
                "target_council": "senate",
                "icon": "🌍",
                "color": "#17A2B8",
                "estimated_resolution_days": 60,
                "requires_attachments": False,
                "priority_level": "medium",
                "display_order": 13
            },
            {
                "name": "الشؤون الاقتصادية",
                "name_en": "Economic Affairs",
                "category": "economic",
                "target_council": "senate",
                "icon": "💰",
                "color": "#28A745",
                "estimated_resolution_days": 75,
                "requires_attachments": False,
                "priority_level": "high",
                "display_order": 14
            }
        ]
        
        created_count = 0
        for type_data in complaint_types_data:
            complaint_type, created = ComplaintType.objects.get_or_create(
                name=type_data['name'],
                defaults=type_data
            )
            if created or force:
                if force and not created:
                    for key, value in type_data.items():
                        setattr(complaint_type, key, value)
                    complaint_type.save()
                created_count += 1
        
        self.stdout.write(f'تم تحميل {created_count} نوع شكوى')

    def load_default_settings(self, force=False):
        """تحميل الإعدادات الافتراضية"""
        settings = ComplaintSettings.get_settings()
        
        if force or not hasattr(settings, 'pk') or settings.pk is None:
            # تحديث الإعدادات بالقيم الافتراضية
            settings.max_complaints_per_day = 5
            settings.max_title_length = 200
            settings.max_description_length = 1500
            settings.max_files_per_complaint = 10
            settings.max_file_size_mb = 10
            settings.max_total_size_mb = 50
            settings.allowed_file_types = 'pdf,doc,docx,jpg,jpeg,png,gif'
            settings.auto_assign_enabled = True
            settings.auto_assign_by_location = True
            settings.auto_assign_by_type = True
            settings.send_email_notifications = True
            settings.send_sms_notifications = False
            settings.notify_on_status_change = True
            settings.notify_on_assignment = True
            settings.require_admin_approval = False
            settings.auto_moderate_content = True
            settings.block_offensive_language = True
            settings.allow_anonymous_complaints = False
            settings.require_phone_verification = True
            settings.save()
            
            self.stdout.write('تم تحميل الإعدادات الافتراضية')
        else:
            self.stdout.write('الإعدادات موجودة مسبقاً')
