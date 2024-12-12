<template>
    <div class="view-applications">
      <v-row justify="center" class="mb-5">
        <v-col cols="12" md="8" class="text-center">
          <h1 class="Activity_title font-weight-bold mb-4">我的活动</h1>
        </v-col>
      </v-row>
      <v-container>
        <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
        <v-row>
          <v-col cols="12" md="12" justify="center">
            <img src="@/assets/apply.png" alt="logo" width="20%">
          </v-col>
          <v-col v-if="dataLoaded" v-for="application in applications" :key="application.id" cols="6" md="4">
            <v-card style="border: 2px solid #d1e9f4; border-radius: 10px;" class="pa-4">
              <v-card-title class="headline">{{ application.status }}</v-card-title>
              <v-card-subtitle>活动名称: {{ activitys[application.activity_id].title }}</v-card-subtitle>
              <v-card-subtitle>活动地点: {{ activitys[application.activity_id].location }}</v-card-subtitle>
              <v-card-subtitle>活动时间: {{ activitys[application.activity_id].starts_at }} - {{ activitys[application.activity_id].ends_at }}</v-card-subtitle>
              <v-card-subtitle>报名时间: {{ application.created_at }}</v-card-subtitle>
              <v-card-text v-if="application.status === 'pending'"  class="d-flex justify-center">
                <v-btn  color="#fcedbe" @click="acceptApplication(application)" >通过</v-btn>
                <v-btn  color="#d1e9f4" class="ml-2" @click="rejectApplication(application)" >退回</v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue';
import { getMyApplications, updateApplicationStatus } from '@/api/volunteer';
import { getProfileByAdmin, getActivityByAdmin } from '@/api/user';
import snackbar from '@/api/snackbar';
const applications = ref([]);
const users = {};
const activitys = {};
const dataLoaded  = ref(false)

onMounted(async() => {
await fetchMyApplications();
})

const fetchMyApplications = async () => {
    try {
        const response = await getMyApplications();
        console.error(response)
        if (response) {
            applications.value = response;
            for (const application of applications.value) {
                const activity = await getActivityByAdmin(application.activity_id);
                activitys[application.activity_id] = activity;
            }
            dataLoaded.value = true;
        } else {
            console.error('获取报名列表失败:', response.message);
        }
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
.Activity_title {
  font-size: 30px;
  color: #3b3b3b; /* White color for subtitle */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); /* Strong shadow for readability */
}
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