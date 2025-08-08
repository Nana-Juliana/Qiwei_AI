# coding=utf-8

import requests
import json
from datetime import datetime
from flask import current_app
from .fallback_ai_service import FallbackAIService

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    # 延迟日志记录，避免在模块导入时访问current_app

class AIService:
    @staticmethod
    def generate_response(customer_message, external_userid=None):
        """
        智能AI回复生成 - 优先使用华为云Maas DeepSeek，失败时使用备用服务
        """
        # 首先尝试使用华为云Maas DeepSeek API
        deepseek_response = AIService._try_deepseek_api(customer_message)
        if deepseek_response:
            return deepseek_response
        
        # 如果DeepSeek API失败，使用备用AI服务
        try:
            current_app.logger.info("DeepSeek API不可用，切换到备用AI服务")
        except:
            pass  # 如果current_app不可用，忽略日志
        return FallbackAIService.generate_response(customer_message, external_userid)
    
    @staticmethod
    def _try_deepseek_api(customer_message):
        """
        尝试调用华为云Maas DeepSeek API
        """
        try:
            # 从配置中获取API配置
            base_url = current_app.config.get('DEEPSEEK_API_URL', "https://maas-cn-southwest-2.modelarts-maas.com/v1/infers/8a062fd4-7367-4ab4-a936-5eeb8fb821c4/v1")
            api_key = current_app.config.get('DEEPSEEK_API_KEY', "qtcLta5Ahc6WdBNZEfDYbmKZ29N3F8tLZ0xycehttB_xrmMytAPp_p858mmwU2mVYpaJmCKbbbCol_XNB9WcQQ")
            
            # 构建专业的客服提示词
            system_prompt = """你是一个专业的教育机构客服助手，专门负责回答家长和学生的咨询问题。

你的职责：
1. 提供专业、友好、耐心的回复
2. 针对教育相关问题给出准确建议
3. 如果涉及具体课程安排、费用、报名等问题，说明会安排专人联系
4. 保持积极正面的服务态度
5. 回复要简洁明了，不超过200字
6. 使用中文回复

请根据客户的具体问题提供个性化的专业回复。"""
            
            # 构建用户消息
            user_message = f"客户咨询：{customer_message}\n\n请提供专业的客服回复："
            
            # 构建完整的API端点URL（用于requests调用）
            chat_completions_url = f"{base_url}/chat/completions"
            
            # 优先使用requests方法，避免OpenAI SDK的兼容性问题
            result = AIService._call_with_requests(chat_completions_url, api_key, system_prompt, user_message)
            if result:
                return result
            
            # 如果requests失败且OpenAI SDK可用，尝试使用OpenAI SDK
            if OPENAI_AVAILABLE:
                try:
                    current_app.logger.info("尝试使用OpenAI SDK作为备用方案")
                except:
                    pass
                return AIService._call_with_openai_sdk(base_url, api_key, system_prompt, user_message)
                
        except Exception as e:
            try:
                current_app.logger.error(f"DeepSeek API调用异常: {str(e)}")
            except:
                pass  # 如果current_app不可用，忽略日志
            return None
    
    @staticmethod
    def _call_with_openai_sdk(base_url, api_key, system_prompt, user_message):
        """
        使用OpenAI SDK调用API（备用方法）
        """
        try:
            # 更安全的客户端创建方式
            try:
                current_app.logger.info("正在使用OpenAI SDK创建客户端")
            except:
                pass
                
            # 明确指定所有参数，避免传递不支持的参数
            client_kwargs = {
                'api_key': api_key,
                'base_url': base_url
            }
            
            # 创建客户端时明确指定参数
            client = OpenAI(**client_kwargs)
            
            response = client.chat.completions.create(
                model="DeepSeek-R1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.6,
                max_tokens=500,
                stream=False
            )
            
            # 获取回复内容
            ai_content = response.choices[0].message.content
            
            if ai_content:
                # 清理和格式化回复内容
                ai_content = ai_content.strip()
                # 移除可能的markdown格式
                ai_content = ai_content.replace('**', '').replace('*', '')
                
                try:
                    current_app.logger.info(f"DeepSeek API调用成功（OpenAI SDK），生成长度: {len(ai_content)}")
                except:
                    pass
                return {
                    'content': ai_content,
                    'confidence': 0.95,
                    'generated_at': datetime.utcnow().isoformat(),
                    'model': 'DeepSeek-R1',
                    'api_provider': 'huawei-maas-openai-sdk'
                }
            
            return None
            
        except Exception as e:
            try:
                current_app.logger.error(f"OpenAI SDK调用失败: {str(e)}")
                current_app.logger.info("OpenAI SDK不兼容，将禁用此方法")
            except:
                pass
            return None
    
    @staticmethod
    def _call_with_requests(chat_completions_url, api_key, system_prompt, user_message):
        """
        使用requests库调用API（主要方法）
        """
        try:
            # 构建请求头
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}'
            }
            
            # 构建请求体（根据接口文档）
            payload = {
                "model": "DeepSeek-R1",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                "temperature": 0.6,
                "stream": False
            }
            
            # 调用华为云Maas DeepSeek API
            try:
                current_app.logger.info(f"正在调用DeepSeek API: {chat_completions_url}")
            except:
                pass
                
            response = requests.post(
                chat_completions_url,
                headers=headers,
                json=payload,
                timeout=30,
                verify=False
            )
            
            try:
                current_app.logger.info(f"DeepSeek API响应状态码: {response.status_code}")
            except:
                pass
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                
                # 解析AI回复内容
                if 'choices' in result and len(result['choices']) > 0:
                    ai_content = result['choices'][0].get('message', {}).get('content', '')
                    
                    if ai_content:
                        # 清理和格式化回复内容
                        ai_content = ai_content.strip()
                        # 移除可能的markdown格式
                        ai_content = ai_content.replace('**', '').replace('*', '')
                        
                        try:
                            current_app.logger.info(f"DeepSeek API调用成功（requests），生成长度: {len(ai_content)}")
                        except:
                            pass
                        return {
                            'content': ai_content,
                            'confidence': 0.95,
                            'generated_at': datetime.utcnow().isoformat(),
                            'model': 'DeepSeek-R1',
                            'api_provider': 'huawei-maas-requests'
                        }
                
                # 如果解析失败，返回None使用备用服务
                try:
                    current_app.logger.warning("DeepSeek API响应格式异常")
                    current_app.logger.debug(f"响应内容: {result}")
                except:
                    pass
                return None
                
            else:
                # API调用失败
                try:
                    current_app.logger.error(f"DeepSeek API调用失败: {response.status_code} - {response.text}")
                except:
                    pass
                return None
                
        except requests.exceptions.Timeout:
            try:
                current_app.logger.error("DeepSeek API调用超时")
            except:
                pass
            return None
            
        except requests.exceptions.RequestException as e:
            try:
                current_app.logger.error(f"DeepSeek API网络请求失败: {str(e)}")
            except:
                pass
            return None
            
        except Exception as e:
            try:
                current_app.logger.error(f"DeepSeek API调用异常: {str(e)}")
            except:
                pass
            return None
