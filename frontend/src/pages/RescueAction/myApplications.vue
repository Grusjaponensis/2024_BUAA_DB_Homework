<template>
    <!-- 主内容区域 -->
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-row>
        <v-col cols="12" md="12" justify="center" align="center">
          <img src="@/assets/myapply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-for="application in applications"
          :key="application.id"
          class="my-2" cols="12" md="4">
          <v-card>
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
  </template>
  
  <script setup>
  import { getMyApplications } from '@/api/volunteer';
  import { ref, onMounted } from 'vue';
  
  const applications = ref([]);
  
  const applicationDate = {
    data: [
      {
        id: 1,
        name: '张三',
        age: 20,
        gender: '男',
        create_at: '2022-01-01 12:00:00',
        status: '已完成',
        reason: '我是申请理由'
      },
      {
        id: 2,
        age: 25,
        gender: '女',
        create_at: '2022-01-02 12:00:00',
        status: '已完成',
        reason: '我是申请理由'
      },
      {
        id: 3,
        age: 30,
        gender: '男',
        create_at: '2022-01-03 12:00:00',
        status: '已完成',
        reason: '我是申请理由'
      }
    ]
  }
  applications.value = applicationDate.data;
  // 获取申请列表
  // const fetchApplications = async () => {
  //   try {
  //     const response = await getMyApplications();
  //     applications.value = response.applications;
  //   } catch (error) {
  //     console.error('获取申请列表失败:', error);
  //   }
  // };
  
  // 组件挂载时获取申请列表
  // onMounted(() => {
  //   fetchApplications();
  // });
  </script>
  
  <style scoped>
  /* 页面的特定样式 */
  </style>