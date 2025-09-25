# 📋 LEADER - دليل خدمة الشكاوى الشامل

**اسم الخدمة:** naebak-complaints-service  
**المنفذ:** 8003  
**الإطار:** Django 4.2 + Django REST Framework  
**قاعدة البيانات:** PostgreSQL (للشكاوى والردود)  
**التخزين:** Google Cloud Storage (للمرفقات)  
**المعالجة:** Celery + Redis (للإشعارات والمهام)  

---

## 📋 **نظرة عامة شاملة على الخدمة**

### **🎯 الغرض الأساسي:**
خدمة الشكاوى هي **نظام تواصل مباشر** بين المواطنين والنواب عبر إدارة المنصة، حيث يقدم المواطن شكواه للإدارة التي تقوم بإسنادها للنائب المناسب، والذي بدوره يعمل على حلها ويحصل على نقاط تقييم لأدائه.

### **🔄 تدفق العمل الكامل:**
```
1. المواطن يقدم شكوى (1500 حرف + 10 مرفقات + رابط يوتيوب + اختيار نائب مفضل)
                                    ↓
2. الإدارة تراجع الشكوى في لوحة إدارة الشكاوى (خدمة الإدارة 8002)
                                    ↓
3. الإدارة تسند الشكوى لنائب محدد عبر زر "إسناد"
                                    ↓
4. النائب يستقبل إشعار (خدمة الإشعارات 8008) ويراجع الشكوى في لوحته
                                    ↓
5. النائب يختار: قبول / رفض / تعليق لمدة 3 أيام للدراسة
                                    ↓
6. إذا قبل: النائب يعمل على الحل ويكتب إفادة بما تم
                                    ↓
7. الإدارة ترد على المواطن بالحل والإفادة عبر نفس المنصة
                                    ↓
8. النائب يحصل على +1 نقطة تظهر في كارته وصفحته (خدمة الإحصائيات 8012)
```

### **🏛️ أهمية الخدمة في منصة نائبك:**
- **القلب النابض** للتفاعل بين المواطن والنائب
- **أداة المساءلة** الرئيسية للنواب
- **مقياس الأداء** من خلال نظام النقاط
- **جسر التواصل** المباشر والشفاف

---

## 👥 **أدوار المستخدمين والصلاحيات**

### **🏠 المواطن (Citizen):**
**الصلاحيات من المخزن:**
```json
{
  "role": "citizen",
  "permissions": [
    "submit_complaints",
    "view_own_complaints", 
    "track_complaint_status",
    "rate_solutions",
    "manage_own_profile"
  ],
  "required_fields": ["phone_number", "whatsapp_number", "governorate"],
  "complaint_limits": {
    "max_text_length": 1500,
    "max_attachments": 10,
    "youtube_links": 1
  }
}
```

**الوظائف:**
- تقديم شكوى جديدة مع جميع التفاصيل
- رفع مرفقات متعددة (صور، مستندات، فيديوهات، صوت)
- إضافة رابط يوتيوب توضيحي (اختياري)
- اختيار نائب مفضل من القائمة (اختياري)
- متابعة حالة الشكوى وتطوراتها
- تقييم الحل المقدم من النائب

### **⚙️ الإدارة (Admin):**
**الصلاحيات من المخزن:**
```json
{
  "role": "admin",
  "permissions": [
    "manage_all_complaints",
    "assign_complaints",
    "moderate_content",
    "reply_to_citizens",
    "view_statistics",
    "manage_representatives"
  ],
  "access_level": "full_system_access"
}
```

**الوظائف:**
- مراجعة جميع الشكاوى الواردة في لوحة الإدارة
- إسناد الشكاوى للنواب المناسبين
- متابعة تقدم النواب في حل الشكاوى
- الرد على المواطنين بنتائج الحلول
- إدارة نظام النقاط والتقييمات
- مراقبة أداء النواب وإحصائياتهم

### **🏛️ النائب (Representative):**
**الصلاحيات من المخزن:**
```json
{
  "role": "representative",
  "permissions": [
    "receive_assigned_complaints",
    "accept_reject_complaints",
    "suspend_complaints",
    "resolve_complaints",
    "write_resolution_statements",
    "manage_own_profile"
  ],
  "council_types": ["parliament", "senate"],
  "points_system": {
    "points_per_resolution": 1,
    "display_locations": ["representative_card", "profile_page", "achievements"]
  }
}
```

**الوظائف:**
- استقبال الشكاوى المسندة إليه
- قبول أو رفض أو تعليق الشكوى (3 أيام للدراسة)
- العمل على حل الشكاوى المقبولة
- كتابة إفادات مفصلة بالحلول المقدمة
- الحصول على نقاط تقييم لكل شكوى محلولة
- إدارة لوحة الشكاوى الخاصة به

---

## 📦 **البيانات الكاملة من المستودع المخزن**

### **🗺️ المحافظات المصرية (27 محافظة):**
```python
GOVERNORATES = [
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
```
**الاستخدام:** تحديد محافظة الشكوى، عرض النواب المتاحين، إحصائيات جغرافية

### **🎉 الأحزاب السياسية المصرية (16 حزب):**
```python
POLITICAL_PARTIES = [
    {"name": "حزب الوفد", "name_en": "Al-Wafd Party", "abbreviation": "الوفد"},
    {"name": "الحزب الوطني الديمقراطي", "name_en": "National Democratic Party", "abbreviation": "الوطني"},
    {"name": "حزب الغد", "name_en": "Al-Ghad Party", "abbreviation": "الغد"},
    {"name": "حزب التجمع الوطني التقدمي الوحدوي", "name_en": "National Progressive Unionist Party", "abbreviation": "التجمع"},
    {"name": "حزب الناصري", "name_en": "Nasserist Party", "abbreviation": "الناصري"},
    {"name": "حزب الكرامة", "name_en": "Al-Karama Party", "abbreviation": "الكرامة"},
    {"name": "حزب الوسط الجديد", "name_en": "New Wasat Party", "abbreviation": "الوسط"},
    {"name": "حزب الحرية المصري", "name_en": "Egyptian Freedom Party", "abbreviation": "الحرية"},
    {"name": "حزب المصريين الأحرار", "name_en": "Free Egyptians Party", "abbreviation": "المصريين الأحرار"},
    {"name": "حزب النور", "name_en": "Al-Nour Party", "abbreviation": "النور"},
    {"name": "حزب البناء والتنمية", "name_en": "Building and Development Party", "abbreviation": "البناء والتنمية"},
    {"name": "حزب الإصلاح والتنمية", "name_en": "Reform and Development Party", "abbreviation": "الإصلاح والتنمية"},
    {"name": "حزب مستقبل وطن", "name_en": "Future of a Nation Party", "abbreviation": "مستقبل وطن"},
    {"name": "حزب المؤتمر", "name_en": "Conference Party", "abbreviation": "المؤتمر"},
    {"name": "حزب الشعب الجمهوري", "name_en": "Republican People's Party", "abbreviation": "الشعب الجمهوري"},
    {"name": "مستقل", "name_en": "Independent", "abbreviation": "مستقل"}
]
```
**الاستخدام:** تصنيف النواب، إحصائيات حزبية، عرض الانتماء السياسي

