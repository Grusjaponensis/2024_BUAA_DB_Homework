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

export const updatePost = async (id: string, params: any, data: any) => {
  let headers = {};
  if (document.cookie.includes('access_token=')) {
    headers = {
      ...headers,
      'Authorization': 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0],
      'Content-Type': 'multipart/form-data',
    };
  }

  try {
    const response = await server.patch(`/posts/${id}`, data, {
      params, 
      headers, 
    });
    return response.data;
  } catch (error) {
    console.error('更新帖子失败:', error);
    throw error;
  }
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
