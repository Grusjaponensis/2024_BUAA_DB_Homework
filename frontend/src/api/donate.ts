import server from "./server";

export const createDonation = async (data: any) => {
  return await server.post('/donations/', data);
};

export const fetchDonationTotal = async (data: any) => {
    return await server.get('/donations/total/', data);
};

export const fetchDonations = async () => { 
    return await server.get('/donations/');
};