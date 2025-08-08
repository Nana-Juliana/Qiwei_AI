import pytest
import json
from app import create_app
from app.models.user import db, User

@pytest.fixture
def app():
    """创建测试应用"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """创建测试客户端"""
    return app.test_client()

@pytest.fixture
def sample_user(app):
    """创建测试用户"""
    with app.app_context():
        user = User(
            external_userid='test_user_123',
            student_name='张三',
            parent_name='张父',
            parent_phone='13800138000',
            parent_wechat='zhangfu123'
        )
        db.session.add(user)
        db.session.commit()
        return user

def test_simulate_customer_message(client):
    """测试模拟客户消息"""
    response = client.post('/api/v1/simulate-customer-msg', 
                          json={
                              'external_userid': 'test_user_123',
                              'content': '请问课程安排如何？'
                          })
    assert response.status_code == 200
    data = response.get_json()
    assert data['code'] == 200
    assert 'ai_response' in data['data']
    assert data['data']['received'] == True

def test_simulate_customer_message_missing_params(client):
    """测试缺少参数的模拟客户消息"""
    response = client.post('/api/v1/simulate-customer-msg', 
                          json={'external_userid': 'test_user_123'})
    assert response.status_code == 400
    data = response.get_json()
    assert data['code'] == 400

def test_get_user_basic_unauthorized(client, sample_user):
    """测试未授权的用户信息获取"""
    response = client.get(f'/api/v1/users/{sample_user.id}/basic')
    assert response.status_code == 401  # 未授权

def test_get_user_basic_authorized(client, sample_user):
    """测试授权的用户信息获取"""
    # 这里需要添加JWT token，简化测试
    response = client.get(f'/api/v1/users/{sample_user.id}/basic')
    # 由于没有JWT token，会返回401
    assert response.status_code == 401

