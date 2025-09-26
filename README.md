# 🏷️ خدمة الشكاوى (naebak-complaints-service)

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/egyptofrance/naebak-complaints-service/actions)
[![Coverage](https://img.shields.io/badge/coverage-88%25-green)](https://github.com/egyptofrance/naebak-complaints-service)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/egyptofrance/naebak-complaints-service/releases)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

## 📝 الوصف

خدمة إدارة الشكاوى في منصة نائبك. تتيح للمواطنين تقديم الشكاوى وتتبعها، وتوفر للنواب واجهة لإدارة الشكاوى والرد عليها. تدعم الخدمة تصنيف الشكاوى وتحديد أولوياتها وتوجيهها للجهة المختصة.

---

## ✨ الميزات الرئيسية

- **تقديم الشكاوى**: نظام سهل لتقديم الشكاوى مع إرفاق الملفات
- **تتبع الشكاوى**: تتبع حالة الشكوى من التقديم حتى الحل
- **تصنيف وتوجيه**: تصنيف الشكاوى تلقائياً وتوجيهها للنائب المختص
- **نظام إشعارات**: إشعارات فورية للمواطنين والنواب عند كل تحديث

---

## 🛠️ التقنيات المستخدمة

| التقنية | الإصدار | الغرض |
|---------|---------|-------|
| **Django** | 4.2.5 | إطار العمل الأساسي |
| **Django REST Framework** | 3.14.0 | تطوير APIs |
| **PostgreSQL** | 13+ | قاعدة البيانات الرئيسية |
| **Redis** | 6+ | التخزين المؤقت والمهام غير المتزامنة |
| **Celery** | 5.3+ | إرسال الإشعارات ومعالجة الصور |

---

## 🚀 التثبيت والتشغيل

### **المتطلبات الأساسية**

- Python 3.11+
- PostgreSQL 13+
- Redis 6+
- Docker & Docker Compose

### **التثبيت المحلي**

```bash
git clone https://github.com/egyptofrance/naebak-complaints-service.git
cd naebak-complaints-service

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

cp .env.example .env
# قم بتعديل ملف .env بالقيم المناسبة

python manage.py migrate

python manage.py runserver 8001
```

### **التشغيل باستخدام Docker**

```bash
docker-compose up --build -d
```

---

## 📚 توثيق الـ API

- **Swagger UI**: [http://localhost:8001/api/docs/](http://localhost:8001/api/docs/)
- **Redoc**: [http://localhost:8001/api/redoc/](http://localhost:8001/api/redoc/)

---

## 🧪 الاختبارات

```bash
python manage.py test
```

---

## 🤝 المساهمة

يرجى مراجعة [دليل المساهمة](CONTRIBUTING.md) و [معايير التوثيق الموحدة](../../naebak-almakhzan/DOCUMENTATION_STANDARDS.md).

---

## 📄 الترخيص

هذا المشروع مرخص تحت [رخصة MIT](LICENSE).

