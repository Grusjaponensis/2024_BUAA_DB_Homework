import server from "./server";

export const getPosts = async () => {
  return await server.get("/posts/");
};

export const deletePost = async (id: string) => {
  try {
    const response = await server._delete(`/posts/${id}`);
    return response.data;
  } catch (error) {
    console.error('删除帖子失败:', error);
    throw error; 
  }
};

export const createPost = async (data: any) => {
  return await server.post('/posts/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
};