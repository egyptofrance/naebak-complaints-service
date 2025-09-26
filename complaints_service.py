#!/usr/bin/env python3
"""
خدمة الشكاوى المبسطة - نائبك
============================

خدمة شكاوى بسيطة وموثوقة باستخدام Flask + SQLite.
تدعم تقديم الشكاوى، متابعتها، وإدارتها بواسطة الإدارة والنواب.

الميزات:
- تقديم شكاوى مع مرفقات (حد أقصى 1500 حرف)
- تتبع حالة الشكوى (7 حالات مختلفة)
- تصنيف حسب النوع والمحافظة والأولوية
- تقييم الحل من قبل المواطن
- إحصائيات شاملة
- API بسيط وواضح
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import uuid
import os
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['JWT_SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database configuration - easy to switch to PostgreSQL later
if os.environ.get('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///naebak_complaints.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# File upload configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

# Models
class Governorate(db.Model):
    """نموذج المحافظات المصرية"""
    __tablename__ = 'governorates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    name_en = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(3), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Governorate {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'code': self.code,
            'is_active': self.is_active,
            'display_order': self.display_order
        }

class ComplaintType(db.Model):
    """نموذج أنواع الشكاوى"""
    __tablename__ = 'complaint_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # infrastructure, health, education, etc.
    target_council = db.Column(db.String(20), nullable=False, default='parliament')  # parliament, senate, both
    priority_level = db.Column(db.String(10), nullable=False, default='medium')  # low, medium, high, urgent
    icon = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ComplaintType {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_en': self.name_en,
            'description': self.description,
            'category': self.category,
            'target_council': self.target_council,
            'priority_level': self.priority_level,
            'icon': self.icon,
            'is_active': self.is_active,
            'display_order': self.display_order
        }

class Complaint(db.Model):
    """نموذج الشكاوى الرئيسي"""
    __tablename__ = 'complaints'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    
    # بيانات المشتكي
    citizen_id = db.Column(db.Integer, nullable=False)  # من خدمة المصادقة
    citizen_name = db.Column(db.String(100), nullable=False)
    citizen_email = db.Column(db.String(120), nullable=False)
    citizen_phone = db.Column(db.String(20), nullable=True)
    
    # بيانات الشكوى
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)  # حد أقصى 1500 حرف
    complaint_type_id = db.Column(db.Integer, db.ForeignKey('complaint_types.id'), nullable=False)
    governorate_id = db.Column(db.Integer, db.ForeignKey('governorates.id'), nullable=False)
    city = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    detailed_location = db.Column(db.String(300), nullable=True)
    
    # الحالة والأولوية
    status = db.Column(db.String(20), nullable=False, default='submitted')
    # submitted, under_review, in_progress, pending_info, resolved, closed, rejected
    priority = db.Column(db.String(10), nullable=False, default='medium')  # low, medium, high, urgent
    
    # المتابعة والإدارة
    assigned_to = db.Column(db.Integer, nullable=True)  # معرف النائب أو المسؤول المكلف
    admin_notes = db.Column(db.Text, nullable=True)
    resolution_details = db.Column(db.Text, nullable=True)
    
    # التقييم
    citizen_rating = db.Column(db.Integer, nullable=True)  # 1-5
    citizen_feedback = db.Column(db.Text, nullable=True)
    
    # التواريخ المهمة
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    resolved_at = db.Column(db.DateTime, nullable=True)
    closed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # العلاقات
    complaint_type = db.relationship('ComplaintType', backref='complaints')
    governorate = db.relationship('Governorate', backref='complaints')
    attachments = db.relationship('ComplaintAttachment', backref='complaint', cascade='all, delete-orphan')
    updates = db.relationship('ComplaintUpdate', backref='complaint', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Complaint {self.complaint_id}>'
    
    def to_dict(self, include_details=True):
        data = {
            'id': self.id,
            'complaint_id': self.complaint_id,
            'citizen_id': self.citizen_id,
            'citizen_name': self.citizen_name,
            'citizen_email': self.citizen_email,
            'citizen_phone': self.citizen_phone,
            'title': self.title,
            'status': self.status,
            'priority': self.priority,
            'complaint_type': self.complaint_type.to_dict() if self.complaint_type else None,
            'governorate': self.governorate.to_dict() if self.governorate else None,
            'city': self.city,
            'district': self.district,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_details:
            data.update({
                'description': self.description,
                'detailed_location': self.detailed_location,
                'assigned_to': self.assigned_to,
                'admin_notes': self.admin_notes,
                'resolution_details': self.resolution_details,
                'citizen_rating': self.citizen_rating,
                'citizen_feedback': self.citizen_feedback,
                'reviewed_at': self.reviewed_at.isoformat() if self.reviewed_at else None,
                'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
                'closed_at': self.closed_at.isoformat() if self.closed_at else None,
                'attachments': [att.to_dict() for att in self.attachments],
                'updates': [upd.to_dict() for upd in self.updates]
            })
        
        return data

class ComplaintAttachment(db.Model):
    """نموذج مرفقات الشكاوى"""
    __tablename__ = 'complaint_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ComplaintAttachment {self.original_filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }

class ComplaintUpdate(db.Model):
    """نموذج تحديثات الشكاوى"""
    __tablename__ = 'complaint_updates'
    
    id = db.Column(db.Integer, primary_key=True)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaints.id'), nullable=False)
    
    # بيانات التحديث
    update_type = db.Column(db.String(20), nullable=False)  # status_change, note, assignment, resolution
    old_status = db.Column(db.String(20), nullable=True)
    new_status = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=True)
    
    # من قام بالتحديث
    updated_by = db.Column(db.Integer, nullable=False)  # معرف المستخدم
    updated_by_name = db.Column(db.String(100), nullable=False)
    updated_by_role = db.Column(db.String(20), nullable=False)  # citizen, admin, deputy
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ComplaintUpdate {self.update_type}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'update_type': self.update_type,
            'old_status': self.old_status,
            'new_status': self.new_status,
            'message': self.message,
            'updated_by': self.updated_by,
            'updated_by_name': self.updated_by_name,
            'updated_by_role': self.updated_by_role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Helper functions
def allowed_file(filename):
    """التحقق من نوع الملف المسموح"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file_path):
    """الحصول على حجم الملف"""
    try:
        return os.path.getsize(file_path)
    except:
        return 0

