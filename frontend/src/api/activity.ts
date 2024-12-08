import server from "./server";

export const getActivities = async () => {
  const response = await server.get("/activities/");
  return response.data;
};

export const deleteActivity = async (id: string) => {
  try {
    const response = await server._delete(`/activities/${id}`,id);
    return response.data;
  } catch (error) {
    console.error('删除活动失败:', error);
    throw error; 
  }
};

export const createActivity = async (data: any) => {
  return await server.post('/activities/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
};

// 报名
export const signUp = async (id: string) => {
    try {
      const response = await server.post(`/activities/${id}/sign-up`);
      return response.data;
    } catch (error) {
      console.error('报名失败:', error);
      throw error;
    }
  };
  
  // 退选
  export const withdraw = async (id: string) => {
    try {
      const response = await server.post(`/activities/${id}/withdraw`);
      return response.data;
    } catch (error) {
      console.error('退选失败:', error);
      throw error;
    }
  };