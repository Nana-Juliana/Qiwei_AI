# 前端API需求文档

## 概述

本文档基于最新前端功能分析，定义了后端需要提供的API接口。前端主要包含两个核心组件：用户信息管理（UserInfoCard）和AI回复管理（AIResponseCard）。

**重要更新：**
- 移除了CRM绑定功能（CRMBindingCard组件已删除）
- 移除了AI回复编辑功能（仅保留显示和发送）
- 移除了课程表功能
- 移除了员工查询功能
- 简化了AI回复管理，只保留核心功能

## 基础信息

- **API基础URL**: `/api/v1`
- **认证方式**: Bearer Token
- **数据格式**: JSON
- **字符编码**: UTF-8

## 1. 用户信息管理API

### 1.1 获取用户基本信息

**接口**: `GET /users/{userId}/basic`

**描述**: 获取用户的基本信息，用于主界面显示

**请求参数**:
- `userId` (path): 用户ID

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "studentName": "Lucy",
    "parentName": "Mrs. Johnson", 
    "phone": "138****1234",
    "wechat": "Mrs_Johnson",
    "studentAge": "5",
    "studentGender": "女",
    "currentCourse": "幼儿英语启蒙A班",
    "teacher": "Emma老师",
    "classTime": "每周三、五 16:00-17:00",
    "expiryDate": "2025-12-31"
  }
}
```

### 1.2 获取学员详细信息

**接口**: `GET /users/{userId}/student-details`

**描述**: 获取学员的详细信息

**请求参数**:
- `userId` (path): 用户ID

**响应示例**:
```json
{
  "code": 200,
  "message": "success", 
  "data": {
    "name": "Lucy",
    "age": "5岁",
    "gender": "女",
    "enrollmentDate": "2024-01-15",
    "totalClasses": 48,
    "completedClasses": 32,
    "attendanceRate": "95%",
    "performance": "优秀",
    "notes": "学习积极性很高，课堂表现优秀，家长配合度良好。"
  }
}
```

### 1.3 获取家长详细信息

**接口**: `GET /users/{userId}/parent-details`

**描述**: 获取家长的详细信息

**请求参数**:
- `userId` (path): 用户ID

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "name": "Mrs. Johnson",
    "relationship": "妈妈",
    "phone": "138****4321", 
    "wechat": "Mrs_Johnson",
    "notes": "对孩子的教育非常重视，经常与老师沟通学习情况，较难沟通。"
  }
}
```

### 1.4 更新用户信息

**接口**: `PUT /users/{userId}`

**描述**: 更新用户的所有信息（包括学员和家长信息）

**请求参数**:
- `userId` (path): 用户ID

**请求体**:
```json
{
  "studentInfo": {
    "name": "Lucy",
    "age": "5岁",
    "gender": "女", 
    "enrollmentDate": "2024-01-15",
    "totalClasses": 48,
    "completedClasses": 32,
    "attendanceRate": "95%",
    "performance": "优秀",
    "notes": "学习积极性很高，课堂表现优秀，家长配合度良好。"
  },
  "parentInfo": {
    "name": "Mrs. Johnson",
    "relationship": "妈妈",
    "phone": "138****4321",
    "wechat": "Mrs_Johnson", 
    "notes": "对孩子的教育非常重视，经常与老师沟通学习情况，较难沟通。"
  },
  "basicInfo": {
    "studentName": "Lucy",
    "parentName": "Mrs. Johnson",
    "phone": "138****1234",
    "wechat": "Mrs_Johnson",
    "studentAge": "5",
    "studentGender": "女",
    "currentCourse": "幼儿英语启蒙A班",
    "teacher": "Emma老师",
    "classTime": "每周三、五 16:00-17:00",
    "expiryDate": "2025-12-31"
  }
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "userId": "12345",
    "updatedAt": "2024-01-15T10:30:00Z"
  }
}
```

## 2. 认证管理API

### 2.1 用户登录

**接口**: `POST /login`

**描述**: 用户登录获取JWT访问令牌

**请求体**:
```json
{
  "external_userid": "test_user_123"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": "1",
    "external_userid": "test_user_123",
    "token_type": "Bearer"
  }
}
```

### 2.2 验证Token

**接口**: `GET /verify`

**描述**: 验证JWT token是否有效

**请求头**:
- `Authorization`: Bearer {access_token}

