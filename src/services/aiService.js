import config from '../config';

// 基础API请求函数
const apiRequest = async (endpoint, options = {}) => {
  const url = `${config.API_BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
    },
    timeout: config.REQUEST_TIMEOUT,
  };

  // 合并选项
  const finalOptions = {
    ...defaultOptions,
    ...options,
    headers: {
      ...defaultOptions.headers,
      ...options.headers,
    },
  };

  if (config.DEBUG) {
    console.log(`API请求: ${finalOptions.method || 'GET'} ${url}`, finalOptions);
  }

  try {
    const response = await fetch(url, finalOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (config.DEBUG) {
      console.log(`API响应:`, data);
    }
    
    return data;
  } catch (error) {
    console.error(`API请求失败 ${url}:`, error);
    throw error;
  }
};

// AI回复相关API服务
class AIService {
  // 获取AI推荐回复 - 使用模拟客户消息API（无需认证）
  async getAIResponse() {
    try {
      const response = await apiRequest('/simulate-customer-msg', {
        method: 'POST',
        body: JSON.stringify({
          external_userid: config.TEST_USER_ID,
          content: '请问课程安排如何？我想了解一下英语课程'
        }),
      });

      if (response.code === 200) {
        return {
          success: true,
          data: {
            content: response.data.ai_response,
            generatedAt: response.data.generated_at,
            confidence: 0.95 // 模拟置信度
          }
        };
      } else {
        throw new Error(response.message || '获取AI回复失败');
      }
    } catch (error) {
      console.error('获取AI回复失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 发送消息给客户（需要认证）
  async sendMessageToCustomer(content, token) {
    try {
      const response = await apiRequest('/send-message', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          content,
          sendMethod: 'wechat',
          customerId: config.TEST_USER_ID,
        }),
      });

      if (response.code === 200) {
        return {
          success: true,
          data: response.data
        };
      } else {
        throw new Error(response.message || '发送失败');
      }
    } catch (error) {
      console.error('发送消息失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 用户登录（获取token）
  async login() {
    try {
      const response = await apiRequest('/login', {
        method: 'POST',
        body: JSON.stringify({
          external_userid: config.TEST_USER_ID
        }),
      });

      if (response.code === 200) {
        return {
          success: true,
          data: {
            token: response.data.access_token,
            user: response.data
          }
        };
      } else {
        throw new Error(response.message || '登录失败');
      }
    } catch (error) {
      console.error('登录失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// 创建单例实例
const aiService = new AIService();

export default aiService;
