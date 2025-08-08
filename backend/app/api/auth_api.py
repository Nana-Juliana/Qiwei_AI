from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.models.user import User
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录 - 简化版，使用external_userid作为认证"""
    try:
        data = request.get_json()
        external_userid = data.get('external_userid')
        
        if not external_userid:
            return jsonify({
                'code': 400,
                'message': '缺少external_userid参数'
            }), 400
        
        # 查找或创建用户
        user = UserService.get_user_by_external_id(external_userid)
        if not user:
            # 创建新用户
            user = UserService.create_user(external_userid)
            current_app.logger.info(f"新用户登录并创建: {external_userid}")
        else:
            current_app.logger.info(f"用户登录: {external_userid}")
        
        # 生成JWT token
        access_token = create_access_token(identity=external_userid)
        
        return jsonify({
            'code': 200,
            'message': '登录成功',
            'data': {
                'access_token': access_token,
                'user_id': str(user.id),
                'external_userid': user.external_userid,
                'token_type': 'Bearer'
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"登录失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'登录失败: {str(e)}'
        }), 500

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify_token():
    """验证JWT token"""
    try:
        current_user_id = get_jwt_identity()
        user = UserService.get_user_by_external_id(current_user_id)
        
        if not user:
            return jsonify({
                'code': 401,
                'message': '用户不存在'
            }), 401
        
        return jsonify({
            'code': 200,
            'message': 'token有效',
            'data': {
                'user_id': str(user.id),
                'external_userid': user.external_userid,
                'student_name': user.student_name,
                'parent_name': user.parent_name
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"token验证失败: {str(e)}")
        return jsonify({
            'code': 401,
            'message': 'token无效'
        }), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required()
def refresh_token():
    """刷新JWT token"""
    try:
        current_user_id = get_jwt_identity()
        new_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'code': 200,
            'message': 'token刷新成功',
            'data': {
                'access_token': new_token,
                'token_type': 'Bearer'
            }
        })
        
    except Exception as e:
        current_app.logger.error(f"token刷新失败: {str(e)}")
        return jsonify({
            'code': 500,
            'message': f'token刷新失败: {str(e)}'
        }), 500