**响应示例**:
```json
{
  "code": 200,
  "message": "token有效",
  "data": {
    "user_id": "1",
    "external_userid": "test_user_123",
    "student_name": "Lucy",
    "parent_name": "Mrs. Johnson"
  }
}
```

### 2.3 刷新Token

**接口**: `POST /refresh`

**描述**: 刷新JWT访问令牌

**请求头**:
- `Authorization`: Bearer {access_token}

**响应示例**:
```json
{
  "code": 200,
  "message": "token刷新成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer"
  }
}
```

## 3. AI回复管理API

### 3.1 生成AI推荐回复

**接口**: `POST /ai-responses`

**描述**: 基于客户消息内容生成AI推荐回复

**请求头**:
- `Authorization`: Bearer {access_token}

**请求体**:
```json
{
  "message": "请问课程安排如何？我想了解一下英语课程",
  "external_userid": "test_user_123"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "content": "尊敬的家长，关于英语课程安排：\n\n1. 本周四的课程将正常进行\n2. 您询问的教材已到货，可随时领取\n3. 下月将有一次家长开放日，稍后我会发送详细通知",
    "generatedAt": "2024-01-15T10:30:00Z",
    "confidence": 0.95
  }
}
```

### 3.2 发送回复给客户

**接口**: `POST /send-message`

**描述**: 将回复内容发送给客户

**请求头**:
- `Authorization`: Bearer {access_token}

**请求体**:
```json
{
  "content": "尊敬的家长，关于英语课程安排：\n\n1. 本周四的课程将正常进行\n2. 您询问的教材已到货，可随时领取\n3. 下月将有一次家长开放日，稍后我会发送详细通知",
  "sendMethod": "wechat",
  "customerId": "test_user_123"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "发送成功",
  "data": {
    "messageId": "msg_1704456123",
    "sentAt": "2024-01-15T10:30:00Z",
    "status": "sent"
  }
}
```

### 3.3 模拟客户消息（测试接口）

**接口**: `POST /simulate-customer-msg`

**描述**: 模拟客户发送消息并自动生成AI回复（无需认证，用于测试）

**请求体**:
```json
{
  "external_userid": "test_user_123",
  "content": "请问课程安排如何？我想了解一下数学课程"
}
```

**响应示例**:
```json
{
  "code": 200,
  "message": "消息接收成功",
  "data": {
    "received": true,
    "user": "test_user_123",
    "message": "请问课程安排如何？我想了解一下数学课程",
    "ai_response": "尊敬的家长，关于数学课程安排，我来为您详细介绍...",
    "generated_at": "2024-01-15T10:30:00Z"
  }
}
```

> **注意**: 根据最新前端代码，已移除了员工查询功能，因此不再需要员工相关的API接口。

## 4. 通用错误响应

### 4.1 错误响应格式

```json
{
  "code": 400,
  "message": "请求参数错误",
  "error": {
    "field": "userId",
    "detail": "用户ID不能为空"
  }
}
```

### 4.2 常见错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 401 | 未授权访问 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 5. 数据模型

### 5.1 用户基本信息模型

```json
{
  "studentName": "string",      // 学员姓名
  "parentName": "string",       // 家长姓名
  "phone": "string",           // 联系电话
  "wechat": "string",          // 微信号
  "studentAge": "string",      // 学员年龄
  "studentGender": "string",   // 学员性别
  "currentCourse": "string",   // 当前课程
  "teacher": "string",         // 教师姓名
  "classTime": "string",       // 上课时间
  "expiryDate": "string"       // 到期日期
}
```

### 5.2 学员详细信息模型

```json
{
  "name": "string",            // 学员姓名
  "age": "string",             // 年龄
  "gender": "string",          // 性别
  "enrollmentDate": "string",  // 入学日期
  "totalClasses": "number",    // 总课时
  "completedClasses": "number", // 已完成课时
  "attendanceRate": "string",  // 出勤率
  "performance": "string",     // 表现评级
  "notes": "string"            // 备注
}
```

### 5.3 家长详细信息模型

```json
{
  "name": "string",            // 家长姓名
  "relationship": "string",    // 关系
  "phone": "string",          // 联系电话
  "wechat": "string",         // 微信号
  "notes": "string"           // 备注
}
```

### 5.4 AI回复模型

```json
{
  "content": "string",         // AI回复内容
  "generatedAt": "string",     // 生成时间
  "confidence": "number"       // 置信度 (0-1)
}
```

