import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_userid = db.Column(db.String(100), unique=True, nullable=False)
    
    # 学员信息
    student_name = db.Column(db.String(100))
    student_age = db.Column(db.String(10))
    student_gender = db.Column(db.String(10))
    enrollment_date = db.Column(db.Date)
    total_classes = db.Column(db.Integer, default=0)
    completed_classes = db.Column(db.Integer, default=0)
    attendance_rate = db.Column(db.String(10))
    performance = db.Column(db.String(50))
    student_notes = db.Column(db.Text)
    
    # 家长信息
    parent_name = db.Column(db.String(100))
    relationship = db.Column(db.String(50))
    parent_phone = db.Column(db.String(20))
    parent_wechat = db.Column(db.String(50))
    parent_notes = db.Column(db.Text)
    
    # 课程信息
    current_course = db.Column(db.String(200))
    teacher = db.Column(db.String(100))
    class_time = db.Column(db.String(200))
    expiry_date = db.Column(db.Date)
    
    # 系统字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': str(self.id),
            'external_userid': self.external_userid,
            'student_name': self.student_name,
            'student_age': self.student_age,
            'student_gender': self.student_gender,
            'enrollment_date': self.enrollment_date.strftime('%Y-%m-%d') if self.enrollment_date else None,
            'total_classes': self.total_classes,
            'completed_classes': self.completed_classes,
            'attendance_rate': self.attendance_rate,
            'performance': self.performance,
            'student_notes': self.student_notes,
            'parent_name': self.parent_name,
            'relationship': self.relationship,
            'parent_phone': self.parent_phone,
            'parent_wechat': self.parent_wechat,
            'parent_notes': self.parent_notes,
            'current_course': self.current_course,
            'teacher': self.teacher,
            'class_time': self.class_time,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def parse_date(date_str):
        """安全解析日期字符串"""
        if not date_str:
            return None
        try:
            if isinstance(date_str, str):
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            elif isinstance(date_str, datetime):
                return date_str.date()
            return date_str
        except (ValueError, TypeError):
            return None
