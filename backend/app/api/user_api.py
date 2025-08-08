from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService
from app.schemas.user_schema import UserUpdateSchema

user_bp = Blueprint('user', __name__)

@user_bp.route('/users/<user_id>/basic', methods=['GET'])
@jwt_required()
def get_user_basic(user_id):
    """获取用户基本信息"""
    try:
        user = UserService.get_user_basic(user_id)
        if not user:
            return jsonify({'code': 404, 'message': '用户不存在'}), 404
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': user
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

@user_bp.route('/users/<user_id>/student-details', methods=['GET'])
@jwt_required()
def get_student_details(user_id):
    """获取学员详细信息"""
    try:
        student = UserService.get_student_details(user_id)
        if not student:
            return jsonify({'code': 404, 'message': '学员信息不存在'}), 404
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': student
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

@user_bp.route('/users/<user_id>/parent-details', methods=['GET'])
@jwt_required()
def get_parent_details(user_id):
    """获取家长详细信息"""
    try:
        parent = UserService.get_parent_details(user_id)
        if not parent:
            return jsonify({'code': 404, 'message': '家长信息不存在'}), 404
        
        return jsonify({
            'code': 200,
            'message': 'success',
            'data': parent
        })
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """更新用户信息"""
    try:
        data = request.get_json()
        
        # 验证数据
        schema = UserUpdateSchema()
        errors = schema.validate(data)
        if errors:
            return jsonify({'code': 400, 'message': '请求参数错误', 'error': errors}), 400
        
        # 更新用户信息
        updated_user = UserService.update_user(user_id, data)
        
        return jsonify({
            'code': 200,
            'message': '更新成功',
            'data': {
                'userId': user_id,
                'updatedAt': updated_user.updated_at.isoformat()
            }
        })
    except ValueError as e:
        return jsonify({'code': 404, 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'code': 500, 'message': f'服务器错误: {str(e)}'}), 500