### **📋 فئات الشكاوى (11 فئة):**
```python
COMPLAINT_CATEGORIES = [
    {
        "id": "infrastructure",
        "name": "البنية التحتية", 
        "name_en": "Infrastructure", 
        "icon": "🏗️",
        "description": "الطرق، الجسور، المرافق العامة",
        "priority_weight": 0.8
    },
    {
        "id": "health",
        "name": "الصحة", 
        "name_en": "Health", 
        "icon": "🏥",
        "description": "المستشفيات، المراكز الصحية، الأدوية",
        "priority_weight": 1.0
    },
    {
        "id": "education",
        "name": "التعليم", 
        "name_en": "Education", 
        "icon": "🎓",
        "description": "المدارس، الجامعات، جودة التعليم",
        "priority_weight": 0.9
    },
    {
        "id": "security",
        "name": "الأمن", 
        "name_en": "Security", 
        "icon": "🛡️",
        "description": "الأمن العام، السلامة، الحماية",
        "priority_weight": 1.0
    },
    {
        "id": "public_services",
        "name": "الخدمات العامة", 
        "name_en": "Public Services", 
        "icon": "🏛️",
        "description": "المصالح الحكومية، الخدمات الإدارية",
        "priority_weight": 0.7
    },
    {
        "id": "transportation",
        "name": "النقل والمواصلات", 
        "name_en": "Transportation", 
        "icon": "🚌",
        "description": "وسائل النقل، المترو، الأتوبيسات",
        "priority_weight": 0.6
    },
    {
        "id": "environment",
        "name": "البيئة", 
        "name_en": "Environment", 
        "icon": "🌱",
        "description": "التلوث، النظافة، المساحات الخضراء",
        "priority_weight": 0.5
    },
    {
        "id": "housing",
        "name": "الإسكان", 
        "name_en": "Housing", 
        "icon": "🏠",
        "description": "الإسكان الاجتماعي، العقارات، السكن",
        "priority_weight": 0.7
    },
    {
        "id": "employment",
        "name": "العمل والتوظيف", 
        "name_en": "Employment", 
        "icon": "💼",
        "description": "فرص العمل، البطالة، التدريب",
        "priority_weight": 0.8
    },
    {
        "id": "social_affairs",
        "name": "الشؤون الاجتماعية", 
        "name_en": "Social Affairs", 
        "icon": "👥",
        "description": "الرعاية الاجتماعية، المساعدات، كبار السن",
        "priority_weight": 0.6
    },
    {
        "id": "other",
        "name": "أخرى", 
        "name_en": "Other", 
        "icon": "📝",
        "description": "شكاوى أخرى غير مصنفة",
        "priority_weight": 0.3
    }
]
```
**الاستخدام:** تصنيف الشكاوى، إحصائيات الفئات، توزيع تلقائي للنواب

### **📊 حالات الشكوى (8 حالات):**
```python
COMPLAINT_STATUSES = [
    {
        "status": "submitted",
        "name": "مُقدمة",
        "name_en": "Submitted",
        "description": "تم تقديم الشكوى وهي في انتظار مراجعة الإدارة",
        "color": "#3498db",
        "icon": "📝",
        "is_active": True,
        "order": 1
    },
    {
        "status": "under_admin_review",
        "name": "قيد مراجعة الإدارة",
        "name_en": "Under Admin Review",
        "description": "الإدارة تراجع الشكوى قبل الإسناد",
        "color": "#f39c12",
        "icon": "👀",
        "is_active": True,
        "order": 2
    },
    {
        "status": "assigned",
        "name": "مُسندة",
        "name_en": "Assigned",
        "description": "تم إسناد الشكوى لنائب محدد",
        "color": "#9b59b6",
        "icon": "📤",
        "is_active": True,
        "order": 3
    },
    {
        "status": "accepted",
        "name": "مقبولة",
        "name_en": "Accepted",
        "description": "النائب قبل الشكوى وسيعمل على حلها",
        "color": "#2ecc71",
        "icon": "✅",
        "is_active": True,
        "order": 4
    },
    {
        "status": "rejected",
        "name": "مرفوضة",
        "name_en": "Rejected",
        "description": "النائب رفض الشكوى مع ذكر الأسباب",
        "color": "#e74c3c",
        "icon": "❌",
        "is_active": False,
        "order": 5
    },
    {
        "status": "suspended",
        "name": "معلقة للدراسة",
        "name_en": "Suspended",
        "description": "النائب علق الشكوى لمدة 3 أيام للدراسة",
        "color": "#95a5a6",
        "icon": "⏸️",
        "is_active": True,
        "duration_days": 3,
        "order": 6
    },
    {
        "status": "resolved",
        "name": "محلولة",
        "name_en": "Resolved",
        "description": "النائب حل الشكوى وقدم إفادة بالحل",
        "color": "#27ae60",
        "icon": "🎉",
        "is_active": False,
        "order": 7,
        "points_awarded": 1
    },
    {
        "status": "closed",
        "name": "مُغلقة",
        "name_en": "Closed",
        "description": "الإدارة ردت على المواطن وأغلقت الشكوى",
        "color": "#34495e",
        "icon": "🔒",
        "is_active": False,
        "order": 8
    }
]
```
**الاستخدام:** تتبع دورة حياة الشكوى، إحصائيات الحالات، واجهة المستخدم

### **📊 أولويات الشكاوى (4 مستويات):**
```python
COMPLAINT_PRIORITIES = [
    {
        "priority": "low",
        "name": "منخفضة",
        "name_en": "Low",
        "color": "#28A745",
        "icon": "🟢",
        "response_time_hours": 168,  # أسبوع
        "weight": 0.25
    },
    {
        "priority": "medium",
        "name": "متوسطة",
        "name_en": "Medium",
        "color": "#FFC107",
        "icon": "🟡",
        "response_time_hours": 72,   # 3 أيام
        "weight": 0.5
    },
    {
        "priority": "high",
        "name": "عالية",
        "name_en": "High",
        "color": "#FF6B35",
        "icon": "🟠",
        "response_time_hours": 24,   # يوم واحد
        "weight": 0.75
    },
    {
        "priority": "urgent",
        "name": "عاجلة",
        "name_en": "Urgent",
        "color": "#DC3545",
        "icon": "🔴",
        "response_time_hours": 6,    # 6 ساعات
        "weight": 1.0
    }
]
```
**الاستخدام:** ترتيب الشكاوى، تحديد أوقات الاستجابة، التنبيهات

