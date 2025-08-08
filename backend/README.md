# 后端API服务

基于Flask + PostgreSQL + DeepSeek AI的教育机构客服系统后端服务。

## 功能特性

- 用户信息管理（学员和家长信息整合）
- AI智能回复生成（基于DeepSeek API）
- 消息发送服务
- JWT认证授权
- RESTful API设计

## 技术栈

- **Web框架**: Flask 2.3+
- **数据库**: PostgreSQL 14+
- **ORM**: SQLAlchemy 2.0+
- **认证**: JWT (PyJWT)
- **数据验证**: Marshmallow
- **AI服务**: DeepSeek API

## 项目结构

```
backend/
├── app/
│   ├── models/          # 数据模型
│   ├── schemas/         # 数据验证
│   ├── api/            # API路由
│   ├── services/       # 业务逻辑
│   └── utils/          # 工具函数
├── migrations/         # 数据库迁移
├── tests/             # 测试文件
├── config.py          # 配置文件
├── requirements.txt   # 依赖管理
└── run.py            # 启动文件
```

## 安装和运行

### 1. 环境准备

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境配置

复制 `env_example.txt` 为 `.env` 并配置：

```bash
# Flask配置
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# 数据库配置（开发环境使用SQLite）
DATABASE_URL=sqlite:///dev.db

# DeepSeek API配置
DEEPSEEK_API_URL=https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1
DEEPSEEK_API_KEY=your-deepseek-api-key
```

### 3. 数据库初始化

```bash
# 自动初始化（推荐）
python start_dev.py

# 或手动初始化
python init_db.py
```

### 4. 启动服务

```bash
# 开发环境启动
python start_dev.py

# 或直接运行
python run.py
```

### 5. 测试API

```bash
# 基础测试
python test_api.py

# 完整测试（包含认证）
python test_api_improved.py
```

## API接口

### 认证管理

- `POST /api/v1/login` - 用户登录
- `GET /api/v1/verify` - 验证JWT token
- `POST /api/v1/refresh` - 刷新JWT token

### 用户管理

- `GET /api/v1/users/<user_id>/basic` - 获取用户基本信息
- `GET /api/v1/users/<user_id>/student-details` - 获取学员详细信息
- `GET /api/v1/users/<user_id>/parent-details` - 获取家长详细信息
- `PUT /api/v1/users/<user_id>` - 更新用户信息

### AI回复管理

- `POST /api/v1/ai-responses` - 获取AI推荐回复
- `POST /api/v1/send-message` - 发送回复给客户

### 模拟接口

- `POST /api/v1/simulate-customer-msg` - 模拟客户消息

## 测试

```bash
# 运行测试
pytest tests/

# 运行特定测试
pytest tests/test_api.py::test_simulate_customer_message
```

## 部署

### 生产环境

```bash
# 使用Gunicorn启动
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker部署

```bash
# 构建镜像
docker build -t backend-api .

# 运行容器
docker run -p 5000:5000 backend-api
```

## 注意事项

1. 确保PostgreSQL数据库已正确配置
2. DeepSeek API密钥需要有效
3. 生产环境请使用HTTPS
4. 定期备份数据库
5. 监控API调用频率和性能

## 开发说明

- 使用UUID作为用户主键
- 不保存对话和AI回复历史
- 支持中文数据存储
- 完整的错误处理和日志记录
