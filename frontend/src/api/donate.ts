import server from "./server";

export const createDonation = async (data: any) => {
  return await server.post('/donations/', data);
};