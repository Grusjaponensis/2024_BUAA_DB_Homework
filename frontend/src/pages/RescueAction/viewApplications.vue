<template>
  <div class="view-applications">
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-row>
        <v-col cols="12" md="12" justify="center">
          <img src="@/assets/apply.png" alt="logo" width="20%">
        </v-col>
        <v-col v-for="application in applications" :key="application.id" cols="6" md="4">
          <v-card style="border: 2px solid #d1e9f4; border-radius: 10px;">
            <v-card-title class="headline">{{ application.status }} 报名</v-card-title>
            <v-card-subtitle>报名者ID: {{ application.user_id }}</v-card-subtitle>
            <v-card-subtitle>报名状态: {{ application.status }}</v-card-subtitle>
            <v-card-subtitle>报名时间: {{ application.created_at }}</v-card-subtitle>
            <v-card-text v-if="application.status === 'pending'"  class="d-flex justify-center">
              <v-btn  color="#fcedbe" @click="acceptApplication(application)" >通过</v-btn>
              <v-btn  color="#d1e9f4" class="ml-2" @click="rejectApplication(application)" >退回</v-btn>
            </v-card-text>
            <v-card-text v-if="application.status === 'approved' || application.status === 'rejected'"  class="d-flex justify-center">
              <v-btn  color="grey" :disabled="true" elevation="2">通过</v-btn>
              <v-btn  color="grey" :disabled="true" class="ml-2" elevation="2">退回</v-btn>
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
import { getProfileByAdmin } from '@/api/user';
import snackbar from '@/api/snackbar';
const applications = ref([]);

onMounted(async() => {
  await fetchApplications();
})

const fetchApplications = async () => {
  try {
    const response = await getApplications();
    applications.value = response;
    console.log('获取申请列表成功:', applications.value);
  } catch (error) {
    console.error('获取申请列表失败:', error);
  }
};

const acceptApplication = async (application) => {
  try {
    await updateApplicationStatus(application.activity_id, application.user_id, "approved");
    application.status = "approved";
    snackbar.success('通过报名成功');
  } catch (error) {
    console.error('通过报名失败:', error);
    snackbar.error('通过报名失败');
  }
};

const rejectApplication = async (application) => {
  try {
    await updateApplicationStatus(application.activity_id, application.user_id, 'rejected');
    application.status = 'rejected';
    snackbar.success('退回报名成功');
  } catch (error) {
    console.error('退回报名失败:', error);
    snackbar.error('退回报名失败');
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