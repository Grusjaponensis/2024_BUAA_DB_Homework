<template>
    <v-container>
      <v-row>
        <v-col v-for="application in applications" :key="application.id" cols="12" md="4">
          <v-card>
            <v-card-title class="headline">{{ application.status }} 申请</v-card-title>
            <v-card-subtitle>基本信息: {{ application.name }} - {{ application.age }} - {{ application.gender }}</v-card-subtitle>
            <v-card-subtitle>申请状态: {{ application.status }}</v-card-subtitle>
            <v-card-subtitle>申请时间: {{ application.created_at }}</v-card-subtitle>
            <v-card-text>申请理由: {{ application.reason }}</v-card-text>
            <v-card-text v-if="application.status === '待审核'">
              <v-btn  color="primary" @click="acceptApplication(application)" class="me-4">通过</v-btn>
              <v-btn  color="primary" @click="rejectApplication(application)" class="ms-4">退回</v-btn>
            </v-card-text>
            <v-card-text v-if="application.status === '已通过' || application.status === '已退回'">
              <v-btn  color="grey" :disabled="true" class="me-4">通过</v-btn>
              <v-btn  color="grey" :disabled="true" class="ms-4">退回</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script setup>
import { ref, onMounted } from 'vue';
import { getApplications, updateApplicationStatus } from '@/api/volunteer';

const applications = ref([]);

// 模拟数据
const applicationDate = {
    data: [
        {
            id: 1,
            name: '张三',
            gender: '男',
            age: 20,
            reason: '我想做义工',
            status: '待审核'
        },
        {
            id: 2,
            name: 'xiaoming',
            gender: '女',
            age: 25,
            reason: '我想做志愿者',
            status: '已通过'
        },
        {
            id: 3,
            name: '王五',
            gender: '男',
            age: 30,
            reason: '我想做志愿者',
            status: '已退回'
        }
    ]
}
applications.value = applicationDate.data;
// const fetchApplications = async () => {
//   try {
//     const response = await getApplications();
//     applications.value = response.data;
//   } catch (error) {
//     console.error('获取申请列表失败:', error);
//   }
// };

const acceptApplication = async (application) => {
  try {
    await updateApplicationStatus(application.id, '已通过');
    application.status = '已通过';
  } catch (error) {
    console.error('接受申请失败:', error);
  }
};

const rejectApplication = async (application) => {
  try {
    await updateApplicationStatus(application.id, '已退回');
    application.status = '已退回';
  } catch (error) {
    console.error('退回申请失败:', error);
  }
};

// onMounted(fetchApplications);
</script>

<style scoped>
.headline {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}
.btn-container {
  display: flex;
  justify-content: center;
}
</style>