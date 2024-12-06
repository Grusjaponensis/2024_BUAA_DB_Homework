<template>
    <v-container>
      <v-card class="mx-auto" max-width="400">
        <v-card-title class="headline">添加猫咪</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submitForm">
            <v-text-field
              v-model="cat.name"
              label="猫咪姓名"
              required
            ></v-text-field>
            <v-text-field
              v-model="cat.age"
              type="number"
              label="猫咪年龄"
              required
            ></v-text-field>
            <v-text-field
              v-model="cat.breed"
              label="猫咪品种"
              required
            ></v-text-field>
            <v-textarea
              v-model="cat.temperament"
              label="对猫咪的描述"
              counter="50"
              required
            ></v-textarea>
            <v-file-input
              v-model="cat.photo"
              label="猫咪照片"
              multiple
              required
            ></v-file-input>
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
  
  const cat = ref({
    name: '',
    age: null,
    breed: '',
    temperament: '',
    photo: '',
  });
  
  const form = ref(null);
  
  // 表单是否有效
  const formIsValid = computed(() => {
    return cat.value.name && cat.value.age && cat.value.breed && cat.value.temperament && cat.value.photo;
  });
  
  // 提交表单
  const submitForm = async () => {
    try {
      //await addCatAPI(cat.value);
      console.log('提交猫咪信息：', cat.value);
      // 提交后重置表单
      cat.value = {
        name: '',
        age: null,
        breed: '',
        temperament: '',
        photo: '',
      };
    } catch (error) {
      console.error('添加猫咪失败:', error);
    }
  };
  </script>
  
  <style scoped>
  /* 针对 addCat 页面的特定样式 */
  </style>