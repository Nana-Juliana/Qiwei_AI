#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
数据库查询脚本
用于查看当前数据库中的所有用户数据
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# 添加项目路径到sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置PostgreSQL数据库URL环境变量（与init_db.py保持一致）
os.environ['DATABASE_URL'] = 'postgresql://postgres:root1234@localhost:5432/dbname'

def query_database():
    """查询数据库中的所有数据"""
    
    # 使用环境变量中的数据库连接URL
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    print("🔍 正在连接数据库...")
    print(f"📡 数据库URL: {DATABASE_URL}")
    print("=" * 60)
    
    try:
        # 创建数据库引擎
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()
        
        print("✅ 数据库连接成功！")
        
        # 1. 查看数据库基本信息
        print("\n📊 数据库基本信息：")
        print("-" * 40)
        
        # 当前数据库名
        db_name = session.execute(text("SELECT current_database()")).scalar()
        print(f"数据库名称: {db_name}")
        
        # 当前时间
        db_time = session.execute(text("SELECT NOW()")).scalar()
        print(f"数据库时间: {db_time}")
        
        # 2. 查看所有表
        print("\n📋 数据库中的表：")
        print("-" * 40)
        
        tables_query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = session.execute(tables_query).fetchall()
        
        if tables:
            for table in tables:
                print(f"• {table[0]}")
        else:
            print("暂无表")
        
        # 3. 查看users表结构（如果存在）
        if any(table[0] == 'users' for table in tables):
            print("\n🏗️ users表结构：")
            print("-" * 40)
            
            columns_query = text("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'users' AND table_schema = 'public'
                ORDER BY ordinal_position
            """)
            columns = session.execute(columns_query).fetchall()
            
            for col in columns:
                nullable = "可空" if col[2] == "YES" else "非空"
                default = f"默认值: {col[3]}" if col[3] else "无默认值"
                print(f"• {col[0]:<20} {col[1]:<15} {nullable:<6} {default}")
        
        # 4. 查看users表数据
        if any(table[0] == 'users' for table in tables):
            print("\n👥 users表数据：")
            print("-" * 40)
            
            # 查询用户总数
            count_query = text("SELECT COUNT(*) FROM users")
            user_count = session.execute(count_query).scalar()
            print(f"用户总数: {user_count}")
            
            if user_count > 0:
                # 查询所有用户数据
                users_query = text("""
                    SELECT 
                        id, external_userid, student_name, parent_name, 
                        parent_phone, student_age, student_gender,
                        current_course, teacher, class_time, 
                        created_at, updated_at
                    FROM users 
                    ORDER BY created_at DESC
                """)
                users = session.execute(users_query).fetchall()
                
                print("\n用户列表:")
                print("=" * 120)
                
                for i, user in enumerate(users, 1):
                    print(f"\n【用户 {i}】")
                    print(f"ID: {user[0]}")
                    print(f"External ID: {user[1]}")
                    print(f"学员姓名: {user[2] or '未设置'}")
                    print(f"家长姓名: {user[3] or '未设置'}")
                    print(f"家长电话: {user[4] or '未设置'}")
                    print(f"学员年龄: {user[5] or '未设置'}")
                    print(f"学员性别: {user[6] or '未设置'}")
                    print(f"当前课程: {user[7] or '未设置'}")
                    print(f"授课教师: {user[8] or '未设置'}")
                    print(f"上课时间: {user[9] or '未设置'}")
                    print(f"创建时间: {user[10]}")
                    print(f"更新时间: {user[11]}")
                    print("-" * 60)
                
                # 5. 查询特定测试用户
                print(f"\n🔍 查询测试用户 (external_userid='test_user_123'):")
                print("-" * 40)
                
                test_user_query = text("""
                    SELECT * FROM users WHERE external_userid = 'test_user_123'
                """)
                test_user = session.execute(test_user_query).fetchone()
                
                if test_user:
                    print("✅ 找到测试用户！")
                    print("详细信息请查看上方用户列表")
                else:
                    print("❌ 未找到测试用户 'test_user_123'")
            else:
                print("数据库中暂无用户数据")
        else:
            print("\n❌ 未找到users表，请先运行数据库初始化脚本")
        
        print(f"\n{'='*60}")
        print("🎉 数据库查询完成！")
        
    except Exception as e:
        print(f"❌ 数据库查询失败: {e}")
        print("\n可能的解决方案:")
        print("1. 确认PostgreSQL服务正在运行")
        print("2. 确认数据库连接信息正确")
        print("3. 确认数据库dbname已创建")
        print("4. 运行 python init_db.py 初始化数据库")
        
    finally:
        try:
            session.close()
            print("🔐 数据库连接已关闭")
        except:
            pass

if __name__ == "__main__":
    print("📂 数据库数据查询工具")
    print("=" * 60)
    query_database()
