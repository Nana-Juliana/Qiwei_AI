from datetime import datetime
from app.models.user import User, db
from flask import current_app

class UserService:
    @staticmethod
    def get_user_basic(user_id):
        """获取用户基本信息"""
        try:
            # 支持通过UUID或external_userid查询
            if isinstance(user_id, str) and len(user_id) > 20:
                # 可能是UUID
                user = User.query.get(user_id)
            else:
                # 可能是external_userid
                user = User.query.filter_by(external_userid=user_id).first()
            
            if not user:
                current_app.logger.warning(f"用户不存在: {user_id}")
                return None
            
            return {
                'studentName': user.student_name,
                'parentName': user.parent_name,
                'phone': user.parent_phone,
                'wechat': user.parent_wechat,
                'studentAge': user.student_age,
                'studentGender': user.student_gender,
                'currentCourse': user.current_course,
                'teacher': user.teacher,
                'classTime': user.class_time,
                'expiryDate': user.expiry_date.strftime('%Y-%m-%d') if user.expiry_date else None
            }
        except Exception as e:
            current_app.logger.error(f"获取用户基本信息失败: {str(e)}")
            return None
    
    @staticmethod
    def get_student_details(user_id):
        """获取学员详细信息"""
        try:
            # 支持通过UUID或external_userid查询
            if isinstance(user_id, str) and len(user_id) > 20:
                user = User.query.get(user_id)
            else:
                user = User.query.filter_by(external_userid=user_id).first()
            
            if not user:
                current_app.logger.warning(f"学员信息不存在: {user_id}")
                return None
            
            return {
                'name': user.student_name,
                'age': user.student_age,
                'gender': user.student_gender,
                'enrollmentDate': user.enrollment_date.strftime('%Y-%m-%d') if user.enrollment_date else None,
                'totalClasses': user.total_classes,
                'completedClasses': user.completed_classes,
                'attendanceRate': user.attendance_rate,
                'performance': user.performance,
                'notes': user.student_notes
            }
        except Exception as e:
            current_app.logger.error(f"获取学员详细信息失败: {str(e)}")
            return None
    
    @staticmethod
    def get_parent_details(user_id):
        """获取家长详细信息"""
        try:
            # 支持通过UUID或external_userid查询
            if isinstance(user_id, str) and len(user_id) > 20:
                user = User.query.get(user_id)
            else:
                user = User.query.filter_by(external_userid=user_id).first()
            
            if not user:
                current_app.logger.warning(f"家长信息不存在: {user_id}")
                return None
            
            return {
                'name': user.parent_name,
                'relationship': user.relationship,
                'phone': user.parent_phone,
                'wechat': user.parent_wechat,
                'notes': user.parent_notes
            }
        except Exception as e:
            current_app.logger.error(f"获取家长详细信息失败: {str(e)}")
            return None
    
    @staticmethod
    def update_user(user_id, data):
        """更新用户信息"""
        try:
            # 支持通过UUID或external_userid查询
            if isinstance(user_id, str) and len(user_id) > 20:
                user = User.query.get(user_id)
            else:
                user = User.query.filter_by(external_userid=user_id).first()
            
            if not user:
                raise ValueError('用户不存在')
            
            # 更新基本信息
            if 'basicInfo' in data:
                basic_info = data['basicInfo']
                user.student_name = basic_info.get('studentName', user.student_name)
                user.parent_name = basic_info.get('parentName', user.parent_name)
                user.parent_phone = basic_info.get('phone', user.parent_phone)
                user.parent_wechat = basic_info.get('wechat', user.parent_wechat)
                user.student_age = basic_info.get('studentAge', user.student_age)
                user.student_gender = basic_info.get('studentGender', user.student_gender)
                
                # 安全处理日期
                enrollment_date = basic_info.get('enrollmentDate')
                if enrollment_date:
                    user.enrollment_date = User.parse_date(enrollment_date)
                
                user.total_classes = basic_info.get('totalClasses', user.total_classes)
                user.completed_classes = basic_info.get('completedClasses', user.completed_classes)
                user.attendance_rate = basic_info.get('attendanceRate', user.attendance_rate)
                user.performance = basic_info.get('performance', user.performance)
                
                # 更新课程信息
                user.current_course = basic_info.get('currentCourse', user.current_course)
                user.teacher = basic_info.get('teacher', user.teacher)
                user.class_time = basic_info.get('classTime', user.class_time)
                
                # 安全处理到期日期
                expiry_date = basic_info.get('expiryDate')
                if expiry_date:
                    user.expiry_date = User.parse_date(expiry_date)
            
            # 更新学员详情
            if 'studentInfo' in data:
                student_info = data['studentInfo']
                user.student_name = student_info.get('name', user.student_name)
                user.student_age = student_info.get('age', user.student_age)
                user.student_gender = student_info.get('gender', user.student_gender)
                
                # 安全处理日期
                enrollment_date = student_info.get('enrollmentDate')
                if enrollment_date:
                    user.enrollment_date = User.parse_date(enrollment_date)
                
                user.total_classes = student_info.get('totalClasses', user.total_classes)
                user.completed_classes = student_info.get('completedClasses', user.completed_classes)
                user.attendance_rate = student_info.get('attendanceRate', user.attendance_rate)
                user.performance = student_info.get('performance', user.performance)
                user.student_notes = student_info.get('notes', user.student_notes)
            
            # 更新家长详情
            if 'parentInfo' in data:
                parent_info = data['parentInfo']
                user.parent_name = parent_info.get('name', user.parent_name)
                user.relationship = parent_info.get('relationship', user.relationship)
                user.parent_phone = parent_info.get('phone', user.parent_phone)
                user.parent_wechat = parent_info.get('wechat', user.parent_wechat)
                user.parent_notes = parent_info.get('notes', user.parent_notes)
            
            # 处理直接传递的字段（前端新的数据格式）
            if 'student_name' in data:
                user.student_name = data.get('student_name', user.student_name)
            if 'student_age' in data:
                user.student_age = data.get('student_age', user.student_age)
            if 'student_gender' in data:
                user.student_gender = data.get('student_gender', user.student_gender)
            if 'parent_name' in data:
                user.parent_name = data.get('parent_name', user.parent_name)
            if 'parent_phone' in data:
                user.parent_phone = data.get('parent_phone', user.parent_phone)
            if 'parent_wechat' in data:
                user.parent_wechat = data.get('parent_wechat', user.parent_wechat)
            if 'relationship' in data:
                user.relationship = data.get('relationship', user.relationship)
            if 'parent_notes' in data:
                user.parent_notes = data.get('parent_notes', user.parent_notes)
            if 'enrollment_date' in data:
                enrollment_date = data.get('enrollment_date')
                if enrollment_date:
                    user.enrollment_date = User.parse_date(enrollment_date)
            if 'total_classes' in data:
                user.total_classes = data.get('total_classes', user.total_classes)
            if 'completed_classes' in data:
                user.completed_classes = data.get('completed_classes', user.completed_classes)
            if 'attendance_rate' in data:
                user.attendance_rate = data.get('attendance_rate', user.attendance_rate)
            if 'performance' in data:
                user.performance = data.get('performance', user.performance)
            if 'student_notes' in data:
                user.student_notes = data.get('student_notes', user.student_notes)
            
            # 处理课程信息字段
            if 'current_course' in data:
                user.current_course = data.get('current_course', user.current_course)
            if 'teacher' in data:
                user.teacher = data.get('teacher', user.teacher)
            if 'class_time' in data:
                user.class_time = data.get('class_time', user.class_time)
            if 'expiry_date' in data:
                expiry_date = data.get('expiry_date')
                if expiry_date:
                    user.expiry_date = User.parse_date(expiry_date)
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            current_app.logger.info(f"用户信息更新成功: {user_id}")
            return user
            
        except ValueError as e:
            current_app.logger.warning(f"用户更新失败 - 用户不存在: {user_id}")
            raise
        except Exception as e:
            current_app.logger.error(f"用户更新失败: {str(e)}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_user_by_external_id(external_userid):
        """根据外部用户ID获取用户"""
        try:
            return User.query.filter_by(external_userid=external_userid).first()
        except Exception as e:
            current_app.logger.error(f"根据外部ID查询用户失败: {str(e)}")
            return None
    
    @staticmethod
    def create_user(external_userid, **kwargs):
        """创建新用户"""
        try:
            user = User(external_userid=external_userid, **kwargs)
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"新用户创建成功: {external_userid}")
            return user
        except Exception as e:
            current_app.logger.error(f"创建用户失败: {str(e)}")
            db.session.rollback()
            raise
