"""
البيانات الأساسية لخدمة الشكاوى - مشروع نائبك
تم نقلها من مستودع المخزن المركزي
"""

# المحافظات المصرية (27 محافظة)
EGYPTIAN_GOVERNORATES = [
    {"name": "القاهرة", "name_en": "Cairo", "code": "CAI"},
    {"name": "الجيزة", "name_en": "Giza", "code": "GIZ"},
    {"name": "الإسكندرية", "name_en": "Alexandria", "code": "ALX"},
    {"name": "الدقهلية", "name_en": "Dakahlia", "code": "DAK"},
    {"name": "البحر الأحمر", "name_en": "Red Sea", "code": "RSS"},
    {"name": "البحيرة", "name_en": "Beheira", "code": "BEH"},
    {"name": "الفيوم", "name_en": "Fayoum", "code": "FAY"},
    {"name": "الغربية", "name_en": "Gharbia", "code": "GHR"},
    {"name": "الإسماعيلية", "name_en": "Ismailia", "code": "ISM"},
    {"name": "المنوفية", "name_en": "Monufia", "code": "MNF"},
    {"name": "المنيا", "name_en": "Minya", "code": "MNY"},
    {"name": "القليوبية", "name_en": "Qalyubia", "code": "QLY"},
    {"name": "الوادي الجديد", "name_en": "New Valley", "code": "WAD"},
    {"name": "شمال سيناء", "name_en": "North Sinai", "code": "NSI"},
    {"name": "جنوب سيناء", "name_en": "South Sinai", "code": "SSI"},
    {"name": "الشرقية", "name_en": "Sharqia", "code": "SHR"},
    {"name": "سوهاج", "name_en": "Sohag", "code": "SOH"},
    {"name": "السويس", "name_en": "Suez", "code": "SUZ"},
    {"name": "أسوان", "name_en": "Aswan", "code": "ASW"},
    {"name": "أسيوط", "name_en": "Asyut", "code": "ASY"},
    {"name": "بني سويف", "name_en": "Beni Suef", "code": "BNS"},
    {"name": "بورسعيد", "name_en": "Port Said", "code": "PTS"},
    {"name": "دمياط", "name_en": "Damietta", "code": "DAM"},
    {"name": "كفر الشيخ", "name_en": "Kafr El Sheikh", "code": "KFS"},
    {"name": "مطروح", "name_en": "Matrouh", "code": "MAT"},
    {"name": "الأقصر", "name_en": "Luxor", "code": "LUX"},
    {"name": "قنا", "name_en": "Qena", "code": "QEN"}
]

# أنواع الشكاوى لمجلس النواب
PARLIAMENT_COMPLAINT_TYPES = [
    {
        "name": "البنية التحتية والطرق",
        "name_en": "Infrastructure and Roads",
        "category": "infrastructure",
        "target_council": "parliament",
        "icon": "🛣️",
        "color": "#FF6B35",
        "estimated_resolution_days": 45,
        "requires_attachments": True,
        "priority_level": "medium"
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
        "priority_level": "high"
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
        "priority_level": "medium"
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
        "priority_level": "urgent"
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
        "priority_level": "medium"
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
        "priority_level": "medium"
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
        "priority_level": "medium"
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
        "priority_level": "medium"
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
        "priority_level": "medium"
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
        "priority_level": "medium"
    }
]

# أنواع الشكاوى لمجلس الشيوخ
SENATE_COMPLAINT_TYPES = [
    {
        "name": "القوانين والتشريعات",
        "name_en": "Laws and Legislation",
        "category": "legislation",
        "target_council": "senate",
        "icon": "⚖️",
        "color": "#6C757D",
        "estimated_resolution_days": 90,
        "requires_attachments": False,
        "priority_level": "medium"
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
        "priority_level": "low"
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
        "priority_level": "medium"
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
        "priority_level": "high"
    }
]

