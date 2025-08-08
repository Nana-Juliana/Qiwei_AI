// API配置
const config = {
  API_BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000/api/v1',
  
  // 测试用户ID - 和后端保持一致
  TEST_USER_ID: 'test_user_456',
  
  // 请求超时时间 (毫秒)
  REQUEST_TIMEOUT: 10000,
  
  // 是否启用调试模式
  DEBUG: process.env.NODE_ENV === 'development'
};

export default config;
