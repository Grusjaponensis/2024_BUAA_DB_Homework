import server from "./server";

export const getCats = async () => {
  const response = await server.get("/cats/");
  return response.data;
};

export const feedCat = async (id: String) => {
    const response = await server.post(`/cats/${id}/feed`);
    return response.data;
  };