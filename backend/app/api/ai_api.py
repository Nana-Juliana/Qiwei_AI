from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.ai_service import AIService
from app.services.message_service import MessageService
from app.schemas.message_schema import MessageSendSchema, AIResponseSchema

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/ai-responses', methods=['POST'])
@jwt_required()
def get_ai_response():
    """获取AI推荐回复"""
    try:
        data = request.get_json()
        customer_message = data.get('message')
        external_userid = data.get('external_userid')
        
        if not customer_message:
            return jsonify({'code': 400, 'message': '消息内容不能为空'}), 400
        
        # 直接生成AI回复，不保存历史
        ai_response = AIService.generate_response(customer_message, external_userid)
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': {
                'content': ai_response['content'],
                'generatedAt': ai_response['generated_at'],
                'confidence': ai_response['confidence']
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

@ai_bp.route('/send-message', methods=['POST'])
@jwt_required()
def send_message():
    """发送回复给客户"""
    try:
        data = request.get_json()
        
        # 验证数据
        schema = MessageSendSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify({'code': 400, 'message': '请求参数错误', 'error': errors}), 400
        
        # 发送消息
        message_result = MessageService.send_message(
            content=data['content'],
            send_method=data.get('sendMethod', 'wechat'),
            customer_id=data['customerId']
        )
        
        return jsonify({
            'code': 200,
            'message': '发送成功',
            'data': {
                'messageId': message_result['message_id'],
                'sentAt': message_result['sent_at'],
                'status': message_result['status']
            }
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

