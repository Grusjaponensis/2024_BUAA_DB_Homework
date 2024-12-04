// src/api/tags.ts
import server from './server';

export const getTags = async () => {
  const response = await server.get('/posts/tags');
  return response.data;
};