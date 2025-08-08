from flask import Blueprint, jsonify, request
from app.services.ai_service import AIService
from app.services.user_service import UserService

simulation_bp = Blueprint('simulation', __name__)

@simulation_bp.route('/simulate-customer-msg', methods=['POST'])
def simulate_customer_message():
    """模拟客户消息API"""
    try:
        data = request.get_json()
        external_userid = data.get("external_userid")
        content = data.get("content")
        
        if not external_userid or not content:
            return jsonify({
                'code': 400,
                'message': '缺少必要参数',
                'error': {
                    'field': 'external_userid/content',
                    'detail': 'external_userid和content不能为空'
                }
            }), 400
        
        print(f"客户 {external_userid} 发来消息：{content}")
        
        # 检查用户是否存在，如果不存在则创建
        user = UserService.get_user_by_external_id(external_userid)
        if not user:
            # 创建新用户
            user = UserService.create_user(external_userid)
            print(f"创建新用户: {external_userid}")
        
        # 直接生成AI回复，不保存对话历史
        ai_response = AIService.generate_response(content, external_userid)
        
        return jsonify({
            'code': 200,
            'message': '消息接收成功',
            'data': {
                'received': True,
                'user': external_userid,
                'message': content,
                'ai_response': ai_response['content'],
                'generated_at': ai_response['generated_at']
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

