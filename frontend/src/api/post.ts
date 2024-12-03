import server from "./server";

export const getPosts = async () => {
  return await server.get("/posts/");
};