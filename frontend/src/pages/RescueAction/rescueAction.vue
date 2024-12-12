<template>
<v-container>
      <!-- 顶部欢迎横栏 -->
      <v-toolbar  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-3' :'#fcedbe'" dark class="top-bar">
        <v-toolbar-title v-if="user.is_volunteer || user.is_superuser">
          Hello，{{ user.nickname }}，欢迎来到救助中心，和我们一起帮助猫猫吧！
        </v-toolbar-title>
        <v-toolbar-title v-if="!user.is_volunteer && !user.is_superuser">
          Hello，{{ user.nickname }}，报名成为志愿者，和我们一起帮助猫猫吧！
        </v-toolbar-title>
      </v-toolbar>

      <v-container>
      <!-- 侧边栏（包含按钮） -->
      <v-row class="mb-4" no-gutters>
        <v-col cols="3" class="sidebar">
          <!-- 分析数据栏 -->
            <v-card variant="outlined" class="mt-5">
              <v-card-text class="pa-4">
                <div class="d-flex flex-column align-start">
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">志愿者总数： </span>
                    <span class="font-weight-bold ml-auto">352{{ totalPosts }}</span>
                  </div>
                  <div class="d-flex align-start">
                    <span class="body-2 mb-2">组织救助行动： </span>
                    <span class="font-weight-bold ml-auto">352{{ totalPosts }}次</span>
                  </div>
                </div>
              </v-card-text>
            </v-card>
              <!-- 按钮组 -->
              <div  class="d-flex flex-column mt-5" v-if="user.login">
                <v-btn
                  v-if="!user.is_volunteer && !user.is_superuser"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' :'orange-darken-1'"
                  @click="applyToBeVolunteer"
                >
                  <v-icon class="mr-1">mdi-pencil</v-icon>
                  申请成为志愿者
                </v-btn>
                
                <v-btn
                  v-if="!user.is_volunteer && !user.is_superuser"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' :'orange-darken-3'"
                  @click="myApplications"
                >
                  <v-icon class="mr-1">mdi-cat</v-icon>
                  申请进度查询
                </v-btn>

                <v-btn
                  v-if="user.is_volunteer"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' :'pink-lighten-2'"
                  @click="myActivities"
                >
                  <v-icon class="mr-1">mdi-heart</v-icon>
                  我的活动
                </v-btn>

                <v-btn
                  v-if="user.is_superuser"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' : 'red-lighten-2'"
                  to="/RescueAction/myApplications"
                >
                  <v-icon class="mr-1">mdi-pencil</v-icon>
                  志愿者申请
                </v-btn>

                <v-btn
                  v-if="user.is_superuser"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' : 'yellow-darken-3'"
                  @click="viewApplications"
                >
                  <v-icon class="mr-1">mdi-heart</v-icon>
                  查看报名
                </v-btn>

                <v-btn
                  v-if="user.is_superuser"
                  class="my-1"
                  variant="outlined"
                  block
                  :color="$vuetify.theme.name === 'dark' ? 'orange-lighten-4' :'yellow-darken-2'"
                  @click = "showAddActionDialog = true"
                >
                  <v-icon class="mr-1">mdi-tag</v-icon>
                  添加活动
                </v-btn>
                <!-- <span class="caption" v-if="user.is_superuser">添加活动</span> -->
              </div>
          <v-img src="@/assets/rescue.png" />
        </v-col>

        <v-col cols="9" class="main-content" v-if="loaded">
          <v-row>
            <v-col cols="6" v-for="activity in activities" :key="activity.id">
              <!-- 主内容区域 -->
              <v-card class="pa-1 mb-4 rounded-lg">
                <template #append>
                  <v-chip
                    :color= "$vuetify.theme.name === 'dark' ? 'grey-lighten-1' :'grey-darken-2'"
                    prepend-icon="mdi-clock-outline"
                    class="ma-1"
                  >
                    请关注活动时间
                  </v-chip>
                </template>
                <template #title>{{ activity.title }}</template>
                <v-card-subtitle class="mb-2">需要志愿者: {{ activity.current_participants }}/{{ activity.max_participants }}</v-card-subtitle>
                <v-card-subtitle class="mb-2">活动地点: {{ activity.location }}</v-card-subtitle>
                <v-card-subtitle class="mb-2">行动时间: {{ new Date(activity.starts_at).toLocaleString() }} - {{ new Date(activity.ends_at).toLocaleString() }}</v-card-subtitle>
                <v-card-subtitle class="mb-2">报名时段: {{ new Date(activity.signup_starts_at).toLocaleString() }} - {{ new Date(activity.signup_ends_at).toLocaleString() }}</v-card-subtitle>
                <v-card-text>{{ activity.description }}</v-card-text>
                <v-card-text v-if="(user.is_volunteer || user.is_superuser)">
                  <v-btn v-if="user.is_volunteer" :disabled="!canSignUp(activity)" :color="$vuetify.theme.name === 'dark' ? 'orange-accent-1' : '#f7cf83'" @click="signUpActivity(activity)">
                    {{ button_text[activity.id] }}
                  </v-btn>
                  <v-btn v-if="user.is_volunteer" :disabled="!canWithdraw(activity)" :color="$vuetify.theme.name === 'dark' ? 'orange-accent-1' : '#fad6b5'" @click="withdrawActivity(activity)">
                    退选
                  </v-btn>
                  <v-btn v-if="user.is_superuser" :color="$vuetify.theme.name === 'dark' ? 'orange-accent-1' : 'deep-orange-lighten-3'" @click="showDeleteDialog = true; deleteId = activity.id">
                    删除
                  </v-btn>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-col>

      </v-row>
      </v-container>

      <v-dialog v-model="showDeleteDialog" max-width="500px">
        <v-card>
          <v-card-title class="headline">
            确认删除
          </v-card-title>
          <v-card-text>
            确认要删除该活动吗？此操作不可恢复。
          </v-card-text>
          <v-card-actions>
            <v-btn  color="green" @click = "showDeleteDialog = false"> 取消</v-btn>
            <v-btn  color="red" @click = "removeActivity(deleteId)"> 确认</v-btn>
          </v-card-actions>
        </v-card>
    </v-dialog>
  </v-container>
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
        <v-btn  :color="primary" @click="submitactivity" :disabled="!isFormValid">创建活动</v-btn>
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
import { getMyRegistrations } from '@/api/volunteer';

