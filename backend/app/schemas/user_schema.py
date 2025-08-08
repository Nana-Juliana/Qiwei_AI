from marshmallow import Schema, fields, validate

class UserBasicSchema(Schema):
    """用户基本信息验证模式"""
    studentName = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    parentName = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    phone = fields.Str(validate=validate.Length(max=20))
    wechat = fields.Str(validate=validate.Length(max=50))
    studentAge = fields.Str(validate=validate.Length(max=10))
    studentGender = fields.Str(validate=validate.OneOf(['男', '女', '其他']))
    enrollmentDate = fields.Date(allow_none=True)
    totalClasses = fields.Int(allow_none=True)
    completedClasses = fields.Int(allow_none=True)
    attendanceRate = fields.Str(validate=validate.Length(max=10))
    performance = fields.Str(validate=validate.Length(max=50))
    # 课程信息字段
    currentCourse = fields.Str(validate=validate.Length(max=200))
    teacher = fields.Str(validate=validate.Length(max=100))
    classTime = fields.Str(validate=validate.Length(max=200))
    expiryDate = fields.Date(allow_none=True)

class UserStudentSchema(Schema):
    """学员详细信息验证模式"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    age = fields.Str(validate=validate.Length(max=10))
    gender = fields.Str(validate=validate.OneOf(['男', '女', '其他']))
    enrollmentDate = fields.Date(allow_none=True)
    totalClasses = fields.Int(allow_none=True)
    completedClasses = fields.Int(allow_none=True)
    attendanceRate = fields.Str(validate=validate.Length(max=10))
    performance = fields.Str(validate=validate.Length(max=50))
    notes = fields.Str(allow_none=True)

class UserParentSchema(Schema):
    """家长详细信息验证模式"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    relationship = fields.Str(validate=validate.Length(max=50))
    phone = fields.Str(validate=validate.Length(max=20))
    wechat = fields.Str(validate=validate.Length(max=50))
    notes = fields.Str(allow_none=True)

class UserUpdateSchema(Schema):
    """用户更新验证模式"""
    # 嵌套结构支持（向后兼容）
    basicInfo = fields.Nested(UserBasicSchema, allow_none=True)
    studentInfo = fields.Nested(UserStudentSchema, allow_none=True)
    parentInfo = fields.Nested(UserParentSchema, allow_none=True)
    
    # 直接字段支持（前端新格式）
    # 学员信息
    student_name = fields.Str(validate=validate.Length(min=1, max=100))
    student_age = fields.Str(validate=validate.Length(max=10))
    student_gender = fields.Str(validate=validate.OneOf(['男', '女', '其他']))
    enrollment_date = fields.Date(allow_none=True)
    total_classes = fields.Int(allow_none=True)
    completed_classes = fields.Int(allow_none=True)
    attendance_rate = fields.Str(validate=validate.Length(max=10))
    performance = fields.Str(validate=validate.Length(max=50))
    student_notes = fields.Str(allow_none=True)
    
    # 家长信息
    parent_name = fields.Str(validate=validate.Length(min=1, max=100))
    relationship = fields.Str(validate=validate.Length(max=50))
    parent_phone = fields.Str(validate=validate.Length(max=20))
    parent_wechat = fields.Str(validate=validate.Length(max=50))
    parent_notes = fields.Str(allow_none=True)
    
    # 课程信息
    current_course = fields.Str(validate=validate.Length(max=200))
    teacher = fields.Str(validate=validate.Length(max=100))
    class_time = fields.Str(validate=validate.Length(max=200))
    expiry_date = fields.Date(allow_none=True)
