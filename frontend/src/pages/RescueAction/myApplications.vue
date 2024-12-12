<template>
  <div class="view-applications">
    <!-- 主内容区域 -->
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-row>
        <v-col cols="6" md="6" class="justify-center">
          <img src="@/assets/myapply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-if="loaded" v-for="application in applications"
          :key="application.id"
          class="my-2" cols="12" md="12">
          <v-card class="elevation-3 pa-2 text-center" outlined rounded="lg">
            <v-card-title class="headline">申请情况</v-card-title>
            <v-card-subtitle class="grey--text text-body-1">用户昵称: {{ users[application.user_id].nickname }}</v-card-subtitle>
            <v-card-subtitle class="grey--text text-body-1">用户邮箱: {{ users[application.user_id].email }}</v-card-subtitle>
            <v-card-subtitle class="grey--text text-body-1">
              申请日期: {{ new Date(application.created_at).toLocaleString() }}
            </v-card-subtitle>
            <v-card-subtitle class="text-body-1">
              状态: {{ application.status }}
            </v-card-subtitle>
            <v-card-subtitle class="mt-2 text-body-1">申请原因：{{ application.reason }}</v-card-subtitle>
            <v-card-items v-if="user.is_superuser && (application.status === 'pending')" class="mt-4 pa-2">
              <v-btn color="green-darken-1" rounded="lg" @click="approveApplication(application)">通过</v-btn>
              <v-btn color="red-darken-1" class="ml-1" rounded="lg" @click="rejectApplication(application)">拒绝</v-btn>
            </v-card-items>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  </template>
  
  <script setup>
  import { getProfileByAdmin } from '@/api/user';
  import { getMyApplications } from '@/api/volunteer';
  import { ref, onMounted } from 'vue';
  import { user } from '@/api/user';
  import { updateVolunteerApplicationStatus } from '@/api/volunteer';
  import snackbar from '@/api/snackbar';
  
  const applications = ref([]);
  const users = {};
  const loaded = ref(false);

  onMounted(() => {
    fetchApplications();
  });

  const approveApplication = async(application) => {
    try {
      await updateVolunteerApplicationStatus(application.id, "approved");
      await fetchApplications();
      snackbar.success('申请已通过');
    } catch (error) {
      snackbar.error('通过申请失败');
      console.error('通过申请失败:', error);
    }
  }

  const rejectApplication = async(application) => {
    try {
      await updateVolunteerApplicationStatus(application.id, "rejected");
      await fetchApplications();
      snackbar.success('申请已拒绝'); 
    } catch (error) {
      snackbar.error('拒绝申请失败');
      console.error('拒绝申请失败:', error);  
    }
  }

  const fetchApplications = async () => {
    try {
      const response = await getMyApplications();
      if (response) {
        applications.value = response;
        for (const application of applications.value) {
          users[application.user_id] = await getProfileByAdmin(application.user_id);
          console.log('获取用户信息成功:', users[application.user_id]);
        }
        console.log('获取申请列表成功:', applications.value);
        loaded.value = true;
      } else {
        console.error('获取申请列表失败:')
      }
    } catch (error) {
      console.error('获取申请列表失败:', error);
    }
  };
  </script>
  
  <style scoped>
  /* 页面的特定样式 */
  .view-applications {
  background-color: #f0f0f0;
  height: 100%;
}
  </style>