def init_database():
    """إنشاء قاعدة البيانات والجداول"""
    with app.app_context():
        # إنشاء مجلد الرفع إذا لم يكن موجوداً
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        db.create_all()
        
        # إضافة المحافظات المصرية إذا لم تكن موجودة
        if Governorate.query.count() == 0:
            governorates = [
                {'name': 'القاهرة', 'name_en': 'Cairo', 'code': 'CAI', 'display_order': 1},
                {'name': 'الجيزة', 'name_en': 'Giza', 'code': 'GIZ', 'display_order': 2},
                {'name': 'الإسكندرية', 'name_en': 'Alexandria', 'code': 'ALX', 'display_order': 3},
                {'name': 'الدقهلية', 'name_en': 'Dakahlia', 'code': 'DKH', 'display_order': 4},
                {'name': 'البحر الأحمر', 'name_en': 'Red Sea', 'code': 'RSE', 'display_order': 5},
                {'name': 'البحيرة', 'name_en': 'Beheira', 'code': 'BHR', 'display_order': 6},
                {'name': 'الفيوم', 'name_en': 'Fayoum', 'code': 'FYM', 'display_order': 7},
                {'name': 'الغربية', 'name_en': 'Gharbia', 'code': 'GHR', 'display_order': 8},
                {'name': 'الإسماعيلية', 'name_en': 'Ismailia', 'code': 'ISM', 'display_order': 9},
                {'name': 'المنوفية', 'name_en': 'Monufia', 'code': 'MNF', 'display_order': 10},
                {'name': 'المنيا', 'name_en': 'Minya', 'code': 'MNY', 'display_order': 11},
                {'name': 'القليوبية', 'name_en': 'Qalyubia', 'code': 'QLY', 'display_order': 12},
                {'name': 'الوادي الجديد', 'name_en': 'New Valley', 'code': 'NVL', 'display_order': 13},
                {'name': 'شمال سيناء', 'name_en': 'North Sinai', 'code': 'NSI', 'display_order': 14},
                {'name': 'بورسعيد', 'name_en': 'Port Said', 'code': 'PTS', 'display_order': 15},
                {'name': 'قنا', 'name_en': 'Qena', 'code': 'QNA', 'display_order': 16},
                {'name': 'الشرقية', 'name_en': 'Sharqia', 'code': 'SHR', 'display_order': 17},
                {'name': 'سوهاج', 'name_en': 'Sohag', 'code': 'SOH', 'display_order': 18},
                {'name': 'جنوب سيناء', 'name_en': 'South Sinai', 'code': 'SSI', 'display_order': 19},
                {'name': 'السويس', 'name_en': 'Suez', 'code': 'SUZ', 'display_order': 20},
                {'name': 'أسوان', 'name_en': 'Aswan', 'code': 'ASW', 'display_order': 21},
                {'name': 'أسيوط', 'name_en': 'Asyut', 'code': 'ASY', 'display_order': 22},
                {'name': 'بني سويف', 'name_en': 'Beni Suef', 'code': 'BSW', 'display_order': 23},
                {'name': 'دمياط', 'name_en': 'Damietta', 'code': 'DMT', 'display_order': 24},
                {'name': 'كفر الشيخ', 'name_en': 'Kafr El Sheikh', 'code': 'KFS', 'display_order': 25},
                {'name': 'الأقصر', 'name_en': 'Luxor', 'code': 'LXR', 'display_order': 26},
                {'name': 'مطروح', 'name_en': 'Matrouh', 'code': 'MTR', 'display_order': 27}
            ]
            
            for gov_data in governorates:
                gov = Governorate(**gov_data)
                db.session.add(gov)
            
            db.session.commit()
            logger.info("تم إضافة المحافظات المصرية")
        
        # إضافة أنواع الشكاوى الأساسية إذا لم تكن موجودة
        if ComplaintType.query.count() == 0:
            complaint_types = [
                {
                    'name': 'البنية التحتية - الطرق',
                    'name_en': 'Infrastructure - Roads',
                    'description': 'شكاوى متعلقة بحالة الطرق والشوارع',
                    'category': 'infrastructure',
                    'target_council': 'parliament',
                    'priority_level': 'medium',
                    'icon': 'road',
                    'display_order': 1
                },
                {
                    'name': 'البنية التحتية - المياه',
                    'name_en': 'Infrastructure - Water',
                    'description': 'شكاوى متعلقة بخدمات المياه والصرف الصحي',
                    'category': 'infrastructure',
                    'target_council': 'parliament',
                    'priority_level': 'high',
                    'icon': 'water',
                    'display_order': 2
                },
                {
                    'name': 'البنية التحتية - الكهرباء',
                    'name_en': 'Infrastructure - Electricity',
                    'description': 'شكاوى متعلقة بخدمات الكهرباء والإنارة',
                    'category': 'infrastructure',
                    'target_council': 'parliament',
                    'priority_level': 'high',
                    'icon': 'electricity',
                    'display_order': 3
                },
                {
                    'name': 'الخدمات الصحية',
                    'name_en': 'Health Services',
                    'description': 'شكاوى متعلقة بالمستشفيات والخدمات الطبية',
                    'category': 'health',
                    'target_council': 'parliament',
                    'priority_level': 'high',
                    'icon': 'health',
                    'display_order': 4
                },
                {
                    'name': 'الخدمات التعليمية',
                    'name_en': 'Education Services',
                    'description': 'شكاوى متعلقة بالمدارس والخدمات التعليمية',
                    'category': 'education',
                    'target_council': 'parliament',
                    'priority_level': 'medium',
                    'icon': 'education',
                    'display_order': 5
                },
                {
                    'name': 'الأمن والسلامة',
                    'name_en': 'Security and Safety',
                    'description': 'شكاوى متعلقة بالأمن العام والسلامة',
                    'category': 'security',
                    'target_council': 'parliament',
                    'priority_level': 'urgent',
                    'icon': 'security',
                    'display_order': 6
                },
                {
                    'name': 'النقل والمواصلات',
                    'name_en': 'Transportation',
                    'description': 'شكاوى متعلقة بوسائل النقل والمواصلات العامة',
                    'category': 'transportation',
                    'target_council': 'parliament',
                    'priority_level': 'medium',
                    'icon': 'transport',
                    'display_order': 7
                },
                {
                    'name': 'البيئة والنظافة',
                    'name_en': 'Environment and Cleanliness',
                    'description': 'شكاوى متعلقة بالبيئة والنظافة العامة',
                    'category': 'environment',
                    'target_council': 'parliament',
                    'priority_level': 'medium',
                    'icon': 'environment',
                    'display_order': 8
                },
                {
                    'name': 'الخدمات الحكومية',
                    'name_en': 'Government Services',
                    'description': 'شكاوى متعلقة بالخدمات الحكومية والإدارية',
                    'category': 'public_services',
                    'target_council': 'parliament',
                    'priority_level': 'medium',
                    'icon': 'government',
                    'display_order': 9
                },
                {
                    'name': 'أخرى',
                    'name_en': 'Other',
                    'description': 'شكاوى أخرى غير مصنفة',
                    'category': 'other',
                    'target_council': 'parliament',
                    'priority_level': 'low',
                    'icon': 'other',
                    'display_order': 10
                }
            ]
            
            for type_data in complaint_types:
                complaint_type = ComplaintType(**type_data)
                db.session.add(complaint_type)
            
            db.session.commit()
            logger.info("تم إضافة أنواع الشكاوى الأساسية")
        
        logger.info("تم إنشاء قاعدة البيانات بنجاح")

# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """فحص حالة الخدمة"""
    return jsonify({
        'status': 'healthy',
        'service': 'naebak-complaints-service',
        'version': '2.0.0',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'SQLite' if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI'] else 'PostgreSQL',
        'features': {
            'complaint_submission': True,
            'complaint_tracking': True,
            'file_attachments': True,
            'status_updates': True,
            'rating_system': True,
            'admin_management': True,
            'statistics': True
        }
    }), 200

@app.route('/api/complaint-types', methods=['GET'])
def get_complaint_types():
    """الحصول على أنواع الشكاوى"""
    try:
        types = ComplaintType.query.filter_by(is_active=True).order_by(ComplaintType.display_order).all()
        return jsonify({
            'complaint_types': [t.to_dict() for t in types]
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على أنواع الشكاوى: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الحصول على أنواع الشكاوى'}), 500

@app.route('/api/governorates', methods=['GET'])
def get_governorates():
    """الحصول على المحافظات"""
    try:
        governorates = Governorate.query.filter_by(is_active=True).order_by(Governorate.display_order).all()
        return jsonify({
            'governorates': [gov.to_dict() for gov in governorates]
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على المحافظات: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الحصول على المحافظات'}), 500

@app.route('/api/complaints', methods=['POST'])
@jwt_required()
def submit_complaint():
    """تقديم شكوى جديدة"""
    try:
        citizen_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'لا توجد بيانات'}), 400
        
        # التحقق من البيانات المطلوبة
        required_fields = ['title', 'description', 'complaint_type_id', 'governorate_id', 'citizen_name', 'citizen_email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} مطلوب'}), 400
        
        # التحقق من طول الوصف (حد أقصى 1500 حرف)
        if len(data['description']) > 1500:
            return jsonify({'error': 'الوصف يجب ألا يزيد عن 1500 حرف'}), 400
        
        # التحقق من وجود نوع الشكوى والمحافظة
        complaint_type = ComplaintType.query.get(data['complaint_type_id'])
        if not complaint_type or not complaint_type.is_active:
            return jsonify({'error': 'نوع الشكوى غير صحيح'}), 400
        
        governorate = Governorate.query.get(data['governorate_id'])
        if not governorate or not governorate.is_active:
            return jsonify({'error': 'المحافظة غير صحيحة'}), 400
        
        # إنشاء الشكوى الجديدة
        complaint = Complaint(
            citizen_id=citizen_id,
            citizen_name=data['citizen_name'].strip(),
            citizen_email=data['citizen_email'].strip(),
            citizen_phone=data.get('citizen_phone', '').strip() if data.get('citizen_phone') else None,
            title=data['title'].strip(),
            description=data['description'].strip(),
            complaint_type_id=data['complaint_type_id'],
            governorate_id=data['governorate_id'],
            city=data.get('city', '').strip() if data.get('city') else None,
            district=data.get('district', '').strip() if data.get('district') else None,
            detailed_location=data.get('detailed_location', '').strip() if data.get('detailed_location') else None,
            priority=complaint_type.priority_level
        )
        
        db.session.add(complaint)
        db.session.commit()
        
        # إضافة تحديث أولي
        initial_update = ComplaintUpdate(
            complaint_id=complaint.id,
            update_type='status_change',
            old_status=None,
            new_status='submitted',
            message='تم تقديم الشكوى بنجاح',
            updated_by=citizen_id,
            updated_by_name=data['citizen_name'],
            updated_by_role='citizen'
        )
        
        db.session.add(initial_update)
        db.session.commit()
        
        logger.info(f"تم تقديم شكوى جديدة: {complaint.complaint_id}")
        
        return jsonify({
            'message': 'تم تقديم الشكوى بنجاح',
            'complaint': complaint.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تقديم الشكوى: {str(e)}")
        return jsonify({'error': 'حدث خطأ في تقديم الشكوى'}), 500

@app.route('/api/complaints', methods=['GET'])
@jwt_required()
def get_complaints():
    """الحصول على قائمة الشكاوى"""
    try:
        citizen_id = get_jwt_identity()
        
        # معاملات البحث والتصفية
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        status = request.args.get('status')
        complaint_type_id = request.args.get('complaint_type_id', type=int)
        governorate_id = request.args.get('governorate_id', type=int)
        priority = request.args.get('priority')
        search = request.args.get('search', '').strip()
        
        # بناء الاستعلام
        query = Complaint.query.filter_by(citizen_id=citizen_id)
        
        if status:
            query = query.filter(Complaint.status == status)
        
        if complaint_type_id:
            query = query.filter(Complaint.complaint_type_id == complaint_type_id)
        
        if governorate_id:
            query = query.filter(Complaint.governorate_id == governorate_id)
        
        if priority:
            query = query.filter(Complaint.priority == priority)
        
        if search:
            query = query.filter(
                db.or_(
                    Complaint.title.contains(search),
                    Complaint.description.contains(search),
                    Complaint.complaint_id.contains(search)
                )
            )
        
        # التصفح
        complaints = query.order_by(Complaint.submitted_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'complaints': [complaint.to_dict(include_details=False) for complaint in complaints.items],
            'total': complaints.total,
            'pages': complaints.pages,
            'current_page': page,
            'per_page': per_page
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الشكاوى: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الحصول على الشكاوى'}), 500

@app.route('/api/complaints/<complaint_id>', methods=['GET'])
@jwt_required()
def get_complaint_details(complaint_id):
    """الحصول على تفاصيل شكوى محددة"""
    try:
        citizen_id = get_jwt_identity()
        
        complaint = Complaint.query.filter_by(
            complaint_id=complaint_id,
            citizen_id=citizen_id
        ).first()
        
        if not complaint:
            return jsonify({'error': 'الشكوى غير موجودة'}), 404
        
        return jsonify({
            'complaint': complaint.to_dict(include_details=True)
        }), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على تفاصيل الشكوى: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الحصول على تفاصيل الشكوى'}), 500

@app.route('/api/complaints/<complaint_id>/rate', methods=['POST'])
@jwt_required()
def rate_complaint_resolution(complaint_id):
    """تقييم حل الشكوى"""
    try:
        citizen_id = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'لا توجد بيانات'}), 400
        
        rating = data.get('rating')
        feedback = data.get('feedback', '').strip()
        
        if not rating or rating not in [1, 2, 3, 4, 5]:
            return jsonify({'error': 'التقييم يجب أن يكون من 1 إلى 5'}), 400
        
        complaint = Complaint.query.filter_by(
            complaint_id=complaint_id,
            citizen_id=citizen_id
        ).first()
        
        if not complaint:
            return jsonify({'error': 'الشكوى غير موجودة'}), 404
        
        if complaint.status not in ['resolved', 'closed']:
            return jsonify({'error': 'لا يمكن تقييم شكوى لم يتم حلها بعد'}), 400
        
        # تحديث التقييم
        complaint.citizen_rating = rating
        complaint.citizen_feedback = feedback if feedback else None
        complaint.updated_at = datetime.utcnow()
        
        # إضافة تحديث
        update = ComplaintUpdate(
            complaint_id=complaint.id,
            update_type='rating',
            message=f'تم تقييم الحل بـ {rating} نجوم',
            updated_by=citizen_id,
            updated_by_name=complaint.citizen_name,
            updated_by_role='citizen'
        )
        
        db.session.add(update)
        db.session.commit()
        
        logger.info(f"تم تقييم الشكوى {complaint_id} بـ {rating} نجوم")
        
        return jsonify({
            'message': 'تم تقييم الحل بنجاح',
            'rating': rating
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"خطأ في تقييم الشكوى: {str(e)}")
        return jsonify({'error': 'حدث خطأ في تقييم الشكوى'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """إحصائيات الخدمة"""
    try:
        stats = {
            'total_complaints': Complaint.query.count(),
            'submitted': Complaint.query.filter_by(status='submitted').count(),
            'under_review': Complaint.query.filter_by(status='under_review').count(),
            'in_progress': Complaint.query.filter_by(status='in_progress').count(),
            'resolved': Complaint.query.filter_by(status='resolved').count(),
            'closed': Complaint.query.filter_by(status='closed').count(),
            'rejected': Complaint.query.filter_by(status='rejected').count(),
            'high_priority': Complaint.query.filter_by(priority='high').count(),
            'urgent_priority': Complaint.query.filter_by(priority='urgent').count(),
            'with_attachments': Complaint.query.join(ComplaintAttachment).count(),
            'rated_complaints': Complaint.query.filter(Complaint.citizen_rating.isnot(None)).count()
        }
        
        # إحصائيات حسب النوع
        type_stats = db.session.query(
            ComplaintType.name,
            db.func.count(Complaint.id).label('count')
        ).join(Complaint).group_by(ComplaintType.name).all()
        
        stats['by_type'] = [{'type': name, 'count': count} for name, count in type_stats]
        
        # إحصائيات حسب المحافظة
        gov_stats = db.session.query(
            Governorate.name,
            db.func.count(Complaint.id).label('count')
        ).join(Complaint).group_by(Governorate.name).all()
        
        stats['by_governorate'] = [{'governorate': name, 'count': count} for name, count in gov_stats]
        
        return jsonify(stats), 200
        
    except Exception as e:
        logger.error(f"خطأ في الحصول على الإحصائيات: {str(e)}")
        return jsonify({'error': 'حدث خطأ في الحصول على الإحصائيات'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'الصفحة غير موجودة'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'خطأ داخلي في الخادم'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'طلب غير صحيح'}), 400

if __name__ == '__main__':
    # إنشاء قاعدة البيانات
    init_database()
    
    logger.info("=" * 50)
    logger.info("🚀 بدء تشغيل خدمة الشكاوى المبسطة v2.0")
    logger.info("=" * 50)
    logger.info("✅ قاعدة البيانات: SQLite (قابلة للانتقال لـ PostgreSQL)")
    logger.info("✅ الشكاوى: تقديم ومتابعة وتقييم")
    logger.info("✅ المرفقات: مدعومة (16MB حد أقصى)")
    logger.info("✅ التصنيف: حسب النوع والمحافظة والأولوية")
    logger.info("✅ الإحصائيات: شاملة ومفصلة")
    logger.info("=" * 50)
    
    app.run(host='0.0.0.0', port=8004, debug=True)
