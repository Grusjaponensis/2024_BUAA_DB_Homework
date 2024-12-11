<template>
  <div class="view-applications">
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-row>
        <v-col cols="12" md="12" justify="center">
          <img src="@/assets/apply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-for="application in applications" :key="application.id" cols="12" md="4">
          <v-card style="border: 2px solid #d1e9f4; border-radius: 10px;">
            <v-card-title class="headline">{{ application.status }} 申请</v-card-title>
            <v-card-subtitle>基本信息: {{ application.name }} - {{ application.age }} - {{ application.gender }}</v-card-subtitle>
            <v-card-subtitle>申请状态: {{ application.status }}</v-card-subtitle>
            <v-card-subtitle>申请时间: {{ application.created_at }}</v-card-subtitle>
            <v-card-text>申请理由: {{ application.reason }}</v-card-text>
            <v-card-text v-if="application.status === '待审核'"  class="d-flex justify-space-between">
              <v-btn  color="#fcedbe" @click="acceptApplication(application)" >通过</v-btn>
              <v-btn  color="#d1e9f4" @click="rejectApplication(application)" >退回</v-btn>
            </v-card-text>
            <v-card-text v-if="application.status === '已通过' || application.status === '已退回'"  class="d-flex justify-space-between">
              <v-btn  color="grey" :disabled="true" class="me-8">通过</v-btn>
              <v-btn  color="grey" :disabled="true" class="ms-8">退回</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
  </template>

<script setup>
import { ref, onMounted } from 'vue';
import { getApplications, updateApplicationStatus } from '@/api/volunteer';
import snackbar from '@/api/snackbar';
const applications = ref([]);

onMounted(async() => {
  await fetchApplications();
})

const fetchApplications = async () => {
  try {
    const response = await getApplications();
    applications.value = response.data;
  } catch (error) {
    console.error('获取申请列表失败:', error);
  }
};

const acceptApplication = async (application) => {
  try {
    await updateApplicationStatus(application.id, '已通过');
    application.status = '已通过';
    snackbar.success('接受申请成功');
  } catch (error) {
    console.error('接受申请失败:', error);
    snackbar.error('接受申请失败');
  }
};

const rejectApplication = async (application) => {
  try {
    await updateApplicationStatus(application.id, '已退回');
    application.status = '已退回';
    snackbar.success('退回申请成功');
  } catch (error) {
    console.error('退回申请失败:', error);
    snackbar.error('退回申请失败');
  }
};
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
.view-applications {
  background-color: #f0f0f0;
  height: 100%;
}
</style>