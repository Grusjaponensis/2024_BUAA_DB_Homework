<template>
<v-container>
    <v-card class="mx-auto" max-width="600">
      <v-card-title class="headline">创建新的志愿活动</v-card-title>
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
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { createActivity } from '@/api/activity';
import { useRouter } from 'vue-router';
import snackbar from '@/api/snackbar';

const rules = {
  people: value => {
    return value > 0 ? true : '志愿者人数必须大于0';
  }
}

const router = useRouter();

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

const menu = ref(false); 

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
    } catch (error) {
      console.error('活动提交失败:', error);
      snackbar.error('活动提交失败');
    }
  }
};
</script>