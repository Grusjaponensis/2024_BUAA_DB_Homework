import axios from "axios";

const server = axios.create({
    baseURL: '/api/v1',
	withCredentials: true,
});

const get = async (url: string, params?: any) => {
    let headers = {};
	if (document.cookie.includes('access_token=')) {
		headers = {
            Authorization: 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0]
		}
	}
	try {
		const res = await server.get(url, { params, headers: { ...headers } })
		return res
	} catch (error) {
		console.error(error);
	}
};

const post = async (url: string, data?: any, headers = {})=> {
	if (document.cookie.includes('access_token=')) {
		headers = {
			...headers,
            Authorization: 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0]
		}
	}
    console.log(headers)    
	try {
		const res = await server.post(
			url,
			data,
			{ headers:{ ...headers } }
		)
		return res
	} catch (error) {
		console.error(error);
	}
};

const put = async (url: string, data?: any, headers = {}) => {
	if (document.cookie.includes('access_token=')) {
		headers = {
			...headers,
            'Authorization': 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0]
		}
	}
	try {
		const res = await server.put(
			url,
			data,
			{ headers:{ ...headers } }
		)
		return res
	} catch (error) {
		console.error(error);
	}
}

const _delete = async (url: string, data?: any) => {
	let headers = {};
	if (document.cookie.includes('access_token=')) {
		headers = {
			...headers,
            'Authorization': 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0]
		}
	}
	try {
		const res = await server.delete(
			url,
			{ headers:{ ...headers } }
		)
		return res
	} catch (error) {
		console.error(error);
	}
}
const patch = async (url: string, data?: any, headers = {}) => {
	if (document.cookie.includes('access_token=')) {
	  headers = {
		...headers,
		Authorization: 'Bearer ' + document.cookie.split('access_token=')[1].split(';')[0]
	  };
	}
	try {
	  const res = await server.patch(url, data, { headers: { ...headers } });
	  return res;
	} catch (error) {
	  console.error(error);
	}
  };
  
export default {
    get,
    post,
    put,
    _delete,
	patch,
};