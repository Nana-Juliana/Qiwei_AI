#!/usr/bin/env python3
"""
开发环境快速启动脚本
用于快速启动后端开发服务器
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        return False
    print(f"✅ Python版本: {sys.version}")
    return True

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import flask
        import sqlalchemy
        import requests
        print("✅ 核心依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def setup_environment():
    """设置环境变量"""
    # 首先尝试加载 .env 文件
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ 已加载 .env 文件")
    except ImportError:
        print("⚠️ 未安装 python-dotenv，跳过 .env 文件加载")
    except Exception as e:
        print(f"⚠️ 加载 .env 文件失败: {e}")
    
    # 设置默认环境变量（如果 .env 中没有配置）
    default_env_vars = {
        'FLASK_ENV': 'development',
        'FLASK_APP': 'run.py',
        'SECRET_KEY': 'dev-secret-key-change-in-production',
        'JWT_SECRET_KEY': 'jwt-secret-key-change-in-production',
        'DATABASE_URL': 'postgresql://postgres:root1234@localhost:5432/dbname',  # 使用PostgreSQL数据库
        'DEEPSEEK_API_URL': 'https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1',
        'DEEPSEEK_API_KEY': 'qtcLta5Ahc6WdBNZEfDYbmKZ29N3F8tLZ0xycehttB_xrmMytAPp_p858mmwU2mVYpaJmCKbbbCol_XNB9WcQQ'
    }
    
    # 只为未设置的环境变量设置默认值
    for key, value in default_env_vars.items():
        if not os.environ.get(key):
            os.environ[key] = value
            print(f"  📝 设置默认值: {key}")
    
    print("✅ 环境变量配置完成")

def create_dev_database():
    """创建开发数据库"""
    try:
        from app import create_app
        from app.models.user import db
        
        app = create_app('development')
        with app.app_context():
            db.create_all()
            print("✅ 开发数据库已创建")
    except Exception as e:
        print(f"⚠️ 数据库创建失败: {e}")
        print("将在首次运行时自动创建")

def start_server():
    """启动开发服务器"""
    print("\n🚀 启动开发服务器...")
    print("📝 服务器将在 http://localhost:5000 运行")
    print("📝 API文档: http://localhost:5000/api/v1/")
    print("📝 按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "run.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def main():
    """主函数"""
    print("🎯 教育机构客服系统 - 后端开发环境启动")
    print("=" * 50)
    
    # 修复Python路径
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
        print(f"✅ 已添加Python路径: {current_dir}")
    
    # 检查Python版本
    if not check_python_version():
        sys.exit(1)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 设置环境
    setup_environment()
    
    # 创建数据库
    create_dev_database()
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main()
