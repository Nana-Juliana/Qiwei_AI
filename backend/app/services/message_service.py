import time
from datetime import datetime

class MessageService:
    @staticmethod
    def send_message(content, send_method='wechat', customer_id=None):
        """
        发送消息给客户，不保存历史记录
        """
        # 模拟消息发送
        print(f"发送消息到客户 {customer_id}: {content}")
        print(f"发送方式: {send_method}")
        
        # 这里可以集成真实的消息发送服务
        # 例如：微信API、短信API、邮件API等
        
        return {
            'message_id': f"msg_{int(time.time())}",
            'sent_at': datetime.utcnow().isoformat(),
            'status': 'sent'
        }

