import server from "./server";

export const getCats = async () => {
  const response = await server.get("/cats/");
  return response.data;
};

// export const feedCat = async (id: String) => {
//     const response = await server.post(`/cats/${id}/feed`);
//     return response.data;
//   };

export const createCat = async (cat: any) => {
  const response = await server.post("/cats/", cat);
  return response.data;
};

export const deleteCat = async (id: String) => {
  const response = await server._delete(`/cats/${id}`);
  return response.data;
};

export const updateCat = async (id: String, cat: any) => {
  const response = await server.put(`/cats/${id}`, cat);
  return response.data;
};

export const getCat = async (id: String) => {
  const response = await server.get(`/cats/${id}`);
  return response.data;
};

export const updateCatByAdmin = async (id: String, cat: any) => {
  try {
    const response = await server.patch(`/cats/${id}/info`, cat ,
      { headers: { "Content-Type": "application/json" } }
    );
    return response.data;
  } catch (error) {
    console.log(error);
  }
}