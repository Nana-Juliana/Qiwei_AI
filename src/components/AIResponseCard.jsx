import React, { useState, useEffect } from "react";
import aiService from '../services/aiService';
import config from '../config';

const AIResponseCard = () => {
  // AI推荐回复内容
  const [aiResponse, setAiResponse] = useState({
    content: "",
    generatedAt: "",
    confidence: 0
  });

  // 状态管理
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sendStatus, setSendStatus] = useState("");
  const [authToken, setAuthToken] = useState(null);

  // 获取AI推荐回复
  const loadAIResponse = async () => {
    try {
      setLoading(true);
      setError(null);

      const result = await aiService.getAIResponse();
      
      if (result.success) {
        setAiResponse(result.data);
        
        if (config.DEBUG) {
          console.log('AI回复加载完成:', result.data);
        }
      } else {
        throw new Error(result.error || '获取AI回复失败');
      }

    } catch (error) {
      console.error('获取AI回复失败:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // 获取认证token
  const getAuthToken = async () => {
    try {
      const result = await aiService.login();
      
      if (result.success) {
        setAuthToken(result.data.token);
        
        if (config.DEBUG) {
          console.log('登录成功，获取token');
        }
      } else {
        console.warn('登录失败:', result.error);
      }
    } catch (error) {
      console.warn('获取token失败:', error);
    }
  };

  // 发送给客户功能
  const handleSendToCustomer = async () => {
    try {
      setSendStatus("发送中...");

      if (!authToken) {
        // 如果没有token，先尝试获取
        await getAuthToken();
        if (!authToken) {
          throw new Error('无法获取认证token');
        }
      }

      const result = await aiService.sendMessageToCustomer(aiResponse.content, authToken);

      if (result.success) {
        setSendStatus("发送成功！");
        
        if (config.DEBUG) {
          console.log("发送成功:", result.data);
        }
      } else {
        throw new Error(result.error || '发送失败');
      }

      // 3秒后清除状态
      setTimeout(() => {
        setSendStatus("");
      }, 3000);

    } catch (error) {
      console.error('发送失败:', error);
      setSendStatus(`发送失败: ${error.message}`);
      
      // 3秒后清除错误状态
      setTimeout(() => {
        setSendStatus("");
      }, 3000);
    }
  };

  // 一键复制功能
  const handleCopyContent = async () => {
    try {
      await navigator.clipboard.writeText(aiResponse.content);
      console.log("内容已复制到剪贴板:", aiResponse.content);
      alert("内容已复制到剪贴板！");
    } catch (err) {
      console.error("复制失败:", err);
      alert("复制失败，请手动复制");
    }
  };

  // 组件加载时获取AI回复和认证token
  useEffect(() => {
    const initializeComponent = async () => {
      // 并行获取AI回复和认证token
      await Promise.all([
        loadAIResponse(),
        getAuthToken()
      ]);
    };

    initializeComponent();
  }, []);



  // Loading状态
  if (loading) {
    return (
      <div className="bg-white shadow-md rounded-2xl p-6 mb-4">
        <div className="animate-pulse">
          <div className="flex items-center justify-between mb-4">
            <div>
              <div className="h-4 bg-gray-300 rounded w-24 mb-2"></div>
              <div className="h-3 bg-gray-300 rounded w-32"></div>
            </div>
          </div>
          <div className="bg-gray-200 p-4 rounded-xl mb-4">
            <div className="space-y-2">
              <div className="h-3 bg-gray-300 rounded w-full"></div>
              <div className="h-3 bg-gray-300 rounded w-3/4"></div>
              <div className="h-3 bg-gray-300 rounded w-1/2"></div>
            </div>
          </div>
          <div className="flex space-x-3">
            <div className="flex-1 h-10 bg-gray-300 rounded-xl"></div>
            <div className="flex-1 h-10 bg-gray-300 rounded-xl"></div>
          </div>
        </div>
      </div>
    );
  }

  // Error状态
  if (error) {
    return (
      <div className="bg-white shadow-md rounded-2xl p-6 mb-4">
        <div className="text-center">
          <div className="text-red-500 mb-4">
            <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h3 className="text-lg font-semibold text-gray-800 mb-2">获取AI回复失败</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadAIResponse}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl transition-colors"
          >
            重新获取
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-6 mb-4">
      {/* 头部标题 */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-lg font-semibold text-gray-800">AI推荐回复</div>
          <div className="text-xs text-gray-500">基于当前对话分析</div>
        </div>
      </div>

      {/* 内容区域 */}
      <div className="bg-gray-50 p-4 rounded-xl mb-4">
        <div className="text-gray-800 leading-relaxed whitespace-pre-line">
          {aiResponse.content}
        </div>
      </div>

      {/* 发送状态提示 */}
      {sendStatus && (
        <div className="mb-4 p-3 bg-green-100 border border-green-300 rounded-xl">
          <div className="text-green-800 text-sm font-medium">{sendStatus}</div>
        </div>
      )}

      {/* 操作按钮 */}
      <div className="flex space-x-3">
        <button 
          onClick={handleSendToCustomer}
          disabled={sendStatus === "发送中..."}
          className="flex-1 bg-green-500 hover:bg-green-600 disabled:bg-green-300 text-white py-2 px-4 rounded-xl text-sm font-medium transition-colors"
        >
          {sendStatus === "发送中..." ? "发送中..." : "发送给客户"}
        </button>
        <button 
          onClick={handleCopyContent}
          className="flex-1 bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-xl text-sm font-medium transition-colors"
        >
          一键复制
        </button>
      </div>


    </div>
  );
};

export default AIResponseCard;