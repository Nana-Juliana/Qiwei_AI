#!/usr/bin/env python3
"""
数据库初始化脚本
用于手动初始化数据库和创建测试数据
"""

import os
import sys
from pathlib import Path

# 修复Python路径
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# 设置PostgreSQL数据库URL环境变量
os.environ['DATABASE_URL'] = 'postgresql://postgres:root1234@localhost:5432/dbname'

from app import create_app
from app.models.user import db, User
from datetime import datetime

def init_database():
    """初始化数据库"""
    print("🗄️ 开始初始化数据库...")
    print(f"📡 数据库URL: {os.environ.get('DATABASE_URL')}")
    
    try:
        # 创建应用
        app = create_app('development')
        
        with app.app_context():
            # 验证数据库连接
            print(f"🔍 当前数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
            
            # 测试数据库连接
            try:
                db.engine.connect()
                print("✅ 数据库连接成功")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                raise
            
            # 删除所有表（如果存在）
            db.drop_all()
            print("✅ 已删除现有表")
            
            # 创建所有表
            db.create_all()
            print("✅ 已创建数据库表")
            
            # 创建测试数据
            create_test_data()
            
            print("🎉 数据库初始化完成！")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False
    
    return True

def create_test_data():
    """创建测试数据"""
    print("📝 创建测试数据...")
    
    # 创建测试用户
    test_users = [
        {
            'external_userid': 'test_user_123',
            'student_name': '张三',
            'student_age': '10',
            'student_gender': '男',
            'enrollment_date': datetime.strptime('2024-01-15', '%Y-%m-%d').date(),
            'total_classes': 20,
            'completed_classes': 15,
            'attendance_rate': '85%',
            'performance': '优秀',
            'student_notes': '学习认真，表现良好',
            'parent_name': '张父',
            'relationship': '父亲',
            'parent_phone': '13800138000',
            'parent_wechat': 'zhangfu123',
            'parent_notes': '家长配合度高',
            # 课程信息
            'current_course': '小学数学提高班',
            'teacher': '王老师',
            'class_time': '每周二、四 18:00-19:30',
            'expiry_date': datetime.strptime('2024-12-31', '%Y-%m-%d').date()
        },
        {
            'external_userid': 'test_user_456',
            'student_name': '李四',
            'student_age': '12',
            'student_gender': '女',
            'enrollment_date': datetime.strptime('2024-02-01', '%Y-%m-%d').date(),
            'total_classes': 15,
            'completed_classes': 12,
            'attendance_rate': '90%',
            'performance': '良好',
            'student_notes': '英语基础较好',
            'parent_name': '李母',
            'relationship': '母亲',
            'parent_phone': '13900139000',
            'parent_wechat': 'limu456',
            'parent_notes': '关注孩子学习进度',
            # 课程信息
            'current_course': '初中英语强化班',
            'teacher': '刘老师',
            'class_time': '每周一、三、五 19:00-20:30',
            'expiry_date': datetime.strptime('2025-06-30', '%Y-%m-%d').date()
        },
        {
            'external_userid': 'demo_parent_001',
            'student_name': 'Lucy',
            'student_age': '5',
            'student_gender': '女',
            'enrollment_date': datetime.strptime('2024-01-15', '%Y-%m-%d').date(),
            'total_classes': 48,
            'completed_classes': 32,
            'attendance_rate': '95%',
            'performance': '优秀',
            'student_notes': '学习积极性很高，课堂表现优秀，家长配合度良好。',
            'parent_name': 'Mrs. Johnson',
            'relationship': '妈妈',
            'parent_phone': '138****4321',
            'parent_wechat': 'Mrs_Johnson',
            'parent_notes': '对孩子的教育非常重视，经常与老师沟通学习情况，较难沟通。',
            # 课程信息
            'current_course': '幼儿英语启蒙A班',
            'teacher': 'Emma老师',
            'class_time': '每周三、五 16:00-17:00',
            'expiry_date': datetime.strptime('2025-12-31', '%Y-%m-%d').date()
        }
    ]
    
    for user_data in test_users:
        user = User(**user_data)
        db.session.add(user)
        print(f"  ✅ 创建用户: {user_data['student_name']} ({user_data['external_userid']})")
    
    db.session.commit()
    print(f"✅ 已创建 {len(test_users)} 个测试用户")

def main():
    """主函数"""
    print("🎯 教育机构客服系统 - 数据库初始化")
    print("=" * 50)
    print(f"🗄️ 目标数据库: PostgreSQL")
    print(f"📡 连接地址: postgresql://postgres:***@localhost:5432/dbname")
    print("=" * 50)
    
    # 确认操作
    response = input("⚠️ 此操作将删除现有PostgreSQL数据库并重新创建，确定继续吗？(y/N): ")
    if response.lower() != 'y':
        print("❌ 操作已取消")
        return
    
    # 初始化数据库
    if init_database():
        print("\n💡 数据库初始化成功！")
        print("💡 现在可以启动后端服务了")
        print("💡 运行命令: python run.py")
    else:
        print("\n❌ 数据库初始化失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
