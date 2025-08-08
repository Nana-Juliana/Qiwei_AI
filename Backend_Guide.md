# 后端实现指南

## 技术栈
- **Web框架**: Flask 2.3+
- **数据库**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0+
- **认证**: JWT (PyJWT)
- **数据验证**: Marshmallow

## 核心功能

### 1. 用户信息管理API
- `GET /api/v1/users/{userId}/basic` - 获取用户基本信息
- `GET /api/v1/users/{userId}/student-details` - 获取学员详情
- `GET /api/v1/users/{userId}/parent-details` - 获取家长详情
- `PUT /api/v1/users/{userId}` - 更新用户信息

### 2. AI回复管理API
- `GET /api/v1/ai-responses/{conversationId}` - 获取AI回复
- `POST /api/v1/ai-responses/{conversationId}/send` - 发送给客户

### 3. 模拟客户消息API
- `POST /api/v1/simulate-customer-msg` - 模拟接收客户消息

## 数据库设计

### 核心表结构
```sql
-- 用户表
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    external_userid VARCHAR(100) UNIQUE NOT NULL,
    student_name VARCHAR(100) NOT NULL,
    parent_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    wechat VARCHAR(100),
    student_age VARCHAR(10),
    student_gender VARCHAR(10),
    current_course VARCHAR(200),
    teacher VARCHAR(100),
    class_time VARCHAR(200),
    expiry_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 学员详情表
CREATE TABLE student_details (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    age VARCHAR(20),
    gender VARCHAR(10),
    enrollment_date DATE,
    total_classes INTEGER DEFAULT 0,
    completed_classes INTEGER DEFAULT 0,
    attendance_rate VARCHAR(10),
    performance VARCHAR(50),
    notes TEXT
);

-- 家长详情表
CREATE TABLE parent_details (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50),
    phone VARCHAR(20),
    wechat VARCHAR(100),
    notes TEXT
);

-- 对话表
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    external_userid VARCHAR(100) NOT NULL,
    customer_message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI回复表
CREATE TABLE ai_responses (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    confidence DECIMAL(3,2),
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    status VARCHAR(20) DEFAULT 'generated'
);
```

## 关键API实现

### 模拟客户消息API
```python
@app.route('/api/v1/simulate-customer-msg', methods=['POST'])
def simulate_customer_message():
    data = request.get_json()
    external_userid = data.get("external_userid")
    content = data.get("content")
    
    if not external_userid or not content:
        return jsonify({
            'code': 400,
            'message': '缺少必要参数'
        }), 400
    
    print(f"客户 {external_userid} 发来消息：{content}")
    
    # 创建对话记录
    conversation = ConversationService.create_conversation(
        external_userid=external_userid,
        customer_message=content
    )
    
    # 调用AI服务生成回复
    ai_response = AIService.generate_response(conversation.id, content)
    
    return jsonify({
        'code': 200,
        'message': '消息接收成功',
        'data': {
            'received': True,
            'user': external_userid,
            'message': content,
            'conversation_id': conversation.id,
            'ai_response_id': ai_response.id if ai_response else None
        }
    })
```

### 用户信息API
```python
@app.route('/api/v1/users/<int:user_id>/basic', methods=['GET'])
@jwt_required
def get_user_basic(user_id):
    user = UserService.get_user_basic(user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': user
    })
```

### AI回复API
```python
@app.route('/api/v1/ai-responses/<int:conversation_id>', methods=['GET'])
@jwt_required
def get_ai_response(conversation_id):
    ai_response = AIService.get_ai_response(conversation_id)
    if not ai_response:
        return jsonify({'code': 404, 'message': 'AI回复不存在'}), 404
    
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'content': ai_response.content,
            'generatedAt': ai_response.generated_at.isoformat(),
            'confidence': float(ai_response.confidence) if ai_response.confidence else None
        }
    })
```

## 服务层实现

### UserService
```python
class UserService:
    @staticmethod
    def get_user_basic(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        
        return {
            'studentName': user.student_name,
            'parentName': user.parent_name,
            'phone': user.phone,
            'wechat': user.wechat,
            'studentAge': user.student_age,
            'studentGender': user.student_gender,
            'currentCourse': user.current_course,
            'teacher': user.teacher,
            'classTime': user.class_time,
            'expiryDate': user.expiry_date.strftime('%Y-%m-%d') if user.expiry_date else None
        }
```

### AIService
```python
class AIService:
    @staticmethod
    def generate_response(conversation_id, customer_message):
        # 模拟AI回复生成
        ai_content = f"""尊敬的家长，关于您的咨询：

{customer_message}

我已经收到您的消息，稍后会为您详细回复。如有紧急情况，请直接联系我们的客服热线。"""
        
        # 保存AI回复
        ai_response = AIResponse(
            conversation_id=conversation_id,
            content=ai_content,
            confidence=0.95,
            status='generated'
        )
        db.session.add(ai_response)
        db.session.commit()
        
        return ai_response
```

## 数据模型

### User模型
```python
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    external_userid = db.Column(db.String(100), unique=True, nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    wechat = db.Column(db.String(100))
    student_age = db.Column(db.String(10))
    student_gender = db.Column(db.String(10))
    current_course = db.Column(db.String(200))
    teacher = db.Column(db.String(100))
    class_time = db.Column(db.String(200))
    expiry_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

## 配置文件

### config.py
```python
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://username:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 跨域配置
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
```

## 依赖管理

### requirements.txt
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.3
marshmallow==3.20.1
psycopg2-binary==2.9.7
python-dotenv==1.0.0
gunicorn==21.2.0
pytest==7.4.2
```

## 部署说明

### 开发环境启动
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export FLASK_APP=run.py
export FLASK_ENV=development

# 初始化数据库
flask db init
flask db migrate
flask db upgrade

# 启动服务
flask run
```

### 生产环境部署
```bash
# 使用Gunicorn启动
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## 关键特点

1. **技术栈现代化**: 使用Flask 2.3+和SQLAlchemy 2.0+
2. **架构清晰**: 采用分层架构，职责分离明确
3. **数据安全**: 完善的认证授权和数据验证机制
4. **易于扩展**: 模块化设计，便于功能扩展
5. **模拟功能**: 通过模拟客户消息API测试AI回复生成

## 总结

本后端实现方案基于前端功能需求，提供了完整的用户信息管理和AI回复管理功能。通过模拟客户消息API，可以方便地测试AI回复生成功能，为后续集成真实的AI服务打下基础。