# حالات الشكاوى
COMPLAINT_STATUSES = [
    {"status": "pending", "name": "في الانتظار", "name_en": "Pending", "color": "#FFC107"},
    {"status": "under_review", "name": "قيد المراجعة", "name_en": "Under Review", "color": "#17A2B8"},
    {"status": "assigned", "name": "تم التعيين", "name_en": "Assigned", "color": "#007BFF"},
    {"status": "in_progress", "name": "قيد التنفيذ", "name_en": "In Progress", "color": "#6F42C1"},
    {"status": "resolved", "name": "تم الحل", "name_en": "Resolved", "color": "#28A745"},
    {"status": "rejected", "name": "مرفوضة", "name_en": "Rejected", "color": "#DC3545"},
    {"status": "closed", "name": "مغلقة", "name_en": "Closed", "color": "#6C757D"}
]

# أولويات الشكاوى
COMPLAINT_PRIORITIES = [
    {"priority": "low", "name": "منخفضة", "name_en": "Low", "color": "#28A745", "weight": 1},
    {"priority": "medium", "name": "متوسطة", "name_en": "Medium", "color": "#FFC107", "weight": 2},
    {"priority": "high", "name": "عالية", "name_en": "High", "color": "#FF6B35", "weight": 3},
    {"priority": "urgent", "name": "عاجلة", "name_en": "Urgent", "color": "#DC3545", "weight": 4}
]

# أنواع الملفات المسموحة
ALLOWED_FILE_TYPES = {
    "images": {
        "extensions": ["jpg", "jpeg", "png", "gif", "webp"],
        "max_size_mb": 5,
        "mime_types": ["image/jpeg", "image/png", "image/gif", "image/webp"]
    },
    "documents": {
        "extensions": ["pdf", "doc", "docx"],
        "max_size_mb": 10, 
        "mime_types": [
            "application/pdf", 
            "application/msword", 
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ]
    },
    "max_files_per_complaint": 10,
    "total_max_size_mb": 50
}

# إعدادات النظام الافتراضية
SYSTEM_SETTINGS = {
    "complaints": {
        "max_title_length": 200,
        "max_description_length": 1500,
        "max_files": 10,
        "max_file_size_mb": 10,
        "auto_assign_enabled": True,
        "auto_assign_by_location": True,
        "auto_assign_by_type": True,
        "require_phone_verification": True,
        "allow_anonymous_complaints": False
    },
    "notifications": {
        "send_email_notifications": True,
        "send_sms_notifications": False,
        "notify_on_status_change": True,
        "notify_on_assignment": True,
        "notify_on_resolution": True
    },
    "moderation": {
        "auto_moderate_content": True,
        "require_admin_approval": False,
        "block_offensive_language": True,
        "max_complaints_per_day": 5,
        "cooldown_period_hours": 24
    }
}

# رسائل النظام الافتراضية
SYSTEM_MESSAGES = {
    "complaint_submitted": "تم إرسال شكواك بنجاح. سيتم مراجعتها من قبل الإدارة خلال 24 ساعة",
    "complaint_assigned": "تم تعيين شكواك للنائب المختص. سيتم التواصل معك قريباً",
    "complaint_in_progress": "شكواك قيد المعالجة من قبل النائب المختص",
    "complaint_resolved": "تم حل شكواك بنجاح. يرجى تقييم الخدمة المقدمة",
    "complaint_rejected": "تم رفض شكواك. يرجى مراجعة أسباب الرفض والتواصل مع الإدارة",
    "file_upload_success": "تم رفع الملف بنجاح",
    "file_upload_error": "حدث خطأ في رفع الملف. يرجى المحاولة مرة أخرى",
    "invalid_file_type": "نوع الملف غير مدعوم. الأنواع المسموحة: PDF, DOC, DOCX, JPG, PNG",
    "file_too_large": "حجم الملف كبير جداً. الحد الأقصى المسموح: {max_size} ميجابايت",
    "max_files_exceeded": "تم تجاوز العدد الأقصى للملفات المسموح ({max_files} ملفات)",
    "complaint_limit_exceeded": "تم تجاوز العدد الأقصى للشكاوى المسموح يومياً ({max_per_day} شكاوى)"
}

