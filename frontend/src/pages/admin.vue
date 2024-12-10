<template>
    <v-container>
      <!-- 用户数量展示 -->
      <v-row justify="center">
        <v-chip class="ma-4" color="primary" label>
          <v-icon left class="mr-2">mdi-account-group</v-icon> 用户数量：{{ count }}
        </v-chip>
      </v-row>
  
      <!-- 用户卡片列表 -->
      <v-row justify="center">
        <v-col cols="12" md="4" v-for="profile in acounts" :key="profile.id">
          <v-card class="mx-auto my-4" max-width="600" rounded="lg" elevation="4">
            <!-- 头像展示 -->
            <v-card-text class="text-center">
              <v-avatar size="128" class="elevation-4" @click="showAvatarUpload = true">
                <v-img :src="addPrefix(profile.avatar_url)" alt="用户头像"></v-img>
              </v-avatar>
              <div class="mt-4">
                <div class="text-h6 font-weight-bold ma-2">{{ profile.nickname }}</div>
                <div class="text-subtitle-1 text-grey-darken-1">{{ profile.email }}</div>
                <div class="text-subtitle-2 mt-2">
                  <v-chip small v-if="!profile.is_superuser && profile.is_volunteer" class="ma-1" color="blue-darken-1">
                    志愿者
                  </v-chip>
                  <v-chip small v-if="profile.is_superuser" class="ma-1" color="purple-darken-1">超级管理员</v-chip>
                  <v-chip small v-if="!profile.is_superuser && !profile.is_volunteer" class="ma-1" color="green-darken-1">普通用户</v-chip>
                </div>
              </div>
  
              <!-- 修改资料区域 -->
              <v-expand-transition>
                <div v-show="showStates[profile.id]?.showProfileEdit" class="mt-8">
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
                  <v-btn color="primary" @click="updateUserProfile(profile.id)">确认更新</v-btn>
                  <v-btn color="grey" text @click="toggleSection(profile.id, 'showProfileEdit', false)">取消</v-btn>
                </div>
              </v-expand-transition>
  
              <!-- 设置身份区域 -->
              <v-expand-transition>
                <div v-show="showStates[profile.id]?.showIdentityEdit" class="mt-8">
                  <v-select
                    v-model="newRole"
                    :items="['志愿者', '普通用户']"
                    label="设置身份"
                    outlined
                    dense
                  ></v-select>
                  <v-btn color="primary" @click="updateUserIdentity(profile.id)">确定</v-btn>
                  <v-btn color="grey" text @click="toggleSection(profile.id, 'showIdentityEdit', false)">取消</v-btn>
                </div>
              </v-expand-transition>

              <v-expand-transition>
                <div v-show="showStates[profile.id]?.showAvatarUpload" class="mt-8">
                  <v-file-input
                    v-model="avatarFile"
                    label="上传头像"
                    placeholder="点击上传头像"
                    accept="image/*"
                  ></v-file-input>
                  <v-btn color="primary" @click="onAvatarUpload(profile.id)">确认上传</v-btn>
                  <v-btn color="grey" text @click="toggleSection(profile.id, 'showAvatarUpload', false)">取消</v-btn>
                </div>
              </v-expand-transition>
            </v-card-text>
  
            <!-- 按钮组 -->
            <v-card-actions class="justify-center pb-4">
              <v-btn
                color="blue-accent-3"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showProfileEdit', true)"
              >
                <v-icon left class="mr-1">mdi-pencil</v-icon> 修改资料
              </v-btn>
              <v-btn
                color="green-accent-2"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showIdentityEdit', true)"
                v-if="!profile.is_superuser"
              >
                <v-icon left class="mr-1">mdi-image</v-icon> 设置身份
              </v-btn>

              <v-btn
                color="red-accent-4"
                rounded="lg"
                variant="elevated"
                @click="showDeleteDialog = true; deleteId = profile.id"
                v-if="!profile.is_superuser"
              >
                <v-icon left class="mr-1">mdi-delete</v-icon> 删除用户
              </v-btn>

              <v-btn
                color="purple-accent-3"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showAvatarUpload', true)"
                v-if="profile.is_superuser"
              >
              <v-icon left class="mr-1">mdi-image</v-icon> 修改头像
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>

      <v-dialog v-model="showDeleteDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">
            确认删除
          </v-card-title>
          <v-card-text>
            确认要删除该用户吗？此操作不可恢复。
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click = "showDeleteDialog = false"> 取消</v-btn>
            <v-btn color="red" @click = "deleteUser(deleteId)"> 确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
    <v-btn
      color="blue-accent-3"
      class="elevation-4"
      style="position: fixed; bottom: 24px; right: 24px;"
      size="large"
      to = "/signup"
    >
    <v-icon>mdi-plus</v-icon>
    </v-btn>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { getUsers } from "../api/superuser";
  import { addPrefix } from "../api/post";
  import snackbar from '../api/snackbar'
  import { useRouter } from 'vue-router';
  import { updateProfileByAdmin , deleteUserByAdmin , updateAvatar } from '@/api/user';
  
  const count = ref(0);
  const acounts = ref([]);
  const showStates = ref({});
  const newNickname = ref("");
  const newEmail = ref("");
  const oldPassword = ref("");
  const newPassword = ref("");
  const router = useRouter();
  const avatarFile = ref(null);
  const showDeleteDialog = ref(false);
  const deleteId = ref(0);

  const showAvatarUpload = ref(false);
  const newRole = ref('');
  const showIdentityEdit = ref(false); 
  const showProfileEdit = ref(false);

  // 初始化数据
  onMounted(async () => {
    const users = await getUsers();
    count.value = users.count;
    acounts.value = users.data;
  
    // 初始化状态管理对象
    acounts.value.forEach((user) => {
      showStates.value[user.id] = {
        showProfileEdit: false,
        showAvatarUpload: false,
        showPasswordChange: false,
      };
    });
  });
  
  // 切换展开状态
  const toggleSection = (id, section, value) => {
    Object.keys(showStates.value).forEach((key) => {
      showStates.value[key][section] = key == id ? value : false;
    });

    if (section === "showProfileEdit" && value) {
        const user = acounts.value.find((u) => u.id === id)
        newNickname.value = user.nickname;
        newEmail.value = user.email;
    }

    if (section === "showIdentityEdit" && value) {
        const user = acounts.value.find((u) => u.id === id)
        newRole.value = user.is_volunteer ? '志愿者' : '普通用户';
    }
  };

  const fetchProfile = async () => {
    try {
        const updatedUsers = await getUsers();
        const updatedData = updatedUsers.data;
        acounts.value = acounts.value.map((user) => {
            const updatedUser = updatedData.find((u) => u.id === user.id);
            return updatedUser ? updatedUser : user;
        });
    } catch (error) {
        console.error('获取更新个人资料失败:', error);
        snackbar.error('获取更新个人资料失败');
    }
  }
  
  // 更新个人资料
  const updateUserProfile = async (id) => {
    try {
      if (!newNickname.value || !newEmail.value || newNickname.value.trim() === '' || newEmail.value.trim() === '') {
        snackbar.error('昵称或邮箱不能为空');
        return;
      }
      const profileData = {
        email: newEmail.value,
        nickname: newNickname.value,
      };
      const response = await updateProfileByAdmin(id , profileData);
      console.log('个人资料更新成功', response);
      showProfileEdit.value = false;
      await fetchProfile();
      snackbar.success('个人资料更新成功');
      toggleSection(id, "showProfileEdit", false);
    } catch (error) {
      console.error('更新个人资料失败:', error);
      snackbar.error('更新个人资料失败');
    }
  };
  
  // 设置身份
  const updateUserIdentity = async(id) => {
    try {
        const profileData = {
            is_volunteer: newRole.value == '志愿者'
        };
        const response = await updateProfileByAdmin(id, profileData);
        console.log('设置身份成功', response);
        showIdentityEdit.value = false;
        await fetchProfile();
        snackbar.success('设置身份成功');
        toggleSection(id, "showIdentityEdit", false);
    } catch (error) {
        console.error('设置身份失败:', error);
        snackbar.error('设置身份失败');
    }
  }

  const deleteUser = async(id) => {
    try {
      const response = await deleteUserByAdmin(id);
      console.log('删除用户成功', response);
      acounts.value = acounts.value.filter((user) => user.id !== id);
      count.value = count.value - 1;
      snackbar.success('删除用户成功');
    } catch (error) {
      console.error('删除用户失败:', error);
      snackbar.error('删除用户失败');
    }
    showDeleteDialog.value = false;
  }

  const onAvatarUpload = async (id) => {
    try {
        const formData = new FormData();
        formData.append('upload_avatar', avatarFile.value);
        if (avatarFile.value === null) {
          snackbar.error('请选择图片文件');
          return;
        }
        await updateAvatar(formData);
        console.log('头像更新成功');
        showAvatarUpload.value = false;
        fetchProfile();
        toggleSection(id, "showAvatarUpload", false);
    } catch (error) {
        console.error('更新头像失败:', error);
    }
  };
  </script>
  
  <style scoped>
  .v-card {
    transition: transform 0.3s ease;
  }
  
  .v-card:hover {
    transform: translateY(-4px);
  }
  
  .v-btn {
    margin: 4px;
    text-transform: none;
  }
  </style>