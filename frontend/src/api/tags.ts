// src/api/tags.ts
import server from './server';

export const getTags = async () => {
  const response = await server.get('/posts/tags');
  return response.data;
};

export const remove = async (id: number) => {
  const response = await server._delete(`/posts/tags/${id}`);
  return response.data;
};

export const create = async (name: string) => {
  const response = await server.post('/posts/tags', { name });
  return response.data;
};