### **📁 أنواع الملفات المدعومة:**
```python
SUPPORTED_FILE_TYPES = {
    "images": {
        "extensions": ["jpg", "jpeg", "png", "gif", "webp"],
        "max_size_mb": 5,
        "mime_types": [
            "image/jpeg", 
            "image/png", 
            "image/gif", 
            "image/webp"
        ],
        "description": "صور توضيحية للمشكلة"
    },
    "documents": {
        "extensions": ["pdf", "doc", "docx", "txt"],
        "max_size_mb": 10,
        "mime_types": [
            "application/pdf",
            "application/msword",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "text/plain"
        ],
        "description": "مستندات ووثائق داعمة"
    },
    "videos": {
        "extensions": ["mp4", "avi", "mov", "webm"],
        "max_size_mb": 50,
        "mime_types": [
            "video/mp4",
            "video/avi", 
            "video/quicktime",
            "video/webm"
        ],
        "description": "فيديوهات توضيحية"
    },
    "audio": {
        "extensions": ["mp3", "wav", "m4a"],
        "max_size_mb": 10,
        "mime_types": [
            "audio/mpeg",
            "audio/wav",
            "audio/mp4"
        ],
        "description": "تسجيلات صوتية"
    },
    "limits": {
        "max_files_per_complaint": 10,
        "total_max_size_mb": 50
    }
}
```
**الاستخدام:** التحقق من صحة الملفات، رفع المرفقات، التخزين

### **🎬 التحقق من روابط اليوتيوب:**
```python
YOUTUBE_LINK_VALIDATION = {
    "required": False,
    "max_links": 1,
    "accepted_formats": [
        "https://www.youtube.com/watch?v=VIDEO_ID",
        "https://youtu.be/VIDEO_ID",
        "https://m.youtube.com/watch?v=VIDEO_ID"
    ],
    "validation_regex": r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|m\.youtube\.com/watch\?v=)[\w-]+",
    "embed_template": "https://www.youtube.com/embed/{video_id}",
    "thumbnail_template": "https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
}
```
**الاستخدام:** التحقق من صحة الروابط، عرض الفيديوهات، الصور المصغرة

### **👥 أنواع المستخدمين (4 أنواع):**
```python
USER_TYPES = [
    {
        "type": "citizen", 
        "name": "مواطن", 
        "name_en": "Citizen",
        "description": "مواطن له صوت انتخابي",
        "required_fields": ["phone_number", "whatsapp_number", "governorate"],
        "permissions": ["submit_complaints", "view_own_complaints", "rate_solutions"]
    },
    {
        "type": "candidate", 
        "name": "مرشح", 
        "name_en": "Candidate",
        "description": "مرشح لعضوية مجلس الشيوخ أو النواب",
        "required_fields": ["phone_number", "whatsapp_number", "governorate", "council_type", "party"],
        "permissions": ["receive_complaints", "resolve_complaints", "manage_profile"]
    },
    {
        "type": "current_member", 
        "name": "عضو حالي", 
        "name_en": "Current Member",
        "description": "عضو فعلي في مجلس الشيوخ أو النواب",
        "required_fields": ["phone_number", "whatsapp_number", "governorate", "council_type", "party"],
        "permissions": ["receive_complaints", "resolve_complaints", "manage_profile"]
    },
    {
        "type": "admin", 
        "name": "إدارة", 
        "name_en": "Admin",
        "description": "إدارة النظام",
        "required_fields": ["phone_number"],
        "permissions": ["manage_all_complaints", "assign_complaints", "moderate_content"]
    }
]
```
**الاستخدام:** تحديد الصلاحيات، التحقق من البيانات، إدارة المستخدمين

### **🏛️ أنواع المجالس (2 نوع):**
```python
COUNCIL_TYPES = [
    {
        "type": "parliament", 
        "name": "مجلس النواب", 
        "name_en": "Parliament",
        "description": "المجلس الأساسي للتشريع",
        "term_duration": 5,
        "total_seats": 596,
        "complaint_handling_priority": 1
    },
    {
        "type": "senate", 
        "name": "مجلس الشيوخ", 
        "name_en": "Senate",
        "description": "المجلس الاستشاري العلوي", 
        "term_duration": 5,
        "total_seats": 300,
        "complaint_handling_priority": 2
    }
]
```
**الاستخدام:** تصنيف النواب، إحصائيات المجالس، توزيع الشكاوى

### **🏆 نظام النقاط والإنجازات:**
```python
POINTS_SYSTEM = {
    "complaint_resolved": {
        "points": 1,
        "description": "نقطة واحدة لكل شكوى محلولة بنجاح"
    },
    "display_locations": [
        {
            "location": "representative_card",
            "description": "كارت النائب في متصفح المرشحين",
            "format": "إجمالي النقاط: {points}"
        },
        {
            "location": "representative_profile",
            "description": "صفحة النائب الرئيسية",
            "format": "الشكاوى المحلولة: {points}"
        },
        {
            "location": "achievements_section",
            "description": "قسم الإنجازات",
            "format": "{points} شكوى محلولة"
        }
    ],
    "calculation_formula": "total_resolved_complaints = total_points",
    "leaderboard_enabled": True,
    "monthly_reset": False
}
```
**الاستخدام:** تحفيز النواب، قياس الأداء، التصنيفات

### **🔔 أنواع الإشعارات (6 أنواع):**
```python
NOTIFICATION_TYPES = [
    {
        "type": "complaint_assigned",
        "name": "شكوى جديدة مسندة",
        "name_en": "New Complaint Assigned",
        "icon": "📋",
        "priority": "high",
        "recipients": ["representative"]
    },
    {
        "type": "complaint_resolved",
        "name": "تم حل الشكوى",
        "name_en": "Complaint Resolved",
        "icon": "✅",
        "priority": "medium",
        "recipients": ["admin", "citizen"]
    },
    {
        "type": "complaint_rejected",
        "name": "تم رفض الشكوى",
        "name_en": "Complaint Rejected",
        "icon": "❌",
        "priority": "medium",
        "recipients": ["admin", "citizen"]
    },
    {
        "type": "suspension_expired",
        "name": "انتهت فترة التعليق",
        "name_en": "Suspension Expired",
        "icon": "⏰",
        "priority": "high",
        "recipients": ["representative", "admin"]
    },
    {
        "type": "admin_reply",
        "name": "رد من الإدارة",
        "name_en": "Admin Reply",
        "icon": "💬",
        "priority": "medium",
        "recipients": ["citizen"]
    },
    {
        "type": "points_awarded",
        "name": "تم منح نقاط",
        "name_en": "Points Awarded",
        "icon": "🏆",
        "priority": "low",
        "recipients": ["representative"]
    }
]
```
**الاستخدام:** إشعار المستخدمين، تتبع الأحداث، التفاعل

