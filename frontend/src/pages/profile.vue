<template>
    <v-container class="pa-10" fluid>
      <v-row justify="center">
        <v-card class="mx-auto my-4" max-width="400" rounded="lg" elevation="4">
            <!-- 头像展示 -->
            <v-card-text class="text-center">
              <v-avatar size="128" class="elevation-4" @click="showAvatarUpload = true">
                <v-img :src="addPrefix(profile.avatar_url)" alt="用户头像"></v-img>
              </v-avatar>
              <div class="mt-4">
                <div class="text-h6 font-weight-bold">昵称：{{ profile.nickname}}</div>
                <div class="text-subtitle-1 text-grey-darken-1">邮箱：{{ profile.email }}</div>
                <div class="text-subtitle-2 mt-2">
                  <v-chip color="green" small v-if="!profile.is_superuser">
                    志愿者：{{ profile.is_volunteer ? "是" : "否" }}
                  </v-chip>
                  <v-chip color="red" small v-if="profile.is_superuser">超级管理员</v-chip>
                </div>
                </div>
                <v-expand-transition>
                <div v-show="showProfileEdit" class="mt-8">
                <v-text-field
                    v-model="newNickname"
                    label="昵称"
                    type="text"
                    outlined
                    :rules="[v => !!v || '昵称不能为空']"
                ></v-text-field>
                <v-text-field
                    v-model="newEmail"
                    label="邮箱"
                    type="text"
                    outlined
                    :rules="[v => !!v || '邮箱不能为空']"
                ></v-text-field>
                <v-btn color="primary" @click="updateUserProfile">确认更新</v-btn>
                <v-btn color="grey" text @click="showProfileEdit = false">取消</v-btn>
                </div>
                </v-expand-transition>

                <v-expand-transition>
                    <div v-show="showAvatarUpload" class="mt-8">
                    <v-file-input
                        v-model="avatarFile"
                        label="更新头像"
                        placeholder="点击上传头像"
                        accept="image/*"
                    ></v-file-input>
                    <v-btn color="primary" @click="updateUserAvatar">确认更新头像</v-btn>
                    <v-btn color="grey" text @click="showAvatarUpload = false">取消</v-btn>
                    </div>
                </v-expand-transition>
        
                <v-expand-transition>
                    <div v-show="showPasswordChange" class="mt-8">
                    <v-text-field
                        v-model="oldPassword"
                        label="旧密码"
                        type="text"
                        outlined
                    ></v-text-field>
                    <v-text-field
                        v-model="newPassword"
                        label="新密码"
                        type="text"
                        outlined
                    ></v-text-field>
                    <v-btn color="primary" @click="updateUserPassword">确认更新密码</v-btn>
                    <v-btn color="grey" text @click="showPasswordChange = false">取消</v-btn>
                    </div>
                </v-expand-transition>
            </v-card-text>
  
            <!-- 按钮组 -->
            <v-card-actions class="justify-center pb-4">
              <v-btn color="primary" rounded="lg" variant="elevated" @click="showProfileEdit = true">
                <v-icon left>mdi-pencil</v-icon> 修改资料
              </v-btn>
              <v-btn color="green" rounded="lg" variant="elevated" @click="showAvatarUpload = true">
                <v-icon left>mdi-image</v-icon> 更新头像
              </v-btn>
              <v-btn color="red" rounded="lg" variant="elevated" @click="showPasswordChange = true">
                <v-icon left>mdi-lock</v-icon> 修改密码
              </v-btn>
            </v-card-actions>
          </v-card>
    </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, reactive, onMounted } from 'vue';
  import { getProfile, updateProfile, updateAvatar, updatePassword } from '@/api/user';
  import { addPrefix } from '@/api/post'
  import snackbar from '@/api/snackbar';
  
const showAvatarUpload = ref(false);
const showPasswordChange = ref(false);
const showProfileEdit = ref(false);

const profile = ref(null);
const avatarFile = ref(null);
const newPassword = ref('');
const oldPassword = ref('');
const newNickname = ref('');
const newEmail = ref('');

const fetchProfile = async () => {
    try {
        const response = await getProfile();
        profile.value = {
          email: response.data.email,
          nickname: response.data.nickname,
          avatar_url: response.data.avatar_url,
          is_volunteer: response.data.is_volunteer,
          is_superuser: response.data.is_superuser,
        }
        newNickname.value = response.data.nickname;
        newEmail.value = response.data.email;
        console.log('个人资料获取成功', profile.value);
    } catch (error) {
        console.error('获取个人资料失败:', error);
    }
};

const updateUserProfile = async () => {
    try {
        const profileData = {
        email: newEmail.value,
        nickname: newNickname.value,
        };

        const response = await  updateProfile(profileData);
        console.log('个人资料更新成功', response);
        showProfileEdit.value = false;
        fetchProfile();
        snackbar.success('个人资料更新成功');
    } catch (error) {
        console.error('更新个人资料失败:', error);
        snackbar.error('更新个人资料失败');
    }
};

const updateUserAvatar = async () => {
    try {
        const formData = new FormData();
        formData.append('avatar', avatarFile.value);
        await updateAvatar(formData);
        console.log('头像更新成功');
        showAvatarUpload.value = false;
        snackbar.success('头像更新成功');
        fetchProfile();
    } catch (error) {
        console.error('更新头像失败:', error);
        snackbar.error('更新头像失败');
    }
};

const updateUserPassword = async () => {
    try {
        const editPasswordData = {
        old_password: oldPassword.value,
        new_password: newPassword.value,
        };
        const response = await updatePassword(editPasswordData);
        console.log('密码更新成功', response);
        snackbar.success('密码更新成功');
        showPasswordChange.value = false;
    } catch (error) {
        console.error('更新密码失败:', error);
        snackbar.error('更新密码失败');
    }
};


onMounted(fetchProfile);
</script>

<style scoped>
  .strong {
  display: block;
  margin-top: 15px;
  }
</style>