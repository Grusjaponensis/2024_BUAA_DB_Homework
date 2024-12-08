<template>
    <v-container>
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
          <v-btn color="primary" @click="submitApplication">提交申请</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </template>

<script setup>
import { ref } from 'vue';
import { submitApplication } from '@/api/volunteer'; 

const volunteerForm = ref(null);
const applicant = ref({
  name: '',
  age: null,
  gender: '',
  reason: '',
  status: '待审核'
});

const submitApplication = async () => {
  if (volunteerForm.value.validate()) {
    try {
      await submitApplication(applicant.value);
      console.log('申请提交成功');
    } catch (error) {
      console.error('申请提交失败:', error);
    }
  }
};
</script>