### **🌟 رسائل النظام الافتراضية:**
```python
SYSTEM_MESSAGES = {
    "complaint_submitted": "تم إرسال شكواك بنجاح. سيتم مراجعتها من قبل الإدارة خلال 24 ساعة",
    "complaint_assigned": "تم إسناد شكوى جديدة إليك. يرجى مراجعتها في أقرب وقت",
    "complaint_accepted": "تم قبول الشكوى. سيتم العمل على حلها في أقرب وقت",
    "complaint_rejected": "تم رفض الشكوى. يرجى مراجعة الأسباب المذكورة",
    "complaint_suspended": "تم تعليق الشكوى لمدة 3 أيام للدراسة",
    "complaint_resolved": "تم حل الشكوى بنجاح. شكراً لك على صبرك",
    "points_awarded": "تهانينا! تم منحك نقطة جديدة لحل الشكوى",
    "admin_reply_sent": "تم إرسال الرد للمواطن بنجاح"
}
```
**الاستخدام:** رسائل تأكيد، إشعارات المستخدمين، واجهة المستخدم

---

## 🌐 **العلاقات مع الخدمات الأخرى**

### **🔗 الخدمات المتفاعلة:**

#### **📨 الخدمات المرسلة إليها:**
1. **خدمة المصادقة (8001):**
   - التحقق من هوية مقدم الشكوى
   - التحقق من صلاحيات النائب والأدمن
   - الحصول على بيانات المستخدم الكاملة

2. **خدمة عداد الزوار (8006):**
   - تتبع زيارات صفحات الشكاوى
   - إحصائيات استخدام النظام

#### **📤 الخدمات المستقبلة منها:**
1. **خدمة الإدارة (8002):**
   - لوحة إدارة الشكاوى للأدمن
   - أدوات الإسناد والمتابعة
   - تقارير الأداء

2. **خدمة الإشعارات (8008):**
   - إشعار النائب بالشكوى الجديدة
   - إشعار المواطن بتطورات الشكوى
   - تنبيهات انتهاء فترات التعليق

3. **خدمة الإحصائيات (8012):**
   - إرسال بيانات النقاط المكتسبة
   - إحصائيات الشكاوى المحلولة
   - تحليلات أداء النواب

4. **خدمة التقييمات (8005):**
   - تقييم المواطنين للحلول المقدمة
   - تقييم أداء النواب
   - نظام التقييم الشامل

### **📊 تدفق البيانات التفصيلي:**
```
المواطن → تقديم شكوى → خدمة الشكاوى (8003)
                              ↓
خدمة المصادقة (8001) ← التحقق من الهوية
                              ↓
خدمة الإدارة (8002) ← عرض في لوحة الإدارة
                              ↓
الأدمن → إسناد الشكوى → خدمة الشكاوى (8003)
                              ↓
خدمة الإشعارات (8008) ← إشعار النائب
                              ↓
النائب → قبول/رفض/تعليق → خدمة الشكاوى (8003)
                              ↓
النائب → حل الشكوى → خدمة الشكاوى (8003)
                              ↓
خدمة الإحصائيات (8012) ← +1 نقطة للنائب
                              ↓
خدمة التقييمات (8005) ← تقييم الحل
                              ↓
الأدمن → رد على المواطن → خدمة الشكاوى (8003)
                              ↓
خدمة الإشعارات (8008) ← إشعار المواطن بالحل
```

---

## ⚙️ **إعدادات Google Cloud Run الكاملة**

### **🛠️ بيئة التطوير (Development):**
```yaml
service_name: naebak-complaints-service-dev
image: gcr.io/naebak-472518/complaints-service:dev
region: us-central1
platform: managed

resources:
  cpu: 0.5
  memory: 512Mi
  
scaling:
  min_instances: 0
  max_instances: 3
  concurrency: 100
  
timeout: 300s
port: 8003

environment_variables:
  # Django Settings
  - DJANGO_SETTINGS_MODULE=app.settings.development
  - DEBUG=true
  - SECRET_KEY=${SECRET_KEY_DEV}
  
  # Database
  - DATABASE_URL=postgresql://localhost:5432/naebak_complaints_dev
  - DB_HOST=localhost
  - DB_PORT=5432
  - DB_NAME=naebak_complaints_dev
  - DB_USER=naebak_dev
  - DB_PASSWORD=${DB_PASSWORD_DEV}
  
  # Redis
  - REDIS_URL=redis://localhost:6379/2
  - REDIS_HOST=localhost
  - REDIS_PORT=6379
  - REDIS_DB=2
  
  # Google Cloud Storage
  - GCS_BUCKET_NAME=naebak-complaints-dev
  - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-dev.json
  
  # File Upload Settings
  - MAX_TEXT_LENGTH=1500
  - MAX_ATTACHMENTS=10
  - MAX_FILE_SIZE_MB=50
  - TOTAL_MAX_SIZE_MB=50
  - ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,webp,pdf,doc,docx,txt,mp4,avi,mov,webm,mp3,wav,m4a
  
  # Complaint Settings
  - SUSPENSION_DAYS=3
  - POINTS_PER_RESOLUTION=1
  - AUTO_ASSIGN_ENABLED=false
  - PRIORITY_CALCULATION_ENABLED=true
  
  # External Services
  - AUTH_SERVICE_URL=http://localhost:8001
  - ADMIN_SERVICE_URL=http://localhost:8002
  - NOTIFICATIONS_SERVICE_URL=http://localhost:8008
  - STATISTICS_SERVICE_URL=http://localhost:8012
  - RATINGS_SERVICE_URL=http://localhost:8005
  
  # Notification Settings
  - NOTIFICATION_WEBHOOK_URL=${NOTIFICATION_WEBHOOK_DEV}
  - EMAIL_NOTIFICATIONS_ENABLED=false
  - SMS_NOTIFICATIONS_ENABLED=false
  
  # Celery Settings
  - CELERY_BROKER_URL=redis://localhost:6379/3
  - CELERY_RESULT_BACKEND=redis://localhost:6379/3
  - CELERY_TASK_ALWAYS_EAGER=true
```

