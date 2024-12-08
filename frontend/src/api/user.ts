import server from "./server";
import snackbar from "./snackbar";
import {reactive} from "vue";

interface User{
    login: boolean;
    email: string;
    nickname: string;
    is_superuser: boolean;
    is_volunteer: boolean;
    avatar_url: string;
    password: string;
}

export const user = reactive<User>({
    login: false,
    email: '',
    nickname: '',
    is_superuser: false,
    is_volunteer: false,
    avatar_url: '',
    password: ''
})

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
            const res = await getProfile();
            if (res.status === 200) {
                snackbar.success("登录成功");
            }
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
        user.login = true;
        user.email = response.data.email;
        user.nickname = response.data.nickname;
        user.is_superuser = response.data.is_superuser;
        user.is_volunteer = response.data.is_volunteer;
        user.avatar_url = response.data.avatar_url;
        user.password = response.data.password;
        console.log(response.data);
    } else {
        user.login = false;
        console.error(response.data);
    }
    return response.data;
}
  
// 更新用户个人资料
export const updateProfile = async (profileData: any) => {
    try {
        const response = await server.patch("/users/profile", profileData);
        return response.data; 
    } catch (error) {
        console.error('更新个人资料失败:', error);
        throw error;
    }
};

// 更新用户头像
export const updateAvatar = async (formData: FormData) => {
try {
    const response = await server.patch("/users/profile/avatar", formData, {
    headers: {
        "Content-Type": "multipart/form-data",
    },
    });
    return response.data; 
} catch (error) {
    console.error('更新头像失败:', error);
    throw error; 
}
};

// 更新用户密码
export const updatePassword = async (formData: FormData) => {
try {
    const response = await server.patch("/users/profile/password", formData, {
    headers: {
        "Content-Type": "multipart/form-data",
    },
    });
    return response.data; 
} catch (error) {
    console.error('更新密码失败:', error);
    throw error; 
}
};