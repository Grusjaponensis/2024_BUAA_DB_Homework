<template>
<v-container>
      <!-- 顶部欢迎横栏 -->
      <v-toolbar color='#fcedbe' dark class="top-bar">
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
        <v-col cols="12" md="3" class="sidebar">
          <!-- 分析数据栏 -->
            <v-card elevation="4" class="mb-4">
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
          <v-card elevation="4"  v-if="user.is_superuser || !user.is_volunteer">
            <v-card-text class="pa-4">
              <!-- 按钮组 -->
              <div class="d-flex flex-column align-center">
                <v-btn
                  v-if="!user.is_volunteer && !user.is_superuser"
                  fab
                  dark
                  rounded
                  color=#f7cf83
                  @click="applyToBeVolunteer"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
                <span class="caption" v-if="!user.is_volunteer && !user.is_superuser">申请成为志愿者</span>
                
                <v-btn
                  v-if="!user.is_volunteer && !user.is_superuser"
                  fab
                  dark
                  rounded
                  color=#f8c9d5
                  @click="myApplications"
                >
                  <v-icon>mdi-cat</v-icon>
                </v-btn>
                <span class="caption" v-if="!user.is_volunteer && !user.is_superuser">申请进度查询</span>
                
                <v-btn
                  v-if="user.is_superuser"
                  fab
                  dark
                  rounded
                  color=#f8c9d5
                  @click="viewApplications"
                >
                  <v-icon>mdi-heart</v-icon>
                </v-btn>
                <span class="caption" v-if="user.is_superuser">查看申请</span>

                <v-btn
                  v-if="user.is_superuser"
                  fab
                  dark
                  rounded
                  color=#f7cf83
                  @click = "showAddActionDialog = true"
                >
                  <v-icon>mdi-tag</v-icon>
                </v-btn>
                <span class="caption" v-if="user.is_superuser">添加活动</span>
              </div>
            </v-card-text>
          </v-card>
          <v-img src="@/assets/rescue.png" />
        </v-col>

        <v-col cols="12" md="9">
        <!-- 主内容区域 -->
        <v-col v-for="activity in activities" :key="activity.id" >
          <v-card style="background-color: #fbf1d7; border: 2px solid #f7cf83;" >
            <v-card-title class="headline">{{ activity.title }}</v-card-title>
            <v-card-subtitle>需要志愿者: 0/{{ activity.max_participants }}</v-card-subtitle>
            <v-card-subtitle>活动地点: {{ activity.location }}</v-card-subtitle>
            <v-card-subtitle>行动时间: {{ activity.starts_at }} - {{ activity.ends_at }}</v-card-subtitle>
            <v-card-subtitle>报名时段: {{ activity.signup_starts_at }} - {{ activity.signup_ends_at }}</v-card-subtitle>
            <v-card-text>{{ activity.description }}</v-card-text>
            <v-card-text v-if="user.is_volunteer || user.is_superuser">
              <v-btn v-if="user.is_volunteer" :disabled="!canSignUp(activity)" color="#f7cf83" @click="signUpActivity(activity)">报名</v-btn>
              <!-- <v-btn v-if="user.is_volunteer" :disabled="!isSignedUp(activity)" color="#fad6b5" @click="withdrawActivity(activity)">退选</v-btn> -->
              <v-btn v-if="user.is_superuser" color="red-lighten-1" @click="showDeleteDialog = true; deleteId = activity.id" >删除</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
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
            <v-btn color="green" @click = "showDeleteDialog = false"> 取消</v-btn>
            <v-btn color="red" @click = "removeActivity(deleteId)"> 确认</v-btn>
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
import { getMyApplications } from '@/api/volunteer';

const router = useRouter();
const showDeleteDialog = ref(false);
const showAddActionDialog = ref(false);

const activities = ref([]);
const deleteId = ref(0);
const applications = ref([]);

onMounted(() => {
  fetchactivities();
  fetchProfile();
  fetchMyApplications();
});

const fetchMyApplications = async () => {
  try {
    const response = await getMyApplications();
    applications.value = response;
    console.log("获取我的报名信息成功:", applications.value);
  } catch (error) {
    console.error('获取我的报名信息失败:', error);
  }
};

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
const username = ref('');
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
    const updatedActivity = await getActivities();
    activities.value = updatedActivity;
    const updatedApplication = await getMyApplications();
    applications.value = updatedApplication;
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
  const condition1 = activity.max_participants > activity.current_participants;
  const condition2 = !applications.value.some(p => p.activity_id === activity.id);
  return condition1 && condition2;
};

const isSignedUp = (activity) => {
  // 是否已经报名
  return applications.value.some(p => p.activity_id === activity.id);
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
      fetchactivities();
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
/* 美化帖子卡片 */
.card {
  border-radius: 10px; /* 圆角 */
  transition: transform 0.3s ease-in-out; /* 平滑变换 */
  background-color: #f0f0f0; /* 背景色 */
  padding: 10px; /* 内边距 */
  margin-bottom: 20px; /* 外边距 */
  cursor: pointer; /* 鼠标指针 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 阴影 */

}

.card:hover {
  transform: translateY(-5px); /* 鼠标悬停时上移 */
}

/* 美化操作按钮 */
.v-btn {
  transition: background-color 0.3s ease-in-out; /* 背景色渐变 */
}

.v-btn:hover {
  background-color: #e0e0e0; /* 鼠标悬停时的背景色 */
}

.sidebar {
  max-width: 200px; 
  margin-right: 30px;
}
.v-btn {
  border-radius: 25%; 
  width: 40px; 
  height: 40px; 
  margin-right: 6px;
}

.top-bar {
  border-radius: 8px; /* 设置圆角 */
  margin-bottom:10px; /* 设置底部间距 */
  padding: 1px 1px; /* 设置内边距 */
}
</style>