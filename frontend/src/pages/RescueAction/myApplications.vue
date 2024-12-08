<template>
    <!-- 主内容区域 -->
    <v-container>
      <v-list>
        <v-list-item
          v-for="application in applications"
          :key="application.id"
          class="my-2"
        >
          <v-list-item-content>
            <v-list-item-title class="headline">申请情况</v-list-item-title>
            <v-list-item-subtitle>基本信息：{{ application.name }} - {{ application.age }} - {{ application.gender }}</v-list-item-subtitle>
            <v-list-item-subtitle class="grey--text">
              申请日期: {{ new Date(application.create_at).toLocaleString() }}
            </v-list-item-subtitle>
            <v-list-item-subtitle>
              状态: {{ application.status }}
            </v-list-item-subtitle>
            <v-list-item-subtitle style="margin-top: 10px;margin-bottom: 10px;">{{ application.reason }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
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