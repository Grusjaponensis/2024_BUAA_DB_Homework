<template>
    <v-container>
      <v-card class="mx-auto" max-width="400">
        <v-card-title class="headline">添加猫咪</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submitForm">
            <v-text-field
              v-model="cat_in.name"
              label="猫咪姓名"
              required
            ></v-text-field>
            <v-select
              v-model="cat_in.is_male"
              :items="['male', 'female']"
              label="猫咪性别"
              required
            ></v-select>
            <v-text-field
              v-model="cat_in.age"
              type="number"
              label="猫咪年龄"
              required
            ></v-text-field>
            <v-text-field
              v-model="cat_in.health_condition"
              type="number"
              label="猫咪健康状况"
              required
            ></v-text-field>
            <!-- <v-text-field
              v-model="cat_in.breed"
              label="猫咪品种"
              required
            ></v-text-field> -->
            <v-textarea
              v-model="cat_in.description"
              label="对猫咪的描述"
              counter="50"
              required
            ></v-textarea>
            <!-- <v-file-input
              v-model="cat_in.photo"
              label="猫咪照片"
              multiple
              required
            ></v-file-input> -->
            <!-- <v-text-field
              v-model="location_in.longitude"
              type="number"
              label="猫咪经度"
              required
            ></v-text-field>
            <v-text-field
              v-model="location_in.latitude"
              type="number"
              label="猫咪纬度"
              required
            ></v-text-field> -->
            <v-btn
              color="primary"
              type="submit"
              :disabled="!formIsValid"
            >
              加入猫咪大军
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-container>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import {createCat} from '@/api/cat';
  import snackbar from '@/api/snackbar';
  const cat_in = ref({
    name: '',
    is_male: null,
    age: null,
    health_condition: null,
    description: '',
  });
  const location_in = ref({
    longitude: 10,
    latitude: 10,
  });
  
  const form = ref(null);
  
  // 表单是否有效
  const formIsValid = computed(() => {
    return cat_in.value.name !== '' && cat_in.value.age !== null && cat_in.value.is_male !== null && cat_in.value.health_condition !== null && cat_in.value.description !== '';
  });
  // 提交表单
  const submitForm = async () => {
    try {
      const data = {
      cat_in: {
        name: cat_in.value.name,
        is_male: cat_in.value.is_male === 'male', 
        age: parseInt(cat_in.value.age, 10),
        health_condition: parseInt(cat_in.value.health_condition, 10),
        description: cat_in.value.description,
      },
      location_in: {
        longitude: parseFloat(location_in.value.longitude),
        latitude: parseFloat(location_in.value.latitude),
      }
    };
      const response = await createCat(data);
      console.log('提交猫咪信息：', response);
      // 提交后重置表单
      cat_in.value = {
        name: '',
        age: null,
        is_male: null,
        health_condition: null,
        description: '',
      };
      snackbar.success('提交成功！');
    } catch (error) {
      console.error('添加猫咪失败:', error);
      snackbar.error('提交失败，请检查输入是否正确');
    }
  };
  </script>
  
  <style scoped>
  /* 针对 addCat 页面的特定样式 */
  </style>