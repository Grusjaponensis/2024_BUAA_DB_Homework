<template>
    <v-container class="pa-0">
      <v-card class="mx-auto my-8 pa-1" max-width="400">
        <v-card-title class="headline font-weight-bold">个人资料</v-card-title>
        <v-card-text class="px-8 pt-6" v-if="profile">
          <div class="text-center">
            <v-avatar size="128" class="mb-4">
              <v-img :src="`${addPrefix(profile.avatar_url)}`" @click="showAvatarUpload = true"></v-img>
            </v-avatar>
          
            <p class="text-h6 font-weight-bold mb-1">{{ profile.nickname }}</p>
            <p class="text-h6 mb-1">{{ profile.email }}</p>
            <v-chip v-if="!profile.is_superuser && profile.is_volunteer" class="mt-3" color="blue-darken-1">志愿者</v-chip>
            <v-chip v-if="profile.is_superuser" class="mt-3" color="purple-darken-1">超级管理员</v-chip>
            <v-chip v-if="!profile.is_superuser && !profile.is_volunteer" class="mt-3" color="green-darken-1">普通用户</v-chip>
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
              <div class="text-center">
                <v-btn color="primary" variant="text" @click="updateUserProfile">确认更新</v-btn>
                <v-btn color="grey" variant="text" @click="showProfileEdit = false">取消</v-btn>
              </div>
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
              <div class="text-center">
                <v-btn color="primary" variant="text" @click="updateUserAvatar">确认更新头像</v-btn>
                <v-btn color="grey" variant="text" @click="showAvatarUpload = false">取消</v-btn>
              </div>
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
              <div class="text-center">
                <v-btn color="primary" variant="text" @click="updateUserPassword">确认更新密码</v-btn>
                <v-btn color="grey" variant="text" @click="showPasswordChange = false">取消</v-btn>
              </div>
            </div>
          </v-expand-transition>
        </v-card-text>
        <div class="pb-8">
          <div class="text-center">
            <v-btn color="primary" variant="text" @click="showProfileEdit = true">修改资料</v-btn>
            <v-btn color="primary" variant="text" @click="showAvatarUpload = true">更新头像</v-btn>
            <v-btn color="primary" variant="text" @click="showPasswordChange = true">修改密码</v-btn>
          </div>
        </div>
      </v-card>
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
      if (!newNickname.value || !newEmail.value || newNickname.value.trim() === '' || newEmail.value.trim() === '') {
        snackbar.error('昵称或邮箱不能为空');
        return;
      }
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