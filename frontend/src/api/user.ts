import server from "./server";
import snackbar from "./snackbar";
import {reactive} from "vue";

interface User{
    login: boolean;
    user_id: string;
    email: string;
    nickname: string;
    is_superuser: boolean;
    is_volunteer: boolean;
    avatar_url: string;
    password: string;
}

export const user = reactive<User>({
    login: false,
    user_id: '',
    email: '',
    nickname: '',
    is_superuser: false,
    is_volunteer: false,
    avatar_url: '',
    password: ''
})

interface Location {
    latitude: number;
    longitude: number;
}

export const location = reactive<Location>({
    latitude: 0,
    longitude: 0
})

export const login = async (username: string, password: string) => {
    try {
        document.cookie = "access_token=;path=/;expires=Thu, 01 Jan 1970 00:00:00 UTC";
        const response = await server.post(
            "/login/access-token",
            { username, password },
            { "Content-Type": "multipart/form-data" }
        );
        if (response != null && response.status === 200) {
            document.cookie = `access_token=${response.data.access_token};path=/`;
            const res = await getProfile();
            if (res === null) {
                snackbar.error("登录失败");
            }
            else if (res.status === 200) {
                snackbar.success("登录成功");
            } else {
                console.log(res.status)
                snackbar.error("登录失败");
            }
        } else {
            snackbar.error("登录失败");
            throw new Error(response.data.detail || '登录失败');
        }
    } catch (error) {
        console.error('登录出错:', error);
        throw error;
    }
};

export const signup = async (email: string, password: string, nickname: string) => {
    try {
        const response = await server.post(
            "/users/register",
            { email, password, nickname },
            { "Content-Type": "application/json" }
        );

        if (response != null && response.status === 200) {
            snackbar.success("注册成功");
        } else if (response != null && response.status === 409) {
            snackbar.error("邮箱已被注册");
        } else {
            snackbar.error("注册失败");
            console.log(response)
            if (response != null && response.data.detail) {
                throw new Error(response.data.detail || '注册失败');
            }
        } 
    } catch (error) {
        snackbar.error("注册出错")
        console.error('注册出错:', error);
        throw error;
    }
};

export const getProfile = async () => {
    const response = await server.get("/users/profile");
    if (response != null && response.status === 200) {
        user.login = true;
        user.user_id = response.data.id;
        user.email = response.data.email;
        user.nickname = response.data.nickname;
        user.is_superuser = response.data.is_superuser;
        user.is_volunteer = response.data.is_volunteer;
        user.avatar_url = response.data.avatar_url;
        user.password = response.data.password;
        console.log("登录成功！");
    } else {
        user.login = false;
        if (response != null) {
            console.error("Failed to load user profile: " + response.data);
        }
    }
    return response;
}

export const getPublicProfile = async (user_id: string) => { 
  console.log(`/users/profile/${user_id}`)
  try {
    const response = await server.get(`/users/profile/${user_id}`);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('获取用户资料失败', error);
    throw error;
  }
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

export const updateProfileByAdmin = async ( userId: number , profileData: any) => {
    try {
        const response = await server.patch(`/users/${userId}`, profileData);
        return response.data;
    } catch (error) {
        console.error('更新个人资料失败:', error);
        throw error;
    }
}

export const deleteUserByAdmin = async (userId: number) => {
    try {
        const response = await server._delete(`/users/${userId}`);
        return response.data;
    } catch (error) {
        console.error('删除用户失败:', error);
        throw error;
    }
}

export const getProfileByAdmin = async ( userId: number) => {
    try {
        const response = await server.get(`/users/${userId}`);
        return response.data;
    } catch (error) {
        console.error('获取个人资料失败', error);
        throw error;
    }
}

export const getActivityByAdmin = async (activityId: number) => {
    try {
        const response = await server.get(`/activities/${activityId}`);
        return response.data;
    } catch (error) {
        console.error('获取活动失败', error);
        throw error;
    }
}

export const updateAvatar = async (formData: FormData) => {
    try {
        const response = await server.patch("/users/profile/avatar", formData,{
            headers: {
                "Content-Type": "multipart/form-data",
            },
        });
        if (response != null && response.status === 200) {
            snackbar.success("更新头像成功");
        } else {
            snackbar.error("更新头像失败");
            console.log(response)
            if (response != null && response.data.detail) {
                throw new Error(response.data.detail || '更新头像失败');
            } else {
                throw new Error("更新头像失败");
            }
        }
    } catch (error) {
        snackbar.error("更新头像出错");
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