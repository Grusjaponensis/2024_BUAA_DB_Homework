import server from "./server";

export const createDonation = async (data: any) => {
  return await server.post('/donations/', data);
};

export const fetchDonationTotal = async (data: any) => {
    return await server.get('/donations/total', data);
};

export const fetchDonations = async () => { 
    return await server.get('/donations/');
};

export const exportDonations = async (data: any) => {
  try {
    console.log('exportDonations', data)
    const res = await server.get('/donations/export', data, 'blob');
    // console.log('res.data', res.data)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    // console.log('url', url)
    const link = document.createElement('a')
    link.href = url
    const filename = res.headers['content-disposition'].split('filename=')[1];
    link.setAttribute('download', filename)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.log(error)
  }
}