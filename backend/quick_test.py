#!/usr/bin/env python3
"""
快速测试脚本 - 验证API服务是否正常运行
"""

import requests
import json
import time

def test_root_endpoint():
    """测试根路径"""
    print("=== 测试根路径 ===")
    try:
        response = requests.get('http://localhost:5000/')
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 根路径访问成功！")
            if '<html' in response.text:
                print("✅ HTML页面正常显示")
            else:
                print("⚠️ 返回的是JSON而不是HTML")
        else:
            print("❌ 根路径访问失败")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_health_endpoint():
    """测试健康检查"""
    print("\n=== 测试健康检查 ===")
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 健康检查通过: {data.get('message', 'N/A')}")
            return True
        else:
            print("❌ 健康检查失败")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_simulation_endpoint():
    """测试模拟消息接口"""
    print("\n=== 测试模拟消息接口 ===")
    try:
        data = {
            "external_userid": "test_user_123",
            "content": "请问课程安排如何？我想了解一下英语课程"
        }
        response = requests.post('http://localhost:5000/api/v1/simulate-customer-msg', json=data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ 模拟消息接口正常")
            print(f"AI回复: {result.get('data', {}).get('ai_response', 'N/A')[:100]}...")
            return True
        else:
            print("❌ 模拟消息接口失败")
            print(f"错误信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始快速API测试...")
    print("请确保后端服务已启动在 http://localhost:5000")
    print("=" * 50)
    
    # 等待一下确保服务启动
    time.sleep(1)
    
    # 测试各个接口
    root_ok = test_root_endpoint()
    health_ok = test_health_endpoint()
    simulation_ok = test_simulation_endpoint()
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print(f"根路径访问: {'✅ 通过' if root_ok else '❌ 失败'}")
    print(f"健康检查: {'✅ 通过' if health_ok else '❌ 失败'}")
    print(f"模拟消息: {'✅ 通过' if simulation_ok else '❌ 失败'}")
    
    if root_ok and health_ok and simulation_ok:
        print("\n🎉 所有测试通过！API服务运行正常。")
        print("💡 现在可以访问 http://localhost:5000 查看API文档页面")
    else:
        print("\n❌ 部分测试失败，请检查服务状态。")
        if not root_ok:
            print("💡 根路径问题已修复，请重启服务后重试")

if __name__ == "__main__":
    main()