# بيانات تجريبية للاختبار
SAMPLE_COMPLAINTS = [
    {
        "title": "تدهور حالة الطريق الرئيسي في منطقة المعادي",
        "description": "الطريق الرئيسي في منطقة المعادي يعاني من تدهور شديد مع وجود حفر كبيرة تسبب أضراراً للسيارات وتعرض السائقين للخطر. نطالب بإصلاح عاجل للطريق.",
        "complaint_type": "البنية التحتية والطرق",
        "governorate": "القاهرة",
        "city": "المعادي",
        "priority": "high",
        "status": "pending"
    },
    {
        "title": "نقص في الأطباء بمستشفى بنها العام",
        "description": "مستشفى بنها العام يعاني من نقص حاد في عدد الأطباء المتخصصين، مما يؤدي إلى طوابير طويلة وتأخير في تقديم الخدمات الطبية للمرضى.",
        "complaint_type": "الخدمات الصحية",
        "governorate": "القليوبية",
        "city": "بنها",
        "priority": "urgent",
        "status": "under_review"
    },
    {
        "title": "انقطاع متكرر للكهرباء في قرية كوم أمبو",
        "description": "تعاني قرية كوم أمبو من انقطاع متكرر للتيار الكهربائي خاصة في فصل الصيف، مما يؤثر على الحياة اليومية للمواطنين والأنشطة التجارية.",
        "complaint_type": "الخدمات العامة",
        "governorate": "أسوان",
        "city": "كوم أمبو",
        "priority": "medium",
        "status": "assigned"
    }
]

def get_complaint_types_by_council(council_type):
    """إرجاع أنواع الشكاوى حسب نوع المجلس"""
    if council_type == "parliament":
        return PARLIAMENT_COMPLAINT_TYPES
    elif council_type == "senate":
        return SENATE_COMPLAINT_TYPES
    else:
        return PARLIAMENT_COMPLAINT_TYPES + SENATE_COMPLAINT_TYPES

def get_governorate_by_name(name):
    """البحث عن محافظة بالاسم"""
    for gov in EGYPTIAN_GOVERNORATES:
        if gov["name"] == name or gov["name_en"] == name:
            return gov
    return None

def get_complaint_type_by_name(name, council_type=None):
    """البحث عن نوع شكوى بالاسم"""
    types = get_complaint_types_by_council(council_type) if council_type else (PARLIAMENT_COMPLAINT_TYPES + SENATE_COMPLAINT_TYPES)
    for complaint_type in types:
        if complaint_type["name"] == name or complaint_type["name_en"] == name:
            return complaint_type
    return None

def validate_file_upload(file_name, file_size_bytes, mime_type):
    """التحقق من صحة الملف المرفوع"""
    # التحقق من نوع الملف
    allowed_mimes = ALLOWED_FILE_TYPES["images"]["mime_types"] + ALLOWED_FILE_TYPES["documents"]["mime_types"]
    if mime_type not in allowed_mimes:
        return False, "نوع الملف غير مدعوم"
    
    # التحقق من حجم الملف
    file_size_mb = file_size_bytes / (1024 * 1024)
    if mime_type in ALLOWED_FILE_TYPES["images"]["mime_types"]:
        max_size = ALLOWED_FILE_TYPES["images"]["max_size_mb"]
    else:
        max_size = ALLOWED_FILE_TYPES["documents"]["max_size_mb"]
    
    if file_size_mb > max_size:
        return False, f"حجم الملف كبير جداً. الحد الأقصى: {max_size} ميجابايت"
    
    return True, "الملف صالح"