### 5.5 消息发送模型

```json
{
  "messageId": "string",       // 消息ID
  "sentAt": "string",          // 发送时间
  "status": "string"           // 发送状态
}
```

## 6. 前端功能映射

### 6.1 UserInfoCard组件功能

| 前端功能 | 对应API | 说明 |
|----------|---------|------|
| 显示基本信息 | GET /users/{userId}/basic | 主界面显示用户基本信息 |
| 显示学员详情 | GET /users/{userId}/student-details | 学员详情弹窗 |
| 显示家长详情 | GET /users/{userId}/parent-details | 家长详情弹窗 |
| 编辑用户信息 | PUT /users/{userId} | 统一编辑学员和家长信息 |

### 6.2 AIResponseCard组件功能

| 前端功能 | 对应API | 说明 |
|----------|---------|------|
| 生成AI回复 | POST /ai-responses | 基于消息内容生成AI推荐回复 |
| 发送给客户 | POST /send-message | 发送回复给客户 |
| 一键复制 | 前端本地功能 | 复制内容到剪贴板 |

### 6.3 认证相关功能

| 前端功能 | 对应API | 说明 |
|----------|---------|------|
| 用户登录 | POST /login | 获取访问令牌 |
| Token验证 | GET /verify | 验证令牌有效性 |
| Token刷新 | POST /refresh | 刷新访问令牌 |

> **注意**: 已移除员工查询功能，AI回复编辑功能也已移除。

## 7. 部署建议

### 7.1 环境配置

- **开发环境**: `http://localhost:5000/api/v1`
- **测试环境**: `https://test-api.example.com/api/v1`
- **生产环境**: `https://api.example.com/api/v1`

### 7.2 安全要求

- 所有API请求需要携带有效的Bearer Token
- 敏感信息（如手机号）需要脱敏处理
- 实现请求频率限制防止滥用
- 支持HTTPS加密传输

### 7.3 性能要求

- API响应时间 < 500ms
- 支持并发请求处理
- 实现数据缓存机制
- 提供API版本控制

## 8. 测试建议

### 8.1 单元测试

- 测试所有API端点的正常流程
- 测试错误处理和边界情况
- 测试数据验证和格式检查

### 8.2 集成测试

- 测试前后端数据交互
- 测试用户认证和授权
- 测试数据一致性

### 8.3 性能测试

- 测试API响应时间
- 测试并发处理能力
- 测试数据量增长时的性能表现

## 9. 更新总结

### 9.1 移除的功能

根据最新前端代码分析，以下功能已被移除：

1. **CRM绑定功能**
   - 删除了CRMBindingCard组件
   - 不再需要CRM相关的API接口

2. **AI回复编辑功能**
   - 移除了AI回复的编辑按钮和编辑状态
   - 仅保留显示和发送功能

3. **课程表功能**
   - 移除了课程表按钮和模态框
   - 不再需要课程表相关的API接口

4. **员工查询功能**
   - 移除了"查询相关员工"按钮
   - 移除了员工列表显示
   - 不再需要员工相关的API接口

### 9.2 保留的核心功能

1. **用户信息管理**
   - 学员和家长信息显示
   - 详细信息查看（学员详情、家长详情）
   - 统一编辑功能

2. **AI回复管理**
   - AI推荐回复生成
   - 发送给客户功能
   - 一键复制功能（前端本地）

3. **认证管理**
   - 用户登录认证
   - Token验证和刷新
   - 安全访问控制

### 9.3 API接口精简

**最终需要的API接口（共9个）：**

1. **认证管理API（3个）：**
   - `POST /login` - 用户登录
   - `GET /verify` - 验证Token
   - `POST /refresh` - 刷新Token

2. **用户管理API（4个）：**
   - `GET /users/{userId}/basic` - 获取基本信息
   - `GET /users/{userId}/student-details` - 获取学员详情
   - `GET /users/{userId}/parent-details` - 获取家长详情
   - `PUT /users/{userId}` - 更新用户信息

3. **AI回复管理API（3个）：**
   - `POST /ai-responses` - 生成AI回复
   - `POST /send-message` - 发送消息给客户
   - `POST /simulate-customer-msg` - 模拟客户消息（测试用）

**移除的API接口：**
- `GET /staff/related/{conversationId}` - 获取相关员工信息
- 所有CRM绑定相关的API接口
- 原有的基于conversationId的AI回复接口 