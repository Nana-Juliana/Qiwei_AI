from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from config import config
from app.models.user import db
from app.api import init_app as init_api

def create_app(config_name='default'):
    """创建Flask应用"""
    app = Flask(__name__, static_folder='static')
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    jwt = JWTManager(app)
    migrate = Migrate(app, db)
    
    # 配置CORS
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # 注册API蓝图
    init_api(app)
    
    # 创建数据库表（仅在开发环境且数据库不存在时）
    if config_name == 'development':
        try:
            with app.app_context():
                db.create_all()
        except Exception as e:
            print(f"⚠️ 数据库初始化失败: {e}")
            print("💡 请运行 python init_db.py 手动初始化数据库")
    
    return app
