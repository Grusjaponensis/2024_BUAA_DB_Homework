<template>
  <v-container>
    <v-container>
      <!-- 行动卡片 -->
      <v-row>
        <v-col v-for="activity in activities" :key="activity.id" cols="12" lg="6" md="12">
          <v-card>
            <v-card-title class="headline">{{ activity.title }}</v-card-title>
            <v-card-subtitle>需要志愿者: 0/{{ activity.max_participants }}</v-card-subtitle>
            <v-card-subtitle>活动地点: {{ activity.location }}</v-card-subtitle>
            <v-card-subtitle>行动时间: {{ activity.starts_at }} - {{ activity.ends_at }}</v-card-subtitle>
            <v-card-subtitle>报名时段: {{ activity.signup_starts_at }} - {{ activity.signup_ends_at }}</v-card-subtitle>
            <v-card-text>{{ activity.description }}</v-card-text>
            <v-card-text v-if="isVolunteer || isAdmin">
              <v-btn v-if="canSignUp(activity) && !isSignedUp(activity)" color="primary" @click="signUpActivity(activity)">报名</v-btn>
              <v-btn v-if="canSignUp(activity) && isSignedUp(activity)" color="primary" @click="withdrawActivity(activity)">退选</v-btn>
              <v-btn v-if="isAdmin" color="red-lighten-1" @click="showDeleteDialog = true; deleteId = activity.id" >删除</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <v-row justify="center" class="text-center" no-gutters>
      <v-row v-if="!isVolunteer && !isAdmin" justify="end" no-gutters>
        <v-btn
          color="primary"
          @click = applyToBeVolunteer
        >
          申请成为志愿者
        </v-btn>
        <v-btn
          color="primary"
          class="mx-4"  
          @click = myApplications
        >
          申请进度查询
        </v-btn>
      </v-row>

      <v-row v-if="isAdmin" justify="end" no-gutters>
        <v-btn
          color="primary"
          to="/RescueAction/viewApplications"
        >
          查看申请
        </v-btn>
      </v-row>
    </v-row>
    <v-dialog v-model="showDeleteDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">
            确认删除
          </v-card-title>
          <v-card-text>
            确认要删除该活动吗？此操作不可恢复。
          </v-card-text>
          <v-card-actions>
            <v-btn color="green" @click = "showDeleteDialog = false"> 取消</v-btn>
            <v-btn color="red" @click = "removeActivity(deleteId)"> 确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-container>
  <v-btn
      color="blue-accent-2"
      class="elevation-4"
      style="position: fixed; bottom: 24px; right: 24px;"
      size="large"
      @click = "showAddActionDialog = true"
    >
    <v-icon>mdi-plus</v-icon>
    </v-btn>
  <v-dialog v-model="showAddActionDialog" 
    max-width="80vw"
    width="750px">
    <v-toolbar title = "添加志愿活动">
      <v-btn icon="mdi-close" @click="showAddActionDialog = false"></v-btn>
    </v-toolbar>
    <v-card>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="activity.name"
            label="活动名称"
            required
          ></v-text-field>

          <v-text-field
            v-model="activity.location"
            label="活动地点"
            required
          ></v-text-field>

          <v-text-field
            v-model="activity.volunteerCount"
            type="number"
            label="活动所需志愿者人数"
            required
            :rules = "[rules.people]"
          ></v-text-field>
          
          <v-textarea
            v-model="activity.description"
            label="活动说明（详情）"
            required
          ></v-textarea>

          <v-col>
            <label for="activity-date">活动开始时间：</label>
            <input
                type="datetime-local"
                id="activity-date"
                class="input-time-picker"
                v-model="activity.startTime"
                required
            />
            <label for="activity-date">活动结束时间：</label>
            <input
                type="datetime-local"
                id="activity-date"
                class="input-time-picker"
                v-model="activity.endTime"
                required
            />
          </v-col>
          <v-col>
            <label for="activity-date">报名开始时间：</label>
            <input
                type="datetime-local"
                id="activity-date"
                class="input-time-picker"
                v-model="activity.signupStartTime"
                required
            />
            <label for="activity-date">报名结束时间：</label>
            <input
                type="datetime-local"
                id="activity-date"
                class="input-time-picker"
                v-model="activity.signupEndTime"
                required
            />
          </v-col>
        </v-form>
      </v-card-text>
      <v-card-actions class="d-flex justify-center" padding="4">
        <v-btn color="primary" @click="submitactivity" :disabled="!isFormValid">创建活动</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
  
<script setup>
import { ref, computed, onMounted } from 'vue';
import { getActivities, deleteActivity, signUp, withdraw , createActivity } from '@/api/activity';
import { getProfile } from '@/api/user';
import snackbar from '@/api/snackbar';
import { user } from '@/api/user';
import { useRouter } from 'vue-router';

const router = useRouter();
const showDeleteDialog = ref(false);
const showAddActionDialog = ref(false);

const activities = ref([]);
const deleteId = ref(0);
const isVolunteer = ref(false);
const isAdmin = ref(false);

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
    activities.value = response;
    console.log("获取行动信息成功:", response);
  } catch (error) {
    console.error('获取行动信息失败:', error);
  }
};

const removeActivity = async (id) => {
  // 删除
  try {
    await deleteActivity(id);
    activities.value = activities.value.filter(p => p.id !== id);
    snackbar.success('删除成功');
    showDeleteDialog.value = false;
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
  fetchactivities();
  fetchProfile();
});


const rules = {
  people: value => {
    return value > 0 ? true : '志愿者人数必须大于0';
  }
}

const isFormValid = computed(() => {
  return (
    activity.value.name &&
    activity.value.location &&
    activity.value.volunteerCount &&
    activity.value.startTime &&
    activity.value.endTime &&
    activity.value.signupStartTime &&
    activity.value.signupEndTime &&
    activity.value.description
  );
});

const activity = ref({
  name: '',
  date: null,
  location: '',
  volunteerCount: null,
  startTime: null,
  endTime: null,
  signupStartTime: null,
  signupEndTime: null,
  description: '',
});

const submitactivity = async () => {
  if (isFormValid.value && activity.value) { 
    try {
      const data = {
        type: "rescue",
        title: activity.value.name,
        description: activity.value.description,
        location: activity.value.location,
        starts_at: activity.value.startTime,
        ends_at: activity.value.endTime,
        signup_starts_at: activity.value.signupStartTime,
        signup_ends_at: activity.value.signupEndTime,
        max_participants: activity.value.volunteerCount,
      }
      if (data.max_participants <= 0) {
        snackbar.error('志愿者人数必须大于0');
        return;
      }
      if (data.starts_at >= data.ends_at) {
        snackbar.error('活动开始时间必须早于活动结束时间');
        return;
      }
      if (data.signup_starts_at >= data.signup_ends_at) {
        snackbar.error('报名开始时间必须早于报名结束时间');
        return;
      }

      const response = await createActivity(data);
      console.log('活动提交成功', response);
      snackbar.success('活动提交成功');
      router.push('/RescueAction/rescueAction'); 
      showAddActionDialog.value = false;
    } catch (error) {
      console.error('活动提交失败:', error);
      snackbar.error('活动提交失败');
    }
  }
};
</script>