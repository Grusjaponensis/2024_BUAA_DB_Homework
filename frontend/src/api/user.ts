import server from "./server";

export const login = async (username: string, password: string) => {
    try {
        document.cookie = "access_token=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC";
        const response = await server.post(
            "/login/access-token",
            { username, password },
            { "Content-Type": "multipart/form-data" }
        );
        if (response.status === 200) {
            document.cookie = `access_token=${response.data.access_token};path=/`;
            await getProfile();
        } else {
            throw new Error(response.data.detail || '登录失败');
        }
    } catch (error) {
        console.error('登录出错:', error);
        throw error;
    }
};

export const signup = async (username: string, password: string) => {
    try {
        document.cookie = "access_token=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC";
        const response = await server.post(
            "users/register",
            { username, password },
            { "Content-Type": "multipart/form-data" }
        );
        if (response.status === 200) {
            document.cookie = `access_token=${response.data.access_token};path=/`;
        } else {
            throw new Error(response.data.detail || '注册失败');
        } 
    } catch (error) {
        console.error('注册出错:', error);
        throw error;
    }
};

export const getProfile = async () => {
    const response = await server.get("/users/profile");
    if (response.status === 200) {
        console.log(response.data);
        return response.data;
    } else {
        console.error(response.data);
    }
}