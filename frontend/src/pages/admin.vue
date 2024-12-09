<template>
    <v-container>
      <!-- 用户数量展示 -->
      <v-row justify="center">
        <v-chip class="ma-4" color="primary" label>
          <v-icon left>mdi-account-group</v-icon> 用户数量：{{ count }}
        </v-chip>
      </v-row>
  
      <!-- 用户卡片列表 -->
      <v-row justify="center">
        <v-col cols="12" md="4" v-for="profile in acounts" :key="profile.id">
          <v-card class="mx-auto my-4" max-width="400" rounded="lg" elevation="4">
            <!-- 头像展示 -->
            <v-card-text class="text-center">
              <v-avatar size="128" class="elevation-4" @click="showAvatarUpload = true">
                <v-img :src="addPrefix(profile.avatar_url)" alt="用户头像"></v-img>
              </v-avatar>
              <div class="mt-4">
                <div class="text-h6 font-weight-bold">昵称：{{ profile.nickname }}</div>
                <div class="text-subtitle-1 text-grey-darken-1">邮箱：{{ profile.email }}</div>
                <div class="text-subtitle-2 mt-2">
                  <v-chip color="green" small v-if="!profile.is_superuser">
                    志愿者：{{ profile.is_volunteer ? "是" : "否" }}
                  </v-chip>
                  <v-chip color="red" small v-if="profile.is_superuser">超级管理员</v-chip>
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
  
              <!-- 更新头像区域 -->
              <v-expand-transition>
                <div v-show="showStates[profile.id]?.showAvatarUpload" class="mt-8">
                  <v-file-input
                    v-model="avatarFile"
                    label="更新头像"
                    placeholder="点击上传头像"
                    accept="image/*"
                  ></v-file-input>
                  <v-btn color="primary" @click="updateUserAvatar(profile.id)">确认更新头像</v-btn>
                  <v-btn color="grey" text @click="toggleSection(profile.id, 'showAvatarUpload', false)">取消</v-btn>
                </div>
              </v-expand-transition>
  
              <!-- 修改密码区域 -->
              <v-expand-transition>
                <div v-show="showStates[profile.id]?.showPasswordChange" class="mt-8">
                  <v-text-field v-model="oldPassword" label="旧密码" type="text" outlined></v-text-field>
                  <v-text-field v-model="newPassword" label="新密码" type="text" outlined></v-text-field>
                  <v-btn color="primary" @click="updateUserPassword(profile.id)">确认更新密码</v-btn>
                  <v-btn color="grey" text @click="toggleSection(profile.id, 'showPasswordChange', false)">取消</v-btn>
                </div>
              </v-expand-transition>
            </v-card-text>
  
            <!-- 按钮组 -->
            <v-card-actions class="justify-center pb-4">
              <v-btn
                color="primary"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showProfileEdit', true)"
              >
                <v-icon left>mdi-pencil</v-icon> 修改资料
              </v-btn>
              <v-btn
                color="green"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showAvatarUpload', true)"
              >
                <v-icon left>mdi-image</v-icon> 更新头像
              </v-btn>
              <v-btn
                color="red"
                rounded="lg"
                variant="elevated"
                @click="toggleSection(profile.id, 'showPasswordChange', true)"
              >
                <v-icon left>mdi-lock</v-icon> 修改密码
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { getUsers } from "../api/superuser";
  import { addPrefix } from "../api/post";
  
  const count = ref(0);
  const acounts = ref([]);
  const showStates = ref({});
  const newNickname = ref("");
  const newEmail = ref("");
  const avatarFile = ref(null);
  const oldPassword = ref("");
  const newPassword = ref("");
  
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
  };
  
  // 更新个人资料
  const updateUserProfile = async (id) => {
    console.log("更新资料:", id, newNickname.value, newEmail.value);
    toggleSection(id, "showProfileEdit", false);
  };
  
  // 更新头像
  const updateUserAvatar = async (id) => {
    console.log("更新头像:", id, avatarFile.value);
    toggleSection(id, "showAvatarUpload", false);
  };
  
  // 更新密码
  const updateUserPassword = async (id) => {
    console.log("更新密码:", id, oldPassword.value, newPassword.value);
    toggleSection(id, "showPasswordChange", false);
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
  