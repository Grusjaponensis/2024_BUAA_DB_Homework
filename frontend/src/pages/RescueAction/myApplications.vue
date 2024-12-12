<template>
  <div class="view-applications">
    <!-- 主内容区域 -->
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-row>
        <v-col cols="12" md="12" class="justify-center">
          <img src="@/assets/myapply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-for="application in applications"
          :key="application.id"
          class="my-2" cols="12" md="4">
          <v-card style="border: 2px solid #d1e9f4; border-radius: 10px;">
            <v-card-title class="headline">申请情况</v-card-title>
            <v-card-subtitle>基本信息：{{ application.name }} - {{ application.age }} - {{ application.gender }}</v-card-subtitle>
            <v-card-subtitle class="grey--text">
              申请日期: {{ new Date(application.create_at).toLocaleString() }}
            </v-card-subtitle>
            <v-card-subtitle>
              状态: {{ application.status }}
            </v-card-subtitle>
            <v-card-subtitle style="margin-top: 10px;margin-bottom: 10px;">{{ application.reason }}</v-card-subtitle>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  </template>
  
  <script setup>
  import { getMyApplications } from '@/api/volunteer';
  import { ref, onMounted } from 'vue';
  
  const applications = ref([]);

  onMounted(() => {
    fetchApplications();
  });

  const fetchApplications = async () => {
    try {
      const response = await getMyApplications();
      applications.value = response.applications;
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