### **🏭 بيئة الإنتاج (Production):**
```yaml
service_name: naebak-complaints-service
image: gcr.io/naebak-472518/complaints-service:latest
region: us-central1
platform: managed

resources:
  cpu: 1
  memory: 1Gi
  
scaling:
  min_instances: 1
  max_instances: 10
  concurrency: 500
  
timeout: 120s
port: 8003

environment_variables:
  # Django Settings
  - DJANGO_SETTINGS_MODULE=app.settings.production
  - DEBUG=false
  - SECRET_KEY=${SECRET_KEY_PROD}
  - ALLOWED_HOSTS=naebak.com,*.naebak.com
  
  # Database
  - DATABASE_URL=${DATABASE_URL_PROD}
  - DB_HOST=${DB_HOST_PROD}
  - DB_PORT=5432
  - DB_NAME=naebak_complaints_prod
  - DB_USER=${DB_USER_PROD}
  - DB_PASSWORD=${DB_PASSWORD_PROD}
  - DB_SSL_MODE=require
  
  # Redis
  - REDIS_URL=${REDIS_URL_PROD}
  - REDIS_HOST=${REDIS_HOST_PROD}
  - REDIS_PORT=6379
  - REDIS_DB=2
  - REDIS_SSL=true
  
  # Google Cloud Storage
  - GCS_BUCKET_NAME=naebak-complaints-prod
  - GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account-prod.json
  - CDN_URL=https://cdn.naebak.com/complaints/
  - MEDIA_URL=https://storage.googleapis.com/naebak-complaints-prod/
  
  # File Upload Settings
  - MAX_TEXT_LENGTH=1500
  - MAX_ATTACHMENTS=10
  - MAX_FILE_SIZE_MB=50
  - TOTAL_MAX_SIZE_MB=50
  - ALLOWED_FILE_TYPES=jpg,jpeg,png,gif,webp,pdf,doc,docx,txt,mp4,avi,mov,webm,mp3,wav,m4a
  
  # Complaint Settings
  - SUSPENSION_DAYS=3
  - POINTS_PER_RESOLUTION=1
  - AUTO_ASSIGN_ENABLED=true
  - PRIORITY_CALCULATION_ENABLED=true
  
  # External Services
  - AUTH_SERVICE_URL=https://auth.naebak.com
  - ADMIN_SERVICE_URL=https://admin.naebak.com
  - NOTIFICATIONS_SERVICE_URL=https://notifications.naebak.com
  - STATISTICS_SERVICE_URL=https://statistics.naebak.com
  - RATINGS_SERVICE_URL=https://ratings.naebak.com
  
  # Notification Settings
  - NOTIFICATION_WEBHOOK_URL=${NOTIFICATION_WEBHOOK_PROD}
  - EMAIL_NOTIFICATIONS_ENABLED=true
  - SMS_NOTIFICATIONS_ENABLED=true
  - FIREBASE_CREDENTIALS=${FIREBASE_CREDENTIALS_PROD}
  
  # Celery Settings
  - CELERY_BROKER_URL=${REDIS_URL_PROD}/3
  - CELERY_RESULT_BACKEND=${REDIS_URL_PROD}/3
  - CELERY_TASK_ALWAYS_EAGER=false
  - CELERY_WORKER_CONCURRENCY=4
  
  # Security Settings
  - SECURE_SSL_REDIRECT=true
  - SECURE_HSTS_SECONDS=31536000
  - SECURE_CONTENT_TYPE_NOSNIFF=true
  - SECURE_BROWSER_XSS_FILTER=true
  - SESSION_COOKIE_SECURE=true
  - CSRF_COOKIE_SECURE=true
  
  # Monitoring
  - SENTRY_DSN=${SENTRY_DSN_PROD}
  - GOOGLE_CLOUD_MONITORING_ENABLED=true
```

### **🧪 بيئة الاختبار (Testing):**
```yaml
service_name: naebak-complaints-service-test
image: gcr.io/naebak-472518/complaints-service:test

resources:
  cpu: 0.3
  memory: 256Mi
  
scaling:
  min_instances: 0
  max_instances: 2
  
environment_variables:
  - DJANGO_SETTINGS_MODULE=app.settings.testing
  - DATABASE_URL=sqlite:///test_complaints.db
  - REDIS_URL=redis://localhost:6379/9
  - GCS_BUCKET_NAME=naebak-complaints-test
  - CELERY_TASK_ALWAYS_EAGER=true
  - EMAIL_NOTIFICATIONS_ENABLED=false
  - SMS_NOTIFICATIONS_ENABLED=false
```

---

## 🔐 **الأمان والحماية الشاملة**

### **🛡️ آليات الحماية (7 مستويات):**

1. **Authentication & Authorization:**
   ```python
   SECURITY_SETTINGS = {
       "authentication_required": True,
       "jwt_token_validation": True,
       "session_based_auth": True,
       "role_based_permissions": True,
       "api_key_validation": True
   }
   ```

2. **File Upload Security:**
   ```python
   FILE_SECURITY = {
       "file_type_validation": True,
       "file_size_limits": True,
       "virus_scanning": True,
       "malware_detection": True,
       "content_type_verification": True,
       "filename_sanitization": True
   }
   ```

3. **Rate Limiting:**
   ```python
   RATE_LIMITS = {
       "complaints_per_user_per_day": 5,
       "attachments_per_hour": 20,
       "api_requests_per_minute": 100,
       "failed_login_attempts": 5
   }
   ```

4. **Content Moderation:**
   ```python
   CONTENT_MODERATION = {
       "profanity_filter": True,
       "spam_detection": True,
       "inappropriate_content_detection": True,
       "automated_flagging": True,
       "manual_review_queue": True
   }
   ```

5. **Data Privacy:**
   ```python
   PRIVACY_SETTINGS = {
       "personal_data_encryption": True,
       "gdpr_compliance": True,
       "data_anonymization": True,
       "right_to_be_forgotten": True,
       "audit_logging": True
   }
   ```

6. **Input Validation:**
   ```python
   INPUT_VALIDATION = {
       "sql_injection_prevention": True,
       "xss_protection": True,
       "csrf_protection": True,
       "input_sanitization": True,
       "parameter_validation": True
   }
   ```

7. **Infrastructure Security:**
   ```python
   INFRASTRUCTURE_SECURITY = {
       "https_only": True,
       "secure_headers": True,
       "cors_configuration": True,
       "firewall_rules": True,
       "ddos_protection": True
   }
   ```

---

## 🔗 **واجهات برمجة التطبيقات (APIs) الكاملة**

### **📡 نقاط النهاية الأساسية (15 API):**
```
# Complaint Management
POST /api/complaints/submit/                    - تقديم شكوى جديدة (مواطن)
GET  /api/complaints/                           - قائمة الشكاوى (أدمن/نائب)
GET  /api/complaints/{id}/                      - تفاصيل شكوى محددة
PUT  /api/complaints/{id}/                      - تحديث الشكوى (أدمن)
DELETE /api/complaints/{id}/                    - حذف الشكوى (أدمن)

# Assignment & Status Management
PUT  /api/complaints/{id}/assign/               - إسناد شكوى لنائب (أدمن)
PUT  /api/complaints/{id}/accept/               - قبول الشكوى (نائب)
PUT  /api/complaints/{id}/reject/               - رفض الشكوى (نائب)
PUT  /api/complaints/{id}/suspend/              - تعليق الشكوى 3 أيام (نائب)
PUT  /api/complaints/{id}/resolve/              - حل الشكوى + إفادة (نائب)

# Communication
POST /api/complaints/{id}/admin-reply/          - رد الأدمن على المواطن (أدمن)
POST /api/complaints/{id}/citizen-feedback/    - تقييم المواطن للحل (مواطن)

# Data & Lists
GET  /api/complaints/representatives/           - قائمة النواب للاختيار
GET  /api/complaints/categories/                - فئات الشكاوى
GET  /api/complaints/governorates/              - المحافظات المصرية

# User-Specific Views
GET  /api/complaints/my-complaints/             - شكاوى المواطن الحالي (مواطن)
GET  /api/complaints/assigned-to-me/            - شكاوى النائب المسندة إليه (نائب)

# Statistics & Reports
GET  /api/complaints/statistics/                - إحصائيات شاملة (أدمن)
GET  /api/complaints/export/                    - تصدير البيانات (أدمن)

# File Management
POST /api/complaints/{id}/attachments/          - رفع مرفقات إضافية
DELETE /api/complaints/{id}/attachments/{file_id}/ - حذف مرفق

# System Health
GET  /health                                    - فحص صحة الخدمة
```

