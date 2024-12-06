import server from "./server"; 

// 获取所有志愿者申请
export const getApplications = async () => {
  try {
    const response = await server.get("/volunteers/");
    return response.data;
  } catch (error) {
    console.error('获取申请列表失败:', error);
    throw error; 
  }
};

// 更新志愿者申请状态
export const updateApplicationStatus = async (id: string, status: string) => {
  try {
    const response = await server.patch(`/volunteers/${id}/status`, { status });
    return response.data;
  } catch (error) {
    console.error(`更新申请状态失败: ${error}`);
    throw error; 
  }
};

export const getMyApplications = async () => {
    try {
      const response = await server.get("/volunteers/my");
      return response.data;
    } catch (error) {
      console.error('获取我的申请列表失败:', error);
      throw error; 
    }
  };

  export const submitApplication = async (applicant: any) => {
    try {
      const response = await server.post("/volunteers/", applicant);
      return response.data; 
    } catch (error) {
      console.error('提交申请失败:', error);
      throw error; 
    }
  };