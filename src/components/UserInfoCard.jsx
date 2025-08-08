import React, { useState, useEffect } from "react";
import userService from '../services/userService';
import config from '../config';

const UserInfoCard = () => {
  const [isEditOpen, setEditOpen] = useState(false);
  
  // 状态管理
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [authToken, setAuthToken] = useState(null);
  const [userExists, setUserExists] = useState(true);
  const [isNewUser, setIsNewUser] = useState(false);
  
  // 用户信息状态 - 从API获取
  const [userInfo, setUserInfo] = useState({
    studentName: "",
    parentName: "",
    phone: "",
    wechat: "",
    studentAge: "",
    studentGender: "",
    currentCourse: "",
    teacher: "",
    classTime: "",
    expiryDate: ""
  });

  // 编辑表单状态
  const [editForm, setEditForm] = useState({
    // 学员信息字段
    studentName: "",
    studentAge: "",
    studentGender: "",
    enrollmentDate: "",
    totalClasses: "",
    completedClasses: "",
    attendanceRate: "",
    performance: "",
    studentNotes: "",
    // 家长信息字段
    parentName: "",
    relationship: "",
    parentPhone: "",
    parentWechat: "",
    parentNotes: "",
    // 课程信息字段
    currentCourse: "",
    teacher: "",
    classTime: "",
    expiryDate: ""
  });

  // 打开编辑弹窗时，将当前数据复制到编辑表单
  const handleEditOpen = () => {
    setEditForm({
      // 学员信息
      studentName: studentDetails.name,
      studentAge: studentDetails.age,
      studentGender: studentDetails.gender,
      enrollmentDate: studentDetails.enrollmentDate,
      totalClasses: studentDetails.totalClasses,
      completedClasses: studentDetails.completedClasses,
      attendanceRate: studentDetails.attendanceRate,
      performance: studentDetails.performance,
      studentNotes: studentDetails.notes,
      // 家长信息
      parentName: parentDetails.name,
      relationship: parentDetails.relationship,
      parentPhone: parentDetails.phone,
      parentWechat: parentDetails.wechat,
      parentNotes: parentDetails.notes,
      // 课程信息
      currentCourse: userInfo.currentCourse,
      teacher: userInfo.teacher,
      classTime: userInfo.classTime,
      expiryDate: userInfo.expiryDate
    });
    setEditOpen(true);
  };

  // 处理表单输入变化
  const handleInputChange = (field, value) => {
    setEditForm(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // 保存编辑内容
  const handleSave = async () => {
    try {
      if (!authToken) {
        throw new Error('未登录，请重新登录');
      }

      // 构建更新数据
      const updateData = {
        studentInfo: {
          name: editForm.studentName,
          age: editForm.studentAge,
          gender: editForm.studentGender,
          enrollmentDate: editForm.enrollmentDate,
          totalClasses: parseInt(editForm.totalClasses) || 0,
          completedClasses: parseInt(editForm.completedClasses) || 0,
          attendanceRate: editForm.attendanceRate,
          performance: editForm.performance,
          notes: editForm.studentNotes
        },
        parentInfo: {
          name: editForm.parentName,
          relationship: editForm.relationship,
          phone: editForm.parentPhone,
          wechat: editForm.parentWechat,
          notes: editForm.parentNotes
        },
        basicInfo: {
          studentName: editForm.studentName,
          parentName: editForm.parentName,
          phone: editForm.parentPhone,
          wechat: editForm.parentWechat,
          studentAge: editForm.studentAge,
          studentGender: editForm.studentGender,
          currentCourse: editForm.currentCourse,
          teacher: editForm.teacher,
          classTime: editForm.classTime,
          expiryDate: editForm.expiryDate
        }
      };

      // 调用API更新数据
      const result = await userService.updateUserInfo(updateData, authToken);
      
      if (result.success) {
        // 更新本地状态
        setUserInfo(updateData.basicInfo);
        setStudentDetails(updateData.studentInfo);
        setParentDetails(updateData.parentInfo);
        setEditOpen(false);
        
        // 如果是新用户，更新状态
        if (isNewUser) {
          setUserExists(true);
          setIsNewUser(false);
        }
        
        if (config.DEBUG) {
          console.log("更新成功:", result.data);
        }
        
        alert(isNewUser ? '用户信息创建成功！' : '更新成功！');
      } else {
        throw new Error(result.error || '保存失败');
      }
      
    } catch (error) {
      console.error('保存失败:', error);
      alert(`保存失败: ${error.message}`);
    }
  };

  // 取消编辑
  const handleCancel = () => {
    setEditOpen(false);
  };

  // 新增状态管理
  const [showStudentDetails, setShowStudentDetails] = useState(false);
  const [showParentDetails, setShowParentDetails] = useState(false);
  


  // 学员详细信息 - 从API获取
  const [studentDetails, setStudentDetails] = useState({
    name: "",
    age: "",
    gender: "",
    enrollmentDate: "",
    totalClasses: 0,
    completedClasses: 0,
    attendanceRate: "",
    performance: "",
    notes: ""
  });

  // 家长详细信息 - 从API获取
  const [parentDetails, setParentDetails] = useState({
    name: "",
    relationship: "",
    phone: "",
    wechat: "",
    notes: ""
  });

  // 加载用户数据
  const loadUserData = async () => {
    try {
      setLoading(true);
      setError(null);

      // 先获取认证token
      const loginResult = await userService.login();
      if (!loginResult.success) {
        throw new Error(loginResult.error || '登录失败');
      }

      const token = loginResult.data.token;
      setAuthToken(token);

      // 获取所有用户数据
      const userDataResult = await userService.getAllUserData(token);
      
      if (userDataResult.success) {
        // 用户存在，设置数据
        setUserInfo(userDataResult.data.basicInfo);
        setStudentDetails(userDataResult.data.studentDetails);
        setParentDetails(userDataResult.data.parentDetails);
        setUserExists(true);
        setIsNewUser(false);
        
        if (config.DEBUG) {
          console.log('用户数据加载完成:', userDataResult.data);
        }
      } else {
        // 用户不存在，显示填写表单
        if (userDataResult.isUserNotFound) {
          setUserExists(false);
          setIsNewUser(true);
          // 打开编辑表单让用户填写信息
          setEditOpen(true);
          
          if (config.DEBUG) {
            console.log('用户不存在，需要填写信息');
          }
        } else {
          throw new Error(userDataResult.error || '获取用户数据失败');
        }
      }

    } catch (error) {
      console.error('加载用户数据失败:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  // 组件加载时获取数据
  useEffect(() => {
    loadUserData();
  }, []);



  // Loading状态
  if (loading) {
    return (
      <div className="bg-white shadow-md rounded-2xl p-6 mb-4">
        <div className="animate-pulse">
          <div className="flex items-start mb-4">
            <div className="w-12 h-12 bg-gray-300 rounded-full mr-4"></div>
            <div className="flex-1">
              <div className="h-4 bg-gray-300 rounded w-1/3 mb-2"></div>
              <div className="h-3 bg-gray-300 rounded w-1/2"></div>
            </div>
          </div>
          <div className="space-y-2 mb-6">
            <div className="h-3 bg-gray-300 rounded w-3/4"></div>
            <div className="h-3 bg-gray-300 rounded w-2/3"></div>
            <div className="h-3 bg-gray-300 rounded w-1/2"></div>
            <div className="h-3 bg-gray-300 rounded w-1/3"></div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="h-16 bg-gray-300 rounded-xl"></div>
            <div className="h-16 bg-gray-300 rounded-xl"></div>
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
          <h3 className="text-lg font-semibold text-gray-800 mb-2">加载失败</h3>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadUserData}
            className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-xl transition-colors"
          >
            重新加载
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white shadow-md rounded-2xl p-6 mb-4">
      {/* 头部信息 */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-start">
          <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center text-white text-xl font-bold mr-4">
            {(userInfo.parentName || "用户").charAt(0)}
          </div>
          <div>
            <div className="text-lg font-semibold text-gray-800">{userInfo.parentName || "家长姓名"}</div>
            <div className="text-sm text-gray-600">{userInfo.studentName || "学员姓名"}的妈妈 ({userInfo.studentAge || "0"}岁)</div>
          </div>
        </div>
        <button
          onClick={handleEditOpen}
          className="flex items-center text-blue-500 text-sm"
        >
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          编辑
        </button>
      </div>

      {/* 课程详情 */}
      <div className="space-y-2 mb-6">
        <div className="flex">
          <span className="text-gray-600 font-medium w-20">当前课程:</span>
          <span className="text-gray-800">{userInfo.currentCourse || "暂无课程"}</span>
        </div>
        <div className="flex">
          <span className="text-gray-600 font-medium w-20">上课时间:</span>
          <span className="text-gray-800">{userInfo.classTime || "暂无安排"}</span>
        </div>
        <div className="flex">
          <span className="text-gray-600 font-medium w-20">教师:</span>
          <span className="text-gray-800">{userInfo.teacher || "暂无教师"}</span>
        </div>
        <div className="flex">
          <span className="text-gray-600 font-medium w-20">到期日:</span>
          <span className="text-gray-800">{userInfo.expiryDate || "暂无日期"}</span>
        </div>
      </div>

      {/* 功能按钮 */}
      <div className="grid grid-cols-2 gap-4">
        <button 
          onClick={() => setShowStudentDetails(true)}
          className="flex flex-col items-center p-3 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors"
        >
          <div className="w-8 h-8 bg-yellow-100 rounded-lg flex items-center justify-center mb-2">
            <svg className="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
            </svg>
          </div>
          <span className="text-xs text-gray-700">学员详情</span>
        </button>
        
        <button 
          onClick={() => setShowParentDetails(true)}
          className="flex flex-col items-center p-3 bg-gray-50 hover:bg-gray-100 rounded-xl transition-colors"
        >
          <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center mb-2">
            <svg className="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
          <span className="text-xs text-gray-700">家长详情</span>
        </button>
      </div>

      {/* 编辑弹窗 */}
      {isEditOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-start justify-center z-50 py-10 px-4">
          <div className="bg-white p-6 rounded-2xl shadow-md w-96 max-h-[80vh] overflow-y-auto">
            {/* 标题栏 */}
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-800">
                {isNewUser ? '填写学员及家长信息' : '编辑学员及家长信息'}
              </h2>
              <button
                onClick={handleCancel}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* 表单内容 */}
             <div className="space-y-4">
               {/* 学员信息 */}
               <div className="border-b pb-4">
                 <h3 className="text-md font-semibold text-gray-800 mb-3">学员信息</h3>
                 <div className="grid grid-cols-2 gap-3">
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">学员姓名</label>
                     <input 
                       type="text" 
                       value={editForm.studentName}
                       onChange={(e) => handleInputChange('studentName', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">年龄</label>
                     <input 
                       type="text" 
                       value={editForm.studentAge}
                       onChange={(e) => handleInputChange('studentAge', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">性别</label>
                     <input 
                       type="text" 
                       value={editForm.studentGender}
                       onChange={(e) => handleInputChange('studentGender', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">入学日期</label>
                     <input 
                       type="text" 
                       value={editForm.enrollmentDate}
                       onChange={(e) => handleInputChange('enrollmentDate', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">总课时</label>
                     <input 
                       type="number" 
                       value={editForm.totalClasses}
                       onChange={(e) => handleInputChange('totalClasses', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">已完成</label>
                     <input 
                       type="number" 
                       value={editForm.completedClasses}
                       onChange={(e) => handleInputChange('completedClasses', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">出勤率</label>
                     <input 
                       type="text" 
                       value={editForm.attendanceRate}
                       onChange={(e) => handleInputChange('attendanceRate', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">表现评级</label>
                     <input 
                       type="text" 
                       value={editForm.performance}
                       onChange={(e) => handleInputChange('performance', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   
                 </div>
                 <div className="mt-3">
                   <label className="block text-sm font-medium text-gray-700 mb-1">学员备注</label>
                   <textarea 
                     value={editForm.studentNotes}
                     onChange={(e) => handleInputChange('studentNotes', e.target.value)}
                     className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                     rows="3"
                     placeholder="请输入学员备注信息..."
                   />
                 </div>
               </div>

               {/* 家长信息 */}
               <div className="border-b pb-4">
                 <h3 className="text-md font-semibold text-gray-800 mb-3">家长信息</h3>
                 <div className="grid grid-cols-2 gap-3">
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">家长姓名</label>
                     <input 
                       type="text" 
                       value={editForm.parentName}
                       onChange={(e) => handleInputChange('parentName', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">关系</label>
                     <input 
                       type="text" 
                       value={editForm.relationship}
                       onChange={(e) => handleInputChange('relationship', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">联系电话</label>
                     <input 
                       type="text" 
                       value={editForm.parentPhone}
                       onChange={(e) => handleInputChange('parentPhone', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">微信</label>
                     <input 
                       type="text" 
                       value={editForm.parentWechat}
                       onChange={(e) => handleInputChange('parentWechat', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                 </div>
                 <div className="mt-3">
                   <label className="block text-sm font-medium text-gray-700 mb-1">家长备注</label>
                   <textarea 
                     value={editForm.parentNotes}
                     onChange={(e) => handleInputChange('parentNotes', e.target.value)}
                     className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                     rows="3"
                     placeholder="请输入家长备注信息..."
                   />
                 </div>
               </div>

               {/* 课程信息 */}
               <div>
                 <h3 className="text-md font-semibold text-gray-800 mb-3">课程信息</h3>
                 <div className="grid grid-cols-2 gap-3">
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">当前课程</label>
                     <input 
                       type="text" 
                       value={editForm.currentCourse}
                       onChange={(e) => handleInputChange('currentCourse', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                       placeholder="请输入课程名称..."
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">教师</label>
                     <input 
                       type="text" 
                       value={editForm.teacher}
                       onChange={(e) => handleInputChange('teacher', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                       placeholder="请输入教师姓名..."
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">上课时间</label>
                     <input 
                       type="text" 
                       value={editForm.classTime}
                       onChange={(e) => handleInputChange('classTime', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                       placeholder="例如: 每周三、五 16:00-17:00"
                     />
                   </div>
                   <div>
                     <label className="block text-sm font-medium text-gray-700 mb-1">到期日</label>
                     <input 
                       type="date" 
                       value={editForm.expiryDate}
                       onChange={(e) => handleInputChange('expiryDate', e.target.value)}
                       className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                     />
                   </div>
                 </div>
               </div>
             </div>

            {/* 操作按钮 */}
            <div className="flex justify-end mt-6 space-x-3">
              <button
                onClick={handleCancel}
                className="px-6 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-xl transition-colors"
              >
                取消
              </button>
              <button
                onClick={handleSave}
                className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-xl transition-colors"
              >
                {isNewUser ? '创建' : '保存'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 学员详情弹窗 */}
      {showStudentDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-start justify-center z-50 py-10 px-4">
          <div className="bg-white p-6 rounded-2xl shadow-md w-96 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-800">学员详情</h2>
              <button
                onClick={() => setShowStudentDetails(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

                         <div className="space-y-4">
               <div className="grid grid-cols-2 gap-4">
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                   <div className="text-gray-800 break-words">{studentDetails.name || "暂无姓名"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">年龄</label>
                   <div className="text-gray-800 break-words">{studentDetails.age || "暂无年龄"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">性别</label>
                   <div className="text-gray-800 break-words">{studentDetails.gender || "暂无信息"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">入学日期</label>
                   <div className="text-gray-800 break-words">{studentDetails.enrollmentDate || "暂无日期"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">总课时</label>
                   <div className="text-gray-800 break-words">{studentDetails.totalClasses || 0}课时</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">已完成</label>
                   <div className="text-gray-800 break-words">{studentDetails.completedClasses || 0}课时</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">出勤率</label>
                   <div className="text-gray-800 break-words">{studentDetails.attendanceRate || "暂无数据"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">表现评级</label>
                   <div className="text-gray-800 break-words">{studentDetails.performance || "暂无评级"}</div>
                 </div>
               </div>
               
               
               
                               <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">备注</label>
                  <div className="text-gray-800 text-sm break-words">{studentDetails.notes || "暂无备注"}</div>
                </div>
             </div>
          </div>
        </div>
      )}

      {/* 家长详情弹窗 */}
      {showParentDetails && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-start justify-center z-50 py-10 px-4">
          <div className="bg-white p-6 rounded-2xl shadow-md w-96 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-lg font-semibold text-gray-800">家长详情</h2>
              <button
                onClick={() => setShowParentDetails(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

                         <div className="space-y-4">
               <div className="grid grid-cols-2 gap-4">
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">姓名</label>
                   <div className="text-gray-800 break-words">{parentDetails.name || "暂无姓名"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">关系</label>
                   <div className="text-gray-800 break-words">{parentDetails.relationship || "暂无关系"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">联系电话</label>
                   <div className="text-gray-800 break-words">{parentDetails.phone || "暂无电话"}</div>
                 </div>
                 <div>
                   <label className="block text-sm font-medium text-gray-700 mb-1">微信</label>
                   <div className="text-gray-800 break-words">{parentDetails.wechat || "暂无微信"}</div>
                 </div>
               </div>
               
                               <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">备注</label>
                  <div className="text-gray-800 text-sm break-words">{parentDetails.notes || "暂无备注"}</div>
                </div>
             </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserInfoCard;