import server from "./server";

export const getPosts = async () => {
  const response = await server.get("/posts/");
  return response.data;
};

export const deletePost = async (id: string) => {
  try {
    const response = await server._delete(`/posts/${id}`,id);
    return response.data;
  } catch (error) {
    console.error('删除帖子失败:', error);
    throw error; 
  }
};

export const createPost = async (data: any) => {
  return await server.post('/posts/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
};

export const likePost = async (id) => {
  const response = await server.post(`/posts/${id}/like`);
  return response.data;
};

export const unlikePost = async (id) => {
  const response = await server._delete(`/posts/${id}/like`);
  return response.data;
};

export const getPost = async (id: string) => {
  try {
    const response = await server.get(`/posts/${id}`);
    return response.data; 
  } catch (error) {
    console.error('获取帖子详情失败:', error);
    throw error; 
  }
};

export const getMyPosts = async () => {
  const response = await server.get("/posts/my");
  return response.data;
};
