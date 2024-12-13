import server from "./server";

export const getCats = async () => {
  const response = await server.get("/cats/");
  if (response != null) {
    return response.data;
  } else {
    throw new Error("Failed to get cats");
  }
};

// export const feedCat = async (id: String) => {
//     const response = await server.post(`/cats/${id}/feed`);
//     return response.data;
//   };

export const createCat = async (cat: any) => {
  const response = await server.post("/cats/", cat);
  if (response.data != null) {
    return response.data;
  } else if (response.status === 400) {
    throw new Error("Failed to create cat");
  }
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
    const response = await server.patch(`/cats/${id}/info`, cat);
    return response.data;
  } catch (error) {
    console.log(error);
  }
}

export const updateCatLocation = async (id: String, longitude: number, latitude: number) => {
  try {
    await server.patch(
      `/cats/${id}/location`, 
      { longitude, latitude },
      { headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.log(error)
  }
}