<template>
  <v-container>
    <v-container>
      <!-- 行动卡片 -->
      <v-row>
        <v-col v-for="activity in activities" :key="activity.id" cols="12" md="4">
          <v-card>
            <v-card-title class="headline">{{ activity.title }}</v-card-title>
            <v-card-subtitle>需要志愿者: {{ activity.volunteersSignedUp }}/{{ activity.volunteerNeeded }}</v-card-subtitle>
            <v-card-subtitle>行动时间: {{ activity.startTime }} - {{ activity.endTime }}</v-card-subtitle>
            <v-card-subtitle>行动地点: {{ activity.activityLocation }}</v-card-subtitle>
            <v-card-subtitle>报名时段: {{ activity.signupStartTime }} - {{ activity.signupEndTime }}</v-card-subtitle>
            <v-card-text>{{ activity.description }}</v-card-text>
            <v-card-text v-if="isVolunteer || isAdmin">
              <v-btn v-if="canSignUp(activity) && !isSignedUp(activity)" color="primary" @click="signUpActivity(activity)">报名</v-btn>
              <v-btn v-if="canSignUp(activity) && isSignedUp(activity)" color="primary" @click="withdrawActivity(activity)">退选</v-btn>
              <v-btn v-if="isAdmin" color="grey" @click="removeActivity(activity)" >删除</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-footer padless>
      <v-row v-if="!isVolunteer && !isAdmin" justify="end" no-gutters>
        <v-btn
          fab
          dark
          fixed
          bottom
          right
          color="primary"
          @click = applyToBeVolunteer
        >
          申请成为志愿者
        </v-btn>
        <v-btn
          fab
          dark
          fixed
          bottom
          right
          color="primary"
          class="mx-4"  
          @click = myApplications
        >
          申请进度查询
        </v-btn>
      </v-row>

      <v-row v-if="isAdmin" justify="end" no-gutters>
        <v-btn
          fab
          dark
          fixed
          bottom
          right
          color="primary"
          to="/RescueAction/viewApplications"
        >
          查看申请
        </v-btn>
        <v-btn
          fab
          dark
          fixed
          bottom
          right
          color="primary"
          class="mx-4"  
          to="/RescueAction/createAction"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-row>
    </v-footer>
  </v-container>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue';
import { getActivities, deleteActivity, signUp, withdraw } from '@/api/activity';
import { getProfile } from '@/api/user';
import snackbar from '@/api/snackbar';
import { user } from '@/api/user';
import router from '@/router';
import { useRouter } from 'vue-router';

const router = useRouter();

const activities = ref([]);

const isVolunteer = ref(false);
const isAdmin = ref(false);

// 模拟数据
const activitiesData = {
  data: [
    { 
      id: 1,
      title: '清理路障',
      volunteerNeeded: 8,
      volunteersSignedUp: 3,
      startTime: '2024-01-01 10:00:00',
      endTime: '12:00:00',
      activityLocation: '校园中路',
      signupStartTime: '20224-01-01 09:00:00',
      signupEndTime: '11:00:00',
      description: '清理路障，为学生提供便利。',
    },
    { 
      id: 2,
      title: '清理垃圾',
      volunteerNeeded: 10,
      volunteersSignedUp: 5,
      startTime: '2024-01-02 10:00:00',
      endTime: '12:00:00',
      activityLocation: '绿园',
      signupStartTime: '2024-01-02 09:00:00',
      signupEndTime: '11:00:00',
      description: '清理垃圾，为学生提供便利。',
    },
  ],
};

activities.value = activitiesData.data;

const myApplications = () => {
  if (!user.login) {
    router.push('/login');
    snackbar.warning('请先登录');
    return;
  } else {
    router.push('/RescueAction/myApplications');
  }
}

const applyToBeVolunteer = () => {
  if (!user.login) {
    router.push('/login');
    snackbar.warning('请先登录');
    return;
  } else {
    router.push('/RescueAction/applyToBeVolunteer');
  }
};

const fetchProfile = async () => {
  try {
    const response = await getProfile();
    isVolunteer.value = response.data.is_volunteer === true;
    isAdmin.value = response.data.is_superuser === true;
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
};

const fetchactivities = async () => {
  try {
    const response = await getActivities();
    activities.value = response.data;
  } catch (error) {
    console.error('获取行动信息失败:', error);
  }
};

const removeActivity = async (activity) => {
  // 删除
  try {
    await deleteActivity(activity.id);
    activities.value = activities.value.filter(p => p.id !== activity.id);
    snackbar.success('删除成功');
  } catch (error) {
    console.error('删除活动失败:', error);
    snackbar.error('删除失败');
  }
};
const signUpActivity = async (activity) => {
  // 报名
  try {
    await signUp(activity.id);
    // 更新活动列表状态
    const updatedActivity = await getActivities();
    activities.value = updatedActivity;
    snackbar.success('报名成功');
  } catch (error) {
    console.error('报名失败:', error);
    snackbar.error('报名失败');
  }
};

const withdrawActivity = async (activity) => {
  // 退选
  try {
    await withdraw(activity.id);
    // 更新活动列表状态
    const updatedActivity = await getActivities();
    activities.value = updatedActivity;
    snackbar.success('退选成功');
  } catch (error) {
    console.error('退选失败:', error);
    snackbar.error('退选失败');
  }
};

const canSignUp = (activity) => {
  // 是否可以报名
  return activity.volunteerNeeded > activity.volunteersSignedUp;
};

const isSignedUp = (activity) => {
  // 是否已报名
  // const userId = store.getters.userId;
  // return activity.volunteers?.some(volunteer => volunteer.id === userId);
};

onMounted(() => {
  // 获取用户信息
  // const user = JSON.parse(localStorage.getItem('user'));
  // if (user) {
  //   isVolunteer.value = user.is_volunteer === true;
  //   isAdmin.value = user.is_superuser === true;
  // }
  // fetchactivities();
  fetchProfile();
});
</script>

<style>
</style>