### **📥 مثال تقديم شكوى جديدة (كامل):**
```json
POST /api/complaints/submit/
Content-Type: multipart/form-data
Authorization: Bearer {jwt_token}

{
  "title": "انقطاع المياه المستمر في منطقة المعادي",
  "description": "انقطاع المياه لأكثر من 3 أيام متتالية مما يسبب معاناة شديدة للسكان. تم التواصل مع شركة المياه ولكن لم يتم الرد. نرجو التدخل العاجل لحل هذه المشكلة المتكررة في المنطقة.",
  "category": "infrastructure",
  "priority": "high",
  "governorate": "القاهرة",
  "district": "المعادي",
  "address": "شارع 9، المعادي الجديدة، بجوار مسجد النور",
  "location": {
    "latitude": 29.9601,
    "longitude": 31.2669
  },
  "contact_phone": "+201234567890",
  "contact_whatsapp": "+201234567890",
  "preferred_representative_id": 15,  // اختياري
  "youtube_link": "https://youtu.be/abc123def456",  // اختياري
  "is_anonymous": false,
  "attachments": [
    "water_shortage_photo1.jpg",
    "water_shortage_photo2.jpg", 
    "complaint_letter.pdf",
    "area_map.png"
  ]
}
```

### **📤 مثال استجابة تقديم الشكوى (كامل):**
```json
{
  "status": "success",
  "data": {
    "complaint_id": "COMP-2025-001234",
    "reference_number": "REF-CAI-001234",
    "title": "انقطاع المياه المستمر في منطقة المعادي",
    "status": "submitted",
    "category": {
      "id": "infrastructure",
      "name": "البنية التحتية",
      "icon": "🏗️"
    },
    "priority": {
      "level": "high",
      "name": "عالية",
      "color": "#FF6B35",
      "response_time_hours": 24
    },
    "submitted_at": "2025-01-01T10:30:00Z",
    "expected_response_time": "2025-01-02T10:30:00Z",
    "governorate": {
      "name": "القاهرة",
      "code": "CAI"
    },
    "preferred_representative": {
      "id": 15,
      "name": "د. أحمد محمد علي",
      "governorate": "القاهرة",
      "constituency": "المعادي",
      "party": "مستقبل وطن",
      "points": 45
    },
    "attachments": [
      {
        "id": 1,
        "filename": "water_shortage_photo1.jpg",
        "size": "2.3 MB",
        "type": "image",
        "url": "https://storage.googleapis.com/naebak-complaints-prod/attachments/1/water_shortage_photo1.jpg"
      },
      {
        "id": 2,
        "filename": "complaint_letter.pdf",
        "size": "1.1 MB", 
        "type": "document",
        "url": "https://storage.googleapis.com/naebak-complaints-prod/attachments/2/complaint_letter.pdf"
      }
    ],
    "youtube_video": {
      "url": "https://youtu.be/abc123def456",
      "embed_url": "https://www.youtube.com/embed/abc123def456",
      "thumbnail": "https://img.youtube.com/vi/abc123def456/maxresdefault.jpg"
    },
    "tracking_url": "https://naebak.com/complaints/track/COMP-2025-001234",
    "estimated_resolution_days": 7,
    "next_steps": [
      "ستتم مراجعة الشكوى من قبل الإدارة خلال 24 ساعة",
      "سيتم إسناد الشكوى للنائب المناسب",
      "ستصلك إشعارات بكل تطورات الشكوى"
    ]
  },
  "message": "تم تقديم شكواك بنجاح. رقم المرجع: REF-CAI-001234"
}
```

### **📥 مثال إسناد الشكوى (أدمن):**
```json
PUT /api/complaints/COMP-2025-001234/assign/
Content-Type: application/json
Authorization: Bearer {admin_jwt_token}

{
  "assigned_representative_id": 15,
  "admin_notes": "شكوى عاجلة تحتاج تدخل سريع - منطقة حيوية",
  "priority_override": "urgent",
  "expected_resolution_date": "2025-01-05",
  "internal_category": "water_infrastructure",
  "escalation_level": 1
}

Response:
{
  "status": "success",
  "data": {
    "complaint_id": "COMP-2025-001234",
    "status": "assigned",
    "assigned_to": {
      "id": 15,
      "name": "د. أحمد محمد علي",
      "governorate": "القاهرة",
      "constituency": "المعادي"
    },
    "assigned_at": "2025-01-01T11:15:00Z",
    "notification_sent": true
  },
  "message": "تم إسناد الشكوى بنجاح وإرسال إشعار للنائب"
}
```

### **📥 مثال حل الشكوى (نائب):**
```json
PUT /api/complaints/COMP-2025-001234/resolve/
Content-Type: application/json
Authorization: Bearer {representative_jwt_token}

{
  "resolution_statement": "تم التواصل الفوري مع شركة مياه القاهرة وتم تحديد سبب العطل في الخط الرئيسي. تم إصلاح العطل وعادت المياه للمنطقة بشكل طبيعي اعتباراً من اليوم. كما تم وضع خطة صيانة دورية لتجنب تكرار المشكلة.",
  "actions_taken": [
    "التواصل الفوري مع شركة مياه القاهرة",
    "زيارة ميدانية للموقع مع فريق الصيانة",
    "تحديد سبب العطل في الخط الرئيسي",
    "متابعة أعمال الإصلاح حتى الانتهاء",
    "التأكد من عودة الخدمة لجميع المنازل",
    "وضع خطة صيانة دورية مع الشركة"
  ],
  "resolution_date": "2025-01-03T14:30:00Z",
  "follow_up_required": true,
  "follow_up_date": "2025-01-10",
  "citizen_satisfaction_expected": 5,
  "attachments": [
    "resolution_report.pdf",
    "maintenance_plan.pdf",
    "before_after_photos.jpg"
  ],
  "cost_estimate": "50000 EGP",
  "timeline_met": true,
  "lessons_learned": "ضرورة الصيانة الدورية للخطوط الرئيسية لتجنب الأعطال المفاجئة"
}

Response:
{
  "status": "success",
  "data": {
    "complaint_id": "COMP-2025-001234",
    "status": "resolved",
    "resolved_at": "2025-01-03T14:30:00Z",
    "resolution_time_hours": 52,
    "points_awarded": 1,
    "new_total_points": 46,
    "citizen_notification_sent": true,
    "admin_notification_sent": true,
    "statistics_updated": true
  },
  "message": "تم حل الشكوى بنجاح وتم منحك نقطة جديدة"
}
```

---

## 🔄 **الفروق التفصيلية بين بيئات التشغيل**