const router = useRouter();
const showDeleteDialog = ref(false);
const showAddActionDialog = ref(false);

const activities = ref([]);
const deleteId = ref(0);
const applications = ref([]);
const button_text = {};
const loaded = ref(false);

onMounted(async() => {
  await fetchProfile();
  await fetchactivities();
  await fetchMyApplications();
  loaded.value = true;
});

const fetchMyApplications = async () => {
  try {
    const response = await getMyRegistrations();
    applications.value = response;
    for (const activity of activities.value) {
      button_text[activity.id] = applications.value.some(p => p.activity_id === activity.id) ? '已报名' : '报名';
      console.error("activity " + activity);
    }
    console.log("获取我的报名信息成功:", applications.value);
  } catch (error) {
    console.error('获取我的报名信息失败:', error);
  }
};

const myActivities = () => {
  if (!user.login) {
    router.push('/login');
    snackbar.warning('请先登录');
    return;
  } else {
    router.push('/RescueAction/myActivities');
  }
}

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

const viewApplications = () => {
  if (!user.login) {
    router.push('/login');
    snackbar.warning('请先登录');
    return;
  } else {
    router.push('/RescueAction/viewApplications');
  }
};

const fetchProfile = async () => {
  try {
    await getProfile();
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
    await signUp(activity.id , user.id);
    // 更新活动列表状态
    await fetchactivities();
    await fetchMyApplications();
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
    await fetchactivities();
    await fetchMyApplications();
    snackbar.success('退选成功');
  } catch (error) {
    console.error('退选失败:', error);
    snackbar.error('退选失败');
  }
};

const canSignUp = (activity) => {
  // 是否可以报名
  const condition1 = activity.max_participants > activity.current_participants;
  const condition2 = !applications.value.some(p => p.activity_id === activity.id);
  return condition1 && condition2;
};

const canWithdraw = (activity) => {
  // 是否可以退选
  // console.log("canWithdraw", applications.value)
  // console.log("canWithdraw", applications.value.some(p => p.activity_id === activity.id))
  // console.log("canWithdraw", applications.value.some(p => p.activity_id === activity.id && p.status === 'pending'))
  return applications.value.some(p => p.activity_id === activity.id && p.status === 'pending');
};

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
      await fetchactivities();
      router.push('/RescueAction/rescueAction'); 
      showAddActionDialog.value = false;
    } catch (error) {
      console.error('活动提交失败:', error);
      snackbar.error('活动提交失败');
    }
  }
};
</script>

<style scoped>  

.sidebar {
  max-width: 200px; 
  margin-right: 30px;
}
.v-btn {
  margin-right: 6px;
} 

.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
</style>