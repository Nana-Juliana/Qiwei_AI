from marshmallow import Schema, fields, validate

class MessageSendSchema(Schema):
    """消息发送验证模式"""
    content = fields.Str(required=True, validate=validate.Length(min=1))
    sendMethod = fields.Str(validate=validate.OneOf(['wechat', 'sms', 'email']), missing='wechat')
    customerId = fields.Str(required=True, validate=validate.Length(min=1))

class AIResponseSchema(Schema):
    """AI回复验证模式"""
    message = fields.Str(required=True, validate=validate.Length(min=1))
    external_userid = fields.Str(validate=validate.Length(min=1))