### **🛠️ بيئة التطوير (Development):**
```yaml
Purpose: "تطوير واختبار الميزات الجديدة"
Database: 
  type: "PostgreSQL محلي"
  host: "localhost:5432"
  name: "naebak_complaints_dev"
  
Storage:
  type: "مجلد محلي"
  path: "/tmp/media/"
  cdn: false
  
Notifications:
  email: false
  sms: false
  push: false
  webhook: "http://localhost:8008/webhook"
  
File_Limits:
  max_size_mb: 10
  max_files: 5
  virus_scan: false
  
Performance:
  cpu: "0.5"
  memory: "512Mi"
  min_instances: 0
  max_instances: 3
  
Security:
  https: false
  csrf: false
  rate_limiting: false
  
Logging:
  level: "DEBUG"
  destination: "console"
  
External_Services:
  auth_service: "http://localhost:8001"
  admin_service: "http://localhost:8002"
  notifications_service: "http://localhost:8008"
```

### **🏭 بيئة الإنتاج (Production):**
```yaml
Purpose: "خدمة المستخدمين الفعليين"
Database:
  type: "Cloud SQL PostgreSQL"
  host: "production-db-instance"
  name: "naebak_complaints_prod"
  ssl: true
  backup: "daily"
  
Storage:
  type: "Google Cloud Storage"
  bucket: "naebak-complaints-prod"
  cdn: "https://cdn.naebak.com/complaints/"
  backup: "hourly"
  
Notifications:
  email: true
  sms: true
  push: true
  webhook: "https://notifications.naebak.com/webhook"
  
File_Limits:
  max_size_mb: 50
  max_files: 10
  virus_scan: true
  malware_scan: true
  
Performance:
  cpu: "1"
  memory: "1Gi"
  min_instances: 1
  max_instances: 10
  auto_scaling: true
  
Security:
  https: true
  csrf: true
  rate_limiting: true
  firewall: true
  ddos_protection: true
  
Logging:
  level: "INFO"
  destination: "Google Cloud Logging"
  retention: "90 days"
  
Monitoring:
  uptime_monitoring: true
  performance_monitoring: true
  error_tracking: "Sentry"
  alerts: true
  
External_Services:
  auth_service: "https://auth.naebak.com"
  admin_service: "https://admin.naebak.com"
  notifications_service: "https://notifications.naebak.com"
```

### **🧪 بيئة الاختبار (Testing):**
```yaml
Purpose: "اختبار التكامل والأداء"
Database:
  type: "SQLite في الذاكرة"
  reset_after_each_test: true
  
Storage:
  type: "مؤقت في الذاكرة"
  cleanup: "automatic"
  
Notifications:
  all_disabled: true
  mock_responses: true
  
File_Limits:
  max_size_mb: 1
  max_files: 2
  
Performance:
  cpu: "0.3"
  memory: "256Mi"
  instances: 1
  
Testing_Features:
  mock_external_services: true
  test_data_seeding: true
  automated_cleanup: true
```

---

## 📈 **المراقبة والتحليلات الشاملة**

### **📊 المقاييس الأساسية (12 مقياس):**
```python
CORE_METRICS = {
    "complaint_submission_rate": {
        "description": "معدل تقديم الشكاوى يومياً",
        "target": "50-100 شكوى/يوم",
        "alert_threshold": "> 200 أو < 10"
    },
    "response_time_average": {
        "description": "متوسط وقت رد النواب",
        "target": "< 24 ساعة",
        "alert_threshold": "> 48 ساعة"
    },
    "resolution_rate": {
        "description": "نسبة الشكاوى المحلولة",
        "target": "> 80%",
        "alert_threshold": "< 60%"
    },
    "citizen_satisfaction": {
        "description": "رضا المواطنين عن الحلول",
        "target": "> 4.0/5.0",
        "alert_threshold": "< 3.0/5.0"
    },
    "representative_performance": {
        "description": "أداء النواب في حل الشكاوى",
        "target": "> 5 شكاوى محلولة/شهر",
        "alert_threshold": "< 2 شكاوى محلولة/شهر"
    },
    "category_distribution": {
        "description": "توزيع الشكاوى حسب الفئة",
        "monitoring": "تحديد المشاكل الأكثر شيوعاً"
    },
    "geographical_distribution": {
        "description": "توزيع الشكاوى حسب المحافظة",
        "monitoring": "تحديد المناطق الأكثر احتياجاً"
    },
    "file_upload_success_rate": {
        "description": "نسبة نجاح رفع المرفقات",
        "target": "> 95%",
        "alert_threshold": "< 90%"
    },
    "system_uptime": {
        "description": "وقت تشغيل النظام",
        "target": "> 99.5%",
        "alert_threshold": "< 99%"
    },
    "api_response_time": {
        "description": "زمن استجابة APIs",
        "target": "< 500ms",
        "alert_threshold": "> 2000ms"
    },
    "storage_usage": {
        "description": "استخدام مساحة التخزين",
        "monitoring": "نمو حجم المرفقات",
        "alert_threshold": "> 80% من الحد الأقصى"
    },
    "points_distribution": {
        "description": "توزيع النقاط بين النواب",
        "monitoring": "عدالة توزيع الشكاوى"
    }
}
```

### **🚨 التنبيهات والإشعارات (8 أنواع):**
```python
ALERT_TYPES = {
    "urgent_complaint_unassigned": {
        "trigger": "شكوى عاجلة لم يتم إسنادها خلال ساعة",
        "recipients": ["admin_team"],
        "severity": "critical"
    },
    "representative_overdue_response": {
        "trigger": "نائب لم يرد على شكوى خلال الوقت المحدد",
        "recipients": ["admin_team", "representative"],
        "severity": "high"
    },
    "high_complaint_volume": {
        "trigger": "زيادة غير طبيعية في عدد الشكاوى",
        "recipients": ["admin_team", "management"],
        "severity": "medium"
    },
    "low_resolution_rate": {
        "trigger": "انخفاض معدل حل الشكاوى عن 60%",
        "recipients": ["admin_team", "management"],
        "severity": "high"
    },
    "system_performance_degradation": {
        "trigger": "تدهور أداء النظام",
        "recipients": ["tech_team", "admin_team"],
        "severity": "high"
    },
    "storage_capacity_warning": {
        "trigger": "اقتراب نفاد مساحة التخزين",
        "recipients": ["tech_team"],
        "severity": "medium"
    },
    "suspicious_activity": {
        "trigger": "نشاط مشبوه أو محاولات اختراق",
        "recipients": ["security_team", "tech_team"],
        "severity": "critical"
    },
    "citizen_satisfaction_drop": {
        "trigger": "انخفاض رضا المواطنين عن 3.0",
        "recipients": ["admin_team", "management"],
        "severity": "medium"
    }
}
```

