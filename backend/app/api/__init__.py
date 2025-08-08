from .user_api import user_bp
from .ai_api import ai_bp
from .simulation_api import simulation_bp
from .auth_api import auth_bp
from flask import Blueprint, jsonify

# 创建根路径蓝图
root_bp = Blueprint('root', __name__)

@root_bp.route('/')
def index():
    """根路径 - API服务状态页面"""
    html_content = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>教育机构客服系统 - API服务</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .status {
            background: rgba(76, 175, 80, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 4px solid #4CAF50;
        }
        .api-section {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .api-section h3 {
            margin-top: 0;
            color: #FFD700;
        }
        .endpoint {
            background: rgba(0, 0, 0, 0.2);
            padding: 10px;
            border-radius: 5px;
            margin: 5px 0;
            font-family: 'Courier New', monospace;
            border-left: 3px solid #FFD700;
        }
        .test-button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 5px;
            font-size: 14px;
        }
        .test-button:hover {
            background: #45a049;
        }
        .response {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px;
            border-radius: 5px;
            margin-top: 10px;
            font-family: 'Courier New', monospace;
            white-space: pre-wrap;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 教育机构客服系统</h1>
        
        <div class="status">
            <h2>✅ 服务状态</h2>
            <p>API服务运行正常，版本 1.0.0</p>
            <p>服务器时间: <span id="server-time"></span></p>
        </div>

        <div class="api-section">
            <h3>📡 可用API接口</h3>
            
            <h4>认证管理</h4>
            <div class="endpoint">POST /api/v1/login</div>
            <div class="endpoint">GET /api/v1/verify</div>
            <div class="endpoint">POST /api/v1/refresh</div>
            
            <h4>用户管理</h4>
            <div class="endpoint">GET /api/v1/users/{user_id}/basic</div>
            <div class="endpoint">GET /api/v1/users/{user_id}/student-details</div>
            <div class="endpoint">GET /api/v1/users/{user_id}/parent-details</div>
            <div class="endpoint">PUT /api/v1/users/{user_id}</div>
            
            <h4>AI回复管理</h4>
            <div class="endpoint">POST /api/v1/ai-responses</div>
            <div class="endpoint">POST /api/v1/send-message</div>
            
            <h4>模拟接口</h4>
            <div class="endpoint">POST /api/v1/simulate-customer-msg</div>
        </div>

        <div class="api-section">
            <h3>🧪 快速测试</h3>
            <button class="test-button" onclick="testHealth()">健康检查</button>
            <button class="test-button" onclick="testLogin()">测试登录</button>
            <button class="test-button" onclick="testSimulation()">测试模拟消息</button>
            <div id="response" class="response"></div>
        </div>

        <div class="api-section">
            <h3>📚 使用说明</h3>
            <p>• 所有API接口都需要在URL前加上 <code>http://localhost:5000</code></p>
            <p>• 用户管理和AI回复管理接口需要JWT认证</p>
            <p>• 模拟客户消息接口无需认证，可直接测试</p>
            <p>• 建议使用Postman或其他API测试工具进行测试</p>
        </div>
    </div>

    <script>
        // 显示服务器时间
        document.getElementById('server-time').textContent = new Date().toLocaleString('zh-CN');

        // 测试健康检查
        async function testHealth() {
            const response = document.getElementById('response');
            response.style.display = 'block';
            response.textContent = '正在测试健康检查...';
            
            try {
                const res = await fetch('/health');
                const data = await res.json();
                response.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                response.textContent = '测试失败: ' + error.message;
            }
        }

        // 测试登录
        async function testLogin() {
            const response = document.getElementById('response');
            response.style.display = 'block';
            response.textContent = '正在测试登录...';
            
            try {
                const res = await fetch('/api/v1/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        external_userid: 'test_user_456'
                    })
                });
                const data = await res.json();
                response.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                response.textContent = '测试失败: ' + error.message;
            }
        }

        // 测试模拟消息
        async function testSimulation() {
            const response = document.getElementById('response');
            response.style.display = 'block';
            response.textContent = '正在测试模拟消息...';
            
            try {
                const res = await fetch('/api/v1/simulate-customer-msg', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        external_userid: 'test_user_456',
                        content: '请问课程安排如何？我想了解一下数学课程的价格'
                    })
                });
                const data = await res.json();
                response.textContent = JSON.stringify(data, null, 2);
            } catch (error) {
                response.textContent = '测试失败: ' + error.message;
            }
        }
    </script>
</body>
</html>
    """
    return html_content

@root_bp.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'code': 200,
        'message': '服务健康',
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z'
    })

def init_app(app):
    """初始化API蓝图"""
    # 注册根路径蓝图（无前缀）
    app.register_blueprint(root_bp)
    
    # 注册API蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(user_bp, url_prefix='/api/v1')
    app.register_blueprint(ai_bp, url_prefix='/api/v1')
    app.register_blueprint(simulation_bp, url_prefix='/api/v1')
