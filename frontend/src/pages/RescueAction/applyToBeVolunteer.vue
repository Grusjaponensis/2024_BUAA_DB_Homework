<template>
    <v-container>
      <v-btn color="#d1e9f4" @click="$router.push('/RescueAction/rescueAction')"><v-icon left>mdi-arrow-left</v-icon>返回</v-btn>
      <v-card class="mx-auto" max-width="600">
        <v-card-title class="headline">申请成为志愿者</v-card-title>
        <v-card-text>
          <v-form ref="volunteerForm">
            <v-text-field
              v-model="applicant.name"
              label="姓名"
              required
            ></v-text-field>
  
            <v-text-field
              v-model="applicant.age"
              type="number"
              label="年龄"
              required
              :rules="[rules.age]"
            ></v-text-field>
  
            <v-select
              v-model="applicant.gender"
              label="性别"
              :items="['男', '女']"
              required
            ></v-select>
  
            <v-textarea
              v-model="applicant.reason"
              label="申请理由"
              required
            ></v-textarea>
  
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="primary" @click="submitApplicationForm">提交申请</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>

<script setup>
import { ref } from 'vue';
import { submitApplication } from '@/api/volunteer'; 
import snackbar from '@/api/snackbar';

const rules = {
  age: value => {
    return value > 0 ? true : '年龄必须大于0';
  }
};

const volunteerForm = ref(null);
const applicant = ref({
  name: '',
  age: null,
  gender: '',
  reason: '',
  status: '待审核'
});

const submitApplicationForm = async () => {
  try {
    if (applicant.value.name === '' ) {
      snackbar.error('请填写姓名');
      return;
    }
    if (applicant.value.age === null ) {
      snackbar.error('请填写年龄');
      return;
    }
    if (applicant.value.age < 0 ) {
      snackbar.error('年龄必须大于0');
      return;
    }
    if (applicant.value.gender === '' ) {
      snackbar.error('请选择性别');
      return;
    }
    if (applicant.value.reason === '' ) {
      snackbar.error('请填写申请理由');
      return;
    }
    await submitApplication(applicant.value);
    console.log('申请提交成功');
    snackbar.success('申请提交成功');
  } catch (error) {
    console.error('申请提交失败:', error);
    snackbar.error('申请提交失败');
  }
};
</script>