<template>
  <div class="view-applications">
    <!-- 主内容区域 -->
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-col>
        <v-col cols="12" md="12" class="justify-center">
          <img src="@/assets/myapply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-for="application in applications"
          :key="application.id"
          class="my-2" cols="12" md="6">
          <v-card class="elevation-3 pa-2 text-center" outlined rounded="lg">
            <v-card-title class="headline">申请情况</v-card-title>
            <!-- <v-card-subtitle>基本信息：{{ users[application.user_id].name }} - {{ users[application.user_id].age }} - {{ application.gender }}</v-card-subtitle> -->
            <v-card-subtitle class="grey--text text-body-2">
              申请日期: {{ new Date(application.created_at).toLocaleString() }}
            </v-card-subtitle>
            <v-card-subtitle class="text-body-2">
              状态: {{ application.status }}
            </v-card-subtitle>
            <v-card-subtitle class="mt-2 text-body-1">申请原因：{{ application.reason }}</v-card-subtitle>
            <v-card-items v-if="user.is_superuser" class="mt-4 pa-2">
              <v-btn color="green-darken-1" rounded="lg" @click="approveApplication(application)">通过</v-btn>
              <v-btn color="red-lighten-1" class="ml-1" rounded="lg" @click="rejectApplication(application)">拒绝</v-btn>
            </v-card-items>
          </v-card>
        </v-col>
      </v-col>
    </v-container>
  </div>
  </template>
  
  <script setup>
  import { getProfileByAdmin } from '@/api/user';
  import { getMyApplications } from '@/api/volunteer';
  import { ref, onMounted } from 'vue';
  import { user } from '@/api/user';
  import { updateVolunteerApplicationStatus } from '@/api/volunteer';
  
  const applications = ref([]);
  const users = {};

  onMounted(() => {
    fetchApplications();
  });

  const approveApplication = async(application) => {
    try {
      await updateVolunteerApplicationStatus(application.id, 'approved');
      await fetchApplications();
    } catch (error) {
      console.error('通过申请失败:', error);
    }
  }

  const fetchApplications = async () => {
    try {
      const response = await getMyApplications();
      applications.value = response;
      for (const application of applications.value) {
        users[application.user_id] = await getProfileByAdmin(application.user_id);
      }
      console.log('获取申请列表成功:', applications.value);
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