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

// 用户信息相关API服务
class UserService {
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

  // 获取用户基本信息
  async getBasicInfo(token) {
    try {
      const response = await apiRequest(`/users/${config.TEST_USER_ID}/basic`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.code === 200) {
        return {
          success: true,
          data: response.data
        };
      } else {
        throw new Error(response.message || '获取基本信息失败');
      }
    } catch (error) {
      console.error('获取基本信息失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 获取学员详细信息
  async getStudentDetails(token) {
    try {
      const response = await apiRequest(`/users/${config.TEST_USER_ID}/student-details`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.code === 200) {
        return {
          success: true,
          data: response.data
        };
      } else {
        throw new Error(response.message || '获取学员详情失败');
      }
    } catch (error) {
      console.error('获取学员详情失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 获取家长详细信息
  async getParentDetails(token) {
    try {
      const response = await apiRequest(`/users/${config.TEST_USER_ID}/parent-details`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.code === 200) {
        return {
          success: true,
          data: response.data
        };
      } else {
        throw new Error(response.message || '获取家长详情失败');
      }
    } catch (error) {
      console.error('获取家长详情失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 更新用户信息
  async updateUserInfo(userData, token) {
    try {
      const response = await apiRequest(`/users/${config.TEST_USER_ID}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(userData),
      });

      if (response.code === 200) {
        return {
          success: true,
          data: response.data
        };
      } else {
        throw new Error(response.message || '更新用户信息失败');
      }
    } catch (error) {
      console.error('更新用户信息失败:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 获取所有用户数据（基本信息、学员详情、家长详情）
  async getAllUserData(token) {
    try {
      // 并行获取所有数据
      const [basicResult, studentResult, parentResult] = await Promise.all([
        this.getBasicInfo(token),
        this.getStudentDetails(token),
        this.getParentDetails(token)
      ]);

      // 检查是否至少有学员或家长信息成功
      const hasStudentData = studentResult.success;
      const hasParentData = parentResult.success;
      const hasBasicData = basicResult.success;

      if (hasStudentData && hasParentData) {
        // 如果学员和家长信息都存在，说明用户存在
        // 基本信息可能不存在或需要从其他数据构建
        let basicInfo = {};
        
        if (hasBasicData) {
          // 如果基本信息API成功，使用返回的数据
          basicInfo = basicResult.data;
        } else {
          // 如果基本信息API失败，从学员和家长信息构建基本信息
          console.log('基本信息API失败，从详细信息构建基本信息:', basicResult.error);
          
          // 处理年龄格式：学员详情返回"5岁"，需要提取数字
          let studentAge = "";
          if (studentResult.data.age) {
            studentAge = studentResult.data.age.toString().replace(/[^\d]/g, '');
          }
          
          basicInfo = {
            studentName: studentResult.data.name || "",
            parentName: parentResult.data.name || "",
            phone: parentResult.data.phone || "",
            wechat: parentResult.data.wechat || "",
            studentAge: studentAge,
            studentGender: studentResult.data.gender || "",
            currentCourse: "暂无课程", // 这些字段在详细信息中不存在
            teacher: "暂无教师",
            classTime: "暂无安排",
            expiryDate: "暂无日期"
          };
        }

        return {
          success: true,
          data: {
            basicInfo: basicInfo,
            studentDetails: studentResult.data,
            parentDetails: parentResult.data
          }
        };
      } else {
        // 如果学员或家长信息都失败，说明用户不存在
        const errors = [];
        if (!basicResult.success) errors.push(`基本信息: ${basicResult.error}`);
        if (!studentResult.success) errors.push(`学员信息: ${studentResult.error}`);
        if (!parentResult.success) errors.push(`家长信息: ${parentResult.error}`);
        
        throw new Error(`获取用户数据失败: ${errors.join(', ')}`);
      }
    } catch (error) {
      console.error('获取所有用户数据失败:', error);
      return {
        success: false,
        error: error.message,
        isUserNotFound: error.message.includes('404') || error.message.includes('不存在')
      };
    }
  }
}

// 创建单例实例
const userService = new UserService();

export default userService;