### **📈 التقارير الدورية:**
```python
REPORTING_SCHEDULE = {
    "daily_summary": {
        "time": "09:00 AM",
        "recipients": ["admin_team"],
        "content": [
            "عدد الشكاوى الجديدة",
            "عدد الشكاوى المحلولة",
            "متوسط وقت الاستجابة",
            "النواب الأكثر نشاطاً"
        ]
    },
    "weekly_performance": {
        "time": "Monday 10:00 AM",
        "recipients": ["management", "admin_team"],
        "content": [
            "إحصائيات الأداء الأسبوعية",
            "تحليل الاتجاهات",
            "أداء النواب",
            "رضا المواطنين"
        ]
    },
    "monthly_analysis": {
        "time": "1st of month 09:00 AM",
        "recipients": ["management", "admin_team", "representatives"],
        "content": [
            "تحليل شامل للشهر",
            "مقارنة بالأشهر السابقة",
            "توصيات للتحسين",
            "إنجازات النواب"
        ]
    }
}
```

---

## 🚀 **خطوات التطوير المرحلية**

### **🎯 المرحلة الأولى - الأساسيات (4 أسابيع):**
```python
PHASE_1_TASKS = [
    {
        "task": "إعداد Django + DRF",
        "duration": "3 أيام",
        "status": "✅ مكتمل",
        "dependencies": []
    },
    {
        "task": "إنشاء نماذج البيانات",
        "duration": "5 أيام",
        "status": "⏳ قيد التنفيذ",
        "dependencies": ["Django setup"]
    },
    {
        "task": "تطبيق رفع الملفات",
        "duration": "7 أيام",
        "status": "⏳ قيد التنفيذ",
        "dependencies": ["Data models"]
    },
    {
        "task": "إنشاء APIs الأساسية",
        "duration": "10 أيام",
        "status": "⏳ قيد التنفيذ",
        "dependencies": ["File upload"]
    },
    {
        "task": "ربط Google Cloud Storage",
        "duration": "3 أيام",
        "status": "⏳ قيد التنفيذ",
        "dependencies": ["APIs"]
    }
]
```

### **🎯 المرحلة الثانية - سير العمل (6 أسابيع):**
```python
PHASE_2_TASKS = [
    {
        "task": "تطبيق نظام الإسناد",
        "duration": "7 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Phase 1 complete"]
    },
    {
        "task": "لوحة إدارة الشكاوى للأدمن",
        "duration": "10 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Assignment system"]
    },
    {
        "task": "لوحة إدارة الشكاوى للنائب",
        "duration": "10 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Admin dashboard"]
    },
    {
        "task": "نظام الحالات والتتبع",
        "duration": "7 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Representative dashboard"]
    },
    {
        "task": "نظام النقاط والتقييم",
        "duration": "5 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Status system"]
    },
    {
        "task": "ربط خدمة الإشعارات",
        "duration": "3 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Points system"]
    }
]
```

### **🎯 المرحلة الثالثة - التحسين والتكامل (4 أسابيع):**
```python
PHASE_3_TASKS = [
    {
        "task": "ربط خدمة الإحصائيات",
        "duration": "3 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Phase 2 complete"]
    },
    {
        "task": "ربط خدمة التقييمات",
        "duration": "3 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Statistics integration"]
    },
    {
        "task": "تحسين الأداء والأمان",
        "duration": "7 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Ratings integration"]
    },
    {
        "task": "إضافة التحليلات والتقارير",
        "duration": "7 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Performance optimization"]
    },
    {
        "task": "اختبارات شاملة ونشر",
        "duration": "8 أيام",
        "status": "⏳ مخطط",
        "dependencies": ["Analytics"]
    }
]
```

---

## 📚 **الموارد والمراجع التقنية**

### **🔧 أدوات التطوير الأساسية:**
```python
DEVELOPMENT_STACK = {
    "backend_framework": "Django 4.2",
    "api_framework": "Django REST Framework 3.14.0",
    "database": "PostgreSQL 14",
    "cache": "Redis 6.2",
    "task_queue": "Celery 5.3.4",
    "storage": "Google Cloud Storage",
    "monitoring": "Google Cloud Monitoring",
    "logging": "Google Cloud Logging",
    "error_tracking": "Sentry",
    "testing": "pytest + Django TestCase",
    "documentation": "Django REST Swagger"
}
```

### **📦 التبعيات الكاملة:**
```python
DEPENDENCIES = {
    "core": [
        "Django==4.2.0",
        "djangorestframework==3.14.0",
        "psycopg2-binary==2.9.7",
        "redis==4.6.0",
        "celery==5.3.4"
    ],
    "storage": [
        "google-cloud-storage==2.10.0",
        "django-storages==1.14.2",
        "Pillow==10.1.0"
    ],
    "security": [
        "django-cors-headers==4.3.1",
        "django-ratelimit==4.1.0",
        "python-magic==0.4.27"
    ],
    "monitoring": [
        "sentry-sdk==1.32.0",
        "google-cloud-monitoring==2.16.0",
        "django-prometheus==2.3.1"
    ],
    "testing": [
        "pytest==7.4.2",
        "pytest-django==4.5.2",
        "factory-boy==3.3.0",
        "coverage==7.3.2"
    ]
}
```

### **📖 وثائق المرجع:**
```python
DOCUMENTATION_LINKS = {
    "django_docs": "https://docs.djangoproject.com/en/4.2/",
    "drf_docs": "https://www.django-rest-framework.org/",
    "google_cloud_storage": "https://cloud.google.com/storage/docs",
    "celery_docs": "https://docs.celeryproject.org/en/stable/",
    "redis_docs": "https://redis.io/documentation",
    "postgresql_docs": "https://www.postgresql.org/docs/14/",
    "naebak_api_docs": "https://api.naebak.com/docs/",
    "project_repository": "https://github.com/egyptofrance/naebak-complaints-service"
}
```

---

## 🎯 **الخلاصة والنقاط الرئيسية**

### **📋 ملخص الخدمة:**
خدمة الشكاوى هي **العمود الفقري** لمنصة نائبك، تمكن المواطنين من تقديم شكاواهم (1500 حرف + 10 مرفقات + رابط يوتيوب) للإدارة التي تسندها للنواب المناسبين. النواب يقبلون أو يرفضون أو يعلقون الشكاوى، وعند الحل يحصلون على نقاط تظهر في ملفاتهم الشخصية.

### **🔑 النقاط الحاسمة:**
1. **البساطة في التصميم** - تدفق واضح ومباشر
2. **الشمولية في البيانات** - جميع المعلومات من المخزن
3. **المرونة في التطوير** - إعدادات متعددة البيئات
4. **الأمان في التنفيذ** - حماية شاملة على 7 مستويات
5. **التكامل مع النظام** - ربط مع 5 خدمات أخرى

### **🚀 الاستعداد للتطوير:**
الخدمة الآن **جاهزة بالكامل** للبدء في التطوير الفعلي مع:
- ✅ جميع البيانات الأساسية محددة
- ✅ جميع الإعدادات موضوعة
- ✅ جميع APIs مخططة
- ✅ جميع العلاقات واضحة
- ✅ خطة التطوير مرحلية

---

**📝 ملاحظة نهائية:** هذا الملف هو **الدليل الشامل والكامل** لخدمة الشكاوى - من التصميم إلى التنفيذ إلى النشر. كل ما يحتاجه المطور موجود هنا.
