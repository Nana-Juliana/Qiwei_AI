#!/usr/bin/env python3
"""
备用AI服务
当华为云Maas DeepSeek API不可用时，使用本地规则引擎生成回复
"""

import re
from datetime import datetime
from flask import current_app

class FallbackAIService:
    """备用AI服务 - 基于规则的智能回复"""
    
    # 关键词匹配规则
    KEYWORD_RULES = {
        # 课程相关
        r'英语|英语课程|英语课': {
            'response': '我们的英语课程采用小班制教学，每周2-3次课，每次90分钟。课程涵盖听说读写四个方面，适合不同年龄段的学生。具体安排可以联系我们的课程顾问详细了解。',
            'confidence': 0.9
        },
        r'数学|数学课程|数学课': {
            'response': '数学课程注重基础巩固和思维训练，采用分层教学方式。我们有经验丰富的数学老师，会根据学生的具体情况制定个性化学习计划。',
            'confidence': 0.9
        },
        r'语文|语文课程|语文课': {
            'response': '语文课程重点培养学生的阅读理解能力和写作水平，通过经典文学作品赏析和写作训练，提升学生的语文素养。',
            'confidence': 0.9
        },
        
        # 费用相关
        r'学费|费用|价格|多少钱|收费': {
            'response': '我们的收费标准根据课程类型和课时安排有所不同。为了给您提供最准确的费用信息，建议您联系我们的课程顾问，他们会根据您的具体需求为您详细说明。',
            'confidence': 0.85
        },
        r'优惠|折扣|活动': {
            'response': '我们经常会有各种优惠活动，比如新学员体验价、团报优惠等。具体活动信息可以关注我们的官方通知或联系客服了解。',
            'confidence': 0.8
        },
        
        # 试听相关
        r'试听|体验|试课': {
            'response': '我们提供免费试听课程，让您和孩子先体验我们的教学方式。试听需要提前预约，您可以联系我们的客服安排试听时间。',
            'confidence': 0.9
        },
        
        # 师资相关
        r'老师|教师|师资|背景|学历': {
            'response': '我们的老师都经过严格筛选，具备相关专业背景和丰富的教学经验。大部分老师都有本科及以上学历，并定期参加教学培训。',
            'confidence': 0.85
        },
        
        # 学习建议
        r'成绩|学习|建议|方法|提高': {
            'response': '每个孩子的学习情况不同，我们建议先进行学习能力评估，然后制定个性化的学习计划。我们的老师会根据学生的具体情况提供针对性的学习建议。',
            'confidence': 0.8
        },
        
        # 时间安排
        r'时间|安排|上课|课程表|什么时候': {
            'response': '我们的课程时间比较灵活，有工作日晚上和周末的课程。具体时间安排会根据您的需求和我们的课程安排来确定。',
            'confidence': 0.8
        },
        
        # 地点相关
        r'地址|位置|在哪里|校区': {
            'response': '我们有多個校区，具体地址可以联系客服了解。所有校区都位于交通便利的位置，方便学生和家长。',
            'confidence': 0.8
        },
        
        # 报名相关
        r'报名|注册|入学|怎么报名': {
            'response': '报名流程很简单，您可以先预约试听，满意后再正式报名。报名时需要提供学生基本信息和家长联系方式。',
            'confidence': 0.85
        }
    }
    
    # 通用回复模板
    GENERAL_RESPONSES = [
        "感谢您的咨询！关于您提到的问题，我建议您联系我们的专业老师，他们会为您提供更详细和个性化的解答。",
        "您的问题很有代表性，为了更好地为您服务，建议您预约我们的课程顾问进行详细咨询。",
        "我们非常重视您的咨询，稍后会有专业的老师联系您，为您提供更全面的解答。",
        "感谢您对我们教育机构的关注！关于您的具体问题，我们的专业团队会为您提供最适合的解决方案。"
    ]
    
    @staticmethod
    def generate_response(customer_message, external_userid=None):
        """
        基于规则的智能回复生成
        """
        try:
            # 清理输入消息
            clean_message = customer_message.strip().lower()
            
            # 查找匹配的关键词规则
            matched_rule = None
            for pattern, rule in FallbackAIService.KEYWORD_RULES.items():
                if re.search(pattern, clean_message):
                    matched_rule = rule
                    break
            
            if matched_rule:
                # 使用匹配的规则生成回复
                response_content = matched_rule['response']
                confidence = matched_rule['confidence']
            else:
                # 使用通用回复
                import random
                response_content = random.choice(FallbackAIService.GENERAL_RESPONSES)
                confidence = 0.6
            
            # 添加个性化开头
            personalized_response = f"尊敬的家长，您好！\n\n{response_content}\n\n如有其他问题，欢迎随时咨询。"
            
            current_app.logger.info(f"备用AI服务生成回复，置信度: {confidence}")
            
            return {
                'content': personalized_response,
                'confidence': confidence,
                'generated_at': datetime.utcnow().isoformat(),
                'model': 'rule-based',
                'api_provider': 'local-fallback'
            }
            
        except Exception as e:
            current_app.logger.error(f"备用AI服务异常: {str(e)}")
            return FallbackAIService._get_default_response(customer_message)
    
    @staticmethod
    def _get_default_response(customer_message):
        """生成默认回复"""
        default_content = f"""尊敬的家长，您好！

关于您的咨询：{customer_message}

我已经收到您的消息，稍后会安排专业的老师为您详细回复。如有紧急情况，请直接联系我们的客服热线。

感谢您对我们教育机构的信任与支持！

祝您生活愉快！"""
        
        return {
            'content': default_content,
            'confidence': 0.5,
            'generated_at': datetime.utcnow().isoformat(),
            'model': 'fallback',
            'api_provider': 'local'
        }
    
    @staticmethod
    def get_supported_keywords():
        """获取支持的关键词列表"""
        keywords = []
        for pattern in FallbackAIService.KEYWORD_RULES.keys():
            # 提取关键词（去除正则表达式符号）
            clean_pattern = pattern.replace('|', '、').replace('(', '').replace(')', '')
            keywords.append(clean_pattern)
        return keywords

