import { a } from "node_modules/unplugin-vue-router/dist/types-DBiN4-4c.cjs";
import server from "./server";

export const getActivities = async () => {
  const response = await server.get("/activities/");
  return response.data;
};

export const deleteActivity = async (id: string) => {
  try {
    const response = await server._delete(`/activities/${id}`);
    return response.data;
  } catch (error) {
    console.error('删除活动失败:', error);
    throw error; 
  }
};

export const createActivity = async (data: any) => {
  return await server.post('/activities/', data);
};

// 报名
export const signUp = async (activity_id: string, user_id :string) => {
    try {
      const response = await server.post(
        `/volunteers/${activity_id}`,
        { user_id , activity_id },
        { "Content-Type" : "application/json" }
      );
      return response.data;
    } catch (error) {
      console.error('报名失败:', error);
      throw error;
    }
  };
  
  // 退选
  export const withdraw = async (activity_id: string) => {
    try {
      const response = await server._delete(`/volunteers/${activity_id}`);
      return response.data;
    } catch (error) {
      console.error('退选失败:', error);
      throw error;
    }
  };